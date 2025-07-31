-- Q1 View 2: Find paths from root using recursive CTE  
-- PostgreSQL compatible version (simplified for compatibility)

CREATE VIEW v_reachable_paths_from_root AS  
WITH RECURSIVE path_finder AS (
    -- Base case: Start from root
    SELECT 
        '/site/index.html'::text as target_url,
        '/site/index.html'::text as path_string,
        0 as path_length,
        ''::text as link_types_used,
        '/site/index.html|'::text as visited_nodes
        
    UNION
    
    -- Recursive case: Follow page links only (simplified)
    SELECT 
        pl.target_url,
        pf.path_string || ' -> ' || pl.target_url,
        pf.path_length + 1,
        CASE 
            WHEN pf.link_types_used = '' THEN pl.link_type
            ELSE pf.link_types_used || ',' || pl.link_type 
        END,
        pf.visited_nodes || pl.target_url || '|'
    FROM path_finder pf
    JOIN page_links pl ON pf.target_url = pl.source_url
    WHERE pf.path_length < 10  -- Prevent infinite recursion
        AND pf.visited_nodes NOT LIKE '%' || pl.target_url || '|%'  -- Prevent cycles
)
SELECT DISTINCT
    target_url,
    path_string,
    path_length,
    link_types_used,
    -- Classify by path characteristics
    CASE 
        WHEN path_length = 1 THEN 'DIRECT - 1 hop from root'
        WHEN path_length = 2 THEN 'SHORT - 2 hops from root'  
        WHEN path_length = 3 THEN 'MEDIUM - 3 hops from root'
        WHEN path_length >= 4 THEN 'LONG - 4+ hops from root'
        ELSE 'ROOT'
    END as path_classification
FROM path_finder
WHERE target_url != '/site/index.html'  -- Exclude root itself
ORDER BY path_length, target_url;

-- Add comment for documentation
COMMENT ON VIEW v_reachable_paths_from_root IS 'Q1: Finds all navigation paths from root index.html using recursive traversal (page links only)';