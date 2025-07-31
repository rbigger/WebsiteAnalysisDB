-- SiteScanner Project-Specific Database Setup
-- Run this after installing the base WebsiteAnalysisDB schema
--
-- This file contains:
-- 1. Project-specific configuration
-- 2. Additional indexes for robertiulo.com analysis
-- 3. Project-specific database settings

-- Set application name for connection tracking
SET application_name = 'SiteScanner';

-- Create project-specific indexes optimized for robertiulo.com analysis
-- (These supplement the base indexes from the main schema)

-- Index for WordPress-style URL patterns (common in robertiulo.com)
CREATE INDEX IF NOT EXISTS idx_crawled_pages_wordpress_structure 
ON crawled_pages(url) 
WHERE url LIKE '%/wp-content/%' OR url LIKE '%/category/%' OR url LIKE '%/tag/%';

-- Index for Italian cuisine content (specific to this site's theme)
CREATE INDEX IF NOT EXISTS idx_crawled_pages_content_theme
ON crawled_pages(title)
WHERE title ILIKE '%italian%' OR title ILIKE '%recipe%' OR title ILIKE '%food%';

-- Index for gallery pages (robertiulo.com has extensive galleries)
CREATE INDEX IF NOT EXISTS idx_crawled_pages_gallery
ON crawled_pages(url)
WHERE url LIKE '%gallery%' OR url LIKE '%galllery%';  -- Note: site has typo "galllery"

-- Index for image analysis specific to this site's structure
CREATE INDEX IF NOT EXISTS idx_discovered_resources_site_images
ON discovered_resources(resource_url, file_size)
WHERE resource_type = 'image' AND file_size > 100000;  -- Focus on larger images

-- Create a project-specific view for robertiulo.com content categorization
CREATE OR REPLACE VIEW v_robertiulo_content_categories AS
SELECT 
    url,
    title,
    CASE 
        WHEN url LIKE '%recipe%' OR title ILIKE '%recipe%' THEN 'Recipe'
        WHEN url LIKE '%gallery%' OR url LIKE '%galllery%' THEN 'Gallery'
        WHEN url LIKE '%essay%' OR title ILIKE '%essay%' THEN 'Essay'
        WHEN url LIKE '%about%' OR title ILIKE '%about%' THEN 'About'
        WHEN url LIKE '%prep%' OR title ILIKE '%instruction%' THEN 'Instructions'
        WHEN url = '/site/index.html' THEN 'Homepage'
        ELSE 'Other'
    END as content_category,
    http_status,
    crawl_timestamp
FROM crawled_pages
WHERE http_status = 200
ORDER BY content_category, title;

-- Add comment for project context
COMMENT ON VIEW v_robertiulo_content_categories 
IS 'SiteScanner: Content categorization specific to robertiulo.com website structure';

-- Project-specific configuration settings
-- These can be referenced by the application
CREATE TABLE IF NOT EXISTS project_config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert project-specific configuration
INSERT INTO project_config (key, value, description) VALUES
    ('project_name', 'SiteScanner', 'Name of the analysis project'),
    ('target_site_path', '/Users/rogerbigger/ForFriends/robertiulo_download/robertiulo.com', 'Local path to analyzed site'),
    ('site_theme', 'Italian Cuisine Blog', 'Theme/topic of the analyzed website'),
    ('analysis_focus', 'Navigation optimization and content organization', 'Primary analysis objectives'),
    ('site_url_pattern', 'WordPress-style with custom gallery structure', 'URL structure pattern'),
    ('last_crawl_date', '', 'Timestamp of last successful crawl (updated by scripts)'),
    ('total_pages_expected', '4000', 'Approximate number of pages expected (based on HTTrack data)')
ON CONFLICT (key) DO UPDATE SET 
    value = EXCLUDED.value,
    created_at = CURRENT_TIMESTAMP;

-- Grant permissions for analysis
GRANT SELECT ON project_config TO dev_user;
GRANT SELECT ON v_robertiulo_content_categories TO dev_user;

-- Display setup completion
\echo ''
\echo '✅ SiteScanner project-specific database setup complete!'
\echo ''
\echo 'Added:'
\echo '  - 4 performance indexes for robertiulo.com analysis'
\echo '  - v_robertiulo_content_categories view'
\echo '  - project_config table with site-specific settings'
\echo ''
\echo 'Next steps:'
\echo '  1. Run crawler to populate base tables'
\echo '  2. Execute analysis views'
\echo '  3. Generate reports'
\echo ''