-- Q2 View 1: High-level image reference summary
-- PostgreSQL compatible version

CREATE VIEW v_image_reference_summary AS
SELECT 
    COUNT(*) as total_filesystem_images,
    COUNT(CASE WHEN is_referenced = true THEN 1 END) as referenced_images,  -- PostgreSQL uses true/false instead of 1/0
    COUNT(CASE WHEN is_referenced = false THEN 1 END) as orphaned_images,
    ROUND(100.0 * COUNT(CASE WHEN is_referenced = true THEN 1 END) / COUNT(*), 1) as referenced_percentage,
    ROUND(100.0 * COUNT(CASE WHEN is_referenced = false THEN 1 END) / COUNT(*), 1) as orphaned_percentage,
    
    -- Size calculations
    SUM(file_size) as total_size_bytes,
    SUM(CASE WHEN is_referenced = true THEN file_size ELSE 0 END) as referenced_size_bytes,
    SUM(CASE WHEN is_referenced = false THEN file_size ELSE 0 END) as orphaned_size_bytes,
    ROUND(SUM(CASE WHEN is_referenced = false THEN file_size ELSE 0 END) / 1024.0 / 1024.0, 2) as orphaned_size_mb,
    
    -- Reference counts
    (SELECT COUNT(DISTINCT resource_url) FROM resource_references WHERE resource_url LIKE '%.jpg' OR resource_url LIKE '%.png' OR resource_url LIKE '%.gif') as images_with_references,
    (SELECT COUNT(*) FROM resource_references WHERE resource_url LIKE '%.jpg' OR resource_url LIKE '%.png' OR resource_url LIKE '%.gif') as total_image_references
FROM filesystem_images;

-- Add comment for documentation  
COMMENT ON VIEW v_image_reference_summary IS 'Q2: High-level summary of referenced vs orphaned images with size metrics';