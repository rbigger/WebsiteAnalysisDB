-- Q5 View 5: Most linked-to pages (authority/popularity)
-- PostgreSQL compatible version

CREATE VIEW v_most_linked_pages AS
SELECT 
    pl.target_url,
    cp.title as page_title,
    COUNT(*) as inbound_links,
    COUNT(DISTINCT pl.source_url) as unique_sources,
    COUNT(DISTINCT pl.link_type) as link_type_variety,
    STRING_AGG(DISTINCT pl.link_type, ', ') as link_types_received,  -- PostgreSQL uses STRING_AGG instead of GROUP_CONCAT
    
    -- Classify page importance
    CASE 
        WHEN COUNT(*) >= 6 THEN 'HIGH - Authority page (6+ inbound links)'
        WHEN COUNT(*) >= 3 THEN 'MEDIUM - Popular page (3-5 inbound links)'  
        WHEN COUNT(*) >= 1 THEN 'LOW - Linked page (1-2 inbound links)'
        ELSE 'ISOLATED - No inbound links'
    END as page_authority,
    
    -- Check if this page also links out (bidirectional connectivity)
    (SELECT COUNT(*) FROM page_links pl2 WHERE pl2.source_url = pl.target_url) as outbound_links
    
FROM page_links pl
LEFT JOIN crawled_pages cp ON pl.target_url = cp.url
GROUP BY pl.target_url, cp.title
ORDER BY inbound_links DESC, unique_sources DESC;

-- Add comment for documentation
COMMENT ON VIEW v_most_linked_pages IS 'Q5: Ranks pages by inbound links to identify authority/hub pages in site structure';