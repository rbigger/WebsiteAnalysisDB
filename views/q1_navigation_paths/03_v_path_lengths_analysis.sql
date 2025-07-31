-- Q1 View 3: Path length analysis and statistics
-- PostgreSQL compatible version

CREATE VIEW v_path_lengths_analysis AS
WITH path_stats AS (
    SELECT 
        target_url,
        COUNT(*) as path_count,
        MIN(path_length) as shortest_path,
        MAX(path_length) as longest_path,
        AVG(path_length) as avg_path_length,
        STRING_AGG(DISTINCT path_classification, ', ') as path_variety  -- PostgreSQL uses STRING_AGG instead of GROUP_CONCAT
    FROM v_reachable_paths_from_root
    GROUP BY target_url
),
node_classification AS (
    SELECT 
        lns.node_url,
        lns.node_type, 
        lns.node_title,
        lns.leaf_status,
        CASE WHEN ps.target_url IS NOT NULL THEN 'REACHABLE' ELSE 'ORPHANED' END as reachability
    FROM v_leaf_nodes_summary lns
    LEFT JOIN path_stats ps ON lns.node_url = ps.target_url
)
SELECT 
    nc.node_url,
    nc.node_type,
    nc.node_title,
    nc.leaf_status,
    nc.reachability,
    COALESCE(ps.path_count, 0) as total_paths,
    COALESCE(ps.shortest_path, 999) as min_hops,
    COALESCE(ps.longest_path, 0) as max_hops,
    ROUND(COALESCE(ps.avg_path_length, 0), 1) as avg_hops,
    ps.path_variety
FROM node_classification nc
LEFT JOIN path_stats ps ON nc.node_url = ps.target_url
ORDER BY nc.reachability DESC, nc.leaf_status DESC, ps.shortest_path, nc.node_type;

-- Add comment for documentation
COMMENT ON VIEW v_path_lengths_analysis IS 'Q1: Analyzes path lengths and reachability statistics for all nodes from root';