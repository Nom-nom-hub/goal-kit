---
description: Generate detailed implementation tasks from goals and execution plans using the tasks template to break down work into actionable items.
handoffs:
  - label: Convert Tasks to Issues
    agent: goalkit.taskstoissues
    prompt: Convert these tasks into GitHub issues
    send: true
  - label: Create Checklist
    agent: goalkit.checklist
    prompt: Create a checklist for the following domain...
scripts:
  sh: scripts/bash/generate-tasks.sh --json
  ps: scripts/powershell/generate-tasks.ps1 -Json
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

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for GOAL_SPEC, MILESTONES, STRATEGY_PLAN, EXECUTION_PLAN, TASKS_PLAN, GOALS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read GOAL_SPEC, MILESTONES, STRATEGY_PLAN, and EXECUTION_PLAN. Load TASKS_PLAN template (already copied).

3. **Execute task breakdown workflow**: Follow the structure in TASKS_PLAN template to:
   - Fill Implementation Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Vision Check section from vision
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Vision Check post-task definition

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, TASKS_PLAN path, and generated artifacts.

## Phases

### Phase 0: Task Outline & Research

1. **Extract unknowns from Implementation Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each implementation approach → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Implementation Context:
     Task: "Research {unknown} for {goal context}"
   For each implementation approach:
     Task: "Find best practices for {approach} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Task Definition & Contracts

**Prerequisites:** `research.md` complete

1. **Extract key elements from goal spec** → `data-model.md`:
   - Key deliverables, success metrics, constraints
   - Validation criteria from requirements
   - Risk factors and mitigation approaches

2. **Generate task contracts** from requirements:
   - For each task → acceptance criteria
   - Use standard task breakdown patterns
   - Output approach documentation to `/contracts/`

3. **Agent context update**:
   - Run `{AGENT_SCRIPT}`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new implementation elements from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key Rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications