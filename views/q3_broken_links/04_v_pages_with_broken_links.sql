-- Q3 View 4: Pages that link to broken resources (need fixing)
-- PostgreSQL compatible version

CREATE VIEW v_pages_with_broken_links AS
SELECT 
    pl.source_url as page_with_broken_link,
    pl.target_url as broken_link,
    pl.link_type,
    COALESCE(cp.http_status, dr.http_status) as broken_status,
    COALESCE(cp.error_message, dr.error_message) as error_message,
    cp.title as page_title
FROM page_links pl
LEFT JOIN crawled_pages cp ON pl.target_url = cp.url AND cp.http_status != 200
LEFT JOIN discovered_resources dr ON pl.target_url = dr.resource_url AND dr.http_status != 200
WHERE cp.url IS NOT NULL OR dr.resource_url IS NOT NULL
ORDER BY pl.source_url, broken_status;

-- Add comment for documentation
COMMENT ON VIEW v_pages_with_broken_links IS 'Q3: Identifies pages that contain broken links and need fixing';