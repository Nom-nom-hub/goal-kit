---
description: Create and plan a milestone for a goal
scripts:
  sh: create-goal.sh --milestone
  ps: create-goal.ps1 -Milestone
---

## Milestone Creation Command

Define and create a milestone within a goal with the following specifications:

**Command**: `{SCRIPT} {ARGS}`

### Parameters

- `goal_id`: ID of the parent goal
- `name`: Name of the milestone
- `description`: Detailed description of the milestone
- `due_date`: Expected completion date
- `dependencies`: List of dependencies (other milestones or tasks)
- `success_criteria`: Clear criteria for milestone completion

### Usage

This command will create a new milestone specification following best practices for goal management. The milestone will include:

1. Clear success criteria and deliverables
2. Timeline and dependencies mapping
3. Resource requirements and potential blockers
4. Progress tracking mechanisms

### Output

A new milestone specification will be added to the parent goal's structure with proper validation.

**Agent Type**: **AGENT**
