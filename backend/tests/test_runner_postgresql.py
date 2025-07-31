#!/usr/bin/env python3
"""
PostgreSQL Test Runner for SiteScanner Analysis
Uses the PostgreSQL views created in database/views/ directory
"""

import sys
import os
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from database import get_db_connection, test_connection
from typing import Dict, List, Any

class PostgreSQLTestRunner:
    """Test runner that uses PostgreSQL views for analysis"""
    
    def __init__(self, db_type: str = 'primary'):
        """Initialize test runner
        
        Args:
            db_type: Database type ('primary', 'development', 'testing')
        """
        self.db_type = db_type
        
    def _execute_view_query(self, view_name: str, limit: int = None) -> List[Dict[str, Any]]:
        """Execute a query against a PostgreSQL view
        
        Args:
            view_name: Name of the view to query
            limit: Optional limit on results
            
        Returns:
            List of result dictionaries
        """
        query = f"SELECT * FROM {view_name}"
        if limit:
            query += f" LIMIT {limit}"
            
        try:
            with get_db_connection(self.db_type) as db:
                return db.execute_query(query, fetch='all')
        except Exception as e:
            print(f"Error querying view {view_name}: {e}")
            return []
    
    def test_q1_navigation_paths(self):
        """Test Q1: Navigation paths from root to leaf nodes"""
        print("\n" + "="*60)
        print("TESTING Q1: What are all the navigation paths from root to leaf nodes?")
        print("="*60)
        
        # Query 1: Leaf nodes summary
        print("\n1. LEAF NODES SUMMARY:")
        print("-" * 25)
        results = self._execute_view_query("v_leaf_nodes_summary", limit=10)
        if results:
            print("Node Type        Leaf Status  Inbound Links")
            print("-" * 45)
            for row in results:
                print(f"{row['node_type']:<15} {row['leaf_status']:<12} {row['inbound_links']}")
        else:
            print("No data available (tables empty)")
        
        # Query 2: Path lengths analysis
        print("\n2. PATH LENGTHS ANALYSIS:")
        print("-" * 30)
        results = self._execute_view_query("v_path_lengths_analysis", limit=8)
        if results:
            print("Node Type        Reachability  Min Hops  Total Paths")
            print("-" * 50)
            for row in results:
                print(f"{row['node_type']:<15} {row['reachability']:<12} {row['min_hops']:<8} {row['total_paths']}")
        
        # Query 3: Orphaned content
        print("\n3. ORPHANED CONTENT (Unreachable from root):")
        print("-" * 45)
        results = self._execute_view_query("v_orphaned_pages", limit=5)
        if results:
            print("Item Type   Total Inbound   URL")
            print("-" * 60)
            for row in results:
                url_short = row['url'][-40:] if len(row['url']) > 40 else row['url']
                print(f"{row['item_type']:<10} {row['total_inbound']:<14} {url_short}")
        else:
            print("✅ No orphaned content found - all nodes reachable from root!")
    
    def test_q2_orphaned_images(self):
        """Test Q2: Referenced vs orphaned images"""
        print("\n" + "="*60)
        print("TESTING Q2: Which images are referenced vs. orphaned and can be safely deleted?")
        print("="*60)
        
        # Query 1: Summary
        print("\n1. IMAGE REFERENCE SUMMARY:")
        print("-" * 35)
        results = self._execute_view_query("v_image_reference_summary", limit=1)
        if results and len(results) > 0:
            row = results[0]
            print(f"Total images: {row.get('total_filesystem_images', 0)}")
            print(f"Referenced: {row.get('referenced_images', 0)}")
            print(f"Orphaned: {row.get('orphaned_images', 0)}")
            print(f"Space savings: {row.get('orphaned_size_mb', 0)} MB")
        else:
            print("No image data available")
        
        # Query 2: Top orphaned images
        print("\n2. TOP ORPHANED IMAGES (DELETION CANDIDATES):")
        print("-" * 55)
        results = self._execute_view_query("v_orphaned_images_detail", limit=5)
        if results:
            print("File                      Size(MB)  Priority             Safety")
            print("-" * 75)
            for row in results:
                filename = row['file_path'].split('/')[-1][:24] if row['file_path'] else 'unknown'
                print(f"{filename:<25} {row['size_mb']:<8} {row['deletion_priority']:<20} {row['safety_assessment']}")
        else:
            print("No orphaned images found")
    
    def test_q3_broken_links(self):
        """Test Q3: Broken links detection"""
        print("\n" + "="*60)
        print("TESTING Q3: What links are broken and need repair?")
        print("="*60)
        
        # Query 1: Broken pages summary
        print("\n1. BROKEN PAGES SUMMARY:")
        print("-" * 30)
        results = self._execute_view_query("v_broken_pages_summary", limit=1)
        if results and len(results) > 0:
            row = results[0]
            print(f"Total pages: {row.get('total_pages', 0)}")
            print(f"Working pages: {row.get('working_pages', 0)}")
            print(f"Broken pages: {row.get('broken_pages', 0)}")
            print(f"404 errors: {row.get('not_found_404', 0)}")
            print(f"500 errors: {row.get('server_error_500', 0)}")
        else:
            print("No page data available")
        
        # Query 2: Broken resources by type
        print("\n2. BROKEN RESOURCES BY TYPE:")
        print("-" * 40)
        results = self._execute_view_query("v_broken_resources_summary", limit=10)
        if results:
            print("Type            Total  Working  Broken  % Broken")
            print("-" * 50)
            for row in results:
                print(f"{row['resource_type']:<15} {row['total_resources']:<6} {row['working_resources']:<8} {row['broken_resources']:<7} {row['broken_percentage']}%")
        else:
            print("No resource data available")
        
        # Query 3: Broken links detail
        print("\n3. BROKEN LINKS DETAIL:")
        print("-" * 25)
        results = self._execute_view_query("v_broken_links_detail", limit=8)
        if results:
            print("Type      Status  Error                URL")
            print("-" * 60)
            for row in results:
                url_short = row['broken_url'][-30:] if len(row['broken_url']) > 30 else row['broken_url']
                error_short = (row['error_message'] or "")[:15]
                print(f"{row['link_type']:<8} {row['http_status']:<6} {error_short:<20} {url_short}")
        else:
            print("No broken links found")
    
    def test_q4_space_savings(self):
        """Test Q4: Space savings from orphaned content"""
        print("\n" + "="*60)
        print("TESTING Q4: How much space could be saved by removing unreferenced content?")
        print("="*60)
        
        # Query 1: Summary
        print("\n1. SPACE SAVINGS SUMMARY:")
        print("-" * 30)
        results = self._execute_view_query("v_orphaned_files_summary", limit=1)
        if results and len(results) > 0:
            row = results[0]
            print(f"Total images: {row.get('total_images', 0)}")
            print(f"Referenced images: {row.get('referenced_images', 0)}")
            print(f"Orphaned images: {row.get('orphaned_images', 0)}")
            print(f"Orphaned size (MB): {row.get('orphaned_size_mb', 0)}")
            print(f"Space savings %: {row.get('space_savings_percent', 0)}%")
        else:
            print("No file data available")
        
        # Query 2: Detail breakdown
        print("\n2. SPACE SAVINGS BY FORMAT/YEAR:")
        print("-" * 40)
        results = self._execute_view_query("v_space_savings_detail", limit=8)
        if results:
            print("Format   Year   Count  Orphaned  MB Saved")
            print("-" * 40)
            for row in results:
                print(f"{row['format']:<8} {row['year'] or 'N/A':<6} {row['image_count']:<6} {row['orphaned_count']:<9} {row['orphaned_mb']}")
        else:
            print("No detailed breakdown available")
        
        # Query 3: Cleanup candidates
        print("\n3. TOP CLEANUP CANDIDATES:")
        print("-" * 30)
        results = self._execute_view_query("v_cleanup_candidates", limit=5)
        if results:
            print("Priority              Size(MB)   File")
            print("-" * 60)
            for row in results:
                filename = row['file_path'].split('/')[-1] if row['file_path'] else 'unknown'
                print(f"{row['cleanup_priority']:<20} {row['size_mb']:<10} {filename}")
        else:
            print("No cleanup candidates found")
    
    def test_q5_site_structure(self):
        """Test Q5: Site structure and navigation patterns"""
        print("\n" + "="*60)
        print("TESTING Q5: What is the overall site structure and navigation patterns?")
        print("="*60)
        
        # Query 1: Site structure summary
        print("\n1. SITE STRUCTURE SUMMARY:")
        print("-" * 35)
        results = self._execute_view_query("v_site_structure_summary", limit=1)
        if results and len(results) > 0:
            row = results[0]
            print(f"Total pages: {row.get('total_pages', 0)}")
            print(f"Category pages: {row.get('category_pages', 0)}")
            print(f"Tag pages: {row.get('tag_pages', 0)}")
            print(f"Date-based posts: {row.get('date_based_posts', 0)}")
            print(f"Total links: {row.get('total_links', 0)}")
            print(f"Avg links per page: {row.get('avg_links_per_page', 0)}")
        else:
            print("No structure data available")
        
        # Query 2: URL pattern breakdown
        print("\n2. URL PATTERN ANALYSIS:")
        print("-" * 30)
        results = self._execute_view_query("v_url_pattern_analysis", limit=10)
        if results:
            print("Category                Count   %     Info")
            print("-" * 50)
            for row in results:
                category = row['page_category'][:22]
                info = (row['extracted_info'] or "")[:12]
                print(f"{category:<23} {row['page_count']:<6} {row['percentage']:<5} {info}")
        else:
            print("No URL pattern data available")
        
        # Query 3: Navigation depth analysis
        print("\n3. NAVIGATION DEPTH ANALYSIS (Top Hub Pages):")
        print("-" * 50)
        results = self._execute_view_query("v_navigation_depth_analysis", limit=6)
        if results:
            print("Page Title               Outbound  Inbound  Role")
            print("-" * 60)
            for row in results:
                title = (row['source_title'] or "Unknown")[:24]
                role = row['navigation_role'][:15]
                print(f"{title:<25} {row['outbound_links']:<9} {row['inbound_links']:<8} {role}")
        else:
            print("No navigation data available")
    
    def run_all_tests(self):
        """Run all analysis tests"""
        print("SiteScanner PostgreSQL Analysis Tests")
        print("=" * 60)
        print(f"Using database: {self.db_type}")
        
        # Test database connection first
        print("\nTesting database connection...", end=' ')
        if test_connection(self.db_type):
            print("✅ Connected")
        else:
            print("❌ Failed")
            print("Cannot proceed without database connection")
            return False
        
        # Run all tests
        self.test_q1_navigation_paths()
        self.test_q2_orphaned_images()
        self.test_q3_broken_links()
        self.test_q4_space_savings()
        self.test_q5_site_structure()
        
        print(f"\n✅ All tests completed using PostgreSQL {self.db_type} database")
        return True

def main():
    """Main test runner function"""
    # Parse command line arguments
    db_type = 'primary'  # Default to shared database
    if len(sys.argv) > 1:
        db_type = sys.argv[1]
        if db_type not in ['primary', 'development', 'testing']:
            print(f"Invalid database type: {db_type}")
            print("Valid options: primary, development, testing")
            sys.exit(1)
    
    runner = PostgreSQLTestRunner(db_type)
    success = runner.run_all_tests()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()