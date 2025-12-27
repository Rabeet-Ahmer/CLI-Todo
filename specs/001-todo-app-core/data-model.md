# Data Model: CLI Todo App

## Task Entity

### Attributes
- **id**: `int` - Unique identifier for the task (auto-incrementing)
- **title**: `str` - Title of the task (required, non-empty)
- **description**: `str` - Optional description of the task (nullable)
- **completed**: `bool` - Completion status (default: False)
- **created_at**: `str` - ISO format timestamp of creation (auto-generated)
- **updated_at**: `str` - ISO format timestamp of last update (auto-generated)

### Validation Rules
- **title**: Must be a non-empty string with length between 1-255 characters
- **description**: Optional, if provided must be less than 1000 characters
- **completed**: Boolean value only (True/False)
- **id**: Must be unique within the task collection
- **created_at**: Auto-generated upon task creation, follows ISO 8601 format
- **updated_at**: Auto-generated upon task creation and updates, follows ISO 8601 format

### State Transitions
- **Incomplete → Complete**: When user marks task as complete
- **Complete → Incomplete**: When user unmarks completed task
- **Any state → Deleted**: When user deletes the task (removal from collection)

## Task Collection

### Structure
- **tasks**: `list[Task]` - In-memory list of all tasks
- **next_id**: `int` - Counter for generating next unique ID (starts at 1)

### Operations
- **Add Task**: Append new task to collection, assign next available ID
- **Find Task**: Retrieve task by ID
- **Update Task**: Modify existing task by ID
- **Delete Task**: Remove task by ID
- **List Tasks**: Return filtered view of all tasks (all, completed, incomplete)

### Constraints
- All operations maintain data consistency
- IDs remain unique within the collection
- No duplicate tasks allowed
- Atomic operations for updates