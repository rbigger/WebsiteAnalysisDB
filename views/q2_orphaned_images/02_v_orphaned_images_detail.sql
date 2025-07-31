-- Q2 View 2: Detailed orphaned images (candidates for deletion)
-- PostgreSQL compatible version

CREATE VIEW v_orphaned_images_detail AS
SELECT 
    file_path,
    format,
    file_size,
    ROUND(file_size / 1024.0 / 1024.0, 3) as size_mb,
    width || 'x' || height as dimensions,
    -- Extract year from uploads path (PostgreSQL compatible)
    SUBSTRING(file_path FROM '/uploads/(\d{4})') as year,
    CASE 
        WHEN file_size > 500000 THEN 'HIGH - Large file >500KB'
        WHEN file_size > 100000 THEN 'MEDIUM - File >100KB'
        ELSE 'LOW - Small file <100KB'
    END as deletion_priority,
    CASE 
        WHEN file_path LIKE '%draft%' OR file_path LIKE '%temp%' OR file_path LIKE '%test%' THEN 'SAFE - Clearly temporary'
        WHEN file_path LIKE '%old%' OR file_path LIKE '%backup%' OR file_path LIKE '%deprecated%' THEN 'SAFE - Clearly outdated'
        WHEN file_path LIKE '%-alt%' OR file_path LIKE '%-v2%' OR file_path LIKE '%-copy%' THEN 'SAFE - Alternative version'
        ELSE 'REVIEW - Verify before deletion'
    END as safety_assessment
FROM filesystem_images
WHERE is_referenced = false
ORDER BY file_size DESC;

-- Add comment for documentation
COMMENT ON VIEW v_orphaned_images_detail IS 'Q2: Detailed list of orphaned images with deletion priority and safety assessment';