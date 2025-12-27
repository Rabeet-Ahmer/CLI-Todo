---
description: "Task list for implementing task enhancements - priorities, tags, search, filter, and sort functionality"
---

# Tasks: Task Enhancements - Priorities, Tags, Search, Filter & Sort

**Input**: Design documents from `/specs/001-task-enhancements/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: Single file `main.py` as specified in plan
- Paths shown below are for the single-file application structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backup of existing main.py before enhancements
- [ ] T002 [P] Add type hints imports for List and Optional in main.py
- [ ] T003 [P] Set up validation functions for new fields (priority, tags, due_date) in main.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Extend Task dataclass with new attributes (priority, tags, due_date) in main.py
- [ ] T005 Update TaskManager class to handle new Task attributes in main.py
- [ ] T006 [P] Update JSON serialization/deserialization to include new fields in main.py
- [ ] T007 [P] Add helper functions for date validation and parsing in main.py
- [ ] T008 [P] Add helper functions for priority and tag validation in main.py
- [ ] T009 Update existing CLI commands to maintain backward compatibility in main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Assign Task Priorities (Priority: P1) 🎯 MVP

**Goal**: Enable users to assign priority levels (high/medium/low) to tasks and visually distinguish them

**Independent Test**: Users can successfully set priority levels on tasks and see them visually distinguished in the task list, delivering immediate value in task organization.

### Implementation for User Story 1

- [ ] T010 [P] [US1] Add priority validation function in main.py
- [ ] T011 [US1] Enhance `add` command with --priority option in main.py
- [ ] T012 [US1] Enhance `update` command with --priority option in main.py
- [ ] T013 [US1] Modify task display format to show priority levels in main.py
- [ ] T014 [US1] Add priority-based sorting functionality in main.py
- [ ] T015 [US1] Update list command to support priority filtering in main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Apply Tags/Categories to Tasks (Priority: P1)

**Goal**: Enable users to assign tags or categories (like work/home) to tasks for grouping and organization

**Independent Test**: Users can successfully add tags to tasks and see them categorized, providing immediate value in organizing tasks by different contexts.

### Implementation for User Story 2

- [ ] T016 [P] [US2] Add tag validation function in main.py
- [ ] T017 [US2] Enhance `add` command with --tag option in main.py
- [ ] T018 [US2] Enhance `update` command with --add-tag and --remove-tag options in main.py
- [ ] T019 [US2] Add tag-based filtering functionality in main.py
- [ ] T020 [US2] Create new `tag` command with list and tasks subcommands in main.py
- [ ] T021 [US2] Update task display format to show tags in main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Search Tasks by Keyword (Priority: P2)

**Goal**: Enable users to search tasks by keyword across title, description, and tags

**Independent Test**: Users can enter search terms and see filtered results that match the keyword, delivering immediate value in task discovery.

### Implementation for User Story 3

- [ ] T022 [P] [US3] Add search utility functions in main.py
- [ ] T023 [US3] Create new `search` command with field filtering options in main.py
- [ ] T024 [US3] Implement search algorithm that searches across title, description, and tags in main.py
- [ ] T025 [US3] Add search-specific display format in main.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Filter Tasks by Status, Priority, or Date (Priority: P2)

**Goal**: Enable users to filter tasks by status (completed/pending), priority (high/medium/low), or date

**Independent Test**: Users can apply filters and see only the tasks that match the filter criteria, providing immediate value in task management.

### Implementation for User Story 4

- [ ] T026 [P] [US4] Add date filtering utility functions in main.py
- [ ] T027 [US4] Enhance `list` command with priority filtering option in main.py
- [ ] T028 [US4] Enhance `list` command with tag filtering option in main.py
- [ ] T029 [US4] Enhance `list` command with date filtering options (--due-before, --due-after) in main.py
- [ ] T030 [US4] Add overdue task filtering functionality in main.py
- [ ] T031 [US4] Implement compound filtering logic in main.py

**Checkpoint**: At this point, all user stories should be independently functional

---

## Phase 7: User Story 5 - Sort Tasks by Due Date, Priority, or Alphabetically (Priority: P3)

**Goal**: Enable users to sort tasks by due date, priority, or alphabetically

**Independent Test**: Users can select different sorting options and see tasks reordered accordingly, delivering value in task organization and visibility.

### Implementation for User Story 5

- [ ] T032 [P] [US5] Add sorting utility functions in main.py
- [ ] T033 [US5] Enhance `list` command with sorting options (--sort, --order) in main.py
- [ ] T034 [US5] Implement due date sorting functionality in main.py
- [ ] T035 [US5] Implement priority sorting functionality in main.py
- [ ] T036 [US5] Implement alphabetical sorting functionality in main.py
- [ ] T037 [US5] Handle edge cases for sorting (tasks with missing due dates) in main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T038 [P] Update help text for all enhanced commands in main.py
- [ ] T039 [P] Add comprehensive error handling for new functionality in main.py
- [ ] T040 [P] Add exit codes for new validation errors in main.py
- [ ] T041 [P] Update interactive mode to support new commands and options in main.py
- [ ] T042 [P] Add backward compatibility for loading existing task files in main.py
- [ ] T043 [P] Add input sanitization for new fields in main.py
- [ ] T044 [P] Run quickstart.md validation scenarios in main.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all parallel tasks for User Story 1:
Task: "Add priority validation function in main.py"
Task: "Enhance `add` command with --priority option in main.py"
Task: "Enhance `update` command with --priority option in main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence