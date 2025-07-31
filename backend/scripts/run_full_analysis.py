#!/usr/bin/env python3
"""
Full Analysis Pipeline Script
Runs the complete SiteScanner analysis pipeline: crawl → populate → analyze → report
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from database import get_db_connection, test_connection

class FullAnalysisPipeline:
    """Manages the complete analysis pipeline"""
    
    def __init__(self, db_type: str = 'primary'):
        """Initialize pipeline
        
        Args:
            db_type: Database type ('primary', 'development', 'testing')
        """
        self.db_type = db_type
        self.project_root = Path(__file__).parent.parent
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def check_prerequisites(self) -> bool:
        """Check that all prerequisites are met
        
        Returns:
            True if ready to proceed
        """
        print("Checking prerequisites...")
        
        # Check database connection
        print("  - Database connection...", end=' ')
        if not test_connection(self.db_type):
            print("❌ FAILED")
            return False
        print("✅ OK")
        
        # Check crawler exists
        crawler_path = self.project_root / 'src' / 'crawlers' / 'basic_scanner.py'
        print("  - Crawler script...", end=' ')
        if not crawler_path.exists():
            print("❌ FAILED")
            return False
        print("✅ OK")
        
        # Check data population script
        populate_script = self.project_root / 'scripts' / 'populate_from_crawler.py'
        print("  - Population script...", end=' ')
        if not populate_script.exists():
            print("❌ FAILED")
            return False
        print("✅ OK")
        
        # Check test runner
        test_runner = self.project_root / 'tests' / 'test_runner_postgresql.py'
        print("  - Test runner...", end=' ')
        if not test_runner.exists():
            print("❌ FAILED")
            return False
        print("✅ OK")
        
        # Check target site exists
        target_site = "/Users/rogerbigger/ForFriends/robertiulo_download/robertiulo.com"
        print("  - Target site...", end=' ')
        if not os.path.exists(target_site):
            print("❌ FAILED")
            print(f"    Target site not found: {target_site}")
            return False
        print("✅ OK")
        
        return True
    
    def run_crawler(self, max_pages: int = 50) -> Optional[str]:
        """Run the website crawler
        
        Args:
            max_pages: Maximum pages to crawl
            
        Returns:
            Path to crawler output file, or None if failed
        """
        print(f"\n🔍 Running crawler (max {max_pages} pages)...")
        
        crawler_script = self.project_root / 'src' / 'crawlers' / 'basic_scanner.py'
        output_dir = self.project_root / 'test-results'
        output_dir.mkdir(exist_ok=True)
        
        # Run crawler
        try:
            os.chdir(self.project_root)
            result = subprocess.run([
                'python3', str(crawler_script), str(max_pages)
            ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
            
            if result.returncode != 0:
                print(f"❌ Crawler failed: {result.stderr}")
                return None
            
            # Find the most recent output file
            output_files = list(output_dir.glob('scan_output_*.txt'))
            if not output_files:
                print("❌ No crawler output file found")
                return None
            
            latest_output = max(output_files, key=lambda f: f.stat().st_mtime)
            print(f"✅ Crawler completed: {latest_output.name}")
            return str(latest_output)
            
        except subprocess.TimeoutExpired:
            print("❌ Crawler timed out (5 minutes)")
            return None
        except Exception as e:
            print(f"❌ Crawler error: {e}")
            return None
    
    def populate_database(self, crawler_output: str, clear_existing: bool = True) -> bool:
        """Populate database from crawler output
        
        Args:
            crawler_output: Path to crawler output file
            clear_existing: Whether to clear existing data
            
        Returns:
            True if successful
        """
        print(f"\n📊 Populating {self.db_type} database...")
        
        populate_script = self.project_root / 'scripts' / 'populate_from_crawler.py'
        
        try:
            os.chdir(self.project_root)
            cmd = ['python3', str(populate_script), crawler_output, '--db-type', self.db_type]
            if clear_existing:
                cmd.append('--clear')
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                print(f"❌ Population failed: {result.stderr}")
                return False
            
            print("✅ Database populated successfully")
            return True
            
        except subprocess.TimeoutExpired:
            print("❌ Database population timed out")
            return False
        except Exception as e:
            print(f"❌ Population error: {e}")
            return False
    
    def run_analysis(self) -> bool:
        """Run the full analysis using PostgreSQL views
        
        Returns:
            True if successful
        """
        print(f"\n📈 Running analysis on {self.db_type} database...")
        
        test_runner = self.project_root / 'tests' / 'test_runner_postgresql.py'
        
        try:
            os.chdir(self.project_root)
            result = subprocess.run([
                'python3', str(test_runner), self.db_type
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                print(f"❌ Analysis failed: {result.stderr}")
                return False
            
            # Save analysis output
            output_dir = self.project_root / 'test-results'
            analysis_file = output_dir / f'analysis_results_{self.timestamp}.txt'
            
            with open(analysis_file, 'w') as f:
                f.write(f"SiteScanner Analysis Results\n")
                f.write(f"Generated: {datetime.now()}\n")
                f.write(f"Database: {self.db_type}\n")
                f.write("=" * 60 + "\n\n")
                f.write(result.stdout)
            
            print(f"✅ Analysis completed: {analysis_file.name}")
            return True
            
        except subprocess.TimeoutExpired:
            print("❌ Analysis timed out")
            return False
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return False
    
    def generate_summary_report(self) -> bool:
        """Generate a summary report of key findings
        
        Returns:
            True if successful
        """
        print(f"\n📋 Generating summary report...")
        
        try:
            with get_db_connection(self.db_type) as db:
                # Get high-level statistics
                stats = {}
                
                # Page counts
                page_stats = db.execute_query("SELECT COUNT(*) as total, COUNT(CASE WHEN http_status = 200 THEN 1 END) as working FROM crawled_pages", fetch='one')
                stats['total_pages'] = page_stats['total']
                stats['working_pages'] = page_stats['working']
                
                # Resource counts
                resource_stats = db.execute_query("SELECT COUNT(*) as total, COUNT(CASE WHEN http_status = 200 THEN 1 END) as working FROM discovered_resources", fetch='one')
                stats['total_resources'] = resource_stats['total']
                stats['working_resources'] = resource_stats['working']
                
                # Link counts
                link_stats = db.execute_query("SELECT COUNT(*) as total FROM page_links", fetch='one')
                stats['total_links'] = link_stats['total']
                
                # Top content categories (if project-specific view exists)
                try:
                    categories = db.execute_query("SELECT content_category, COUNT(*) as count FROM v_robertiulo_content_categories GROUP BY content_category ORDER BY count DESC LIMIT 5", fetch='all')
                    stats['top_categories'] = categories
                except:
                    stats['top_categories'] = []
            
            # Write summary report
            output_dir = self.project_root / 'test-results'
            summary_file = output_dir / f'summary_report_{self.timestamp}.txt'
            
            with open(summary_file, 'w') as f:
                f.write("SiteScanner Summary Report\n")
                f.write("=" * 50 + "\n")
                f.write(f"Generated: {datetime.now()}\n")
                f.write(f"Database: {self.db_type}\n\n")
                
                f.write("OVERVIEW\n")
                f.write("-" * 20 + "\n")
                f.write(f"Total Pages: {stats['total_pages']}\n")
                f.write(f"Working Pages: {stats['working_pages']}\n")
                f.write(f"Total Resources: {stats['total_resources']}\n")
                f.write(f"Working Resources: {stats['working_resources']}\n")
                f.write(f"Total Links: {stats['total_links']}\n\n")
                
                if stats['top_categories']:
                    f.write("CONTENT CATEGORIES\n")
                    f.write("-" * 20 + "\n")
                    for cat in stats['top_categories']:
                        f.write(f"{cat['content_category']}: {cat['count']} pages\n")
                    f.write("\n")
                
                f.write("ANALYSIS VIEWS AVAILABLE\n")
                f.write("-" * 30 + "\n")
                f.write("• Q1 Navigation Paths: v_leaf_nodes_summary, v_reachable_paths_from_root\n")
                f.write("• Q2 Orphaned Images: v_image_reference_summary, v_orphaned_images_detail\n")
                f.write("• Q3 Broken Links: v_broken_links_detail, v_pages_with_broken_links\n")
                f.write("• Q4 Space Savings: v_orphaned_files_summary, v_cleanup_candidates\n")
                f.write("• Q5 Site Structure: v_site_structure_summary, v_url_pattern_analysis\n\n")
                
                f.write("NEXT STEPS\n")
                f.write("-" * 15 + "\n")
                f.write("1. Review detailed analysis results\n")
                f.write("2. Query specific views for targeted insights\n")
                f.write("3. Export findings for stakeholder review\n")
                f.write("4. Implement optimization recommendations\n")
            
            print(f"✅ Summary report generated: {summary_file.name}")
            return True
            
        except Exception as e:
            print(f"❌ Report generation error: {e}")
            return False
    
    def run_full_pipeline(self, max_pages: int = 50, clear_existing: bool = True) -> bool:
        """Run the complete analysis pipeline
        
        Args:
            max_pages: Maximum pages to crawl
            clear_existing: Whether to clear existing data
            
        Returns:
            True if successful
        """
        print("=" * 60)
        print("SiteScanner Full Analysis Pipeline")
        print("=" * 60)
        print(f"Target database: {self.db_type}")
        print(f"Max pages: {max_pages}")
        print(f"Clear existing: {clear_existing}")
        print()
        
        # Check prerequisites
        if not self.check_prerequisites():
            print("❌ Prerequisites not met")
            return False
        
        # Run crawler
        crawler_output = self.run_crawler(max_pages)
        if not crawler_output:
            print("❌ Pipeline failed at crawler stage")
            return False
        
        # Populate database
        if not self.populate_database(crawler_output, clear_existing):
            print("❌ Pipeline failed at population stage")
            return False
        
        # Run analysis
        if not self.run_analysis():
            print("❌ Pipeline failed at analysis stage")
            return False
        
        # Generate summary
        if not self.generate_summary_report():
            print("❌ Pipeline failed at reporting stage")
            return False
        
        print("\n" + "=" * 60)
        print("✅ Full analysis pipeline completed successfully!")
        print("=" * 60)
        print(f"\nResults available in: {self.project_root}/test-results/")
        print(f"  - Crawler output: {Path(crawler_output).name}")
        print(f"  - Analysis results: analysis_results_{self.timestamp}.txt")
        print(f"  - Summary report: summary_report_{self.timestamp}.txt")
        print()
        
        return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Run complete SiteScanner analysis pipeline')
    parser.add_argument('--pages', type=int, default=50, help='Maximum pages to crawl')
    parser.add_argument('--db-type', default='primary', choices=['primary', 'development', 'testing'],
                       help='Database type to use')
    parser.add_argument('--keep-existing', action='store_true', help='Keep existing data (do not clear)')
    
    args = parser.parse_args()
    
    pipeline = FullAnalysisPipeline(args.db_type)
    
    try:
        success = pipeline.run_full_pipeline(args.pages, not args.keep_existing)
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Pipeline error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()