-- Q4 View 2: Detailed breakdown by format/year
-- PostgreSQL compatible version

CREATE VIEW v_space_savings_detail AS
SELECT 
    format,
    -- Extract year from uploads path (PostgreSQL compatible)
    SUBSTRING(file_path FROM '/uploads/(\d{4})') as year,
    COUNT(*) as image_count,
    COUNT(CASE WHEN is_referenced = false THEN 1 END) as orphaned_count,
    SUM(file_size) as total_bytes,
    SUM(CASE WHEN is_referenced = false THEN file_size ELSE 0 END) as orphaned_bytes,
    ROUND(SUM(CASE WHEN is_referenced = false THEN file_size ELSE 0 END) / 1024.0 / 1024.0, 2) as orphaned_mb
FROM filesystem_images
GROUP BY format, SUBSTRING(file_path FROM '/uploads/(\d{4})')
HAVING COUNT(CASE WHEN is_referenced = false THEN 1 END) > 0
ORDER BY orphaned_bytes DESC;

-- Add comment for documentation
COMMENT ON VIEW v_space_savings_detail IS 'Q4: Detailed breakdown of space savings potential by file format and year';