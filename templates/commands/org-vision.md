---
description: Establish organization vision, values, strategic pillars, and 3-year objectives. Foundation for all goal alignment.
handoffs:
  - label: Set Quarterly OKRs
    agent: goalkit.okrs
    prompt: Set quarterly OKRs aligned with this organization vision
    send: true
  - label: Create Aligned Goal
    agent: goalkit.goal-alignment
    prompt: Create a goal aligned to this organization vision
    send: true
scripts:
  sh: scripts/bash/create-org-vision.sh --json
  ps: scripts/powershell/create-org-vision.ps1 -Json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

The text the user typed after `/goalkit.org-vision` **is** the organization description/context. Assume you always have it available even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that organization description, do this:

1. Run `{SCRIPT}` from repo root and parse JSON for ORG_VISION_FILE. For single quotes in args like "We're Groot", use escape syntax: e.g 'We'\''re Groot' (or double-quote if possible: "We're Groot").

2. Load `templates/org-vision-template.md` to understand required sections.

3. Follow this execution flow:

   1. Parse organization description from Input
      If empty: ERROR "No organization description provided"
   2. Extract key concepts from description
      Identify: core mission, values, strategic focus areas, business drivers
   3. For unclear aspects:
      - Make informed guesses based on industry standards and context
      - Only mark with [NEEDS CLARIFICATION: specific question] if:
        - The choice significantly impacts strategic direction or focus areas
        - Multiple reasonable interpretations exist with different implications
        - No reasonable default exists
      - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
      - Prioritize clarifications by impact: mission > pillars > metrics
   4. Fill Mission Statement section
      If no clear mission: ERROR "Cannot determine organization mission"
   5. Generate Core Values
      Define 4-5 values with behavioral indicators
      Each value must be actionable and observable in how team operates
   6. Define Strategic Pillars
      3-5 areas where organization invests long-term
      Include vision for each pillar + why it matters
   7. Set 3-Year Objectives
      Measurable outcomes aligned with pillars
      Include both organizational and per-pillar objectives
   8. Define Success Metrics
      Track progress toward 3-year vision
      Include metrics by pillar where relevant
   9. Establish Guiding Principles
      How the organization approaches work
      Should reflect values and culture
   10. Return: SUCCESS (org vision ready for OKR setting)

4. **Validate Vision Check gate**:
   - Ensure mission is clear and inspiring (not generic)
   - Verify 3-5 strategic pillars are distinct and meaningful
   - Confirm values have clear behavioral indicators
   - Verify objectives are measurable with specific targets
   - ERROR if vision lacks clarity or strategic direction is ambiguous

5. Write the vision to ORG_VISION_FILE using the template structure, replacing placeholders with concrete details derived from the organization description while preserving section order and headings.

6. Report completion with org vision file path and readiness for next phases (`/goalkit.okrs` or `/goalkit.goal-alignment`).

**NOTE:** The script creates the vision file before writing.

## General Guidelines

- Focus on **long-term direction** (3+ years)
- Mission should describe **why** the organization exists
- Strategic pillars should represent **areas of sustained investment**
- Values should be **actionable** and observable in team behavior
- Success metrics should be **meaningful** to business and team

### Section Requirements

- **Mandatory sections**: Mission, Values (4-5), Strategic Pillars (3-5), 3-Year Objectives, Success Metrics, Guiding Principles
- **Optional sections**: None for org vision (all are mandatory)
- Do not remove sections

### For AI Generation

When creating org vision from a user prompt:

1. **Make informed guesses**: Use context and industry standards to fill gaps
2. **Document assumptions**: Record reasonable defaults in assumptions
3. **Limit clarifications**: Maximum 3 [NEEDS CLARIFICATION] markers
4. **Prioritize clarifications**: Mission > Strategic Direction > Metrics
5. **Think like validator**: Is this vision inspiring and strategic (not tactical)?

**Examples of reasonable defaults** (don't ask about these):

- Number of strategic pillars: 3-5 is standard
- Success metrics: Industry benchmarks for the domain
- Value count: 4-5 core values (not 10+)
- 3-year timeline: Standard strategic planning horizon

### Validation Gates

Vision Check must pass before proceeding:

- [ ] Mission statement is clear, inspiring, and specific (not generic)
- [ ] Values have behavioral indicators (not just abstract concepts)
- [ ] Strategic pillars are 3-5 distinct areas
- [ ] 3-year objectives are measurable with specific targets
- [ ] Success metrics feed into strategic pillars
- [ ] Guiding principles are actionable (not vague)
- [ ] No implementation details leak into vision

If any gate fails, report ERROR and request clarifications.
