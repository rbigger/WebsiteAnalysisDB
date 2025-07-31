# Technical Debt Tracking

This directory tracks technical debt, architectural decisions that need review, and known limitations in the SiteScanner project.

## Current Items

### High Priority
- None currently

### Medium Priority
- [Database Strategy Review](./database-strategy.md) - SQLite stored procedure limitations

### Low Priority
- None currently

## Guidelines

When adding technical debt items:

1. **Create a descriptive filename**: `issue-name.md`
2. **Include standard headers**:
   - Date
   - Priority (High/Medium/Low)
   - Impact (Performance/Architecture/Maintenance/Security)
3. **Document**:
   - Problem statement
   - Current workarounds
   - Potential solutions with effort estimates
   - Files affected
   - Decision timeline

## Review Process

Technical debt should be reviewed:
- Before major feature implementations
- During sprint planning
- When performance issues arise
- Before production deployment