---
description: Create a new goal with specifications and milestones
scripts:
  sh: create-goal.sh
  ps: create-goal.ps1
---

## Goal Creation Command

Create and define a new goal with the following specifications:

**Command**: `{SCRIPT} {ARGS}`

### Parameters
- `name`: Name of the goal
- `description`: Detailed description of what the goal aims to achieve
- `category`: Category of the goal (personal, business, learning, etc.)
- `priority`: Priority level (high, medium, low)
- `milestones`: Key milestones to track progress

### Usage
This command will create a new goal specification file following the goal-template.json structure. The goal will include:

1. Goal metadata (name, description, category, priority)
2. Milestone definitions with success criteria
3. Optional dependencies and resources
4. Timeline and deadline information

### Output
A new goal specification file will be created in the appropriate directory with proper structure and validation.

**Agent Type**: __AGENT__