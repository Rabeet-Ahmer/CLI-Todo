# CLI Todo App

A command-line interface application for managing todo tasks.

## Installation

1. Make sure you have Python 3.11+ installed
2. Install the required dependencies:
   ```bash
   uv pip install click
   ```
   or if using pip:
   ```bash
   pip install click
   ```

## Usage

### Interactive Mode (Recommended)
Run the application in interactive mode to perform multiple operations in a single session:
```bash
uv run main.py
```

In interactive mode, you can use the following commands:
- `add "Buy groceries" "Milk, eggs, bread"` - Add a new task
- `list` - List all tasks
- `list completed` - List completed tasks
- `list pending` - List pending tasks
- `complete 1` - Mark task as complete/incomplete
- `update 1 "New title" "New description"` - Update a task
- `delete 1` - Delete a task
- `help` - Show available commands
- `q` or `quit` or `exit` - Exit the application

### Command Line Mode
You can also use the traditional command line mode:
```bash
python main.py add "Buy groceries" "Milk, eggs, bread"
python main.py list
python main.py list completed
python main.py update 1 "Buy groceries and cook dinner" "Milk, eggs, bread, chicken"
python main.py complete 1
python main.py delete 1
```

## Exit Codes

- `0`: Success
- `1`: General error
- `2`: Invalid input/command-line error
- `3`: Task not found