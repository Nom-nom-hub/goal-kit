# Implementation Plan: [GOAL]

**Goal Branch**: `[###-goal-name]` | **Date**: [DATE] | **Input**: [link to goal/milestones]
**Note**: This template is filled in by the `/goalkit.execute` command. See `.goalkit/templates/commands/execute.md` for the execution workflow.

## Summary

[Extract from goal and milestones: primary outcome + implementation approach from research]

## Implementation Context

<!--
  ACTION REQUIRED: Replace the content in this section with the implementation details
  for the goal. The structure here is presented in advisory capacity to guide
  the execution process.
-->

**Goal Priority**: [e.g., P1-Critical, P2-High, P3-Medium or NEEDS CLARIFICATION]
**Implementation Approach**: [e.g., Agile, Waterfall, Experimental or NEEDS CLARIFICATION]
**Resource Allocation**: [if applicable, e.g., 2 person-weeks, 50 hours or N/A]
**Success Metrics**: [e.g., user satisfaction, engagement, conversion or NEEDS CLARIFICATION]
**Target Timeline**: [e.g., Q1 2024, 3 months, 6 sprints or NEEDS CLARIFICATION]
**Team Structure**: [single/multi-person - determines collaboration approach]
**Risk Tolerance**: [domain-specific, e.g., low-risk conservative, medium-risk balanced, high-risk experimental or NEEDS CLARIFICATION]
**Success Thresholds**: [domain-specific, e.g., 80% achievement, 50% improvement, baseline maintenance or NEEDS CLARIFICATION]

## Vision Check

*GATE: Must pass before Implementation 0 planning. Re-check after Implementation 1 execution.*

[Gates determined based on vision document]

## Implementation Structure

### Documentation (this goal)

```markdown
.goalkit/
├── goals/
│   └── [###-goal-name]/
│       ├── execution.md       # This file (/goalkit.execute command output)
│       ├── research.md        # Implementation 0 output (/goalkit.execute command)
│       ├── data-model.md      # Implementation 1 output (/goalkit.execute command)
│       ├── quickstart.md      # Implementation 1 output (/goalkit.execute command)
│       ├── contracts/         # Implementation 1 output (/goalkit.execute command)
│       └── tasks.md           # Implementation 2 output - detailed implementation tasks
```

### Implementation Phases
<!--
  ACTION REQUIRED: Replace the placeholder phases below with the concrete implementation
  phases for this goal. Delete unused phases and expand the chosen approach with
  real implementation elements. The delivered plan must not include Phase labels.
-->

```markdown
# [REMOVE IF UNUSED] Option 1: Iterative Implementation (DEFAULT)
- Phase 1: [Core validation of key assumptions]
- Phase 2: [Initial working version or proof of concept]
- Phase 3: [User validation and refinement]
- Phase 4: [Full implementation and testing]

# [REMOVE IF UNUSED] Option 2: Learning-Focused (when "hypothesis-heavy" + "risk mitigation" detected)
- Phase 1: [Core concept validation with low-fidelity prototypes]
- Phase 2: [Technical feasibility with working prototype]
- Phase 3: [User validation with real users]
- Phase 4: [Business validation with broader rollout]

# [REMOVE IF UNUSED] Option 3: Value-Delivery (when "incremental value" detected)
- Phase 1: [Core value phase - deliver fundamental benefit]
- Phase 2: [Enhancement phase - add incremental improvements]
- Phase 3: [Scale phase - expand to broader user base]
- Phase 4: [Optimization phase - improve existing functionality]
```

**Implementation Considerations**:

- **Progressive Validation**: Early phases validate riskiest assumptions
- **Independent Value**: Each phase delivers standalone value
- **Adaptive Execution**: Phases can be modified based on learning
- **Learning Integration**: Each phase builds on insights from previous ones
- **Stakeholder Communication**: Clear progress indicators for stakeholders

**Implementation Decision**: [Document the selected implementation approach and reference the real approach captured above]

## Complexity Tracking

> **Fill ONLY if Vision Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., Complex implementation structure] | [current need] | [why simple approach insufficient] |
| [e.g., Multi-phase validation] | [specific problem] | [why single-phase approach insufficient] |