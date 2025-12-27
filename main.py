import json
import os
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import click


# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Set up basic Click CLI structure with "todo" group
@click.group()
def cli():
    """CLI Todo Application - Manage your tasks from the command line"""
    pass


# Add comprehensive help text for all commands following Click conventions (T044)
# Implement consistent exit codes across all commands (0=success, 1=general error, 2=input error, 3=task not found) (T043)
# Implement proper error handling for file I/O operations with appropriate messages (T045)


@cli.command()
@click.argument('title')
@click.argument('description', required=False)
def add(title, description):
    """Add a new todo task with title and optional description"""
    task_manager = TaskManager()

    # Implement validation for task title (non-empty, max length 255 chars)
    if not validate_task_title(title):
        click.echo("Error: Task title must be non-empty and less than 255 characters.", err=True)
        click.get_current_context().exit(2)  # Exit with code 2 for input error

    # Implement validation for task description (max length 1000 chars if provided)
    if not validate_task_description(description):
        click.echo("Error: Task description must be less than 1000 characters.", err=True)
        click.get_current_context().exit(2)  # Exit with code 2 for input error

    # Implement task creation logic with auto-incrementing ID and timestamp generation
    task = task_manager.add_task(title, description)

    # Implement JSON persistence for newly created tasks (already done in add_task method)

    # Add success message with assigned task ID after task creation
    click.echo(f"Task added successfully with ID: {task.id}")


@cli.command()
@click.argument('status', required=False, default=None)
def list(status):
    """Display all tasks or filter by completion status (all, completed, pending)"""
    task_manager = TaskManager()

    # Implement task listing functionality with filtering by completion status
    if status and status not in ['all', 'completed', 'pending']:
        click.echo(f"Error: Invalid status '{status}'. Use 'all', 'completed', or 'pending'.", err=True)
        click.get_current_context().exit(2)  # Exit with code 2 for input error

    tasks = task_manager.list_tasks(status)

    # Implement appropriate message when no tasks exist
    if not tasks:
        if status:
            click.echo(f"No {status} tasks found.")
        else:
            click.echo("No tasks found.")
        return

    # Implement tabular output format for task display with ID, Status, Title, Description
    # Implement visual indicators for task completion status ([ ] for incomplete, [x] for complete)
    click.echo(f"{'ID':<4} {'Status':<8} {'Title':<30} {'Description'}")
    click.echo("-" * 70)
    for task in tasks:
        status_indicator = "[x]" if task.completed else "[ ]"
        title = task.title[:27] + "..." if len(task.title) > 30 else task.title
        desc = task.description[:30] + "..." if task.description and len(task.description) > 30 else (task.description or "")
        click.echo(f"{task.id:<4} {status_indicator:<8} {title:<30} {desc}")


@cli.command()
@click.argument('task_id', type=int)
def complete(task_id):
    """Mark a task as complete by ID"""
    task_manager = TaskManager()

    # Implement validation to ensure task with given ID exists
    task = task_manager.find_task(task_id)
    if not task:
        click.echo(f"Error: Task with ID {task_id} not found.", err=True)
        click.get_current_context().exit(3)  # Exit with code 3 for task not found

    # Implement logic to toggle task completion status by ID
    task_manager.complete_task(task_id)

    # Add success message after completion status change
    updated_task = task_manager.find_task(task_id)
    status = "completed" if updated_task.completed else "incomplete"
    click.echo(f"Task {task_id} marked as {status}.")


@cli.command()
@click.argument('task_id', type=int)
@click.argument('title')
@click.argument('description', required=False)
def update(task_id, title, description):
    """Update an existing task's title and/or description"""
    task_manager = TaskManager()

    # Implement validation to ensure task with given ID exists
    task = task_manager.find_task(task_id)
    if not task:
        click.echo(f"Error: Task with ID {task_id} not found.", err=True)
        click.get_current_context().exit(3)  # Exit with code 3 for task not found

    # Implement validation for updated task title and description
    if not validate_task_title(title):
        click.echo("Error: Task title must be non-empty and less than 255 characters.", err=True)
        click.get_current_context().exit(2)  # Exit with code 2 for input error

    if not validate_task_description(description):
        click.echo("Error: Task description must be less than 1000 characters.", err=True)
        click.get_current_context().exit(2)  # Exit with code 2 for input error

    # Implement logic to update task details by ID
    updated_task = task_manager.update_task(task_id, title, description)

    if updated_task:
        # Implement update of updated_at timestamp when task details change (already handled in update_task method)
        # Add success message after task update
        click.echo(f"Task {task_id} updated successfully.")
    else:
        click.echo(f"Error: Failed to update task {task_id}.", err=True)
        click.get_current_context().exit(1)  # Exit with code 1 for general error


@cli.command()
@click.argument('task_id', type=int)
def delete(task_id):
    """Delete a task by ID"""
    task_manager = TaskManager()

    # Implement validation to ensure task with given ID exists
    task = task_manager.find_task(task_id)
    if not task:
        click.echo(f"Error: Task with ID {task_id} not found.", err=True)
        click.get_current_context().exit(3)  # Exit with code 3 for task not found

    # Add confirmation prompt for task deletion (to follow explicit user intent principle)
    click.confirm(f"Are you sure you want to delete task {task_id} '{task.title}'?", abort=True)

    # Implement logic to delete task by ID
    success = task_manager.delete_task(task_id)

    if success:
        # Add success message after task deletion
        click.echo(f"Task {task_id} deleted successfully.")
    else:
        click.echo(f"Error: Failed to delete task {task_id}.", err=True)
        click.get_current_context().exit(1)  # Exit with code 1 for general error


@dataclass
class Task:
    """Task data class with id, title, description, completed, created_at, updated_at attributes"""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at


class TaskManager:
    """TaskManager class to handle in-memory storage and operations"""

    def __init__(self, data_file: str = "tasks.json"):
        self.tasks: List[Task] = []
        self.next_id: int = 1
        self.data_file = data_file
        self.load_tasks()

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Add a new task to the collection with auto-incrementing ID and timestamp generation"""
        task = Task(
            id=self.next_id,
            title=title,
            description=description
        )
        self.tasks.append(task)
        logger.info(f"Added task {task.id}: {task.title}")
        self.next_id += 1
        self.save_tasks()
        return task

    def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        """Return filtered view of all tasks (all, completed, incomplete)"""
        if status == "completed":
            return [task for task in self.tasks if task.completed]
        elif status == "pending":
            return [task for task in self.tasks if not task.completed]
        return self.tasks

    def find_task(self, task_id: int) -> Optional[Task]:
        """Retrieve task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """Modify existing task by ID"""
        task = self.find_task(task_id)
        if task:
            old_title = task.title
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            task.updated_at = datetime.now().isoformat()
            logger.info(f"Updated task {task.id}: '{old_title}' -> '{task.title}'")
            self.save_tasks()
            return task
        logger.warning(f"Update failed: Task with ID {task_id} not found")
        return None

    def complete_task(self, task_id: int) -> Optional[Task]:
        """Toggle task completion status by ID"""
        task = self.find_task(task_id)
        if task:
            old_status = "completed" if task.completed else "incomplete"
            new_status = "incomplete" if task.completed else "completed"
            task.completed = not task.completed  # Toggle completion status
            task.updated_at = datetime.now().isoformat()
            logger.info(f"Toggled task {task.id} status: {old_status} -> {new_status}")
            self.save_tasks()
            return task
        logger.warning(f"Complete task failed: Task with ID {task_id} not found")
        return None

    def delete_task(self, task_id: int) -> bool:
        """Remove task by ID"""
        task = self.find_task(task_id)
        if task:
            logger.info(f"Deleted task {task.id}: {task.title}")
            self.tasks.remove(task)
            self.save_tasks()
            return True
        logger.warning(f"Delete task failed: Task with ID {task_id} not found")
        return False

    def save_tasks(self):
        """JSON persistence functionality for tasks"""
        data = []
        for task in self.tasks:
            data.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed,
                'created_at': task.created_at,
                'updated_at': task.updated_at
            })

        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        logger.debug(f"Saved {len(self.tasks)} tasks to {self.data_file}")

    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                self.tasks = []
                self.next_id = 1

                for item in data:
                    task = Task(
                        id=item['id'],
                        title=item['title'],
                        description=item.get('description'),
                        completed=item.get('completed', False),
                        created_at=item.get('created_at', ''),
                        updated_at=item.get('updated_at', '')
                    )
                    self.tasks.append(task)

                    if task.id >= self.next_id:
                        self.next_id = task.id + 1

                logger.info(f"Loaded {len(self.tasks)} tasks from {self.data_file}")
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                # If there's an error loading the file, start fresh
                logger.error(f"Error loading tasks from {self.data_file}: {e}")
                self.tasks = []
                self.next_id = 1
        else:
            logger.info(f"Task file {self.data_file} does not exist, starting with empty task list")


def validate_task_title(title: str) -> bool:
    """Input validation function for task title (non-empty, max length 255 chars)"""
    if not title or not title.strip():
        return False
    if len(title.strip()) > 255:
        return False
    return True


def validate_task_description(description: Optional[str]) -> bool:
    """Input validation function for task description (max length 1000 chars if provided)"""
    if description is None:
        return True
    if len(description) > 1000:
        return False
    return True


def sanitize_input(input_str: Optional[str]) -> Optional[str]:
    """Input sanitization for all user inputs to prevent potential issues (T046)"""
    if input_str is None:
        return None
    # Remove potentially harmful characters or patterns
    # For now, just strip leading/trailing whitespace
    return input_str.strip()


def generate_timestamp() -> str:
    """Timestamp utility function for created_at and updated_at"""
    return datetime.now().isoformat()


def interactive_mode():
    """Run the CLI application in interactive mode with a continuous loop"""
    task_manager = TaskManager()
    print("Welcome to the CLI Todo Application!")
    print("Available commands:")
    print("  add <title> [description]    - Add a new task")
    print("  list [all|completed|pending] - List tasks with optional filter")
    print("  complete <id>                - Mark task as complete/incomplete")
    print("  update <id> <title> [desc]   - Update a task")
    print("  delete <id>                  - Delete a task")
    print("  help                         - Show this help message")
    print("  q/quit/exit                  - Exit the application")
    print("-" * 60)

    while True:
        try:
            user_input = input("todo> ").strip()

            if not user_input:
                continue

            # Parse the input into command and arguments
            parts = user_input.split()
            command = parts[0].lower() if parts else ""

            # Check for quit commands
            if command in ['q', 'quit', 'exit']:
                print("Goodbye!")
                break

            # Help command
            if command == 'help':
                print("Available commands:")
                print("  add <title> [description]    - Add a new task")
                print("  list [all|completed|pending] - List tasks with optional filter")
                print("  complete <id>                - Mark task as complete/incomplete")
                print("  update <id> <title> [desc]   - Update a task")
                print("  delete <id>                  - Delete a task")
                print("  help                         - Show this help message")
                print("  q/quit/exit                  - Exit the application")
                continue

            # Process commands
            if command == 'add':
                if len(parts) < 2:
                    print("Error: Please provide a task title")
                    continue
                title = parts[1]
                description = ' '.join(parts[2:]) if len(parts) > 2 else None

                if not validate_task_title(title):
                    print("Error: Task title must be non-empty and less than 255 characters.")
                    continue

                if not validate_task_description(description):
                    print("Error: Task description must be less than 1000 characters.")
                    continue

                task = task_manager.add_task(title, description)
                print(f"Task added successfully with ID: {task.id}")

            elif command == 'list':
                status = parts[1] if len(parts) > 1 else None
                if status and status not in ['all', 'completed', 'pending']:
                    print(f"Error: Invalid status '{status}'. Use 'all', 'completed', or 'pending'.")
                    continue

                tasks = task_manager.list_tasks(status)
                if not tasks:
                    if status:
                        print(f"No {status} tasks found.")
                    else:
                        print("No tasks found.")
                    continue

                print(f"{'ID':<4} {'Status':<8} {'Title':<30} {'Description'}")
                print("-" * 70)
                for task in tasks:
                    status_indicator = "[x]" if task.completed else "[ ]"
                    title = task.title[:27] + "..." if len(task.title) > 30 else task.title
                    desc = task.description[:30] + "..." if task.description and len(task.description) > 30 else (task.description or "")
                    print(f"{task.id:<4} {status_indicator:<8} {title:<30} {desc}")

            elif command == 'complete':
                if len(parts) < 2:
                    print("Error: Please provide a task ID")
                    continue
                try:
                    task_id = int(parts[1])
                except ValueError:
                    print("Error: Task ID must be a number")
                    continue

                task = task_manager.find_task(task_id)
                if not task:
                    print(f"Error: Task with ID {task_id} not found.")
                    continue

                task_manager.complete_task(task_id)
                updated_task = task_manager.find_task(task_id)
                status = "completed" if updated_task.completed else "incomplete"
                print(f"Task {task_id} marked as {status}.")

            elif command == 'update':
                if len(parts) < 3:
                    print("Error: Please provide task ID and new title")
                    continue
                try:
                    task_id = int(parts[1])
                except ValueError:
                    print("Error: Task ID must be a number")
                    continue

                task = task_manager.find_task(task_id)
                if not task:
                    print(f"Error: Task with ID {task_id} not found.")
                    continue

                title = parts[2]
                description = ' '.join(parts[3:]) if len(parts) > 3 else None

                if not validate_task_title(title):
                    print("Error: Task title must be non-empty and less than 255 characters.")
                    continue

                if not validate_task_description(description):
                    print("Error: Task description must be less than 1000 characters.")
                    continue

                updated_task = task_manager.update_task(task_id, title, description)
                if updated_task:
                    print(f"Task {task_id} updated successfully.")
                else:
                    print(f"Error: Failed to update task {task_id}.")

            elif command == 'delete':
                if len(parts) < 2:
                    print("Error: Please provide a task ID")
                    continue
                try:
                    task_id = int(parts[1])
                except ValueError:
                    print("Error: Task ID must be a number")
                    continue

                task = task_manager.find_task(task_id)
                if not task:
                    print(f"Error: Task with ID {task_id} not found.")
                    continue

                # Confirmation prompt
                confirm = input(f"Are you sure you want to delete task {task_id} '{task.title}'? (y/N): ").strip().lower()
                if confirm in ['y', 'yes']:
                    success = task_manager.delete_task(task_id)
                    if success:
                        print(f"Task {task_id} deleted successfully.")
                    else:
                        print(f"Error: Failed to delete task {task_id}.")
                else:
                    print("Deletion cancelled.")

            else:
                print(f"Error: Unknown command '{command}'. Type 'help' for available commands.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == '__main__':
    # Check if any command-line arguments were provided
    import sys
    if len(sys.argv) > 1:
        # Use Click's normal command-line interface
        cli()
    else:
        # Run in interactive mode
        interactive_mode()