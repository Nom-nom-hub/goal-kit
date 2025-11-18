---
description: Conduct project review and retrospective to capture learnings and improve future goal achievement.
handoffs:
  - label: Create Improvement Goals
    agent: goalkit.goal
    prompt: Create goals based on review findings to improve future performance. I want to address...
scripts:
  sh: scripts/bash/run-review.sh --json "{ARGS}"
  ps: scripts/powershell/run-review.ps1 -Json "{ARGS}"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

The text the user typed after `/goalkit.review` in the triggering message **is** the review context. This could specify which goal, sprint, or time period to review.

Given that review context, do this:

1. **Determine review scope**:
   - If a specific goal is mentioned, focus on that goal's lifecycle
   - If a time period is specified, gather all goals from that period
   - If no specific scope provided, default to most recent goal

2. **Gather relevant information**:
   - Collect goal definition, strategies considered, milestones, and outcomes
   - Gather metrics and validation data
   - Collect any retrospective notes from the goal's execution

3. **Run the review script** `{SCRIPT}` to set up the review structure:
   - Bash example: `{SCRIPT} --json --scope "recent" "Review of recent goal"`
   - PowerShell example: `{SCRIPT} -Json -Scope "recent" "Review of recent goal"`

4. Load `templates/review-template.md` to understand required sections.

5. **Conduct review analysis using the template structure**:

    a. Review what was planned vs. what was achieved
    b. Identify what went well and what didn't go well
    c. Analyze why certain outcomes were or weren't achieved
    d. Extract key learnings and insights
    e. Document recommendations for future goals

6. Write the review to REVIEW_FILE using the template structure, replacing placeholders with concrete details derived from the gathered information while preserving section order and headings.

7. **Create action items** from the review findings:
   - Identify 1-3 specific improvement goals that emerge from the review
   - Note these in the "Next Steps" section

8. Report the review summary and suggest next steps, including creating improvement goals with `/goalkit.goal`.

## Review Focus Areas

When conducting the review, consider these areas:

### Goal Definition
- Was the goal clearly defined with measurable outcomes?
- Were the success metrics appropriate and meaningful?
- Did the goal align with overall project vision?

### Strategy Exploration
- Were enough strategy options considered?
- Were the evaluation criteria appropriate?
- Did we select the best approach based on available information?

### Execution
- Were milestones realistic and measurable?
- Did the execution plan adapt to changing information?
- Were appropriate metrics tracked during execution?

### Outcomes
- Did we achieve the planned outcomes?
- Were there unexpected benefits or drawbacks?
- What did we learn about user needs or business impact?

## General Guidelines

### For AI Generation

When conducting this review:

1. **Focus on learning**: The purpose is to extract insights for future improvement, not to assign blame.
2. **Be specific**: Use concrete data and examples rather than generalizations.
3. **Balance perspectives**: Include both positive and negative findings.
4. **Connect to outcomes**: Link findings back to the original goal outcomes to understand impact.
5. **Actionable insights**: Ensure that every significant finding has a corresponding recommendation.

### Review Quality Requirements

Reviews must:

1. **Be evidence-based**: Ground findings in observed data, not assumptions
2. **Address multiple dimensions**: Cover goal definition, strategy, execution, and outcomes
3. **Include actionable recommendations**: Every major finding should have a corresponding suggestion for improvement
4. **Be forward-looking**: Focus on how to improve future goal achievement

## Quick Guidelines

- Focus on **WHAT** was learned and **HOW** to improve.
- Connect findings back to measurable outcomes.
- Identify specific, actionable improvements.
- Document both successes and failures equally.