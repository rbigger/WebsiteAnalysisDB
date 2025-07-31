# SiteScanner Analysis Views

This directory contains PostgreSQL views extracted from the original Python test files. These views provide comprehensive analysis capabilities for website structure, navigation, orphaned content, and optimization opportunities.

## Directory Structure

```
views/
├── q1_navigation_paths/     # Navigation path analysis from root to leaf nodes
├── q2_orphaned_images/      # Referenced vs orphaned image analysis
├── q3_broken_links/         # Broken link detection and reporting
├── q4_space_savings/        # Space optimization through cleanup
├── q5_site_structure/       # Overall site structure and patterns
├── create_all_views.sql     # Master installation script
└── README.md               # This file
```

## Installation

To install all views into the PostgreSQL database:

```bash
# Connect to site_analysis database and run master script
/opt/homebrew/opt/postgresql@15/bin/psql -d site_analysis -f create_all_views.sql
```

Or install individual view categories:

```bash
# Install only Q2 orphaned images views
/opt/homebrew/opt/postgresql@15/bin/psql -d site_analysis -f q2_orphaned_images/01_v_image_reference_summary.sql
/opt/homebrew/opt/postgresql@15/bin/psql -d site_analysis -f q2_orphaned_images/02_v_orphaned_images_detail.sql
# ... etc
```

## View Categories

### Q1: Navigation Paths (5 views)
Analyzes navigation paths from root index.html to all leaf nodes (images, external links, etc.)

- `v_leaf_nodes_summary` - Identifies all leaf nodes with no outgoing internal links
- `v_reachable_paths_from_root` - Recursive path finding from root to all reachable nodes
- `v_path_lengths_analysis` - Path statistics and reachability analysis
- `v_orphaned_pages` - Content unreachable from root
- `v_all_leaf_destinations` - Shortest paths to all leaf nodes with alternatives

### Q2: Orphaned Images (4 views)
Identifies referenced vs orphaned images for cleanup decisions

- `v_image_reference_summary` - High-level metrics of image usage
- `v_orphaned_images_detail` - Detailed orphaned images with safety assessment
- `v_image_usage_by_page` - Which pages use the most images
- `v_referenced_vs_discovered` - Cross-validation of crawler results

### Q3: Broken Links (4 views)
Detects broken links and pages that need repair

- `v_broken_pages_summary` - Overview of working vs broken pages
- `v_broken_resources_summary` - Broken resources grouped by type
- `v_broken_links_detail` - All broken links with error information
- `v_pages_with_broken_links` - Pages containing broken links (need fixing)

### Q4: Space Savings (3 views)
Calculates potential space savings from removing orphaned content

- `v_orphaned_files_summary` - High-level space savings metrics
- `v_space_savings_detail` - Breakdown by file format and year
- `v_cleanup_candidates` - Individual files ranked by cleanup priority

### Q5: Site Structure (5 views)
Analyzes overall site structure and navigation patterns

- `v_site_structure_summary` - High-level site metrics and link analysis
- `v_url_pattern_analysis` - WordPress/CMS structure organization
- `v_navigation_depth_analysis` - Hub vs connector vs leaf page classification
- `v_link_type_patterns` - Usage patterns of different link types
- `v_most_linked_pages` - Authority/popularity ranking by inbound links

## Usage Examples

```sql
-- Get overall image cleanup summary
SELECT * FROM v_image_reference_summary;

-- Find top 10 largest orphaned images
SELECT file_path, size_mb, deletion_priority 
FROM v_orphaned_images_detail 
ORDER BY size_mb DESC 
LIMIT 10;

-- Identify all broken links
SELECT link_type, broken_url, http_status, error_message 
FROM v_broken_links_detail 
ORDER BY http_status;

-- Calculate potential space savings
SELECT orphaned_size_mb, space_savings_percent 
FROM v_orphaned_files_summary;

-- Analyze site navigation structure
SELECT page_category, page_count, percentage 
FROM v_url_pattern_analysis 
ORDER BY page_count DESC;

-- Find hub pages (most outbound links)
SELECT source_title, outbound_links, navigation_role 
FROM v_navigation_depth_analysis 
WHERE navigation_role LIKE 'Hub%' 
ORDER BY outbound_links DESC;
```

## PostgreSQL Compatibility Notes

These views have been converted from SQLite to PostgreSQL with the following changes:

1. **Aggregation functions**: `GROUP_CONCAT()` → `STRING_AGG()`
2. **Boolean values**: `1/0` → `true/false`
3. **String extraction**: SQLite `SUBSTR()/INSTR()` → PostgreSQL `SUBSTRING()/regex`
4. **Regex patterns**: SQLite `LIKE` → PostgreSQL `~` for complex patterns
5. **Precision**: `FLOAT` → `NUMERIC` for better decimal precision
6. **Comments**: Added `COMMENT ON VIEW` statements for documentation

## Dependencies

These views depend on the following tables being present in the `site_analysis` database:

- `crawled_pages` - Pages discovered through crawling
- `discovered_resources` - Images, CSS, JS, external links found
- `page_links` - Navigation links between pages  
- `resource_references` - Which pages reference which resources
- `filesystem_images` - Complete filesystem inventory
- `crawl_state` - Checkpointing data for recovery

Views have dependency relationships (some views reference others), so use the master `create_all_views.sql` script for proper installation order.

## Migration from Python Tests

These views replace the SQL queries that were embedded in the Python test files:

- `backend/tests/test_q1_navigation_paths.py` → `q1_navigation_paths/`
- `backend/tests/test_q2_orphaned_images.py` → `q2_orphaned_images/`
- `backend/tests/test_q3_broken_links.py` → `q3_broken_links/`
- `backend/tests/test_q4_space_savings.py` → `q4_space_savings/`
- `backend/tests/test_q5_site_structure.py` → `q5_site_structure/`

The Python files can now be updated to use these PostgreSQL views instead of creating temporary SQLite views.