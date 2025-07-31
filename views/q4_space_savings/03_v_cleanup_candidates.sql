-- Q4 View 3: Individual cleanup candidates (largest orphaned files first)
-- PostgreSQL compatible version

CREATE VIEW v_cleanup_candidates AS
SELECT 
    file_path,
    format,
    file_size,
    ROUND(file_size / 1024.0 / 1024.0, 2) as size_mb,
    width || 'x' || height as dimensions,
    CASE 
        WHEN file_size > 2000000 THEN 'HIGH - Large file >2MB'
        WHEN file_size > 1000000 THEN 'MEDIUM - File >1MB'
        ELSE 'LOW - Small file <1MB'
    END as cleanup_priority
FROM filesystem_images
WHERE is_referenced = false
ORDER BY file_size DESC;

-- Add comment for documentation
COMMENT ON VIEW v_cleanup_candidates IS 'Q4: Individual orphaned files ranked by size for cleanup prioritization';