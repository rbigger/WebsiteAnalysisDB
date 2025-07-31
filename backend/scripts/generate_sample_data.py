#!/usr/bin/env python3
"""
Sample Data Generator for SiteScanner
Creates realistic test data for development and testing without running full crawl
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any
import argparse
import random

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from database import get_db_connection

class SampleDataGenerator:
    """Generates realistic sample data for SiteScanner testing"""
    
    def __init__(self, db_type: str = 'development'):
        """Initialize generator
        
        Args:
            db_type: Database type ('primary', 'development', 'testing')
        """
        self.db_type = db_type
        self.session_id = f"sample_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def generate_sample_pages(self, count: int = 50) -> List[Dict[str, Any]]:
        """Generate sample pages based on robertiulo.com structure
        
        Args:
            count: Number of pages to generate
            
        Returns:
            List of page dictionaries
        """
        pages = []
        base_timestamp = datetime.now() - timedelta(days=30)
        
        # Homepage
        pages.append({
            'url': '/site/index.html',
            'file_path': 'index.html',
            'title': 'Homepage - Reveries and Recipes',
            'http_status': 200,
            'error_message': None,
            'discovery_timestamp': base_timestamp,
            'crawl_timestamp': base_timestamp + timedelta(minutes=1)
        })
        
        # Main sections
        main_sections = [
            ('about-reveries-and-recipes/index.html', 'About Reveries and Recipes'),
            ('essays/index.html', 'Essays and Stories'),
            ('prep-instructions/index.html', 'Preparation Instructions'),
            ('galllery/index.html', 'Photo Gallery'),
        ]
        
        for i, (path, title) in enumerate(main_sections):
            pages.append({
                'url': f'/site/{path}',
                'file_path': path,
                'title': title,
                'http_status': 200,
                'error_message': None,
                'discovery_timestamp': base_timestamp + timedelta(minutes=i+2),
                'crawl_timestamp': base_timestamp + timedelta(minutes=i+5)
            })
        
        # Gallery pages
        gallery_names = ['gallery_i', 'gallery-ii', 'gallery-iii-2', 'gallery-iv', 'gallery-v']
        for i, gallery in enumerate(gallery_names[:min(5, count//10)]):
            pages.append({
                'url': f'/site/galllery/{gallery}/index.html',
                'file_path': f'galllery/{gallery}/index.html',
                'title': f'Photo Gallery {gallery.replace("gallery", "").replace("-", "").replace("_", "").upper()}',
                'http_status': 200,
                'error_message': None,
                'discovery_timestamp': base_timestamp + timedelta(minutes=10+i),
                'crawl_timestamp': base_timestamp + timedelta(minutes=15+i)
            })
        
        # Recipe pages
        recipe_themes = [
            'pasta-carbonara', 'risotto-milanese', 'osso-buco', 'tiramisu-classic',
            'minestrone-soup', 'pizza-margherita', 'gelato-vanilla', 'bruschetta-tomato',
            'lasagna-bolognese', 'panna-cotta', 'gnocchi-potato', 'focaccia-bread'
        ]
        
        for i, recipe in enumerate(recipe_themes[:min(len(recipe_themes), count//4)]):
            recipe_title = recipe.replace('-', ' ').title()
            pages.append({
                'url': f'/site/recipes/{recipe}/index.html',
                'file_path': f'recipes/{recipe}/index.html',
                'title': f'{recipe_title} Recipe',
                'http_status': 200,
                'error_message': None,
                'discovery_timestamp': base_timestamp + timedelta(minutes=20+i),
                'crawl_timestamp': base_timestamp + timedelta(minutes=25+i)
            })
        
        # Fill remaining with varied content
        content_types = [
            ('stories', 'Story'),
            ('techniques', 'Cooking Technique'),
            ('ingredients', 'Ingredient Guide'),
            ('wine-pairing', 'Wine Pairing'),
            ('seasonal', 'Seasonal Recipe')
        ]
        
        remaining = count - len(pages)
        for i in range(remaining):
            content_type, type_name = random.choice(content_types)
            item_num = i + 1
            pages.append({
                'url': f'/site/{content_type}/item-{item_num:03d}/index.html',
                'file_path': f'{content_type}/item-{item_num:03d}/index.html',
                'title': f'{type_name} {item_num:03d}',
                'http_status': 200,
                'error_message': None,
                'discovery_timestamp': base_timestamp + timedelta(minutes=30+i),
                'crawl_timestamp': base_timestamp + timedelta(minutes=35+i)
            })
        
        # Add some broken pages (404s)
        broken_pages = [
            '/site/old-menu.html',
            '/site/deprecated/old-gallery.html',
            '/site/temp/test-page.html'
        ]
        
        for broken_url in broken_pages:
            pages.append({
                'url': broken_url,
                'file_path': broken_url.replace('/site/', ''),
                'title': None,
                'http_status': 404,
                'error_message': 'File not found',
                'discovery_timestamp': base_timestamp + timedelta(minutes=40),
                'crawl_timestamp': base_timestamp + timedelta(minutes=41)
            })
        
        return pages[:count]
    
    def generate_sample_links(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate realistic page links
        
        Args:
            pages: List of page dictionaries
            
        Returns:
            List of link dictionaries
        """
        links = []
        working_pages = [p for p in pages if p['http_status'] == 200]
        
        if not working_pages:
            return links
        
        homepage = next((p for p in working_pages if 'index.html' == p['file_path']), working_pages[0])
        
        # Homepage navigation links
        main_sections = [p for p in working_pages if '/' not in p['file_path'].replace('index.html', '')][:8]
        for section in main_sections:
            if section != homepage:
                links.append({
                    'source_url': homepage['url'],
                    'target_url': section['url'],
                    'link_type': 'navigation'
                })
        
        # Section to content links
        for page in working_pages:
            # Each page links to 2-5 related pages
            related_count = random.randint(2, 5)
            potential_targets = [p for p in working_pages if p != page]
            
            for target in random.sample(potential_targets, min(related_count, len(potential_targets))):
                # Determine link type based on content (using valid constraint values)
                if 'gallery' in page['file_path'] and 'gallery' in target['file_path']:
                    link_type = 'content'  # gallery navigation
                elif 'recipe' in page['file_path'] and 'recipe' in target['file_path']:
                    link_type = 'content'  # related recipe
                elif 'essay' in page['file_path'] and 'essay' in target['file_path']:
                    link_type = 'content'  # related content
                else:
                    link_type = 'internal'  # general internal link
                
                links.append({
                    'source_url': page['url'],
                    'target_url': target['url'],
                    'link_type': link_type
                })
        
        return links
    
    def generate_sample_resources(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate sample resources (images, CSS, JS)
        
        Args:
            pages: List of page dictionaries
            
        Returns:  
            List of resource dictionaries
        """
        resources = []
        
        # Global site resources
        global_resources = [
            ('/site/css/main.css', 'css', None, None, 'CSS', 35000),
            ('/site/css/gallery.css', 'css', None, None, 'CSS', 15000),
            ('/site/js/main.js', 'js', None, None, 'JS', 25000),
            ('/site/js/gallery.js', 'js', None, None, 'JS', 18000),
            ('/site/images/logo.png', 'image', 200, 100, 'PNG', 45000),
            ('/site/images/banner.jpg', 'image', 1200, 400, 'JPEG', 250000),
        ]
        
        for url, res_type, width, height, format_type, size in global_resources:
            resources.append({
                'resource_url': url,
                'resource_type': res_type,
                'file_path': url.replace('/site/', ''),
                'http_status': 200,
                'error_message': None,
                'file_size': size,
                'width': width,
                'height': height,
                'format': format_type
            })
        
        # Page-specific images
        for page in pages:
            if page['http_status'] != 200:
                continue
                
            # Gallery pages have many images
            if 'gallery' in page['file_path'] or 'galllery' in page['file_path']:
                image_count = random.randint(8, 20)
                for i in range(image_count):
                    width = random.randint(600, 1200)
                    height = random.randint(400, 900)
                    size = random.randint(100000, 500000)
                    
                    image_url = page['url'].replace('/index.html', f'/photo_{i+1:02d}.jpg')
                    resources.append({
                        'resource_url': image_url,
                        'resource_type': 'image',
                        'file_path': image_url.replace('/site/', ''),
                        'http_status': 200,
                        'error_message': None,
                        'file_size': size,
                        'width': width,
                        'height': height,
                        'format': 'JPEG'
                    })
            
            # Recipe pages have food photos
            elif 'recipe' in page['file_path']:
                for i in range(random.randint(2, 5)):
                    width = random.randint(800, 1000)
                    height = random.randint(600, 800)
                    size = random.randint(150000, 300000)
                    
                    image_url = page['url'].replace('/index.html', f'/step_{i+1}.jpg')
                    resources.append({
                        'resource_url': image_url,
                        'resource_type': 'image',
                        'file_path': image_url.replace('/site/', ''),
                        'http_status': 200,
                        'error_message': None,
                        'file_size': size,
                        'width': width,
                        'height': height,
                        'format': 'JPEG'
                    })
        
        # Add some broken resources
        broken_resources = [
            ('/site/images/old-logo.png', 'image'),
            ('/site/css/deprecated.css', 'css'),
            ('/site/js/unused.js', 'js')
        ]
        
        for url, res_type in broken_resources:
            resources.append({
                'resource_url': url,
                'resource_type': res_type,
                'file_path': url.replace('/site/', ''),
                'http_status': 404,
                'error_message': 'File not found',
                'file_size': None,
                'width': None,
                'height': None,
                'format': None
            })
        
        return resources
    
    def generate_resource_references(self, pages: List[Dict[str, Any]], resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate resource reference relationships
        
        Args:
            pages: List of page dictionaries
            resources: List of resource dictionaries
            
        Returns:
            List of resource reference dictionaries
        """
        references = []
        working_pages = [p for p in pages if p['http_status'] == 200]
        working_resources = [r for r in resources if r['http_status'] == 200]
        
        # Global resources referenced by all pages
        global_resources = [r for r in working_resources if 'main.' in r['resource_url'] or 'logo' in r['resource_url']]
        
        for page in working_pages:
            for resource in global_resources:
                ref_type = 'link_href' if resource['resource_type'] == 'css' else 'script_src' if resource['resource_type'] == 'js' else 'img_src'
                references.append({
                    'page_url': page['url'],
                    'resource_url': resource['resource_url'],
                    'reference_type': ref_type
                })
        
        # Page-specific resource references
        for page in working_pages:
            page_dir = '/'.join(page['url'].split('/')[:-1])  # Get directory of page
            page_resources = [r for r in working_resources if r['resource_url'].startswith(page_dir)]
            
            for resource in page_resources:
                ref_type = 'img_src' if resource['resource_type'] == 'image' else 'link_href' if resource['resource_type'] == 'css' else 'script_src'
                references.append({
                    'page_url': page['url'],
                    'resource_url': resource['resource_url'],
                    'reference_type': ref_type
                })
        
        return references
    
    def populate_database(self, page_count: int = 50, clear_existing: bool = True):
        """Generate and populate database with sample data
        
        Args:
            page_count: Number of pages to generate
            clear_existing: Whether to clear existing data first
        """
        print(f"Generating sample data for {self.db_type} database...")
        print(f"Target pages: {page_count}")
        
        # Generate sample data
        pages = self.generate_sample_pages(page_count)
        links = self.generate_sample_links(pages)
        resources = self.generate_sample_resources(pages)
        references = self.generate_resource_references(pages, resources)
        
        print(f"Generated:")
        print(f"  - Pages: {len(pages)}")
        print(f"  - Links: {len(links)}")
        print(f"  - Resources: {len(resources)}")
        print(f"  - References: {len(references)}")
        
        with get_db_connection(self.db_type) as db:
            if clear_existing:
                print("Clearing existing data...")
                clear_queries = [
                    "DELETE FROM crawl_state",
                    "DELETE FROM resource_references", 
                    "DELETE FROM page_links",
                    "DELETE FROM filesystem_images",
                    "DELETE FROM discovered_resources",
                    "DELETE FROM crawled_pages"
                ]
                for query in clear_queries:
                    db.execute_query(query, fetch='none')
            
            # Insert data
            print("Inserting pages...")
            page_query = """
            INSERT INTO crawled_pages (url, file_path, title, http_status, error_message, discovery_timestamp, crawl_timestamp)
            VALUES (%(url)s, %(file_path)s, %(title)s, %(http_status)s, %(error_message)s, %(discovery_timestamp)s, %(crawl_timestamp)s)
            ON CONFLICT (url) DO NOTHING
            """
            db.execute_many(page_query, pages)
            
            print("Inserting links...")
            link_query = """
            INSERT INTO page_links (source_url, target_url, link_type)
            VALUES (%(source_url)s, %(target_url)s, %(link_type)s)
            ON CONFLICT (source_url, target_url) DO NOTHING
            """
            db.execute_many(link_query, links)
            
            print("Inserting resources...")
            resource_query = """
            INSERT INTO discovered_resources (resource_url, resource_type, file_path, http_status, error_message, file_size, width, height, format)
            VALUES (%(resource_url)s, %(resource_type)s, %(file_path)s, %(http_status)s, %(error_message)s, %(file_size)s, %(width)s, %(height)s, %(format)s)
            ON CONFLICT (resource_url) DO NOTHING
            """
            db.execute_many(resource_query, resources)
            
            print("Inserting resource references...")
            ref_query = """
            INSERT INTO resource_references (page_url, resource_url, reference_type)
            VALUES (%(page_url)s, %(resource_url)s, %(reference_type)s)
            ON CONFLICT (page_url, resource_url, reference_type) DO NOTHING
            """
            db.execute_many(ref_query, references)
            
            # Insert crawl state
            crawl_state = {
                'session_id': self.session_id,
                'visited_urls': '["' + '", "'.join([p['url'] for p in pages if p['http_status'] == 200]) + '"]',
                'queue_urls': '[]',
                'checkpoint_timestamp': datetime.now(),
                'pages_crawled': len([p for p in pages if p['http_status'] == 200]),
                'resources_found': len([r for r in resources if r['http_status'] == 200])
            }
            
            print("Recording crawl state...")
            state_query = """
            INSERT INTO crawl_state (session_id, visited_urls, queue_urls, checkpoint_timestamp, pages_crawled, resources_found)
            VALUES (%(session_id)s, %(visited_urls)s, %(queue_urls)s, %(checkpoint_timestamp)s, %(pages_crawled)s, %(resources_found)s)
            ON CONFLICT (session_id) DO UPDATE SET
                visited_urls = EXCLUDED.visited_urls,
                queue_urls = EXCLUDED.queue_urls,
                checkpoint_timestamp = EXCLUDED.checkpoint_timestamp,
                pages_crawled = EXCLUDED.pages_crawled,
                resources_found = EXCLUDED.resources_found
            """
            db.execute_query(state_query, crawl_state, fetch='none')
        
        print(f"✅ Sample data generation complete!")
        print(f"   - Session ID: {self.session_id}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Generate sample data for testing')
    parser.add_argument('--pages', type=int, default=50, help='Number of pages to generate')
    parser.add_argument('--db-type', default='development', choices=['primary', 'development', 'testing'],
                       help='Database type to populate')
    parser.add_argument('--keep-existing', action='store_true', help='Keep existing data (do not clear)')
    
    args = parser.parse_args()
    
    generator = SampleDataGenerator(args.db_type)
    
    try:
        generator.populate_database(args.pages, not args.keep_existing)
        print(f"\n✅ Successfully generated sample data in {args.db_type} database")
    except Exception as e:
        print(f"❌ Failed to generate sample data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()