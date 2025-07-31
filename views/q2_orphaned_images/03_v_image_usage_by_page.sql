-- Q2 View 3: Image usage breakdown by page
-- PostgreSQL compatible version

CREATE VIEW v_image_usage_by_page AS
SELECT 
    rr.page_url,
    cp.title as page_title,
    COUNT(*) as images_used,
    COUNT(DISTINCT rr.reference_type) as reference_types,
    SUM(CASE WHEN fi.file_size IS NOT NULL THEN fi.file_size ELSE 0 END) as total_image_bytes,
    ROUND(SUM(CASE WHEN fi.file_size IS NOT NULL THEN fi.file_size ELSE 0 END) / 1024.0 / 1024.0, 2) as total_image_mb,
    STRING_AGG(DISTINCT rr.reference_type, ', ') as reference_type_list  -- PostgreSQL uses STRING_AGG instead of GROUP_CONCAT
FROM resource_references rr
LEFT JOIN crawled_pages cp ON rr.page_url = cp.url  
LEFT JOIN filesystem_images fi ON rr.resource_url = fi.file_path
WHERE rr.resource_url LIKE '%.jpg' OR rr.resource_url LIKE '%.png' OR rr.resource_url LIKE '%.gif'
GROUP BY rr.page_url, cp.title
ORDER BY images_used DESC;

-- Add comment for documentation
COMMENT ON VIEW v_image_usage_by_page IS 'Q2: Shows which pages use the most images and their total size consumption';