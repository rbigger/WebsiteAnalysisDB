-- Q5 View 4: Link type patterns and usage
-- PostgreSQL compatible version

CREATE VIEW v_link_type_patterns AS
SELECT 
    link_type,
    COUNT(*) as usage_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM page_links), 1) as usage_percentage,
    COUNT(DISTINCT source_url) as pages_using_this_type,
    COUNT(DISTINCT target_url) as unique_targets,
    
    -- Example source and target
    (SELECT source_url FROM page_links pl2 WHERE pl2.link_type = page_links.link_type LIMIT 1) as example_source,
    (SELECT target_url FROM page_links pl2 WHERE pl2.link_type = page_links.link_type LIMIT 1) as example_target
    
FROM page_links
GROUP BY link_type
ORDER BY usage_count DESC;

-- Add comment for documentation
COMMENT ON VIEW v_link_type_patterns IS 'Q5: Shows how different link types are used across the site for navigation pattern analysis';