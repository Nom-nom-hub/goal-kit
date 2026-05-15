---
description: Set up async-first collaboration for goal execution. Defines communication patterns, decision processes, and learning capture.
handoffs:
  - label: Setup Cross-Goal Coordination
    agent: goalkit.cross-goal-coordination
    prompt: Set up coordination between this goal and dependent goals
    send: false
  - label: Execute Implementation
    agent: goalkit.execute
    prompt: Execute implementation with async-first practices
    send: true
scripts:
  sh: scripts/bash/setup-async-coordination.sh --json "{GOAL_ID}"
  ps: scripts/powershell/setup-async-coordination.ps1 -Json "{GOAL_ID}"
---

## User Input

```text
$ARGUMENTS
```

Goal to set up async coordination: **$ARGUMENTS**

You **MUST** use this goal reference before proceeding.

## Outline

The text the user provided is the goal ID. Do NOT ask them to repeat it.

Given that goal reference, do this:

1. **Locate the goal**:
   - If ARGUMENTS contains goal ID (e.g., "003"): Load `.goalkit/goals/003/execution.md`
   - If not found: ERROR "Goal execution plan not found. Run `/goalkit.execute` first"

2. Run `{SCRIPT}` from repo root to initialize async coordination file. Pass goal ID via script.

3. Load both:
   - `templates/async-coordination-template.md` (structure)
   - The execution.md file (to understand teams, phases, timeline)
   - The milestones.md file (to understand handoff points)

4. Follow this execution flow:

   1. Parse execution plan from execution.md
      Extract: Team structure, timeline, phases, communication plan
   2. Load milestones
      Identify: Handoff points, validation gates, team transitions
   3. Define async communication rituals
      Daily async standup format
      Weekly async updates
      Async decision process
      Learning share cadence
   4. Design daily standup structure
      What should be reported each day?
      Who reports? To where (Slack, doc, etc.)?
      Cadence and format
   5. Design weekly async updates
      Summary of progress
      Blockers and needs
      Confidence in timeline
   6. Define async decision framework
      How are decisions made without sync meetings?
      What decisions need escalation?
      Timeline for decisions
   7. Plan milestone handoff protocol
      When handoff happens (specific date/condition)
      Who hands off to whom
      What gets transferred (docs, context, code)
      Acceptance criteria for handoff
   8. Define learning capture ritual
      How do we capture insights during execution?
      When do we share learnings?
      Format for documenting
   9. Identify sync points (exceptions)
      What sync work truly needs real-time discussion?
      When do sync discussions happen?
      Duration and attendees
   10. Create escalation path
        When do decisions escalate?
        Who has final authority?
        Timeline for escalation resolution
   11. Return: SUCCESS (async coordination plan complete)

5. **Validate Async Coordination Check gate**:
   - Confirm daily standup structure defined
   - Verify weekly async updates planned
   - Confirm milestone handoff protocols documented
   - Verify decision process clear (escalation path defined)
   - Confirm learning capture ritual defined
   - Verify team knows sync meeting needs are minimal
   - ERROR if coordination plan incomplete

6. Write the async coordination document using template structure.

7. Report completion with:
   - Goal ID and name
   - Daily standup format
   - Weekly update cadence
   - Milestone handoff dates
   - Decision escalation path
   - Readiness for execution

**NOTE:** The script creates the coordination file before writing.

## General Guidelines

- **Async-first principle**: Default to async, use sync only for decisions that truly need real-time
- **Clarity over meetings**: Better written decisions than lengthy discussions
- **Explicit handoffs**: Know exactly when ownership changes and what gets transferred
- **Learning embedded**: Capture insights as work happens, not just at end
- **Time zones respected**: Async work respects distributed teams

### Section Requirements

- **Mandatory**: Daily Standup, Weekly Updates, Milestone Handoffs, Decision Process, Learning Capture, Sync Exceptions, Escalation Path
- **Optional**: None for async coordination (all important)

### For AI Generation

When setting up async coordination:

1. **Understand team structure** - who reports to whom?
2. **Map timeline** - when are handoffs? When are decisions needed?
3. **Identify risks** - where might async fail? What needs sync?
4. **Design clarity** - make standup/update format crystal clear
5. **Embed learning** - make it easy to capture insights

### Validation Gates

Async Coordination Check must pass:

- [ ] Daily standup format documented (what, when, where, who)
- [ ] Weekly async update format defined
- [ ] Milestone handoff points identified with dates
- [ ] Who hands off to whom is explicit
- [ ] Handoff acceptance criteria defined
- [ ] Decision process documented (who decides? when?)
- [ ] Escalation path clear (when escalate? to whom?)
- [ ] Learning capture ritual defined
- [ ] Sync meeting needs explicitly identified (not just "if needed")
- [ ] Sync attendees and duration defined
- [ ] Communication channels chosen (Slack, doc, email, etc.)
- [ ] Time zone considerations addressed

If coordination check fails, report ERROR and specific issues.
