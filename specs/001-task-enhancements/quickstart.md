# Quickstart Guide: Task Enhancements - Priorities, Tags, Search, Filter & Sort

**Feature**: 001-task-enhancements
**Date**: 2025-12-27

## Overview

This guide provides a quick introduction to the enhanced CLI TODO application with priority assignment, tag categorization, search, filtering, and sorting functionality.

## Prerequisites

- Python 3.11 or higher
- uv package manager
- Basic command-line knowledge

## Installation

The enhanced functionality is built into the main.py file. No additional installation required:

```bash
python main.py --help
```

## Quick Examples

### Adding Tasks with Priority and Tags

```bash
# Add a high priority work task with due date
todo add "Complete project proposal" --priority high --tag work --due-date 2025-12-31

# Add a personal task with multiple tags
todo add "Buy groceries" --priority medium --tag personal --tag shopping

# Add a low priority task
todo add "Learn new framework" --priority low --tag learning
```

### Viewing and Filtering Tasks

```bash
# List all tasks
todo list

# List only high priority tasks
todo list --priority high

# List tasks with specific tag
todo list --tag work

# List tasks sorted by due date
todo list --sort due-date --order asc

# List overdue tasks
todo list --overdue --pending
```

### Searching Tasks

```bash
# Search for tasks containing "project"
todo search "project"

# Search only in tags
todo search "work" --in-tags
```

### Updating Tasks

```bash
# Update task priority and add tags
todo update 1 --priority high --add-tag urgent

# Set or update due date
todo update 1 --due-date 2025-12-30

# Remove a tag
todo update 1 --remove-tag shopping
```

### Managing Tags

```bash
# List all tags in use
todo tag list

# List all tasks with a specific tag
todo tag tasks work
```

## Command Reference

### Task Management
- `todo add <title> [OPTIONS]` - Add new task with priority/tags/due date
- `todo list [OPTIONS]` - List tasks with filtering and sorting
- `todo search <query> [OPTIONS]` - Search tasks by keyword
- `todo complete <id>` - Mark task as complete
- `todo update <id> [OPTIONS]` - Update task details
- `todo delete <id>` - Delete task

### Tag Management
- `todo tag list` - List all unique tags
- `todo tag tasks <tag>` - List tasks with specific tag

## Priority Levels

- **high**: Tasks requiring immediate attention
- **medium**: Normal priority tasks (default)
- **low**: Tasks that can be deferred

## Common Use Cases

### Work Task Management
```bash
# Add work tasks with appropriate priority
todo add "Prepare presentation" --priority high --tag work --due-date 2025-12-30
todo add "Team meeting notes" --priority medium --tag work

# View all work tasks
todo list --tag work

# Focus on high priority work
todo list --tag work --priority high --sort priority --order desc
```

### Personal Task Organization
```bash
# Organize personal tasks by tags
todo add "Doctor appointment" --tag personal --tag health --due-date 2025-01-15
todo add "Grocery shopping" --tag personal --tag shopping

# View upcoming personal tasks
todo list --tag personal --sort due-date --order asc
```

## Tips and Best Practices

1. **Use consistent tags**: Establish a consistent set of tags across your tasks
2. **Set realistic due dates**: Use due dates to track actual deadlines, not just preferences
3. **Review priorities regularly**: Adjust priorities as your needs change
4. **Clean up old tasks**: Regularly review and complete or delete outdated tasks
5. **Use search for quick access**: Use search to quickly find specific tasks

## Troubleshooting

### Common Issues

**Invalid date format**: Make sure to use YYYY-MM-DD format (e.g., 2025-12-31)

**Invalid priority**: Use only "high", "medium", or "low" for priority values

**Task not found**: Verify the task ID exists using `todo list` first

## Next Steps

- Review the full help for each command: `todo <command> --help`
- Explore advanced filtering and sorting options
- Set up recurring tasks (if supported in future versions)
- Integrate with other tools in your workflow