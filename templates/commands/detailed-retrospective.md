---
description: Conduct a comprehensive retrospective covering execution, quality, governance, and lessons learned. Captures what worked, what didn't, and how to improve future goals.
handoffs: []
scripts:
  sh: scripts/bash/setup-detailed-retrospective.sh --json "{GOAL_ID}"
  ps: scripts/powershell/setup-detailed-retrospective.ps1 -Json "{GOAL_ID}"
---

## User Input

- **Goal or Program**: Which goal or program are you retrospecting on?
- **Participants**: Who should participate (team members, stakeholders, leadership)?
- **Scope**: Full execution, specific phase, particular challenges, or entire program?

## Outline

### Execution Flow

1. **Execution Review** (60 min)
   - **Timeline Accuracy**: Compare planned vs. actual timeline
     - Which milestones shipped on time, late, or early?
     - Root causes for delays (scope, dependencies, technical, staffing)
     - Velocity trends (improved, stable, degraded over time)
   - **Resource Utilization**: Did we have the right people, skills, time?
     - Staffing: Was team size appropriate, skill mix right?
     - Load: Were people over/under-utilized?
     - Blockers: What resource constraints existed?
   - **Scope Management**: Did scope creep occur?
     - Unplanned work added vs. planned scope
     - Decisions to defer/cut scope
     - Impact of scope changes on timeline

2. **Quality & Reliability Review** (45 min)
   - **Quality Metrics**: Review code quality, test coverage, bug trends
     - Coverage vs. target (met, exceeded, fell short)
     - Bug severity distribution (Critical/High vs. Low)
     - Post-release issues (customer-reported, severity, resolution time)
   - **Release Readiness**: Did we meet quality gates?
     - Release gate criteria and pass/fail status
     - Critical issues at release (known limitations documented?)
   - **Reliability in Production**: Uptime, errors, user impact
     - Incident count and severity
     - Response/resolution times
     - Customer satisfaction (NPS, feedback)

3. **Governance & Risk Review** (45 min)
   - **Risk Register Performance**: Which risks materialized, which were avoided?
     - Risks that hit (did mitigation help reduce impact?)
     - Risks that didn't hit (was mitigation effective?)
     - New risks that emerged (what should we do better next time?)
   - **Compliance & Security**: Any regulatory/security issues?
     - Were compliance requirements met?
     - Any security incidents or findings?
     - Audit readiness (passed/failed, findings count)
   - **Communication & Alignment**: Did stakeholders stay informed?
     - Status update cadence (met expectations?)
     - Escalations and how they were resolved
     - Decisions made and documented

4. **Team & Culture Review** (30 min)
   - **Team Collaboration**: How well did team work together?
     - Cross-functional coordination (smooth, friction points?)
     - Async-first effectiveness (clear decisions, reduced meetings?)
     - Team morale and engagement (survey: 1-5 scale)
   - **Skills & Learning**: What did team learn?
     - New technologies, patterns, or approaches adopted
     - Skills gaps identified and how addressed
     - Mentoring/coaching that happened
   - **Process Effectiveness**: Which processes worked well, which slowed us down?
     - Daily standups, weekly syncs (useful or unnecessary?)
     - Code review, testing process (friction or helpful?)
     - Deployment process (smooth or painful?)

5. **Data-Driven Insights** (30 min)
   - Quantify outcomes:
     - **Delivery**: On-time delivery %, velocity (story points or features/week), cycle time (idea to production)
     - **Quality**: Code coverage %, test pass rate %, bugs per feature, post-release issues
     - **Reliability**: Uptime %, incident count, MTTR (mean time to resolution)
     - **Velocity**: Features shipped, scope delivered vs. planned, rework %
     - **Engagement**: Team satisfaction (1-5 scale), participation in syncs, code review quality
   - Compare to baseline (previous goal, team average, industry benchmark)
   - Identify trends (improving, declining, stable)

6. **Lessons Learned & Action Items** (45 min)
   - **What Worked Well** (3-5 items):
     - Specific practices or decisions to repeat
     - People/teams to celebrate
     - Conditions that enabled success
   - **What Could Improve** (3-5 items):
     - Specific pain points to address
     - Bottlenecks or inefficiencies
     - Skill gaps or process issues
   - **Action Items** (5-7 items):
     - Specific, measurable improvements
     - Owner and timeline
     - How to measure success
     - Examples: "Implement automated security scanning in CI/CD", "Establish code review SLA of 24 hours", "Create runbook for on-call escalations"
   - **Carry-Forward**: Practices or patterns to apply to next goal

7. **Leadership Summary** (15 min)
   - Create executive summary (1 page):
     - Goal achieved? % complete, shipping date, quality/reliability
     - Key metrics (on-time, quality, team satisfaction)
     - Top 3 successes and 3 improvement areas
     - Recommendations for next goals
   - Communicate findings to leadership and stakeholders

### Validation Gate: Detailed Retrospective Check

**Agent Must Confirm**:
- [ ] Execution metrics documented (timeline, velocity, scope)
- [ ] Quality/reliability metrics reviewed (coverage, bugs, uptime)
- [ ] Risk register outcomes analyzed (risks hit, avoided, new risks)
- [ ] Team feedback collected (via survey or interviews)
- [ ] Data-driven insights quantified with baselines/trends
- [ ] Action items specific and measurable with owners
- [ ] Leadership summary prepared

**If Not Met**: Expand data collection or team feedback.

### General Guidelines

- **Survey Questions** (for team feedback):
  - "How clear was the goal?" (1-5)
  - "How well did the team collaborate?" (1-5)
  - "How effective was our communication?" (1-5)
  - "What's one thing we should keep doing?" (open)
  - "What's one thing we should improve?" (open)

- **Metrics Interpretation**:
  - **On-Time Delivery**: ≥80% is good, ≥95% is excellent, <60% signals planning/execution issues
  - **Code Coverage**: 70-80% is typical for mature products, <50% signals quality risk, >90% signals diminishing returns
  - **Bug Density**: <2 bugs per 1000 LOC is good, >5 signals quality issues
  - **Uptime**: 99%+ for production, <99% signals reliability issues
  - **Team Satisfaction**: 4+ is healthy, 3-4 signals engagement/process issues, <3 signals need for immediate intervention
  - **Cycle Time**: Faster is better; if increasing, signals process friction

- **Comparison Baselines**: Compare to previous goal (improvement/regression), team average (above/below), industry benchmark (competitive position)

- **Action Item Quality**: SMART format (Specific: clear what to do, Measurable: how to know success, Assigned: owner, Realistic: doable in timeframe, Time-bound: deadline)

- **Retrospective Cadence**: After every significant goal completion; for long goals (3+ months), conduct mid-point retrospective

### Reporting

- **Output File**: `.goalkit/goals/[GOAL_ID]/detailed-retrospective.md`
- **Executive Summary**: 1-page summary for leadership (goal achieved %, key metrics, top findings)
- **Metrics Dashboard**: Quantified outcomes with baseline comparisons and trends
- **Action Items Tracker**: All improvements with owners, deadlines, and success criteria
- **Team Feedback Summary**: Aggregated survey results and top themes
- **Lessons Learned Archive**: Stored for reference by future teams
