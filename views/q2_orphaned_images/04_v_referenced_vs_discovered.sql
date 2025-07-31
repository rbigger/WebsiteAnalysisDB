-- Q2 View 4: Compare referenced images vs discovered images
-- PostgreSQL compatible version

CREATE VIEW v_referenced_vs_discovered AS
SELECT 
    fi.file_path,
    fi.format,
    fi.file_size,
    CASE WHEN COUNT(rr.resource_url) > 0 THEN 'YES' ELSE 'NO' END as has_references,
    CASE WHEN COUNT(dr.resource_url) > 0 THEN 'YES' ELSE 'NO' END as discovered_by_crawler,
    COUNT(rr.page_url) as reference_count,
    STRING_AGG(DISTINCT rr.page_url, ', ') as referencing_pages,  -- PostgreSQL uses STRING_AGG instead of GROUP_CONCAT
    CASE 
        WHEN COUNT(rr.resource_url) > 0 AND COUNT(dr.resource_url) > 0 THEN 'ACTIVE - Referenced and crawled'
        WHEN COUNT(rr.resource_url) > 0 AND COUNT(dr.resource_url) = 0 THEN 'REFERENCED - But not crawled'
        WHEN COUNT(rr.resource_url) = 0 AND COUNT(dr.resource_url) > 0 THEN 'CRAWLED - But no references found'
        ELSE 'ORPHANED - No references or crawling'
    END as status
FROM filesystem_images fi
LEFT JOIN resource_references rr ON fi.file_path = rr.resource_url
LEFT JOIN discovered_resources dr ON fi.file_path = dr.resource_url AND dr.resource_type = 'image'
WHERE fi.is_referenced = true  -- Only look at images marked as referenced
GROUP BY fi.file_path, fi.format, fi.file_size
ORDER BY reference_count DESC, fi.file_size DESC;

-- Add comment for documentation
COMMENT ON VIEW v_referenced_vs_discovered IS 'Q2: Cross-validates referenced images against crawler discoveries to identify inconsistencies';