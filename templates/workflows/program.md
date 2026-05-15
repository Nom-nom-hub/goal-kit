---
description: Create or manage a program - a group of 2-5 related goals working toward a shared outcome.
handoffs:
  - label: Create Goals in Program
    agent: goalkit.goal-alignment
    prompt: Create a goal aligned to this program
    send: false
  - label: View Program Status
    agent: goalkit.portfolio
    prompt: Show this program in portfolio view
    send: false
scripts:
  sh: scripts/bash/create-program.sh --json "{PROGRAM_NAME}"
  ps: scripts/powershell/create-program.ps1 -Json "{PROGRAM_NAME}"
---

## User Input

```text
$ARGUMENTS
```

Program name/description: **$ARGUMENTS**

You **MUST** use this program specification before proceeding.

## Outline

The text the user typed after `/goalkit.program` is the program name or description. Use it directly.

Given that program specification, do this:

1. Run `{SCRIPT}` from repo root to initialize program file. Pass program name via script.

2. Load `templates/program-template.md` to understand structure.

3. Follow this execution flow:

   1. Parse program specification from ARGUMENTS
      If empty: ERROR "No program name or description provided"
   2. Clarify program scope
      Is this a new program to plan? Or update to existing program?
      NEW: Create program vision and structure
      UPDATE: Load existing program file and validate changes
   3. Define program vision
      Why does this program exist? What shared outcome?
      2-3 sentence vision statement
   4. Assess if program-worthy
      Will this be 2-5 related goals? (YES = program; NO = single goal)
      Is there meaningful coordination needed? (YES = program; NO = independent goals)
      Will timeline be 6+ weeks? (YES = program; NO = milestone or single goal)
      If NO on all: WARN "This might be better as a single goal, not a program"
   5. Define strategic context
      Which strategic pillar(s) does this serve?
      Business impact? Capability building?
   6. Decompose into goals
      Identify 2-5 key goals that will execute program
      Map dependencies (what blocks what?)
      Sequence execution (order of goal starts)
   7. Document goal details
      For each goal in program:
      - Goal name and owner
      - Timeline (start/end dates)
      - Success criteria
      - Dependency/sequencing rationale
   8. Create timeline visualization
      ASCII diagram showing goal sequence + dependencies
      Highlight critical path
   9. Plan resource allocation
      Which teams? How many people? Duration?
      Budget if applicable
   10. Define program governance
        Who's the exec sponsor? Program manager?
        Decision authority for scope/timeline/resources?
        Review cadence (weekly syncs, monthly steering)?
   11. Establish success criteria
        Functional: What gets built?
        Business: Revenue/cost/market impact?
        Quality: Uptime/reliability targets?
        Team: Skills/morale/retention?
   12. Plan launch/transition
        When does program launch?
        How does work transition to steady state?
   13. Return: SUCCESS (program structure complete)

4. **Validate Program Check gate**:
   - Confirm program is 2-5 related goals (not more)
   - Verify goals have documented dependencies
   - Confirm timeline is 6+ weeks (worth program overhead)
   - Verify exec sponsor identified
   - Confirm governance structure defined
   - Verify success criteria defined (not just goal-level)
   - ERROR if program structure invalid

5. Write the program document to PROGRAM_FILE using the template structure.

6. Report completion with:
   - Program name and vision
   - # of goals in program
   - Timeline (start to complete)
   - Critical path
   - Governance structure
   - Next step (create goals within program)

**NOTE:** The script creates the program file before writing.

## General Guidelines

- **Program = coordination overhead** - only use if coordination truly needed
- **2-5 goals** - more = too complex; fewer = single goal
- **6+ weeks** - longer timelines justify program structure
- **Shared outcome** - goals should serve program vision, not just happen together
- **Explicit dependencies** - map what blocks what clearly

### Section Requirements

- **Mandatory**: Vision, Goals (2-5), Timeline, Governance, Success Criteria, Resource Allocation
- **Optional**: Learnings & Retrospective (fill after program completes), Completion & Closure
- Do not skip mandatory sections

### For AI Generation

When creating a program:

1. **Validate scope** - is this really 2-5 goals or just 1 big goal?
2. **Map dependencies** - be explicit about sequencing
3. **Name stakeholders** - who's sponsor? Who's program manager?
4. **Define success explicitly** - not just "all goals succeed" but program-level outcomes
5. **Plan governance** - who decides what? How often do they meet?

### Program vs. Goal Decision Tree

```
Is this one clear outcome?
  YES → Single Goal (use /goalkit.goal)
  NO → Is this 2-5 related goals?
    NO → Multiple independent goals (use /goalkit.portfolio)
    YES → Is timeline 6+ weeks?
      NO → Milestone cluster (use single goal with milestones)
      YES → Is coordination across teams needed?
        NO → Just sequential goals (use /goalkit.portfolio view)
        YES → PROGRAM (use /goalkit.program)
```

### Validation Gates

Program Check must pass:

- [ ] Program has clear, inspiring vision statement
- [ ] 2-5 goals identified (not more, not fewer)
- [ ] Each goal has documented owner and timeline
- [ ] Dependencies explicitly mapped (sequencing visible)
- [ ] Critical path identified
- [ ] Exec sponsor identified and committed
- [ ] Program manager identified
- [ ] Governance structure defined (decision authority, review cadence)
- [ ] Success criteria defined at program level (not just goal-level)
- [ ] Resource allocation visible (teams, allocation %, duration)
- [ ] Budget estimated (if applicable)
- [ ] Launch plan documented
- [ ] Transition to steady-state plan documented

If program check fails, report ERROR and specific issues.
