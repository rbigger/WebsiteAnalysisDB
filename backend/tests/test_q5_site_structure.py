#!/usr/bin/env python3
"""
Test Q5: Site structure and navigation patterns

Creates dummy data and queries to answer:
"What is the overall site structure and navigation patterns?"
"""

import sqlite3

def create_dummy_data_q5(db_path):
    """Create dummy crawled_pages, page_links, and resource_references data for structure analysis"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM crawled_pages")
    cursor.execute("DELETE FROM page_links")
    cursor.execute("DELETE FROM resource_references WHERE reference_type != 'img_src'")  # Keep image refs from Q2
    
    print("Creating dummy data for Q5: Site structure and navigation patterns...")
    
    # Comprehensive crawled_pages data showing WordPress structure
    pages_data = [
        # Root and main pages
        ('/site/index.html', '/site/index.html', 'Home - Recipe Blog', 200, None, '2024-01-15T10:00:00', '2024-01-15T10:01:00'),
        ('/site/about/index.html', '/site/about/index.html', 'About the Chef', 200, None, '2024-01-15T10:02:00', '2024-01-15T10:03:00'),
        ('/site/contact/index.html', '/site/contact/index.html', 'Contact Us', 200, None, '2024-01-15T10:04:00', '2024-01-15T10:05:00'),
        
        # Category pages (WordPress structure)
        ('/site/category/appetizers/index.html', '/site/category/appetizers/index.html', 'Appetizer Recipes', 200, None, '2024-01-15T10:06:00', '2024-01-15T10:07:00'),
        ('/site/category/main-courses/index.html', '/site/category/main-courses/index.html', 'Main Course Recipes', 200, None, '2024-01-15T10:08:00', '2024-01-15T10:09:00'),
        ('/site/category/desserts/index.html', '/site/category/desserts/index.html', 'Dessert Recipes', 200, None, '2024-01-15T10:10:00', '2024-01-15T10:11:00'),
        ('/site/category/beverages/index.html', '/site/category/beverages/index.html', 'Drink Recipes', 200, None, '2024-01-15T10:12:00', '2024-01-15T10:13:00'),
        
        # Tag pages  
        ('/site/tag/italian/index.html', '/site/tag/italian/index.html', 'Italian Cuisine', 200, None, '2024-01-15T10:14:00', '2024-01-15T10:15:00'),
        ('/site/tag/vegetarian/index.html', '/site/tag/vegetarian/index.html', 'Vegetarian Recipes', 200, None, '2024-01-15T10:16:00', '2024-01-15T10:17:00'),
        ('/site/tag/quick-meals/index.html', '/site/tag/quick-meals/index.html', 'Quick 30-Minute Meals', 200, None, '2024-01-15T10:18:00', '2024-01-15T10:19:00'),
        
        # Individual recipe posts (date-based structure)
        ('/site/2024/01/pasta-carbonara/index.html', '/site/2024/01/pasta-carbonara/index.html', 'Classic Pasta Carbonara', 200, None, '2024-01-15T10:20:00', '2024-01-15T10:21:00'),
        ('/site/2024/01/bruschetta-appetizer/index.html', '/site/2024/01/bruschetta-appetizer/index.html', 'Fresh Tomato Bruschetta', 200, None, '2024-01-15T10:22:00', '2024-01-15T10:23:00'),
        ('/site/2023/12/tiramisu-recipe/index.html', '/site/2023/12/tiramisu-recipe/index.html', 'Authentic Italian Tiramisu', 200, None, '2024-01-15T10:24:00', '2024-01-15T10:25:00'),
        ('/site/2023/12/eggnog-cocktail/index.html', '/site/2023/12/eggnog-cocktail/index.html', 'Holiday Eggnog Recipe', 200, None, '2024-01-15T10:26:00', '2024-01-15T10:27:00'),
        ('/site/2023/11/roasted-vegetables/index.html', '/site/2023/11/roasted-vegetables/index.html', 'Herb Roasted Winter Vegetables', 200, None, '2024-01-15T10:28:00', '2024-01-15T10:29:00'),
        ('/site/2023/11/quick-stir-fry/index.html', '/site/2023/11/quick-stir-fry/index.html', '15-Minute Vegetable Stir Fry', 200, None, '2024-01-15T10:30:00', '2024-01-15T10:31:00'),
        
        # Archive pages
        ('/site/2024/index.html', '/site/2024/index.html', '2024 Recipe Archive', 200, None, '2024-01-15T10:32:00', '2024-01-15T10:33:00'),
        ('/site/2023/index.html', '/site/2023/index.html', '2023 Recipe Archive', 200, None, '2024-01-15T10:34:00', '2024-01-15T10:35:00'),
        
        # Pagination
        ('/site/page/2/index.html', '/site/page/2/index.html', 'Recipes - Page 2', 200, None, '2024-01-15T10:36:00', '2024-01-15T10:37:00'),
        ('/site/page/3/index.html', '/site/page/3/index.html', 'Recipes - Page 3', 200, None, '2024-01-15T10:38:00', '2024-01-15T10:39:00'),
        
        # Author page
        ('/site/author/chef-mario/index.html', '/site/author/chef-mario/index.html', 'Chef Mario - Recipe Author', 200, None, '2024-01-15T10:40:00', '2024-01-15T10:41:00'),
        
        # Special pages
        ('/site/recipe-index/index.html', '/site/recipe-index/index.html', 'Complete Recipe Index', 200, None, '2024-01-15T10:42:00', '2024-01-15T10:43:00'),
        ('/site/search/index.html', '/site/search/index.html', 'Recipe Search', 200, None, '2024-01-15T10:44:00', '2024-01-15T10:45:00'),
    ]
    
    cursor.executemany('''
        INSERT INTO crawled_pages (url, file_path, title, http_status, error_message, discovery_timestamp, crawl_timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', pages_data)
    
    # Comprehensive page_links data showing navigation patterns
    links_data = [
        # Homepage navigation (main menu)
        ('/site/index.html', '/site/about/index.html', 'navigation'),
        ('/site/index.html', '/site/contact/index.html', 'navigation'),
        ('/site/index.html', '/site/recipe-index/index.html', 'navigation'),
        ('/site/index.html', '/site/search/index.html', 'navigation'),
        
        # Homepage to categories (featured sections)
        ('/site/index.html', '/site/category/appetizers/index.html', 'category_link'),
        ('/site/index.html', '/site/category/main-courses/index.html', 'category_link'),
        ('/site/index.html', '/site/category/desserts/index.html', 'category_link'),
        ('/site/index.html', '/site/category/beverages/index.html', 'category_link'),
        
        # Homepage to recent posts
        ('/site/index.html', '/site/2024/01/pasta-carbonara/index.html', 'recent_post'),
        ('/site/index.html', '/site/2024/01/bruschetta-appetizer/index.html', 'recent_post'),
        ('/site/index.html', '/site/2023/12/tiramisu-recipe/index.html', 'recent_post'),
        
        # Category pages to individual recipes
        ('/site/category/appetizers/index.html', '/site/2024/01/bruschetta-appetizer/index.html', 'category_post'),
        ('/site/category/main-courses/index.html', '/site/2024/01/pasta-carbonara/index.html', 'category_post'),
        ('/site/category/main-courses/index.html', '/site/2023/11/quick-stir-fry/index.html', 'category_post'),
        ('/site/category/desserts/index.html', '/site/2023/12/tiramisu-recipe/index.html', 'category_post'),
        ('/site/category/beverages/index.html', '/site/2023/12/eggnog-cocktail/index.html', 'category_post'),
        
        # Tag pages to recipes
        ('/site/tag/italian/index.html', '/site/2024/01/pasta-carbonara/index.html', 'tag_post'),
        ('/site/tag/italian/index.html', '/site/2023/12/tiramisu-recipe/index.html', 'tag_post'),
        ('/site/tag/italian/index.html', '/site/2024/01/bruschetta-appetizer/index.html', 'tag_post'),
        ('/site/tag/vegetarian/index.html', '/site/2023/11/roasted-vegetables/index.html', 'tag_post'),
        ('/site/tag/vegetarian/index.html', '/site/2023/11/quick-stir-fry/index.html', 'tag_post'),
        ('/site/tag/quick-meals/index.html', '/site/2023/11/quick-stir-fry/index.html', 'tag_post'),
        
        # Archive pages to individual posts
        ('/site/2024/index.html', '/site/2024/01/pasta-carbonara/index.html', 'archive_post'),
        ('/site/2024/index.html', '/site/2024/01/bruschetta-appetizer/index.html', 'archive_post'),
        ('/site/2023/index.html', '/site/2023/12/tiramisu-recipe/index.html', 'archive_post'),
        ('/site/2023/index.html', '/site/2023/12/eggnog-cocktail/index.html', 'archive_post'),
        ('/site/2023/index.html', '/site/2023/11/roasted-vegetables/index.html', 'archive_post'),
        ('/site/2023/index.html', '/site/2023/11/quick-stir-fry/index.html', 'archive_post'),
        
        # Recipe posts to related recipes (cross-linking)
        ('/site/2024/01/pasta-carbonara/index.html', '/site/2024/01/bruschetta-appetizer/index.html', 'related_post'),
        ('/site/2024/01/pasta-carbonara/index.html', '/site/2023/12/tiramisu-recipe/index.html', 'related_post'),
        ('/site/2023/12/tiramisu-recipe/index.html', '/site/2023/12/eggnog-cocktail/index.html', 'related_post'),
        ('/site/2023/11/roasted-vegetables/index.html', '/site/2023/11/quick-stir-fry/index.html', 'related_post'),
        
        # Recipe posts to categories/tags (bidirectional linking)
        ('/site/2024/01/pasta-carbonara/index.html', '/site/category/main-courses/index.html', 'category_link'),
        ('/site/2024/01/pasta-carbonara/index.html', '/site/tag/italian/index.html', 'tag_link'),
        ('/site/2024/01/bruschetta-appetizer/index.html', '/site/category/appetizers/index.html', 'category_link'),
        ('/site/2024/01/bruschetta-appetizer/index.html', '/site/tag/italian/index.html', 'tag_link'),
        
        # Author page links
        ('/site/author/chef-mario/index.html', '/site/2024/01/pasta-carbonara/index.html', 'author_post'),
        ('/site/author/chef-mario/index.html', '/site/2023/12/tiramisu-recipe/index.html', 'author_post'),
        
        # Pagination links
        ('/site/index.html', '/site/page/2/index.html', 'pagination'),
        ('/site/page/2/index.html', '/site/page/3/index.html', 'pagination'),
        ('/site/page/2/index.html', '/site/index.html', 'pagination'),
        ('/site/page/3/index.html', '/site/page/2/index.html', 'pagination'),
        
        # Recipe index to all recipes
        ('/site/recipe-index/index.html', '/site/2024/01/pasta-carbonara/index.html', 'index_link'),
        ('/site/recipe-index/index.html', '/site/2024/01/bruschetta-appetizer/index.html', 'index_link'),
        ('/site/recipe-index/index.html', '/site/2023/12/tiramisu-recipe/index.html', 'index_link'),
        ('/site/recipe-index/index.html', '/site/2023/12/eggnog-cocktail/index.html', 'index_link'),
    ]
    
    cursor.executemany('''
        INSERT INTO page_links (source_url, target_url, link_type)
        VALUES (?, ?, ?)
    ''', links_data)
    
    # Add some resource references for CSS/JS structure analysis
    resource_refs_data = [
        # Global resources (used on every page)
        ('/site/index.html', '/site/wp-content/themes/recipe-theme/style.css', 'stylesheet'),
        ('/site/index.html', '/site/wp-content/themes/recipe-theme/js/main.js', 'script'),
        ('/site/about/index.html', '/site/wp-content/themes/recipe-theme/style.css', 'stylesheet'),
        ('/site/about/index.html', '/site/wp-content/themes/recipe-theme/js/main.js', 'script'),
        
        # Recipe-specific resources
        ('/site/2024/01/pasta-carbonara/index.html', '/site/wp-content/themes/recipe-theme/css/recipe.css', 'stylesheet'),
        ('/site/2024/01/pasta-carbonara/index.html', '/site/wp-content/themes/recipe-theme/js/recipe.js', 'script'),
        
        # Search page specific resources
        ('/site/search/index.html', '/site/wp-content/themes/recipe-theme/js/search.js', 'script'),
    ]
    
    cursor.executemany('''
        INSERT INTO resource_references (page_url, resource_url, reference_type)
        VALUES (?, ?, ?)
    ''', resource_refs_data)
    
    conn.commit()
    conn.close()
    
    print("✅ Dummy data created for Q5")
    print("  - 22 pages with realistic WordPress structure")
    print("  - 46 page links showing navigation patterns")
    print("  - 7 resource references for CSS/JS analysis")
    print("  - URL patterns: categories, tags, dates, pagination, archives")

def create_q5_stored_procs(db_path):
    """Create stored procedures (views) for Q5 queries"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\nCreating Q5 stored procedures...")
    
    # Drop existing views
    cursor.execute("DROP VIEW IF EXISTS v_site_structure_summary")
    cursor.execute("DROP VIEW IF EXISTS v_url_pattern_analysis")
    cursor.execute("DROP VIEW IF EXISTS v_navigation_depth_analysis")
    cursor.execute("DROP VIEW IF EXISTS v_link_type_patterns")
    cursor.execute("DROP VIEW IF EXISTS v_most_linked_pages")
    
    # View 1: High-level site structure summary
    cursor.execute('''
        CREATE VIEW v_site_structure_summary AS
        SELECT 
            COUNT(*) as total_pages,
            COUNT(CASE WHEN url LIKE '%/category/%' THEN 1 END) as category_pages,
            COUNT(CASE WHEN url LIKE '%/tag/%' THEN 1 END) as tag_pages,
            COUNT(CASE WHEN url LIKE '%/20__/%' THEN 1 END) as date_based_posts,
            COUNT(CASE WHEN url LIKE '%/page/%' THEN 1 END) as pagination_pages,
            COUNT(CASE WHEN url LIKE '%/author/%' THEN 1 END) as author_pages,
            COUNT(CASE WHEN url = '/site/index.html' OR url LIKE '%/about/%' OR url LIKE '%/contact/%' THEN 1 END) as static_pages,
            
            -- Link analysis
            (SELECT COUNT(*) FROM page_links) as total_links,
            (SELECT COUNT(DISTINCT link_type) FROM page_links) as link_types,
            (SELECT COUNT(DISTINCT source_url) FROM page_links) as pages_with_outbound_links,
            (SELECT COUNT(DISTINCT target_url) FROM page_links) as pages_receiving_links,
            
            -- Navigation depth (rough estimate)
            ROUND(CAST((SELECT COUNT(*) FROM page_links) AS FLOAT) / COUNT(*), 1) as avg_links_per_page
        FROM crawled_pages
    ''')
    
    # View 2: URL pattern analysis
    cursor.execute('''
        CREATE VIEW v_url_pattern_analysis AS
        SELECT 
            CASE 
                WHEN url LIKE '%/category/%' THEN 'Category Pages'
                WHEN url LIKE '%/tag/%' THEN 'Tag Pages'
                WHEN url LIKE '%/20__/0_/%' THEN 'Recipe Posts (Date-based)'
                WHEN url LIKE '%/20__/%' AND url NOT LIKE '%/20__/0_/%' THEN 'Archive Pages'
                WHEN url LIKE '%/page/%' THEN 'Pagination Pages'
                WHEN url LIKE '%/author/%' THEN 'Author Pages'
                WHEN url IN ('/site/index.html', '/site/about/index.html', '/site/contact/index.html', '/site/recipe-index/index.html', '/site/search/index.html') THEN 'Static/Utility Pages'
                ELSE 'Other'
            END as page_category,
            
            COUNT(*) as page_count,
            ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM crawled_pages), 1) as percentage,
            
            -- Extract year/category info where possible
            CASE 
                WHEN url LIKE '%/category/%' THEN SUBSTR(url, INSTR(url, '/category/') + 10, INSTR(SUBSTR(url, INSTR(url, '/category/') + 10), '/') - 1)
                WHEN url LIKE '%/tag/%' THEN SUBSTR(url, INSTR(url, '/tag/') + 5, INSTR(SUBSTR(url, INSTR(url, '/tag/') + 5), '/') - 1)
                WHEN url LIKE '%/20__/%' THEN SUBSTR(url, INSTR(url, '/site/') + 6, 4)
                ELSE NULL
            END as extracted_info,
            
            -- Average title length by category
            ROUND(AVG(LENGTH(title)), 1) as avg_title_length
            
        FROM crawled_pages
        GROUP BY page_category
        ORDER BY page_count DESC
    ''')
    
    # View 3: Navigation depth and connectivity analysis
    cursor.execute('''
        CREATE VIEW v_navigation_depth_analysis AS
        SELECT 
            pl.source_url,
            cp.title as source_title,
            COUNT(*) as outbound_links,
            COUNT(DISTINCT pl.link_type) as link_types_used,
            GROUP_CONCAT(DISTINCT pl.link_type) as link_types_list,
            
            -- Classify pages by their role in navigation
            CASE 
                WHEN COUNT(*) >= 8 THEN 'Hub Page (8+ outbound links)'
                WHEN COUNT(*) >= 4 THEN 'Connector Page (4-7 outbound links)'
                WHEN COUNT(*) >= 1 THEN 'Standard Page (1-3 outbound links)'
                ELSE 'Dead End (0 outbound links)'
            END as navigation_role,
            
            -- Check if this page is linked TO by others (inbound links)
            (SELECT COUNT(*) FROM page_links pl2 WHERE pl2.target_url = pl.source_url) as inbound_links
            
        FROM page_links pl
        LEFT JOIN crawled_pages cp ON pl.source_url = cp.url
        GROUP BY pl.source_url, cp.title
        ORDER BY outbound_links DESC, inbound_links DESC
    ''')
    
    # View 4: Link type patterns and usage
    cursor.execute('''
        CREATE VIEW v_link_type_patterns AS
        SELECT 
            link_type,
            COUNT(*) as usage_count,
            ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM page_links), 1) as usage_percentage,
            COUNT(DISTINCT source_url) as pages_using_this_type,
            COUNT(DISTINCT target_url) as unique_targets,
            
            -- Example source and target
            (SELECT source_url FROM page_links pl2 WHERE pl2.link_type = page_links.link_type LIMIT 1) as example_source,
            (SELECT target_url FROM page_links pl2 WHERE pl2.link_type = page_links.link_type LIMIT 1) as example_target
            
        FROM page_links
        GROUP BY link_type
        ORDER BY usage_count DESC
    ''')
    
    # View 5: Most linked-to pages (authority/popularity)
    cursor.execute('''
        CREATE VIEW v_most_linked_pages AS
        SELECT 
            pl.target_url,
            cp.title as page_title,
            COUNT(*) as inbound_links,
            COUNT(DISTINCT pl.source_url) as unique_sources,
            COUNT(DISTINCT pl.link_type) as link_type_variety,
            GROUP_CONCAT(DISTINCT pl.link_type) as link_types_received,
            
            -- Classify page importance
            CASE 
                WHEN COUNT(*) >= 6 THEN 'HIGH - Authority page (6+ inbound links)'
                WHEN COUNT(*) >= 3 THEN 'MEDIUM - Popular page (3-5 inbound links)'  
                WHEN COUNT(*) >= 1 THEN 'LOW - Linked page (1-2 inbound links)'
                ELSE 'ISOLATED - No inbound links'
            END as page_authority,
            
            -- Check if this page also links out (bidirectional connectivity)
            (SELECT COUNT(*) FROM page_links pl2 WHERE pl2.source_url = pl.target_url) as outbound_links
            
        FROM page_links pl
        LEFT JOIN crawled_pages cp ON pl.target_url = cp.url
        GROUP BY pl.target_url, cp.title
        ORDER BY inbound_links DESC, unique_sources DESC
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Q5 stored procedures created:")
    print("  - v_site_structure_summary (overall metrics and link analysis)")
    print("  - v_url_pattern_analysis (WordPress structure breakdown)")
    print("  - v_navigation_depth_analysis (hub vs connector vs leaf pages)")
    print("  - v_link_type_patterns (how different link types are used)")
    print("  - v_most_linked_pages (authority/popularity ranking)")

def test_q5_queries(db_path):
    """Test the Q5 queries and display results"""
    conn = sqlite3.connect(db_path)
    
    print("\n" + "="*60)
    print("TESTING Q5: What is the overall site structure and navigation patterns?")
    print("="*60)
    
    # Query 1: Site structure summary
    print("\n1. SITE STRUCTURE SUMMARY:")
    print("-" * 35)
    cursor = conn.execute("SELECT * FROM v_site_structure_summary")
    row = cursor.fetchone()
    if row:
        cols = [desc[0] for desc in cursor.description]
        for i, col in enumerate(cols):
            print(f"{col}: {row[i]}")
    
    # Query 2: URL pattern breakdown
    print("\n2. URL PATTERN ANALYSIS:")
    print("-" * 30)
    cursor = conn.execute("SELECT page_category, page_count, percentage, extracted_info, avg_title_length FROM v_url_pattern_analysis")
    rows = cursor.fetchall()
    if rows:
        print("Category" + " " * 15 + "Count % Info" + " " * 10 + "AvgTitle")
        print("-" * 65)
        for row in rows:
            category = row[0][:22]
            info = (row[3] or "")[:12]
            print(f"{category:<23} {row[1]:<5} {row[2]:<4} {info:<14} {row[4]}")
    
    # Query 3: Navigation roles (top 8)
    print("\n3. NAVIGATION DEPTH ANALYSIS (Top Hub/Connector Pages):")
    print("-" * 60)
    cursor = conn.execute("SELECT source_title, outbound_links, navigation_role, inbound_links FROM v_navigation_depth_analysis LIMIT 8")
    rows = cursor.fetchall()
    if rows:
        print("Page Title" + " " * 15 + "Out In  Role")
        print("-" * 50)
        for row in rows:
            title = (row[0] or "Unknown")[:24]
            role = row[2][:20]
            print(f"{title:<25} {row[1]:<3} {row[3]:<3} {role}")
    
    # Query 4: Link type usage
    print("\n4. LINK TYPE PATTERNS:")
    print("-" * 25)
    cursor = conn.execute("SELECT link_type, usage_count, usage_percentage, pages_using_this_type FROM v_link_type_patterns")
    rows = cursor.fetchall()
    if rows:
        print("Link Type" + " " * 8 + "Count %   Pages")
        print("-" * 35)
        for row in rows:
            link_type = row[0][:16]
            print(f"{link_type:<17} {row[1]:<5} {row[2]:<4} {row[3]}")
    
    # Query 5: Most linked pages (authority)
    print("\n5. MOST LINKED PAGES (Authority Ranking):")
    print("-" * 45)
    cursor = conn.execute("SELECT page_title, inbound_links, unique_sources, page_authority FROM v_most_linked_pages LIMIT 8")
    rows = cursor.fetchall()
    if rows:
        print("Page Title" + " " * 15 + "Links Sources Authority")
        print("-" * 55)
        for row in rows:
            title = (row[0] or "Unknown")[:24]
            authority = row[3][:20]
            print(f"{title:<25} {row[1]:<5} {row[2]:<7} {authority}")
    
    conn.close()

def main():
    db_path = "/Users/rogerbigger/ForFriends/site_analysis.db"
    
    create_dummy_data_q5(db_path)
    create_q5_stored_procs(db_path)
    test_q5_queries(db_path)
    
    print(f"\n✅ Q5 test complete. Database updated at: {db_path}")

if __name__ == "__main__":
    main()