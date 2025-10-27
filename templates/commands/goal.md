---
description: Create a new goal with measurable outcomes and success criteria. This command ensures proper goal-driven development methodology.
scripts:
  sh: .goalkit/scripts/python/create_new_goal.py --json "{ARGS}"
  ps: .goalkit/scripts/python/create_new_goal.py --json "{ARGS}"
agent_scripts:
  sh: .goalkit/scripts/python/update_agent_context.py __AGENT__
  ps: .goalkit/scripts/python/update_agent_context.py __AGENT__
---

# ⚠️ CRITICAL: Proper Goal Creation Process

**Goal Description**: `{ARGS}`

**🚨 MANDATORY STEP 1**: Run the Python script to create the goal structure:

```python
cd "{PROJECT_ROOT}"
python scripts/python/create_new_goal.py --json "{ARGS}"
```

## **⚠️ CRITICAL: The --json flag is REQUIRED for proper workflow integration**

**🛡️ WORKFLOW ENFORCEMENT**: After running the script, verify compliance:

```python
python scripts/python/workflow_enforcer.py --check
```

**⚠️ DO NOT manually create goal directories** - This bypasses the proper methodology and will cause issues with:

- Goal numbering (001-, 002-, etc.)
- Git branch creation and management
- Goal template structure and validation
- Agent context updates
- Methodology compliance
- **Workflow enforcement detection** (violations will be logged and reported)

**STEP 2**: Parse the JSON output to get:

- `GOAL_DIR`: Where the goal files are created (in `.goalkit/goals/`)
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

**STEP 6**: Verify workflow compliance (recommended):

```bash
python scripts/python/workflow_enforcer.py --check
```

**🛑 STOP HERE** - Do NOT proceed to strategies or implementation automatically
**🛑 STOP HERE** - Wait for user to explicitly run `/goalkit.strategies`

## Critical Rules

✅ **DO**: Focus on measurable outcomes, not implementation details
✅ **DO**: Include specific success metrics with quantifiable targets
✅ **DO**: Identify target users and stakeholders
✅ **DO**: Document assumptions and validation methods
✅ **DO**: Run workflow compliance checks after goal creation
❌ **DON'T**: Include languages, frameworks, or APIs in goal definition
❌ **DON'T**: Skip success metrics or use vague targets
❌ **DON'T**: Forget to create the quality checklist
❌ **DON'T**: Skip the --json flag when running creation scripts
❌ **DON'T**: Bypass workflow enforcement verification

## Key Reminders

- **Simple tasks** → Use `/goalkit.execute` for direct implementation
- **Complex goals** → Use full methodology: goal → strategies → milestones → execute
- **Always** end with reminder to use `/goalkit.strategies` next
- **Workflow enforcement** → Run `python scripts/python/workflow_enforcer.py --check` to verify compliance
- **Script execution** → Always use `--json` flag for proper integration
