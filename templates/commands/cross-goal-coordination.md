---
description: Coordinate work between goals with explicit dependencies. Maps goal relationships, sequencing, and handoff points.
handoffs:
  - label: Async Coordination
    agent: goalkit.async-coordination
    prompt: Set up async communication for this goal
    send: false
  - label: View Dependencies in Portfolio
    agent: goalkit.portfolio
    prompt: Show all goals with dependency graph
    send: false
scripts:
  sh: scripts/bash/setup-cross-goal-coordination.sh --json "{GOAL_ID}"
  ps: scripts/powershell/setup-cross-goal-coordination.ps1 -Json "{GOAL_ID}"
---

## User Input

```text
$ARGUMENTS
```

Goal to coordinate with others: **$ARGUMENTS**

You **MUST** use this goal reference before proceeding.

## Outline

The text the user provided is the goal ID. Do NOT ask them to repeat it.

Given that goal reference, do this:

1. **Locate the goal**:
   - If ARGUMENTS contains goal ID (e.g., "003"): Load `.goalkit/goals/003/goal.md` and `.goalkit/goals/003/execution.md`
   - If not found: ERROR "Goal not found"

2. Run `{SCRIPT}` from repo root to initialize cross-goal coordination file. Pass goal ID via script.

3. Load required documents:
   - `templates/cross-goal-coordination-template.md` (structure)
   - The goal file (to understand outcomes)
   - The execution file (to understand timeline and teams)
   - All other `.goalkit/goals/*/execution.md` files (to understand all goals in portfolio)

4. Follow this execution flow:

   1. Parse goal from goal.md
      Extract: Goal name, success criteria, timeline, team
   2. Scan all other goals
      Which goals exist? What are their timelines and owners?
   3. Identify dependencies
      What does THIS goal depend on? (blocking goals)
      What goals depend on THIS goal? (unblocking goals)
      Dependency type: Data? API contract? Approval? Resource? Scheduling?
   4. Map sequencing
      If this goal is blocked: When can it start? What unblocks it?
      If this goal unblocks others: When do they start after completion?
      Are there parallel opportunities?
   5. Define critical path
      If this goal slips 1 week, what's the impact?
      Which dependent goals would be affected?
   6. Plan handoff points
      When does ownership transfer between teams/goals?
      What gets handed off? (Code? Design? Data model? API contract?)
      How is handoff validated? (acceptance criteria)
   7. Document coordination gates
      What must be complete before dependent goal starts?
      Who signs off on handoff?
      What happens if handoff fails?
   8. Create synchronization plan
      Do dependent goals need to sync with this one during execution?
      At what milestones?
      Sync format (async update or real-time sync)?
   9. Identify risk cascades
      If this goal at-risk, which others are impacted?
      What's the mitigation? (parallel path? contingency goal?)
   10. Plan contingency
        If this goal slips: How do we unblock dependent goals?
        Can dependent work proceed independently?
        What's the fallback strategy?
   11. Return: SUCCESS (cross-goal coordination plan complete)

5. **Validate Cross-Goal Coordination Check gate**:
   - Confirm all blocking goals identified
   - Verify all unblocking goals identified
   - Confirm critical path clear
   - Verify handoff points documented with acceptance criteria
   - Verify dependent goal owners are aware and aligned
   - Confirm contingency plan for slippage
   - ERROR if coordination plan incomplete or dependent goals not aware

6. Write the cross-goal coordination document using template structure.

7. Report completion with:
   - Goal ID and name
   - Blocking goals (# and names)
   - Unblocking goals (# and names)
   - Critical path impact
   - Key handoff points and dates
   - Readiness for cross-team sync

**NOTE:** The script creates the coordination file before writing.

## General Guidelines

- **Explicit dependencies**: Don't assume others know they're blocked/unblocked
- **Owner alignment**: Dependent goal owners must agree on handoff plan
- **Contingency planning**: Never assume perfect execution
- **Early warning**: If dependency at-risk, escalate immediately to dependent goals
- **Clear handoffs**: Know exactly what's being handed off and when

### Section Requirements

- **Mandatory**: Goal Summary, Blocking Goals, Unblocking Goals, Critical Path, Handoff Protocol, Synchronization Plan, Risk Cascades, Contingency Plan, Owner Alignment
- **Optional**: None for cross-goal coordination (all important)

### For AI Generation

When coordinating across goals:

1. **Scan full portfolio** - don't miss dependencies
2. **Be explicit** - spell out who depends on whom
3. **Include owner** - dependent goal owners must agree
4. **Plan handoffs** - what, when, acceptance criteria
5. **Anticipate slippage** - what if this goal slips 1-2 weeks?

### Validation Gates

Cross-Goal Coordination Check must pass:

- [ ] All blocking goals identified (goals this depends on)
- [ ] All unblocking goals identified (goals that depend on this)
- [ ] Blocking goals listed with specific dependency (data? API? approval?)
- [ ] Unblocking goals listed with specific impact
- [ ] Critical path calculated (impact if this goal slips 1-2 weeks)
- [ ] Handoff point dates explicit (not "sometime in week 6")
- [ ] Handoff acceptance criteria defined (how is it "done"?)
- [ ] Dependent goal owners explicitly aligned (they know the plan)
- [ ] Synchronization points planned (do teams sync? when? how?)
- [ ] Risk cascade identified (what fails if this fails?)
- [ ] Contingency plan documented (fallback if dependency slips)
- [ ] Escalation path clear (who to notify if at-risk?)

If coordination check fails, report ERROR and specific issues.

### Key Questions

**For blocking goals**: "We can't start until Goal X delivers [specific deliverable] by [date]. If Goal X slips, we slip 1 week."

**For unblocking goals**: "Goal Y waits for us to deliver [specific deliverable] by [date]. When we complete it on [date], Goal Y can start immediately on [date]."

**For contingency**: "If we slip 2 weeks, Goal Y can proceed with [fallback approach] that allows them to start 1 week later than planned."
