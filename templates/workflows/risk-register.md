---
description: Identify, assess, and track risks that could impact goal achievement. Builds a shared register with mitigation strategies and ownership.
handoffs:
  - label: Security Review
    agent: goalkit.security-review
    prompt: Identify and assess security-specific risks
    send: false
  - label: Cross-Goal Coordination
    agent: goalkit.cross-goal-coordination
    prompt: Communicate risk cascades to dependent goals
    send: false
scripts:
  sh: scripts/bash/setup-risk-register.sh --json "{GOAL_ID}"
  ps: scripts/powershell/setup-risk-register.ps1 -Json "{GOAL_ID}"
---

## User Input

- **Goal or Program**: Which goal or program are you assessing risks for?
- **Scope**: Full delivery, specific phase, or technical area?
- **Stakeholders**: Engineering, product, design, ops?

## Execution Flow

1. **Risk Identification** (20 min)
   - Brainstorm 8-12 risks across Technical, Organizational, Market, and External categories
   - Document each as: "If X happens, impact on goal is Y"

2. **Risk Assessment** (20 min)
   - Rate each: Probability (Low/Medium/High) × Impact (Low/Medium/High) = Score (1-9)
   - Flag Top 5 risks for active mitigation

3. **Mitigation Planning** (30 min)
   - For Top 5: define mitigation strategy, owner, timeline, acceptance criteria
   - For others: define monitoring approach (passive vs. active watch)
   - Set review cadence (weekly for Top 5, bi-weekly for others)
   - Link to escalation path for leadership visibility

## Validation Gate

- [ ] 8-12 risks identified across multiple categories
- [ ] Top 5 risks have explicit mitigations and owners
- [ ] Risk scores defensible with clear calculations
- [ ] Review cadence and escalation path defined

## Guidelines

- **Probability**: Low (<25%), Medium (25-70%), High (>70%)
- **Impact**: Low (minor delay), Medium (1-4 week delay), High (goal at risk)
- **Risk Statuses**: New, Mitigating, Resolved, Accepted
- **Mitigation Timing**: Start High/Medium-High risks immediately; others within 2 weeks

## Output

- **Output File**: `.goalkit/goals/[GOAL_ID]/risk-register.md`
- **Status Dashboard**: Weekly triage summary (Mitigating/Resolved/Escalated counts)
