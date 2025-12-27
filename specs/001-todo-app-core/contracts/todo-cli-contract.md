# CLI Contract: Todo App

## Command Structure

### `todo add <title> [description]`
- **Purpose**: Add a new todo task
- **Parameters**:
  - `title` (required): Task title (string)
  - `description` (optional): Task description (string)
- **Options**: None
- **Output**: Success message with assigned task ID
- **Exit Code**: 0 on success, non-zero on error
- **Validation**: Title must not be empty

### `todo list [status]`
- **Purpose**: Display all tasks or filter by completion status
- **Parameters**:
  - `status` (optional): Filter by status (all, completed, pending)
- **Options**: None
- **Output**: Formatted list of tasks with IDs and status
- **Exit Code**: 0 on success, non-zero on error

### `todo update <id> <title> [description]`
- **Purpose**: Update an existing task's title and/or description
- **Parameters**:
  - `id` (required): Task identifier (integer)
  - `title` (required): New task title (string)
  - `description` (optional): New task description (string)
- **Options**: None
- **Output**: Success message
- **Exit Code**: 0 on success, non-zero on error
- **Validation**: Task with given ID must exist

### `todo complete <id>`
- **Purpose**: Mark a task as complete
- **Parameters**:
  - `id` (required): Task identifier (integer)
- **Options**: None
- **Output**: Success message
- **Exit Code**: 0 on success, non-zero on error
- **Validation**: Task with given ID must exist

### `todo delete <id>`
- **Purpose**: Delete a task
- **Parameters**:
  - `id` (required): Task identifier (integer)
- **Options**: None
- **Output**: Success message
- **Exit Code**: 0 on success, non-zero on error
- **Validation**: Task with given ID must exist

## Exit Codes

- `0`: Success
- `1`: General error
- `2`: Invalid input/command-line error
- `3`: Task not found

## Error Messages

All error messages will be human-readable and provide actionable feedback to the user.

## Output Format

Task lists will be displayed in a tabular format with columns for ID, Status, Title, and Description.