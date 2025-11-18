# Progress Report: [REPORT PERIOD/TITLE]

**Goal Branch**: `[###-goal-name]` | **Date**: [DATE] | **Input**: [goal outcomes and metrics]
**Note**: This template is filled in by the `/goalkit.report` command. See `.goalkit/templates/commands/report.md` for the execution workflow.

## Summary

[Extract from goals and outcomes: key achievements, metrics summary, and insights from review]

## Reporting Context

<!--
  ACTION REQUIRED: Replace the content in this section with the reporting details
  for the goal. The structure here is presented in advisory capacity to guide
  the report generation process.
-->

**Reporting Period**: [e.g., January 2024, Q1 2024, Project Alpha or NEEDS CLARIFICATION]
**Goals Analyzed**: [e.g., 5 goals completed, 2 in progress, 1 abandoned or N/A]
**Success Metrics**: [e.g., user satisfaction, engagement, conversion or NEEDS CLARIFICATION]
**Performance Baseline**: [e.g., previous period comparison data or NEEDS CLARIFICATION]
**Reporting Structure**: [periodic/ad-hoc - determines reporting approach]
**Thresholds**: [domain-specific, e.g., 80% achievement, 50% improvement, baseline maintenance or NEEDS CLARIFICATION]

## Vision Check

*GATE: Must pass before Report 0 analysis. Re-check after Report 1 completion.*

[Gates determined based on vision alignment]

## Report Structure

### Documentation (this goal)

```markdown
.goalkit/
├── goals/
│   └── [###-goal-name]/
│       ├── report.md        # This file (/goalkit.report command output)
│       ├── analysis.md      # Report 0 output (/goalkit.report command)
│       ├── insights.md      # Report 1 output (/goalkit.report command)
│       ├── recommendations.md # Report 1 output (/goalkit.report command)
│       └── action-items.md  # Report 2 output - detailed next steps
```

### Report Components
<!--
  ACTION REQUIRED: Replace the placeholder components below with the concrete reporting
  elements for this period. Delete unused components and expand the chosen approach with
  real reporting elements. The delivered report must not include Component labels.
-->

```markdown
# [REMOVE IF UNUSED] Option 1: Periodic Status Report (DEFAULT)
- Goal Status Overview: [Status of all goals for the period]
- Success Metrics Summary: [Quantitative performance analysis]
- Key Outcomes & Impact: [Qualitative impact assessment]
- Trends & Insights: [Pattern identification and analysis]

# [REMOVE IF UNUSED] Option 2: Impact-Focused (when "value-driven" + "stakeholder-focused" detected)
- Executive Summary: [Key metrics and high-level outcomes]
- Business Impact: [Quantified business value delivered]
- User Impact: [User experience and satisfaction changes]
- ROI Analysis: [Return on investment assessment]

# [REMOVE IF UNUSED] Option 3: Learning-Focused (when "improvement-focused" detected)
- What Worked Well: [Successful approaches and strategies]
- What Did Not Work: [Areas of challenge or failure]
- Process Effectiveness: [Methodology assessment]
- Improvement Recommendations: [Future improvement suggestions]
```

**Reporting Considerations**:

- **Data Accuracy**: Ensure all metrics and figures are based on actual project data
- **Stakeholder Relevance**: Focus on information that matters to decision makers
- **Actionable Insights**: Provide insights that can guide future decisions
- **Pattern Recognition**: Look for trends across multiple goals rather than isolated incidents
- **Forward-Looking**: Include insights that inform future goal achievement

**Report Decision**: [Document the selected reporting approach and reference the real approach captured above]

## Complexity Tracking

> **Fill ONLY if Vision Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., Complex reporting structure] | [current need] | [why simple approach insufficient] |
| [e.g., Multi-metric analysis] | [specific problem] | [why single-metric approach insufficient] |