# Retrospective Review: [REVIEW SUBJECT]

**Goal Branch**: `[###-goal-name]` | **Date**: [DATE] | **Input**: [goal outcomes and execution data]
**Note**: This template is filled in by the `/goalkit.review` command. See `.goalkit/templates/commands/review.md` for the execution workflow.

## Summary

[Extract from goal outcomes: performance assessment, key learnings, and improvement recommendations]

## Review Context

<!--
  ACTION REQUIRED: Replace the content in this section with the retrospective details
  for the goal. The structure here is presented in advisory capacity to guide
  the review process.
-->

**Review Period**: [e.g., January 2024, Q1 2024, specific goal lifecycle or NEEDS CLARIFICATION]
**Goals Reviewed**: [e.g., specific goal or goals during period or N/A]
**Success Metrics**: [e.g., user satisfaction, engagement, conversion or NEEDS CLARIFICATION]
**Baseline Performance**: [e.g., previous performance data or NEEDS CLARIFICATION]
**Review Structure**: [periodic/ad-hoc - determines review approach]
**Success Thresholds**: [domain-specific, e.g., 80% achievement, 50% improvement, baseline maintenance or NEEDS CLARIFICATION]

## Vision Check

*GATE: Must pass before Review 0 analysis. Re-check after Review 1 completion.*

[Gates determined based on vision alignment]

## Review Structure

### Documentation (this goal)

```markdown
.goalkit/
├── goals/
│   └── [###-goal-name]/
│       ├── review.md        # This file (/goalkit.review command output)
│       ├── analysis.md      # Review 0 output (/goalkit.review command)
│       ├── insights.md      # Review 1 output (/goalkit.review command)
│       ├── recommendations.md # Review 1 output (/goalkit.review command)
│       └── action-items.md  # Review 2 output - detailed improvement steps
```

### Review Components
<!--
  ACTION REQUIRED: Replace the placeholder components below with the concrete retrospective
  elements for this review. Delete unused components and expand the chosen approach with
  real review elements. The delivered review must not include Component labels.
-->

```markdown
# [REMOVE IF UNUSED] Option 1: Standard Retrospective (DEFAULT)
- What Went Well: [Successful approaches and positive outcomes]
- What Did Not Go Well: [Challenges and areas for improvement]
- Goal Achievement Analysis: [Planned vs. actual results]
- Key Learnings: [Insights for future improvement]

# [REMOVE IF UNUSED] Option 2: Process-Focused (when "methodology-improvement" + "efficiency-focused" detected)
- Strategy Effectiveness: [Assessment of strategy selection and execution]
- Execution Insights: [Assessment of implementation approach]
- Measurement & Validation: [Assessment of metrics and validation methods]
- Process Improvements: [Specific recommendations for methodology]

# [REMOVE IF UNUSED] Option 3: Outcome-Focused (when "impact-driven" detected)
- Success Metrics Assessment: [Quantitative outcome evaluation]
- Value Delivered: [Assessment of business/user value created]
- ROI Analysis: [Return on investment evaluation]
- Future Recommendations: [Strategic next steps]
```

**Review Considerations**:

- **Learning Focus**: Extract insights for future improvement, not to assign blame
- **Evidence-Based**: Ground findings in observed data, not assumptions
- **Actionable Recommendations**: Every major finding should have a corresponding suggestion for improvement
- **Forward-Looking**: Focus on how to improve future goal achievement
- **Comprehensive Coverage**: Address goal definition, strategy, execution, and outcomes

**Review Decision**: [Document the selected review approach and reference the real approach captured above]

## Complexity Tracking

> **Fill ONLY if Vision Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., Complex review structure] | [current need] | [why simple approach insufficient] |
| [e.g., Multi-dimensional analysis] | [specific problem] | [why single-metric approach insufficient] |