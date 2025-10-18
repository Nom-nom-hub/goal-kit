---
description: Execute the goal definition workflow by creating a new goal using the goal template to generate a goal definition.
scripts:
  sh: scripts/bash/create-new-goal.sh --json
  ps: scripts/powershell/create-new-goal.ps1 -Json
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for GOAL_DESCRIPTION, GOALS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read `.goalkit/vision.md` and load goal template from `templates/goal-template.md`.

3. **Execute goal workflow**: Follow the structure in goal template to:
   - Fill Goal Overview (Goal Statement, Context, Success Level)
   - Fill Success Metrics (Primary and Secondary metrics with targets)
   - Fill Target Users & Stakeholders (Primary Users and Stakeholders)
   - Fill Goal Hypotheses (Key Assumptions and Risk Factors)
   - Fill Goal Milestones (Measurable progress steps)
   - Fill Validation Strategy (Measurement approach and learning objectives)

4. **Goal Validation**: Ensure success metrics are specific, measurable, and achievable.

5. **Stop and report**: Command ends after goal creation. Report branch, goal path, and generated artifacts.

## Key rules

- Use absolute paths
- All metrics must be quantifiable with specific targets (%, $, timeframes, user counts)
- Each goal must include testable hypotheses with validation methods
- Goal should align with existing project vision in `.goalkit/vision.md`