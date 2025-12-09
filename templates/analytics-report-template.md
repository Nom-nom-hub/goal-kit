# Analytics Report Template

**Goal**: [GOAL_NAME] (Goal ID: ###)
**Report Date**: [DATE]
**Reporting Period**: [START_DATE] to [END_DATE]
**Report Type**: [Weekly/Monthly/Completion]

---

## 📊 Executive Summary

One-paragraph summary of progress and status.

**Example**:
> Goal "Improve API Performance" is on track with 67% completion (8 of 12 tasks). Team velocity is steady at 3.2 tasks/week. One infrastructure blocker identified but being resolved. Expected completion: January 24 (3 days early). No actions required unless blocker escalates.

**Your Summary**:
[Write 2-3 sentences covering: completion %, velocity status, blockers, risk level, expected outcome]

---

## 📉 Progress Visualization

### Burndown Chart

```
Tasks Remaining
     12 │
     10 │     ╱
      8 │    ╱
      6 │   ╱
      4 │  ╱
      2 │ ╱
      0 └──────────────► Days
        0  5  10  15
```

**Current Status**:
- Tasks Completed: [X of Y] ([%]%)
- Ideal Pace: [X] tasks/week
- Actual Pace: [X] tasks/week
- Position: [Ahead/On Track/Behind] by [X] tasks

**Interpretation**: [1-2 sentences explaining what the chart means]

---

## 📈 Velocity Analysis

### Weekly Breakdown

| Week | Tasks Completed | Velocity | Trend |
|------|-----------------|----------|-------|
| Week 1 | [X] | [X] tasks/week | - |
| Week 2 | [X] | [X] tasks/week | [↑/→/↓] |
| Week 3 | [X] | [X] tasks/week | [↑/→/↓] |
| Week 4 | [X] | [X] tasks/week | [↑/→/↓] |

**Average Velocity**: [X] tasks/week
**Trend**: [Increasing/Stable/Declining] by [X] tasks/week
**Confidence (R²)**: [X] ([High/Moderate/Low] - [X]%)

**Interpretation**:
[1-2 sentences explaining velocity pattern and what it means for deadline]

**Example**:
> Velocity has declined from 4 tasks/week (Week 1) to 2 tasks/week (Week 4), with R²=0.78 (high confidence). This 50% decline suggests a structural issue (blockers, fatigue, or scope creep) that needs investigation.

---

## 🔮 Forecast & Timeline

### Completion Prediction

**Target Deadline**: [DATE]
**Predicted Completion**: [DATE]
**Days to Completion**: [X] days

**Confidence Intervals**:
- 10% confidence (optimistic): [DATE] ([X] days early/late)
- 50% confidence (likely): [DATE] ([X] days early/late)
- 90% confidence (pessimistic): [DATE] ([X] days early/late)

**Risk Assessment**: [ON TRACK ✅ / AT RISK ⚠️ / CRITICAL 🚨]

**Rationale**:
[Explain how forecast was calculated and confidence level]

**Example**:
> With current velocity of 2.5 tasks/week and 8 tasks remaining, we need 3.2 weeks. Adding to today's date (Jan 15) yields Jan 30 as 50% forecast. However, R²=0.65 (moderate confidence) due to high week-to-week variance. Planning for 90% confidence (Feb 6) is recommended given deadline risk.

---

## 🚧 Blockers & Bottlenecks

### Identified Blockers

| Blocker | Affected Tasks | Duration | Impact | Status |
|---------|----------------|----------|--------|--------|
| [BLOCKER_NAME] | [TASK_NAMES] | [X days] | [X days delay] | [Open/Escalated/Resolved] |
| [BLOCKER_NAME] | [TASK_NAMES] | [X days] | [X days delay] | [Open/Escalated/Resolved] |

**Total Impact**: [X] tasks stalled, [X] days of productivity lost

### Blocker Details

#### Blocker 1: [NAME]
- **Cause**: [What's blocking progress]
- **Affected Tasks**: [Which tasks are waiting]
- **Duration**: [How long blocked]
- **Severity**: [High/Medium/Low]
- **Resolution Path**: [How we're fixing it]
- **Owner**: [Who's responsible]
- **Target Unblock Date**: [DATE]

**Example**:
> **Blocker 1: Design Review Delay**
> - **Cause**: Design team backlog, high priority items blocking our reviews
> - **Affected Tasks**: API endpoint specifications (2 tasks)
> - **Duration**: 5 days
> - **Severity**: High (blocks 40% of remaining work)
> - **Resolution Path**: Escalated to design manager, pre-approval of specs requested
> - **Owner**: Engineering manager
> - **Target Unblock Date**: Jan 18

---

## 💡 Automated Insights

### Key Patterns Identified

**Pattern 1: [PATTERN_NAME]**
- **What**: [Describe the pattern observed in data]
- **Impact**: [How this affects the project]
- **Recommendation**: [What to do about it]

**Pattern 2: [PATTERN_NAME]**
- **What**: [Describe the pattern]
- **Impact**: [How this affects the project]
- **Recommendation**: [What to do about it]

**Example Patterns**:
> **Pattern 1: Tuesday-Wednesday Productivity Peak**
> - **What**: Tasks completed on Tues/Wed average 1.8 tasks/day vs 0.9 tasks/day other days
> - **Impact**: 50% variance in daily output makes short-term planning difficult
> - **Recommendation**: Schedule risky/complex tasks for peak days, routine work for other days

> **Pattern 2: Design Review Bottleneck**
> - **What**: 4 of 5 blocked tasks waiting on design feedback (average 4 days per review)
> - **Impact**: Design reviews are critical path item, blocking 35% of work
> - **Recommendation**: Implement pre-approval process or parallel design reviews

### Status Summary

| Category | Status | Color |
|----------|--------|-------|
| **Progress** | [On Track/Behind/Ahead] | ✅/⚠️/🚨 |
| **Velocity** | [Stable/Increasing/Declining] | ✅/⚠️/🚨 |
| **Blockers** | [None/Minor/Major] | ✅/⚠️/🚨 |
| **Deadline** | [Safe/At Risk/Critical] | ✅/⚠️/🚨 |

---

## 🎯 Decision Points

### Continue Current Approach?

**Recommendation**: [YES / NO / WITH CONDITIONS]

**Rationale**: [Why continue or why change approach]

**Conditions (if applicable)**:
1. [Condition 1 that must be true]
2. [Condition 2 that must be true]
3. [Condition 3 that must be true]

**Example - Continue**:
> **Recommendation**: YES - Continue current approach
> 
> **Rationale**: 
> - Velocity stable at 3.2 tasks/week (meets forecast requirements)
> - No critical blockers (design delay is on track for resolution)
> - 90% forecast (Jan 24) safely within deadline (Jan 31)
> - Team morale and quality both high
>
> **Conditions**: 
> 1. Infrastructure blocker must be resolved by Jan 18
> 2. Design review cycle must stay ≤4 days
> 3. No unplanned scope additions

**Example - Adjust Tactics**:
> **Recommendation**: YES but ADJUST TACTICS
> 
> **Rationale**:
> - Velocity declining (3 week downtrend, R²=0.72)
> - Infrastructure blocker still unresolved after 5 days
> - 90% forecast (Feb 6) now 6 days late
> - Trend unsustainable if continues
>
> **Actions Required**:
> 1. Escalate infrastructure blocker to manager (target 2 days)
> 2. Pre-approve design specs to reduce review cycle
> 3. Re-forecast after blockers resolved
> 4. If velocity doesn't recover, consider scope reduction

**Example - Pivot**:
> **Recommendation**: NO - Consider Pivot
> 
> **Rationale**:
> - Velocity declining sharply (50% drop, R²=0.81 high confidence)
> - Multiple fundamental blockers (Design, Infra, unknown unknowns)
> - 90% forecast (Feb 20) now 20 days late
> - Team fatigue evident from comments in daily standups
> - Current strategy not working
>
> **Options**:
> 1. **Tactical Pivot**: Different execution order (defer low-priority tasks)
> 2. **Strategic Pivot**: Try Strategy #2 (simpler approach, fewer dependencies)
> 3. **Scope Pivot**: Reduce success criteria (80% instead of 95% for core metric)
>
> **Recommendation**: Strategic Pivot - Try Strategy #2 with simplified scope
> **Next Step**: Call `/goalkit.strategies` to revisit approach

---

## 📋 Recommended Actions

### Immediate (This Week)

- [ ] **Action 1**: [Description] - Owner: [WHO] - Target: [DATE]
- [ ] **Action 2**: [Description] - Owner: [WHO] - Target: [DATE]
- [ ] **Action 3**: [Description] - Owner: [WHO] - Target: [DATE]

**Example Immediate Actions**:
- [ ] **Escalate Design Blocker**: Contact design manager, request pre-approval process - Owner: PM - Target: Today
- [ ] **Re-plan Infrastructure Work**: Break into smaller pieces, parallelize - Owner: Tech Lead - Target: Jan 17
- [ ] **Team Retrospective**: Understand velocity decline root cause - Owner: Manager - Target: Jan 18

### This Sprint

- [ ] **Action 1**: [Description] - Owner: [WHO] - Target: [DATE]
- [ ] **Action 2**: [Description] - Owner: [WHO] - Target: [DATE]

**Example Sprint Actions**:
- [ ] **Monitor Unblock**: Verify blockers resolved on schedule
- [ ] **Velocity Check**: Run `/goalkit.velocity` mid-sprint to catch new declines early

### Next Review Period

- [ ] **Action 1**: [Description]
- [ ] **Action 2**: [Description]

---

## 📊 Metrics Summary

### Goal Success Criteria Tracking

| Criteria | Baseline | Target | Current | % Complete | Status |
|----------|----------|--------|---------|------------|--------|
| [SC-1] | [BASELINE] | [TARGET] | [CURRENT] | [%] | [✅/⚠️/🚨] |
| [SC-2] | [BASELINE] | [TARGET] | [CURRENT] | [%] | [✅/⚠️/🚨] |
| [SC-3] | [BASELINE] | [TARGET] | [CURRENT] | [%] | [✅/⚠️/🚨] |

**Example**:
| Criteria | Baseline | Target | Current | % Complete | Status |
|----------|----------|--------|---------|------------|--------|
| API Response Time (p95) | 450ms | <200ms | 220ms | 92% | ✅ |
| Error Rate | 0.5% | <0.1% | 0.12% | 88% | ✅ |
| User Satisfaction | 6.2/10 | ≥8.0/10 | 7.8/10 | 97% | ✅ |

---

## 🔗 Related Documents

- **Goal**: `.goalkit/goals/[###]/goal.md` - Original goal definition
- **Strategies**: `.goalkit/goals/[###]/strategies.md` - Implementation approach
- **Milestones**: `.goalkit/goals/[###]/milestones.md` - Progress checkpoints
- **Execution**: `.goalkit/goals/[###]/execution.md` - Current execution plan
- **Analytics Data**: `.goalkit/analytics_history.json` - Raw analytics snapshots

---

## 📝 Notes

[Any additional context, decisions, or observations]

**Example Notes**:
> - Team working well together, morale high
> - Infrastructure team very responsive despite being blocked
> - Consider frontend performance optimization for future goals
> - Design feedback loop was critical path - invest in parallelization

---

## ✅ Next Steps

1. **Review & Discuss**: Share this report with stakeholders
2. **Action Planning**: Assign owners to recommended actions
3. **Monitor**: Check progress daily on critical items
4. **Re-report**: [When is next analytics report due? After next milestone? Weekly?]

**Next Report Due**: [DATE]
**Next Checkpoint**: [MILESTONE / DATE]

---

*Report Generated*: [AUTO-GENERATED by `/goalkit.insights` and `/goalkit.forecast`]
*Template Version*: 1.0
*Reference Guide*: [See `docs/analytics-guide.md` for interpretation help]
