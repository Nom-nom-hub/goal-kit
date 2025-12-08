# Metrics Plan: [GOAL NAME]

**Goal Reference**: Links to `/goals/[###-goal-name]/goal.md`  
**Goal Branch**: `[###-goal-name]` | **Date**: [DATE]

**Note**: This template helps plan how to measure success criteria defined in your goal. Use this to ensure metrics are measurable, actionable, and properly instrumented.

---

## Success Criteria Review

Extract success criteria from goal.md and validate metric quality.

| Metric ID | Description | Target | Timeframe | Quality Score |
|-----------|-------------|--------|-----------|---------------|
| SC-001 | [Metric description] | [Target value] | [By when] | [See checklist below] |
| SC-002 | [Metric description] | [Target value] | [By when] | [See checklist below] |
| SC-003 | [Metric description] | [Target value] | [By when] | [See checklist below] |

---

## Metric Quality Validation

For each success criterion, validate against quality checklist:

### SC-001: [Metric Name]

**Metric Description**: [Full description of what's being measured]

#### Quality Checklist
- [ ] **Measurable**: Can we collect this data reliably and objectively?
  - *How measured*: [Specific measurement method]
  - *Data source*: [Where data comes from]
  - *Frequency*: [How often measured]

- [ ] **Actionable**: Will this metric drive specific decisions?
  - *Green zone (≥ target)*: [What action to take]
  - *Yellow zone (near target)*: [What action to take]
  - *Red zone (< threshold)*: [What action to take]

- [ ] **Leading**: Does it predict future success (not just lag)?
  - *Leading indicator*: [Yes/No - explain]
  - *Lag time*: [How long until impact visible]

- [ ] **Bounded**: Is there a clear target and timeframe?
  - *Target*: [Specific number/percentage]
  - *Baseline*: [Current state]
  - *Deadline*: [When to achieve by]

- [ ] **Valuable**: Does it connect to user/business outcomes?
  - *User value*: [How this helps users]
  - *Business value*: [How this helps business]
  - *Alignment*: [Links to vision scenario]

**Quality Score**: [Pass/Needs Improvement/Fail]

**Issues to address**: [Any quality gaps to fix]

---

### SC-002: [Metric Name]

[Repeat same structure as SC-001]

---

### SC-003: [Metric Name]

[Repeat same structure as SC-001]

---

## Baseline Measurements

Establish current state before starting work.

| Metric | Current Baseline | Measurement Date | Measurement Method | Notes |
|--------|------------------|------------------|-------------------|-------|
| SC-001 | [Current value] | [Date measured] | [How measured] | [Context] |
| SC-002 | [Current value] | [Date measured] | [How measured] | [Context] |
| SC-003 | [Current value] | [Date measured] | [How measured] | [Context] |

**Baseline validation**:
- [ ] Baselines measured using same method as target measurement
- [ ] Baselines represent typical state (not outliers)
- [ ] Baselines documented with context (time period, conditions)

---

## Instrumentation Plan

Define how to collect data for each metric.

### SC-001: [Metric Name]

**What to instrument**:
- [Specific events to track]
- [User behaviors to log]
- [System metrics to capture]

**How to collect**:
- **Tool/Platform**: [Analytics tool, logging system, database query]
- **Implementation**: [Code changes needed, tracking setup]
- **Storage**: [Where data is stored]

**When to measure**:
- **Frequency**: [Real-time, daily, weekly]
- **Triggers**: [Events that trigger measurement]
- **Duration**: [How long to collect data]

**Who analyzes**:
- **Responsible person**: [Name/role]
- **Review frequency**: [How often to review]
- **Reporting format**: [Dashboard, report, alert]

**Validation**:
- [ ] Instrumentation tested and working
- [ ] Data collection verified accurate
- [ ] Dashboard/reporting set up

---

### SC-002: [Metric Name]

[Repeat same structure as SC-001]

---

### SC-003: [Metric Name]

[Repeat same structure as SC-001]

---

## Metric Types Classification

Categorize metrics to ensure balanced measurement.

### User Behavior Metrics
Metrics that measure how users actually use the feature:
- **[Metric ID]**: [Description]
- **[Metric ID]**: [Description]

### Business Impact Metrics
Metrics that measure business value delivered:
- **[Metric ID]**: [Description]
- **[Metric ID]**: [Description]

### Technical Quality Metrics
Metrics that measure system performance/reliability:
- **[Metric ID]**: [Description]
- **[Metric ID]**: [Description]

### Learning Metrics
Metrics that measure what we discovered/capabilities built:
- **[Metric ID]**: [Description]
- **[Metric ID]**: [Description]

**Balance check**:
- [ ] At least one user behavior metric
- [ ] At least one business impact metric
- [ ] Technical metrics support user/business metrics
- [ ] Learning objectives defined

---

## Decision Thresholds

Define what actions to take based on metric values.

### SC-001: [Metric Name]

| Zone | Threshold | Status | Action |
|------|-----------|--------|--------|
| 🟢 **Green (Success)** | ≥ [target] | Goal met | Scale feature, celebrate, document success |
| 🟡 **Yellow (Warning)** | [X] to [Y] | Needs attention | Investigate root cause, adjust tactics |
| 🔴 **Red (Failure)** | < [threshold] | Goal at risk | Pivot strategy, escalate, consider alternatives |

**Pivot triggers**:
- If metric stays in red zone for [duration] → [specific action]
- If metric trends downward for [duration] → [specific action]

---

### SC-002: [Metric Name]

[Repeat same structure as SC-001]

---

### SC-003: [Metric Name]

[Repeat same structure as SC-001]

---

## Measurement Dashboard

Define how metrics will be visualized and monitored.

### Dashboard Design

**Tool/Platform**: [Grafana, Metabase, Tableau, Google Analytics, Custom]

**Dashboard sections**:
1. **Overview**: All metrics at-a-glance with status indicators
2. **Trends**: Time-series charts showing metric evolution
3. **Breakdowns**: Segmentation by user type, platform, etc.
4. **Alerts**: Notifications when metrics cross thresholds

**Access**:
- **Who can view**: [Team members, stakeholders]
- **Update frequency**: [Real-time, hourly, daily]
- **Link**: [URL to dashboard when created]

### Visualization Plan

| Metric | Chart Type | Breakdown Dimensions | Update Frequency |
|--------|------------|---------------------|------------------|
| SC-001 | Line chart | By platform, user segment | Real-time |
| SC-002 | Bar chart | By cohort, time period | Daily |
| SC-003 | Gauge | Overall, by milestone | Weekly |

---

## Measurement Schedule

Timeline for metric collection and review.

### Milestone-Based Measurement

| Milestone | Metrics to Measure | When | Success Criteria |
|-----------|-------------------|------|------------------|
| M1: [Name] | [Subset of metrics] | [Date/timeframe] | [Partial targets] |
| M2: [Name] | [Subset of metrics] | [Date/timeframe] | [Partial targets] |
| M3: [Name] | [All metrics] | [Date/timeframe] | [Full targets] |

### Review Cadence

- **Daily**: Quick check of real-time metrics (if applicable)
- **Weekly**: Team review of metric trends and issues
- **Milestone completion**: Full metric review and analysis
- **Goal completion**: Final metric analysis and learnings capture

---

## Data Collection Validation

Ensure data quality and reliability.

### Validation Checklist

- [ ] **Accuracy**: Metrics measure what they claim to measure
  - *Test*: [How to verify accuracy]
  - *Result*: [Validation outcome]

- [ ] **Completeness**: All relevant data is captured
  - *Test*: [How to verify completeness]
  - *Result*: [Validation outcome]

- [ ] **Consistency**: Measurements are repeatable
  - *Test*: [How to verify consistency]
  - *Result*: [Validation outcome]

- [ ] **Timeliness**: Data is available when needed
  - *Test*: [How to verify timeliness]
  - *Result*: [Validation outcome]

### Known Limitations

Document any measurement limitations or caveats:

- **[Limitation 1]**: [Description and impact]
- **[Limitation 2]**: [Description and impact]

---

## Metric Evolution Plan

How metrics might change based on learning.

### Initial Metrics (M1)
Focus on validating core assumptions:
- [Metric focus for early milestones]

### Evolved Metrics (M2-M3)
Refine based on M1 learnings:
- [How metrics might evolve]
- [New metrics to add if needed]

### Post-Launch Metrics
Long-term success indicators:
- [Metrics to track after goal completion]
- [Transition to BAU monitoring]

---

## Risk Mitigation

Address risks to measurement quality.

| Risk | Impact | Mitigation | Owner |
|------|--------|------------|-------|
| Data collection fails | Can't measure success | Backup manual tracking method | [Name] |
| Metric gaming | False positive results | Cross-validate with qualitative feedback | [Name] |
| Delayed data availability | Can't make timely decisions | Set up alerts for data delays | [Name] |
| Baseline shifts | Invalid comparisons | Document context changes, adjust targets | [Name] |

---

## Success Criteria

This measurement plan is ready when:

- [ ] All metrics pass quality validation checklist
- [ ] Baselines measured and documented
- [ ] Instrumentation implemented and tested
- [ ] Dashboard created and accessible
- [ ] Decision thresholds defined and agreed
- [ ] Review schedule established
- [ ] Team trained on metric interpretation

---

## Appendix: Metric Definitions

### Detailed Metric Specifications

#### SC-001: [Metric Name]

**Full Definition**: [Precise definition of what's measured]

**Calculation Method**: [Exact formula or query]
```
Example: 
Adoption Rate = (Active Users / Total Eligible Users) × 100
Where:
- Active Users = users who used feature ≥3 times in last 7 days
- Total Eligible Users = all users with access to feature
```

**Data Sources**: [Specific tables, APIs, tools]

**Exclusions**: [What's not counted and why]

**Edge Cases**: [How to handle special situations]

---

#### SC-002: [Metric Name]

[Repeat same structure as SC-001]

---

#### SC-003: [Metric Name]

[Repeat same structure as SC-001]

---

## Document Metadata

**Created**: [DATE]  
**Last Updated**: [DATE]  
**Owner**: [Person responsible for metrics]  
**Review Status**: [Draft/Reviewed/Approved]  
**Next Review**: [When to revisit this plan]
