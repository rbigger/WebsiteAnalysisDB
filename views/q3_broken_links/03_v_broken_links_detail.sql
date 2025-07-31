-- Q3 View 3: Detailed broken links with error info
-- PostgreSQL compatible version

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

ORDER BY http_status, broken_url;

-- Add comment for documentation
COMMENT ON VIEW v_broken_links_detail IS 'Q3: Detailed list of all broken links (pages and resources) with error information';