# Data Model: Task Enhancements - Priorities, Tags, Search, Filter & Sort

**Feature**: 001-task-enhancements
**Date**: 2025-12-27

## Overview

This document defines the enhanced data model for the CLI TODO application to support priority assignment, tag categorization, search, filtering, and sorting functionality.

## Enhanced Task Model

### Task Entity

```python
@dataclass
class Task:
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: str = ""
    updated_at: str = ""
    priority: str = "medium"  # Values: "high", "medium", "low"
    tags: List[str] = None   # List of tag strings
    due_date: Optional[str] = None  # ISO format date string (YYYY-MM-DD or ISO 8601)
```

### Field Definitions

| Field | Type | Required | Default | Validation |
|-------|------|----------|---------|------------|
| id | int | Yes | N/A | Auto-incrementing, unique |
| title | str | Yes | N/A | 1-255 characters, non-empty |
| description | Optional[str] | No | None | 0-1000 characters |
| completed | bool | No | False | Boolean value |
| created_at | str | No | Current timestamp | ISO 8601 format |
| updated_at | str | No | Current timestamp | ISO 8601 format |
| priority | str | No | "medium" | One of: "high", "medium", "low" |
| tags | List[str] | No | [] | List of non-empty strings, max 50 chars each |
| due_date | Optional[str] | No | None | ISO 8601 date format (YYYY-MM-DD) |

### Priority Enum
- **high**: Top priority tasks requiring immediate attention
- **medium**: Normal priority tasks
- **low**: Low priority tasks, can be deferred

### Validation Rules

1. **Priority Validation**: Must be one of "high", "medium", "low"
2. **Tag Validation**: Each tag must be 1-50 characters, alphanumeric with hyphens/underscores
3. **Due Date Validation**: If present, must be in ISO 8601 format
4. **Title Uniqueness**: Within user's tasks (optional enhancement)

## State Transitions

### Task State Changes
- **Creation**: New task with default priority "medium", empty tags, no due date
- **Priority Update**: Priority changes from one level to another
- **Tag Update**: Tags added or removed from the list
- **Due Date Update**: Due date set, modified, or cleared
- **Completion**: Toggle between completed/incomplete states (existing functionality)

## Relationships

### Task-to-Tag Relationship
- One task can have multiple tags (0 to N tags)
- Tags are stored as a list within the task object
- Tags can be shared across multiple tasks

### Task-to-Priority Relationship
- One task has exactly one priority level
- Priority is an attribute of the task object

## JSON Serialization

### Task to JSON
```json
{
  "id": 1,
  "title": "Sample task",
  "description": "Sample description",
  "completed": false,
  "created_at": "2025-12-27T10:30:00",
  "updated_at": "2025-12-27T10:30:00",
  "priority": "high",
  "tags": ["work", "urgent"],
  "due_date": "2025-12-31"
}
```

### Backward Compatibility
- New fields (priority, tags, due_date) have default values
- Existing tasks without these fields will use defaults when loaded
- JSON serialization includes all fields for consistency

## Indexing Strategy

### Search Indexes
- **Title Index**: Full-text search on title field
- **Description Index**: Full-text search on description field
- **Tag Index**: Exact match on tags
- **Priority Index**: Exact match on priority level
- **Due Date Index**: Range queries on due date
- **Status Index**: Exact match on completion status

### Query Performance
- Search operations: O(n) where n is number of tasks (acceptable for up to 1000 tasks)
- Filter operations: O(n) with early termination where possible
- Sort operations: O(n log n) using Python's built-in sorting

## Data Integrity

### Consistency Rules
1. **Timestamp Consistency**: updated_at must be >= created_at
2. **Priority Consistency**: Only valid priority values allowed
3. **Tag Consistency**: No duplicate tags per task
4. **Date Consistency**: due_date should be >= current date (optional validation)

### Validation on Operations
- **Create**: Validate all input fields before creation
- **Update**: Validate changed fields before update
- **Delete**: No special validation required
- **Load**: Validate data structure on deserialization

## Extension Points

### Future Enhancements
- **Categories**: Hierarchical tag system
- **Subtasks**: Nested task relationships
- **Recurrence**: Repeating task patterns
- **Attachments**: File attachment support
- **Collaboration**: Shared task support (out of scope per constitution)

## Storage Format

### In-Memory Structure
- List of Task objects in TaskManager class
- Maintains insertion order with auto-incrementing IDs
- Supports JSON serialization to file

### File Format
- Single JSON file containing array of task objects
- Maintains same structure as in-memory representation
- Human-readable format for debugging