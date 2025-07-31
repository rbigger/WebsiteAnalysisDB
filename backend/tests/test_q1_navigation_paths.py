#!/usr/bin/env python3
"""
Test Q1: Navigation paths from root to leaf nodes

Creates dummy data and queries to answer:
"What are all the navigation paths from root index.html to leaf nodes (images, external links)?"
"""

import sqlite3

def create_dummy_data_q1(db_path):
    """Create dummy data for comprehensive path analysis"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Clear existing data completely for clean Q1 test
    cursor.execute("DELETE FROM crawled_pages")
    cursor.execute("DELETE FROM page_links")
    cursor.execute("DELETE FROM discovered_resources")
    cursor.execute("DELETE FROM resource_references")
    
    print("Creating dummy data for Q1: Navigation paths from root to leaf nodes...")
    
    # Create a focused set of pages for clear path analysis
    pages_data = [
        # Root page
        ('/site/index.html', '/site/index.html', 'Home Page', 200, None, '2024-01-15T10:00:00', '2024-01-15T10:01:00'),
        
        # Level 1 - Main navigation from home
        ('/site/recipes/index.html', '/site/recipes/index.html', 'Recipe Categories', 200, None, '2024-01-15T10:02:00', '2024-01-15T10:03:00'),
        ('/site/blog/index.html', '/site/blog/index.html', 'Blog Posts', 200, None, '2024-01-15T10:04:00', '2024-01-15T10:05:00'),
        ('/site/about.html', '/site/about.html', 'About Us', 200, None, '2024-01-15T10:06:00', '2024-01-15T10:07:00'),
        
        # Level 2 - Recipe categories
        ('/site/recipes/pasta/index.html', '/site/recipes/pasta/index.html', 'Pasta Recipes', 200, None, '2024-01-15T10:08:00', '2024-01-15T10:09:00'),
        ('/site/recipes/salads/index.html', '/site/recipes/salads/index.html', 'Salad Recipes', 200, None, '2024-01-15T10:10:00', '2024-01-15T10:11:00'),
        
        # Level 2 - Blog categories
        ('/site/blog/cooking-tips/index.html', '/site/blog/cooking-tips/index.html', 'Cooking Tips', 200, None, '2024-01-15T10:12:00', '2024-01-15T10:13:00'),
        ('/site/blog/reviews/index.html', '/site/blog/reviews/index.html', 'Restaurant Reviews', 200, None, '2024-01-15T10:14:00', '2024-01-15T10:15:00'),
        
        # Level 3 - Individual recipe posts (LEAF NODES - no outgoing internal links)
        ('/site/recipes/pasta/carbonara.html', '/site/recipes/pasta/carbonara.html', 'Pasta Carbonara Recipe', 200, None, '2024-01-15T10:16:00', '2024-01-15T10:17:00'),
        ('/site/recipes/pasta/bolognese.html', '/site/recipes/pasta/bolognese.html', 'Bolognese Sauce Recipe', 200, None, '2024-01-15T10:18:00', '2024-01-15T10:19:00'),
        ('/site/recipes/salads/caesar.html', '/site/recipes/salads/caesar.html', 'Caesar Salad Recipe', 200, None, '2024-01-15T10:20:00', '2024-01-15T10:21:00'),
        
        # Level 3 - Individual blog posts (LEAF NODES)
        ('/site/blog/cooking-tips/knife-skills.html', '/site/blog/cooking-tips/knife-skills.html', 'Essential Knife Skills', 200, None, '2024-01-15T10:22:00', '2024-01-15T10:23:00'),
        ('/site/blog/reviews/italian-restaurant.html', '/site/blog/reviews/italian-restaurant.html', 'Best Italian Restaurant Downtown', 200, None, '2024-01-15T10:24:00', '2024-01-15T10:25:00'),
        
        # Isolated page (unreachable from root - orphaned)
        ('/site/old/deprecated.html', '/site/old/deprecated.html', 'Old Deprecated Page', 200, None, '2024-01-15T10:26:00', '2024-01-15T10:27:00'),
    ]
    
    cursor.executemany('''
        INSERT INTO crawled_pages (url, file_path, title, http_status, error_message, discovery_timestamp, crawl_timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', pages_data)
    
    # Create clear navigation paths
    links_data = [
        # Level 0 -> Level 1 (Root to main sections)
        ('/site/index.html', '/site/recipes/index.html', 'main_nav'),
        ('/site/index.html', '/site/blog/index.html', 'main_nav'),
        ('/site/index.html', '/site/about.html', 'main_nav'),
        
        # Level 1 -> Level 2 (Main sections to categories)
        ('/site/recipes/index.html', '/site/recipes/pasta/index.html', 'category_nav'),
        ('/site/recipes/index.html', '/site/recipes/salads/index.html', 'category_nav'),
        ('/site/blog/index.html', '/site/blog/cooking-tips/index.html', 'category_nav'),
        ('/site/blog/index.html', '/site/blog/reviews/index.html', 'category_nav'),
        
        # Level 2 -> Level 3 (Categories to individual posts - PATHS TO LEAF NODES)
        ('/site/recipes/pasta/index.html', '/site/recipes/pasta/carbonara.html', 'post_link'),
        ('/site/recipes/pasta/index.html', '/site/recipes/pasta/bolognese.html', 'post_link'),
        ('/site/recipes/salads/index.html', '/site/recipes/salads/caesar.html', 'post_link'),
        ('/site/blog/cooking-tips/index.html', '/site/blog/cooking-tips/knife-skills.html', 'post_link'),
        ('/site/blog/reviews/index.html', '/site/blog/reviews/italian-restaurant.html', 'post_link'),
        
        # Some cross-references between categories (alternative paths)
        ('/site/recipes/pasta/index.html', '/site/recipes/salads/index.html', 'related_category'),
        ('/site/blog/cooking-tips/index.html', '/site/recipes/pasta/index.html', 'related_content'),
        
        # Direct shortcuts from home to some popular content (shorter paths)
        ('/site/index.html', '/site/recipes/pasta/carbonara.html', 'featured_recipe'),
        ('/site/index.html', '/site/blog/cooking-tips/knife-skills.html', 'featured_post'),
        
        # NOTE: /site/old/deprecated.html has NO incoming links - unreachable from root
    ]
    
    cursor.executemany('''
        INSERT INTO page_links (source_url, target_url, link_type)
        VALUES (?, ?, ?)
    ''', links_data)
    
    # Add discovered resources (images, external links) as additional leaf nodes
    resources_data = [
        # Images referenced by leaf pages (ultimate leaf nodes)
        ('/site/images/carbonara-step1.jpg', 'image', '/site/images/carbonara-step1.jpg', 200, None, 85000, 600, 400, 'JPEG'),
        ('/site/images/carbonara-final.jpg', 'image', '/site/images/carbonara-final.jpg', 200, None, 120000, 800, 600, 'JPEG'),
        ('/site/images/bolognese-sauce.jpg', 'image', '/site/images/bolognese-sauce.jpg', 200, None, 95000, 600, 450, 'JPEG'),
        ('/site/images/caesar-salad.jpg', 'image', '/site/images/caesar-salad.jpg', 200, None, 110000, 700, 500, 'JPEG'),
        ('/site/images/knife-techniques.jpg', 'image', '/site/images/knife-techniques.jpg', 200, None, 140000, 900, 600, 'JPEG'),
        
        # External links (leaf nodes - no outgoing internal links)
        ('https://amazon.com/pasta-maker', 'external_link', None, 200, None, None, None, None, None),
        ('https://youtube.com/cooking-video', 'external_link', None, 200, None, None, None, None, None),
        
        # CSS/JS resources (leaf nodes)
        ('/site/css/recipe-styles.css', 'stylesheet', '/site/css/recipe-styles.css', 200, None, 25000, None, None, None),
        ('/site/js/recipe-timer.js', 'script', '/site/js/recipe-timer.js', 200, None, 15000, None, None, None),
    ]
    
    cursor.executemany('''
        INSERT INTO discovered_resources (resource_url, resource_type, file_path, http_status, error_message, file_size, width, height, format)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', resources_data)
    
    # Link pages to their resources (extends paths to ultimate leaf nodes)
    resource_refs_data = [
        # Recipe pages to their images
        ('/site/recipes/pasta/carbonara.html', '/site/images/carbonara-step1.jpg', 'img_src'),
        ('/site/recipes/pasta/carbonara.html', '/site/images/carbonara-final.jpg', 'img_src'),
        ('/site/recipes/pasta/bolognese.html', '/site/images/bolognese-sauce.jpg', 'img_src'),
        ('/site/recipes/salads/caesar.html', '/site/images/caesar-salad.jpg', 'img_src'),
        ('/site/blog/cooking-tips/knife-skills.html', '/site/images/knife-techniques.jpg', 'img_src'),
        
        # External link references
        ('/site/recipes/pasta/carbonara.html', 'https://amazon.com/pasta-maker', 'external_link'),
        ('/site/blog/cooking-tips/knife-skills.html', 'https://youtube.com/cooking-video', 'external_link'),
        
        # CSS/JS references (from multiple pages)
        ('/site/recipes/pasta/carbonara.html', '/site/css/recipe-styles.css', 'stylesheet'),
        ('/site/recipes/pasta/carbonara.html', '/site/js/recipe-timer.js', 'script'),
        ('/site/recipes/pasta/bolognese.html', '/site/css/recipe-styles.css', 'stylesheet'),
    ]
    
    cursor.executemany('''
        INSERT INTO resource_references (page_url, resource_url, reference_type)
        VALUES (?, ?, ?)
    ''', resource_refs_data)
    
    conn.commit()
    conn.close()
    
    print("✅ Dummy data created for Q1")
    print("  - 14 pages in clear hierarchy (root -> categories -> posts)")
    print("  - 15 page-to-page links creating multiple paths")
    print("  - 9 resources (images, external links, CSS/JS) as ultimate leaf nodes")
    print("  - 10 resource references extending paths to resources")
    print("  - 1 orphaned page (unreachable from root)")
    print("  - Multiple path types: direct shortcuts, category navigation, cross-references")

def create_q1_stored_procs(db_path):
    """Create stored procedures (views) for Q1 path analysis queries"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\nCreating Q1 stored procedures...")
    
    # Drop existing views
    cursor.execute("DROP VIEW IF EXISTS v_leaf_nodes_summary")
    cursor.execute("DROP VIEW IF EXISTS v_reachable_paths_from_root")
    cursor.execute("DROP VIEW IF EXISTS v_path_lengths_analysis")
    cursor.execute("DROP VIEW IF EXISTS v_orphaned_pages")
    cursor.execute("DROP VIEW IF EXISTS v_all_leaf_destinations")
    
    # View 1: Identify all leaf nodes (pages/resources with no outgoing internal links)
    cursor.execute('''
        CREATE VIEW v_leaf_nodes_summary AS
        WITH all_nodes AS (
            -- All pages
            SELECT url as node_url, 'page' as node_type, title as node_title, url as source_location
            FROM crawled_pages
            
            UNION ALL
            
            -- All resources  
            SELECT resource_url as node_url, resource_type as node_type, 
                   resource_type || ' resource' as node_title, resource_url as source_location
            FROM discovered_resources
        ),
        nodes_with_outbound AS (
            -- Nodes that have outgoing internal links
            SELECT DISTINCT pl.source_url as node_url
            FROM page_links pl
            WHERE pl.target_url LIKE '/site/%'  -- Internal links only
            
            UNION
            
            SELECT DISTINCT rr.page_url as node_url  
            FROM resource_references rr
            WHERE rr.resource_url LIKE '/site/%'  -- Internal resources only
        )
        SELECT 
            an.node_url,
            an.node_type,
            an.node_title,
            CASE WHEN nwo.node_url IS NULL THEN 'LEAF' ELSE 'NON-LEAF' END as leaf_status,
            -- Count inbound links to this node
            COALESCE((SELECT COUNT(*) FROM page_links pl2 WHERE pl2.target_url = an.node_url), 0) +
            COALESCE((SELECT COUNT(*) FROM resource_references rr2 WHERE rr2.resource_url = an.node_url), 0) as inbound_links
        FROM all_nodes an
        LEFT JOIN nodes_with_outbound nwo ON an.node_url = nwo.node_url
        ORDER BY leaf_status DESC, inbound_links DESC, an.node_type, an.node_url
    ''')
    
    # View 2: Find paths from root using recursive CTE (SQLite supports this)
    cursor.execute('''
        CREATE VIEW v_reachable_paths_from_root AS
        WITH RECURSIVE path_finder(
            target_url, 
            path_string, 
            path_length, 
            link_types_used,
            visited_nodes
        ) AS (
            -- Base case: Start from root
            SELECT 
                '/site/index.html' as target_url,
                '/site/index.html' as path_string,
                0 as path_length,
                '' as link_types_used,
                '/site/index.html|' as visited_nodes
                
            UNION ALL
            
            -- Recursive case: Follow page links
            SELECT 
                pl.target_url,
                pf.path_string || ' -> ' || pl.target_url,
                pf.path_length + 1,
                CASE 
                    WHEN pf.link_types_used = '' THEN pl.link_type
                    ELSE pf.link_types_used || ',' || pl.link_type 
                END,
                pf.visited_nodes || pl.target_url || '|'
            FROM path_finder pf
            JOIN page_links pl ON pf.target_url = pl.source_url
            WHERE pf.path_length < 10  -- Prevent infinite recursion
                AND pf.visited_nodes NOT LIKE '%' || pl.target_url || '|%'  -- Prevent cycles
                
            UNION ALL
            
            -- Extend to resources referenced by pages
            SELECT 
                rr.resource_url,
                pf.path_string || ' -> ' || rr.resource_url,
                pf.path_length + 1,
                CASE 
                    WHEN pf.link_types_used = '' THEN rr.reference_type
                    ELSE pf.link_types_used || ',' || rr.reference_type 
                END,
                pf.visited_nodes || rr.resource_url || '|'
            FROM path_finder pf
            JOIN resource_references rr ON pf.target_url = rr.page_url
            WHERE pf.path_length < 10
                AND pf.visited_nodes NOT LIKE '%' || rr.resource_url || '|%'
        )
        SELECT DISTINCT
            target_url,
            path_string,
            path_length,
            link_types_used,
            -- Classify by path characteristics
            CASE 
                WHEN path_length = 1 THEN 'DIRECT - 1 hop from root'
                WHEN path_length = 2 THEN 'SHORT - 2 hops from root'  
                WHEN path_length = 3 THEN 'MEDIUM - 3 hops from root'
                WHEN path_length >= 4 THEN 'LONG - 4+ hops from root'
                ELSE 'ROOT'
            END as path_classification
        FROM path_finder
        WHERE target_url != '/site/index.html'  -- Exclude root itself
        ORDER BY path_length, target_url
    ''')
    
    # View 3: Path length analysis and statistics
    cursor.execute('''
        CREATE VIEW v_path_lengths_analysis AS
        WITH path_stats AS (
            SELECT 
                target_url,
                COUNT(*) as path_count,
                MIN(path_length) as shortest_path,
                MAX(path_length) as longest_path,
                AVG(path_length) as avg_path_length,
                GROUP_CONCAT(DISTINCT path_classification) as path_variety
            FROM v_reachable_paths_from_root
            GROUP BY target_url
        ),
        node_classification AS (
            SELECT 
                lns.node_url,
                lns.node_type, 
                lns.node_title,
                lns.leaf_status,
                CASE WHEN ps.target_url IS NOT NULL THEN 'REACHABLE' ELSE 'ORPHANED' END as reachability
            FROM v_leaf_nodes_summary lns
            LEFT JOIN path_stats ps ON lns.node_url = ps.target_url
        )
        SELECT 
            nc.node_url,
            nc.node_type,
            nc.node_title,
            nc.leaf_status,
            nc.reachability,
            COALESCE(ps.path_count, 0) as total_paths,
            COALESCE(ps.shortest_path, 999) as min_hops,
            COALESCE(ps.longest_path, 0) as max_hops,
            ROUND(COALESCE(ps.avg_path_length, 0), 1) as avg_hops,
            ps.path_variety
        FROM node_classification nc
        LEFT JOIN path_stats ps ON nc.node_url = ps.target_url
        ORDER BY nc.reachability DESC, nc.leaf_status DESC, ps.shortest_path, nc.node_type
    ''')
    
    # View 4: Identify orphaned pages (unreachable from root)
    cursor.execute('''
        CREATE VIEW v_orphaned_pages AS
        SELECT 
            cp.url,
            cp.title,
            cp.file_path,
            'PAGE' as item_type,
            -- Check if it has any inbound links at all
            COALESCE((SELECT COUNT(*) FROM page_links pl WHERE pl.target_url = cp.url), 0) as inbound_page_links,
            COALESCE((SELECT COUNT(*) FROM resource_references rr WHERE rr.resource_url = cp.url), 0) as inbound_resource_refs,
            -- Total inbound
            COALESCE((SELECT COUNT(*) FROM page_links pl WHERE pl.target_url = cp.url), 0) + 
            COALESCE((SELECT COUNT(*) FROM resource_references rr WHERE rr.resource_url = cp.url), 0) as total_inbound,
            
            'Not reachable from root index.html via any navigation path' as orphan_reason
        FROM crawled_pages cp
        WHERE cp.url NOT IN (
            SELECT DISTINCT target_url 
            FROM v_reachable_paths_from_root
        )
        AND cp.url != '/site/index.html'  -- Exclude root itself
        
        UNION ALL
        
        SELECT 
            dr.resource_url as url,
            dr.resource_type || ' resource' as title,
            dr.file_path,
            'RESOURCE' as item_type,
            0 as inbound_page_links,
            COALESCE((SELECT COUNT(*) FROM resource_references rr WHERE rr.resource_url = dr.resource_url), 0) as inbound_resource_refs,
            COALESCE((SELECT COUNT(*) FROM resource_references rr WHERE rr.resource_url = dr.resource_url), 0) as total_inbound,
            'Resource not referenced by any reachable page' as orphan_reason
        FROM discovered_resources dr
        WHERE dr.resource_url NOT IN (
            SELECT DISTINCT target_url 
            FROM v_reachable_paths_from_root
        )
        
        ORDER BY item_type, total_inbound DESC, url
    ''')
    
    # View 5: All possible destinations from root with their best paths
    cursor.execute('''
        CREATE VIEW v_all_leaf_destinations AS
        WITH best_paths AS (
            SELECT 
                target_url,
                path_string,
                path_length,
                link_types_used,
                ROW_NUMBER() OVER (PARTITION BY target_url ORDER BY path_length, path_string) as path_rank
            FROM v_reachable_paths_from_root
        ),
        leaf_destinations AS (
            SELECT node_url as target_url
            FROM v_leaf_nodes_summary 
            WHERE leaf_status = 'LEAF'
        )
        SELECT 
            bp.target_url as leaf_node,
            CASE 
                WHEN bp.target_url LIKE '/site/images/%' THEN 'IMAGE'
                WHEN bp.target_url LIKE 'https://%' THEN 'EXTERNAL_LINK'
                WHEN bp.target_url LIKE '/site/css/%' THEN 'STYLESHEET'
                WHEN bp.target_url LIKE '/site/js/%' THEN 'SCRIPT'
                WHEN bp.target_url LIKE '%.html' THEN 'PAGE'
                ELSE 'OTHER'
            END as leaf_type,
            bp.path_string as shortest_path,
            bp.path_length as hops_from_root,
            bp.link_types_used as path_link_types,
            (SELECT COUNT(*) FROM v_reachable_paths_from_root rpr WHERE rpr.target_url = bp.target_url) as alternative_paths
        FROM best_paths bp
        JOIN leaf_destinations ld ON bp.target_url = ld.target_url
        WHERE bp.path_rank = 1  -- Only shortest path for each destination
        ORDER BY bp.path_length, leaf_type, bp.target_url
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Q1 stored procedures created:")
    print("  - v_leaf_nodes_summary (identify all leaf nodes)")
    print("  - v_reachable_paths_from_root (recursive path finding)")
    print("  - v_path_lengths_analysis (path statistics and reachability)")
    print("  - v_orphaned_pages (unreachable content)")
    print("  - v_all_leaf_destinations (shortest paths to all leaf nodes)")

def test_q1_queries(db_path):
    """Test the Q1 queries and display results"""
    conn = sqlite3.connect(db_path)
    
    print("\n" + "="*60)
    print("TESTING Q1: What are all the navigation paths from root to leaf nodes?")
    print("="*60)
    
    # Query 1: Leaf nodes summary
    print("\n1. LEAF NODES SUMMARY:")
    print("-" * 25)
    cursor = conn.execute("SELECT leaf_status, node_type, COUNT(*) as count FROM v_leaf_nodes_summary GROUP BY leaf_status, node_type ORDER BY leaf_status DESC, count DESC")
    rows = cursor.fetchall()
    if rows:
        print("Status     Type           Count")
        print("-" * 30)
        for row in rows:
            print(f"{row[0]:<10} {row[1]:<15} {row[2]}")
    
    # Query 2: Sample paths from root (shortest for each destination)
    print("\n2. SHORTEST PATHS TO LEAF NODES (Sample):")
    print("-" * 45)
    cursor = conn.execute("SELECT leaf_node, leaf_type, hops_from_root, shortest_path FROM v_all_leaf_destinations LIMIT 10")
    rows = cursor.fetchall()
    if rows:
        print("Leaf Node" + " " * 20 + "Type     Hops Path")
        print("-" * 80)
        for row in rows:
            leaf = row[0][-25:] if len(row[0]) > 25 else row[0]
            path = row[3][-40:] if len(row[3]) > 40 else row[3]
            print(f"{leaf:<30} {row[1]:<8} {row[2]:<4} ...{path}")
    
    # Query 3: Path length analysis
    print("\n3. PATH LENGTH ANALYSIS:")
    print("-" * 30)
    cursor = conn.execute("SELECT reachability, leaf_status, COUNT(*) as nodes, AVG(min_hops) as avg_min_hops FROM v_path_lengths_analysis GROUP BY reachability, leaf_status ORDER BY reachability DESC")
    rows = cursor.fetchall()
    if rows:
        print("Reachability   Leaf Status  Nodes  Avg Min Hops")
        print("-" * 45)
        for row in rows:
            print(f"{row[0]:<15} {row[1]:<12} {row[2]:<6} {row[3]:.1f}")
    
    # Query 4: Orphaned content
    print("\n4. ORPHANED CONTENT (Unreachable from root):")
    print("-" * 45)
    cursor = conn.execute("SELECT url, item_type, total_inbound FROM v_orphaned_pages")
    rows = cursor.fetchall()
    if rows:
        print("URL" + " " * 35 + "Type     Inbound")
        print("-" * 50)
        for row in rows:
            url = row[0][-37:] if len(row[0]) > 37 else row[0]
            print(f"{url:<40} {row[1]:<8} {row[2]}")
    else:
        print("✅ No orphaned content found - all nodes reachable from root!")
    
    # Query 5: Path variety analysis
    print("\n5. MULTIPLE PATH ANALYSIS:")
    print("-" * 30)
    cursor = conn.execute("SELECT leaf_node, alternative_paths, hops_from_root FROM v_all_leaf_destinations WHERE alternative_paths > 1 ORDER BY alternative_paths DESC LIMIT 6")
    rows = cursor.fetchall()
    if rows:
        print("Leaf Node" + " " * 20 + "Alt Paths  Min Hops")
        print("-" * 45)
        for row in rows:
            leaf = row[0][-29:] if len(row[0]) > 29 else row[0] 
            print(f"{leaf:<30} {row[1]:<10} {row[2]}")
    else:
        print("No nodes with multiple paths found")
    
    conn.close()

def main():
    db_path = "/Users/rogerbigger/ForFriends/site_analysis.db"
    
    create_dummy_data_q1(db_path)
    create_q1_stored_procs(db_path)
    test_q1_queries(db_path)
    
    print(f"\n✅ Q1 test complete. Database updated at: {db_path}")

if __name__ == "__main__":
    main()