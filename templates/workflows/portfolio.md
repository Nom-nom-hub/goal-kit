---
description: View and manage organization portfolio - all goals across teams with status, alignment, and health.
handoffs:
  - label: Create Aligned Goal
    agent: goalkit.goal-alignment
    prompt: Create a new goal aligned to strategic pillars
    send: false
  - label: Assess At-Risk Goal
    agent: goalkit.goal
    prompt: Review and update an at-risk goal
    send: false
scripts:
  sh: scripts/bash/generate-portfolio.sh --json
  ps: scripts/powershell/generate-portfolio.ps1 -Json
---

## User Input

```text
$ARGUMENTS
```

Portfolio scope: **$ARGUMENTS** (optional: "all", "strategic-pillar-name", "team-name", or empty for full portfolio)

You **MUST** consider this scope if provided.

## Outline

The text the user typed after `/goalkit.portfolio` is optional scope filter. Use it if provided, otherwise show full portfolio.

Given that scope, do this:

1. Run `{SCRIPT}` from repo root to scan all `.goalkit/goals/*/` directories and gather portfolio data.

2. Load `templates/portfolio-template.md` to understand structure.

3. Follow this execution flow:

   1. Scan all goals in `.goalkit/goals/*/`
      For each: Load goal.md, status, completion %, health score
   2. Load organization vision
      For strategic pillar grouping
   3. Load current quarter OKRs (if exist)
      For OKR support visibility
   4. Gather goal metadata
      Status: On track / At risk / Completed / Not started
      Owner, team, strategic pillar, OKRs supported, health score
   5. Calculate portfolio metrics
      # on track, # at risk, # completed
      Average completion %, average health score
      Velocity (goals/month)
   6. Group goals by status, then by pillar
      Create clear sections for each status
   7. Identify top risks
      Which goals are at risk? Why? What's the mitigation?
      Which risks affect multiple goals (cascade risk)?
   8. Identify resource allocation
      Which teams are over/under-allocated?
      Any team with more than 3 concurrent goals?
   9. Identify opportunities
      What could accelerate portfolio? What's blocked?
   10. Map dependencies
        What's on critical path?
        Where are potential bottlenecks?
   11. Plan leadership actions
        What decisions are needed?
        What escalations?
   12. Return: SUCCESS (portfolio view complete)

4. **Validate Portfolio Check gate**:
   - Confirm all active goals captured
   - Verify status assessments accurate
   - Confirm metrics calculated correctly
   - Verify top risks identified
   - Confirm resource allocation visible
   - Warn if > 50% of goals at risk
   - ERROR if portfolio data incomplete or stale

5. Generate the portfolio document using the template structure.

6. Report completion with:
   - Portfolio health snapshot (# on track, # at risk, # completed)
   - Key metrics (velocity, completion %, health score)
   - Top 3 risks
   - Leadership actions needed
   - Readiness for portfolio review meeting

**NOTE:** The script gathers portfolio data; this command generates the report document.

## General Guidelines

- **Portfolio is leadership view** - focus on health, alignment, risks (not task details)
- **Status matters** - be honest about at-risk goals (don't hide problems)
- **Dependencies visible** - show what blocks what
- **Actions clear** - what do leaders need to decide/do?

### Section Requirements

- **Mandatory**: Executive Summary, Portfolio Metrics, Goals by Status, Strategic Pillar Distribution, Resource Allocation, Risks & Opportunities, Dependencies, Leadership Actions
- **Optional**: Team Health (if multiple teams), Changes this Period (if tracking over time)

### For AI Generation

When generating portfolio:

1. **Scan all goals** - don't miss anyone
2. **Use current data** - status from goal files, not assumptions
3. **Be realistic** - if goal is at risk, say so clearly
4. **Surface conflicts** - are multiple goals competing for same resource?
5. **Identify cascades** - if Goal 1 at risk, what's impact on Goal 2 & 3?

### Portfolio Status Assessment

- **On Track**: Completion % matches plan + metrics trending + no blockers
- **At Risk**: Completion % behind plan OR metrics stalling OR blocker identified
- **Completed**: All success criteria met + learnings captured
- **Not Started**: Waiting for dependencies or not yet scheduled

### Validation Gates

Portfolio Check must pass:

- [ ] All active goals captured (from all teams)
- [ ] Each goal has current status (on track / at risk / completed / not started)
- [ ] Completion % reflects actual progress (from goal files)
- [ ] Health scores calculated (if available)
- [ ] Goals grouped by status clearly
- [ ] Strategic pillar distribution shown
- [ ] Resource allocation visible
- [ ] Top 5 risks identified + mitigations
- [ ] Dependencies mapped (critical path visible)
- [ ] Leadership actions identified
- [ ] Portfolio metrics calculated correctly

If portfolio check fails, report ERROR and what data is missing.
