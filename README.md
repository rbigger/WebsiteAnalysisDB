# SiteScanner-App - Website Structure Analysis Platform

A comprehensive multi-language platform for analyzing static websites, identifying optimization opportunities, and managing content cleanup.

## 🏗️ Architecture

This monorepo contains all components of the SiteScanner platform:

- **Backend** (Python): Core crawler and analysis engine
- **Database**: PostgreSQL integration with shared analysis schema
- **Rust Analyzer**: High-performance data processing
- **Frontend** (React): Interactive analysis dashboard
- **Scripts**: Deployment and automation tools

## 📁 Project Structure

```
SiteScanner-App/
├── backend/          # Python crawler & analysis engine
├── database/         # PostgreSQL schema & project-specific elements
├── rust-analyzer/    # Performance-critical processing
├── frontend/         # React web dashboard
├── scripts/          # Automation & deployment
├── docker/           # Container definitions
└── docs/             # Architecture & API docs
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Rust 1.70+
- PostgreSQL 15+

### Setup
```bash
# Install shared development environment (first time only)
cd /Users/rogerbigger/dev/environments
./scripts/install-dev-stack.sh

# Clone the repository
git clone https://github.com/yourusername/SiteScanner-App.git
cd SiteScanner-App

# Set up Python environment
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set up project-specific databases
createdb sitescanner_dev
createdb sitescanner_test

# Initialize schema (shared schema is installed via dev-environments)
psql -d sitescanner_dev -f database/schema/create_tables.sql
```

### Component Development
See individual component READMEs:
- [Backend Development](./backend/README.md)
- [Database Management](./database/README.md)
- [Frontend Development](./frontend/README.md)
- [Rust Components](./rust-analyzer/README.md)

## 📖 Documentation

- [Architecture Overview](./docs/architecture/overview.md)
- [API Reference](./docs/api/README.md)
- [Development Guide](./docs/guides/development.md)
- [Deployment Guide](./docs/guides/deployment.md)

## 🤝 Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
