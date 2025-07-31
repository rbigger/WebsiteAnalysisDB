-- Q4 View 1: High-level space savings summary
-- PostgreSQL compatible version

CREATE VIEW v_orphaned_files_summary AS
SELECT 
    COUNT(*) as total_images,
    COUNT(CASE WHEN is_referenced = true THEN 1 END) as referenced_images,  -- PostgreSQL uses true/false instead of 1/0
    COUNT(CASE WHEN is_referenced = false THEN 1 END) as orphaned_images,
    SUM(file_size) as total_size_bytes,
    SUM(CASE WHEN is_referenced = true THEN file_size ELSE 0 END) as referenced_size_bytes,
    SUM(CASE WHEN is_referenced = false THEN file_size ELSE 0 END) as orphaned_size_bytes,
    ROUND(SUM(CASE WHEN is_referenced = false THEN file_size ELSE 0 END) / 1024.0 / 1024.0, 2) as orphaned_size_mb,
    ROUND(100.0 * SUM(CASE WHEN is_referenced = false THEN file_size ELSE 0 END) / SUM(file_size), 1) as space_savings_percent
FROM filesystem_images;

-- Add comment for documentation
COMMENT ON VIEW v_orphaned_files_summary IS 'Q4: High-level summary of potential space savings from removing orphaned files';