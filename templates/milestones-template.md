# Milestone Plan: [GOAL]

**Goal Branch**: `[###-goal-name]` | **Date**: [DATE] | **Strategy**: [link]
**Input**: Goal definition and selected strategy from `/goals/[###-goal-name]/`

**Note**: This template is filled in by the `/goalkit.milestones` command. See `.goalkit/templates/commands/milestones.md` for the execution workflow.

## Summary

[Extract from goal and strategy: primary outcome + milestone approach from research]

## Progress Tracking Context

<!--
  ACTION REQUIRED: Replace the content in this section with the milestone details
  for the goal. The structure here is presented in advisory capacity to guide
  the milestone planning process.
-->

**Goal Priority**: [e.g., P1-Critical, P2-High, P3-Medium or NEEDS CLARIFICATION]
**Milestone Alignment**: [e.g., User Experience, Business Growth, Technical Validation or NEEDS CLARIFICATION]
**Success Metrics**: [e.g., user satisfaction, engagement, conversion or NEEDS CLARIFICATION]
**Target Timeline**: [e.g., Q1 2024, 3 months, 6 sprints or NEEDS CLARIFICATION]
**Milestone Structure**: [single/multi-milestone - determines planning approach]
**Validation Thresholds**: [domain-specific, e.g., 80% achievement, 50% improvement, baseline maintenance or NEEDS CLARIFICATION]

## Vision Check

*GATE: Must pass before Milestone 0 planning. Re-check after Milestone 1 definition.*

[Gates determined based on vision document]

## Milestone Structure

### Documentation (this goal)

```markdown
.goalkit/
├── goals/
│   └── [###-goal-name]/
│       ├── milestones.md      # This file (/goalkit.milestones command output)
│       ├── research.md        # Milestone 0 output (/goalkit.milestones command)
│       ├── data-model.md      # Milestone 1 output (/goalkit.milestones command)
│       ├── quickstart.md      # Milestone 1 output (/goalkit.milestones command)
│       ├── contracts/         # Milestone 1 output (/goalkit.milestones command)
│       └── actions.md         # Milestone 2 output - detailed milestone tasks
```

### Milestone Options
<!--
  ACTION REQUIRED: Replace the placeholder options below with the concrete milestone
  approaches for this goal. Delete unused options and expand the chosen approach with
  real milestone elements. The delivered plan must not include Option labels.
-->

```markdown
# [REMOVE IF UNUSED] Option 1: Phased Milestones (DEFAULT)
- Milestone 1: [Core validation of key assumptions]
- Milestone 2: [Initial working version or proof of concept]
- Milestone 3: [User validation and refinement]
- Milestone 4: [Full implementation and testing]

# [REMOVE IF UNUSED] Option 2: Learning-Focused (when "hypothesis-heavy" + "risk mitigation" detected)
- Milestone 1: [Core concept validation with low-fidelity prototypes]
- Milestone 2: [Technical feasibility with working prototype]
- Milestone 3: [User validation with real users]
- Milestone 4: [Business validation with broader rollout]

# [REMOVE IF UNUSED] Option 3: Value-Delivery (when "incremental value" detected)
- Milestone 1: [Core value milestone - deliver fundamental benefit]
- Milestone 2: [Enhancement milestone - add incremental improvements]
- Milestone 3: [Scale milestone - expand to broader user base]
- Milestone 4: [Optimization milestone - improve existing functionality]
```

**Milestone Considerations**:

- **Progressive Validation**: Early milestones validate riskiest assumptions
- **Independent Value**: Each milestone delivers standalone value
- **Adaptive Planning**: Milestones can be modified based on learning
- **Learning Integration**: Each milestone builds on insights from previous ones
- **Stakeholder Communication**: Clear progress indicators for stakeholders

**Milestone Decision**: [Document the selected milestone approach and reference the real approach captured above]

## Complexity Tracking

> **Fill ONLY if Vision Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., Complex milestone structure] | [current need] | [why simple approach insufficient] |
| [e.g., Multi-phase validation] | [specific problem] | [why single-phase approach insufficient] |
