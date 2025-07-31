-- Q1 View 5: All possible destinations from root with their best paths
-- PostgreSQL compatible version

CREATE VIEW v_all_leaf_destinations AS
WITH best_paths AS (
    SELECT 
        target_url,
        path_string,
        path_length,
        link_types_used,
        ROW_NUMBER() OVER (PARTITION BY target_url ORDER BY path_length, path_string) as path_rank
    FROM v_reachable_paths_from_root
),
leaf_destinations AS (
    SELECT node_url as target_url
    FROM v_leaf_nodes_summary 
    WHERE leaf_status = 'LEAF'
)
SELECT 
    bp.target_url as leaf_node,
    CASE 
        WHEN bp.target_url LIKE '/site/images/%' THEN 'IMAGE'
        WHEN bp.target_url LIKE 'https://%' THEN 'EXTERNAL_LINK'
        WHEN bp.target_url LIKE '/site/css/%' THEN 'STYLESHEET'
        WHEN bp.target_url LIKE '/site/js/%' THEN 'SCRIPT'
        WHEN bp.target_url LIKE '%.html' THEN 'PAGE'
        ELSE 'OTHER'
    END as leaf_type,
    bp.path_string as shortest_path,
    bp.path_length as hops_from_root,
    bp.link_types_used as path_link_types,
    (SELECT COUNT(*) FROM v_reachable_paths_from_root rpr WHERE rpr.target_url = bp.target_url) as alternative_paths
FROM best_paths bp
JOIN leaf_destinations ld ON bp.target_url = ld.target_url
WHERE bp.path_rank = 1  -- Only shortest path for each destination
ORDER BY bp.path_length, leaf_type, bp.target_url;

-- Add comment for documentation
COMMENT ON VIEW v_all_leaf_destinations IS 'Q1: Shows shortest paths from root to all leaf nodes with alternative path counts';