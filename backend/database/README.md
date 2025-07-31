# SiteScanner Database Integration

This directory contains project-specific database elements for the SiteScanner application analyzing robertiulo.com.

## Files

- **`setup.sql`** - Project-specific database setup (indexes, views, config)
- **`sample_data.sql`** - Sample data for testing (generated separately)
- **`custom_queries.sql`** - Analysis queries specific to robertiulo.com

## Setup Instructions

### 1. Install Base Schema (One-time)
First, install the base WebsiteAnalysisDB schema:
```bash
# Clone and install base database schema (when available)
git clone [WebsiteAnalysisDB-repo-url]
cd WebsiteAnalysisDB
psql -d site_analysis -f create_schema.sql
psql -d site_analysis -f views/create_all_views.sql
```

### 2. Install Project-Specific Setup
Then add SiteScanner-specific enhancements:
```bash
cd /Users/rogerbigger/dev/Projects/SiteScanner/backend
psql -d site_analysis -f database/setup.sql
```

### 3. Populate Data
Use the data population scripts:
```bash
# Option A: Populate from existing crawler output
python3 scripts/populate_from_crawler.py

# Option B: Run fresh crawl and populate
python3 scripts/run_full_analysis.py

# Option C: Generate sample data for testing
python3 scripts/generate_sample_data.py
```

## Project-Specific Database Elements

### Indexes
- **WordPress structure**: Optimized for `/wp-content/`, `/category/`, `/tag/` patterns
- **Content theme**: Italian cuisine, recipe, food content
- **Gallery pages**: Handles both `gallery` and `galllery` (site typo)
- **Large images**: Focus on images >100KB for optimization analysis

### Views
- **`v_robertiulo_content_categories`**: Categorizes pages by content type
  - Recipe pages
  - Gallery pages  
  - Essay pages
  - About pages
  - Instructions
  - Homepage

### Configuration Table
- **`project_config`**: Stores project-specific settings
  - Target site path
  - Site theme and focus
  - Expected page counts
  - Last crawl timestamps

## Database Connection

The application uses the shared `site_analysis` database with project-specific enhancements:

```python
from database import get_db_connection

# Connect to shared database with project customizations
with get_db_connection('primary') as db:
    results = db.execute_query("SELECT * FROM v_robertiulo_content_categories")
```

## Analysis Workflow

1. **Crawl**: Discover pages and resources
2. **Populate**: Insert discoveries into base tables
3. **Analyze**: Query views for insights
4. **Report**: Export findings and recommendations

The project-specific setup enhances the base schema for optimal analysis of the robertiulo.com website structure and content.