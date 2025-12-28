# Contract: Recurring Tasks API

## Overview
This contract defines the expected behavior and interfaces for the recurring tasks feature in the CLI TODO application.

## CLI Commands Contract

### `todo recurring create`
**Purpose**: Create a new recurring task template

**Arguments**:
- `title` (required): The title of the recurring task

**Options**:
- `--pattern`: Recurrence pattern (daily, weekly, monthly, yearly)
- `--day`: Specific day(s) for the pattern (e.g., monday, 1st, etc.)
- `--month`: Specific month for yearly patterns
- `--interval`: Interval between occurrences (default: 1)
- `--end-never`: Never end the recurrence (default)
- `--end-after`: End after specified number of occurrences
- `--end-on`: End on specific date (YYYY-MM-DD format)
- `--description`: Task description
- `--priority`: Task priority (high, medium, low)
- `--tag`: Add tag to task (can be used multiple times)

**Success Response**:
- Exit code: 0
- Output: "Recurring task created successfully with ID: {id}"

**Error Responses**:
- Invalid pattern: Exit code 4, "Error: Invalid recurrence pattern"
- Invalid date: Exit code 5, "Error: Invalid date format"
- Invalid end condition: Exit code 6, "Error: Invalid end condition"

### `todo recurring list`
**Purpose**: List all recurring task templates

**Options**:
- `--status`: Filter by status (active, paused, completed)

**Success Response**:
- Exit code: 0
- Output: Tabular format showing ID, Status, Pattern, Title, Next Due Date

**Error Responses**:
- No recurring tasks: Exit code 0, "No recurring tasks found."

### `todo recurring update`
**Purpose**: Update an existing recurring task template

**Arguments**:
- `task_id` (required): ID of the recurring task template to update

**Options**:
- `--pattern`: New recurrence pattern
- `--day`: New specific day(s) for the pattern
- `--month`: New month for yearly patterns
- `--interval`: New interval between occurrences
- `--end-never`: Change to never-ending recurrence
- `--end-after`: Change to end after X occurrences
- `--end-on`: Change to end on specific date

**Success Response**:
- Exit code: 0
- Output: "Recurring task {id} updated successfully."

**Error Responses**:
- Task not found: Exit code 3, "Error: Recurring task with ID {id} not found."
- Invalid inputs: Appropriate error code and message

### `todo recurring pause`
**Purpose**: Pause a recurring task template (stop generating new instances)

**Arguments**:
- `task_id` (required): ID of the recurring task template to pause

**Success Response**:
- Exit code: 0
- Output: "Recurring task {id} paused successfully."

**Error Responses**:
- Task not found: Exit code 3, "Error: Recurring task with ID {id} not found."

### `todo recurring resume`
**Purpose**: Resume a paused recurring task template

**Arguments**:
- `task_id` (required): ID of the recurring task template to resume

**Success Response**:
- Exit code: 0
- Output: "Recurring task {id} resumed successfully."

**Error Responses**:
- Task not found: Exit code 3, "Error: Recurring task with ID {id} not found."
- Task not paused: Exit code 7, "Error: Recurring task {id} is not paused."

### `todo recurring delete`
**Purpose**: Delete a recurring task template

**Arguments**:
- `task_id` (required): ID of the recurring task template to delete

**Success Response**:
- Exit code: 0
- Output: "Recurring task {id} deleted successfully."

**Error Responses**:
- Task not found: Exit code 3, "Error: Recurring task with ID {id} not found."

## Data Model Contract

### Recurring Task Template
The recurring task template extends the base Task model with additional fields:

```python
class RecurringTaskTemplate:
    id: int  # Same as base Task.id
    title: str
    description: Optional[str]
    completed: bool  # Always False for templates
    created_at: str  # ISO format timestamp
    updated_at: str  # ISO format timestamp
    priority: str  # high, medium, low
    tags: List[str]
    due_date: Optional[str]  # Base due date for generated instances
    is_recurring_template: bool  # Always True
    recurrence_pattern_id: int  # Foreign key to RecurrencePattern
    next_instance_due: Optional[str]  # Next scheduled instance date
    end_condition_type: Optional[str]  # never, after_occurrences, on_date
    end_condition_value: Optional[str or int]  # Value for end condition
    is_active: bool  # Whether the template is currently generating instances
```

### Recurrence Pattern
```python
class RecurrencePattern:
    id: int
    pattern_type: str  # daily, weekly, monthly, yearly, custom
    interval: int  # Interval between occurrences
    days_of_week: Optional[List[str]]  # For weekly patterns
    days_of_month: Optional[List[int]]  # For monthly patterns
    months_of_year: Optional[List[str]]  # For yearly patterns
    occurrence_count: Optional[int]  # For patterns ending after X occurrences
    created_at: str
    updated_at: str
```

## Business Logic Contract

### Instance Generation
- New task instances are generated on-demand based on recurrence patterns
- Generated instances inherit properties from the template
- Each instance gets a unique ID and its own completion status
- Templates continue generating instances until an end condition is met

### End Conditions
- `never`: Template continues indefinitely (until manually paused/deleted)
- `after_occurrences`: Template stops after specified number of instances generated
- `on_date`: Template stops after the specified date (inclusive)

### State Management
- Active templates generate new instances according to their pattern
- Paused templates do not generate new instances
- Completed templates have reached their end condition and do not generate instances