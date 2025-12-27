# Quickstart Guide: CLI Todo App

## Installation

1. Ensure you have Python 3.11+ installed
2. Install the required dependencies:
   ```bash
   uv pip install click
   ```

## Usage

### Add a new task
```bash
python -m todo_cli.main add "Buy groceries"
```

### List all tasks
```bash
python -m todo_cli.main list
```

### Update a task
```bash
python -m todo_cli.main update 1 "Buy groceries and cook dinner"
```

### Mark a task as complete
```bash
python -m todo_cli.main complete 1
```

### Delete a task
```bash
python -m todo_cli.main delete 1
```

### View help
```bash
python -m todo_cli.main --help
```

## Task Status Indicators

- `[ ]` - Incomplete task
- `[x]` - Completed task

## Data Persistence

Tasks are automatically saved to `tasks.json` in the current directory when you perform operations. The file is loaded when the application starts.

## Example Workflow

```bash
# Add tasks
python -m todo_cli.main add "Complete project proposal"
python -m todo_cli.main add "Schedule team meeting"
python -m todo_cli.main add "Review documentation"

# View all tasks
python -m todo_cli.main list

# Mark a task as complete
python -m todo_cli.main complete 1

# Update a task
python -m todo_cli.main update 2 "Schedule team meeting for Friday"

# View updated list
python -m todo_cli.main list
```