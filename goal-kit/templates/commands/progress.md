---
title: "Progress Tracking Command"
description: "Track and report goal progress with comprehensive metrics"
agent: "goal-kit"
version: "1.0"
command_type: "progress_tracking"
execution_context: "monitoring_reporting"
required_tools: ["file_system", "metrics_calculator", "report_generator"]
---

# Progress Tracking Command Template

## Command Overview

**Command:** `goal progress`
**Purpose:** Track, analyze, and report goal progress with comprehensive metrics
**Input:** Goal file and progress data
**Output:** Progress reports and updated goal status

## Command Usage

### Basic Syntax

```bash
goal progress [goal-file] --update --progress [percentage]
```

### Advanced Syntax

```bash
goal progress "ai-project-goal.json" \
  --update \
  --progress 65 \
  --status on_track \
  --metrics "accuracy:94%,training-time:2.3h,dataset-size:1.2GB" \
  --evidence-add "./reports/weekly-progress.pdf"
```

## Command Types

### Update Progress

```bash
goal progress [goal-file] --update --progress [percentage] --status [status]
```

### Generate Report

```bash
goal progress [goal-file] --report --format [format] --period [period]
```

### Analyze Progress

```bash
goal progress [goal-file] --analyze --baseline [baseline-date]
```

### Track Metrics

```bash
goal progress [goal-file] --metrics-add "key:value,key2:value2"
```

### Visual Progress

```bash
goal progress [goal-file] --visualize --chart-type [type]
```

## Command Parameters

### Required Parameters

- **goal-file** (string): Path to the goal JSON file

### Progress Parameters

- **update** (flag): Update progress information
- **progress** (number): Overall progress percentage (0-100)
- **status** (string): Progress status [not_started/in_progress/on_track/behind/ahead/completed/at_risk]

### Optional Parameters

- **metrics** (string): Key-value pairs of progress metrics
- **evidence-add** (string): Path to evidence file or URL
- **notes** (string): Progress notes and observations
- **milestone** (string): Specific milestone to update
- **achievement** (string): Specific achievement to update

### Report Parameters

- **report** (flag): Generate progress report
- **format** (string): Report format [json/markdown/html/pdf]
- **period** (string): Reporting period [daily/weekly/monthly/quarterly]
- **include-evidence** (flag): Include evidence in report
- **include-metrics** (flag): Include detailed metrics

### Analysis Parameters

- **analyze** (flag): Perform progress analysis
- **baseline** (date): Baseline date for comparison (YYYY-MM-DD)
- **forecast** (flag): Generate progress forecasts
- **risk-analysis** (flag): Analyze risks and issues

## Command Examples

### Example 1: Basic Progress Update

```bash
goal progress "web-app-goal.json" \
  --update \
  --progress 45 \
  --status on_track \
  --notes "Completed user authentication, starting on dashboard"
```

### Example 2: Detailed Progress with Metrics

```bash
goal progress "ml-project-goal.json" \
  --update \
  --progress 72 \
  --status on_track \
  --metrics "model-accuracy:94.2%,training-loss:0.023,validation-score:91.8%" \
  --evidence-add "./reports/model-performance.pdf" \
  --notes "Model performance exceeding expectations, considering early deployment"
```

### Example 3: Milestone-Specific Progress

```bash
goal progress "startup-goal.json" \
  --update \
  --milestone "2.1" \
  --progress 80 \
  --status ahead \
  --notes "MVP development ahead of schedule due to efficient team collaboration"
```

### Example 4: Generate Progress Report

```bash
goal progress "quarterly-objectives.json" \
  --report \
  --format markdown \
  --period monthly \
  --include-metrics \
  --include-evidence
```

### Example 5: Progress Analysis

```bash
goal progress "research-project.json" \
  --analyze \
  --baseline 2024-01-01 \
  --forecast \
  --risk-analysis
```

### Example 6: Visual Progress Tracking

```bash
goal progress "product-launch-goal.json" \
  --visualize \
  --chart-type burndown \
  --include-trend-lines \
  --output-format png
```

## Progress Tracking Methodologies

### Burndown Chart Methodology

```javascript
const burndownTracking = {
  goal: "Software Development Project",
  totalWork: 100, // story points or hours
  remainingWork: 65,
  idealBurndown: calculateIdealBurndown(),
  actualBurndown: calculateActualBurndown(),
  trendAnalysis: analyzeTrend(),
  prediction: predictCompletion(),
};

function calculateIdealBurndown() {
  // Linear burndown from start to end date
  const daysElapsed = Math.floor(
    (Date.now() - startDate) / (1000 * 60 * 60 * 24),
  );
  const totalDays = Math.floor((endDate - startDate) / (1000 * 60 * 60 * 24));
  const idealRemaining = totalWork * (1 - daysElapsed / totalDays);
  return Math.max(0, idealRemaining);
}
```

### Velocity-Based Tracking

```javascript
const velocityTracking = {
  goal: "Agile Development",
  sprintVelocity: 25, // story points per sprint
  completedVelocity: 28, // last sprint completion
  averageVelocity: 26.5, // average over sprints
  velocityTrend: "increasing",
  forecast: {
    basedOnLastSprint: calculateCompletion(28),
    basedOnAverage: calculateCompletion(26.5),
  },
};

function calculateCompletion(velocity) {
  const remainingWork = totalWork - completedWork;
  const sprintsRemaining = Math.ceil(remainingWork / velocity);
  const completionDate = addSprintsToDate(currentDate, sprintsRemaining);
  return { sprintsRemaining, completionDate };
}
```

### Milestone-Based Tracking

```javascript
const milestoneTracking = {
  milestones: [
    { id: "M1", name: "Planning", progress: 100, status: "completed" },
    { id: "M2", name: "Development", progress: 75, status: "on_track" },
    { id: "M3", name: "Testing", progress: 0, status: "not_started" },
    { id: "M4", name: "Deployment", progress: 0, status: "not_started" },
  ],
  overallProgress: 35,
  criticalPath: identifyCriticalPath(),
  milestoneVariance: calculateVariance(),
};
```

## Progress Metrics Framework

### Quantitative Metrics

```javascript
const quantitativeMetrics = {
  completion: {
    tasksCompleted: 45,
    totalTasks: 120,
    completionRate: 37.5,
    storyPointsCompleted: 180,
    totalStoryPoints: 450,
    velocity: 22.5,
  },
  time: {
    daysElapsed: 18,
    totalDays: 60,
    timeUtilization: 30,
    scheduleVariance: -2, // days ahead/behind
    estimatedCompletion: "2024-03-15",
  },
  quality: {
    testCoverage: 88,
    defectDensity: 0.02, // defects per story point
    codeQualityScore: "A",
    securityVulnerabilities: 0,
  },
};
```

### Qualitative Metrics

```javascript
const qualitativeMetrics = {
  stakeholderSatisfaction: {
    overall: 4.2, // out of 5
    communication: 4.5,
    quality: 4.0,
    timeliness: 4.1,
  },
  teamPerformance: {
    collaboration: "Excellent",
    skillUtilization: "Good",
    morale: "High",
    knowledgeTransfer: "Effective",
  },
  riskManagement: {
    risksIdentified: 12,
    risksMitigated: 8,
    activeRisks: 4,
    riskExposure: "Medium",
  },
};
```

### Predictive Metrics

```javascript
const predictiveMetrics = {
  trendAnalysis: {
    progressTrend: "accelerating",
    velocityTrend: "stable",
    qualityTrend: "improving",
    riskTrend: "decreasing",
  },
  forecasting: {
    completionProbability: 85,
    estimatedCompletion: "2024-03-10",
    confidenceInterval: "±3 days",
    keyAssumptions: ["team stability", "no scope changes"],
  },
  recommendations: [
    "Continue current approach",
    "Consider adding resources to accelerate",
    "Focus on high-risk milestones",
  ],
};
```

## Progress Visualization

### Chart Types

```javascript
const chartTypes = {
  burndown: {
    type: "line",
    xAxis: "Date",
    yAxis: "Remaining Work",
    datasets: ["Ideal Burndown", "Actual Progress"],
    annotations: ["Milestones", "Key Events"],
  },
  progress: {
    type: "bar",
    categories: ["Milestones", "Achievements"],
    measures: ["Planned", "Actual", "Variance"],
  },
  velocity: {
    type: "line",
    xAxis: "Sprint",
    yAxis: "Story Points",
    datasets: ["Completed", "Committed", "Rolling Average"],
  },
  risk: {
    type: "bubble",
    xAxis: "Probability",
    yAxis: "Impact",
    bubbleSize: "Risk Level",
    categories: ["Technical", "Business", "Operational"],
  },
};
```

### Dashboard Components

```javascript
const progressDashboard = {
  header: {
    title: "Project Progress Dashboard",
    lastUpdated: "2024-01-20 14:30",
    overallStatus: "On Track",
    completionPercentage: 65,
  },
  charts: [
    { id: "burndown-chart", position: "top-left", size: "medium" },
    { id: "milestone-progress", position: "top-right", size: "medium" },
    { id: "velocity-chart", position: "bottom-left", size: "small" },
    { id: "risk-matrix", position: "bottom-right", size: "small" },
  ],
  metrics: [
    { name: "Days Remaining", value: 42, trend: "stable" },
    { name: "Budget Remaining", value: "68%", trend: "positive" },
    { name: "Quality Score", value: "A-", trend: "improving" },
    { name: "Risk Level", value: "Medium", trend: "decreasing" },
  ],
};
```

## Progress Reporting

### Report Templates

```javascript
const reportTemplates = {
  executive: {
    sections: [
      "Executive Summary",
      "Key Metrics",
      "Major Achievements",
      "Upcoming Milestones",
      "Risks and Issues",
      "Recommendations",
    ],
    audience: "Executives and Stakeholders",
    frequency: "Monthly",
    format: "Dashboard + Summary",
  },
  detailed: {
    sections: [
      "Progress Overview",
      "Milestone Status",
      "Task Completion",
      "Quality Metrics",
      "Time Tracking",
      "Risk Analysis",
      "Detailed Metrics",
    ],
    audience: "Project Team and Managers",
    frequency: "Weekly",
    format: "Comprehensive Report",
  },
  technical: {
    sections: [
      "Technical Progress",
      "Code Quality",
      "Testing Status",
      "Performance Metrics",
      "Security Status",
      "Infrastructure Updates",
    ],
    audience: "Technical Team",
    frequency: "Weekly",
    format: "Technical Report",
  },
};
```

### Automated Reporting

```javascript
const automatedReporting = {
  triggers: [
    { event: "milestone_completed", report: "milestone_summary" },
    { event: "quality_gate_passed", report: "quality_update" },
    { event: "schedule_variance", report: "variance_alert" },
    { event: "weekly_digest", report: "weekly_summary" },
  ],
  distribution: [
    { audience: "team", method: "email", format: "html" },
    { audience: "stakeholders", method: "dashboard", format: "summary" },
    { audience: "executives", method: "email", format: "executive" },
  ],
};
```

## Progress Analysis

### Trend Analysis

```javascript
const trendAnalysis = {
  dataPoints: [
    { date: "2024-01-01", progress: 0, velocity: 0 },
    { date: "2024-01-08", progress: 12, velocity: 12 },
    { date: "2024-01-15", progress: 28, velocity: 16 },
    { date: "2024-01-22", progress: 45, velocity: 17 },
    { date: "2024-01-29", progress: 65, velocity: 20 },
  ],
  trends: {
    progressAcceleration: "increasing",
    velocityStability: "improving",
    qualityConsistency: "stable",
  },
  predictions: {
    completionDate: "2024-03-15",
    confidenceLevel: 85,
    influencingFactors: ["team performance", "scope changes"],
  },
};
```

### Variance Analysis

```javascript
const varianceAnalysis = {
  schedule: {
    plannedProgress: 70,
    actualProgress: 65,
    variance: -5, // 5% behind schedule
    varianceReason: "technical_challenges",
    recoveryPlan: "add_resources",
  },
  budget: {
    plannedSpend: 150000,
    actualSpend: 145000,
    variance: 5000, // under budget
    varianceReason: "efficient_execution",
  },
  scope: {
    plannedFeatures: 25,
    completedFeatures: 24,
    variance: 1, // one feature behind
    varianceReason: "complexity_underestimated",
  },
};
```

### Risk Analysis

```javascript
const riskAnalysis = {
  risks: [
    {
      category: "Technical",
      risk: "API integration complexity",
      probability: 0.7,
      impact: 0.8,
      riskLevel: "high",
      mitigation: "early_prototyping",
      status: "monitoring",
    },
    {
      category: "Resource",
      risk: "Key developer availability",
      probability: 0.3,
      impact: 0.9,
      riskLevel: "high",
      mitigation: "backup_resources",
      status: "mitigating",
    },
  ],
  overallRisk: "medium",
  riskTrend: "decreasing",
  recommendations: ["increase testing", "add contingency time"],
};
```

## Integration Points

### Version Control Integration

- Progress updates on commits
- Evidence linking to code changes
- Automated progress calculation from Git activity
- Milestone tracking in branches

### Time Tracking Integration

- Integration with time tracking tools
- Automatic progress updates from time logs
- Effort estimation vs. actual comparison
- Resource utilization analysis

### Communication Integration

- Progress updates to team chat
- Automated status emails
- Dashboard sharing with stakeholders
- Meeting agenda generation

## Best Practices

### Progress Tracking

- **Regular Updates:** Update progress frequently (daily/weekly)
- **Evidence-Based:** Support progress claims with evidence
- **Transparent:** Share progress openly with stakeholders
- **Actionable:** Use progress data to make decisions

### Metrics Selection

- **Relevant Metrics:** Choose metrics that matter for your goal
- **Balanced View:** Include quantitative and qualitative metrics
- **Trend Focus:** Monitor trends, not just snapshots
- **Predictive Value:** Use metrics that help predict outcomes

### Reporting

- **Audience-Appropriate:** Tailor reports to different audiences
- **Visual Clarity:** Use charts and visuals for complex data
- **Timely Delivery:** Deliver reports when stakeholders need them
- **Action-Oriented:** Include clear next steps and recommendations

## Troubleshooting

### Common Issues

1. **Inaccurate Progress:** Implement validation checks and evidence requirements
2. **Missing Metrics:** Define clear metrics at goal definition time
3. **Stakeholder Confusion:** Use consistent terminology and clear visualizations
4. **Data Overload:** Focus on key metrics rather than everything

### Data Quality

- **Validation:** Validate progress data before acceptance
- **Consistency:** Use consistent measurement methods
- **Completeness:** Ensure all required metrics are tracked
- **Timeliness:** Update data in a timely manner

### Performance Issues

- **Automation:** Automate data collection where possible
- **Efficiency:** Optimize queries and calculations
- **Caching:** Cache frequently accessed data
- **Archiving:** Archive old data to maintain performance

## Related Commands

- `goal define` - Create goals with progress tracking structure
- `goal milestone` - Manage milestones and dependencies
- `goal achieve` - Mark achievements and completion
- `goal report` - Generate detailed progress reports
- `goal visualize` - Create progress visualizations

## Command Reference

- `goal progress --help` - Show detailed help
- `goal progress examples` - Show usage examples
- `goal progress templates` - List progress tracking templates
- `goal progress validate [goal-file]` - Validate progress data
