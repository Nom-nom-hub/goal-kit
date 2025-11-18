# Implementation Tasks: [GOAL]

**Goal Branch**: `[###-goal-name]` | **Date**: [DATE] | **Input**: [goal/milestones/execution plans]
**Note**: This template is filled in by the `/goalkit.tasks` command. See `.goalkit/templates/commands/tasks.md` for the execution workflow.

## Summary

[Extract from goal and execution: primary deliverables, task breakdown approach, and implementation priorities]

## Task Context

<!--
  ACTION REQUIRED: Replace the content in this section with the implementation details
  for the goal. The structure here is presented in advisory capacity to guide
  the task breakdown process.
-->

**Goal Priority**: [e.g., P1-Critical, P2-High, P3-Medium or NEEDS CLARIFICATION]
**Task Approach**: [e.g., Agile, Waterfall, Experimental or NEEDS CLARIFICATION]
**Resource Allocation**: [if applicable, e.g., 2 person-weeks, 50 hours or N/A]
**Success Metrics**: [e.g., user satisfaction, engagement, conversion or NEEDS CLARIFICATION]
**Target Timeline**: [e.g., Q1 2024, 3 months, 6 sprints or NEEDS CLARIFICATION]
**Team Structure**: [single/multi-person - determines collaboration approach]
**Risk Tolerance**: [domain-specific, e.g., low-risk conservative, medium-risk balanced, high-risk experimental or NEEDS CLARIFICATION]
**Success Thresholds**: [domain-specific, e.g., 80% achievement, 50% improvement, baseline maintenance or NEEDS CLARIFICATION]

## Vision Check

*GATE: Must pass before Task 0 planning. Re-check after Task 1 definition.*

[Gates determined based on vision document]

## Task Structure

### Documentation (this goal)

```markdown
.goalkit/
├── goals/
│   └── [###-goal-name]/
│       ├── tasks.md         # This file (/goalkit.tasks command output)
│       ├── research.md      # Task 0 output (/goalkit.tasks command)
│       ├── data-model.md    # Task 1 output (/goalkit.tasks command)
│       ├── quickstart.md    # Task 1 output (/goalkit.tasks command)
│       ├── contracts/       # Task 1 output (/goalkit.tasks command)
│       └── action-items.md  # Task 2 output - detailed work breakdown
```

### Task Breakdown Options
<!--
  ACTION REQUIRED: Replace the placeholder breakdowns below with the concrete task
  breakdown for this goal. Delete unused breakdowns and expand the chosen approach with
  real implementation tasks. The delivered plan must not include Breakdown labels.
-->

```markdown
# [REMOVE IF UNUSED] Option 1: Phase-Based Breakdown (DEFAULT)
- Foundation Tasks: [Core setup and preparation work]
- Implementation Tasks: [Core implementation work]
- Validation Tasks: [Testing and validation work]
- Integration Tasks: [Integration and deployment work]

# [REMOVE IF UNUSED] Option 2: Component-Focused (when "feature-heavy" + "modular" detected)
- Component 1 Tasks: [Tasks related to first major component]
- Component 2 Tasks: [Tasks related to second major component]
- Integration Tasks: [Tasks to connect components]
- End-to-End Tasks: [Tasks to validate complete functionality]

# [REMOVE IF UNUSED] Option 3: Priority-Driven (when "risk mitigation" detected)
- Critical Path Tasks: [Tasks that must be completed first]
- High-Impact Tasks: [Tasks with highest value delivery]
- Medium-Impact Tasks: [Tasks with moderate value delivery]
- Low-Impact Tasks: [Tasks with minimal value delivery]
```

**Task Considerations**:

- **Sequential Dependencies**: Identify tasks that must be completed in order
- **Parallel Execution**: Identify tasks that can be worked on simultaneously
- **Effort Estimation**: Assign relative effort values to each task
- **Risk Assessment**: Identify risky tasks that may need extra attention
- **Stakeholder Impact**: Identify tasks with significant stakeholder impact

**Task Decision**: [Document the selected task breakdown approach and reference the real approach captured above]

## Complexity Tracking

> **Fill ONLY if Vision Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., Complex task structure] | [current need] | [why simple approach insufficient] |
| [e.g., Multi-dependency tracking] | [specific problem] | [why single-dependency approach insufficient] |