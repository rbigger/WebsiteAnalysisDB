-- Q3 View 2: Broken resources summary
-- PostgreSQL compatible version

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
ORDER BY broken_resources DESC;

-- Add comment for documentation
COMMENT ON VIEW v_broken_resources_summary IS 'Q3: Summary of broken resources grouped by type (images, CSS, JS, external links)';