# Website Analysis Database Schema

**Reusable PostgreSQL database schema and views for website analysis applications**

A comprehensive database foundation for website crawling, analysis, and optimization projects. Provides shared schema, analytical views, and data population utilities that can be used across multiple website analysis applications.

## 🏗️ Architecture

This repository contains the core database infrastructure for website analysis:

- **Schema** - Core tables for pages, links, resources, and analysis data
- **Views** - 21+ analytical SQL views for common analysis patterns
- **Utilities** - Data population and sample data generation scripts
- **Migration** - Database setup and maintenance tools

## 📁 Repository Structure

```
WebsiteAnalysisDB/
├── README.md                 # This file
├── schema/
│   ├── create_tables.sql     # Core table definitions
│   └── README.md             # Schema documentation
├── views/                    # Analytical SQL views organized by category
│   ├── q1_navigation_paths/  # Navigation and link analysis
│   ├── q2_orphaned_images/   # Resource optimization views
│   ├── q3_broken_links/      # Link validation and health
│   ├── q4_space_savings/     # Site structure analysis
│   └── q5_site_structure/    # Performance and resource views
├── utilities/                # Data management scripts
│   ├── populate_from_crawler.py  # Convert crawler output to database
│   ├── generate_sample_data.py   # Create test data
│   └── README.md             # Utility documentation
└── migrations/               # Database version management
    └── README.md             # Migration documentation
```

## 🚀 Quick Start

### Prerequisites
- PostgreSQL 15+
- Python 3.9+ (for utilities)
- Access to shared databases: `site_analysis`, `web_scraping_common`, `resource_cache`

### Installation

```bash
# Clone the repository
git clone https://github.com/rbigger/WebsiteAnalysisDB.git
cd WebsiteAnalysisDB

# Install shared databases (if not already done)
createdb site_analysis
createdb web_scraping_common  
createdb resource_cache

# Install core schema
psql -d site_analysis -f schema/create_tables.sql

# Install analytical views
find views/ -name "*.sql" -exec psql -d site_analysis -f {} \;

# Verify installation
psql -d site_analysis -c "\dt"  # List tables
psql -d site_analysis -c "\dv"  # List views
```

### Quick Test with Sample Data

```bash
# Set up Python environment for utilities (if needed)
python3 -m venv .venv
source .venv/bin/activate
pip install psycopg2-binary pyyaml

# Note: utilities are included in SiteScanner-App repository
# This is a schema-only repository for reusability
# For sample data generation, use:
git clone https://github.com/rbigger/SiteScanner-App.git ../SiteScanner-App
cd ../SiteScanner-App/backend/scripts
python generate_sample_data.py

# Verify data population
psql -d site_analysis -c "SELECT COUNT(*) FROM crawled_pages;"
```

## 📊 Database Schema

### Core Tables

**crawled_pages** - Website page inventory
- `url` (Primary Key) - Page URL
- `file_path` - Local file system path
- `title` - Page title
- `http_status` - HTTP response status
- `crawl_timestamp` - When page was crawled

**page_links** - Inter-page relationships
- Links between pages with categorization
- Link types: internal, external, navigation, content

**discovered_resources** - Page assets and resources
- Images, CSS, JavaScript, documents
- Resource metadata and optimization data

**page_content** - Text content analysis
- Word counts, language detection
- Content categorization and metadata

**error_log** - Crawling and analysis errors
- Error tracking and debugging information

**analysis_metadata** - Analysis session tracking
- Crawl sessions, analysis runs, timestamps

### Analytical Views (21+ views)

**Navigation Analysis**
- `v_navigation_structure` - Site navigation hierarchy
- `v_reachable_paths_from_root` - Page accessibility analysis
- `v_page_link_density` - Link distribution patterns

**Resource Optimization**
- `v_orphaned_images` - Unused image detection
- `v_missing_images` - Broken image references
- `v_large_resources` - Performance optimization candidates

**Content Analysis**
- `v_content_summary_by_directory` - Content distribution
- `v_pages_by_language` - Multi-language site analysis
- `v_duplicate_titles` - SEO optimization opportunities

**Technical Health**
- `v_broken_links` - Link validation results
- `v_http_status_summary` - Overall site health
- `v_crawl_performance` - Crawling efficiency metrics

## 🔧 Integration

### Using with Projects

```python
# Example: Connect from your application
from database.config import DatabaseConnection

# Connect to shared analysis database
db = DatabaseConnection('shared')
conn = db.get_connection()

# Run analytical queries
cursor = conn.cursor()
cursor.execute("SELECT * FROM v_orphaned_images")
orphaned_images = cursor.fetchall()
```

### Data Population

```bash
# Note: Data population utilities are in SiteScanner-App
# Clone SiteScanner-App for full functionality:
git clone https://github.com/rbigger/SiteScanner-App.git

# From crawler output file
cd SiteScanner-App/backend/scripts
python populate_from_crawler.py /path/to/crawler_output.txt

# Generate test data for development
python generate_sample_data.py --pages 1000 --max-links 10
```

## 🔍 Common Use Cases

### Website Optimization
```sql
-- Find pages with no incoming links
SELECT * FROM v_orphaned_pages;

-- Identify large images for optimization
SELECT * FROM v_large_resources WHERE resource_type = 'image';

-- Check for broken links
SELECT * FROM v_broken_links WHERE http_status >= 400;
```

### Content Analysis
```sql
-- Content distribution across site sections
SELECT * FROM v_content_summary_by_directory;

-- Pages with duplicate titles (SEO issue)
SELECT * FROM v_duplicate_titles;

-- Navigation depth analysis
SELECT * FROM v_page_depth_analysis;
```

### Performance Monitoring
```sql
-- Crawl performance metrics
SELECT * FROM v_crawl_performance;

-- Resource loading patterns
SELECT * FROM v_resource_usage_patterns;

-- Site health overview
SELECT * FROM v_http_status_summary;
```

## 🤝 Compatible Projects

This database schema is designed to work with:

- **[SiteScanner-App](https://github.com/rbigger/SiteScanner-App)** - Website analysis application
- **[dev-environments](https://github.com/rbigger/dev-environments-)** - Shared development setup
- Any website crawler or analysis tool that follows the schema

## 📖 Documentation

- [Schema Documentation](schema/README.md) - Detailed table and column descriptions
- [View Documentation](views/README.md) - Analytical view usage examples
- [Utility Documentation](utilities/README.md) - Data population and management tools
- [Migration Guide](migrations/README.md) - Database version management

## 🔒 Data Privacy

- No personal or sensitive data stored in schema
- Focus on technical website structure and performance data
- Suitable for public website analysis and optimization

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Designed for comprehensive website analysis workflows
- Optimized for PostgreSQL performance and analytical queries
- Built for multi-project reusability and consistency

---

**Ready to analyze website structure and performance? Install the schema and start exploring your data!**
