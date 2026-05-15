---
description: Align a goal to organization vision and strategic pillars. Creates or updates goal alignment document.
handoffs:
  - label: Set OKR Mapping
    agent: goalkit.okr-mapping
    prompt: Map this goal to quarterly OKRs
    send: true
  - label: Explore Strategies
    agent: goalkit.strategies
    prompt: Explore strategy options for this goal
    send: true
scripts:
  sh: scripts/bash/create-goal-alignment.sh --json "{GOAL_ID}"
  ps: scripts/powershell/create-goal-alignment.ps1 -Json "{GOAL_ID}"
---

## User Input

```text
$ARGUMENTS
```

Goal to align: **$ARGUMENTS**

You **MUST** use this goal ID/reference before proceeding.

## Outline

The text the user provided is the goal ID or name. Do NOT ask them to repeat it.

Given that goal reference, do this:

1. **Locate the goal**:
   - If ARGUMENTS contains goal ID (e.g., "003" or "#003"): Load `.goalkit/goals/003/goal.md`
   - If ARGUMENTS contains goal name: Search `.goalkit/goals/*/goal.md` for matching goal
   - If not found: ERROR "Goal not found. Please provide goal ID or verify goal exists"

2. Run `{SCRIPT}` from repo root to initialize alignment file. Pass goal ID via script.

3. Load both:
   - `templates/goal-alignment-template.md` (to understand structure)
   - `org-vision-template.md` or existing `.goalkit/org-vision.md` (to understand organization's vision)

4. Follow this execution flow:

   1. Parse the goal from goal.md file
      Extract: goal name, success criteria, strategic value
   2. Load organization vision (if exists)
      If org vision doesn't exist: WARN "Organization vision not created yet. Run `/goalkit.org-vision` first for better alignment."
   3. Map goal to strategic pillar
      Which of org's 3-5 strategic pillars does this goal advance?
      Create explicit connection statement
   4. Identify supported 3-year objectives
      Which 3-year objectives does this goal help achieve?
      Document how (what dimension of the objective)
   5. Assess values alignment
      For each core value, check if goal approach demonstrates it
      Highlight any value misalignments with mitigation strategy
   6. Check principles adherence
      Does goal follow org's guiding principles?
      Document any exceptions with justification
   7. Complete business impact assessment
      Revenue, cost, risk, capability, stakeholder impact
   8. Map dependencies
      What other goals must succeed for this goal to succeed?
      Are dependent goals identified and scheduled?
   9. Assess metrics alignment
      Do goal success criteria feed org-level metrics?
      Create explicit linkage where relevant
   10. Run alignment checklist
       Validate all alignment items complete
   11. Gather stakeholder alignment (document who agreed)
   12. Return: SUCCESS (goal alignment complete and ready for OKR mapping or strategy exploration)

5. **Validate Alignment Check gate**:
   - Confirm goal maps to at least one strategic pillar (not scattered)
   - Verify goal advances identified 3-year objectives
   - Check values/principles alignment (or documented exceptions)
   - Confirm business case articulated
   - Verify stakeholders aligned (documented)
   - ERROR if goal fails alignment check

6. Write the alignment document to GOAL_ALIGNMENT_FILE using the template structure, preserving section order.

7. Report completion with:
   - Goal ID and name
   - Primary strategic pillar
   - Supported 3-year objectives
   - Alignment checklist results
   - Readiness for next phase (`/goalkit.okr-mapping` if OKR quarter, or `/goalkit.strategies`)

**NOTE:** The script creates the alignment file before writing.

## General Guidelines

- **Alignment is not optional** - every goal must connect to organizational strategy
- **Explicit over implicit** - write out connections clearly, don't assume reader knows
- **Honesty about exceptions** - if goal doesn't align, document why and whether it's justified
- **Stakeholder buy-in** - alignment document should show who approved this goal

### Section Requirements

- **Mandatory**: Strategic Pillar, 3-Year Objectives, Values Alignment, Business Impact, Stakeholder Alignment, Checklist
- **Optional**: Misalignment Notes (only if applicable), Dependencies
- If section not applicable, still document why (don't leave blank)

### For AI Generation

When aligning a goal:

1. **Read the goal completely** - understand success criteria, scope, team
2. **Reference org vision** - read org-vision.md thoroughly
3. **Make explicit connections** - avoid vague linkages
4. **Call out misalignments** - if goal doesn't fit pillar well, say so and suggest fix
5. **Document assumptions** - if org vision missing, note what we assumed

### Validation Gates

Alignment Check must pass:

- [ ] Goal maps to one of org's strategic pillars (primary + optional secondary)
- [ ] Connection to pillar is explicit and justified
- [ ] At least one 3-year objective explicitly supported
- [ ] Values alignment assessed for all core values
- [ ] Principles adherence documented (exception mitigations if needed)
- [ ] Business case articulated (revenue/cost/risk/capability)
- [ ] Key stakeholders documented as aligned
- [ ] All checklist items completed
- [ ] No [NEEDS CLARIFICATION] markers remain

If alignment check fails, report ERROR and specific issues.
