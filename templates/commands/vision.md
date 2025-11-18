---
description: Establish project vision, values, and success criteria using the vision template to provide foundation for all goal-driven development.
handoffs:
  - label: Create Goal
    agent: goalkit.goal
    prompt: Define a goal aligned with the project vision
    send: true
scripts:
  sh: scripts/bash/create-vision.sh --json
  ps: scripts/powershell/create-vision.ps1 -Json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

The text the user typed after `/goalkit.vision` in the triggering message **is** the project description. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that project description, do this:

1. Run `{SCRIPT}` from repo root and parse JSON for VISION_FILE. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. Load `templates/vision-template.md` to understand required sections.

3. Follow this execution flow:

    1. Parse user description from Input
       If empty: ERROR "No project description provided"
    2. Extract key concepts from description
       Identify: core mission, desired outcomes, success measures
    3. For unclear aspects:
       - Make informed guesses based on context and industry standards
       - Only mark with [NEEDS CLARIFICATION: specific question] if:
         - The choice significantly impacts project scope or user experience
         - Multiple reasonable interpretations exist with different implications
         - No reasonable default exists
       - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
       - Prioritize clarifications by impact: scope > user experience > technical details
    4. Fill Core Mission section
       If no clear mission: ERROR "Cannot determine project mission"
    5. Generate Vision Statement
       Each statement must be inspiring and outcome-focused
       Use reasonable defaults for unspecified details (document assumptions in Assumptions section)
    6. Define Success Criteria
       Create measurable, outcome-focused success measures
       Include both quantitative measures (percentages, timeframes, user counts) and qualitative measures (user satisfaction, business impact)
       Each criterion must be verifiable without knowing implementation details
    7. Identify Guiding Principles (if relevant)
    8. Return: SUCCESS (vision ready for goal creation)

4. Write the vision to VISION_FILE using the template structure, replacing placeholders with concrete details derived from the project description (arguments) while preserving section order and headings.

5. Report completion with vision file path and readiness for the next phase (`/goalkit.goal`).

**NOTE:** The script creates the vision file before writing.

## General Guidelines

## Quick Guidelines

- Focus on **WHAT** outcomes users/businesses need and **WHY**.
- Avoid HOW to implement (no tech stack, APIs, code structure).
- Written for business stakeholders, not developers.

### Section Requirements

- **Mandatory sections**: Must be completed for every vision
- **Optional sections**: Include only when relevant to the vision
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation

When creating this vision from a user prompt:

1. **Make informed guesses**: Use context, industry standards, and common patterns to fill gaps
2. **Document assumptions**: Record reasonable defaults in the Assumptions section
3. **Limit clarifications**: Maximum 3 [NEEDS CLARIFICATION] markers - use only for critical decisions that:
   - Significantly impact project scope or outcomes
   - Have multiple reasonable interpretations with different implications
   - Lack any reasonable default
4. **Prioritize clarifications**: scope > outcomes > implementation details
5. **Think like a validator**: Every vague vision should fail the "inspiring and outcome-focused" checklist item
6. **Common areas needing clarification** (only if no reasonable default exists):
   - Project scope and boundaries (include/exclude specific outcomes)
   - Target user groups (if multiple conflicting interpretations possible)
   - Success metrics (when critical for measuring progress)

**Examples of reasonable defaults** (don't ask about these):

- Success metrics: Industry-standard practices for the domain
- Timeline expectations: Standard project delivery times for similar scope
- Performance targets: User-friendly goals that align with business value
- Target user groups: Primary persona that benefits most from the project

### Success Criteria Guidelines

Success criteria must be:

1. **Measurable**: Include specific metrics (%, $, time, user counts)
2. **Outcome-focused**: No mention of implementation details or technical approaches
3. **Business/user-focused**: Describe results from user/business perspective, not system internals
4. **Verifiable**: Can be validated without knowing implementation details

**Good examples**:

- "Increase user engagement by 25% over 3 months"
- "Improve customer satisfaction to 90% NPS score"
- "Reduce task completion time by 50% for primary workflow"
- "Generate $50K in additional revenue within 6 months"

**Bad examples** (implementation-focused):

- "Implement React-based UI" (technology-specific)
- "Database supports 1000 TPS" (implementation detail)
- "API response time under 200ms" (too technical)
- "Deploy to AWS" (technology-specific)
