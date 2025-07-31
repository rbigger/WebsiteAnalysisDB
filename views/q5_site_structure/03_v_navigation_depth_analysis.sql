-- Q5 View 3: Navigation depth and connectivity analysis
-- PostgreSQL compatible version

CREATE VIEW v_navigation_depth_analysis AS
SELECT 
    pl.source_url,
    cp.title as source_title,
    COUNT(*) as outbound_links,
    COUNT(DISTINCT pl.link_type) as link_types_used,
    STRING_AGG(DISTINCT pl.link_type, ', ') as link_types_list,  -- PostgreSQL uses STRING_AGG instead of GROUP_CONCAT
    
    -- Classify pages by their role in navigation
    CASE 
        WHEN COUNT(*) >= 8 THEN 'Hub Page (8+ outbound links)'
        WHEN COUNT(*) >= 4 THEN 'Connector Page (4-7 outbound links)'
        WHEN COUNT(*) >= 1 THEN 'Standard Page (1-3 outbound links)'
        ELSE 'Dead End (0 outbound links)'
    END as navigation_role,
    
    -- Check if this page is linked TO by others (inbound links)
    (SELECT COUNT(*) FROM page_links pl2 WHERE pl2.target_url = pl.source_url) as inbound_links
    
FROM page_links pl
LEFT JOIN crawled_pages cp ON pl.source_url = cp.url
GROUP BY pl.source_url, cp.title
ORDER BY outbound_links DESC, inbound_links DESC;

-- Add comment for documentation
COMMENT ON VIEW v_navigation_depth_analysis IS 'Q5: Analyzes navigation depth and classifies pages by their connectivity role';