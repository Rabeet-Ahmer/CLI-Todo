# Quickstart: Recurring Tasks Feature

## Overview
This guide provides a quick introduction to the recurring tasks feature in the CLI TODO application. Learn how to create, manage, and use recurring tasks that automatically generate new instances based on defined patterns.

## Prerequisites
- CLI TODO application installed and running
- Basic familiarity with the existing todo commands

## Creating Recurring Tasks

### Basic Recurring Task
Create a simple recurring task that repeats weekly:
```bash
todo recurring create "Weekly team meeting" --pattern weekly --day monday
```

### Advanced Recurring Task
Create a recurring task with specific options:
```bash
todo recurring create "Monthly report" --pattern monthly --day 1 --description "Monthly status report" --priority high --tag work
```

### Recurring Task with End Condition
Create a recurring task that ends after 5 occurrences:
```bash
todo recurring create "Daily workout" --pattern daily --end-after 7 --priority medium
```

## Available Patterns

### Daily Pattern
```bash
todo recurring create "Daily habit" --pattern daily
```

### Weekly Pattern
```bash
todo recurring create "Weekly review" --pattern weekly --day monday
# Multiple days:
todo recurring create "Team sync" --pattern weekly --day monday --day wednesday --day friday
```

### Monthly Pattern
```bash
todo recurring create "Monthly billing" --pattern monthly --day 1
```

### Yearly Pattern
```bash
todo recurring create "Annual review" --pattern yearly --day 31 --month december
```

## Managing Recurring Tasks

### List Recurring Tasks
View all recurring task templates:
```bash
todo recurring list
```

### Update Recurring Task
Modify an existing recurring task template:
```bash
todo recurring update 1 --pattern weekly --day tuesday
```

### Pause/Resume Recurring Task
Pause a recurring task (stops generating new instances):
```bash
todo recurring pause 1
```

Resume a paused recurring task:
```bash
todo recurring resume 1
```

### Delete Recurring Task
Remove a recurring task template:
```bash
todo recurring delete 1
```

## Viewing Generated Instances

Recurring task instances appear in your regular task list when generated:
```bash
# List all tasks (includes generated instances)
todo list

# Filter for recurring tasks
todo list --tag recurring
```

## End Conditions

### No End (Never)
```bash
todo recurring create "Daily habit" --pattern daily --end never
```

### After X Occurrences
```bash
todo recurring create "Training course" --pattern weekly --end-after 8
```

### On Specific Date
```bash
todo recurring create "Project check-in" --pattern weekly --end-on 2026-06-30
```

## Examples

### Weekly Meeting
```bash
todo recurring create "Team standup" --pattern weekly --day monday --day tuesday --day wednesday --day thursday --day friday --description "Daily team standup meeting" --priority medium
```

### Monthly Review
```bash
todo recurring create "Monthly budget review" --pattern monthly --day 15 --description "Review monthly budget and expenses" --priority high --tag finance
```

### Yearly Event
```bash
todo recurring create "Annual license renewal" --pattern yearly --day 1 --month january --description "Renew annual software licenses" --priority high
```

## Best Practices

1. **Use Descriptive Names**: Name your recurring tasks clearly to distinguish them from regular tasks
2. **Set Appropriate Priorities**: Set priorities that make sense for the recurring nature of the task
3. **Plan End Conditions**: Consider whether recurring tasks should run indefinitely or have a defined end
4. **Review Regularly**: Periodically review recurring tasks to ensure they're still relevant
5. **Use Tags**: Apply relevant tags to organize recurring tasks with other related tasks

## Troubleshooting

### Recurring Task Not Generating Instances
- Verify the recurrence pattern is correctly configured
- Check that the template is in ACTIVE state (not paused)
- Ensure the system date is current and correct

### Unexpected Task Generation
- Review the recurrence pattern and end conditions
- Check for overlapping recurrence patterns
- Verify timezone settings if applicable

### Performance Concerns
- The system generates instances on-demand to prevent performance issues
- Very complex recurrence patterns may impact performance
- Consider simplifying complex patterns if performance degrades