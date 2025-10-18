# Strategy Plan: [GOAL]

**Branch**: `[###-goal-name]` | **Date**: [DATE] | **Goal**: [link]
**Input**: Goal definition from `/goals/[###-goal-name]/goal.md`

**Note**: This template is filled in by the `/goalkit.strategies` command. See `.goalkit/templates/commands/strategies.md` for the execution workflow.

## Summary

[Extract from goal definition: primary outcome + strategic approach from research]

## Strategic Context

<!--
  ACTION REQUIRED: Replace the content in this section with the strategic details
  for the goal. The structure here is presented in advisory capacity to guide
  the strategy exploration process.
-->

**Goal Priority**: [e.g., P1-Critical, P2-High, P3-Medium or NEEDS CLARIFICATION]  
**Strategic Alignment**: [e.g., User Experience, Business Growth, Technical Debt or NEEDS CLARIFICATION]  
**Resource Budget**: [if applicable, e.g., 2 person-months, $50K, 100 hours or N/A]  
**Success Metrics**: [e.g., user satisfaction, engagement, conversion or NEEDS CLARIFICATION]  
**Target Timeline**: [e.g., Q1 2024, 3 months, 6 sprints or NEEDS CLARIFICATION]
**Team Structure**: [single/multi-team - determines collaboration approach]  
**Risk Tolerance**: [domain-specific, e.g., low-risk conservative, medium-risk balanced, high-risk experimental or NEEDS CLARIFICATION]  
**Success Thresholds**: [domain-specific, e.g., 80% achievement, 50% improvement, baseline maintenance or NEEDS CLARIFICATION]

## Vision Check

*GATE: Must pass before Strategy 0 research. Re-check after Strategy 1 planning.*

[Gates determined based on vision document]

## Strategy Structure

### Documentation (this goal)

```
goals/[###-goal-name]/
├── strategies.md        # This file (/goalkit.strategies command output)
├── research.md          # Strategy 0 output (/goalkit.strategies command)
├── data-model.md        # Strategy 1 output (/goalkit.strategies command)
├── quickstart.md        # Strategy 1 output (/goalkit.strategies command)
├── contracts/           # Strategy 1 output (/goalkit.strategies command)
└── actions.md           # Strategy 2 output - detailed implementation tasks
```

### Strategy Options
<!-- 
  ACTION REQUIRED: Replace the placeholder options below with the concrete strategic
  approaches for this goal. Delete unused options and expand the chosen approach with
  real strategic elements. The delivered plan must not include Option labels.
-->

```
# [REMOVE IF UNUSED] Option 1: Direct Implementation (DEFAULT)
- Approach: [Implement goal directly with primary strategy]
- Resources: [team size and skill requirements]
- Timeline: [estimated implementation period]
- Risk: [estimated risk level]

# [REMOVE IF UNUSED] Option 2: Iterative Approach (when "learn-first" + "risk mitigation" detected)
- Approach: [Experiment with multiple strategies before committing]
- Resources: [research and experimentation time required]
- Timeline: [research + implementation period]
- Risk: [reduced risk through learning]

# [REMOVE IF UNUSED] Option 3: Phased Implementation (when "complex goal" detected)
- Phase 1: [Initial milestone with core functionality]
- Phase 2: [Secondary milestone with advanced features]
- Phase 3: [Final milestone with optimization]
```

**Strategy Decision**: [Document the selected strategy and reference the real approach captured above]

## Complexity Tracking

*Fill ONLY if Vision Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., High complexity strategy] | [current need] | [why simple approach insufficient] |
| [e.g., Multi-team coordination] | [specific problem] | [why single-team approach insufficient] |