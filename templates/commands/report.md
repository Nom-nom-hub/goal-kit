---
description: Generate progress and insight reports from project goals and outcomes.
handoffs:
  - label: Deep Dive on Findings
    agent: goalkit.analyze
    prompt: Analyze specific findings from the report. I want to understand...
scripts:
  sh: scripts/bash/create-report.sh --json "{ARGS}"
  ps: scripts/powershell/create-report.ps1 -Json "{ARGS}"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

The text the user typed after `/goalkit.report` in the triggering message **is** the report specification. This could specify what type of report, time period, or specific metrics to focus on.

Given that report specification, do this:

1. **Determine report scope**:
   - If a specific time period is mentioned, focus on goals from that period
   - If specific metrics are requested, focus the report on those measurements
   - If no specific scope provided, default to overall project status

2. **Gather relevant information**:
   - Collect all goals from the specified time period
   - Gather success metrics and outcomes from completed goals
   - Collect any current progress metrics from in-progress goals
   - Compile learnings from any completed reviews/retrospectives

3. **Run the report script** `{SCRIPT}` to generate the report structure:
   - Bash example: `{SCRIPT} --json --period "last-month" "Monthly progress report"`
   - PowerShell example: `{SCRIPT} -Json -Period "last-month" "Monthly progress report"`

4. Load `templates/report-template.md` to understand required sections.

5. **Generate report content using the template structure**:

    a. Calculate overall goal achievement rates
    b. Identify trends in success metrics
    c. Highlight significant outcomes and impacts
    d. Summarize key learnings from all goals in the period
    e. Provide insights and recommendations based on patterns

6. Write the report to REPORT_FILE using the template structure, replacing placeholders with concrete details derived from the gathered data while preserving section order and headings.

7. **Identify key insights** from the pattern of goals and outcomes:
   - Are there common success factors across goals?
   - Are there recurring challenges or roadblocks?
   - Are certain types of goals more likely to succeed?

8. Report the findings and suggest next steps based on the insights.

## Report Focus Areas

When generating the report, analyze these areas:

### Goal Achievement
- Percentage of goals completed vs. in-progress vs. abandoned
- Average time to complete goals
- Success rate by goal category/type

### Metric Performance
- Overall achievement rate of success metrics
- Which types of metrics are most commonly achieved
- Trends in metric performance over time

### Outcome Impact
- Aggregate business/user value delivered
- Quality of outcomes relative to expectations
- Unintended consequences (positive or negative)

### Process Effectiveness
- How well did the goal-driven methodology work?
- Which phases were most valuable?
- Where did most improvements come from?

## General Guidelines

### For AI Generation

When creating this report:

1. **Use data-driven insights**: Base conclusions on actual metrics and outcomes, not just anecdotes.
2. **Provide context**: Help readers understand not just what happened but why it might have happened.
3. **Focus on trends**: Look for patterns across multiple goals rather than just isolated incidents.
4. **Make it actionable**: Ensure stakeholders can use the report to make decisions.
5. **Balance detail with clarity**: Provide enough detail to be informative but not so much as to be overwhelming.

### Report Quality Requirements

Reports must:

1. **Be accurate**: All metrics and figures must be based on actual project data
2. **Be timely**: Include the most recent data available for the period
3. **Be comprehensive**: Cover all significant goals from the specified period
4. **Be actionable**: Include insights that can guide future decisions

## Quick Guidelines

- Focus on **WHAT** happened and **WHAT** can be learned.
- Use specific metrics and figures where possible.
- Identify trends and patterns across multiple goals.
- Provide clear insights for leadership and teams.