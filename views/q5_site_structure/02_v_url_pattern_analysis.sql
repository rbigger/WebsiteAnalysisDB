-- Q5 View 2: URL pattern analysis  
-- PostgreSQL compatible version

CREATE VIEW v_url_pattern_analysis AS
SELECT 
    CASE 
        WHEN url LIKE '%/category/%' THEN 'Category Pages'
        WHEN url LIKE '%/tag/%' THEN 'Tag Pages'
        WHEN url ~ '/20\d{2}/\d{2}/' THEN 'Recipe Posts (Date-based)'  -- PostgreSQL regex
        WHEN url ~ '/20\d{2}/' AND url !~ '/20\d{2}/\d{2}/' THEN 'Archive Pages'
        WHEN url LIKE '%/page/%' THEN 'Pagination Pages'
        WHEN url LIKE '%/author/%' THEN 'Author Pages'
        WHEN url IN ('/site/index.html', '/site/about/index.html', '/site/contact/index.html', '/site/recipe-index/index.html', '/site/search/index.html') THEN 'Static/Utility Pages'
        ELSE 'Other'
    END as page_category,
    
    COUNT(*) as page_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM crawled_pages), 1) as percentage,
    
    -- Extract year/category info where possible (PostgreSQL compatible)
    MAX(CASE 
        WHEN url LIKE '%/category/%' THEN SUBSTRING(url FROM '/category/([^/]+)')
        WHEN url LIKE '%/tag/%' THEN SUBSTRING(url FROM '/tag/([^/]+)')
        WHEN url ~ '/20\d{2}/' THEN SUBSTRING(url FROM '/(20\d{2})/')
        ELSE NULL
    END) as extracted_info,
    
    -- Average title length by category
    ROUND(AVG(LENGTH(title)), 1) as avg_title_length
    
FROM crawled_pages
GROUP BY page_category
ORDER BY page_count DESC;

-- Add comment for documentation
COMMENT ON VIEW v_url_pattern_analysis IS 'Q5: Analyzes URL patterns to understand WordPress/CMS structure organization';