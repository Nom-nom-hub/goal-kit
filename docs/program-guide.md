# Program Management Guide

*How to group related goals into cohesive programs.*

---

## Overview

A **program** is a collection of related goals working toward a shared outcome that can't be achieved by a single goal.

Examples:
- "Mobile App Launch Program" (3 goals: architecture, client, backend)
- "API Modernization Program" (4 goals: design, implementation, migration, documentation)
- "Enterprise GTM Program" (5 goals: product features, sales enablement, compliance, support, marketing)

Programs add structure when you have dependent work across multiple teams or long timelines.

---

## Program vs. Goal vs. Milestone

Know when to use each:

| **Unit** | **Duration** | **Scope** | **Teams** | **Example** |
|----------|----------|----------|----------|----------|
| **Goal** | 1-4 months | Single outcome | 1-2 | "Build API rate limiting" |
| **Program** | 2-6 months | Multiple outcomes (2-5 goals) | 2+ | "API Modernization" (design + build + migrate) |
| **Milestone** | 1-4 weeks | Part of a goal | Shared team | Milestone 1 of goal: "Infrastructure ready" |

**Decision Tree**:
- Is it one outcome? → Goal
- Is it 2-5 related goals with dependencies? → Program
- Is it 1-4 weeks of work? → Milestone (inside a goal)

---

## When to Use Programs

**Use a program if**:
- ✅ Work requires 5+ goals over 3+ months
- ✅ Multiple teams coordinating toward shared outcome
- ✅ Significant dependencies between goals
- ✅ Outcome is big strategic bet (customer-facing feature, system redesign)

**Don't use a program if**:
- ❌ Single goal with clear boundary
- ❌ Work is 1-2 months (just make it a goal)
- ❌ Goals are independent (no coordination needed)

---

## Program Structure

### Anatomy of a Program

```
Program: Mobile App Launch
├─ Goal 1: Core Architecture (5 weeks)
│   └─ Milestone 1: Design (Week 1-2)
│   └─ Milestone 2: Infra (Week 3-4)
│   └─ Milestone 3: Testing (Week 5)
│
├─ Goal 2: Client Features (6 weeks, starts Week 3)
│   └─ Blocks on Goal 1 Milestone 2
│
├─ Goal 3: Backend APIs (5 weeks, starts Week 1)
│   └─ Parallel to Goal 1
│
├─ Goal 4: User Testing & Polish (3 weeks, starts Week 9)
│   └─ Blocks on Goals 1-3 completion
│
└─ Goal 5: Beta Launch (2 weeks, starts Week 12)
    └─ Blocks on Goal 4 completion
```

### Key Elements

**Program Vision**: Why does the program exist?  
*Example: "Enable customers to build custom workflows, unlocking $5M new revenue."*

**Program Goals**: 2-5 goals executing the program

**Program Timeline**: Start date, key milestones, completion date

**Program Stakeholders**: Executive sponsor, program manager, goal owners, teams

**Program Success Criteria**: Program-level metrics (not goal-level)

**See**: `templates/program-template.md`

---

## Creating a Program

### Step 1: Validate Need
Ask:
- Is this really 2-5 goals? (not just 1 big goal)
- Do they have shared outcome? (not random collection)
- Are there dependencies? (sequencing matters)
- Is there executive sponsorship? (someone leading it)

If yes to all → Program. If no → Maybe just a goal.

---

### Step 2: Define Program Vision
Write 2-3 sentence vision statement:

*Example: "Launch real-time collaboration features to become the fastest-shipping product platform. Success means enabling 20% faster feature development for customers and improving code review experience from 20 min to 12 min average."*

Should answer:
- Why are we doing this?
- What's the outcome?
- How do we know it worked?

---

### Step 3: Decompose into Goals
Break program into 2-5 goals:

**Criteria**:
- Each goal is independently valuable (can ship standalone if needed)
- Each goal has clear owner and team
- Goals have explicit dependencies (G1 → G2 → G3)
- Goals fit in 4-8 week timeframe

**Example decomposition**:
- Goal 1: WebSocket server architecture + API (backend team, 6 weeks)
- Goal 2: Client integration + UI (frontend team, 6 weeks, starts Week 3)
- Goal 3: User testing + optimizations (QA + product, 2 weeks, starts Week 10)

**Anti-pattern**:
- ❌ 15 tiny goals (too many to coordinate)
- ❌ 1 mega-goal (harder to track progress)
- ✅ 3-4 medium goals (goldilocks)

---

### Step 4: Define Dependencies
Map what blocks what:

```
Program Timeline:
    Week 1-6
    ├─ Goal 1: Architecture ◄─── must complete before
    │    └─ Goal 2: Client (Weeks 3-8) - can start at Week 3
    │    └─ Goal 3: Testing (Weeks 8-9) - must wait for Goal 1 complete
    
    Week 10
    └─ Goal 4: Launch (Weeks 10-11) - depends on Goals 1-3 complete
```

**Types of dependencies**:
- **Sequential** (G1 → G2): G1 must complete before G2 starts
- **Parallel with handoff** (G1 | G2): Run parallel but sync at milestone
- **Completely parallel** (G1 || G2): No coordination needed

---

### Step 5: Resource the Program
Who's doing what?

| Goal | Team | Lead | Allocation | Duration |
|------|------|------|-----------|----------|
| 1 | Backend | Alice | 4 FTE | 6 weeks |
| 2 | Frontend | Bob | 3 FTE | 6 weeks (starts Week 3) |
| 3 | QA | Carol | 2 FTE | 2 weeks (starts Week 8) |
| 4 | Cross-functional | David (PM) | 6 FTE | 2 weeks (starts Week 10) |

**Total investment**: ~11 person-months over 11 weeks

---

### Step 6: Set Program Success Criteria
Not goal-level metrics. Program-level outcomes.

**Example**:
- Functional: "5 power users can build 50+ workflows"
- Business: "$5M ARR contribution by Q3"
- Quality: "99.9% uptime; <1% workflow failure"
- Team: "Developed expertise in microservices; zero attrition"

---

## Program Governance

### Roles

**Executive Sponsor**: Makes strategic decisions, approves budget, escalates risks

**Program Manager**: Coords goals, runs syncs, tracks timeline, manages dependencies

**Goal Owners**: Execute their goal; coordinate handoffs with other goals

**Steering Committee** (optional for big programs): Exec + goal leads + PM; meets monthly

### Decision Authority

| Decision | Authority | Timeline |
|----------|-----------|----------|
| Scope change (add/remove features) | Sponsor | Within 48 hours |
| Timeline slip >1 week | Sponsor | Escalate immediately |
| Goal reprioritization | Sponsor + Program Manager | Weekly review |
| Resource reallocation between goals | Program Manager | Immediate if goals agree |
| New risk mitigation | Goal Owner (if <resources), Sponsor (if >resources) | Within 24 hours |

---

### Communication Cadence

**Weekly**: Goal owners async status in channel
- 1-2 sentence per goal
- Any blockers or changes
- Dependencies on track?

**Bi-weekly**: Program team sync (30 min)
- Goal status walk-through
- Risk identification
- Decision on any escalations
- Celebrate progress

**Monthly**: Program steering/review (60 min)
- Executive sponsor reviews program health
- Any strategic changes?
- Resource needs?
- Budget on track?

**At key milestones**: Demo/verification
- Goal 1 completion → Demo to stakeholders
- Goal 3 completion → Review with customer
- Full program → Launch celebration

---

## Program Risks

### Common Risks

**Scope Creep**
- **Problem**: Stakeholders keep adding features mid-program
- **Solution**: Explicit scope document; strict gate on changes (only sponsor can approve)
- **Mitigation**: Separate scope into Phase 1 (MVP) vs. Phase 2 (enhancements)

**Dependency Delays**
- **Problem**: Goal 1 slips 2 weeks; cascades to Goals 2-4
- **Solution**: Critical path management + buffer time on blocking goals
- **Mitigation**: Parallel work where possible; fallback strategies

**Resource Unavailability**
- **Problem**: Team member leaves; Goal 2 at risk
- **Solution**: Cross-training before program starts
- **Mitigation**: Hire contractor; pull resources from lower-priority goal

**Quality Issues**
- **Problem**: Team ships fast but bugs pile up; Goal 4 testing takes longer
- **Solution**: Quality checkpoints at each milestone
- **Mitigation**: Testing gates; require code review + test coverage

**Integration Failures**
- **Problem**: Goal 1 & Goal 2 work independently; integration is hard
- **Solution**: Clear API contracts; integration testing from Week 3
- **Mitigation**: Regular integration tests; fail fast

---

## Program Metrics

### Tracking Progress

| Metric | Frequency | How to Measure |
|--------|-----------|---|
| On-Time Progress | Weekly | % completion vs. planned schedule |
| Goal Health | Weekly | # on track / at risk / completed |
| Resource Utilization | Weekly | Are teams allocated properly? |
| Risk Status | Bi-weekly | Any new risks? Mitigations working? |
| Quality Metrics | Per milestone | Test coverage, bug density |
| Scope Management | Weekly | Any changes requested? Approved? |

### Program Health Scorecard

Each week, rate program 1-5:

```
Week 4 Program Health:
- Schedule adherence: 4/5 (Goal 1 on track, Goal 2 started on time)
- Quality: 4/5 (Code review + tests passing, minor bugs captured)
- Team morale: 5/5 (Great collaboration, good energy)
- Stakeholder alignment: 4/5 (Executive sponsor happy, one customer question)
- Risk management: 3/5 (Resource availability concern, discussing mitigation)

Overall: 4/5 (On track, minor risks being addressed)
```

---

## Program Completion & Transition

### Launch Phase (2 weeks pre-launch)
- [ ] All goals meet success criteria
- [ ] Documentation complete (user guides, API docs, troubleshooting)
- [ ] Support team trained
- [ ] Monitoring + alerting configured
- [ ] Rollback plan tested
- [ ] Customer communication ready

### Launch
- [ ] Soft launch (internal + power users)
- [ ] Monitor for 1 week (any showstoppers?)
- [ ] Public launch + marketing campaign
- [ ] Customer success team ready to support

### Post-Launch (Weeks 1-4)
- [ ] Daily standup with program team
- [ ] Customer feedback loop active
- [ ] Hot fixes for any issues
- [ ] Success metrics dashboard live
- [ ] Begin handoff to steady-state product team

### Program Closure (Week 4+)
- [ ] All goals transitioned to regular product team
- [ ] Learning retrospective completed
- [ ] Team celebration
- [ ] Program documented and archived
- [ ] Lessons applied to future programs

---

## Program Common Mistakes

❌ **Too many goals (7+)**  
Instead: Keep to 3-5 goals; excess becomes own program

❌ **Unclear dependencies; hoping things will work out**  
Instead: Explicit dependency map; schedule sequentially

❌ **Program manager is bottleneck; makes all decisions**  
Instead: Clear decision authority; PM coordinates, doesn't decide everything

❌ **No scope boundaries; feature requests added during execution**  
Instead: Strict scope gate; changes require sponsor approval + timeline extension

❌ **All program goals start same day (no staggering)**  
Instead: Stagger start dates based on dependencies (Goal 1 complete → Goal 2 start)

❌ **No celebration at completion**  
Instead: Team lunch, internal announcement, thank-you notes from sponsor

---

## Program vs. Project Management

**Goal Kit Programs** are not project management (JIRA, timelines, Gantt charts).

Programs in Goal Kit:
- ✅ Focus on **outcomes** not tasks
- ✅ Teams retain autonomy on **how** to execute
- ✅ Flexible on **timeline** if metrics prove progress
- ✅ **Learning-focused** not compliance-focused
- ✅ **Goal owners** lead, not external PMs controlling teams

If you need formal project management (strict timelines, task breakdowns, resource leveling), use a separate tool. Goal Kit programs provide strategic grouping + coordination, not task management.

---

## Related Templates & Guides

- `templates/program-template.md` - Program planning template
- `docs/alignment-guide.md` - Align program goals to vision
- `docs/portfolio-management.md` - Manage program in portfolio
- `docs/coordination-guide.md` - Cross-goal coordination within programs (Phase 2)
