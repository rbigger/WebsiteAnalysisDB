-- Q1 View 1: Identify all leaf nodes (pages/resources with no outgoing internal links)
-- PostgreSQL compatible version

CREATE VIEW v_leaf_nodes_summary AS
WITH all_nodes AS (
    -- All pages
    SELECT url as node_url, 'page' as node_type, title as node_title, url as source_location
    FROM crawled_pages
    
    UNION ALL
    
    -- All resources  
    SELECT resource_url as node_url, resource_type as node_type, 
           resource_type || ' resource' as node_title, resource_url as source_location
    FROM discovered_resources
),
nodes_with_outbound AS (
    -- Nodes that have outgoing internal links
    SELECT DISTINCT pl.source_url as node_url
    FROM page_links pl
    WHERE pl.target_url LIKE '/site/%'  -- Internal links only
    
    UNION
    
    SELECT DISTINCT rr.page_url as node_url  
    FROM resource_references rr
    WHERE rr.resource_url LIKE '/site/%'  -- Internal resources only
)
SELECT 
    an.node_url,
    an.node_type,
    an.node_title,
    CASE WHEN nwo.node_url IS NULL THEN 'LEAF' ELSE 'NON-LEAF' END as leaf_status,
    -- Count inbound links to this node
    COALESCE((SELECT COUNT(*) FROM page_links pl2 WHERE pl2.target_url = an.node_url), 0) +
    COALESCE((SELECT COUNT(*) FROM resource_references rr2 WHERE rr2.resource_url = an.node_url), 0) as inbound_links
FROM all_nodes an
LEFT JOIN nodes_with_outbound nwo ON an.node_url = nwo.node_url
ORDER BY leaf_status DESC, inbound_links DESC, an.node_type, an.node_url;

-- Add comment for documentation
COMMENT ON VIEW v_leaf_nodes_summary IS 'Q1: Identifies all leaf nodes (pages/resources with no outgoing internal links) for navigation path analysis';