---
description: Define team roles and responsibilities for goal execution. Creates RACI matrix and role clarity.
handoffs:
  - label: Async Coordination
    agent: goalkit.async-coordination
    prompt: Set up async communication with these roles defined
    send: false
  - label: View Goal Status
    agent: goalkit.goal
    prompt: View goal with role assignments
    send: false
scripts:
  sh: scripts/bash/setup-team-roles.sh --json "{GOAL_ID}"
  ps: scripts/powershell/setup-team-roles.ps1 -Json "{GOAL_ID}"
---

## User Input

```text
$ARGUMENTS
```

Goal with team roles: **$ARGUMENTS**

You **MUST** use this goal reference before proceeding.

## Outline

The text the user provided is the goal ID. Do NOT ask them to repeat it.

Given that goal reference, do this:

1. **Locate the goal**:
   - If ARGUMENTS contains goal ID (e.g., "003"): Load `.goalkit/goals/003/execution.md`
   - If not found: ERROR "Goal not found. Run `/goalkit.execute` first"

2. Run `{SCRIPT}` from repo root to initialize team roles file. Pass goal ID via script.

3. Load required documents:
   - `templates/team-roles-template.md` (structure)
   - The execution.md file (to understand teams and phases)
   - The milestones.md file (to understand sequencing)

4. Follow this execution flow:

   1. Parse execution plan from execution.md
      Extract: Team structure, phases, timeline
   2. Identify all roles needed
      Goal owner? Technical lead? Product owner?
      QA owner? DevOps owner? Communication owner? Data owner?
   3. For each role, define:
      - Responsibility (what does this role own?)
      - Authority (what decisions can they make?)
      - Escalation (what escalates up?)
      - Accountability (how are they measured?)
   4. Create RACI matrix
      Rows: Each milestone or major decision
      Cols: Each role
      Cell: R (responsible/does), A (accountable/approves), C (consulted), I (informed)
   5. Define role interactions
      Which roles must coordinate?
      How do they communicate?
      What's the handoff between roles?
   6. Identify role conflicts
      Are there competing interests between roles?
      How are conflicts resolved?
   7. Plan role transitions
      As phases change, do role responsibilities shift?
      How do we hand off between phases?
   8. Define role success metrics
      How do we know each role is performing well?
      What does "done" look like for each role?
   9. Plan handoff protocol
      When ownership transfers between roles
      What gets handed off
      Acceptance criteria
   10. Identify critical path roles
        Which roles are on critical path?
        Which roles can be bottlenecks?
        Mitigation strategies?
   11. Return: SUCCESS (team roles plan complete)

5. **Validate Team Roles Check gate**:
   - Confirm goal owner identified and committed
   - Verify all critical roles assigned (at least technical lead, product, QA)
   - Confirm RACI matrix complete (all milestones x all roles)
   - Verify role responsibilities clear and distinct (no gaps, no overlaps)
   - Confirm role authority matches responsibility
   - Verify escalation path clear
   - Confirm all roles understand their success metrics
   - ERROR if team roles incomplete or ambiguous

6. Write the team roles document using template structure.

7. Report completion with:
   - Goal ID and name
   - Primary goal owner
   - # of critical roles
   - RACI matrix summary
   - Key handoff points
   - Readiness for execution with clear roles

**NOTE:** The script creates the team roles file before writing.

## General Guidelines

- **Clarity over perfection**: Better to have role assigned than have ambiguity
- **Accountability matters**: Each milestone should have clear owner
- **Escalation defined**: Know who decides when roles disagree
- **Handoff explicit**: Know when roles transition
- **Communication clear**: Roles understand each other's success criteria

### Section Requirements

- **Mandatory**: Goal Summary, Role Definitions (Goal Owner minimum), RACI Matrix, Role Interactions, Handoff Protocol, Escalation Path
- **Optional**: Role Conflicts, Role Transitions (if applicable)

### For AI Generation

When defining team roles:

1. **Understand execution** - read execution plan fully
2. **Identify natural roles** - who naturally owns what?
3. **Avoid vagueness** - spell out authority and responsibility
4. **Plan transitions** - how do phases change roles?
5. **Make RACI clear** - matrix should be obvious, not debated

### Validation Gates

Team Roles Check must pass:

- [ ] Goal owner explicitly named and committed
- [ ] Technical lead identified
- [ ] Product owner identified
- [ ] QA owner identified
- [ ] All roles have clear responsibilities (not vague)
- [ ] All roles have clear authority (what can they decide?)
- [ ] RACI matrix complete (all milestones x roles, no blanks)
- [ ] Each milestone has exactly one "A" (accountable)
- [ ] Role interactions documented (who talks to whom?)
- [ ] Handoff points explicit (when role changes)
- [ ] Handoff acceptance criteria defined
- [ ] Escalation path defined (who decides if roles disagree?)
- [ ] Success metrics per role defined
- [ ] All roles signed off (understand their role)

If team roles check fails, report ERROR and specific issues.

### RACI Guidelines

**R (Responsible)**: Does the work
**A (Accountable)**: Makes final decision / approves
**C (Consulted)**: Provides input (before decision)
**I (Informed)**: Notified after decision

**Rules**:
- Each task must have at least one "R"
- Each task must have exactly one "A"
- "A" usually same as "R" or their manager
- Avoid too many "C" (wastes time)
- "I" should be minimal (keep people informed, not involved)

**Example**:
| Milestone | Goal Owner | Tech Lead | Product | QA | DevOps |
|-----------|-----------|-----------|---------|-----|--------|
| M1: API Design | A | R/C | C | I | I |
| M1: Infrastructure | A/I | R | I | I | R |
| M2: Client Integration | A/C | R | R | I | I |
| M3: Testing | A/I | C | C | R | C |
