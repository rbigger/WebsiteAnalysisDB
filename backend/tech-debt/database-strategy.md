# Technical Debt: Database Strategy Review

## Issue: SQLite Stored Procedure Limitations

**Date:** 2025-07-31  
**Priority:** Medium  
**Impact:** Architecture Design

### Problem Statement

SQLite does not support stored procedures, which limits our ability to encapsulate complex business logic at the database layer. Our current architecture assumes stored procedure capabilities that don't exist in SQLite.

### Current Workarounds

1. **SQL Views**: Static SELECT queries in `database/views/q1_navigation/`, etc.
2. **Python Methods**: Complex logic implemented in Python rather than SQL
3. **Inline SQL**: Ad-hoc queries mixed with application code

### Limitations Identified

- **No Stored Procedures**: Cannot encapsulate complex multi-step operations
- **No User-Defined Functions**: Limited extensibility for custom calculations
- **No Advanced Control Flow**: No IF/ELSE, WHILE loops, etc. in SQL
- **No Transaction Control**: Limited BEGIN/COMMIT/ROLLBACK capabilities within procedures

### Potential Solutions

#### Option 1: Continue with SQLite + Python Hybrid
- **Pros**: Lightweight, portable, no additional dependencies
- **Cons**: Business logic scattered between SQL views and Python code
- **Effort**: Low (current approach)

#### Option 2: Migrate to PostgreSQL
- **Pros**: Full stored procedure support, advanced SQL features, better performance for large datasets
- **Cons**: Additional deployment complexity, requires PostgreSQL server
- **Effort**: High (significant refactoring required)

#### Option 3: Hybrid Approach with SQLite Extensions
- **Pros**: Keep SQLite portability, add custom functions via C extensions
- **Cons**: Platform-specific compilation, maintenance overhead
- **Effort**: Medium

#### Option 4: Structured Python Database Layer
- **Pros**: Clean separation of concerns, testable business logic, maintains SQLite simplicity
- **Cons**: More Python code to maintain
- **Effort**: Medium

### Recommended Next Steps

1. **Document current architecture**: Map which logic lives in SQL vs Python
2. **Evaluate data volume requirements**: Will the 19,854+ files strain SQLite?
3. **Create database abstraction layer**: Prepare for potential migration
4. **Benchmark performance**: Test SQLite with realistic data loads

### Files Affected

- `database/views/q*_*/` - Current "stored procedure" implementations as views
- `backend/src/database/` - Future home for procedural logic
- All test files in `backend/tests/` - May need refactoring if database changes

### Decision Timeline

**Target Decision Date:** Before implementing full site crawler (est. 2-3 weeks)

### Notes

- Current test framework with dummy data works well regardless of database choice
- Migration complexity increases significantly once real data is in production
- Consider data export/import strategies for any database transition