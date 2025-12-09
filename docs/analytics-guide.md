# Analytics Guide - Interpreting Goal Kit Data

## Overview

Goal Kit analytics transforms task completion data into actionable insights. This guide helps you understand each metric and make data-driven decisions.

## Core Metrics

### Burndown Chart

**What it shows**: Visual representation of task completion over time

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

**Interpretation**:
- **Diagonal line**: Ideal pace (if you complete 1 task per day)
- **Line below diagonal**: Ahead of schedule ✅
- **Line above diagonal**: Behind schedule ⚠️
- **Flat sections**: No progress, stalled work 🚨

**How to read it**:
```
Current: 8 of 12 tasks (67%)
Timeline: 15 days elapsed of 20-day plan
Ideal pace: Should be ~10 tasks by now
Actual: 8 tasks
Status: 2 tasks behind (but recoverable)
```

**When to act**:
- 1-2 tasks behind = Keep monitoring, adjust if gap grows
- 3+ tasks behind = Investigate blockers with `/goalkit.insights`
- Flat line for >2 days = Immediate escalation needed

### Velocity

**What it shows**: How many tasks your team completes per week

```
Velocity Trend:
Week 1: 3 tasks/week
Week 2: 4 tasks/week  ← increasing
Week 3: 4 tasks/week
Week 4: 2 tasks/week  ← declining (investigate!)
```

**Interpretation**:
- **Increasing velocity**: Team hitting stride, getting faster ✅
- **Consistent velocity**: Predictable delivery, plan with confidence ✅
- **Declining velocity**: Blockers, fatigue, or scope creep ⚠️

**What to do**:
- Increasing: Celebrate! You can accelerate timeline if needed
- Consistent: Use this for accurate forecasting
- Declining: Run `/goalkit.insights` to find blockers

**Note**: Velocity naturally varies by week - only be concerned if 3+ week downtrend

### Trend Analysis (Linear Regression)

**What it shows**: The underlying direction of your progress

```
Raw Data:     [2, 3, 2, 4, 3, 3]
Trend Line:   Slightly positive +0.2 tasks/week
Confidence:   R² = 0.68 (moderate)
```

**Understanding Confidence (R²)**:
- **0.8+** (High): Trend is very reliable, use for forecasting ✅
- **0.5-0.8** (Moderate): Trend exists but has noise, be careful ⚠️
- **<0.5** (Low): Trend unreliable, plan conservatively 🚨

**Example interpretations**:

```
Scenario 1: +0.3 tasks/week, R²=0.85
→ Strong upward trend, accelerating delivery likely
→ Action: Can reduce timeline estimate

Scenario 2: 0.0 tasks/week, R²=0.92
→ Flat progress, very predictable
→ Action: Use current velocity for reliable forecast

Scenario 3: -0.5 tasks/week, R²=0.73
→ Declining trend, velocity dropping
→ Action: Investigate blockers before forecasting
```

### Completion Forecast

**What it shows**: Predicted completion date based on current velocity

```
Model: Linear extrapolation from recent velocity
Today: Jan 15 (8 of 12 tasks done)
Velocity: 3 tasks/week
Remaining: 4 tasks
Time needed: 4 ÷ 3 = 1.33 weeks = 9 days

Prediction: Jan 24
Confidence interval:
  10%: Jan 22 (optimistic)
  50%: Jan 24 (most likely)
  90%: Jan 28 (pessimistic, plan for this)
```

**Confidence Intervals Explained**:

| Interval | Meaning | When to Use |
|----------|---------|------------|
| **10%** | Best-case, rare | Recognition only |
| **50%** | Most likely outcome | Internal commitments |
| **90%** | Worst-case, plan for | External commitments |

**Example decision-making**:
```
Deadline: Jan 26
50% forecast: Jan 24 ✅ Can promise
90% forecast: Jan 28 ⚠️ Too risky to promise

Decision: Either reduce scope or extend deadline
```

### Deadline Risk

**What it shows**: Whether you'll hit your deadline

```
Scenarios:
- On Track:  Likely to complete before/by deadline ✅
- At Risk:   Might miss deadline (50/50 chance)      ⚠️
- Critical:  Very likely to miss deadline            🚨
```

**Risk determination**:
```
Required pace: 4 tasks / 10 days = 0.4 tasks/day
Current pace: 3 tasks / week = 0.43 tasks/day
Status: ON TRACK (barely - monitor closely)

vs. Deadline-critical example:
Required: 10 tasks / 5 days = 2.0 tasks/day
Current: 3 tasks / week = 0.43 tasks/day
Status: CRITICAL (miss by 2 weeks)
```

**Actions by risk level**:

| Risk | Action |
|------|--------|
| ON TRACK | Continue, no changes needed |
| AT RISK | Reduce scope OR reduce deadline OR add resources |
| CRITICAL | Immediate action: major scope cut OR extend deadline OR both |

### Bottleneck Detection

**What it shows**: What's blocking progress

```
Blockers Identified:
├─ 3 tasks blocked by Infrastructure team (avg 5 days blocked)
├─ 1 task waiting for Design review (2 days blocked)
├─ 2 tasks blocked on each other (circular dependency)
└─ Network outages (3 hours downtime)

Impact: 5 tasks stalled, 7 days of productivity lost
```

**Types of blockers**:
- **Dependency blocks**: Task can't start until another finishes
- **External blocks**: Waiting on another team (design, infra, etc)
- **Technical blocks**: Missing tools, libraries, or knowledge
- **Resource blocks**: Team member unavailable

**How to respond**:
1. Quantify impact (days of delay)
2. Prioritize by impact (highest impact first)
3. Try to unblock (can it be fixed in <1 day?)
4. If unblockable, consider scope reduction in that area

### Automated Insights

**What it shows**: Pattern analysis and recommendations

```
📊 Pattern: Productivity peaks on Tuesday-Wednesday
💡 Recommendation: Schedule high-risk work for peak days

⚠️  Pattern: Design review takes average 3 days
💡 Recommendation: Request pre-approval to reduce wait time

✅ Pattern: Bug fixes average 4 hours, features average 2 days
💡 Recommendation: Batch smaller bugs for efficiency

🚨 Pattern: Tasks blocked for >3 days rarely get unblocked
💡 Recommendation: Escalate blocked items to manager within 2 days
```

---

## Decision Framework

### When to Continue Current Approach

✅ **Continue if**:
- Burndown chart tracking below diagonal (ahead)
- Velocity consistent and predictable
- R² trend confidence ≥ 0.7
- 90% forecast ≤ deadline
- No blockers lasting >3 days
- Automated insights all green

### When to Adjust Tactics

⚠️ **Adjust if**:
- Burndown above diagonal but gap <2 days
- Velocity declining but >75% of needed
- Some yellow insights (blockers)
- 90% forecast ≤ 5 days after deadline

**Adjustment options**:
1. Unblock stalled tasks (highest impact first)
2. Reduce scope of low-priority features
3. Shift resources to critical path
4. Parallelize dependent tasks

**Example**:
```
Status: 2 tasks behind, 10 days left, 4 tasks remaining
Velocity: 2.5 tasks/week (need 2.8 tasks/week)

Option 1: Unblock 1 task blocked by Design
  → Gain 1 day, back on track
  
Option 2: Reduce scope (defer 1 feature)
  → 3 remaining tasks, 1.5 tasks/week needed, safely ahead

Option 3: Extend deadline 4 days
  → Comfortable 2.5 tasks/week pace

Decision: Implement Options 1 + 2 for safety
```

### When to Pivot

🔴 **Pivot if**:
- Burndown gap growing (3+ days behind)
- Velocity declining >2 weeks with R² ≥ 0.7
- Blockers blocking critical path tasks
- 90% forecast ≥ 2 weeks after deadline
- Multiple red insights

**Pivot options**:
1. **Tactical pivot**: Different execution approach (different tools, order, team)
2. **Strategic pivot**: Different strategy (try Strategy #2 or #3)
3. **Goal pivot**: Reframe the goal (easier success criteria, longer timeline)

**Decision tree**:
```
Multiple blockers?
├─ YES, can unblock in 1 day
│   → Adjust tactics, unblock
├─ YES, fundamental issue
│   → Review Strategy #2/#3, may need strategic pivot
└─ NO
    └─ Velocity declining?
       ├─ YES, fundamental skill gap
       │   → Goal pivot (easier success criteria)
       └─ NO, just behind on pace
           → Adjust tactics, add resources or cut scope
```

---

## Common Analysis Scenarios

### Scenario 1: Ahead of Schedule

```
Burndown: 2 tasks ahead
Velocity: 4 tasks/week (target: 3)
Trend: +0.2 tasks/week
Forecast: 3 days early
Status: ✅ ON TRACK

Decision Options:
1. Accelerate: Add stretch goals or next features
2. Quality focus: Add more testing, refinement
3. Buffer: Maintain current pace, reduce risk

Recommendation: Quality focus - lock in what works
```

### Scenario 2: Exactly on Pace

```
Burndown: On diagonal
Velocity: 3 tasks/week (consistent)
Trend: 0.0 tasks/week (flat, R²=0.88)
Forecast: On deadline
Status: ✅ ON TRACK

Decision: Continue current approach, monitor for blockers
```

### Scenario 3: Slightly Behind, Recoverable

```
Burndown: 1-2 tasks behind
Velocity: 2.5 tasks/week (need 2.8)
Trend: Slightly declining (-0.1, R²=0.65)
Forecast: 3 days late
Blockers: 1 task waiting on Design
Status: ⚠️  AT RISK

Actions:
1. Immediate: Escalate Design bottleneck (1 day gain)
2. This week: Cut 1 low-priority task from scope
3. Monitor: Run insights daily until back on track

Expected: Back on track within 5 days
```

### Scenario 4: Significantly Behind, Intervention Needed

```
Burndown: 3+ tasks behind
Velocity: 1.5 tasks/week (need 3.5)
Trend: Declining -0.3 tasks/week (R²=0.78)
Forecast: 10 days late
Blockers: 4 tasks blocked (different teams)
Status: 🚨 CRITICAL

Actions:
1. Emergency unblock: Escalate all 4 blockers
2. Scope reduction: Cut 40% of remaining features
3. Re-negotiate: Extend deadline 1 week minimum
4. Team meeting: Diagnose root cause (skills? design? scope?)

Options:
- Option A: Cut scope (now feasible) + unblock (3 days catch-up)
- Option B: Extend deadline 2 weeks + unblock
- Option C: Both (safest, recommended)

DO NOT: Ignore metrics and hope for the best
```

### Scenario 5: Contradictory Signals

```
Burndown: Behind (8 of 12)
Velocity: Increasing (3 tasks week 3, 4 tasks week 4)
Trend: Positive +0.3 (R²=0.72)
Forecast: Actually on track!
Status: ✅ CATCHING UP

Explanation: Started slow but team accelerating
Action: Continue current pace, velocity trend is working

Wait for next data point: Is velocity sustainable?
```

---

## Anti-Patterns to Avoid

### ❌ Ignoring Burndown Chart

**Problem**: "We'll catch up at the end"

**Why it fails**: By the time you notice, too late to fix. Burndown shows daily status.

**Solution**: Check burndown **daily** during execution. Act within 2-3 days of slipping.

### ❌ Trusting Low-Confidence Forecasts

**Problem**: "R²=0.45 but we'll definitely make it"

**Why it fails**: Low confidence means data is unreliable. Optimism bias makes you overestimate.

**Solution**: Plan for 90% confidence interval, not 50% forecast. Be pessimistic when confidence is low.

### ❌ Dismissing Declining Velocity

**Problem**: "Week 4 was slow, but we'll accelerate in week 5"

**Why it fails**: Trends persist. If velocity declining for 3+ weeks with high R², it will continue.

**Solution**: Investigate cause immediately. Something structural changed (blocker, fatigue, scope creep).

### ❌ Not Acting on Insights

**Problem**: Insights say "unblock Design dependency" but you don't

**Why it fails**: Bottlenecks compound. Days become weeks.

**Solution**: Treat red insights as immediate action items.

### ❌ Adjusting Without Data

**Problem**: "I feel like we're behind, let's work weekends"

**Why it fails**: Might already be on track. Working weekends reduces next-week velocity.

**Solution**: Check metrics first. Data beats intuition.

### ❌ Hiding Behind Metrics

**Problem**: "Analytics say we're on track, so I won't communicate"

**Why it fails**: 50% forecast ≠ guaranteed. Stakeholders need context.

**Solution**: Share 90% forecast and explain confidence. Set expectations realistically.

---

## Quick Reference: When to Use Each Command

| Situation | Command | Frequency |
|-----------|---------|-----------|
| Daily status check | `/goalkit.burndown` | Every day |
| Weekly team meeting | `/goalkit.velocity` | Weekly |
| Spotting trends | `/goalkit.trends` | After each milestone |
| Deadline commitment | `/goalkit.forecast` | Before promising dates |
| Problem solving | `/goalkit.insights` | On stalls or surprises |
| Stakeholder update | `/goalkit.burndown` + `/goalkit.forecast` | Weekly |
| Pivot decision | `/goalkit.insights` + `/goalkit.trends` | On red indicators |

---

## Pro Tips

1. **Run `/goalkit.burndown` daily** - Makes trends visible early
2. **Trust the 90% forecast** - It accounts for uncertainty better than 50%
3. **Act within 2 days of slipping** - Delays compound quickly
4. **Combine metrics for decisions** - Don't trust one metric alone
5. **Document blockers** - Quantify impact for escalation
6. **Share insights with team** - They can unblock issues you can't

---

## See Also

- [Analytics Commands](../templates/commands/analytics.md) - Using the commands
- [Webhooks](../templates/commands/webhooks.md) - Automating actions based on metrics
- [Forecast Command Details](../templates/commands/analytics.md#goalkitforecast)
