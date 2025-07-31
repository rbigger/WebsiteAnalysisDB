# SiteScanner Backend

Python-based web crawler and analysis engine for static website optimization.

## Features

- Headless browser crawling with Selenium
- Comprehensive resource discovery
- Link validation and broken link detection
- Orphaned resource identification
- Navigation path analysis

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
# Basic crawling
python -m src.crawlers.site_scanner --url /path/to/site --db /path/to/db

# Run tests
pytest tests/
```

## Architecture

- `src/crawlers/`: Web crawling engines
- `src/analyzers/`: Data analysis modules
- `src/database/`: Database interfaces
- `tests/`: Unit and integration tests
