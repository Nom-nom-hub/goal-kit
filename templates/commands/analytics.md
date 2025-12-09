# Analytics Command Guide

## Purpose

Use `/goalkit.analytics` commands to visualize project progress, analyze velocity trends, forecast completion dates, and identify bottlenecks preventing goal achievement.

These commands transform raw execution data into actionable insights for data-driven decision making.

## When to Use

| Situation | Command | Frequency |
|-----------|---------|-----------|
| 🔥 Need immediate project status | `/goalkit.burndown` | Daily during execution |
| 📈 Track team velocity trends | `/goalkit.velocity` | Weekly reviews |
| 🔮 Predict completion date | `/goalkit.forecast` | After each milestone |
| 📊 Analyze trend patterns | `/goalkit.trends` | Weekly retrospectives |
| 💡 Get automated insights | `/goalkit.insights` | Before pivot decisions |

## Command Reference

### `/goalkit.burndown [--goal GOAL_ID]`

**Purpose**: Visualize progress with ASCII burndown chart showing completed vs total tasks

**When to use**:
- Daily status check during execution
- Identify if you're on track
- Spot stalled progress patterns
- Communicate progress to stakeholders

**Outputs**:
```
Burndown for Goal: Improve API Performance
════════════════════════════════════════
Tasks Completed: 8 of 12 (67%)

Progress Chart:
█████████░░░░░░░░░░ 50%

Timeline:
Plan Start:   2025-01-15
Target End:   2025-02-15  
Days Elapsed: 20 / 31 days
Est. Completion: 2025-02-20 (5 days over)
```

**Example**:
```bash
/goalkit.burndown --goal 001

# Expected: ASCII burndown chart with task counts
```

**Interpretation**:
- Chart below diagonal = ahead of schedule ✅
- Chart above diagonal = behind schedule ⚠️
- Flat sections = no progress (stalled) 🚨

---

### `/goalkit.velocity [--weeks 4] [--goal GOAL_ID]`

**Purpose**: Calculate and trend your completion velocity (tasks/week)

**When to use**:
- Weekly team meetings
- Forecasting remaining work
- Identifying slowdowns
- Capacity planning

**Outputs**:
```
Velocity Analysis for Goal: Improve API Performance
════════════════════════════════════════════════════

Velocity by Week:
Week 1: 3 tasks/week
Week 2: 4 tasks/week
Week 3: 2 tasks/week  ← Slowdown detected
Week 4: 3 tasks/week

Average Velocity: 3.0 tasks/week
Trend: Slightly declining (-0.2 tasks/week)
```

**Example**:
```bash
/goalkit.velocity --goal 001 --weeks 4

# Expected: Weekly completion rates and trend
```

**Interpretation**:
- Consistent velocity = predictable delivery ✅
- Declining velocity = blockers emerging ⚠️
- Increasing velocity = team hitting stride ✅

---

### `/goalkit.trends [--goal GOAL_ID]`

**Purpose**: Linear regression analysis identifying the underlying trend direction

**When to use**:
- Spotting patterns you can't see in raw data
- Deciding if current trend is sustainable
- Planning adjustment strategies
- Reporting to stakeholders

**Outputs**:
```
Trend Analysis for Goal: Improve API Performance
═════════════════════════════════════════════════

Trend Direction: Slightly positive (+0.3 tasks/week)
Confidence (R²): 0.72 (Moderate - watch for changes)

Forecast (if trend continues):
- Current pace: Will complete in 14 days
- Confidence: 70% likely to be accurate
- Risk factors: Blockers may accelerate decline
```

**Example**:
```bash
/goalkit.trends --goal 001

# Expected: Linear trend analysis with confidence
```

**Interpretation**:
- High R² (0.8+) = Trend is reliable ✅
- Low R² (<0.5) = Trend is unreliable ⚠️ (plan conservatively)
- Negative trend = Will miss deadline unless course corrects 🚨

---

### `/goalkit.forecast [--goal GOAL_ID] [--deadline DATE]`

**Purpose**: Predict completion date with confidence intervals based on velocity

**When to use**:
- Deadline commitments
- Before reporting to stakeholders
- Deciding if pivot/scope reduction needed
- Risk assessment

**Outputs**:
```
Completion Forecast for Goal: Improve API Performance
══════════════════════════════════════════════════════

Target Deadline: 2025-02-15
Predicted Completion: 2025-02-10 (5 days early) ✅
Confidence Intervals:
  10% chance: Completed by 2025-02-08
  50% chance: Completed by 2025-02-10
  90% chance: Completed by 2025-02-20

Risk Assessment: ON TRACK ✅
Required Velocity: 2.5 tasks/week (achieving 3.0)
```

**Example**:
```bash
/goalkit.forecast --goal 001 --deadline 2025-02-15

# Expected: Completion date prediction with confidence bands
```

**Interpretation**:
- Early prediction = On track or ahead ✅
- Late prediction = At risk or critical 🚨
- Wide confidence band = High uncertainty ⚠️ (plan conservatively)

**Confidence Interval Meanings**:
- **10% Confidence**: Best-case scenario (rare)
- **50% Confidence**: Most likely outcome
- **90% Confidence**: Worst-case scenario (plan for this)

---

### `/goalkit.insights [--goal GOAL_ID]`

**Purpose**: Automated analysis identifying patterns, blockers, and recommendations

**When to use**:
- Before decision points (pivot vs continue)
- After major milestone completion
- When progress stalls or surprises
- Retrospective analysis

**Outputs**:
```
Automated Insights for Goal: Improve API Performance
════════════════════════════════════════════════════

📊 Progress Pattern
- Completion: 67% of tasks
- Velocity: 3.0 tasks/week (normal for team)
- On Track: Yes, 5 days early

🚧 Blockers Identified
- 3 tasks blocked by infrastructure team
- 1 task waiting for design review
- Blocked duration: 5 days average

💡 Recommendations
1. Unblock infrastructure tasks (2 days gain)
2. Prioritize design review (1 day gain)
3. Continue current pace - velocity sustainable

⚠️ Risks
- No technical blockers yet
- Design feedback may impact timeline
- Team capacity stable

✅ What's Going Well
- Team velocity consistent
- Early detection of blockers
- Good progress on core features
```

**Example**:
```bash
/goalkit.insights --goal 001

# Expected: Automated analysis with patterns and recommendations
```

**Interpretation**:
- Green insights = Continue current approach ✅
- Yellow insights = Monitor and adjust ⚠️
- Red insights = Immediate action needed 🚨

---

## Integration with Other Commands

**After each milestone**, run analytics to inform next steps:

```bash
# 1. Milestone completed
/goalkit.milestones --update

# 2. Check progress
/goalkit.burndown --goal 001

# 3. Predict timeline
/goalkit.forecast --goal 001 --deadline [DATE]

# 4. Get insights
/goalkit.insights --goal 001

# 5. Decide: Continue? Adjust? Pivot?
# If decision needed:
/goalkit.strategies --revisit 001
# If all going well:
/goalkit.execute --continue 001
```

## Common Questions

### Q: What if burndown chart looks bad?
**A**: Use `/goalkit.insights` to identify blockers, then:
- Are blockers fixable quickly? → Unblock and continue
- Are blockers fundamental? → Explore new strategies via `/goalkit.strategies`
- Is scope too large? → Consider scope reduction scenario in `/goalkit.forecast`

### Q: How do I know if velocity is normal?
**A**: Compare to:
- Team's historical velocity (from previous goals)
- Industry benchmarks for similar work
- Your own forecast requirements

If lower than needed: use `/goalkit.forecast` scenario analysis to explore options.

### Q: Should I trust the forecast?
**A**: Only if:
- R² confidence is ≥0.7 (see `/goalkit.trends`)
- Sample size is ≥2 weeks (not enough data yet)
- Conditions haven't changed dramatically

If low confidence: plan conservatively using 90% confidence interval.

### Q: When should I pivot based on analytics?
**A**: Use this decision tree:

```
Check /goalkit.insights
├─ All green → Continue current approach
├─ Yellow items → Investigate, don't change yet
└─ Red items with no fix
   ├─ Can unblock in <1 day → Unblock and continue
   ├─ Strategic issue → Explore new strategies
   ├─ Scope issue → Consider scope reduction
   └─ Deadline issue → Re-negotiate or reduce scope
```

## Data Files

Analytics data persists in `.goalkit/analytics_history.json`:
- Daily snapshots: date, completed tasks, total tasks, blocked count, in-progress count
- Used for trending and forecasting
- Automatically maintained (don't edit manually)

## Pro Tips

1. **Run `/goalkit.burndown` daily** during active execution for early warning signals
2. **Run `/goalkit.velocity` weekly** to catch trend shifts before they affect deadline
3. **Run `/goalkit.forecast` after major blockers** to update stakeholder expectations
4. **Use insights as decision trigger** - don't ignore red insights
5. **Trust the trend, not a single data point** - changes matter when consistent

## See Also

- [Webhooks](./webhooks.md) - Automate actions based on analytics thresholds
- [Report](./report.md) - Generate formal progress reports with analytics data
- [Review](./review.md) - Retrospective analysis after goal completion
- [Analytics Guide](../analytics-guide.md) - Detailed interpretation guide
