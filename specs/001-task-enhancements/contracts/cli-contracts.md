# CLI Command Contracts: Task Enhancements

**Feature**: 001-task-enhancements
**Date**: 2025-12-27

## Overview

This document defines the CLI command contracts for the enhanced task functionality including priority assignment, tag categorization, search, filtering, and sorting.

## Extended Commands

### 1. `add` Command (Enhanced)

#### Current Signature
```
todo add <title> [description]
```

#### Enhanced Signature
```
todo add <title> [description] [OPTIONS]
```

#### Options
- `--priority`, `-p`: Set priority level (high, medium, low) [default: medium]
- `--tag`, `-t`: Add tag to task (can be used multiple times)
- `--due-date`, `-d`: Set due date (YYYY-MM-DD format)

#### Examples
```
todo add "Complete report" "Finish the quarterly report" --priority high --tag work --due-date 2025-12-31
todo add "Buy groceries" --tag personal --priority medium
todo add "Fix bug" --due-date 2025-12-30 --tag work --tag urgent
```

#### Validation
- Priority must be one of: high, medium, low
- Tags must be 1-50 alphanumeric characters (hyphens/underscores allowed)
- Due date must be in YYYY-MM-DD format

### 2. `update` Command (Enhanced)

#### Current Signature
```
todo update <task_id> <title> [description]
```

#### Enhanced Signature
```
todo update <task_id> [OPTIONS]
```

#### Options
- `--title`: Update task title
- `--description`: Update task description
- `--priority`, `-p`: Update priority level (high, medium, low)
- `--add-tag`, `-a`: Add tag to task (can be used multiple times)
- `--remove-tag`, `-r`: Remove tag from task (can be used multiple times)
- `--due-date`, `-d`: Update due date (YYYY-MM-DD format)
- `--clear-due-date`: Remove due date

#### Examples
```
todo update 1 --priority high --add-tag urgent
todo update 1 --remove-tag personal --add-tag work
todo update 1 --due-date 2025-12-31 --priority low
todo update 1 --clear-due-date
```

#### Validation
- All validation rules from `add` command apply
- Task ID must exist
- Cannot specify both `--add-tag` and `--remove-tag` with same tag

## New Commands

### 3. `search` Command (New)

#### Signature
```
todo search <query>
```

#### Options
- `--in-title`: Search in title only
- `--in-description`: Search in description only
- `--in-tags`: Search in tags only
- `--all-fields`: Search in all fields (default)

#### Examples
```
todo search "report"
todo search "urgent" --in-tags
todo search "meeting" --in-title
```

#### Output Format
```
ID   Status Priority Title                      Due Date     Tags
--   ------ -------- -----                      --------     ----
1    [x]    high     Complete report            2025-12-31   work,urgent
5    [ ]    medium   Schedule team meeting      2025-12-28   work
```

### 4. `list` Command (Enhanced)

#### Current Signature
```
todo list [status]
```

#### Enhanced Signature
```
todo list [OPTIONS]
```

#### Options
- `--status`: Filter by status (all, completed, pending) [default: all]
- `--priority`: Filter by priority (high, medium, low)
- `--tag`: Filter by tag (can be used multiple times)
- `--completed`: Show only completed tasks
- `--pending`: Show only pending tasks
- `--overdue`: Show only overdue tasks
- `--sort`: Sort by (id, title, priority, due-date, created-date, updated-date) [default: id]
- `--order`: Sort order (asc, desc) [default: asc]
- `--due-before`: Show tasks due before date (YYYY-MM-DD)
- `--due-after`: Show tasks due after date (YYYY-MM-DD)

#### Examples
```
todo list --priority high --sort priority --order desc
todo list --tag work --completed
todo list --sort due-date --order asc
todo list --due-before 2025-12-31 --pending
```

#### Output Format
```
ID   Status Priority Title                      Due Date     Tags
--   ------ -------- -----                      --------     ----
1    [x]    high     Complete report            2025-12-31   work,urgent
3    [ ]    medium   Review code                2025-12-29   work
5    [ ]    low      Research new tools         2025-01-15   personal
```

### 5. `tag` Command (New)

#### Signature
```
todo tag [OPTIONS]
```

#### Subcommands
- `todo tag list`: List all unique tags in use
- `todo tag tasks <tag_name>`: List all tasks with specific tag

#### Examples
```
todo tag list
todo tag tasks work
```

#### Output Format for `tag list`:
```
Tags in use:
- work
- personal
- urgent
- home
```

#### Output Format for `tag tasks <tag_name>`:
```
Tasks with tag 'work':
ID   Status Priority Title                      Due Date
--   ------ -------- -----                      --------
1    [x]    high     Complete report            2025-12-31
3    [ ]    medium   Review code                2025-12-29
```

## Exit Codes

### Consistent Exit Codes
- `0`: Success
- `1`: General error
- `2`: Input validation error
- `3`: Task not found
- `4`: Invalid priority value
- `5`: Invalid date format
- `6`: Invalid tag format

## Error Messages

### Standard Error Format
```
Error: [descriptive message] (exit code: N)
```

### Common Error Cases
- **Invalid priority**: "Error: Priority must be one of: high, medium, low (exit code: 4)"
- **Invalid date**: "Error: Date must be in YYYY-MM-DD format (exit code: 5)"
- **Invalid tag**: "Error: Tags must be 1-50 alphanumeric characters (exit code: 6)"
- **Task not found**: "Error: Task with ID X not found (exit code: 3)"

## Help Text

### Enhanced Help Format
All commands include comprehensive help text accessible via `--help` flag, following Click conventions with clear descriptions, parameter explanations, and usage examples.

## Backward Compatibility

### Compatibility Guarantees
- All existing command signatures continue to work
- New options are optional with sensible defaults
- Existing JSON data files remain compatible
- All existing functionality preserved