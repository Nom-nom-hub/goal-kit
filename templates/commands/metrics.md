---
description: Create a detailed measurement plan for tracking goal success criteria using the metrics template to generate measurement artifacts.
handoffs:
  - label: View Metrics Dashboard
    agent: goalkit.analytics
    prompt: Display metrics dashboard and trends
    send: false
  - label: Create Checklist
    agent: goalkit.checklist
    prompt: Create a checklist for the following domain...
scripts:
  sh: scripts/bash/setup-metrics.sh --json
  ps: scripts/powershell/setup-metrics.ps1 -Json
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

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for GOAL_SPEC, METRICS_PLAN, GOALS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read GOAL_SPEC and extract all success criteria. Load METRICS_PLAN template (already copied).

3. **Validate Success Criteria Quality**:
   - Confirm all success criteria pass the 5-point quality checklist (Measurable, Actionable, Leading, Bounded, Valuable)
   - Verify each metric has clear baseline, target, and measurement method
   - ERROR if any success criterion fails quality validation

4. **Execute metrics workflow**: Follow the structure in METRICS_PLAN template to:
    - Fill Success Criteria Review table with all metrics from goal.md
    - Complete Metric Quality Validation for each criterion
    - Define Baseline Measurements (mark unknowns as "NEEDS CLARIFICATION")
    - Create Instrumentation Plan for data collection
    - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
    - Phase 1: Generate data-model.md, contracts/, quickstart.md
    - Phase 1: Update agent context by running the agent script
    - Define Decision Thresholds (green/yellow/red zones)

5. **Validate Metrics Check gate**:
   - Ensure all metrics are measurable with specific collection methods
   - Confirm instrumentation is feasible and testable
   - Verify decision thresholds are actionable
   - ERROR if metrics lack clear measurement or instrumentation plan

6. **Stop and report**: Command ends after metrics plan is complete. Report branch, METRICS_PLAN path, validated metrics count, and generated artifacts.

## Phases

### Phase 0: Metrics Research & Baseline

1. **Extract unknowns from Success Criteria** above:
   - For each NEEDS CLARIFICATION → research task
   - For each measurement method → best practices task
   - For each instrumentation approach → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Baseline Measurements:
     Task: "Research how to measure {metric} for {goal context}"
   For each instrumentation approach:
     Task: "Find best practices for {approach} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Metric: [what needs to be measured]
   - Method: [how to measure it]
   - Tools: [what tools/platforms to use]
   - Baseline: [current state if known]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Metrics Design & Instrumentation

**Prerequisites:** `research.md` complete

1. **Extract measurement requirements from goal spec** → `data-model.md`:
   - Key metrics, success criteria, validation methods
   - Data sources and collection points
   - Dashboard and reporting requirements

2. **Generate metrics contracts** from measurement requirements:
   - For each success criterion → instrumentation specification
   - Use standard metrics tracking patterns
   - Output measurement documentation to `/contracts/`

3. **Agent context update**:
   - Run `{AGENT_SCRIPT}`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new metrics elements from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key Rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications
- All metrics MUST pass 5-point quality validation
- Baselines MUST be measured before implementation begins
- Instrumentation MUST be testable and verifiable
