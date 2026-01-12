# Team Roles & RACI: [GOAL]

**Goal**: [Name] | **Goal ID**: [###] | **Created**: [Date]

---

## Summary

*Clear role definitions and decision authority for goal execution.*

Successful execution requires clarity: Who owns what? Who decides? Who gets consulted? This document eliminates ambiguity.

---

## Goal Owner & Sponsor

**Goal Owner** (DRI - Directly Responsible Individual):  
**Name**: [Name]  
**Title**: [Title]  
**Authority**: Make all decisions about goal direction, timeline, scope  
**Accountability**: Goal success/failure  
**Success metric**: All success criteria met on timeline

**Executive Sponsor** (if applicable):  
**Name**: [Name]  
**Title**: [Title]  
**Authority**: Approve scope changes, resource reallocation, timeline extensions  
**Role**: Unblock escalations  

---

## Core Roles

### Technical Lead
**Name**: [Name]  
**Team**: [Team]  
**Responsibility**:
- Technical architecture decisions
- Code quality standards
- Performance targets
- Technology choices
- Risk assessment (technical)

**Authority**:
- Can make tech decisions within goal scope
- Can't change success criteria
- Can request scope reduction if technical blocker
- Escalates architectural conflicts to Goal Owner

**Success metric**: Code quality [standards], performance [targets], on-time delivery

---

### Product Owner
**Name**: [Name]  
**Team**: [Team]  
**Responsibility**:
- Feature prioritization
- User story definition
- Acceptance criteria
- Stakeholder communication
- Success criteria definition

**Authority**:
- Can prioritize features within milestones
- Can request feature scope changes
- Can't change delivery timeline without Goal Owner approval
- Validates acceptance criteria are met

**Success metric**: User satisfaction [NPS target], adoption [%], business impact [metric]

---

### QA Owner
**Name**: [Name]  
**Team**: [Team]  
**Responsibility**:
- Test strategy
- Acceptance validation
- Bug severity assessment
- Quality gates
- Deployment readiness

**Authority**:
- Can block deployment for critical bugs
- Can require additional testing
- Can't extend timeline without Goal Owner approval
- Can recommend scope reduction for quality

**Success metric**: Bug escape rate [%], test coverage [%], deployment success [%]

---

### DevOps / Infrastructure Owner (if applicable)
**Name**: [Name]  
**Team**: [Team]  
**Responsibility**:
- Infrastructure provisioning
- Deployment strategy
- Monitoring & alerting
- Rollback planning
- Performance optimization

**Authority**:
- Can require infrastructure changes
- Can block deployment for reliability risks
- Can recommend resource allocation
- Escalates capacity constraints

**Success metric**: Deployment success [%], SLA achievement [99.X%], incident response [MTTR]

---

### Data / Analytics Owner (if applicable)
**Name**: [Name]  
**Team**: [Team]  
**Responsibility**:
- Metrics definition
- Data collection setup
- Analytics dashboard
- Data privacy/compliance
- Performance measurement

**Authority**:
- Can request changes to measurement approach
- Can block unsafe data practices
- Can recommend data architecture
- Escalates compliance issues

**Success metric**: Metric accuracy [%], dashboard uptime [%], data quality [%]

---

### Communication / Project Owner (if applicable)
**Name**: [Name]  
**Team**: [Team]  
**Responsibility**:
- Stakeholder updates
- Status reporting
- Dependency coordination
- Team morale
- Process facilitation

**Authority**:
- Can request status updates
- Escalates blockers to stakeholders
- Can facilitate team discussions
- Recommends process improvements

**Success metric**: Stakeholder satisfaction [score], update timeliness [%], team engagement [eNPS]

---

## RACI Matrix

*For each milestone, define who is Responsible, Accountable, Consulted, Informed*

### Milestone 1: [Name]

| Activity | Goal Owner | Tech Lead | Product | QA | DevOps | Data |
|----------|-----------|-----------|---------|-----|--------|------|
| Define requirements | I | C | A/R | I | I | C |
| Architecture design | A | R | C | I | C | I |
| Infrastructure setup | I | C | I | I | A/R | I |
| Development | I | R | C | C | I | I |
| Code review | C | A/R | I | I | I | I |
| Testing | I | C | A/R | R | I | I |
| Deployment prep | C | C | I | A | R | C |
| Launch go-live | A | C | C | C | R | I |

### Milestone 2: [Name]

| Activity | Goal Owner | Tech Lead | Product | QA | DevOps | Data |
|----------|-----------|-----------|---------|-----|--------|------|
| Define requirements | I | C | A/R | I | I | C |
| Development | I | R | C | I | I | I |
| Integration testing | I | C | A/R | R | I | I |
| Performance testing | I | R | I | A | R | I |
| Launch | A | C | C | C | R | I |

### Milestone 3: [Name]

| Activity | Goal Owner | Tech Lead | Product | QA | DevOps | Data |
|----------|-----------|-----------|---------|-----|--------|------|
| Beta testing | I | C | A | R | I | C |
| Bug fixing | C | R | I | A | I | I |
| Performance optimization | C | R | I | A | A | C |
| Launch | A | C | C | C | R | I |

---

## RACI Legend

**R = Responsible** (does the work / actually implements)  
**A = Accountable** (makes final decision / approves / owns success)  
**C = Consulted** (provides input before decision)  
**I = Informed** (notified after decision made)

### RACI Rules

- **Every activity must have at least one R** (someone does the work)
- **Every activity must have exactly one A** (one person accountable)
- **A is usually the person's manager** or they own the role
- **Minimize C** (too many consultations = slow decisions)
- **Use I sparingly** (don't spam people with notifications)

---

## Role Interactions & Handoffs

### Tech Lead ↔ Product Owner
- **When**: Feature definition, scope discussions
- **How**: Async doc review (Tech proposes architecture, Product approves scope)
- **Conflict resolution**: Goal Owner decides scope vs. technical feasibility
- **Handoff**: Tech delivers implementation, Product validates acceptance

### QA ↔ Tech Lead
- **When**: Test strategy, bug assessment
- **How**: Weekly async updates on test coverage, blockers
- **Conflict resolution**: Critical bugs → Goal Owner decides (fix vs. defer)
- **Handoff**: Tech delivers code for testing, QA validates readiness

### DevOps ↔ Tech Lead
- **When**: Infrastructure, deployment, performance
- **How**: Async infrastructure planning before milestone starts
- **Conflict resolution**: Capacity constraints → Goal Owner prioritizes
- **Handoff**: Tech delivers code, DevOps deploys and monitors

### Product ↔ QA
- **When**: Acceptance criteria, user testing
- **How**: Async - Product defines, QA validates
- **Conflict resolution**: Quality vs. timeline → Goal Owner decides
- **Handoff**: QA validates acceptance, Product confirms launch readiness

---

## Phase Transitions & Role Changes

### Transition: M1 → M2

**Before transition (1 week prior)**:
- M1 owner (Tech Lead) prepares handoff
- M2 owner (Product/QA) reviews and asks questions
- Goal Owner validates readiness

**At transition**:
- M1 deliverables accepted by M2 team
- Knowledge transfer complete
- M1 team becomes support (available for questions)

**After transition**:
- M2 team owns execution
- M1 team available for ~1 week escalations
- M1 team transitions to new work

---

## Escalation Path

### When Roles Disagree

**Example conflict**: Tech Lead says "We can't meet timeline", Product says "We must ship by [date]"

**Escalation steps**:

1. **Tech Lead + Product negotiate** (24 hours)
   - Can they find compromise? (reduce scope? extend timeline?)
   - If resolved, done

2. **Escalate to Goal Owner** (4 hours response)
   - Goal Owner reviews both perspectives
   - Goal Owner decides: Reduce scope? Extend timeline? Add resources?
   - Decision final

3. **If Goal Owner needs more authority, escalate to Sponsor** (2 hours)
   - Sponsor approves resource allocation, timeline change, scope reduction
   - Decision final

### Example Decisions by Role

| Conflict | Authority | Decision |
|----------|-----------|----------|
| Tech wants clean code, QA wants speed | Goal Owner | "Ship with [technical debt]. QA writes 2-week plan to address" |
| Product wants 5 features, timeline has room for 3 | Goal Owner | "Ship 3 features. Other 2 → next quarter" |
| DevOps says infrastructure costs too high | Goal Owner | "Use [cost-optimized approach]. Revisit after launch" |
| Tech + Product agree, but Sponsor says "No" | Sponsor | "Not approved. [Reason]" |

---

## Success Metrics by Role

### Goal Owner
- Goal success criteria met (all SC achieved)
- On-time delivery (within 10% of planned timeline)
- Team satisfaction (eNPS >40)
- No critical escalations (≤1 per month)

### Technical Lead
- Code quality (test coverage >80%, review time <2 days)
- Performance targets (SC-001, SC-002 metrics)
- Technical debt tracking (documented and planned)
- On-time delivery of technical milestones

### Product Owner
- User satisfaction (NPS >50 or [target])
- Feature adoption ([target]% of users using new feature)
- Stakeholder satisfaction (score >4/5)
- On-time delivery of product milestones

### QA Owner
- Bug escape rate (<[X]% critical bugs found in production)
- Test coverage (>80% of code paths tested)
- Deployment success rate (>99% deployments succeed)
- On-time quality gate sign-off

### DevOps Owner
- SLA achievement (>99.X% uptime)
- Deployment success (>99% deployments succeed)
- Incident MTTR (<[X] minutes for critical issues)
- Infrastructure cost efficiency (within [budget])

### Data Owner
- Metric accuracy (data quality >99%)
- Dashboard uptime (>99.5% availability)
- Data collection completeness (>95% of events captured)
- Privacy compliance (zero violations)

---

## Communication Commitments

### By Role

**Goal Owner**:
- Weekly async update to all roles
- Daily availability for escalations
- Monthly steering meeting with sponsor

**Technical Lead**:
- Daily async standup
- Weekly update to Goal Owner
- Available same-day for technical blockers

**Product Owner**:
- Weekly async update
- Acceptance criteria clarity within 24 hours
- Daily availability for scope questions

**QA Owner**:
- Weekly test coverage update
- Blocker notification within 4 hours
- Daily availability for quality decisions

**DevOps Owner**:
- Weekly infrastructure/deployment status
- Capacity constraint notification within 24 hours
- Escalation resolution within 48 hours

**Data Owner**:
- Weekly metrics dashboard update
- Data quality issues within 48 hours
- Compliance issues immediately

---

## Team Sign-Off

**Goal Owner**: [Name] - Confirms role assignments and authority  
**Date**: [Date]

**Technical Lead**: [Name] - Understands scope and success metrics  
**Date**: [Date]

**Product Owner**: [Name] - Understands acceptance criteria authority  
**Date**: [Date]

**QA Owner**: [Name] - Understands quality gates and timelines  
**Date**: [Date]

**DevOps Owner**: [Name] - Understands infrastructure/deployment authority  
**Date**: [Date]

*Other roles (if applicable)*

---

## Related Documents

- `templates/async-coordination-template.md` - Communication patterns
- `templates/cross-goal-coordination-template.md` - Dependencies and handoffs
- `execution.md` - This goal's execution plan
