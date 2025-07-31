-- Master script to create all PostgreSQL views for SiteScanner analysis
-- Run this file to install all analysis views into the site_analysis database
-- 
-- Usage: psql -d site_analysis -f create_all_views.sql

SET client_min_messages = warning;

\echo 'Creating SiteScanner Analysis Views...'
\echo ''

-- Drop all existing views in correct dependency order
\echo 'Dropping existing views (if any)...'
DROP VIEW IF EXISTS v_all_leaf_destinations CASCADE;
DROP VIEW IF EXISTS v_path_lengths_analysis CASCADE;
DROP VIEW IF EXISTS v_reachable_paths_from_root CASCADE;
DROP VIEW IF EXISTS v_orphaned_pages CASCADE;
DROP VIEW IF EXISTS v_leaf_nodes_summary CASCADE;

DROP VIEW IF EXISTS v_referenced_vs_discovered CASCADE;
DROP VIEW IF EXISTS v_image_usage_by_page CASCADE;
DROP VIEW IF EXISTS v_orphaned_images_detail CASCADE;
DROP VIEW IF EXISTS v_image_reference_summary CASCADE;

DROP VIEW IF EXISTS v_pages_with_broken_links CASCADE;
DROP VIEW IF EXISTS v_broken_links_detail CASCADE;
DROP VIEW IF EXISTS v_broken_resources_summary CASCADE;
DROP VIEW IF EXISTS v_broken_pages_summary CASCADE;

DROP VIEW IF EXISTS v_cleanup_candidates CASCADE;
DROP VIEW IF EXISTS v_space_savings_detail CASCADE;
DROP VIEW IF EXISTS v_orphaned_files_summary CASCADE;

DROP VIEW IF EXISTS v_most_linked_pages CASCADE;
DROP VIEW IF EXISTS v_link_type_patterns CASCADE;
DROP VIEW IF EXISTS v_navigation_depth_analysis CASCADE;
DROP VIEW IF EXISTS v_url_pattern_analysis CASCADE;
DROP VIEW IF EXISTS v_site_structure_summary CASCADE;

\echo 'Creating Q1: Navigation Paths views...'
\i q1_navigation_paths/01_v_leaf_nodes_summary.sql
\i q1_navigation_paths/02_v_reachable_paths_from_root.sql
\i q1_navigation_paths/03_v_path_lengths_analysis.sql
\i q1_navigation_paths/04_v_orphaned_pages.sql
\i q1_navigation_paths/05_v_all_leaf_destinations.sql

\echo 'Creating Q2: Orphaned Images views...'
\i q2_orphaned_images/01_v_image_reference_summary.sql
\i q2_orphaned_images/02_v_orphaned_images_detail.sql
\i q2_orphaned_images/03_v_image_usage_by_page.sql
\i q2_orphaned_images/04_v_referenced_vs_discovered.sql

\echo 'Creating Q3: Broken Links views...'
\i q3_broken_links/01_v_broken_pages_summary.sql
\i q3_broken_links/02_v_broken_resources_summary.sql
\i q3_broken_links/03_v_broken_links_detail.sql
\i q3_broken_links/04_v_pages_with_broken_links.sql

\echo 'Creating Q4: Space Savings views...'
\i q4_space_savings/01_v_orphaned_files_summary.sql
\i q4_space_savings/02_v_space_savings_detail.sql
\i q4_space_savings/03_v_cleanup_candidates.sql

\echo 'Creating Q5: Site Structure views...'
\i q5_site_structure/01_v_site_structure_summary.sql
\i q5_site_structure/02_v_url_pattern_analysis.sql
\i q5_site_structure/03_v_navigation_depth_analysis.sql
\i q5_site_structure/04_v_link_type_patterns.sql
\i q5_site_structure/05_v_most_linked_pages.sql

\echo ''
\echo '✅ All SiteScanner analysis views created successfully!'
\echo ''
\echo 'Available view categories:'
\echo '  Q1 Navigation Paths: 5 views (v_leaf_nodes_summary, v_reachable_paths_from_root, etc.)'
\echo '  Q2 Orphaned Images:  4 views (v_image_reference_summary, v_orphaned_images_detail, etc.)'
\echo '  Q3 Broken Links:     4 views (v_broken_pages_summary, v_broken_resources_summary, etc.)'
\echo '  Q4 Space Savings:    3 views (v_orphaned_files_summary, v_space_savings_detail, etc.)'
\echo '  Q5 Site Structure:   5 views (v_site_structure_summary, v_url_pattern_analysis, etc.)'
\echo ''
\echo 'Usage examples:'
\echo '  SELECT * FROM v_image_reference_summary;'
\echo '  SELECT * FROM v_broken_links_detail LIMIT 10;'
\echo '  SELECT * FROM v_site_structure_summary;'
\echo ''