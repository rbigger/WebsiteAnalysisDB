# CLAUDE.md - Project Documentation

This file provides guidance to Claude Code when working with the SiteScanner-App project and related repositories.

## Project Overview

**SiteScanner-App** - A comprehensive multi-language platform for analyzing static websites, identifying optimization opportunities, and managing content cleanup. Originally developed to analyze the HTTrack-downloaded robertiulo.com website.

**Current Status**: Production-ready application with complete PostgreSQL backend, analytical views, and data population scripts.

## 🏗️ Multi-Repository Architecture

This project is now organized across **4 GitHub repositories**:

1. **[SiteScanner-App](https://github.com/rbigger/SiteScanner-App)** - Main application
2. **[WebsiteAnalysisDB](https://github.com/rbigger/WebsiteAnalysisDB)** - Reusable database schema  
3. **[dev-environments](https://github.com/rbigger/dev-environments-)** - Shared development setup
4. **[ProjectScaffolding](https://github.com/rbigger/ProjectScaffolding)** - Project templates

## Database Architecture (PostgreSQL)

**Migration Completed**: Successfully migrated from SQLite to PostgreSQL with shared database strategy.

### Shared Databases (Cross-Project)
- `site_analysis` - Main analysis database with 6 core tables and 21+ analytical views
- `web_scraping_common` - Shared scraping patterns and rate limiting
- `resource_cache` - Cross-project resource optimization cache

### Core Tables (in site_analysis)
- **`crawled_pages`** - Website page inventory with metadata
- **`page_links`** - Inter-page relationships with link categorization  
- **`discovered_resources`** - Page assets (images, CSS, JavaScript, documents)
- **`page_content`** - Text content analysis and metadata
- **`error_log`** - Crawling and analysis error tracking
- **`analysis_metadata`** - Analysis session tracking and timestamps

### Analytical Views (21+ views)
- **Navigation Analysis**: `v_navigation_structure`, `v_reachable_paths_from_root`
- **Resource Optimization**: `v_orphaned_images`, `v_missing_images`, `v_large_resources`
- **Content Analysis**: `v_content_summary_by_directory`, `v_duplicate_titles`
- **Technical Health**: `v_broken_links`, `v_http_status_summary`

## 🚀 Quick Development Setup

### Prerequisites
- macOS with zsh shell
- PostgreSQL 15+ (installed via dev-environments)
- Python 3.9+
- Git access to all 4 repositories

### Environment Setup
```bash
# 1. Install shared development environment
git clone https://github.com/rbigger/dev-environments-.git
cd dev-environments
./scripts/install-dev-stack.sh

# 2. Clone main application
git clone https://github.com/rbigger/SiteScanner-App.git
cd SiteScanner-App

# 3. Set up Python environment
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 4. Initialize database schema
git clone https://github.com/rbigger/WebsiteAnalysisDB.git ../WebsiteAnalysisDB
psql -d site_analysis -f ../WebsiteAnalysisDB/schema/create_tables.sql
find ../WebsiteAnalysisDB/views/ -name "*.sql" -exec psql -d site_analysis -f {} \;
```

### Development Commands
```bash
# Generate sample data for testing
cd backend/scripts && python generate_sample_data.py

# Run basic website scan  
cd ../src && python main.py --url https://example.com

# Populate database from crawler output
cd ../scripts && python populate_from_crawler.py ../test-results/scan_output_*.txt

# Run analytical queries
psql -d site_analysis -c "SELECT * FROM v_orphaned_images_detail LIMIT 10;"
```

## 📁 Current Project Structure

```
SiteScanner-App/                    # Main application repository
├── backend/                       # Python crawler & analysis engine
│   ├── src/
│   │   ├── crawlers/basic_scanner.py    # Basic website scanner
│   │   ├── database/config.py           # PostgreSQL connection management
│   │   └── main.py                      # Main application entry point
│   ├── scripts/                         # Data population and utilities
│   │   ├── generate_sample_data.py      # Create test data
│   │   ├── populate_from_crawler.py     # Convert crawler output to DB
│   │   └── run_full_analysis.py         # Complete analysis pipeline
│   ├── tests/                           # PostgreSQL view tests
│   ├── tech-debt/                       # Technical debt documentation
│   └── requirements.txt                 # Python dependencies
├── database/                            # Project-specific database elements
│   ├── setup.sql                        # Project database configuration
│   └── README.md                        # Database documentation
├── frontend/                            # React dashboard (placeholder)
├── rust-analyzer/                       # Performance components (placeholder)
└── CLAUDE.md                            # This file
```

## 🔗 Related Repositories

### WebsiteAnalysisDB
- **Purpose**: Reusable PostgreSQL schema and analytical views
- **Contents**: Core tables, 21+ SQL views, schema documentation
- **Usage**: Shared across multiple website analysis projects

### dev-environments  
- **Purpose**: Shared development environment setup
- **Contents**: PostgreSQL, Redis, language stacks, installation scripts
- **Usage**: One-time setup for consistent development environment

### ProjectScaffolding
- **Purpose**: Project template system for rapid development
- **Contents**: Python web, React frontend, full-stack templates
- **Usage**: Create new projects with best practices built-in

## ✅ Current Implementation Status

### Completed Features
- ✅ **PostgreSQL Migration**: Successfully migrated from SQLite to PostgreSQL
- ✅ **Database Schema**: 6 core tables with proper relationships and constraints
- ✅ **Analytical Views**: 21+ PostgreSQL views for website analysis
- ✅ **Data Population**: Scripts to convert crawler output to database format
- ✅ **Sample Data Generation**: Test data creation for development
- ✅ **Multi-Repository Organization**: Clean separation of concerns
- ✅ **Comprehensive Documentation**: READMEs and setup guides for all components
- ✅ **GitHub Backup**: All repositories pushed to private GitHub repos

### Working Components
- **Basic Scanner** (`backend/src/crawlers/basic_scanner.py`) - Functional website crawler
- **Database Connection** (`backend/src/database/config.py`) - PostgreSQL connection management
- **Data Scripts** (`backend/scripts/`) - Population and sample data utilities
- **SQL Views** (WebsiteAnalysisDB repository) - 21+ analytical queries

### Architecture Decisions Made
- **Database**: PostgreSQL over SQLite for advanced features (CTEs, JSONB, performance)
- **Repository Strategy**: 4 separate repos for modularity and reusability
- **Shared Environment**: Common development setup across projects
- **Schema Separation**: Reusable database schema in separate repository

## 🎯 Key Analysis Capabilities

The system can answer these core questions:
1. **Navigation Paths**: Complete paths from root to leaf nodes
2. **Orphaned Resources**: Images and files not referenced by any page
3. **Broken Links**: 404s and other HTTP errors requiring repair
4. **Space Savings**: Potential cleanup candidates and storage optimization
5. **Site Structure**: Overall architecture and navigation patterns

---

## 📋 For New Claude Instances

### Essential Context
This is a **mature, production-ready project** with:
- Complete PostgreSQL backend with 21+ analytical views
- Working data population and sample generation scripts  
- 4 organized GitHub repositories with comprehensive documentation
- Proven architecture that successfully analyzed 19,854+ files across 4,634+ directories

### Original Use Case
- **Target Site**: HTTrack-downloaded WordPress recipe blog (robertiulo.com)
- **Site Stats**: ~19,854 files across 4,634 subdirectories
- **Challenge**: Identify orphaned resources, broken links, optimization opportunities
- **Success**: Successfully crawled 159 pages, identified navigation patterns

### Development Workflow
1. **Environment**: Use dev-environments repository for consistent setup
2. **Database**: All schema and views in WebsiteAnalysisDB repository  
3. **Application**: Main logic in SiteScanner-App repository
4. **Templates**: Use ProjectScaffolding for new related projects

### Key Files to Understand
- `backend/scripts/generate_sample_data.py` - Creates test data
- `backend/scripts/populate_from_crawler.py` - Converts crawler output to database
- `backend/src/crawlers/basic_scanner.py` - Core scanning functionality
- `backend/src/database/config.py` - PostgreSQL connection management

### Next Development Areas
- **Frontend Dashboard**: React-based visualization of analysis results
- **Rust Performance**: High-performance data processing components
- **Advanced Crawling**: JavaScript-heavy sites, dynamic content discovery
- **API Layer**: RESTful API for analysis results and crawler control

---

## 🔧 Technical Reference

### Key Dependencies
- **psycopg2-binary** - PostgreSQL database adapter for Python
- **selenium** - Headless Chrome automation for crawling
- **webdriver-manager** - Automatic ChromeDriver management  
- **beautifulsoup4** - HTML parsing and content extraction
- **Pillow** - Image processing and metadata extraction
- **pyyaml** - Configuration file parsing

### Platform Requirements
- **macOS** (primary) with zsh shell
- **PostgreSQL 15+** with shared database setup
- **Python 3.9+** with virtual environment support
- **Chrome/Chromium** for headless browser automation

### Repository URLs (Private)
- https://github.com/rbigger/SiteScanner-App.git
- https://github.com/rbigger/WebsiteAnalysisDB.git  
- https://github.com/rbigger/dev-environments-.git
- https://github.com/rbigger/ProjectScaffolding.git

---

## 🎯 Project Success Metrics

**Architecture Migration**: ✅ Successfully migrated from SQLite to PostgreSQL  
**Repository Organization**: ✅ 4 well-structured GitHub repositories  
**Data Pipeline**: ✅ Complete crawler → database → analysis workflow  
**Reusability**: ✅ Shared components for future website analysis projects  
**Documentation**: ✅ Comprehensive setup and usage guides  

This project represents a complete, production-ready website analysis platform with proven scalability and extensibility.