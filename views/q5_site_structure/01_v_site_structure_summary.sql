-- Q5 View 1: High-level site structure summary
-- PostgreSQL compatible version

CREATE VIEW v_site_structure_summary AS
SELECT 
    COUNT(*) as total_pages,
    COUNT(CASE WHEN url LIKE '%/category/%' THEN 1 END) as category_pages,
    COUNT(CASE WHEN url LIKE '%/tag/%' THEN 1 END) as tag_pages,
    COUNT(CASE WHEN url ~ '/20\d{2}/' THEN 1 END) as date_based_posts,  -- PostgreSQL regex syntax
    COUNT(CASE WHEN url LIKE '%/page/%' THEN 1 END) as pagination_pages,
    COUNT(CASE WHEN url LIKE '%/author/%' THEN 1 END) as author_pages,
    COUNT(CASE WHEN url = '/site/index.html' OR url LIKE '%/about/%' OR url LIKE '%/contact/%' THEN 1 END) as static_pages,
    
    -- Link analysis
    (SELECT COUNT(*) FROM page_links) as total_links,
    (SELECT COUNT(DISTINCT link_type) FROM page_links) as link_types,
    (SELECT COUNT(DISTINCT source_url) FROM page_links) as pages_with_outbound_links,
    (SELECT COUNT(DISTINCT target_url) FROM page_links) as pages_receiving_links,
    
    -- Navigation depth (rough estimate)
    ROUND(CAST((SELECT COUNT(*) FROM page_links) AS NUMERIC) / COUNT(*), 1) as avg_links_per_page  -- PostgreSQL uses NUMERIC for precision
FROM crawled_pages;

-- Add comment for documentation
COMMENT ON VIEW v_site_structure_summary IS 'Q5: High-level overview of site structure with page types and link analysis';