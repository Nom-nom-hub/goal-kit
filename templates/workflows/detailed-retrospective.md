---
description: Conduct a comprehensive retrospective covering execution, quality, governance, and lessons learned. Captures what worked, what didn't, and how to improve.
handoffs: []
scripts:
  sh: scripts/bash/setup-detailed-retrospective.sh --json "{GOAL_ID}"
  ps: scripts/powershell/setup-detailed-retrospective.ps1 -Json "{GOAL_ID}"
---

## User Input

- **Goal or Program**: Which goal or program are you retrospecting on?
- **Participants**: Team members, stakeholders, leadership?
- **Scope**: Full execution, specific phase, or particular challenges?

## Execution Flow

1. **Execution Review** (30 min)
   - Compare planned vs. actual timeline: what shipped on time, late, early?
   - Analyze root causes for delays (scope, dependencies, technical, staffing)
   - Assess resource utilization and scope management

2. **Quality & Reliability Review** (20 min)
   - Review code coverage, bug trends, post-release issues
   - Assess release gate pass/fail and incident count/severity

3. **Governance & Risk Review** (20 min)
   - Analyze risk register outcomes (risks hit, avoided, new risks)
   - Review compliance/security outcomes and stakeholder communication

4. **Team & Culture Review** (15 min)
   - Assess collaboration, async effectiveness, and process effectiveness
   - Collect team feedback via survey (1-5 scale)

5. **Lessons Learned** (25 min)
   - **What Worked** (3-5 items): practices to repeat
   - **What to Improve** (3-5 items): pain points to address
   - **Action Items** (5-7 SMART items): owners, timelines, success measures

6. **Leadership Summary** (10 min)
   - 1-page executive summary: goal achieved %, key metrics, top 3 successes/improvements

## Validation Gate

- [ ] Execution metrics documented (timeline, velocity, scope)
- [ ] Quality/reliability metrics reviewed
- [ ] Risk register outcomes analyzed
- [ ] Team feedback collected via survey
- [ ] Action items have owners and timelines
- [ ] Leadership summary prepared

## Guidelines

- **Survey**: Clarity (1-5), Collaboration (1-5), Communication (1-5), open-ended keep/improve
- **Metrics**: On-time ≥80% good, Coverage 70-80% typical, Bug density <2/1000 LOC good
- **Action Items**: SMART format (Specific, Measurable, Assigned, Realistic, Time-bound)

## Output

- **Output File**: `.goalkit/goals/[GOAL_ID]/detailed-retrospective.md`
- **Executive Summary**, Metrics Dashboard, Action Items Tracker, Team Feedback
