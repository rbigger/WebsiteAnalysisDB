# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Website Structure Analysis** - Comprehensive analysis of the HTTrack-downloaded robertiulo.com website to understand its structure, identify all resources, detect broken links, and locate orphaned files for potential cleanup.

**Original Site**: WordPress recipe blog converted to static files via HTTrack Website Copier
**Purpose**: Complete resource inventory and structural analysis for optimization and maintenance

## Project Goals

1. **Complete Path Discovery**: Map all navigation paths from root index.html to leaf nodes (images, external links)
2. **Resource Inventory**: Identify ALL images in the site, both referenced and orphaned
3. **Broken Link Detection**: Find 404s and capture all error details for repair
4. **Structure Analysis**: Understand site architecture for potential restructuring and cleanup

## Database Schema

The analysis uses SQLite database at `/Users/rogerbigger/ForFriends/site_analysis.db` with 6 tables designed to answer key questions:

**`crawled_pages`** - Pages discovered through browser crawling from root
**`discovered_resources`** - Images and external links found during crawling  
**`page_links`** - Navigation graph (page → page relationships)
**`resource_references`** - Which pages reference which resources
**`filesystem_images`** - Complete filesystem image inventory
**`crawl_state`** - Checkpointing data for recovery

## Crawler Design

**Two-Phase Approach**:
1. **Browser Crawling**: Headless Chrome with Window Load Event detection starting from root
2. **Filesystem Inventory**: Complete scan of all image files to identify orphaned resources

**Key Features**:
- BFS traversal with circular reference detection
- Stays within domain (records but doesn't follow external links)
- Checkpointing for crash recovery
- Comprehensive resource discovery including JavaScript-loaded content

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run basic scanner for testing (implemented)
python basic_scanner.py [max_leaf_nodes]  # Default: 50

# Run the full crawler (when implemented)
python src/crawlers/site_structure_crawler.py --site-path /Users/rogerbigger/ForFriends/robertiulo_download/robertiulo.com --database /Users/rogerbigger/ForFriends/site_analysis.db

# Analyze results
python src/analyzers/structure_analyzer.py --database /Users/rogerbigger/ForFriends/site_analysis.db
```

## Project Structure

This project is organized as a monorepo with language-specific components:

```
SiteScanner/
├── backend/                 # Python crawler & analysis engine
│   ├── src/crawlers/        # Web crawling implementations
│   ├── tests/               # Test files with SQL views and dummy data
│   ├── tech-debt/           # Technical debt documentation
│   └── requirements.txt     # Python dependencies
├── database/                # SQLite schema, views, and queries
│   ├── schema/              # Table definitions
│   ├── views/q1_navigation/ # SQL views for each analysis question
│   └── migrations/          # Schema version management
├── .claude/                 # Claude development context and notes
│   ├── development-context.md    # Current project understanding
│   ├── session-notes/            # Development session history
│   ├── architecture-decisions/   # Technical decision documentation
│   └── file-mappings.md          # File organization documentation
└── scripts/setup/           # Development environment setup
```

## Development Environment and Context

### Environment Setup
This project uses the shared development environment system:

1. **General Setup**: See [General Development Guide](../../.claude/general-development-guide.md)
   - macOS/zsh platform requirements and conventions
   - Shared tooling (PostgreSQL, Redis, Chrome, etc.)
   - Common keyboard shortcuts and shell commands
   - Project creation and management workflows

2. **SiteScanner-Specific**: See [SiteScanner Development Guide](.claude/sitescanner-development-guide.md)
   - Project architecture and analysis questions
   - Database design and migration status
   - Crawler implementation and testing
   - Performance characteristics and troubleshooting

### Claude Development Context
The `.claude/` directory contains comprehensive development context:

- **`development-context.md`**: Current project status and architecture
- **`sitescanner-development-guide.md`**: Complete project-specific development guide
- **`session-notes/`**: Chronological development session documentation
- **`architecture-decisions/`**: Key technical decisions and rationale
- **`file-mappings.md`**: Documentation of file reorganizations
- **`todo-archive/`**: Historical progress tracking
- **`restart-instructions.md`**: Session recovery procedures

### Quick Reference
```zsh
# Set up shared environment (first time)
cd /Users/rogerbigger/dev/environments && ./scripts/install-dev-stack.sh

# Set up SiteScanner project
cd /Users/rogerbigger/dev/Projects/SiteScanner/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Create databases
createdb site_analysis && createdb site_analysis_test

# Run tests
pytest tests/ -v
```

## Project Status

### Completed
- ✅ Created requirements.txt with all dependencies
- ✅ Verified access to database and site folder
- ✅ Implemented basic_scanner.py for path discovery testing
- ✅ Fixed double-crawling optimization issue
- ✅ Added file output with timestamp and relative paths
- ✅ Organized project into monorepo structure
- ✅ Created all 5 analysis questions with test data and SQL views
- ✅ Documented technical debt (SQLite limitations)
- ✅ Established Claude development context system

### Basic Scanner Results
- Successfully crawled 159 pages to find 50 leaf nodes
- Discovered site has ~19,854 files across 4,634 subdirectories
- Found extensive cross-linking (queue grew to ~2,900 URLs)
- Identified WordPress structure: wp-content/, category/, tag/, etc.
- Leaf nodes are primarily images (92%) with some tag pages

### Technical Debt Documented
- **Database Strategy**: SQLite lacks stored procedures (see `backend/tech-debt/database-strategy.md`)
- **Decision Timeline**: Database choice review before full crawler implementation

### Next Steps
- Extract SQL views from test files to `database/views/q*_*/`
- Initialize git repository with organized structure
- Set up development environment with `scripts/setup/setup_dev_environment.sh`
- Implement full site_structure_crawler.py with database integration
- Add resource discovery (CSS backgrounds, JavaScript-loaded images)
- Implement filesystem scanner for orphaned file detection
- Add progress checkpointing for crash recovery

## Key Dependencies

- **selenium** (headless Chrome automation)
- **webdriver-manager** (automatic ChromeDriver management)
- **beautifulsoup4** (HTML parsing)
- **Pillow** (image processing and metadata)

## Data Sources

- **Root Page**: `/Users/rogerbigger/ForFriends/robertiulo_download/robertiulo.com/index.html`
- **Site Directory**: `/Users/rogerbigger/ForFriends/robertiulo_download/robertiulo.com/`
- **Analysis Database**: `/Users/rogerbigger/ForFriends/site_analysis.db`

## Key Questions the Database Answers

- What are all the navigation paths from root to leaf nodes?
- Which images are referenced vs. orphaned and can be safely deleted?
- What links are broken and need repair?
- How much space could be saved by removing unreferenced content?
- What is the overall site structure and navigation patterns?