#!/usr/bin/env python3
"""
Test Q3: Broken links detection

Creates dummy data and queries to answer:
"What links are broken and need repair?"
"""

import sqlite3

def create_dummy_data_q3(db_path):
    """Create dummy crawled_pages and discovered_resources data with broken links"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM crawled_pages")
    cursor.execute("DELETE FROM discovered_resources")
    cursor.execute("DELETE FROM page_links")
    
    print("Creating dummy data for Q3: Broken links...")
    
    # Dummy crawled_pages data (mix of working and broken pages)
    pages_data = [
        # Working pages
        ('/site/index.html', '/site/index.html', 'Home Page', 200, None, '2024-01-15T10:00:00', '2024-01-15T10:01:00'),
        ('/site/recipes/pasta.html', '/site/recipes/pasta.html', 'Pasta Recipes', 200, None, '2024-01-15T10:02:00', '2024-01-15T10:03:00'),
        ('/site/about.html', '/site/about.html', 'About Us', 200, None, '2024-01-15T10:04:00', '2024-01-15T10:05:00'),
        
        # Broken pages (404s)
        ('/site/old-menu.html', '/site/old-menu.html', None, 404, 'File not found', '2024-01-15T10:06:00', '2024-01-15T10:07:00'),
        ('/site/temp-page.html', '/site/temp-page.html', None, 404, 'File not found', '2024-01-15T10:08:00', '2024-01-15T10:09:00'),
        
        # Server error page
        ('/site/contact.html', '/site/contact.html', None, 500, 'Internal server error', '2024-01-15T10:10:00', '2024-01-15T10:11:00'),
    ]
    
    cursor.executemany('''
        INSERT INTO crawled_pages (url, file_path, title, http_status, error_message, discovery_timestamp, crawl_timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', pages_data)
    
    # Dummy discovered_resources data (mix of working and broken resources)
    resources_data = [
        # Working images
        ('/site/images/logo.png', 'image', '/site/images/logo.png', 200, None, 45000, 200, 100, 'PNG'),
        ('/site/images/hero.jpg', 'image', '/site/images/hero.jpg', 200, None, 180000, 1200, 800, 'JPEG'),
        
        # Broken images (404s)
        ('/site/images/old-banner.jpg', 'image', '/site/images/old-banner.jpg', 404, 'File not found', None, None, None, None),
        ('/site/images/missing-thumb.png', 'image', '/site/images/missing-thumb.png', 404, 'File not found', None, None, None, None),
        ('/site/images/deleted.gif', 'image', '/site/images/deleted.gif', 404, 'File not found', None, None, None, None),
        
        # Working external links
        ('https://example.com', 'external_link', None, 200, None, None, None, None, None),
        ('https://github.com/project', 'external_link', None, 200, None, None, None, None, None),
        
        # Broken external links
        ('https://dead-site.com', 'external_link', None, 404, 'Site not found', None, None, None, None),
        ('https://timeout-site.com', 'external_link', None, 408, 'Request timeout', None, None, None, None),
        
        # Working CSS/JS
        ('/site/css/style.css', 'stylesheet', '/site/css/style.css', 200, None, 25000, None, None, None),
        ('/site/js/main.js', 'script', '/site/js/main.js', 200, None, 15000, None, None, None),
        
        # Broken CSS/JS
        ('/site/css/old-theme.css', 'stylesheet', '/site/css/old-theme.css', 404, 'File not found', None, None, None, None),
        ('/site/js/deprecated.js', 'script', '/site/js/deprecated.js', 404, 'File not found', None, None, None, None),
    ]
    
    cursor.executemany('''
        INSERT INTO discovered_resources (resource_url, resource_type, file_path, http_status, error_message, file_size, width, height, format)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', resources_data)
    
    # Add some page_links to show which pages link to broken resources
    links_data = [
        ('/site/index.html', '/site/old-menu.html', 'internal'),
        ('/site/index.html', '/site/images/old-banner.jpg', 'image'),
        ('/site/recipes/pasta.html', '/site/images/missing-thumb.png', 'image'),
        ('/site/about.html', 'https://dead-site.com', 'external'),
        ('/site/contact.html', '/site/css/old-theme.css', 'stylesheet'),
    ]
    
    cursor.executemany('''
        INSERT INTO page_links (source_url, target_url, link_type)
        VALUES (?, ?, ?)
    ''', links_data)
    
    conn.commit()
    conn.close()
    
    print("✅ Dummy data created for Q3")
    print("  - 6 pages (3 working, 2 404s, 1 500 error)")
    print("  - 13 resources (6 working, 7 broken)")
    print("  - 5 page links to broken resources")

def create_q3_stored_procs(db_path):
    """Create stored procedures (views) for Q3 queries"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\nCreating Q3 stored procedures...")
    
    # Drop existing views
    cursor.execute("DROP VIEW IF EXISTS v_broken_pages_summary")
    cursor.execute("DROP VIEW IF EXISTS v_broken_resources_summary")
    cursor.execute("DROP VIEW IF EXISTS v_broken_links_detail")
    cursor.execute("DROP VIEW IF EXISTS v_pages_with_broken_links")
    
    # View 1: Broken pages summary
    cursor.execute('''
        CREATE VIEW v_broken_pages_summary AS
        SELECT 
            COUNT(*) as total_pages,
            COUNT(CASE WHEN http_status = 200 THEN 1 END) as working_pages,
            COUNT(CASE WHEN http_status != 200 THEN 1 END) as broken_pages,
            COUNT(CASE WHEN http_status = 404 THEN 1 END) as not_found_404,
            COUNT(CASE WHEN http_status = 500 THEN 1 END) as server_error_500,
            COUNT(CASE WHEN http_status NOT IN (200, 404, 500) THEN 1 END) as other_errors,
            ROUND(100.0 * COUNT(CASE WHEN http_status != 200 THEN 1 END) / COUNT(*), 1) as broken_percentage
        FROM crawled_pages
    ''')
    
    # View 2: Broken resources summary
    cursor.execute('''
        CREATE VIEW v_broken_resources_summary AS
        SELECT 
            resource_type,
            COUNT(*) as total_resources,
            COUNT(CASE WHEN http_status = 200 THEN 1 END) as working_resources,
            COUNT(CASE WHEN http_status != 200 THEN 1 END) as broken_resources,
            COUNT(CASE WHEN http_status = 404 THEN 1 END) as not_found_404,
            ROUND(100.0 * COUNT(CASE WHEN http_status != 200 THEN 1 END) / COUNT(*), 1) as broken_percentage
        FROM discovered_resources
        GROUP BY resource_type
        ORDER BY broken_resources DESC
    ''')
    
    # View 3: Detailed broken links with error info
    cursor.execute('''
        CREATE VIEW v_broken_links_detail AS
        SELECT 
            'PAGE' as link_type,
            url as broken_url,
            http_status,
            error_message,
            title,
            crawl_timestamp
        FROM crawled_pages 
        WHERE http_status != 200
        
        UNION ALL
        
        SELECT 
            'RESOURCE' as link_type,
            resource_url as broken_url,
            http_status,
            error_message,
            resource_type as title,
            NULL as crawl_timestamp
        FROM discovered_resources 
        WHERE http_status != 200
        
        ORDER BY http_status, broken_url
    ''')
    
    # View 4: Pages that link to broken resources (need fixing)
    cursor.execute('''
        CREATE VIEW v_pages_with_broken_links AS
        SELECT 
            pl.source_url as page_with_broken_link,
            pl.target_url as broken_link,
            pl.link_type,
            COALESCE(cp.http_status, dr.http_status) as broken_status,
            COALESCE(cp.error_message, dr.error_message) as error_message,
            cp.title as page_title
        FROM page_links pl
        LEFT JOIN crawled_pages cp ON pl.target_url = cp.url AND cp.http_status != 200
        LEFT JOIN discovered_resources dr ON pl.target_url = dr.resource_url AND dr.http_status != 200
        WHERE cp.url IS NOT NULL OR dr.resource_url IS NOT NULL
        ORDER BY pl.source_url, broken_status
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Q3 stored procedures created:")
    print("  - v_broken_pages_summary (page health overview)")
    print("  - v_broken_resources_summary (resource health by type)")
    print("  - v_broken_links_detail (all broken links with errors)")
    print("  - v_pages_with_broken_links (pages that need fixing)")

def test_q3_queries(db_path):
    """Test the Q3 queries and display results"""
    conn = sqlite3.connect(db_path)
    
    print("\n" + "="*60)
    print("TESTING Q3: What links are broken and need repair?")
    print("="*60)
    
    # Query 1: Broken pages summary
    print("\n1. BROKEN PAGES SUMMARY:")
    print("-" * 30)
    cursor = conn.execute("SELECT * FROM v_broken_pages_summary")
    row = cursor.fetchone()
    if row:
        cols = [desc[0] for desc in cursor.description]
        for i, col in enumerate(cols):
            print(f"{col}: {row[i]}")
    
    # Query 2: Broken resources by type
    print("\n2. BROKEN RESOURCES BY TYPE:")
    print("-" * 40)
    cursor = conn.execute("SELECT * FROM v_broken_resources_summary")
    rows = cursor.fetchall()
    if rows:
        print(f"{'Type':<15} {'Total':<6} {'Working':<8} {'Broken':<7} {'404s':<5} {'% Broken'}")
        print("-" * 55)
        for row in rows:
            print(f"{row[0]:<15} {row[1]:<6} {row[2]:<8} {row[3]:<7} {row[4]:<5} {row[5]}%")
    
    # Query 3: All broken links
    print("\n3. ALL BROKEN LINKS:")
    print("-" * 40)
    cursor = conn.execute("SELECT * FROM v_broken_links_detail")
    rows = cursor.fetchall()
    if rows:
        print(f"{'Type':<8} {'Status':<6} {'Error':<20} {'URL'}")
        print("-" * 70)
        for row in rows:
            url_short = row[1][-40:] if len(row[1]) > 40 else row[1]
            error_short = (row[3] or "")[:20]
            print(f"{row[0]:<8} {row[2]:<6} {error_short:<20} {url_short}")
    
    # Query 4: Pages that need fixing
    print("\n4. PAGES WITH BROKEN LINKS (NEED FIXING):")
    print("-" * 50)
    cursor = conn.execute("SELECT * FROM v_pages_with_broken_links")
    rows = cursor.fetchall()
    if rows:
        print(f"{'Page':<30} {'Broken Link':<30} {'Status':<6} {'Type'}")
        print("-" * 80)
        for row in rows:
            page = row[0][-25:] if len(row[0]) > 25 else row[0]
            link = row[1][-25:] if len(row[1]) > 25 else row[1]
            print(f"{page:<30} {link:<30} {row[3]:<6} {row[2]}")
    
    conn.close()

def main():
    db_path = "/Users/rogerbigger/ForFriends/site_analysis.db"
    
    create_dummy_data_q3(db_path)
    create_q3_stored_procs(db_path)
    test_q3_queries(db_path)
    
    print(f"\n✅ Q3 test complete. Database updated at: {db_path}")

if __name__ == "__main__":
    main()