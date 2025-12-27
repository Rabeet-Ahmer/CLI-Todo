# Research: Task Enhancements - Priorities, Tags, Search, Filter & Sort

**Feature**: 001-task-enhancements
**Date**: 2025-12-27

## Overview

Research into implementing priority assignment, tag categorization, search, filtering, and sorting functionality for the CLI TODO application. This analysis covers the current state of the application and the necessary changes to implement the requested features.

## Current State Analysis

### Existing Task Model
- Current `Task` class has: `id`, `title`, `description`, `completed`, `created_at`, `updated_at`
- Uses in-memory storage with JSON persistence
- CLI commands: `add`, `list`, `complete`, `update`, `delete`
- Current `list` command supports filtering by status (all/completed/pending)

### Required Enhancements
Based on the feature specification:
1. **Priority levels**: high/medium/low
2. **Tags/Categories**: work/home (and custom tags)
3. **Search functionality**: by keyword in title, description, or tags
4. **Filtering**: by status, priority, date
5. **Sorting**: by due date, priority, alphabetically

## Implementation Plan

### 1. Extended Task Model
- Add `priority` field (enum: high/medium/low, default: medium)
- Add `tags` field (list of strings)
- Add `due_date` field (ISO format string, optional)
- Update dataclass and JSON serialization

### 2. CLI Command Extensions
- Add `priority` parameter to `add` and `update` commands
- Add `--tag` option to `add` and `update` commands
- Add `--due-date` option to `add` and `update` commands
- Create new `search` command
- Enhance `list` command with additional filtering options
- Add sorting options to `list` command

### 3. Backend Logic
- Implement search algorithms (substring matching across title, description, tags)
- Implement filtering functions (status, priority, date ranges)
- Implement sorting functions (by priority, due date, title)
- Maintain backward compatibility with existing commands

## Technical Considerations

### Data Model Changes
- The Task dataclass needs extension with new attributes
- JSON serialization/deserialization needs updates
- Validation functions needed for new fields

### CLI Interface Design
- Follow Click conventions for new options
- Maintain backward compatibility
- Consistent help text and error messages
- Proper validation for new input types (dates, priority levels)

### Performance Considerations
- Search should be efficient for up to 1000 tasks
- Filtering and sorting should be fast
- Memory usage should remain reasonable

## Dependencies & Tools

### Current Dependencies
- Python 3.11
- Click for CLI framework
- Built-in modules (json, datetime, dataclasses, etc.)

### Potential New Dependencies
- No additional dependencies needed - can implement with built-in Python features

## Risk Assessment

### Low Risk Areas
- Adding new attributes to Task class
- Creating new CLI commands alongside existing ones
- JSON serialization updates

### Medium Risk Areas
- Maintaining backward compatibility with existing data
- Ensuring performance with larger datasets
- Proper input validation for new features

### Mitigation Strategies
- Thorough testing of JSON serialization/deserialization
- Input validation for new fields
- Performance testing with larger datasets

## Research Outcomes

### Decision: Task Model Extension
- Extend the existing Task dataclass with new fields rather than creating a new model
- This maintains consistency with existing architecture

### Rationale: Single File Approach
- Follows the user requirement to keep all code in main.py
- Maintains simplicity for the current scope
- Consistent with existing application structure

### Alternatives Considered
1. **Separate models for different features** - Rejected to maintain simplicity
2. **Database storage instead of JSON** - Rejected as it violates the constitution's in-memory storage requirement
3. **Complex search algorithms** - Rejected in favor of simple substring matching for performance

## Implementation Approach

### Phase 1: Core Model Changes
1. Extend Task class with new attributes
2. Update JSON serialization methods
3. Add validation functions

### Phase 2: CLI Extensions
1. Add priority and tag options to existing commands
2. Create new search command
3. Enhance list command with filters and sort options

### Phase 3: Business Logic
1. Implement search functionality
2. Implement filtering functions
3. Implement sorting functions

## Architecture Compliance

The planned implementation aligns with the CLI TODO App Constitution:
- Uses Python and Click as specified
- Maintains single-project structure
- Preserves CLI contract and backward compatibility
- Follows data integrity principles
- Meets performance standards
- Follows code quality requirements