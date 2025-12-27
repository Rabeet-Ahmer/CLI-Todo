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
    """CLI Todo Application - Manage your tasks from the command line

    A comprehensive task management tool that supports priorities, tags, due dates,
    search, filtering, and sorting. Use 'todo COMMAND --help' for detailed help
    on each command.
    """
    pass


# Add comprehensive help text for all commands following Click conventions (T044)
# Implement consistent exit codes across all commands (0=success, 1=general error, 2=input error, 3=task not found) (T043)
# Implement proper error handling for file I/O operations with appropriate messages (T045)


@cli.command()
@click.argument('title')
@click.option('--description', '-desc', help='Task description')
@click.option('--priority', '-p', default='medium', type=click.Choice(['high', 'medium', 'low']), help='Set priority level (high, medium, low) [default: medium]')
@click.option('--tag', '-t', multiple=True, help='Add tag to task (can be used multiple times)')
@click.option('--due-date', '-d', help='Set due date (YYYY-MM-DD format)')
def add(title, description, priority, tag, due_date):
    """Add a new todo task with title and optional description

    Examples:
      todo add "Buy groceries" --description "Milk, bread, eggs"
      todo add "Meeting prep" --priority high --tag work --due-date 2025-12-31
    """
    task_manager = TaskManager()

    # Sanitize inputs
    title = sanitize_input(title)
    description = sanitize_input(description)
    priority = sanitize_input(priority)
    due_date = sanitize_input(due_date)
    # Sanitize tags
    sanitized_tags = [sanitize_input(t) for t in tag] if tag else []

    # Implement validation for task title (non-empty, max length 255 chars)
    if not validate_task_title(title):
        click.echo("Error: Task title must be non-empty and less than 255 characters.", err=True)
        click.get_current_context().exit(2)  # Exit with code 2 for input error

    # Implement validation for task description (max length 1000 chars if provided)
    if not validate_task_description(description):
        click.echo("Error: Task description must be less than 1000 characters.", err=True)
        click.get_current_context().exit(2)  # Exit with code 2 for input error

    # Validate priority
    if not validate_task_priority(priority):
        click.echo("Error: Priority must be one of: high, medium, low", err=True)
        click.get_current_context().exit(4)  # Exit with code 4 for invalid priority

    # Validate tags
    if not validate_task_tags(sanitized_tags):
        click.echo("Error: Tags must be 1-50 alphanumeric characters (hyphens/underscores allowed)", err=True)
        click.get_current_context().exit(6)  # Exit with code 6 for invalid tag

    # Validate due date
    if due_date and not validate_task_due_date(due_date):
        click.echo("Error: Date must be in YYYY-MM-DD format", err=True)
        click.get_current_context().exit(5)  # Exit with code 5 for invalid date

    # Implement task creation logic with auto-incrementing ID and timestamp generation
    task = task_manager.add_task(title, description, priority, sanitized_tags, due_date)

    # Implement JSON persistence for newly created tasks (already done in add_task method)

    # Add success message with assigned task ID after task creation
    click.echo(f"Task added successfully with ID: {task.id}")


@cli.command()
@click.option('--status', type=click.Choice(['all', 'completed', 'pending']), default=None, help='Filter by status (all, completed, pending) [default: all]')
@click.option('--priority', type=click.Choice(['high', 'medium', 'low']), help='Filter by priority (high, medium, low)')
@click.option('--tag', multiple=True, help='Filter by tag (can be used multiple times)')
@click.option('--completed', 'completed_only', is_flag=True, help='Show only completed tasks')
@click.option('--pending', 'pending_only', is_flag=True, help='Show only pending tasks')
@click.option('--overdue', is_flag=True, help='Show only overdue tasks')
@click.option('--sort', type=click.Choice(['id', 'title', 'priority', 'due-date', 'created-date', 'updated-date']), default='id', help='Sort by (id, title, priority, due-date, created-date, updated-date) [default: id]')
@click.option('--order', type=click.Choice(['asc', 'desc']), default='asc', help='Sort order (asc, desc) [default: asc]')
@click.option('--due-before', help='Show tasks due before date (YYYY-MM-DD)')
@click.option('--due-after', help='Show tasks due after date (YYYY-MM-DD)')
def list(status, priority, tag, completed_only, pending_only, overdue, sort, order, due_before, due_after):
    """Display tasks with filtering and sorting options

    Examples:
      todo list --status pending --priority high
      todo list --tag work --sort due-date --order desc
      todo list --overdue --completed
      todo list --due-before 2025-12-31 --sort priority
    """
    task_manager = TaskManager()

    # Get all tasks
    tasks = task_manager.tasks

    # Apply filters - check for conflicting options first
    if status is not None and (completed_only or pending_only):
        click.echo("Error: --status option cannot be used with --completed or --pending", err=True)
        click.get_current_context().exit(2)  # Exit with code 2 for input error

    if status == 'completed':
        tasks = [task for task in tasks if task.completed]
    elif status == 'pending':
        tasks = [task for task in tasks if not task.completed]
    elif completed_only:
        tasks = [task for task in tasks if task.completed]
    elif pending_only:
        tasks = [task for task in tasks if not task.completed]

    # Filter by priority
    if priority:
        tasks = [task for task in tasks if task.priority == priority]

    # Filter by tags
    if tag:
        tag_list = list(tag)
        tasks = [task for task in tasks if any(t in task.tags for t in tag_list)]

    # Filter by overdue
    if overdue:
        tasks = [task for task in tasks if not task.completed and is_task_overdue(task.due_date)]

    # Filter by due date range
    if due_before:
        if not validate_task_due_date(due_before):
            click.echo("Error: Date must be in YYYY-MM-DD format", err=True)
            click.get_current_context().exit(5)  # Exit with code 5 for invalid date
        try:
            before_date = datetime.strptime(due_before, '%Y-%m-%d').date()
            tasks = [task for task in tasks if task.due_date and datetime.strptime(task.due_date, '%Y-%m-%d').date() < before_date]
        except ValueError:
            click.echo("Error: Invalid date format", err=True)
            click.get_current_context().exit(5)

    if due_after:
        if not validate_task_due_date(due_after):
            click.echo("Error: Date must be in YYYY-MM-DD format", err=True)
            click.get_current_context().exit(5)  # Exit with code 5 for invalid date
        try:
            after_date = datetime.strptime(due_after, '%Y-%m-%d').date()
            tasks = [task for task in tasks if task.due_date and datetime.strptime(task.due_date, '%Y-%m-%d').date() > after_date]
        except ValueError:
            click.echo("Error: Invalid date format", err=True)
            click.get_current_context().exit(5)

    # Apply sorting
    if sort == 'id':
        tasks.sort(key=lambda t: t.id, reverse=(order == 'desc'))
    elif sort == 'title':
        tasks.sort(key=lambda t: t.title.lower(), reverse=(order == 'desc'))
    elif sort == 'priority':
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        tasks.sort(key=lambda t: priority_order.get(t.priority, 3), reverse=(order == 'desc'))
    elif sort == 'due-date':
        def sort_key(task):
            if task.due_date is None:
                # For ascending order, None should come first; for descending, None should come last
                return (1, datetime.min) if order == 'asc' else (0, datetime.max)
            try:
                return (0, datetime.strptime(task.due_date, '%Y-%m-%d'))
            except ValueError:
                return (1, datetime.min) if order == 'asc' else (0, datetime.max)
        tasks.sort(key=sort_key, reverse=(order == 'desc'))
    elif sort == 'created-date':
        tasks.sort(key=lambda t: datetime.fromisoformat(t.created_at), reverse=(order == 'desc'))
    elif sort == 'updated-date':
        tasks.sort(key=lambda t: datetime.fromisoformat(t.updated_at), reverse=(order == 'desc'))

    # Implement appropriate message when no tasks exist
    if not tasks:
        click.echo("No tasks found matching the criteria.")
        return

    # Implement tabular output format for task display with ID, Status, Title, Description
    # Implement visual indicators for task completion status ([ ] for incomplete, [x] for complete)
    click.echo(f"{'ID':<4} {'Status':<8} {'Priority':<8} {'Title':<30} {'Description':<30} {'Due Date':<12} {'Tags'}")
    click.echo("-" * 120)
    for task in tasks:
        status_indicator = "[x]" if task.completed else "[ ]"
        title = task.title[:27] + "..." if len(task.title) > 30 else task.title
        description = (task.description[:27] + "..." if task.description and len(task.description) > 30 else (task.description or "")) if task.description else ""
        due_date_str = task.due_date or ""
        tags_str = ",".join(task.tags) if task.tags else ""
        click.echo(f"{task.id:<4} {status_indicator:<8} {task.priority:<8} {title:<30} {description:<30} {due_date_str:<12} {tags_str}")


@cli.command()
@click.argument('task_id', type=int)
def complete(task_id):
    """Mark a task as complete by ID

    Examples:
      todo complete 1
    """
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
@click.option('--title', help='Update task title')
@click.option('--description', help='Update task description')
@click.option('--priority', '-p', type=click.Choice(['high', 'medium', 'low']), help='Update priority level (high, medium, low)')
@click.option('--add-tag', '-a', multiple=True, help='Add tag to task (can be used multiple times)')
@click.option('--remove-tag', '-r', multiple=True, help='Remove tag from task (can be used multiple times)')
@click.option('--due-date', '-d', help='Update due date (YYYY-MM-DD format)')
@click.option('--clear-due-date', is_flag=True, help='Remove due date')
def update(task_id, title, description, priority, add_tag, remove_tag, due_date, clear_due_date):
    """Update an existing task's details

    Examples:
      todo update 1 --title "Updated task title"
      todo update 1 --priority high --add-tag urgent --due-date 2025-12-31
      todo update 1 --remove-tag work --clear-due-date
    """
    task_manager = TaskManager()

    # Implement validation to ensure task with given ID exists
    task = task_manager.find_task(task_id)
    if not task:
        click.echo(f"Error: Task with ID {task_id} not found.", err=True)
        click.get_current_context().exit(3)  # Exit with code 3 for task not found

    # Check for conflicting due date options
    if due_date is not None and clear_due_date:
        click.echo("Error: --due-date and --clear-due-date cannot be used together", err=True)
        click.get_current_context().exit(2)  # Exit with code 2 for input error

    # If clear-due-date flag is set, use None for due_date
    if clear_due_date:
        due_date = None

    # Sanitize inputs
    title = sanitize_input(title)
    description = sanitize_input(description)
    priority = sanitize_input(priority)
    due_date = sanitize_input(due_date)
    # Sanitize tags
    sanitized_add_tags = [sanitize_input(t) for t in add_tag] if add_tag else []
    sanitized_remove_tags = [sanitize_input(t) for t in remove_tag] if remove_tag else []

    # Validate title if provided
    if title is not None and not validate_task_title(title):
        click.echo("Error: Task title must be non-empty and less than 255 characters.", err=True)
        click.get_current_context().exit(2)  # Exit with code 2 for input error

    # Validate description if provided
    if description is not None and not validate_task_description(description):
        click.echo("Error: Task description must be less than 1000 characters.", err=True)
        click.get_current_context().exit(2)  # Exit with code 2 for input error

    # Validate priority if provided
    if priority is not None and not validate_task_priority(priority):
        click.echo("Error: Priority must be one of: high, medium, low", err=True)
        click.get_current_context().exit(4)  # Exit with code 4 for invalid priority

    # Validate tags if provided
    if sanitized_add_tags and not validate_task_tags(sanitized_add_tags):
        click.echo("Error: Tags must be 1-50 alphanumeric characters (hyphens/underscores allowed)", err=True)
        click.get_current_context().exit(6)  # Exit with code 6 for invalid tag

    if sanitized_remove_tags and not validate_task_tags(sanitized_remove_tags):
        click.echo("Error: Tags must be 1-50 alphanumeric characters (hyphens/underscores allowed)", err=True)
        click.get_current_context().exit(6)  # Exit with code 6 for invalid tag

    # Validate due date if provided
    if due_date is not None and not validate_task_due_date(due_date):
        click.echo("Error: Date must be in YYYY-MM-DD format", err=True)
        click.get_current_context().exit(5)  # Exit with code 5 for invalid date

    # Implement logic to update task details by ID
    updated_task = task_manager.update_task(
        task_id,
        title=title,
        description=description,
        priority=priority,
        add_tags=sanitized_add_tags,
        remove_tags=sanitized_remove_tags,
        due_date=due_date
    )

    if updated_task:
        # Implement update of updated_at timestamp when task details change (already handled in update_task method)
        # Add success message after task update
        click.echo(f"Task {task_id} updated successfully.")
    else:
        click.echo(f"Error: Failed to update task {task_id}.", err=True)
        click.get_current_context().exit(1)  # Exit with code 1 for general error


@cli.command()
@click.argument('query')
@click.option('--in-title', 'search_in_title', is_flag=True, help='Search in title only')
@click.option('--in-description', 'search_in_description', is_flag=True, help='Search in description only')
@click.option('--in-tags', 'search_in_tags', is_flag=True, help='Search in tags only')
@click.option('--all-fields', 'search_all_fields', is_flag=True, default=True, help='Search in all fields (default)')
def search(query, search_in_title, search_in_description, search_in_tags, search_all_fields):
    """Search tasks by keyword across title, description, and tags

    Examples:
      todo search "groceries"
      todo search "urgent" --in-title
      todo search "meeting" --in-description
      todo search "work" --in-tags
    """
    task_manager = TaskManager()

    # Sanitize the query
    query = sanitize_input(query)
    if not query:
        click.echo("Error: Search query cannot be empty.", err=True)
        click.get_current_context().exit(2)  # Exit with code 2 for input error

    # Determine which fields to search
    if search_in_title:
        search_in_description = False
        search_in_tags = False
    elif search_in_description:
        search_in_title = False
        search_in_tags = False
    elif search_in_tags:
        search_in_title = False
        search_in_description = False
    else:
        # Default to search all fields if no specific field is selected
        search_in_title = True
        search_in_description = True
        search_in_tags = True

    # Search tasks
    results = search_tasks(task_manager.tasks, query, search_in_title, search_in_description, search_in_tags)

    # Display results
    if not results:
        click.echo("No tasks found matching the search query.")
        return

    # Display search results in the same format as list command
    click.echo(f"{'ID':<4} {'Status':<8} {'Priority':<8} {'Title':<30} {'Description':<30} {'Due Date':<12} {'Tags'}")
    click.echo("-" * 120)
    for task in results:
        status_indicator = "[x]" if task.completed else "[ ]"
        title = task.title[:27] + "..." if len(task.title) > 30 else task.title
        description = (task.description[:27] + "..." if task.description and len(task.description) > 30 else (task.description or "")) if task.description else ""
        due_date_str = task.due_date or ""
        tags_str = ",".join(task.tags) if task.tags else ""
        click.echo(f"{task.id:<4} {status_indicator:<8} {task.priority:<8} {title:<30} {description:<30} {due_date_str:<12} {tags_str}")


@cli.group()
def tag():
    """Manage task tags - list available tags or find tasks with specific tags

    Examples:
      todo tag list
      todo tag tasks work
    """
    pass


@tag.command()
def list():
    """List all available tags"""
    task_manager = TaskManager()

    # Collect all unique tags from all tasks
    all_tags = set()
    for task in task_manager.tasks:
        for tag in task.tags:
            all_tags.add(tag)

    if not all_tags:
        click.echo("No tags found.")
        return

    click.echo("Available tags:")
    for tag in sorted(all_tags):
        click.echo(f"  - {tag}")


@tag.command()
@click.argument('tag_name')
def tasks(tag_name):
    """List tasks with a specific tag

    Examples:
      todo tag tasks work
      todo tag tasks personal
    """
    task_manager = TaskManager()

    # Sanitize the tag name
    tag_name = sanitize_input(tag_name)
    if not tag_name:
        click.echo("Error: Tag name cannot be empty.", err=True)
        click.get_current_context().exit(2)  # Exit with code 2 for input error

    # Find all tasks with the specified tag
    matching_tasks = [task for task in task_manager.tasks if tag_name in task.tags]

    if not matching_tasks:
        click.echo(f"No tasks found with tag '{tag_name}'.")
        return

    # Display matching tasks in the same format as list command
    click.echo(f"{'ID':<4} {'Status':<8} {'Priority':<8} {'Title':<30} {'Description':<30} {'Due Date':<12} {'Tags'}")
    click.echo("-" * 120)
    for task in matching_tasks:
        status_indicator = "[x]" if task.completed else "[ ]"
        title = task.title[:27] + "..." if len(task.title) > 30 else task.title
        description = (task.description[:27] + "..." if task.description and len(task.description) > 30 else (task.description or "")) if task.description else ""
        due_date_str = task.due_date or ""
        tags_str = ",".join(task.tags) if task.tags else ""
        click.echo(f"{task.id:<4} {status_indicator:<8} {task.priority:<8} {title:<30} {description:<30} {due_date_str:<12} {tags_str}")


@cli.command()
@click.argument('task_id', type=int)
def delete(task_id):
    """Delete a task by ID

    Examples:
      todo delete 1
    """
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
    """Task data class with id, title, description, completed, created_at, updated_at, priority, tags, due_date attributes"""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: str = ""
    updated_at: str = ""
    priority: str = "medium"  # Values: "high", "medium", "low"
    tags: List[str] = None   # List of tag strings
    due_date: Optional[str] = None  # ISO format date string (YYYY-MM-DD or ISO 8601)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at
        if self.tags is None:
            self.tags = []


class TaskManager:
    """TaskManager class to handle in-memory storage and operations"""

    def __init__(self, data_file: str = "tasks.json"):
        self.tasks: List[Task] = []
        self.next_id: int = 1
        self.data_file = data_file
        self.load_tasks()

    def add_task(self, title: str, description: Optional[str] = None, priority: str = "medium", tags: Optional[List[str]] = None, due_date: Optional[str] = None) -> Task:
        """Add a new task to the collection with auto-incrementing ID and timestamp generation"""
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags if tags is not None else [],
            due_date=due_date
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

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[str] = None, add_tags: Optional[List[str]] = None, remove_tags: Optional[List[str]] = None, due_date: Optional[str] = None) -> Optional[Task]:
        """Modify existing task by ID"""
        task = self.find_task(task_id)
        if task:
            old_title = task.title
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if priority is not None:
                task.priority = priority
            if add_tags is not None:
                for tag in add_tags:
                    if tag not in task.tags:
                        task.tags.append(tag)
            if remove_tags is not None:
                for tag in remove_tags:
                    if tag in task.tags:
                        task.tags.remove(tag)
            if due_date is not None:
                task.due_date = due_date
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
                'updated_at': task.updated_at,
                'priority': task.priority,
                'tags': task.tags,
                'due_date': task.due_date
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
                        updated_at=item.get('updated_at', ''),
                        priority=item.get('priority', 'medium'),  # Default to medium for backward compatibility
                        tags=item.get('tags', []),  # Default to empty list for backward compatibility
                        due_date=item.get('due_date')  # Default to None for backward compatibility
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


def validate_task_priority(priority: Optional[str]) -> bool:
    """Input validation function for task priority (high, medium, low)"""
    if priority is None:
        return True  # Allow None for backward compatibility
    return priority in ['high', 'medium', 'low']


def validate_task_tags(tags: Optional[List[str]]) -> bool:
    """Input validation function for task tags (list of non-empty strings, max 50 chars each)"""
    if tags is None:
        return True  # Allow None for backward compatibility
    if not isinstance(tags, list):
        return False
    for tag in tags:
        if not isinstance(tag, str) or not tag or len(tag) > 50:
            return False
    return True


def validate_task_due_date(due_date: Optional[str]) -> bool:
    """Input validation function for task due date (ISO 8601 format YYYY-MM-DD)"""
    if due_date is None:
        return True  # Allow None for backward compatibility
    if not isinstance(due_date, str):
        return False

    # Check if the date string matches YYYY-MM-DD format
    import re
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, due_date):
        return False

    # Try to parse the date to ensure it's a valid date
    try:
        datetime.strptime(due_date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_task_overdue(due_date: Optional[str]) -> bool:
    """Check if a task is overdue based on its due date"""
    if due_date is None:
        return False

    try:
        due_datetime = datetime.strptime(due_date, '%Y-%m-%d')
        current_date = datetime.now().date()
        due_date_only = due_datetime.date()
        return due_date_only < current_date
    except ValueError:
        return False  # If date is invalid, it's not overdue


def search_tasks(tasks: List[Task], query: str, search_in_title: bool = True, search_in_description: bool = True, search_in_tags: bool = True) -> List[Task]:
    """Search tasks by query string across specified fields"""
    query_lower = query.lower()
    results = []

    for task in tasks:
        match = False

        # Search in title
        if search_in_title and query_lower in task.title.lower():
            match = True

        # Search in description
        if not match and search_in_description and task.description and query_lower in task.description.lower():
            match = True

        # Search in tags
        if not match and search_in_tags and task.tags:
            for tag in task.tags:
                if query_lower in tag.lower():
                    match = True
                    break

        if match:
            results.append(task)

    return results


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
    """Run the CLI application in interactive mode with a menu-driven interface"""
    try:
        import inquirer
    except ImportError:
        print("Error: inquirer library is required for interactive mode. Please install it with 'pip install inquirer'")
        return

    task_manager = TaskManager()
    print("Welcome to the CLI Todo Application!")
    print("Use arrow keys to navigate and Enter to select.")

    while True:
        try:
            # Main menu options
            main_questions = [
                inquirer.List('action',
                             message="Select an operation",
                             choices=[
                                 'Add',
                                 'List',
                                 'Complete',
                                 'Update',
                                 'Delete',
                                 'Search',
                                 'Tag',
                                 'Help',
                                 'Exit'
                             ])
            ]

            main_answer = inquirer.prompt(main_questions)
            if not main_answer:  # User pressed Ctrl+C
                print("\nGoodbye!")
                break

            action = main_answer['action'].lower()

            if action == 'add':
                add_task_interactive(task_manager)
            elif action == 'list':
                list_tasks_interactive(task_manager)
            elif action == 'complete':
                complete_task_interactive(task_manager)
            elif action == 'update':
                update_task_interactive(task_manager)
            elif action == 'delete':
                delete_task_interactive(task_manager)
            elif action == 'search':
                search_tasks_interactive(task_manager)
            elif action == 'tag':
                tag_tasks_interactive(task_manager)
            elif action == 'help':
                show_help_interactive()
            elif action == 'exit':
                print("Goodbye!")
                break

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


def add_task_interactive(task_manager):
    """Interactive task addition with guided prompts"""
    try:
        import inquirer

        # Get title
        title_question = [
            inquirer.Text('title', message="Enter task title")
        ]
        title_answer = inquirer.prompt(title_question)
        if not title_answer:
            return  # User cancelled

        title = sanitize_input(title_answer['title'])
        if not title:
            print("Error: Task title cannot be empty.")
            return

        if not validate_task_title(title):
            print("Error: Task title must be less than 255 characters.")
            return

        # Get description
        desc_question = [
            inquirer.Text('description', message="Enter task description (optional, press Enter to skip)")
        ]
        desc_answer = inquirer.prompt(desc_question)
        if not desc_answer:
            return  # User cancelled

        description = sanitize_input(desc_answer['description']) or None
        if description and not validate_task_description(description):
            print("Error: Task description must be less than 1000 characters.")
            return

        # Get priority
        priority_question = [
            inquirer.List('priority',
                         message="Select priority",
                         choices=['high', 'medium', 'low'])
        ]
        priority_answer = inquirer.prompt(priority_question)
        if not priority_answer:
            return  # User cancelled
        priority = priority_answer['priority']

        # Get tags
        tags_input = input("Enter tags separated by commas (optional, press Enter to skip): ").strip()
        tags = []
        if tags_input:
            tags = [sanitize_input(tag.strip()) for tag in tags_input.split(',') if tag.strip()]
            if not validate_task_tags(tags):
                print("Error: Tags must be 1-50 alphanumeric characters (hyphens/underscores allowed)")
                return

        # Get due date
        due_date_input = input("Enter due date (YYYY-MM-DD format, optional, press Enter to skip): ").strip()
        due_date = None
        if due_date_input:
            due_date = sanitize_input(due_date_input)
            if not validate_task_due_date(due_date):
                print("Error: Date must be in YYYY-MM-DD format")
                return

        # Confirm and add task
        confirm_question = [
            inquirer.Confirm('confirm',
                           message=f"Add task '{title}' with description '{description}', priority '{priority}', tags {tags}, due date '{due_date}'?")
        ]
        confirm_answer = inquirer.prompt(confirm_question)
        if not confirm_answer or not confirm_answer['confirm']:
            print("Task addition cancelled.")
            return

        task = task_manager.add_task(title, description, priority, tags, due_date)
        print(f"Task added successfully with ID: {task.id}")

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except EOFError:
        print("\nOperation cancelled.")


def list_tasks_interactive(task_manager):
    """Interactive task listing with filtering and sorting options"""
    try:
        import inquirer

        # Get filtering options
        filter_questions = [
            inquirer.List('status',
                         message="Filter by status",
                         choices=['all', 'completed', 'pending']),
            inquirer.List('priority',
                         message="Filter by priority (optional)",
                         choices=['any', 'high', 'medium', 'low']),
            inquirer.Confirm('overdue',
                           message="Show only overdue tasks?"),
        ]

        filter_answers = inquirer.prompt(filter_questions)
        if not filter_answers:
            return  # User cancelled

        status = filter_answers['status'] if filter_answers['status'] != 'all' else None
        priority = filter_answers['priority'] if filter_answers['priority'] != 'any' else None
        overdue = filter_answers['overdue']

        # Get tags to filter by
        all_tags = set()
        for task in task_manager.tasks:
            for tag in task.tags:
                all_tags.add(tag)

        selected_tags = []
        if all_tags:
            tag_questions = [
                inquirer.Checkbox('tags',
                                message="Select tags to filter by (space to select, Enter to continue)",
                                choices=sorted(list(all_tags)) + ['(none)'])
            ]
            tag_answers = inquirer.prompt(tag_questions)
            if not tag_answers:
                return  # User cancelled
            selected_tags = [tag for tag in tag_answers['tags'] if tag != '(none)']

        # Get sorting options
        sort_questions = [
            inquirer.List('sort',
                         message="Sort by",
                         choices=['id', 'title', 'priority', 'due-date', 'created-date', 'updated-date']),
            inquirer.List('order',
                         message="Sort order",
                         choices=['asc', 'desc'])
        ]
        sort_answers = inquirer.prompt(sort_questions)
        if not sort_answers:
            return  # User cancelled
        sort = sort_answers['sort']
        order = sort_answers['order']

        # Apply filters and sorting
        tasks = task_manager.tasks

        # Apply status filter
        if status == 'completed':
            tasks = [task for task in tasks if task.completed]
        elif status == 'pending':
            tasks = [task for task in tasks if not task.completed]

        # Apply priority filter
        if priority:
            tasks = [task for task in tasks if task.priority == priority]

        # Apply tag filter
        if selected_tags:
            tasks = [task for task in tasks if any(t in task.tags for t in selected_tags)]

        # Apply overdue filter
        if overdue:
            tasks = [task for task in tasks if not task.completed and is_task_overdue(task.due_date)]

        # Apply sorting
        if sort == 'id':
            tasks.sort(key=lambda t: t.id, reverse=(order == 'desc'))
        elif sort == 'title':
            tasks.sort(key=lambda t: t.title.lower(), reverse=(order == 'desc'))
        elif sort == 'priority':
            priority_order = {'high': 0, 'medium': 1, 'low': 2}
            tasks.sort(key=lambda t: priority_order.get(t.priority, 3), reverse=(order == 'desc'))
        elif sort == 'due-date':
            def sort_key(task):
                if task.due_date is None:
                    # For ascending order, None should come first; for descending, None should come last
                    return (1, datetime.min) if order == 'asc' else (0, datetime.max)
                try:
                    return (0, datetime.strptime(task.due_date, '%Y-%m-%d'))
                except ValueError:
                    return (1, datetime.min) if order == 'asc' else (0, datetime.max)
            tasks.sort(key=sort_key, reverse=(order == 'desc'))
        elif sort == 'created-date':
            tasks.sort(key=lambda t: datetime.fromisoformat(t.created_at), reverse=(order == 'desc'))
        elif sort == 'updated-date':
            tasks.sort(key=lambda t: datetime.fromisoformat(t.updated_at), reverse=(order == 'desc'))

        # Display results
        if not tasks:
            print("No tasks found matching the criteria.")
            input("Press Enter to continue...")
            return

        # Display with the new format that includes priority, description, and tags
        print(f"{'ID':<4} {'Status':<8} {'Priority':<8} {'Title':<30} {'Description':<30} {'Due Date':<12} {'Tags'}")
        print("-" * 120)
        for task in tasks:
            status_indicator = "[x]" if task.completed else "[ ]"
            title = task.title[:27] + "..." if len(task.title) > 30 else task.title
            description = (task.description[:27] + "..." if task.description and len(task.description) > 30 else (task.description or "")) if task.description else ""
            due_date_str = task.due_date or ""
            tags_str = ",".join(task.tags) if task.tags else ""
            print(f"{task.id:<4} {status_indicator:<8} {task.priority:<8} {title:<30} {description:<30} {due_date_str:<12} {tags_str}")

        input("Press Enter to continue...")

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except EOFError:
        print("\nOperation cancelled.")


def complete_task_interactive(task_manager):
    """Interactive task completion"""
    try:
        import inquirer

        # Get all tasks to show as options
        tasks = task_manager.tasks
        if not tasks:
            print("No tasks available.")
            input("Press Enter to continue...")
            return

        # Create choices for task IDs
        task_choices = [str(task.id) for task in tasks]
        task_choices.append('(cancel)')

        task_question = [
            inquirer.List('task_id',
                         message="Select task to complete/incomplete",
                         choices=task_choices)
        ]

        task_answer = inquirer.prompt(task_question)
        if not task_answer or task_answer['task_id'] == '(cancel)':
            return  # User cancelled

        task_id = int(task_answer['task_id'])
        task = task_manager.find_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            input("Press Enter to continue...")
            return

        task_manager.complete_task(task_id)
        updated_task = task_manager.find_task(task_id)
        status = "completed" if updated_task.completed else "incomplete"
        print(f"Task {task_id} marked as {status}.")
        input("Press Enter to continue...")

    except ValueError:
        print("Error: Invalid task ID.")
        input("Press Enter to continue...")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except EOFError:
        print("\nOperation cancelled.")


def update_task_interactive(task_manager):
    """Interactive task update"""
    try:
        import inquirer

        # Get all tasks to show as options
        tasks = task_manager.tasks
        if not tasks:
            print("No tasks available.")
            input("Press Enter to continue...")
            return

        # Create choices for task IDs
        task_choices = [str(task.id) for task in tasks]
        task_choices.append('(cancel)')

        task_question = [
            inquirer.List('task_id',
                         message="Select task to update",
                         choices=task_choices)
        ]

        task_answer = inquirer.prompt(task_question)
        if not task_answer or task_answer['task_id'] == '(cancel)':
            return  # User cancelled

        task_id = int(task_answer['task_id'])
        task = task_manager.find_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            input("Press Enter to continue...")
            return

        print(f"Current task details:")
        print(f"  ID: {task.id}")
        print(f"  Title: {task.title}")
        print(f"  Description: {task.description or '(none)'}")
        print(f"  Priority: {task.priority}")
        print(f"  Tags: {', '.join(task.tags) if task.tags else '(none)'}")
        print(f"  Due Date: {task.due_date or '(none)'}")
        print(f"  Status: {'Completed' if task.completed else 'Pending'}")

        # Ask what to update
        update_options = [
            'title', 'description', 'priority', 'tags', 'due_date'
        ]

        update_question = [
            inquirer.Checkbox('fields',
                            message="Select fields to update (space to select, Enter to continue)",
                            choices=update_options + ['(cancel)'])
        ]

        update_answer = inquirer.prompt(update_question)
        if not update_answer or '(cancel)' in update_answer['fields']:
            return  # User cancelled

        updates = {}

        for field in update_answer['fields']:
            if field == 'title':
                title_question = [
                    inquirer.Text('title', message="Enter new title", default=task.title)
                ]
                title_answer = inquirer.prompt(title_question)
                if not title_answer:
                    continue
                title = sanitize_input(title_answer['title'])
                if title and validate_task_title(title):
                    updates['title'] = title
                else:
                    print("Error: Invalid title.")
                    continue
            elif field == 'description':
                desc_question = [
                    inquirer.Text('description', message="Enter new description", default=task.description or "")
                ]
                desc_answer = inquirer.prompt(desc_question)
                if not desc_answer:
                    continue
                description = sanitize_input(desc_answer['description']) or None
                if description and not validate_task_description(description):
                    print("Error: Invalid description.")
                    continue
                updates['description'] = description
            elif field == 'priority':
                priority_question = [
                    inquirer.List('priority',
                                 message="Select new priority",
                                 choices=['high', 'medium', 'low'],
                                 default=task.priority)
                ]
                priority_answer = inquirer.prompt(priority_question)
                if not priority_answer:
                    continue
                updates['priority'] = priority_answer['priority']
            elif field == 'tags':
                # Offer to add or remove tags
                current_tags = task.tags if task.tags else []
                print(f"Current tags: {', '.join(current_tags) if current_tags else '(none)'}")

                tag_action_question = [
                    inquirer.List('action',
                                 message="Add or remove tags?",
                                 choices=['add', 'remove', 'replace'])
                ]
                action_answer = inquirer.prompt(tag_action_question)
                if not action_answer:
                    continue

                action = action_answer['action']

                if action == 'add':
                    new_tags_input = input("Enter tags to add, separated by commas: ").strip()
                    if new_tags_input:
                        new_tags = [sanitize_input(tag.strip()) for tag in new_tags_input.split(',') if tag.strip()]
                        if validate_task_tags(new_tags):
                            all_tags = list(set(current_tags + new_tags))  # Remove duplicates
                            updates['add_tags'] = new_tags
                        else:
                            print("Error: Invalid tags.")
                            continue
                elif action == 'remove':
                    if current_tags:
                        remove_questions = [
                            inquirer.Checkbox('tags',
                                            message="Select tags to remove (space to select, Enter to continue)",
                                            choices=current_tags + ['(cancel)'])
                        ]
                        remove_answer = inquirer.prompt(remove_questions)
                        if not remove_answer or '(cancel)' in remove_answer['tags']:
                            continue
                        remove_tags = [tag for tag in remove_answer['tags'] if tag != '(cancel)']
                        updates['remove_tags'] = remove_tags
                elif action == 'replace':
                    replace_tags_input = input("Enter new tags, separated by commas: ").strip()
                    if replace_tags_input:
                        replace_tags = [sanitize_input(tag.strip()) for tag in replace_tags_input.split(',') if tag.strip()]
                        if validate_task_tags(replace_tags):
                            # Remove all current tags first, then add new ones
                            updates['remove_tags'] = current_tags
                            updates['add_tags'] = replace_tags
                        else:
                            print("Error: Invalid tags.")
                            continue
            elif field == 'due_date':
                due_date_input = input(f"Enter new due date (YYYY-MM-DD format, current: {task.due_date or '(none)'}): ").strip()
                if due_date_input.lower() == 'none' or due_date_input == '':
                    updates['due_date'] = None
                else:
                    due_date = sanitize_input(due_date_input)
                    if validate_task_due_date(due_date):
                        updates['due_date'] = due_date
                    else:
                        print("Error: Invalid date format.")
                        continue

        # Confirm update
        if updates:
            confirm_question = [
                inquirer.Confirm('confirm',
                               message="Update task with these changes?")
            ]
            confirm_answer = inquirer.prompt(confirm_question)
            if not confirm_answer or not confirm_answer['confirm']:
                print("Update cancelled.")
                return

            # Perform update
            updated_task = task_manager.update_task(task_id, **updates)
            if updated_task:
                print(f"Task {task_id} updated successfully.")
            else:
                print(f"Error: Failed to update task {task_id}.")
        else:
            print("No updates made.")

        input("Press Enter to continue...")

    except ValueError:
        print("Error: Invalid input.")
        input("Press Enter to continue...")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except EOFError:
        print("\nOperation cancelled.")


def delete_task_interactive(task_manager):
    """Interactive task deletion"""
    try:
        import inquirer

        # Get all tasks to show as options
        tasks = task_manager.tasks
        if not tasks:
            print("No tasks available.")
            input("Press Enter to continue...")
            return

        # Create choices for task IDs
        task_choices = [f"{task.id}: {task.title}" for task in tasks]
        task_choices.append('(cancel)')

        task_question = [
            inquirer.List('task',
                         message="Select task to delete",
                         choices=task_choices)
        ]

        task_answer = inquirer.prompt(task_question)
        if not task_answer or task_answer['task'] == '(cancel)':
            return  # User cancelled

        # Extract task ID from selection
        selected_task_info = task_answer['task']
        task_id = int(selected_task_info.split(':')[0])

        task = task_manager.find_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            input("Press Enter to continue...")
            return

        # Confirm deletion
        confirm_question = [
            inquirer.Confirm('confirm',
                           message=f"Are you sure you want to delete task {task_id} '{task.title}'?")
        ]
        confirm_answer = inquirer.prompt(confirm_question)
        if not confirm_answer or not confirm_answer['confirm']:
            print("Deletion cancelled.")
            return

        success = task_manager.delete_task(task_id)
        if success:
            print(f"Task {task_id} deleted successfully.")
        else:
            print(f"Error: Failed to delete task {task_id}.")

        input("Press Enter to continue...")

    except ValueError:
        print("Error: Invalid task ID.")
        input("Press Enter to continue...")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except EOFError:
        print("\nOperation cancelled.")


def search_tasks_interactive(task_manager):
    """Interactive task search"""
    try:
        import inquirer

        # Get search query
        query_question = [
            inquirer.Text('query', message="Enter search query")
        ]
        query_answer = inquirer.prompt(query_question)
        if not query_answer:
            return  # User cancelled

        query = sanitize_input(query_answer['query'])
        if not query:
            print("Error: Search query cannot be empty.")
            input("Press Enter to continue...")
            return

        # Get search scope
        scope_question = [
            inquirer.List('scope',
                         message="Search in",
                         choices=['all fields', 'title only', 'description only', 'tags only'])
        ]
        scope_answer = inquirer.prompt(scope_question)
        if not scope_answer:
            return  # User cancelled

        # Determine search parameters
        search_in_title = search_in_description = search_in_tags = False

        if scope_answer['scope'] == 'all fields':
            search_in_title = search_in_description = search_in_tags = True
        elif scope_answer['scope'] == 'title only':
            search_in_title = True
        elif scope_answer['scope'] == 'description only':
            search_in_description = True
        elif scope_answer['scope'] == 'tags only':
            search_in_tags = True

        # Perform search
        results = search_tasks(task_manager.tasks, query, search_in_title, search_in_description, search_in_tags)

        if not results:
            print("No tasks found matching the search query.")
            input("Press Enter to continue...")
            return

        # Display search results in the same format as list command
        print(f"{'ID':<4} {'Status':<8} {'Priority':<8} {'Title':<30} {'Description':<30} {'Due Date':<12} {'Tags'}")
        print("-" * 120)
        for task in results:
            status_indicator = "[x]" if task.completed else "[ ]"
            title = task.title[:27] + "..." if len(task.title) > 30 else task.title
            description = (task.description[:27] + "..." if task.description and len(task.description) > 30 else (task.description or "")) if task.description else ""
            due_date_str = task.due_date or ""
            tags_str = ",".join(task.tags) if task.tags else ""
            print(f"{task.id:<4} {status_indicator:<8} {task.priority:<8} {title:<30} {description:<30} {due_date_str:<12} {tags_str}")

        input("Press Enter to continue...")

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except EOFError:
        print("\nOperation cancelled.")


def tag_tasks_interactive(task_manager):
    """Interactive tag operations"""
    try:
        import inquirer

        # Main tag operations menu
        tag_operations = [
            'list all tags',
            'list tasks with specific tag',
            '(back to main menu)'
        ]

        operation_question = [
            inquirer.List('operation',
                         message="Select tag operation",
                         choices=tag_operations)
        ]

        operation_answer = inquirer.prompt(operation_question)
        if not operation_answer or operation_answer['operation'] == '(back to main menu)':
            return  # User cancelled or back to main

        operation = operation_answer['operation']

        if operation == 'list all tags':
            # Collect all unique tags from all tasks
            all_tags = set()
            for task in task_manager.tasks:
                for tag in task.tags:
                    all_tags.add(tag)

            if not all_tags:
                print("No tags found.")
            else:
                print("Available tags:")
                for tag in sorted(all_tags):
                    print(f"  - {tag}")

            input("Press Enter to continue...")

        elif operation == 'list tasks with specific tag':
            # Get all available tags
            all_tags = set()
            for task in task_manager.tasks:
                for tag in task.tags:
                    all_tags.add(tag)

            if not all_tags:
                print("No tags available.")
                input("Press Enter to continue...")
                return

            # Ask for specific tag
            tag_question = [
                inquirer.List('tag',
                             message="Select tag to search for",
                             choices=sorted(list(all_tags)) + ['(cancel)'])
            ]

            tag_answer = inquirer.prompt(tag_question)
            if not tag_answer or tag_answer['tag'] == '(cancel)':
                return  # User cancelled

            tag_to_find = tag_answer['tag']

            # Find all tasks with the specified tag
            matching_tasks = [task for task in task_manager.tasks if tag_to_find in task.tags]

            if not matching_tasks:
                print(f"No tasks found with tag '{tag_to_find}'.")
            else:
                # Display matching tasks
                print(f"Tasks with tag '{tag_to_find}':")
                print(f"{'ID':<4} {'Status':<8} {'Priority':<8} {'Title':<30} {'Description':<30} {'Due Date':<12} {'Tags'}")
                print("-" * 120)
                for task in matching_tasks:
                    status_indicator = "[x]" if task.completed else "[ ]"
                    title = task.title[:27] + "..." if len(task.title) > 30 else task.title
                    description = (task.description[:27] + "..." if task.description and len(task.description) > 30 else (task.description or "")) if task.description else ""
                    due_date_str = task.due_date or ""
                    tags_str = ",".join(task.tags) if task.tags else ""
                    print(f"{task.id:<4} {status_indicator:<8} {task.priority:<8} {title:<30} {description:<30} {due_date_str:<12} {tags_str}")

            input("Press Enter to continue...")

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except EOFError:
        print("\nOperation cancelled.")


def show_help_interactive():
    """Display help information"""
    print("\nCLI Todo Application Help")
    print("=" * 40)
    print("This application helps you manage your tasks efficiently.")
    print("\nAvailable Operations:")
    print("  Add      - Create new tasks with title, description, priority, tags, and due date")
    print("  List     - View tasks with filtering and sorting options")
    print("  Complete - Mark tasks as complete/incomplete")
    print("  Update   - Modify existing task details")
    print("  Delete   - Remove tasks from your list")
    print("  Search   - Find tasks by keyword in title, description, or tags")
    print("  Tag      - View available tags or filter tasks by tag")
    print("  Help     - Show this help information")
    print("  Exit     - Quit the application")
    print("\nTips:")
    print("- Use arrow keys to navigate menus")
    print("- Press Enter to select options")
    print("- Press Ctrl+C at any time to cancel and return to main menu")
    print("=" * 40)
    input("Press Enter to continue...")


if __name__ == '__main__':
    # Check if any command-line arguments were provided
    import sys
    if len(sys.argv) > 1:
        # Use Click's normal command-line interface
        cli()
    else:
        # Run in interactive mode
        interactive_mode()