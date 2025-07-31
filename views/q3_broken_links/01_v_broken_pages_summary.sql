-- Q3 View 1: Broken pages summary
-- PostgreSQL compatible version

CREATE VIEW v_broken_pages_summary AS
SELECT 
    COUNT(*) as total_pages,
    COUNT(CASE WHEN http_status = 200 THEN 1 END) as working_pages,
    COUNT(CASE WHEN http_status != 200 THEN 1 END) as broken_pages,
    COUNT(CASE WHEN http_status = 404 THEN 1 END) as not_found_404,
    COUNT(CASE WHEN http_status = 500 THEN 1 END) as server_error_500,
    COUNT(CASE WHEN http_status NOT IN (200, 404, 500) THEN 1 END) as other_errors,
    ROUND(100.0 * COUNT(CASE WHEN http_status != 200 THEN 1 END) / COUNT(*), 1) as broken_percentage
FROM crawled_pages;

-- Add comment for documentation
COMMENT ON VIEW v_broken_pages_summary IS 'Q3: High-level summary of working vs broken pages with HTTP status breakdown';