-- SiteScanner Database Schema for PostgreSQL
-- Converted from SQLite schema on 2025-07-31
-- Database: site_analysis (shared across projects)

-- Enable important PostgreSQL features
SET client_min_messages = warning;

-- Drop existing tables if they exist (for clean recreation)
DROP TABLE IF EXISTS crawl_state CASCADE;
DROP TABLE IF EXISTS resource_references CASCADE;
DROP TABLE IF EXISTS page_links CASCADE;
DROP TABLE IF EXISTS filesystem_images CASCADE;
DROP TABLE IF EXISTS discovered_resources CASCADE;
DROP TABLE IF EXISTS crawled_pages CASCADE;

-- Table: crawled_pages
-- Pages discovered through browser crawling from root
CREATE TABLE crawled_pages (
    url TEXT PRIMARY KEY,
    file_path TEXT NOT NULL,
    title TEXT,
    http_status INTEGER,
    error_message TEXT,
    discovery_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    crawl_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table: discovered_resources  
-- Images, CSS, JS, and external links found during crawling
CREATE TABLE discovered_resources (
    resource_url TEXT PRIMARY KEY,
    resource_type TEXT NOT NULL CHECK (resource_type IN ('image', 'external_link', 'css', 'js', 'other')),
    file_path TEXT, -- NULL for external links
    http_status INTEGER,
    error_message TEXT,
    file_size BIGINT,
    width INTEGER,
    height INTEGER,
    format TEXT -- 'JPEG', 'PNG', 'CSS', 'JS', etc.
);

-- Table: page_links
-- Navigation graph (page → page relationships)
CREATE TABLE page_links (
    source_url TEXT,
    target_url TEXT,
    link_type TEXT CHECK (link_type IN ('internal', 'external', 'fragment', 'navigation', 'content')),
    PRIMARY KEY (source_url, target_url)
);

-- Table: resource_references
-- Resource usage mapping (page → resource relationships)
CREATE TABLE resource_references (
    page_url TEXT,
    resource_url TEXT,
    reference_type TEXT CHECK (reference_type IN ('img_src', 'css_background', 'link_href', 'script_src', 'other')),
    PRIMARY KEY (page_url, resource_url, reference_type)
);

-- Table: filesystem_images
-- Complete filesystem inventory with reference flags
CREATE TABLE filesystem_images (
    file_path TEXT PRIMARY KEY,
    file_size BIGINT,
    width INTEGER,
    height INTEGER,
    format TEXT,
    is_referenced BOOLEAN DEFAULT FALSE
);

-- Table: crawl_state
-- Checkpointing data for crash recovery
CREATE TABLE crawl_state (
    session_id TEXT PRIMARY KEY,
    visited_urls JSONB, -- JSON array (PostgreSQL JSONB type)
    queue_urls JSONB,   -- JSON array (PostgreSQL JSONB type)
    checkpoint_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    pages_crawled INTEGER DEFAULT 0,
    resources_found INTEGER DEFAULT 0
);

-- Create indexes for performance
CREATE INDEX idx_crawled_pages_status ON crawled_pages(http_status);
CREATE INDEX idx_crawled_pages_timestamp ON crawled_pages(crawl_timestamp);
CREATE INDEX idx_discovered_resources_type ON discovered_resources(resource_type);
CREATE INDEX idx_discovered_resources_status ON discovered_resources(http_status);
CREATE INDEX idx_page_links_source ON page_links(source_url);
CREATE INDEX idx_page_links_target ON page_links(target_url);
CREATE INDEX idx_page_links_type ON page_links(link_type);
CREATE INDEX idx_resource_references_page ON resource_references(page_url);
CREATE INDEX idx_resource_references_resource ON resource_references(resource_url);
CREATE INDEX idx_resource_references_type ON resource_references(reference_type);
CREATE INDEX idx_filesystem_images_referenced ON filesystem_images(is_referenced);
CREATE INDEX idx_filesystem_images_format ON filesystem_images(format);
CREATE INDEX idx_filesystem_images_size ON filesystem_images(file_size);

-- Add foreign key constraints (PostgreSQL supports these, SQLite didn't enforce them)
-- Note: We're not adding FK constraints initially to allow flexible data loading
-- They can be added later once data integrity is verified

-- Add comments for documentation
COMMENT ON TABLE crawled_pages IS 'Pages discovered through browser crawling starting from root index.html';
COMMENT ON TABLE discovered_resources IS 'Images, CSS, JS, and external links found during crawling process';
COMMENT ON TABLE page_links IS 'Navigation graph showing relationships between pages';
COMMENT ON TABLE resource_references IS 'Mapping of which pages reference which resources';
COMMENT ON TABLE filesystem_images IS 'Complete inventory of image files found in filesystem';
COMMENT ON TABLE crawl_state IS 'Checkpointing data for crash recovery during long crawls';

COMMENT ON COLUMN crawled_pages.discovery_timestamp IS 'When this page URL was first discovered';
COMMENT ON COLUMN crawled_pages.crawl_timestamp IS 'When this page was actually crawled and processed';
COMMENT ON COLUMN discovered_resources.resource_type IS 'Type of resource: image, external_link, css, js, other';
COMMENT ON COLUMN page_links.link_type IS 'Type of link: internal, external, fragment, navigation, content';
COMMENT ON COLUMN resource_references.reference_type IS 'How resource is referenced: img_src, css_background, link_href, script_src, other';
COMMENT ON COLUMN filesystem_images.is_referenced IS 'Flag indicating if this image is referenced by any page';

-- Grant permissions (adjust as needed for your setup)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO sitescanner_user;

-- Display table creation summary
\echo 'SiteScanner PostgreSQL schema created successfully!'
\echo 'Tables created: crawled_pages, discovered_resources, page_links, resource_references, filesystem_images, crawl_state'
\echo 'Indexes created for performance optimization'
\echo 'Ready for SQL views and data migration'