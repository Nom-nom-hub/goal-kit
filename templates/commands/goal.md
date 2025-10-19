---
description: Create a new goal with measurable outcomes and success criteria. This command ensures proper goal-driven development methodology.
scripts:
  sh: .goalkit/scripts/python/create_new_goal.py --json "{ARGS}"
  ps: .goalkit/scripts/python/create_new_goal.py --json "{ARGS}"
agent_scripts:
  sh: .goalkit/scripts/python/update_agent_context.py __AGENT__
  ps: .goalkit/scripts/python/update_agent_context.py __AGENT__
---

## Quick Start

**Goal Description**: `{ARGS}`

**STEP 1**: Run the Python script to create the goal structure:
```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/create_new_goal.py --json "{ARGS}"
```

**STEP 2**: Parse the JSON output to get:
- `GOAL_DIR`: Where the goal files are created
- `BRANCH_NAME`: The git branch for this goal
- `GOAL_FILE`: Path to the main goal.md file

**STEP 3**: Write a comprehensive goal definition to `GOAL_FILE` with:
- Clear goal statement and context
- Specific success metrics with targets (%, $, timeframes, user counts)
- Target users and stakeholders
- Key assumptions and risk factors
- Validation strategy

**STEP 4**: Create a quality checklist at `GOALS_DIR/checklists/goal-quality.md`

**STEP 5**: Report completion and remind user of next steps:
- `/goalkit.strategies` - Explore implementation approaches
- `/goalkit.milestones` - Create measurable progress checkpoints
- `/goalkit.execute` - Implement with learning and adaptation

## Critical Rules

✅ **DO**: Focus on measurable outcomes, not implementation details
✅ **DO**: Include specific success metrics with quantifiable targets
✅ **DO**: Identify target users and stakeholders
✅ **DO**: Document assumptions and validation methods
❌ **DON'T**: Include languages, frameworks, or APIs in goal definition
❌ **DON'T**: Skip success metrics or use vague targets
❌ **DON'T**: Forget to create the quality checklist

## Key Reminders

- **Simple tasks** → Use `/goalkit.execute` for direct implementation
- **Complex goals** → Use full methodology: goal → strategies → milestones → execute
- **Always** end with reminder to use `/goalkit.strategies` next