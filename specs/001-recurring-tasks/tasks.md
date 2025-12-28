---
description: "Task list for recurring tasks feature implementation"
---

# Tasks: Recurring Tasks

**Input**: Design documents from `/specs/001-recurring-tasks/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `main.py` at repository root
- **Tests**: `tests/` at repository root
- Paths adjusted for CLI TODO application structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Update main.py with recurring tasks imports and dataclass extensions
- [x] T002 [P] Add required imports for datetime and date calculations in main.py
- [ ] T003 [P] Create tests/unit/test_recurring_tasks.py file
- [ ] T004 [P] Create tests/integration/test_cli_recurring.py file

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Extend Task class with recurrence metadata fields in main.py
- [x] T006 Create RecurrencePattern class in main.py
- [x] T007 Create RecurringTaskTemplate class in main.py
- [x] T008 Add recurrence utility functions for date calculations in main.py
- [x] T009 Update TaskManager to handle recurring tasks in main.py
- [x] T010 Add basic CLI command group for recurring tasks in main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Recurring Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to create recurring task templates that automatically generate new task instances based on defined recurrence patterns

**Independent Test**: Can be fully tested by creating a recurring task with a specific schedule and verifying that new instances of the task are automatically generated at the specified intervals.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T011 [P] [US1] Contract test for todo recurring create command in tests/contract/test_recurring_contracts.py
- [ ] T012 [P] [US1] Integration test for creating recurring task workflow in tests/integration/test_cli_recurring.py

### Implementation for User Story 1

- [x] T013 [P] [US1] Implement RecurrencePattern validation methods in main.py
- [x] T014 [US1] Implement recurring task creation logic in TaskManager in main.py
- [x] T015 [US1] Add recurring task instance generation methods in TaskManager in main.py
- [x] T016 [US1] Implement todo recurring create command in main.py
- [x] T017 [US1] Add input validation for recurrence patterns in main.py
- [x] T018 [US1] Add recurrence pattern parsing and validation in main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Manage Recurring Task Patterns (Priority: P2)

**Goal**: Allow users to modify the recurrence pattern of their recurring tasks (change frequency, end date, etc.) so that they can adjust the schedule as their needs change

**Independent Test**: Can be tested by creating a recurring task, modifying its pattern, and verifying that future instances follow the new pattern.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T019 [P] [US2] Contract test for todo recurring update command in tests/contract/test_recurring_contracts.py
- [ ] T020 [P] [US2] Contract test for todo recurring list command in tests/contract/test_recurring_contracts.py

### Implementation for User Story 2

- [x] T021 [P] [US2] Implement recurring task update logic in TaskManager in main.py
- [x] T022 [US2] Implement recurring task listing logic in TaskManager in main.py
- [x] T023 [US2] Implement todo recurring update command in main.py
- [x] T024 [US2] Implement todo recurring list command in main.py
- [x] T025 [US2] Add end condition validation and handling in main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Complete Recurring Task Instances (Priority: P3)

**Goal**: Allow users to complete individual instances of recurring tasks while preserving the recurrence pattern so that they can track progress without disrupting the ongoing schedule

**Independent Test**: Can be tested by completing an instance of a recurring task and verifying that the next scheduled instance still appears.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T026 [P] [US3] Contract test for todo recurring pause/resume commands in tests/contract/test_recurring_contracts.py
- [ ] T027 [P] [US3] Integration test for completing recurring task instances in tests/integration/test_cli_recurring.py

### Implementation for User Story 3

- [x] T028 [P] [US3] Implement recurring task pause/resume logic in TaskManager in main.py
- [x] T029 [US3] Implement todo recurring pause command in main.py
- [x] T030 [US3] Implement todo recurring resume command in main.py
- [x] T031 [US3] Implement todo recurring delete command in main.py
- [x] T032 [US3] Add proper handling of completed instances vs template in main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T033 [P] Update README with recurring tasks documentation
- [ ] T034 Add comprehensive help text for recurring commands in main.py
- [ ] T035 Add error handling for edge cases in recurring functionality in main.py
- [ ] T036 [P] Add unit tests for recurrence pattern logic in tests/unit/test_recurrence_patterns.py
- [ ] T037 Add timezone handling for recurrence patterns in main.py
- [ ] T038 Run quickstart.md validation for recurring tasks feature

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for todo recurring create command in tests/contract/test_recurring_contracts.py"
Task: "Integration test for creating recurring task workflow in tests/integration/test_cli_recurring.py"

# Launch all models for User Story 1 together:
Task: "Implement RecurrencePattern validation methods in main.py"
Task: "Implement recurring task creation logic in TaskManager in main.py"
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
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
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