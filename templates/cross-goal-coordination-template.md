# Cross-Goal Coordination: [GOAL]

**Goal**: [Name] | **Goal ID**: [###] | **Created**: [Date]

---

## Summary

*How this goal coordinates with other goals in the portfolio.*

This goal is part of a larger execution context with [# other goals]. Coordination ensures:
- Blocked goals know when they'll be unblocked
- Dependent goals get what they need on time
- Slippage doesn't cascade
- Teams can plan handoffs explicitly

---

## Goals This Goal Depends On

### Blocking Goals (must complete first)

| Goal ID | Goal Name | Critical Deliverable | Timeline | Impact if Slips |
|---------|-----------|-----|---|---|
| [###] | [Name] | [What we're waiting for] | Must complete by [date] | We can't start. Slip impacts us by [time] |
| [###] | [Name] | [What we're waiting for] | Must complete by [date] | We can't start. Slip impacts us by [time] |

### Dependency Details

**Goal [###]: [Name]**
- **Why it blocks us**: [Explain the dependency]
- **What we're waiting for**: [Specific deliverable - API contract, design, data model, code, etc.]
- **When we need it**: [Specific date/milestone]
- **If it slips**: [How much does our timeline slip?]
- **Contingency if it slips 2+ weeks**: [Do we have a fallback approach?]
- **Owner contact**: [Who to escalate to if at-risk]

**Goal [###]: [Name]**
- **Why it blocks us**: [Explain]
- **What we're waiting for**: [Specific deliverable]
- **When we need it**: [Specific date]
- **If it slips**: [Timeline impact]
- **Contingency if it slips 2+ weeks**: [Fallback approach]
- **Owner contact**: [Escalation contact]

---

## Goals This Goal Unblocks

### Dependent Goals (waiting on us)

| Goal ID | Goal Name | What They're Waiting For | Timeline | Impact if We Slip |
|---------|-----------|-----|---|---|
| [###] | [Name] | [What we deliver to them] | They start on [date] | They slip [time] if we're late |
| [###] | [Name] | [What we deliver to them] | They start on [date] | They slip [time] if we're late |

### Unblocking Details

**Goal [###]: [Name]**
- **Why we unblock them**: [Explain]
- **What they need from us**: [Specific deliverable - API, design, code review, etc.]
- **When they need it**: [Specific date]
- **What they'll do when they get it**: [How will they use it?]
- **If we slip 1 week**: [What happens to their timeline?]
- **If we slip 2 weeks**: [Do they have fallback?]
- **Owner contact**: [Who manages the coordination]

**Goal [###]: [Name]**
- **Why we unblock them**: [Explain]
- **What they need from us**: [Specific deliverable]
- **When they need it**: [Specific date]
- **What they'll do with it**: [Usage]
- **If we slip 1 week**: [Timeline impact]
- **If we slip 2 weeks**: [Their fallback]
- **Owner contact**: [Coordination contact]

---

## Critical Path Analysis

### Overall Sequence

```
Start                [Now]
  ↓
Goal [###] (Blocker 1)
  │ Duration: [weeks]
  │ Critical: Yes/No - if this slips, [impact]
  ↓ [completion date]
Goal [###] (This Goal)        ← WE ARE HERE
  │ Duration: [weeks]
  │ Critical: Yes/No - if we slip, [impact on dependent goals]
  ↓ [completion date]
Goal [###] (Dependent)
  │ Duration: [weeks]
  ↓ [completion date]
Launch / Completion
```

### Critical Path Impact

**If this goal slips by 1 week**:
- Goal [###] slips 1 week → overall timeline slips 1 week
- Goal [###] slips 3 days (can start early) → minimal impact
- Overall impact: **+1 week to launch**

**If this goal slips by 2 weeks**:
- Goal [###] must choose: slip 2 weeks OR use contingency plan
- Goal [###] can only proceed with fallback approach
- Overall impact: **+2 weeks to launch OR quality degraded**

**Mitigation**:
- Buffer time: [This goal has X weeks buffer]
- Parallel work: [These tasks can run in parallel with blocking goal]
- Fallback: [If blocker slips, we can use contingency]

---

## Handoff Points

### Handoff 1: [From Goal X to This Goal]

**Handoff date**: [Date]  
**Handoff from**: [Goal X, Team A]  
**Handoff to**: [This Goal, Team B]  
**What's being handed off**: [Specific deliverable - code, design, spec, etc.]

**Before handoff (1 week prior)**:
- [ ] Handoff item is [% complete]
- [ ] Documentation being prepared
- [ ] Receiving team identified and ready
- [ ] Questions from receiving team gathered

**At handoff**:
- [ ] Deliverable complete and meets acceptance criteria (see below)
- [ ] Documentation provided
- [ ] Handoff reviewed and approved
- [ ] Issue tracking transferred (if applicable)

**Acceptance Criteria**:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]
- [ ] [Specific criterion 3]

**Post-handoff support**:
- Sending team available for questions: [1 week / 2 weeks / duration]
- Contact person: [Name]
- Response time: [Same day / next day]

---

### Handoff 2: [From This Goal to Goal Y]

**Handoff date**: [Date]  
**Handoff from**: [This Goal, Team B]  
**Handoff to**: [Goal Y, Team C]  
**What's being handed off**: [Specific deliverable]

**Before handoff (1 week prior)**:
- [ ] Deliverable [% complete]
- [ ] Documentation being prepared
- [ ] Receiving team identified
- [ ] Questions gathered

**At handoff**:
- [ ] Deliverable complete and meets acceptance criteria
- [ ] Documentation provided
- [ ] Handoff reviewed and approved
- [ ] Issue tracking transferred

**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Post-handoff support**:
- Team available for questions: [duration]
- Contact: [Name]
- Response time: [SLA]

---

## Synchronization Points

### During Execution, Teams Coordinate At:

| Date/Milestone | Teams | Purpose | Sync Type | Contact |
|---|---|---|---|---|
| [Milestone 1 completion] | This + Dependent | M1 approval + M2 kickoff | Async doc + call if issues | [Owner] |
| [Mid-Milestone 2] | This + Blocker | Progress check + help identify risks | Async update | [Owner] |
| [Milestone 2 completion] | This + Dependent | Handoff preparation | Async doc | [Owner] |

### Sync Exceptions (Real-Time Discussion Needed)

**When**:
- Critical blocker identified
- Handoff failing acceptance criteria
- Scope change requested
- Emergency issue affecting dependent goal

**Who**: Affected goal owners + escalation contact  
**Format**: Slack + phone call same day  
**Timeline**: Resolve within 24 hours

---

## Risk Cascades

### If Blocker Goal Slips

**Scenario**: Goal [###] slips 2 weeks

**Impact on this goal**:
- We can't start M1 until [new date]
- We shift timeline by 2 weeks
- We now have [X] weeks to complete instead of [Y]

**Mitigation**:
- Option 1: Start with [partial approach] while blocker completes
- Option 2: Add resources to compress timeline
- Option 3: Accept 2-week slip to launch
- Recommended: [Which option]

---

### If This Goal Slips

**Scenario**: This goal slips 1 week

**Impact on dependent goals**:
- Goal [###] can't start until [new date] (slips 1 week)
- Goal [###] can use contingency and start on [alternative date]
- Overall impact: **+1 week OR quality trade-off**

**Impact on overall launch**:
- Launch date moves from [original] to [new date]
- Revenue impact: [X impact]
- Market impact: [Y impact]

**Mitigation**:
- Early warning: Flag at first sign of risk (don't wait)
- Add resources: [Can we add 1-2 people?]
- Reduce scope: [What can we defer to v2?]
- Parallel path: [Can dependent goals proceed anyway?]

---

### If Multiple Goals Slip

**Scenario**: Both blocker and this goal slip 1 week each

**Cascade effect**:
- Blocker slips 1 week → this goal delayed 1 week
- This goal also slips 1 week internally
- Total impact: +2 weeks to dependent goals
- Total impact: +2 weeks to launch

**Mitigation**:
- Have fallback for each blocker
- Buffer time in critical path
- Escalate immediately if 2+ goals at risk

---

## Contingency Plans

### If Blocker Goal [###] Slips 2+ Weeks

**Current plan**: Wait for Goal [###]'s [deliverable] and integrate

**Contingency plan**:
1. Start with [simplified/mock version] of deliverable
2. [Team X] builds [simplified approach] in parallel
3. [When blocker completes, integrate real version]
4. Timeline impact: **-[X weeks] (only 1 week slip instead of 2)**

**Trigger for contingency**: If Goal [###] is at-risk by [date]

**Owner**: [Who owns contingency execution?]

---

### If This Goal Slips, Dependent Goals Options

**Goal [###] options if we slip**:

| Slip Duration | Option 1 | Option 2 | Option 3 |
|---|---|---|---|
| 1 week | Use [fallback] and delay 1 week | Parallel path with [mock deliverable] | Slip to next quarter |
| 2 weeks | Fallback only option | Use mock + rework later | Defer to next quarter |
| 3+ weeks | Defer to next quarter | Use mock (accept quality risk) | Cancel goal |

---

## Owner Alignment

### Team Awareness

- [ ] Blocking goal owner: [Name] - aware of timeline + contingency
- [ ] This goal owner: [Name] - understands impact on dependents
- [ ] Dependent goal owner #1: [Name] - aware of handoff + timeline
- [ ] Dependent goal owner #2: [Name] - aware of fallback options
- [ ] Cross-team sync contact: [Name] - coordinates any issues
- [ ] Escalation path: [Name] - final authority on conflicts

### Sign-Off

**Blocking goal owner**: [Name] - confirms timeline realistic  
**Date**: [Date]

**This goal owner**: [Name] - confirms dependencies mapped  
**Date**: [Date]

**Dependent goal owner #1**: [Name] - confirms contingency acceptable  
**Date**: [Date]

**Dependent goal owner #2**: [Name] - confirms contingency acceptable  
**Date**: [Date]

---

## Related Documents

- `templates/async-coordination-template.md` - Async communication patterns
- `templates/team-roles-template.md` - Role definitions and RACI
- `portfolio.md` - See all goals and dependencies
- `execution.md` - This goal's execution plan
