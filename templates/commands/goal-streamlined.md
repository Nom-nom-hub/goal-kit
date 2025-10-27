---
description: Create a new goal with measurable outcomes and success criteria.
scripts:
  sh: .goalkit/scripts/python/create_new_goal.py --json "{ARGS}"
  ps: .goalkit/scripts/python/create_new_goal.py --json "{ARGS}"
agent_scripts:
  sh: .goalkit/scripts/python/update_agent_context.py __AGENT__
  ps: .goalkit/scripts/python/update_agent_context.py __AGENT__
---

# Goal Creation

**Goal**: `{ARGS}`

## Quick Process

1. **Run script**: `python scripts/python/create_new_goal.py --json "{ARGS}"`
2. **Parse JSON** output for goal directory and file paths
3. **Write goal.md** with clear outcomes and success metrics
4. **Choose next**: `/goalkit.strategies` (complex) or `/goalkit.execute` (simple)

## Essential Elements

- **Clear goal statement** - What success looks like
- **Measurable success criteria** - Specific targets (%, $, timeframes, user counts)
- **Target users/stakeholders** - Who benefits from this goal
- **Validation approach** - How you'll know it's achieved

## Guidelines

✅ **Focus on outcomes**, not implementation
✅ **Use specific metrics** with quantifiable targets
✅ **Document assumptions** and validation methods
❌ **Avoid technical details** (languages, frameworks, APIs)

## For Simple Tasks

Tasks like "fix button styling" or "update error message" can use `/goalkit.execute` directly.
