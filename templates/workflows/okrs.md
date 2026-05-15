---
description: Set quarterly OKRs (Objectives + Key Results) aligned with organization vision. Foundation for goal creation.
handoffs:
  - label: Create Goal Supporting OKR
    agent: goalkit.goal
    prompt: Create a goal that supports these OKRs
    send: false
  - label: View Portfolio with OKRs
    agent: goalkit.portfolio
    prompt: Show portfolio with OKR alignment
    send: false
scripts:
  sh: scripts/bash/create-okrs.sh --json "{QUARTER}"
  ps: scripts/powershell/create-okrs.ps1 -Json "{QUARTER}"
---

## User Input

```text
$ARGUMENTS
```

Quarter for OKRs: **$ARGUMENTS** (e.g., "Q1 2025")

You **MUST** consider this quarter specification before proceeding.

## Outline

The text the user typed after `/goalkit.okrs` is the quarter (e.g., "Q1 2025", "Q2", etc.). Use it directly.

Given that quarter specification, do this:

1. Run `{SCRIPT}` from repo root to initialize OKR file. Pass quarter via script.

2. Load both:
   - `templates/okr-template.md` (to understand structure)
   - Existing `.goalkit/org-vision.md` (to understand strategic direction)
   - Previous quarter OKRs if they exist (to assess trends)

3. Follow this execution flow:

   1. Confirm quarter specification
      Parse quarter from ARGUMENTS (Q1 2025, Q2, etc.)
      If ambiguous: ERROR "Please specify quarter clearly (e.g., Q1 2025)"
   2. Load organization vision
      If org vision doesn't exist: ERROR "Organization vision required. Run `/goalkit.org-vision` first"
   3. Review previous quarter results (if applicable)
      How did we perform on last quarter's OKRs?
      What did we learn?
   4. Draft 3-5 organizational objectives
      Use strategic pillars and 3-year objectives as reference
      Each objective should be aspirational (not guaranteed)
      Each should map to a strategic pillar
   5. For each objective, define 3-4 key results
      Each KR must be measurable with specific targets
      Each KR must be achievable but ambitious (70-80% confidence)
      KRs should be distinct (not redundant)
   6. Gather business context
      What market changes? Customer feedback? Strategic shifts?
      Should any OKRs reflect these?
   7. Set confidence levels
      For each objective, assess probability of achieving all KRs
      1-5 scale where 5 = certain
   8. Plan goal support
      Identify which goals will execute to achieve these OKRs
      Document anticipated goal mapping (can be refined later)
   9. Identify dependencies and risks
      What could block OKR achievement?
      What goals block other goals?
   10. Plan quarterly reviews
        Schedule mid-quarter check-in and end-of-quarter retrospective
   11. Return: SUCCESS (OKRs ready for all-hands discussion and goal planning)

4. **Validate OKR Check gate**:
   - Confirm 3-5 objectives per quarter (not more)
   - Verify each objective has 3-4 key results
   - Confirm each KR is measurable (specific target, not vague)
   - Verify each KR is aspirational not guaranteed (70-80% confidence)
   - Confirm OKRs map to strategic pillars
   - Verify OKRs differ from last quarter (not just repeating)
   - ERROR if OKR check fails

5. Write the OKRs to OKR_FILE using the template structure, preserving section order.

6. Report completion with:
   - Quarter and dates
   - 3-5 objectives + their KRs
   - Anticipated goal count to achieve OKRs
   - Confidence level
   - Next steps (all-hands discussion, goal planning)

**NOTE:** The script creates the OKR file before writing.

## General Guidelines

- **OKRs are strategic**, not tactical - focus on outcomes not activities
- **Aspirational not guaranteed** - 70-80% confidence, not 100%
- **3-5 OKRs max** - focus beats comprehensiveness
- **Business-driven** - reflect strategic pillars and 3-year objectives
- **Measurable** - every KR must have specific, verifiable target

### Section Requirements

- **Mandatory**: Summary, Objectives (3-5), Key Results (3-4 per objective), Goals Supporting, Dependencies/Risks
- **Optional**: Previous Quarter Assessment, Mid-Quarter Review, End-of-Quarter Review (fill at those times)

### For AI Generation

When setting OKRs:

1. **Understand strategic direction** - read org vision carefully
2. **Balance pillars** - don't overweight one pillar (unless intentional)
3. **Make KRs measurable** - include specific targets, not vague language
4. **Assess confidence** - are these ambitious but achievable?
5. **Document rationale** - why these OKRs? What changed from last quarter?

### Common OKR Structures

**Growth-focused**:
- Ship N major features
- Achieve >X% adoption
- Reduce feature cycle time by X%

**Market-focused**:
- Close N enterprise customers
- Expand to N new geographies
- Achieve NPS of X

**Team-focused**:
- Hire N senior engineers
- Achieve Y eNPS (employee satisfaction)
- Develop [skill] across N people

**Reliability-focused**:
- Achieve 99.X% uptime
- Reduce incident MTTR to X minutes
- Resolve security vulnerabilities by X%

### Validation Gates

OKR Check must pass:

- [ ] 3-5 objectives (not more, not fewer)
- [ ] Each objective maps to a strategic pillar
- [ ] Each objective has 3-4 key results
- [ ] Each KR is specific and measurable (not vague)
- [ ] Each KR has explicit target (%, time, count, score)
- [ ] Confidence level 70-80% per objective (not 100%)
- [ ] OKRs differ meaningfully from previous quarter (showing progress)
- [ ] Mix of growth, efficiency, and team objectives
- [ ] Goals to achieve OKRs are identified (or will be created)

If OKR check fails, report ERROR and specific issues.
