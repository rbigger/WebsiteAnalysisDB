#!/usr/bin/env python3
"""
Test Q4: Space savings from orphaned content

Creates dummy data and queries to answer:
"How much space could be saved by removing unreferenced content?"
"""

import sqlite3
import os

def create_dummy_data_q4(db_path):
    """Create dummy filesystem_images and discovered_resources data"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM filesystem_images")
    cursor.execute("DELETE FROM discovered_resources")
    
    print("Creating dummy data for Q4: Space savings...")
    
    # Dummy filesystem_images data (mix of referenced and orphaned)
    filesystem_data = [
        # Referenced images (smaller sizes)
        ('/site/wp-content/uploads/2023/pasta.jpg', 85000, 800, 600, 'JPEG', True),
        ('/site/wp-content/uploads/2023/bread.png', 120000, 1024, 768, 'PNG', True),
        ('/site/wp-content/uploads/2023/wine.jpg', 95000, 900, 675, 'JPEG', True),
        
        # Orphaned images (larger sizes - good candidates for cleanup)
        ('/site/wp-content/uploads/2020/old_banner.jpg', 2500000, 1920, 1080, 'JPEG', False),
        ('/site/wp-content/uploads/2019/unused_photo1.jpg', 1800000, 1600, 1200, 'JPEG', False),
        ('/site/wp-content/uploads/2021/draft_image.png', 3200000, 2048, 1536, 'PNG', False),
        ('/site/wp-content/uploads/2018/temp_backup.jpg', 1200000, 1280, 960, 'JPEG', False),
        
        # More referenced images
        ('/site/wp-content/uploads/2024/featured.jpg', 180000, 1200, 800, 'JPEG', True),
        ('/site/wp-content/uploads/2024/thumbnail.jpg', 45000, 300, 200, 'JPEG', True),
    ]
    
    cursor.executemany('''
        INSERT INTO filesystem_images (file_path, file_size, width, height, format, is_referenced)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', filesystem_data)
    
    # Dummy discovered_resources data (subset of referenced images)
    discovered_data = [
        ('/site/wp-content/uploads/2023/pasta.jpg', 'image', '/site/wp-content/uploads/2023/pasta.jpg', 200, None, 85000, 800, 600, 'JPEG'),
        ('/site/wp-content/uploads/2023/bread.png', 'image', '/site/wp-content/uploads/2023/bread.png', 200, None, 120000, 1024, 768, 'PNG'),
        ('/site/wp-content/uploads/2024/featured.jpg', 'image', '/site/wp-content/uploads/2024/featured.jpg', 200, None, 180000, 1200, 800, 'JPEG'),
    ]
    
    cursor.executemany('''
        INSERT INTO discovered_resources (resource_url, resource_type, file_path, http_status, error_message, file_size, width, height, format)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', discovered_data)
    
    conn.commit()
    conn.close()
    
    print("✅ Dummy data created for Q4")
    print("  - 9 total images in filesystem")
    print("  - 5 referenced images (active)")
    print("  - 4 orphaned images (candidates for cleanup)")

def create_q4_stored_procs(db_path):
    """Create stored procedures (views) for Q4 queries"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\nCreating Q4 stored procedures...")
    
    # Drop existing views
    cursor.execute("DROP VIEW IF EXISTS v_orphaned_files_summary")
    cursor.execute("DROP VIEW IF EXISTS v_space_savings_detail")
    cursor.execute("DROP VIEW IF EXISTS v_cleanup_candidates")
    
    # View 1: High-level space savings summary
    cursor.execute('''
        CREATE VIEW v_orphaned_files_summary AS
        SELECT 
            COUNT(*) as total_images,
            COUNT(CASE WHEN is_referenced = 1 THEN 1 END) as referenced_images,
            COUNT(CASE WHEN is_referenced = 0 THEN 1 END) as orphaned_images,
            SUM(file_size) as total_size_bytes,
            SUM(CASE WHEN is_referenced = 1 THEN file_size ELSE 0 END) as referenced_size_bytes,
            SUM(CASE WHEN is_referenced = 0 THEN file_size ELSE 0 END) as orphaned_size_bytes,
            ROUND(SUM(CASE WHEN is_referenced = 0 THEN file_size ELSE 0 END) / 1024.0 / 1024.0, 2) as orphaned_size_mb,
            ROUND(100.0 * SUM(CASE WHEN is_referenced = 0 THEN file_size ELSE 0 END) / SUM(file_size), 1) as space_savings_percent
        FROM filesystem_images
    ''')
    
    # View 2: Detailed breakdown by format/year
    cursor.execute('''
        CREATE VIEW v_space_savings_detail AS
        SELECT 
            format,
            SUBSTR(file_path, INSTR(file_path, '/uploads/') + 9, 4) as year,
            COUNT(*) as image_count,
            COUNT(CASE WHEN is_referenced = 0 THEN 1 END) as orphaned_count,
            SUM(file_size) as total_bytes,
            SUM(CASE WHEN is_referenced = 0 THEN file_size ELSE 0 END) as orphaned_bytes,
            ROUND(SUM(CASE WHEN is_referenced = 0 THEN file_size ELSE 0 END) / 1024.0 / 1024.0, 2) as orphaned_mb
        FROM filesystem_images
        GROUP BY format, year
        HAVING orphaned_count > 0
        ORDER BY orphaned_bytes DESC
    ''')
    
    # View 3: Individual cleanup candidates (largest orphaned files first)
    cursor.execute('''
        CREATE VIEW v_cleanup_candidates AS
        SELECT 
            file_path,
            format,
            file_size,
            ROUND(file_size / 1024.0 / 1024.0, 2) as size_mb,
            width || 'x' || height as dimensions,
            CASE 
                WHEN file_size > 2000000 THEN 'HIGH - Large file >2MB'
                WHEN file_size > 1000000 THEN 'MEDIUM - File >1MB'
                ELSE 'LOW - Small file <1MB'
            END as cleanup_priority
        FROM filesystem_images
        WHERE is_referenced = 0
        ORDER BY file_size DESC
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Q4 stored procedures created:")
    print("  - v_orphaned_files_summary (high-level metrics)")
    print("  - v_space_savings_detail (breakdown by format/year)")
    print("  - v_cleanup_candidates (individual files to remove)")

def test_q4_queries(db_path):
    """Test the Q4 queries and display results"""
    conn = sqlite3.connect(db_path)
    
    print("\n" + "="*60)
    print("TESTING Q4: How much space could be saved by removing unreferenced content?")
    print("="*60)
    
    # Query 1: Summary
    print("\n1. SPACE SAVINGS SUMMARY:")
    print("-" * 30)
    cursor = conn.execute("SELECT * FROM v_orphaned_files_summary")
    row = cursor.fetchone()
    if row:
        cols = [desc[0] for desc in cursor.description]
        for i, col in enumerate(cols):
            print(f"{col}: {row[i]}")
    
    # Query 2: Detail breakdown
    print("\n2. SPACE SAVINGS BY FORMAT/YEAR:")
    print("-" * 40)
    cursor = conn.execute("SELECT * FROM v_space_savings_detail")
    rows = cursor.fetchall()
    if rows:
        print(f"{'Format':<8} {'Year':<6} {'Count':<6} {'Orphaned':<9} {'MB Saved':<8}")
        print("-" * 40)
        for row in rows:
            print(f"{row[0]:<8} {row[1]:<6} {row[2]:<6} {row[3]:<9} {row[6]:<8}")
    
    # Query 3: Cleanup candidates
    print("\n3. TOP CLEANUP CANDIDATES:")
    print("-" * 50)
    cursor = conn.execute("SELECT * FROM v_cleanup_candidates LIMIT 5")
    rows = cursor.fetchall()
    if rows:
        print(f"{'Priority':<20} {'Size (MB)':<10} {'Dimensions':<12} {'File'}")
        print("-" * 80)
        for row in rows:
            filename = os.path.basename(row[0])
            print(f"{row[5]:<20} {row[3]:<10} {row[4]:<12} {filename}")
    
    conn.close()

def main():
    db_path = "/Users/rogerbigger/ForFriends/site_analysis.db"
    
    create_dummy_data_q4(db_path)
    create_q4_stored_procs(db_path)
    test_q4_queries(db_path)
    
    print(f"\n✅ Q4 test complete. Database updated at: {db_path}")

if __name__ == "__main__":
    main()