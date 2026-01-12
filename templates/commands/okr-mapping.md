---
description: Map a goal to specific quarterly OKRs. Shows how goal execution drives OKR achievement.
handoffs:
  - label: Explore Strategies
    agent: goalkit.strategies
    prompt: Explore strategy options for this goal
    send: true
  - label: View Portfolio
    agent: goalkit.portfolio
    prompt: Show portfolio with OKR support visible
    send: false
scripts:
  sh: scripts/bash/create-okr-mapping.sh --json "{GOAL_ID}"
  ps: scripts/powershell/create-okr-mapping.ps1 -Json "{GOAL_ID}"
---

## User Input

```text
$ARGUMENTS
```

Goal to map to OKRs: **$ARGUMENTS**

You **MUST** use this goal reference before proceeding.

## Outline

The text the user provided is the goal ID/name. Do NOT ask them to repeat it.

Given that goal reference, do this:

1. **Locate the goal**:
   - If ARGUMENTS contains goal ID (e.g., "003"): Load `.goalkit/goals/003/goal.md`
   - If ARGUMENTS contains goal name: Search `.goalkit/goals/*/goal.md` for match
   - If not found: ERROR "Goal not found"

2. Run `{SCRIPT}` from repo root to initialize mapping file. Pass goal ID via script.

3. Load required documents:
   - `templates/okr-mapping-template.md` (structure)
   - The goal file (`.goalkit/goals/[ID]/goal.md`)
   - Current quarter OKRs (`.goalkit/okrs.md` or equivalent)

4. Follow this execution flow:

   1. Parse goal from goal.md
      Extract: goal name, success criteria, business impact
   2. Load current quarter OKRs
      If OKRs don't exist: ERROR "Quarterly OKRs required. Run `/goalkit.okrs` first"
   3. Identify supporting KRs
      Which OKR Key Results does this goal help achieve?
      Goal typically supports 1-3 KRs (not more)
   4. Map success criteria to KRs
      How do goal success metrics prove KR achievement?
      Create explicit causal link for each mapping
   5. Calculate contribution %
      What % of KR progress does this goal represent?
      Example: "This is 1 of 5 features (20%)" or "Directly impacts KR 1.2"
   6. Assess timeline alignment
      Does goal completion before OKR measurement date?
      If goal slips past EOQ: Is that acceptable? Why?
   7. Impact analysis
      If goal succeeds: What happens to supported KRs? (probability increases)
      If goal fails: What's the risk to KRs? (blocked, harder, impossible)
   8. Document dependencies
      What other goals must succeed for this goal to drive the KRs?
      What goals does this goal unblock?
   9. Confidence assessment
      How confident are we that goal execution will achieve the KRs?
      Scale 1-5 where 5 = certain
   10. Identify risks to OKR contribution
       What could prevent this goal from driving OKRs?
       Mitigation strategies?
   11. Plan OKR check-in integration
       At mid-quarter review: Will this goal's progress be visible?
       At EOQ: How will we measure impact on KRs?
   12. Return: SUCCESS (OKR mapping complete and goal ready for strategy)

5. **Validate OKR Mapping Check gate**:
   - Confirm goal maps to 1-3 OKR KRs (not scattered)
   - Verify causal link between goal success criteria and KR proof
   - Confirm contribution % realistic (not over-claiming)
   - Verify timeline allows OKR measurement of goal impact
   - Verify risks identified and mitigations planned
   - ERROR if mapping check fails

6. Write the mapping document to OKR_MAPPING_FILE using the template structure.

7. Report completion with:
   - Goal ID and name
   - Mapped KRs (with contribution %)
   - Confidence level
   - Key risks + mitigations
   - Readiness for strategy exploration

**NOTE:** The script creates the mapping file before writing.

## General Guidelines

- **Explicit connections** - show how goal metrics prove KR achievement
- **Realistic contribution** - goal is 1 of N, not 100% of KR
- **Transparent about risks** - what could break this connection?
- **Timeline matters** - goal completion after OKR measurement = no credit

### Section Requirements

- **Mandatory**: Mapping Summary, Goal-KR Connections, Timeline Alignment, Impact Assessment, Dependency Management, Confidence & Risk, OKR Check-In Integration
- **Optional**: None for OKR mappings (all important)

### For AI Generation

When mapping goals to OKRs:

1. **Understand both documents** - read goal.md and OKRs thoroughly
2. **Make links explicit** - don't assume reader sees the connection
3. **Be realistic about contribution** - is this really 20% of the KR or 5%?
4. **Name the risks** - what could prevent goal from achieving the KR?
5. **Plan for tracking** - how will we know if goal helped achieve KR?

### Validation Gates

OKR Mapping Check must pass:

- [ ] Goal maps to 1-3 OKR KRs (not scattered across many)
- [ ] Explicit causal link between goal success criteria and KR proof
- [ ] Contribution % is realistic (not exaggerated)
- [ ] Timeline allows goal completion before OKR measurement date
- [ ] If goal slips past EOQ: documented why acceptable and impact understood
- [ ] Risks to OKR contribution identified
- [ ] Mitigations planned for each risk
- [ ] Confidence 1-5 assessed
- [ ] OKR check-in process defined (mid-Q and EOQ)
- [ ] Dependencies on other goals documented

If mapping check fails, report ERROR and specific issues.

### No Mapping Cases

Some goals don't map to quarterly OKRs:

- **Tech debt/maintenance**: Ongoing work, not OKR-driven
- **Process improvements**: May support operations but not strategic OKRs
- **One-time fixes**: Urgent issue, not planned OKR work
- **Research/exploration**: Pre-commitment work, not OKR execution

For these, document why no OKR mapping in goal document (not missing mapping).
