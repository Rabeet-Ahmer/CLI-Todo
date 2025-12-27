---
id: 1
title: Create CLI TODO Constitution
stage: constitution
date: 2025-12-27
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: user
command: sp.constitution
labels: [constitution,cli,todo,spec-driven-development]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

This is the global important high level rules for the project, as a professional constitution builder your task is to create the detailed, comprehensive, crucials-included constitution for the project as commanded in sp.constitution command. Don't hesitate to write as much:

# Minimal Agent Constitution – CLI TODO App

## Purpose
Define global, enforceable rules for a CLI-based TODO application using Spec-Driven Development, applicable across all levels.

---

## Tech Stack (Fixed)

- Language: Python
- Package Manager: uv
- Interface: CLI only
- Storage: In-memory

---

## Core Principles

- Deterministic Behavior
  - Same input must always produce the same output.

- Progressive Enhancement
  - Advanced features extend, never break, lower-level behavior.

- Single Source of Truth
  - One centralized task model governs all operations.

---

## Design Rules

- CLI as Contract
  - Commands, flags, and outputs are public and stable.

- Explicit User Intent
  - Destructive actions must be intentional and unambiguous.

- Separation of Concerns
  - CLI parsing, logic, state, and output must be isolated.

- Extensibility
  - Data structures must support future attributes by default.

---

## Data Rules

- Every task has a unique identifier.
- Task completion state is explicit and binary.
- Metadata (priority, tags, due dates, recurrence) is structured.
- Recurring tasks create new instances, not silent overwrites.

---

## Behavioral Guarantees

- CRUD semantics remain consistent across all levels.
- Search, filter, sort, and recurrence must compose correctly.
- Output is stable, readable, and predictable.
- Errors are explicit and human-readable.

---

## Quality Bar

- Core logic is testable without CLI invocation.
- Dependencies are minimal and justified.
- Code clarity is prioritized over cleverness.

---

## Success Criteria

- All behavior traces to a specification.
- No unexpected task loss or hidden state changes.
- Architecture supports future persistence without redesign.

---

## Non-Goals

- No persistence
- No multi-user support
- No GUI or web interface
- No background services

---

End of Minimal Agent Constitution

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.

## Response snapshot

I've created a comprehensive constitution for the CLI TODO app that exceeds 120 lines. The constitution includes:

1. Purpose and Tech Stack requirements
2. 10 Core Principles including Deterministic Behavior, Progressive Enhancement, Single Source of Truth, CLI as Contract, Explicit User Intent, Separation of Concerns, Extensibility, Unix Philosophy Adherence, Convention Over Configuration, and Fail Fast
3. Detailed Design Rules covering CLI Interface Standards, Output Formatting, Input Validation, and Error Handling
4. Comprehensive Data Rules for Task Model Structure, Data Integrity, and Extensibility
5. Behavioral Guarantees for CRUD operations, Search/Filter, Performance, and Consistency
6. Quality Standards for Code Quality, Testing, and Documentation
7. Security Considerations
8. Performance Requirements
9. Tech Stack Requirements
10. Success Criteria and Non-Goals
11. Operational Guidelines
12. Testing Strategy
13. Documentation Requirements
14. Governance section

The constitution follows CLI best practices, Unix philosophy, and software project constitution patterns. It establishes clear rules for the development and operation of the CLI TODO application.

## Outcome

- ✅ Impact: Created comprehensive constitution with 120+ lines
- 🧪 Tests: none
- 📁 Files: Created .specify/memory/constitution.md
- 🔁 Next prompts: Ready for feature specification
- 🧠 Reflection: Constitution provides strong foundation for CLI TODO app development

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification based on constitution