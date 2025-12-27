# Implementation Tasks: CLI Todo App Core Functionality

**Feature**: CLI Todo App Core Functionality
**Branch**: `001-todo-app-core`
**Spec**: specs/001-todo-app-core/spec.md
**Plan**: specs/001-todo-app-core/plan.md

## Implementation Strategy

MVP approach: Implement User Story 1 (Add New Tasks) first as it's foundational, then build other features incrementally. Each user story should be independently testable and deliver value.

## Dependencies

User stories can be implemented in parallel after foundational setup, but US1 (Add Tasks) should be completed before US2 (View Tasks) for full functionality.

## Parallel Execution Examples

- US3 (Mark Complete) and US4 (Update Task Details) can be developed in parallel after foundational components are in place
- US5 (Delete Tasks) can be developed independently after the TaskService is implemented

---

## Phase 1: Setup

### Goal
Initialize project structure and dependencies for the CLI Todo application.

- [x] T001 Create project directory structure: src/todo_cli/
- [x] T002 Create pyproject.toml with Python 3.11 requirement and Click dependency
- [x] T003 Create main.py file in src/todo_cli/ directory
- [x] T004 Create .gitignore file with Python patterns
- [x] T005 Set up basic Click CLI structure in main.py with "todo" group

---

## Phase 2: Foundational Components

### Goal
Implement core data models and services that will be used by all user stories.

- [x] T006 [P] Implement Task data class in main.py with id, title, description, completed, created_at, updated_at attributes
- [x] T007 [P] Implement TaskManager class in main.py to handle in-memory storage and operations
- [x] T008 [P] Implement JSON persistence functionality for tasks in main.py
- [x] T009 [P] Implement input validation functions for task attributes in main.py
- [x] T010 [P] Implement timestamp utility functions for created_at and updated_at in main.py

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1)

### Goal
Enable users to create new todo items so that they can keep track of tasks they need to complete.

### Independent Test Criteria
Can be fully tested by creating new tasks and verifying they appear in the task list, delivering the core value of task tracking.

- [x] T011 [US1] Implement "add" command in main.py with title and optional description parameters
- [x] T012 [US1] Implement validation for task title (non-empty, max length 255 chars)
- [x] T013 [US1] Implement validation for task description (max length 1000 chars if provided)
- [x] T014 [US1] Implement task creation logic with auto-incrementing ID and timestamp generation
- [x] T015 [US1] Implement JSON persistence for newly created tasks
- [x] T016 [US1] Add error handling for empty title input with appropriate error message
- [x] T017 [US1] Add success message with assigned task ID after task creation

---

## Phase 4: User Story 2 - View Task List (Priority: P1)

### Goal
Enable users to see all their tasks in one place so that they can get an overview of what needs to be done.

### Independent Test Criteria
Can be fully tested by viewing the task list and verifying all added tasks are displayed, delivering the core value of task visibility.

- [x] T018 [US2] Implement "list" command in main.py with optional status filter parameter
- [x] T019 [US2] Implement task listing functionality with filtering by completion status
- [x] T020 [US2] Implement tabular output format for task display with ID, Status, Title, Description
- [x] T021 [US2] Implement visual indicators for task completion status ([ ] for incomplete, [x] for complete)
- [x] T022 [US2] Implement appropriate message when no tasks exist
- [x] T023 [US2] Add support for filtering tasks by status (all, completed, pending)

---

## Phase 5: User Story 3 - Mark Tasks as Complete (Priority: P2)

### Goal
Enable users to toggle the completion status of tasks so that they can track what they have finished.

### Independent Test Criteria
Can be fully tested by toggling task completion status and seeing the visual change, delivering the value of progress tracking.

- [x] T024 [US3] Implement "complete" command in main.py with task ID parameter
- [x] T025 [US3] Implement logic to toggle task completion status by ID
- [x] T026 [US3] Implement validation to ensure task with given ID exists
- [x] T027 [US3] Implement update of updated_at timestamp when completion status changes
- [x] T028 [US3] Add error handling for invalid task ID with appropriate error message
- [x] T029 [US3] Add success message after completion status change

---

## Phase 6: User Story 4 - Update Task Details (Priority: P2)

### Goal
Enable users to modify existing task details so that they can correct mistakes or update task information.

### Independent Test Criteria
Can be fully tested by updating task details and verifying changes are saved and displayed correctly, delivering the value of task maintenance.

- [x] T030 [US4] Implement "update" command in main.py with ID, title, and optional description parameters
- [x] T031 [US4] Implement logic to update task details by ID
- [x] T032 [US4] Implement validation to ensure task with given ID exists
- [x] T033 [US4] Implement validation for updated task title and description
- [x] T034 [US4] Implement update of updated_at timestamp when task details change
- [x] T035 [US4] Add error handling for invalid task ID with appropriate error message
- [x] T036 [US4] Add success message after task update

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P3)

### Goal
Enable users to remove tasks from their list so that they can clean up completed or irrelevant tasks.

### Independent Test Criteria
Can be fully tested by deleting a task and verifying it no longer appears in the list, delivering the value of list maintenance.

- [x] T037 [US5] Implement "delete" command in main.py with task ID parameter
- [x] T038 [US5] Implement logic to delete task by ID
- [x] T039 [US5] Implement validation to ensure task with given ID exists
- [x] T040 [US5] Add confirmation prompt for task deletion (to follow explicit user intent principle)
- [x] T041 [US5] Add error handling for invalid task ID with appropriate error message
- [x] T042 [US5] Add success message after task deletion

---

## Phase 8: Polish & Cross-Cutting Concerns

### Goal
Complete the application with proper error handling, documentation, and final touches.

- [x] T043 Implement consistent exit codes across all commands (0=success, 1=general error, 2=input error, 3=task not found)
- [x] T044 Add comprehensive help text for all commands following Click conventions
- [x] T045 Implement proper error handling for file I/O operations with appropriate messages
- [x] T046 Add input sanitization for all user inputs to prevent potential issues
- [x] T047 Implement proper logging of operations if needed
- [x] T048 Add README.md with usage instructions based on quickstart guide
- [x] T049 Test all commands and verify they work as specified in the CLI contract
- [x] T050 Perform end-to-end testing of all user workflows