# Analytics Report Generation Guide

## Purpose

Generate a comprehensive analytics report for a goal by automatically collecting data from all analytics commands, parsing results, and filling the analytics report template with real data.

**Result**: Complete `.goalkit/goals/[###]/analytics-report.md` with burndown, velocity, trends, forecast, and insights—ready for human review.

## When to Use

| Situation | Action |
|-----------|--------|
| 📊 Weekly progress review | Generate report |
| 🎯 Milestone completion | Generate report |
| 🔮 Deadline decision point | Generate report |
| ⚠️ Risk assessment needed | Generate report |
| 📝 Stakeholder communication | Generate report |

---

## Workflow Overview

```
Goal ID provided
    ↓
1. Run /goalkit.burndown → Extract chart data
    ↓
2. Run /goalkit.velocity → Extract velocity metrics
    ↓
3. Run /goalkit.trends → Extract trend analysis
    ↓
4. Run /goalkit.forecast → Extract completion prediction
    ↓
5. Run /goalkit.insights → Extract automated insights
    ↓
6. Parse all JSON outputs
    ↓
7. Fill analytics-report-template.md sections
    ↓
8. Save as .goalkit/goals/[###]/analytics-report.md
    ↓
Report generated ✅ (ready for human review)
```

---

## Step-by-Step Agent Workflow

### Step 1: Gather Report Metadata

**Determine**:
- `GOAL_ID`: Which goal to analyze (required)
- `REPORT_DATE`: Today's date
- `GOAL_NAME`: From goal.md

**Get Goal Info**:
```bash
# Read .goalkit/goals/[###]/goal.md
# Extract: Goal Name, Success Criteria
```

**Example**:
```
GOAL_ID = "001"
GOAL_NAME = "Improve API Performance"
REPORT_DATE = "2025-01-15"
```

---

### Step 2: Run Burndown Command

**Command**:
```bash
/goalkit.burndown --goal [GOAL_ID] --output json
```

**Parse JSON Output**:
```json
{
  "goal_id": "001",
  "dates": ["2025-01-01", "2025-01-02", ...],
  "ideal_remaining": [12, 11, 10, 9, ...],
  "actual_remaining": [12, 11, 9, 8, ...],
  "completed_count": [0, 1, 3, 4, ...]
}
```

**Fill Template Section**: `Progress Visualization → Burndown Chart`
```markdown
### Burndown Chart

[Generate ASCII art or simple text representation]

**Current Status**:
- Tasks Completed: [completed_count[-1]] of [ideal_remaining[0]] ([%]%)
- Ideal Pace: [tasks/week from dates]
- Actual Pace: [completed_count[-1] / days_elapsed] tasks/day
- Position: [Ahead/On Track/Behind] by [X] tasks
```

**Interpretation to write** (agent):
```markdown
**Interpretation**: [1-2 sentences explaining trend - 
is velocity on track? ahead? behind?]
```

---

### Step 3: Run Velocity Command

**Command**:
```bash
/goalkit.velocity --goal [GOAL_ID] --periods 4 --output json
```

**Parse JSON Output**:
```json
{
  "goal_id": "001",
  "periods": ["Week 1", "Week 2", "Week 3", "Week 4"],
  "tasks_completed": [4, 3, 2, 2],
  "average_velocity": 2.75,
  "trend": "declining",
  "momentum": -0.3
}
```

**Fill Template Section**: `Velocity Analysis → Weekly Breakdown`
```markdown
### Weekly Breakdown

| Week | Tasks Completed | Velocity | Trend |
|------|-----------------|----------|-------|
| Week 1 | 4 | 4 tasks/week | - |
| Week 2 | 3 | 3 tasks/week | ↓ |
| Week 3 | 2 | 2 tasks/week | ↓ |
| Week 4 | 2 | 2 tasks/week | → |

**Average Velocity**: 2.75 tasks/week
**Trend**: Declining by 0.3 tasks/week
**Confidence (R²)**: [Get from trends command - see Step 4]
```

**Interpretation to write** (agent):
```markdown
**Interpretation**: [1-2 sentences explaining velocity pattern]
```

---

### Step 4: Run Trends Command

**Command**:
```bash
/goalkit.trends --goal [GOAL_ID] --output json
```

**Parse JSON Output**:
```json
{
  "goal_id": "001",
  "slope": -0.3,
  "intercept": 4.2,
  "r_squared": 0.78,
  "direction": "negative",
  "velocity_change": -0.3,
  "momentum_score": -2.1
}
```

**Fill Template Section**: `Velocity Analysis → Summary`
```markdown
**Confidence (R²)**: 0.78 (High - 78% of variance explained)
```

**Update Step 3 Velocity Analysis** with R² value.

**Interpretation to write** (agent):
```markdown
**Interpretation**: [Explain what R² means for this trend. 
If R²=0.78: "High confidence in declining trend"
If R²=0.35: "Low confidence - be cautious with predictions"
]
```

---

### Step 5: Run Forecast Command

**Command**:
```bash
/goalkit.forecast --goal [GOAL_ID] --deadline [DEADLINE] --output json
```

Note: `DEADLINE` from goal.md or milestones.md (e.g., "2025-02-15")

**Parse JSON Output**:
```json
{
  "goal_id": "001",
  "estimated_date": "2025-01-24",
  "confidence": 0.72,
  "probability": 0.75,
  "low_estimate": "2025-01-22",
  "high_estimate": "2025-02-06",
  "days_remaining": 9,
  "tasks_remaining": 4,
  "required_velocity": 0.44
}
```

**Fill Template Section**: `Forecast & Timeline → Completion Prediction`
```markdown
### Completion Prediction

**Target Deadline**: [DEADLINE from goal.md]
**Predicted Completion**: 2025-01-24
**Days to Completion**: 9 days

**Confidence Intervals**:
- 10% confidence (optimistic): 2025-01-22 (2 days early)
- 50% confidence (likely): 2025-01-24 (on time)
- 90% confidence (pessimistic): 2025-02-06 (6 days late)

**Risk Assessment**: [ON TRACK ✅ / AT RISK ⚠️ / CRITICAL 🚨]
```

**Determine Risk Level**:
```
IF estimated_date <= deadline: ON TRACK ✅
IF low_estimate > deadline AND high_estimate <= deadline: AT RISK ⚠️
IF high_estimate > deadline (90% forecast late): CRITICAL 🚨
```

**Interpretation to write** (agent):
```markdown
**Rationale**: [Explain forecast math and confidence level]

**Example**: "With current velocity of 2.75 tasks/week and 4 tasks 
remaining, we need 1.45 weeks. Forecast: Jan 24. Confidence: 72% 
due to declining trend (R²=0.78)."
```

---

### Step 6: Run Insights Command

**Command**:
```bash
/goalkit.insights --goal [GOAL_ID] --output json
```

**Parse JSON Output**:
```json
{
  "goal_id": "001",
  "insights": [
    "Velocity declining 3 weeks - investigate root cause",
    "3 tasks blocked by Infrastructure team (5 days)",
    "Design review cycle averaging 4 days - critical path",
    "Team morale stable, no quality issues detected",
    "Recommend: Escalate Infrastructure blockers by EOD"
  ]
}
```

**Fill Template Section**: `Automated Insights`

**Extract Patterns**:
```markdown
### Key Patterns Identified

**Pattern 1: [FIRST INSIGHT]**
- **What**: [Describe pattern]
- **Impact**: [How it affects project]
- **Recommendation**: [What to do]
```

**Example**:
```markdown
### Key Patterns Identified

**Pattern 1: Declining Velocity**
- **What**: Velocity declined from 4 tasks/week to 2 tasks/week over 4 weeks
- **Impact**: 50% reduction in throughput, pushing deadline at risk
- **Recommendation**: Investigate root cause immediately (blockers, fatigue, or scope creep)

**Pattern 2: Infrastructure Bottleneck**
- **What**: 3 tasks blocked by Infrastructure team, average 5 days per blocker
- **Impact**: 25% of work stalled, critical path delay
- **Recommendation**: Escalate to Infrastructure manager, request 2-day turnaround

**Pattern 3: Design Review Critical Path**
- **What**: Design reviews averaging 4 days, required for 4 tasks
- **Impact**: 16 days of required review time, overlaps with remaining timeline
- **Recommendation**: Implement pre-approval process or parallel reviews
```

---

### Step 7: Fill Decision Points Section

**This is semi-automated** - agent uses forecast + insights to determine recommendation.

**Decision Logic**:
```
IF risk_level == "ON TRACK":
  recommendation = "YES - Continue current approach"
  conditions = [
    "Maintain current velocity",
    "Monitor blockers weekly",
    "[Any condition from insights]"
  ]

ELIF risk_level == "AT RISK":
  recommendation = "YES but ADJUST TACTICS"
  actions = [
    "Escalate [blocker] to [owner]",
    "Reduce scope of [low-priority]",
    "Re-forecast after blockers resolved"
  ]

ELIF risk_level == "CRITICAL":
  recommendation = "NO - Consider Pivot"
  options = [
    "Tactical Pivot: [different execution order]",
    "Strategic Pivot: [try Strategy #2]",
    "Scope Pivot: [reduce success criteria]"
  ]
```

**Fill Template Section**: `Decision Points → Continue Current Approach?`

**Example ON TRACK**:
```markdown
### Continue Current Approach?

**Recommendation**: YES - Continue current approach

**Rationale**: 
- Forecast on schedule (Jan 24 vs deadline Jan 31)
- Velocity stable at 2.75 tasks/week
- No critical blockers (Infrastructure issue on track for resolution)
- 90% confidence interval (Feb 6) safely within deadline

**Conditions**: 
1. Infrastructure blocker resolved by Jan 17
2. Design review cycle stays ≤4 days
3. No unplanned scope additions
```

---

### Step 8: Fill Recommended Actions Section

**Parse from insights** - extract actionable items.

**Fill Template Section**: `Recommended Actions`

**Example**:
```markdown
### Immediate (This Week)

- [ ] **Escalate Infrastructure Blocker**: Contact Infrastructure manager, request 2-day turnaround on 3 tasks - Owner: PM - Target: Today
- [ ] **Optimize Design Reviews**: Request pre-approval of API specs to reduce review cycle - Owner: Tech Lead - Target: Jan 16
- [ ] **Team Retrospective**: Investigate velocity decline root cause - Owner: Manager - Target: Jan 17

### This Sprint

- [ ] **Monitor Unblock**: Verify blockers resolved on schedule
- [ ] **Weekly Velocity Check**: Run /goalkit.velocity to catch new declines early

### Next Review Period

- [ ] Schedule next analytics report (mid-milestone)
- [ ] Document any learnings from this goal
```

---

### Step 9: Fill Success Criteria Tracking

**Read from goal.md** success criteria.

**Check progress** against baseline and target.

**Example**:
```markdown
### Goal Success Criteria Tracking

| Criteria | Baseline | Target | Current | % Complete | Status |
|----------|----------|--------|---------|------------|--------|
| API Response Time (p95) | 450ms | <200ms | 220ms | 92% | ✅ |
| Error Rate | 0.5% | <0.1% | 0.12% | 88% | ✅ |
| User Satisfaction | 6.2/10 | ≥8.0/10 | 7.8/10 | 97% | ✅ |
```

---

### Step 10: Generate Final Report

**Create file**:
```
.goalkit/goals/[GOAL_ID]/analytics-report.md
```

**Template sections filled automatically**:
- ✅ Executive Summary (burndown + forecast)
- ✅ Progress Visualization (burndown chart)
- ✅ Velocity Analysis (weekly breakdown + trends)
- ✅ Forecast & Timeline (completion prediction)
- ✅ Blockers & Bottlenecks (from insights)
- ✅ Automated Insights (patterns from insights)
- ✅ Decision Points (based on risk level)
- ✅ Recommended Actions (from insights)
- ✅ Success Criteria Tracking (from goal.md)

**Sections agent writes** (agent judgment needed):
- Executive Summary (2-3 sentence overview)
- Interpretation sections (explain what metrics mean)
- Notes (additional context)

**Output message**:
```
✅ Analytics Report Generated
Location: .goalkit/goals/001/analytics-report.md
Next: Review report, validate decisions, take recommended actions
```

---

## Example: Complete Workflow

**User requests**: "Generate analytics report for goal 001"

**Agent executes**:

```bash
# 1. Get goal info
READ .goalkit/goals/001/goal.md
# Goal Name: "Improve API Performance"
# Deadline: "2025-02-15"

# 2. Run burndown
/goalkit.burndown --goal 001 --output json
# Extract: 8 of 12 tasks, ideal=9, actual=8 (on track)

# 3. Run velocity  
/goalkit.velocity --goal 001 --periods 4 --output json
# Extract: [4, 3, 2, 2], avg=2.75, trend=declining

# 4. Run trends
/goalkit.trends --goal 001 --output json
# Extract: slope=-0.3, R²=0.78 (high confidence decline)

# 5. Run forecast
/goalkit.forecast --goal 001 --deadline 2025-02-15 --output json
# Extract: Jan 24 (on track), 90% confidence: Feb 6 (6 days late)

# 6. Run insights
/goalkit.insights --goal 001 --output json
# Extract: declining velocity, infrastructure blocker, design reviews

# 7. Fill template
CREATE .goalkit/goals/001/analytics-report.md
  - Burndown chart: 8 of 12 (67%)
  - Velocity table: [4, 3, 2, 2]
  - Trends: R²=0.78, declining -0.3 tasks/week
  - Forecast: Jan 24 (ON TRACK ✅)
  - Insights: 3 patterns identified
  - Actions: Escalate Infrastructure, optimize Design reviews
  - Decision: Continue current approach with conditions

# 8. Output
Report generated ✅
.goalkit/goals/001/analytics-report.md
```

**User opens report** → Reads auto-filled data → Reviews recommended actions → Makes decisions ✅

---

## Quality Checklist

Agent must verify:
- [ ] All 5 commands ran successfully
- [ ] JSON parsed correctly
- [ ] All template sections filled
- [ ] Numbers are accurate and match source data
- [ ] Interpretations make sense (read them back)
- [ ] Risk level determination is correct
- [ ] Recommended actions are specific and actionable
- [ ] Report file saved in correct location
- [ ] Report is readable markdown

---

## Common Issues & Solutions

### Command Returns "Insufficient Data"
**Cause**: Goal just created, not enough history
**Solution**: Run basic commands, note that forecasting requires 2+ weeks of data
**Fill report with**: "Report generated, but forecasting unavailable - check back after next week"

### JSON Parse Fails
**Cause**: Command output format unexpected
**Solution**: Run command manually, check output format
**Action**: Use text output instead if JSON unavailable

### Forecast Date Beyond Deadline
**Cause**: Goal likely to miss deadline
**Solution**: Correctly identify as CRITICAL risk
**Action**: Fill decision section with pivot recommendations

### Metrics Contradict (e.g., On Track but Declining)
**Cause**: Early-stage decline or catch-up pattern
**Solution**: Note in interpretation: "Early decline but still on track due to early lead"
**Action**: Flag for next week's follow-up

---

## Pro Tips

1. **Run all 5 commands early** - Gets full picture before filling template
2. **Parse JSON first** - Easier to fill template from structured data
3. **Fill metrics sections first** - Then interpretations last (they're easier to add)
4. **Sanity check numbers** - Do velocity numbers match burndown progression?
5. **Reread interpretations** - Do they sound accurate?
6. **Note any surprises** - If metrics contradict, document it

---

## See Also

- **Template**: `templates/analytics-report-template.md` - Fill this with data
- **Analytics Guide**: `docs/analytics-guide.md` - How to interpret metrics
- **Burndown Command**: `templates/commands/analytics.md#goalkitburndown`
- **Velocity Command**: `templates/commands/analytics.md#goalkitvelocity`
- **Forecast Command**: `templates/commands/analytics.md#goalkitforecast`
- **Insights Command**: `templates/commands/analytics.md#goalkitinsights`
