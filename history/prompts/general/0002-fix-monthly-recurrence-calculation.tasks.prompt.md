---
id: 0002
title: Fix Monthly Recurrence Calculation
stage: tasks
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: unknown
command: sp.phr
labels: ["recurrence", "bug-fix", "monthly-tasks", "calendar"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - /mnt/d/GIAIC/Hackathon/Hackathon2.0/Phase1/main.py
tests: []
---

# PHR-0002: Fix Monthly Recurrence Calculation

## Prompt Text
In main.py around lines 748-808, the monthly recurrence date calculation and
single-instance creation are broken: the 30-day months list and February check
are wrong and the code only creates one missed instance. Fix by replacing manual
month/day heuristics with Python's calendar.monthrange(year, month) to get the
correct last day of the target month (handle year/month overflow by incrementing
month and adjusting year), and compute next_date using that last-day when the
original day is too large; also change the creation logic to a loop that
repeatedly advances last_completed by the recurrence_interval (days/weeks or
months) and creates one new Task per missed occurrence until next_date > today,
updating self.next_id and appending each new task; ensure monthly advancement
uses the same month-add logic each iteration and preserve intended fields
(completed=False, is_recurring=False) for each new instance, then call
save_tasks() once at the end.

## Response Text
Fixed the monthly recurrence date calculation in main.py by replacing the flawed manual month/day heuristics with calendar.monthrange() and implementing a proper loop to create all missed instances since the last completion.

## Outcome Impact
Fixed incorrect monthly recurrence logic that was creating only one missed instance instead of all missed instances, and corrected the flawed 30-day month and February handling logic.

## Tests Summary
none

## Files Summary
- /mnt/d/GIAIC/Hackathon/Hackathon2.0/Phase1/main.py: Updated check_and_create_recurring_tasks method and added _get_next_monthly_date helper method

## Next Prompts
none

## Reflection Note
Using calendar.monthrange() provides the correct last day of any month, properly handling leap years and month boundaries, which was the core issue in the original implementation.

## Acceptance Criteria
- [x] Import calendar module added
- [x] Monthly recurrence calculation fixed using calendar.monthrange()
- [x] Loop implemented to create all missed instances, not just one
- [x] Proper handling of month/year overflow
- [x] Day overflow handled correctly (e.g., Jan 31 + monthly = Feb 28/29)
- [x] All new instances have correct fields (completed=False, is_recurring=False)

## Failure Modes Observed
none

## Next Experiment to Improve Prompt Quality
none