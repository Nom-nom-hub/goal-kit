# Detailed Retrospective

**Goal/Program**: [Goal or Program Name]  
**Review Period**: [Start Date] to [End Date]  
**Retrospective Conducted**: [Date]  
**Facilitator**: [Name]  
**Participants**: [Names, roles]  

---

## Executive Summary

### Goal Status

| Metric | Plan | Actual | Status |
|--------|------|--------|--------|
| **Delivery Date** | [Planned Date] | [Actual Date] | [✓ On-Time / ⚠ Late / ✓ Early] |
| **Scope Delivered** | 100% | [%] | [✓ / ⚠] |
| **Quality Gate** | All passing | [# Passing / Total] | [✓ / ✗] |
| **Team Satisfaction** | - | [Score 1-5] | [Assessment] |

### Key Metrics Summary

| Metric | Value | Assessment |
|--------|-------|-----------|
| On-time delivery % | [%] | [✓ Good / ⚠ At risk / ✗ Failed] |
| Code coverage | [%] | [✓ / ⚠ / ✗] |
| Post-release bugs (7 days) | [#] | [✓ / ⚠ / ✗] |
| Uptime | [%] | [✓ / ⚠ / ✗] |
| Team satisfaction | [Score/5] | [✓ / ⚠ / ✗] |

### Overall Assessment

[1-2 sentence summary of goal success, major accomplishments, and key learnings]

---

## Execution Review

### Timeline Accuracy

**Planned Timeline**:
- Kickoff: [Date]
- Phase 1: [Dates]
- Phase 2: [Dates]
- Release: [Date]

**Actual Timeline**:
- Kickoff: [Date] ([variance])
- Phase 1: [Dates] ([variance])
- Phase 2: [Dates] ([variance])
- Release: [Date] ([variance])

**Analysis**:

| Milestone | Planned | Actual | Variance | Root Cause |
|-----------|---------|--------|----------|-----------|
| Milestone 1 | [Date] | [Date] | [+/- days] | [Why early/late] |
| Milestone 2 | [Date] | [Date] | [+/- days] | [Why early/late] |
| Milestone 3 | [Date] | [Date] | [+/- days] | [Why early/late] |

**Velocity Trend**:
- Week 1-2: [Features/points completed]
- Week 3-4: [Features/points completed]
- Week 5-6: [Features/points completed]
- **Trend**: [Improving / Stable / Declining]

**Key Lessons**:
- [ ] Lesson 1: [What we learned about estimation or execution]
- [ ] Lesson 2: [What we learned about estimation or execution]

### Resource Utilization

**Staffing**:

| Role | Planned | Actual | Utilization | Assessment |
|------|---------|--------|-------------|-----------|
| Engineering | [# headcount] | [# headcount] | [%] | [Over/under-staffed] |
| QA | [# headcount] | [# headcount] | [%] | [Over/under-staffed] |
| Design | [# headcount] | [# headcount] | [%] | [Over/under-staffed] |
| Product | [# headcount] | [# headcount] | [%] | [Over/under-staffed] |

**Skill Mix Assessment**:
- [ ] Did we have the right technical skills? [Yes / Partial / No]
- [ ] Were there skill gaps? [List any gaps]
- [ ] How were gaps addressed? [Training, hiring, external support, etc.]

**Load Assessment**:
- [ ] Were people over-utilized? [Yes / Partial / No]
  - Who: [Names]
  - Impact: [Burnout risk, quality issues, timeline pressure]
- [ ] Were people under-utilized? [Yes / Partial / No]
  - Who: [Names]
  - Reason: [Work not scoped, blocked, over-planned]

### Scope Management

**Original Scope**: [Scope list or features]  
**Planned Scope**: [Scope at project start]  
**Delivered Scope**: [Scope actually shipped]  
**Deferred Scope**: [Features cut or deferred]  

**Scope Changes Summary**:

| Change | Type | Size | Reason | Impact |
|--------|------|------|--------|--------|
| [Feature/task added] | Added | [S/M/L] | [Why] | [Timeline/quality impact] |
| [Feature cut] | Removed | [S/M/L] | [Why] | [Timeline/quality impact] |

**Total Scope Creep**: [+/- %, analysis of impact]

**Key Lessons**:
- [ ] Lesson 1: [How to prevent future scope creep]
- [ ] Lesson 2: [How to better scope goals upfront]

---

## Quality & Reliability Review

### Code Quality Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Code coverage (unit) | 80% | [%] | [✓ / ⚠ / ✗] |
| Code coverage (integration) | 40% | [%] | [✓ / ⚠ / ✗] |
| Code review turnaround | 24 hours | [hours] | [✓ / ⚠ / ✗] |
| Test pass rate | 95% | [%] | [✓ / ⚠ / ✗] |
| Linting errors | 0 | [#] | [✓ / ⚠ / ✗] |
| Type checking errors | 0 | [#] | [✓ / ⚠ / ✗] |

**Assessment**: [Summary of code quality, any concerning trends]

### Bug Metrics

| Severity | Identified | Resolved | Post-Release |
|----------|-----------|----------|-------------|
| Critical | [#] | [#] | [#] |
| High | [#] | [#] | [#] |
| Medium | [#] | [#] | [#] |
| Low | [#] | [#] | [#] |

**Bug Density**: [# bugs per 1000 LOC] (Target: < 2)

**Post-Release Quality** (first 7 days):
- Critical issues: [#] | Resolution time: [hours]
- High issues: [#] | Resolution time: [hours]
- Customer-reported issues: [#] | Response time: [hours]

**Assessment**: [Were quality gates adequate? Any surprises?]

### Release Readiness

**Release Gates at Ship**:

| Gate | Target | Actual | Status |
|------|--------|--------|--------|
| Code quality (lint/types) | 100% passing | [%] | [✓ / ✗] |
| Functional tests | 95%+ passing | [%] | [✓ / ✗] |
| Coverage | ≥80% unit | [%] | [✓ / ✗] |
| Security scan | 0 Critical/High | [#] | [✓ / ✗] |
| Performance benchmarks | Targets met | [Met/Miss] | [✓ / ✗] |
| Accessibility audit | WCAG AA | [# violations] | [✓ / ✗] |

**Release Decision**: [Go / No-Go / Go with exceptions (list)]

### Production Reliability

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Uptime (7 days post-launch) | 99.9% | [%] | [✓ / ⚠ / ✗] |
| Error rate | < 0.5% | [%] | [✓ / ⚠ / ✗] |
| Response time (p95) | < 200ms | [ms] | [✓ / ⚠ / ✗] |
| Critical incidents | 0 | [#] | [✓ / ⚠ / ✗] |
| MTTR (mean time to resolve) | < 1 hour | [hours] | [✓ / ⚠ / ✗] |

**Incident Analysis** (if any):
- Incident 1: [Date, description, root cause, resolution time, prevention measure]
- Incident 2: [Date, description, root cause, resolution time, prevention measure]

**Assessment**: [Overall reliability assessment, any patterns or concerns]

---

## Governance & Risk Review

### Risk Register Outcomes

**Risks Materialized**:
- Risk [ID]: [Description] | Mitigation effectiveness: [% impact reduction]
- Risk [ID]: [Description] | Mitigation effectiveness: [% impact reduction]

**Risks Avoided**:
- Risk [ID]: [Description] | Mitigation prevented: [Yes / Partial / No]

**Unexpected Risks** (emerged during execution):
- New Risk 1: [Description, how handled, lessons learned]
- New Risk 2: [Description, how handled, lessons learned]

**Risk Management Assessment**:
- [ ] Were top risks identified accurately upfront? [Yes / Partial / No]
- [ ] Were mitigations effective? [Yes / Partial / No]
- [ ] Did new risks surprise us? [Yes / Partially / No]

**Key Lessons**:
- [ ] Lesson 1: [How to improve risk identification]
- [ ] Lesson 2: [How to improve mitigation planning]

### Compliance & Security

**Compliance Requirements Met**:
- [ ] [Requirement 1]: [Status: Met / Partial / Gap]
  - Evidence: [Where compliance is documented]
- [ ] [Requirement 2]: [Status: Met / Partial / Gap]

**Security Review**:
- Findings: [# Critical, # High, # Medium, # Low]
- Remediation status: [% resolved, timeline for remaining]
- Post-release security issues: [#, resolution time]

**Assessment**: [Any compliance or security concerns]

### Communication & Alignment

**Status Update Cadence**:
- Planned: [Daily standup, weekly sync, etc.]
- Actual: [Cadence maintained? Any skips?]
- Effectiveness: [1-5 scale, feedback]

**Escalations**:
- Count: [#]
- Types: [Decision needed, blocker, quality concern, etc.]
- Resolution time: [Average days to resolve]
- Effectiveness: [Did escalation process work well?]

**Key Decision Documentation**:
- [ ] [Decision 1]: Documented where? [Issue tracker, wiki, Slack, etc.]
- [ ] [Decision 2]: Documented where?

**Assessment**: [Was communication sufficient? Any blind spots?]

---

## Team & Culture Review

### Collaboration Assessment

| Aspect | Rating | Feedback |
|--------|--------|----------|
| **Cross-functional collaboration** | [1-5] | [What went well / what didn't] |
| **Engineering <-> Product alignment** | [1-5] | [What went well / what didn't] |
| **Engineering <-> QA alignment** | [1-5] | [What went well / what didn't] |
| **Decision-making clarity** | [1-5] | [What went well / what didn't] |
| **Conflict resolution** | [1-5] | [What went well / what didn't] |

### Async-First Effectiveness

- **Daily Standups**: [Useful / Mostly useful / Ceremony / Not useful]
  - Feedback: [What should change]
- **Weekly Syncs**: [Useful / Mostly useful / Ceremony / Not useful]
  - Feedback: [What should change]
- **Documentation**: [Excellent / Good / Adequate / Poor]
  - Gaps: [What wasn't documented well]
- **Decision-Making**: [Clear / Mostly clear / Often unclear / Chaotic]
  - Improvement ideas: [How to improve]

### Skills & Learning

**Technologies Learned**:
- [ ] [Tech 1]: Who learned it? [Names]
- [ ] [Tech 2]: Who learned it? [Names]

**Skills Developed**:
- [ ] [Skill 1]: [Team member], level improved from [X] to [Y]
- [ ] [Skill 2]: [Team member], level improved from [X] to [Y]

**Skills Gaps Identified** (for future goals):
- [ ] Gap 1: [Description, plan to address]
- [ ] Gap 2: [Description, plan to address]

**Mentoring/Coaching**:
- [ ] [Mentor 1] mentored [Mentee 1] on [Topic]
- [ ] [Mentor 2] mentored [Mentee 2] on [Topic]

### Process Effectiveness

| Process | Effectiveness | Feedback |
|---------|----------------|----------|
| **Daily standup** | [Useful / Ceremony / Skip] | [What to change] |
| **Code review** | [Helpful / Adding friction / Need improvement] | [Turnaround, feedback quality, rigor] |
| **Testing process** | [Well-structured / Ad hoc / Chaotic] | [What to change] |
| **Deployment process** | [Smooth / Manual / Error-prone] | [What to improve] |
| **Issue tracking** | [Clear / Confusing / Inconsistent] | [What to change] |

### Team Satisfaction

**Survey Results** (1-5 scale):

| Question | Score | Comment |
|----------|-------|---------|
| How clear was the goal? | [Score] | [Feedback] |
| How well did the team collaborate? | [Score] | [Feedback] |
| How effective was our communication? | [Score] | [Feedback] |
| Did you feel supported/unblocked? | [Score] | [Feedback] |
| Would you want to work on this team again? | [Score] | [Feedback] |

**Average Team Satisfaction**: [Score/5]

**Assessment**: [Overall morale, engagement, burnout risk]

---

## Quantified Outcomes & Trends

### Delivery Metrics

| Metric | Baseline | Actual | vs. Target | vs. Industry |
|--------|----------|--------|-----------|--------------|
| On-time delivery | [% prev goal] | [%] | [Target: >80%] | [Benchmark: X%] |
| Velocity (features/week) | [# prev] | [#] | [Target: X/wk] | [Team avg: X/wk] |
| Cycle time (days idea→production) | [# days prev] | [# days] | [Target: <14 days] | [Industry avg: X] |
| Rework % | [% prev] | [%] | [Target: <10%] | [Team avg: X%] |

### Quality Metrics

| Metric | Baseline | Actual | vs. Target | Trend |
|--------|----------|--------|-----------|-------|
| Coverage (unit) | [% prev] | [%] | [Target: 80%] | [↑ / → / ↓] |
| Bugs per 1K LOC | [# prev] | [#] | [Target: <2] | [↑ / → / ↓] |
| Post-release issues | [# prev] | [#] | [Target: <5 critical] | [↑ / → / ↓] |
| Uptime | [% prev] | [%] | [Target: 99.9%] | [↑ / → / ↓] |

### Team Metrics

| Metric | Baseline | Actual | Trend |
|--------|----------|--------|-------|
| Team satisfaction | [Score prev] | [Score] | [↑ / → / ↓] |
| Overtime hours/person/week | [# prev] | [#] | [↑ / → / ↓] |
| Training hours/person | [# prev] | [#] | [↑ / → / ↓] |
| Participation in syncs | [% prev] | [%] | [↑ / → / ↓] |

### Analysis & Insights

**Improving Metrics**: [Which metrics are trending up, what drove improvement]

**Declining Metrics**: [Which metrics are trending down, root causes, how to reverse]

**Stable Metrics**: [Which metrics remained consistent, is this expected/acceptable?]

---

## What Worked Well (Keep Doing)

### Practice 1: [Specific practice or approach]

- **Why it worked**: [What was effective about it]
- **Team feedback**: [Quotes or key themes]
- **Recommendation**: Keep doing this for future goals

### Practice 2: [Specific practice or approach]

- **Why it worked**: [What was effective about it]
- **Team feedback**: [Quotes or key themes]
- **Recommendation**: Keep doing this for future goals

### Practice 3: [Specific practice or approach]

- **Why it worked**: [What was effective about it]
- **Team feedback**: [Quotes or key themes]
- **Recommendation**: Keep doing this for future goals

### Shout-Outs

- [ ] **[Team Member 1]**: [Recognition for contribution]
- [ ] **[Team Member 2]**: [Recognition for contribution]

---

## What Could Improve

### Challenge 1: [Specific pain point or inefficiency]

- **Why it was a problem**: [Impact on timeline, quality, morale, etc.]
- **Root cause**: [What caused the issue]
- **Team feedback**: [Quotes or themes]

### Challenge 2: [Specific pain point or inefficiency]

- **Why it was a problem**: [Impact on timeline, quality, morale, etc.]
- **Root cause**: [What caused the issue]
- **Team feedback**: [Quotes or themes]

### Challenge 3: [Specific pain point or inefficiency]

- **Why it was a problem**: [Impact on timeline, quality, morale, etc.]
- **Root cause**: [What caused the issue]
- **Team feedback**: [Quotes or themes]

---

## Action Items for Improvement

### Priority 1: [Improvement Area]

- **Action**: [Specific, measurable action to take]
- **Owner**: [Name]
- **Timeline**: [When to complete]
- **Success Criteria**: [How we measure success]
- **Owner Commit**: [Owner signature / date]

### Priority 2: [Improvement Area]

- **Action**: [Specific, measurable action to take]
- **Owner**: [Name]
- **Timeline**: [When to complete]
- **Success Criteria**: [How we measure success]
- **Owner Commit**: [Owner signature / date]

### Priority 3: [Improvement Area]

- **Action**: [Specific, measurable action to take]
- **Owner**: [Name]
- **Timeline**: [When to complete]
- **Success Criteria**: [How we measure success]
- **Owner Commit**: [Owner signature / date]

### Priority 4: [Improvement Area]

[Same structure]

### Priority 5: [Improvement Area]

[Same structure]

---

## Carry-Forward to Next Goal

### Patterns & Approaches to Repeat

- [ ] **[Pattern/Approach 1]**: [Why effective, when to use, team contact]
- [ ] **[Pattern/Approach 2]**: [Why effective, when to use, team contact]
- [ ] **[Pattern/Approach 3]**: [Why effective, when to use, team contact]

### Tools & Templates to Reuse

- [ ] **[Tool/Template 1]**: [What it is, where it's stored, how to use]
- [ ] **[Tool/Template 2]**: [What it is, where it's stored, how to use]

### Knowledge & Documentation

- [ ] **[Doc/Runbook 1]**: [What's documented, where stored, owner for updates]
- [ ] **[Doc/Runbook 2]**: [What's documented, where stored, owner for updates]

---

## Leadership Summary (1 Page)

**Goal**: [Goal name and objective]  
**Status**: [Shipped, % complete, quality/reliability]  

**Key Metrics**:
- Delivery: [On-time / Late / Early + days]
- Quality: Coverage [%], bugs [#], post-release issues [#]
- Reliability: [Uptime %], incidents [#], MTTR [hours]
- Team: Satisfaction [Score/5], morale [Assessment]

**Top 3 Successes**:
1. [Achievement + why it matters]
2. [Achievement + why it matters]
3. [Achievement + why it matters]

**Top 3 Areas for Improvement**:
1. [Challenge + business impact + how to fix]
2. [Challenge + business impact + how to fix]
3. [Challenge + business impact + how to fix]

**Recommendations for Next Goals**:
- [Recommendation 1: Specific action or pattern]
- [Recommendation 2: Specific action or pattern]
- [Recommendation 3: Specific action or pattern]

---

## Appendix: Raw Data & Supporting Evidence

### Survey Responses
[Attach anonymized survey results]

### Metrics Dashboards
[Link to live dashboards or screenshots]

### Risk Register Review
[Link to risk register with outcomes]

### Incident Reports
[Links to any major incident post-mortems]

---

**Retrospective Prepared By**: [Name]  
**Approved By**: [Engineering Lead / Director]  
**Conducted On**: [Date]  
**Distribution**: [Team, Leadership, Archive]  

**Next Goal Kickoff**: [Date]
