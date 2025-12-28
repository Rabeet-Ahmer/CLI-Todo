# Data Model: Recurring Tasks

## Overview
This document defines the data structures and relationships for the recurring tasks feature in the CLI TODO application. The design extends the existing task model while introducing new classes to manage recurrence patterns and templates.

## Entity: Task (Extended)
**Description**: The core Task entity is extended with recurrence metadata to support recurring functionality while maintaining compatibility with existing task operations.

**Fields**:
- `id`: int (primary key, auto-incrementing) - Existing field
- `title`: str - Existing field
- `description`: Optional[str] - Existing field
- `completed`: bool - Existing field
- `created_at`: str (ISO format timestamp) - Existing field
- `updated_at`: str (ISO format timestamp) - Existing field
- `priority`: str ("high", "medium", "low") - Existing field
- `tags`: List[str] - Existing field
- `due_date`: Optional[str] (YYYY-MM-DD format) - Existing field
- `is_recurring_template`: bool - New field indicating if this task is a recurring template
- `recurrence_pattern_id`: Optional[int] - New field linking to recurrence pattern
- `next_instance_due`: Optional[str] (YYYY-MM-DD format) - New field for next scheduled instance
- `end_condition_type`: Optional[str] ("never", "after_occurrences", "on_date") - New field
- `end_condition_value`: Optional[str or int] - New field for end condition value
- `last_generated_instance_id`: Optional[int] - New field for tracking last generated instance

**Relationships**:
- One-to-one with RecurrencePattern via `recurrence_pattern_id`
- One-to-many with Task instances (generated from this template)

## Entity: RecurrencePattern
**Description**: Defines the recurrence pattern for recurring tasks, including frequency, interval, specific days, and other recurrence rules.

**Fields**:
- `id`: int (primary key, auto-incrementing)
- `pattern_type`: str ("daily", "weekly", "monthly", "yearly", "custom")
- `interval`: int (e.g., every 2 weeks, every 3 months)
- `days_of_week`: Optional[List[str]] (e.g., ["monday", "wednesday", "friday"] for weekly patterns)
- `days_of_month`: Optional[List[int]] (e.g., [1, 15] for specific days of month)
- `months_of_year`: Optional[List[str]] (for yearly patterns)
- `occurrence_count`: Optional[int] (for patterns that end after X occurrences)
- `created_at`: str (ISO format timestamp)
- `updated_at`: str (ISO format timestamp)

**Validation Rules**:
- `interval` must be a positive integer
- For weekly patterns, `days_of_week` values must be valid day names
- For monthly patterns, `days_of_month` values must be 1-31
- `pattern_type` must be one of the allowed values

## Entity: RecurringTaskTemplate
**Description**: Represents a template for recurring tasks that defines the base task properties and recurrence pattern. This is essentially a Task entity with recurrence metadata.

**Fields**:
- `id`: int (primary key, same as the Task.id)
- `title`: str (base title for generated instances)
- `description`: Optional[str] (base description for generated instances)
- `priority`: str ("high", "medium", "low") (base priority for generated instances)
- `tags`: List[str] (base tags for generated instances)
- `due_date`: Optional[str] (base due date for generated instances)
- `recurrence_pattern_id`: int (foreign key to RecurrencePattern)
- `is_active`: bool (whether the template is currently generating instances)
- `created_at`: str (ISO format timestamp)
- `updated_at`: str (ISO format timestamp)
- `end_condition_type`: Optional[str] ("never", "after_occurrences", "on_date")
- `end_condition_value`: Optional[str or int]

**Relationships**:
- Many-to-one with RecurrencePattern via `recurrence_pattern_id`
- One-to-many with generated Task instances

## State Transitions

### RecurringTaskTemplate States
- **ACTIVE**: Template is generating new task instances according to its pattern
- **PAUSED**: Template is not generating new instances but can be resumed
- **COMPLETED**: Template has reached its end condition and will not generate more instances

**Transitions**:
- ACTIVE → PAUSED: When user pauses the recurring task
- PAUSED → ACTIVE: When user resumes the recurring task
- ACTIVE → COMPLETED: When end condition is reached
- PAUSED → COMPLETED: When end condition is reached while paused

### Task Instance States
- **PENDING**: New instance created from template, not yet completed
- **COMPLETED**: Instance marked as completed by user
- **SKIPPED**: Instance was not completed by its due date and was skipped

## Data Relationships

```
RecurringTaskTemplate (1) ←→ (n) Task (instances generated from template)
RecurringTaskTemplate (n) ←→ (1) RecurrencePattern
```

## Data Validation Rules

1. **Recurrence Pattern Validation**:
   - A recurring task must have a valid recurrence pattern
   - End condition must be consistent with pattern type
   - Dates must be valid and in the future when specified

2. **Task Instance Validation**:
   - Generated instances inherit properties from template
   - Instance due dates must be consistent with recurrence pattern
   - Instance titles may include date suffixes for clarity

3. **Template Validation**:
   - Recurring templates cannot be marked as completed (only paused)
   - Templates must have valid end conditions
   - Templates must reference existing recurrence patterns

## Persistence Considerations

### JSON Storage Format
The existing tasks.json format will be extended to include recurrence metadata:

```json
{
  "id": 1,
  "title": "Weekly team meeting",
  "description": "Team sync meeting",
  "completed": false,
  "created_at": "2025-12-28T10:00:00",
  "updated_at": "2025-12-28T10:00:00",
  "priority": "medium",
  "tags": ["work", "meeting"],
  "due_date": null,
  "is_recurring_template": true,
  "recurrence_pattern_id": 1,
  "next_instance_due": "2025-01-05",
  "end_condition_type": "never",
  "end_condition_value": null,
  "last_generated_instance_id": 5
}
```

### Recurrence Pattern Storage
Recurrence patterns will be stored in a separate structure within the same JSON file or as a reference:

```json
{
  "id": 1,
  "pattern_type": "weekly",
  "interval": 1,
  "days_of_week": ["sunday"],
  "created_at": "2025-12-28T10:00:00",
  "updated_at": "2025-12-28T10:00:00"
}
```

## Extensibility Considerations

The data model is designed to support future enhancements:
- Additional pattern types can be added to `pattern_type` enum
- New end condition types can be added to `end_condition_type`
- Timezone-specific recurrence can be added as additional fields
- Advanced recurrence rules (like "last Monday of month") can be implemented through custom patterns