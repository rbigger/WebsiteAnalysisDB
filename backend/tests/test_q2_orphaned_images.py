#!/usr/bin/env python3
"""
Test Q2: Referenced vs orphaned images

Creates dummy data and queries to answer:
"Which images are referenced vs. orphaned and can be safely deleted?"
"""

import sqlite3

def create_dummy_data_q2(db_path):
    """Create dummy filesystem_images, resource_references, and discovered_resources data"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM filesystem_images")
    cursor.execute("DELETE FROM resource_references")
    cursor.execute("DELETE FROM discovered_resources WHERE resource_type = 'image'")
    cursor.execute("DELETE FROM crawled_pages")
    
    print("Creating dummy data for Q2: Referenced vs orphaned images...")
    
    # Create some pages first (needed for resource_references)
    pages_data = [
        ('/site/index.html', '/site/index.html', 'Home Page', 200, None, '2024-01-15T10:00:00', '2024-01-15T10:01:00'),
        ('/site/recipes/pasta.html', '/site/recipes/pasta.html', 'Pasta Recipes', 200, None, '2024-01-15T10:02:00', '2024-01-15T10:03:00'),
        ('/site/gallery.html', '/site/gallery.html', 'Photo Gallery', 200, None, '2024-01-15T10:04:00', '2024-01-15T10:05:00'),
        ('/site/about.html', '/site/about.html', 'About Us', 200, None, '2024-01-15T10:06:00', '2024-01-15T10:07:00'),
    ]
    
    cursor.executemany('''
        INSERT INTO crawled_pages (url, file_path, title, http_status, error_message, discovery_timestamp, crawl_timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', pages_data)
    
    # Comprehensive filesystem_images data
    filesystem_data = [
        # REFERENCED IMAGES (will have entries in resource_references)
        
        # Homepage images - actively used
        ('/site/wp-content/uploads/2024/logo.png', 15000, 200, 100, 'PNG', True),
        ('/site/wp-content/uploads/2024/hero-banner.jpg', 250000, 1920, 600, 'JPEG', True),
        ('/site/wp-content/uploads/2024/featured-dish.jpg', 180000, 800, 600, 'JPEG', True),
        
        # Recipe images - actively used
        ('/site/wp-content/uploads/2023/pasta-carbonara.jpg', 120000, 600, 400, 'JPEG', True),
        ('/site/wp-content/uploads/2023/pasta-step1.jpg', 85000, 400, 300, 'JPEG', True),
        ('/site/wp-content/uploads/2023/pasta-step2.jpg', 90000, 400, 300, 'JPEG', True),
        
        # Gallery images - actively used
        ('/site/wp-content/uploads/2023/gallery-thumb1.jpg', 35000, 200, 150, 'JPEG', True),
        ('/site/wp-content/uploads/2023/gallery-thumb2.jpg', 38000, 200, 150, 'JPEG', True),
        
        # ORPHANED IMAGES (no references - candidates for deletion)
        
        # Old unused logos/banners
        ('/site/wp-content/uploads/2020/old-logo.png', 45000, 300, 150, 'PNG', False),
        ('/site/wp-content/uploads/2021/old-banner.jpg', 800000, 1600, 400, 'JPEG', False),
        ('/site/wp-content/uploads/2019/deprecated-hero.jpg', 650000, 1200, 800, 'JPEG', False),
        
        # Draft/temporary images never published
        ('/site/wp-content/uploads/2023/draft-photo1.jpg', 200000, 800, 600, 'JPEG', False),
        ('/site/wp-content/uploads/2023/temp-screenshot.png', 150000, 1024, 768, 'PNG', False),
        ('/site/wp-content/uploads/2022/backup-image.jpg', 300000, 900, 600, 'JPEG', False),
        
        # Duplicate/alternative versions never used
        ('/site/wp-content/uploads/2023/pasta-carbonara-alt.jpg', 125000, 600, 400, 'JPEG', False),
        ('/site/wp-content/uploads/2023/pasta-carbonara-v2.jpg', 135000, 600, 400, 'JPEG', False),
        
        # Test images
        ('/site/wp-content/uploads/2024/test-upload.jpg', 50000, 300, 200, 'JPEG', False),
        ('/site/wp-content/uploads/2024/sample.png', 25000, 100, 100, 'PNG', False),
    ]
    
    cursor.executemany('''
        INSERT INTO filesystem_images (file_path, file_size, width, height, format, is_referenced)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', filesystem_data)
    
    # Resource references - showing which pages reference which images
    references_data = [
        # Homepage references
        ('/site/index.html', '/site/wp-content/uploads/2024/logo.png', 'img_src'),
        ('/site/index.html', '/site/wp-content/uploads/2024/hero-banner.jpg', 'img_src'),
        ('/site/index.html', '/site/wp-content/uploads/2024/featured-dish.jpg', 'img_src'),
        ('/site/index.html', '/site/wp-content/uploads/2023/gallery-thumb1.jpg', 'img_src'),
        ('/site/index.html', '/site/wp-content/uploads/2023/gallery-thumb2.jpg', 'img_src'),
        
        # Recipe page references
        ('/site/recipes/pasta.html', '/site/wp-content/uploads/2023/pasta-carbonara.jpg', 'img_src'),
        ('/site/recipes/pasta.html', '/site/wp-content/uploads/2023/pasta-step1.jpg', 'img_src'),
        ('/site/recipes/pasta.html', '/site/wp-content/uploads/2023/pasta-step2.jpg', 'img_src'),
        ('/site/recipes/pasta.html', '/site/wp-content/uploads/2024/logo.png', 'img_src'),  # Header logo
        
        # Gallery page references
        ('/site/gallery.html', '/site/wp-content/uploads/2023/gallery-thumb1.jpg', 'img_src'),
        ('/site/gallery.html', '/site/wp-content/uploads/2023/gallery-thumb2.jpg', 'img_src'),
        ('/site/gallery.html', '/site/wp-content/uploads/2024/logo.png', 'img_src'),  # Header logo
        
        # About page references
        ('/site/about.html', '/site/wp-content/uploads/2024/logo.png', 'img_src'),  # Header logo
    ]
    
    cursor.executemany('''
        INSERT INTO resource_references (page_url, resource_url, reference_type)
        VALUES (?, ?, ?)
    ''', references_data)
    
    # Discovered resources (subset of referenced images found during crawling)
    discovered_data = [
        ('/site/wp-content/uploads/2024/logo.png', 'image', '/site/wp-content/uploads/2024/logo.png', 200, None, 15000, 200, 100, 'PNG'),
        ('/site/wp-content/uploads/2024/hero-banner.jpg', 'image', '/site/wp-content/uploads/2024/hero-banner.jpg', 200, None, 250000, 1920, 600, 'JPEG'),
        ('/site/wp-content/uploads/2023/pasta-carbonara.jpg', 'image', '/site/wp-content/uploads/2023/pasta-carbonara.jpg', 200, None, 120000, 600, 400, 'JPEG'),
        ('/site/wp-content/uploads/2023/gallery-thumb1.jpg', 'image', '/site/wp-content/uploads/2023/gallery-thumb1.jpg', 200, None, 35000, 200, 150, 'JPEG'),
    ]
    
    cursor.executemany('''
        INSERT INTO discovered_resources (resource_url, resource_type, file_path, http_status, error_message, file_size, width, height, format)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', discovered_data)
    
    conn.commit()
    conn.close()
    
    print("✅ Dummy data created for Q2")
    print("  - 18 total images in filesystem")
    print("  - 8 referenced images (used on website)")
    print("  - 10 orphaned images (candidates for deletion)")
    print("  - 13 resource references across 4 pages")
    print("  - 4 discovered resources from crawling")

def create_q2_stored_procs(db_path):
    """Create stored procedures (views) for Q2 queries"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\nCreating Q2 stored procedures...")
    
    # Drop existing views
    cursor.execute("DROP VIEW IF EXISTS v_image_reference_summary")
    cursor.execute("DROP VIEW IF EXISTS v_orphaned_images_detail")
    cursor.execute("DROP VIEW IF EXISTS v_image_usage_by_page")
    cursor.execute("DROP VIEW IF EXISTS v_referenced_vs_discovered")
    
    # View 1: High-level image reference summary
    cursor.execute('''
        CREATE VIEW v_image_reference_summary AS
        SELECT 
            COUNT(*) as total_filesystem_images,
            COUNT(CASE WHEN is_referenced = 1 THEN 1 END) as referenced_images,
            COUNT(CASE WHEN is_referenced = 0 THEN 1 END) as orphaned_images,
            ROUND(100.0 * COUNT(CASE WHEN is_referenced = 1 THEN 1 END) / COUNT(*), 1) as referenced_percentage,
            ROUND(100.0 * COUNT(CASE WHEN is_referenced = 0 THEN 1 END) / COUNT(*), 1) as orphaned_percentage,
            
            -- Size calculations
            SUM(file_size) as total_size_bytes,
            SUM(CASE WHEN is_referenced = 1 THEN file_size ELSE 0 END) as referenced_size_bytes,
            SUM(CASE WHEN is_referenced = 0 THEN file_size ELSE 0 END) as orphaned_size_bytes,
            ROUND(SUM(CASE WHEN is_referenced = 0 THEN file_size ELSE 0 END) / 1024.0 / 1024.0, 2) as orphaned_size_mb,
            
            -- Reference counts
            (SELECT COUNT(DISTINCT resource_url) FROM resource_references WHERE resource_url LIKE '%.jpg' OR resource_url LIKE '%.png' OR resource_url LIKE '%.gif') as images_with_references,
            (SELECT COUNT(*) FROM resource_references WHERE resource_url LIKE '%.jpg' OR resource_url LIKE '%.png' OR resource_url LIKE '%.gif') as total_image_references
        FROM filesystem_images
    ''')
    
    # View 2: Detailed orphaned images (candidates for deletion)
    cursor.execute('''
        CREATE VIEW v_orphaned_images_detail AS
        SELECT 
            file_path,
            format,
            file_size,
            ROUND(file_size / 1024.0 / 1024.0, 3) as size_mb,
            width || 'x' || height as dimensions,
            SUBSTR(file_path, INSTR(file_path, '/uploads/') + 9, 4) as year,
            CASE 
                WHEN file_size > 500000 THEN 'HIGH - Large file >500KB'
                WHEN file_size > 100000 THEN 'MEDIUM - File >100KB'
                ELSE 'LOW - Small file <100KB'
            END as deletion_priority,
            CASE 
                WHEN file_path LIKE '%draft%' OR file_path LIKE '%temp%' OR file_path LIKE '%test%' THEN 'SAFE - Clearly temporary'
                WHEN file_path LIKE '%old%' OR file_path LIKE '%backup%' OR file_path LIKE '%deprecated%' THEN 'SAFE - Clearly outdated'
                WHEN file_path LIKE '%-alt%' OR file_path LIKE '%-v2%' OR file_path LIKE '%-copy%' THEN 'SAFE - Alternative version'
                ELSE 'REVIEW - Verify before deletion'
            END as safety_assessment
        FROM filesystem_images
        WHERE is_referenced = 0
        ORDER BY file_size DESC
    ''')
    
    # View 3: Image usage breakdown by page
    cursor.execute('''
        CREATE VIEW v_image_usage_by_page AS
        SELECT 
            rr.page_url,
            cp.title as page_title,
            COUNT(*) as images_used,
            COUNT(DISTINCT rr.reference_type) as reference_types,
            SUM(CASE WHEN fi.file_size IS NOT NULL THEN fi.file_size ELSE 0 END) as total_image_bytes,
            ROUND(SUM(CASE WHEN fi.file_size IS NOT NULL THEN fi.file_size ELSE 0 END) / 1024.0 / 1024.0, 2) as total_image_mb,
            GROUP_CONCAT(DISTINCT rr.reference_type) as reference_type_list
        FROM resource_references rr
        LEFT JOIN crawled_pages cp ON rr.page_url = cp.url  
        LEFT JOIN filesystem_images fi ON rr.resource_url = fi.file_path
        WHERE rr.resource_url LIKE '%.jpg' OR rr.resource_url LIKE '%.png' OR rr.resource_url LIKE '%.gif'
        GROUP BY rr.page_url, cp.title
        ORDER BY images_used DESC
    ''')
    
    # View 4: Compare referenced images vs discovered images
    cursor.execute('''
        CREATE VIEW v_referenced_vs_discovered AS
        SELECT 
            fi.file_path,
            fi.format,
            fi.file_size,
            CASE WHEN rr.resource_url IS NOT NULL THEN 'YES' ELSE 'NO' END as has_references,
            CASE WHEN dr.resource_url IS NOT NULL THEN 'YES' ELSE 'NO' END as discovered_by_crawler,
            COUNT(rr.page_url) as reference_count,
            GROUP_CONCAT(DISTINCT rr.page_url) as referencing_pages,
            CASE 
                WHEN rr.resource_url IS NOT NULL AND dr.resource_url IS NOT NULL THEN 'ACTIVE - Referenced and crawled'
                WHEN rr.resource_url IS NOT NULL AND dr.resource_url IS NULL THEN 'REFERENCED - But not crawled'
                WHEN rr.resource_url IS NULL AND dr.resource_url IS NOT NULL THEN 'CRAWLED - But no references found'
                ELSE 'ORPHANED - No references or crawling'
            END as status
        FROM filesystem_images fi
        LEFT JOIN resource_references rr ON fi.file_path = rr.resource_url
        LEFT JOIN discovered_resources dr ON fi.file_path = dr.resource_url AND dr.resource_type = 'image'
        WHERE fi.is_referenced = 1  -- Only look at images marked as referenced
        GROUP BY fi.file_path, fi.format, fi.file_size, 
                 CASE WHEN rr.resource_url IS NOT NULL THEN 'YES' ELSE 'NO' END,
                 CASE WHEN dr.resource_url IS NOT NULL THEN 'YES' ELSE 'NO' END
        ORDER BY reference_count DESC, fi.file_size DESC
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Q2 stored procedures created:")
    print("  - v_image_reference_summary (high-level metrics)")
    print("  - v_orphaned_images_detail (deletion candidates with safety assessment)")
    print("  - v_image_usage_by_page (which pages use most images)")
    print("  - v_referenced_vs_discovered (cross-validation of crawler results)")

def test_q2_queries(db_path):
    """Test the Q2 queries and display results"""
    conn = sqlite3.connect(db_path)
    
    print("\n" + "="*60)
    print("TESTING Q2: Which images are referenced vs. orphaned and can be safely deleted?")
    print("="*60)
    
    # Query 1: Summary
    print("\n1. IMAGE REFERENCE SUMMARY:")
    print("-" * 35)
    cursor = conn.execute("SELECT * FROM v_image_reference_summary")
    row = cursor.fetchone()
    if row:
        cols = [desc[0] for desc in cursor.description]
        for i, col in enumerate(cols):
            print(f"{col}: {row[i]}")
    
    # Query 2: Top orphaned images for deletion
    print("\n2. TOP ORPHANED IMAGES (DELETION CANDIDATES):")
    print("-" * 55)
    cursor = conn.execute("SELECT * FROM v_orphaned_images_detail LIMIT 8")
    rows = cursor.fetchall()
    if rows:
        print(f"{'File':<25} {'Size(MB)':<8} {'Priority':<20} {'Safety':<25}")
        print("-" * 80)
        for row in rows:
            filename = row[0].split('/')[-1][:24]  # Get filename only
            print(f"{filename:<25} {row[3]:<8} {row[6]:<20} {row[7]:<25}")
    
    # Query 3: Image usage by page
    print("\n3. IMAGE USAGE BY PAGE:")
    print("-" * 30)
    cursor = conn.execute("SELECT * FROM v_image_usage_by_page")
    rows = cursor.fetchall()
    if rows:
        print(f"{'Page':<25} {'Images':<7} {'Total MB':<8} {'Types'}")
        print("-" * 50)
        for row in rows:
            page = row[0].split('/')[-1][:24]  # Get page filename only
            print(f"{page:<25} {row[2]:<7} {row[5]:<8} {row[6]}")
    
    # Query 4: Referenced vs discovered validation
    print("\n4. REFERENCED VS DISCOVERED VALIDATION:")
    print("-" * 45)
    cursor = conn.execute("SELECT * FROM v_referenced_vs_discovered LIMIT 6")
    rows = cursor.fetchall()
    if rows:
        print(f"{'File':<20} {'Refs':<5} {'Crawled':<8} {'Status':<25}")
        print("-" * 60)
        for row in rows:
            filename = row[0].split('/')[-1][:19]  # Get filename only
            print(f"{filename:<20} {row[5]:<5} {row[4]:<8} {row[7]:<25}")
    
    conn.close()

def main():
    db_path = "/Users/rogerbigger/ForFriends/site_analysis.db"
    
    create_dummy_data_q2(db_path)
    create_q2_stored_procs(db_path)
    test_q2_queries(db_path)
    
    print(f"\n✅ Q2 test complete. Database updated at: {db_path}")

if __name__ == "__main__":
    main()