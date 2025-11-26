---
description: Explore multiple strategic approaches to achieve the goal using the strategy template to generate strategic artifacts.
handoffs:
  - label: Create Milestones
    agent: goalkit.milestones
    prompt: Create measurable progress checkpoints for the selected strategy
    send: true
  - label: Create Checklist
    agent: goalkit.checklist
    prompt: Create a checklist for the following domain...
scripts:
  sh: scripts/bash/setup-strategy.sh --json
  ps: scripts/powershell/setup-strategy.ps1 -Json
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

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for GOAL_SPEC, STRATEGY_PLAN, GOALS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read GOAL_SPEC and `/memory/vision.md`. Load STRATEGY_PLAN template (already copied).

3. **Validate Goal Alignment**:
   - Confirm all 3 strategy options directly address goal's success metrics
   - Verify each option's assumptions are justified
   - ERROR if strategies drift from goal scope

4. **Execute strategy workflow**: Follow the structure in STRATEGY_PLAN template to:
    - Fill Strategic Context (mark unknowns as "NEEDS CLARIFICATION")
    - Fill Strategy Check section (evaluation criteria, decision rationale)
    - Evaluate gates (ERROR if violations unjustified)
    - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
    - Phase 1: Generate data-model.md, contracts/, quickstart.md
    - Phase 1: Update agent context by running the agent script
    - Re-evaluate Strategy Check post-selection

5. **Validate Strategy Check gate**:
   - Ensure decision rationale clearly explains why selected strategy was chosen
   - Verify all 3 options were rigorously evaluated against criteria
   - Confirm key assumptions are explicit and justified
   - ERROR if strategy selection lacks clear rationale

6. **Stop and report**: Command ends after Phase 2 planning. Report branch, STRATEGY_PLAN path, selected strategy, and generated artifacts.

## Phases

### Phase 0: Strategy Outline & Research

1. **Extract unknowns from Strategic Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each strategic approach → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Strategic Context:
     Task: "Research {unknown} for {goal context}"
   For each strategic approach:
     Task: "Find best practices for {approach} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Strategy Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract key elements from goal spec** → `data-model.md`:
   - Key deliverables, success metrics, constraints
   - Validation criteria from requirements
   - Risk factors and mitigation approaches

2. **Generate strategy contracts** from strategic requirements:
   - For each strategic approach → validation criteria
   - Use standard strategic planning patterns
   - Output approach documentation to `/contracts/`

3. **Agent context update**:
   - Run `{AGENT_SCRIPT}`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new strategic elements from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key Rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications
