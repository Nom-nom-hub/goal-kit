---
description: Identify, assess, and track risks that could impact goal achievement. Builds a shared register of risks with mitigation strategies and ownership.
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

- **Goal or Program**: Which goal or program are you building a risk register for?
- **Scope**: Full goal delivery, specific phase, or particular technical area?
- **Stakeholders**: Who should contribute risk identification (engineering, product, design, ops)?

## Outline

### Execution Flow

1. **Risk Identification** (30 min)
   - Brainstorm risks across technical, organizational, market, and dependency categories
   - Extract 8-12 distinct risks; discard duplicates
   - Document risk statement (if X happens, impact on goal is Y)

2. **Risk Assessment** (30 min)
   - Rate each risk: Probability (Low/Medium/High) and Impact (Low/Medium/High)
   - Calculate Risk Score: (Probability × Impact) on 1-9 scale
   - Flag Top 5 risks (highest score)

3. **Mitigation Planning** (45 min)
   - For each Top 5 risk, define:
     - **Mitigation Strategy**: How to reduce probability or impact
     - **Mitigation Owner**: Who owns this action
     - **Timeline**: When mitigation begins
     - **Acceptance Criteria**: How we know mitigation is effective
   - For other risks, define monitoring approach (passive vs. active watch)

4. **Risk Register Structure** (15 min)
   - Create register table: Risk ID, Statement, Category, P/I/Score, Status, Owner, Mitigation, Review Date
   - Establish review cadence (weekly for Top 5, bi-weekly for others)
   - Link to escalation path (when to surface risk to leadership)

5. **Handoff & Communication** (15 min)
   - Share register with team and stakeholders
   - Assign monitoring owners for each risk
   - Schedule weekly risk triage (15 min)

### Validation Gate: Risk Register Check

**Agent Must Confirm**:
- [ ] 8-12 risks identified across multiple categories
- [ ] Top 5 risks have explicit mitigation strategies and owners
- [ ] Risk scores are defensible (probability × impact calculation clear)
- [ ] Review cadence and escalation path defined
- [ ] All risks have status ("New", "Mitigating", "Resolved", "Accepted")

**If Not Met**: Ask stakeholder group to expand brainstorm or clarify mitigation approach.

### General Guidelines

- **Probability Scale**: Low (< 25%), Medium (25-70%), High (> 70%)
- **Impact Scale**: Low (minor delay/scope), Medium (1-4 week delay, significant scope cut), High (goal at risk, major scope impact)
- **Risk Categories**: Technical (architecture, dependencies), Organizational (staffing, budget), Market (demand, competition), External (regulation, vendors)
- **Mitigation Timing**: Start mitigation for P=High or (P=Medium AND I=High) immediately; others within 2 weeks
- **Watch List**: Risks below Top 5 should still be monitored; escalate if they spike in probability or impact
- **Dependency Risks**: Link risks from cross-goal-coordination (dependencies on other teams) to this register

### Reporting

- **Output File**: `.goalkit/goals/[GOAL_ID]/risk-register.md`
- **Status Dashboard**: Weekly risk triage summary (Mitigating/Resolved/Escalated counts)
- **Escalation Report**: Any High Impact or High Probability risks for leadership visibility
