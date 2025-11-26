---
description: Create measurable milestone checkpoints to track goal progress using the milestone template to generate tracking artifacts.
handoffs:
  - label: Execute with Learning
    agent: goalkit.execute
    prompt: Implement with learning and adaptation
    send: true
  - label: Create Checklist
    agent: goalkit.checklist
    prompt: Create a checklist for the following domain...
scripts:
  sh: scripts/bash/setup-milestones.sh --json
  ps: scripts/powershell/setup-milestones.ps1 -Json
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

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for GOAL_SPEC, MILESTONE_PLAN, GOALS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read GOAL_SPEC and `strategies.md`. Load MILESTONE_PLAN template (already copied).

3. **Validate Strategy Alignment**:
   - Confirm all milestones are sequenced to deliver selected strategy
   - Verify each milestone has clear success criteria tied to goal metrics
   - ERROR if milestones don't trace back to strategy selection

4. **Execute milestone workflow**: Follow the structure in MILESTONE_PLAN template to:
    - Fill Progress Tracking Context (mark unknowns as "NEEDS CLARIFICATION")
    - Fill Milestones Check section with phase gates and KPIs
    - Evaluate gates (ERROR if violations unjustified)
    - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
    - Phase 1: Generate data-model.md, contracts/, quickstart.md
    - Phase 1: Update agent context by running the agent script
    - Re-evaluate Milestones Check post-definition

5. **Validate Milestones Check gate**:
   - Ensure all 3 milestones are measurable with specific KPIs
   - Confirm deliverables and dependencies are clearly defined
   - Verify timeline is realistic and resource-constrained
   - ERROR if milestones lack measurable success criteria

6. **Stop and report**: Command ends after Phase 2 milestone definition. Report branch, MILESTONE_PLAN path, milestone sequence, and generated artifacts.

## Phases

### Phase 0: Milestone Outline & Research

1. **Extract unknowns from Progress Tracking Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each measurement approach → best practices task
   - For each tracking method → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Progress Tracking Context:
     Task: "Research {unknown} for {goal context}"
   For each tracking approach:
     Task: "Find best practices for {approach} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Milestone Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract key progress indicators from goal spec** → `data-model.md`:
   - Key measurable outcomes, success metrics, validation criteria
   - Progress indicators from requirements
   - Risk factors and mitigation points

2. **Generate milestone contracts** from progress requirements:
   - For each milestone → acceptance criteria
   - Use standard milestone planning patterns
   - Output milestone documentation to `/contracts/`

3. **Agent context update**:
   - Run `{AGENT_SCRIPT}`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new milestone elements from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key Rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications
