# CLI Todo App

A command-line interface application for managing todo tasks efficiently. This application provides both interactive and command-line modes for managing your daily tasks.

## Features

- **Interactive Mode**: Engage with the application in a session-based environment
- **Command Line Mode**: Execute single commands for quick operations
- **Task Management**: Add, list, update, complete, and delete tasks
- **Persistent Storage**: Tasks are saved to a JSON file for persistence
- **Flexible Filtering**: List all, completed, or pending tasks
- **Task Descriptions**: Add detailed descriptions to your tasks

## Installation

1. Make sure you have Python 3.11+ installed on your system
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
- `add "Buy groceries" "Milk, eggs, bread"` - Add a new task with title and description
- `list` - List all tasks with their status
- `list completed` - List only completed tasks
- `list pending` - List only pending tasks
- `complete 1` - Mark task with ID 1 as complete (use `incomplete 1` to mark as incomplete)
- `update 1 "New title" "New description"` - Update task with ID 1
- `delete 1` - Delete task with ID 1
- `help` - Show available commands
- `q` or `quit` or `exit` - Exit the application

### Command Line Mode

You can also use the traditional command line mode for single operations:
```bash
python main.py add "Buy groceries" "Milk, eggs, bread"
python main.py list
python main.py list completed
python main.py list pending
python main.py update 1 "Buy groceries and cook dinner" "Milk, eggs, bread, chicken"
python main.py complete 1
python main.py incomplete 1
python main.py delete 1
python main.py help
```

## Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `add` | Add a new task | `add "Task title" "Task description"` |
| `list` | List all tasks | `list` or `list all` |
| `list completed` | List completed tasks | `list completed` |
| `list pending` | List pending tasks | `list pending` |
| `complete` | Mark task as complete | `complete 1` |
| `incomplete` | Mark task as incomplete | `incomplete 1` |
| `update` | Update task title and description | `update 1 "New title" "New description"` |
| `delete` | Delete a task | `delete 1` |
| `help` | Show help information | `help` |

## Exit Codes

- `0`: Success - Operation completed successfully
- `1`: General error - Unexpected error occurred
- `2`: Invalid input/command-line error - Incorrect command or arguments
- `3`: Task not found - Referenced task ID does not exist

## Examples

### Adding and Managing Tasks
```bash
# Add a new task
python main.py add "Complete project" "Finish the CLI todo app project"

# List all tasks
python main.py list

# Mark a task as complete
python main.py complete 1

# Update a task
python main.py update 1 "Complete project" "Finish the CLI todo app project and write documentation"

# Delete a task
python main.py delete 1
```

### Using Interactive Mode
```bash
# Start interactive mode
uv run main.py

# In the interactive mode:
add "Buy groceries" "Milk, eggs, bread, fruits"
list
complete 1
list completed
quit
```

## File Structure

The application stores tasks in a JSON file named `tasks.json` in the same directory as the application.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please file an issue in the repository.