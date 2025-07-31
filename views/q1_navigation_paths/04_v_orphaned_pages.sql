-- Q1 View 4: Identify orphaned pages (unreachable from root)
-- PostgreSQL compatible version

CREATE VIEW v_orphaned_pages AS
SELECT 
    cp.url,
    cp.title,
    cp.file_path,
    'PAGE' as item_type,
    -- Check if it has any inbound links at all
    COALESCE((SELECT COUNT(*) FROM page_links pl WHERE pl.target_url = cp.url), 0) as inbound_page_links,
    COALESCE((SELECT COUNT(*) FROM resource_references rr WHERE rr.resource_url = cp.url), 0) as inbound_resource_refs,
    -- Total inbound
    COALESCE((SELECT COUNT(*) FROM page_links pl WHERE pl.target_url = cp.url), 0) + 
    COALESCE((SELECT COUNT(*) FROM resource_references rr WHERE rr.resource_url = cp.url), 0) as total_inbound,
    
    'Not reachable from root index.html via any navigation path' as orphan_reason
FROM crawled_pages cp
WHERE cp.url NOT IN (
    SELECT DISTINCT target_url 
    FROM v_reachable_paths_from_root
)
AND cp.url != '/site/index.html'  -- Exclude root itself

UNION ALL

SELECT 
    dr.resource_url as url,
    dr.resource_type || ' resource' as title,
    dr.file_path,
    'RESOURCE' as item_type,
    0 as inbound_page_links,
    COALESCE((SELECT COUNT(*) FROM resource_references rr WHERE rr.resource_url = dr.resource_url), 0) as inbound_resource_refs,
    COALESCE((SELECT COUNT(*) FROM resource_references rr WHERE rr.resource_url = dr.resource_url), 0) as total_inbound,
    'Resource not referenced by any reachable page' as orphan_reason
FROM discovered_resources dr
WHERE dr.resource_url NOT IN (
    SELECT DISTINCT target_url 
    FROM v_reachable_paths_from_root
)

ORDER BY item_type, total_inbound DESC, url;

-- Add comment for documentation
COMMENT ON VIEW v_orphaned_pages IS 'Q1: Identifies pages and resources that are not reachable from root index.html';