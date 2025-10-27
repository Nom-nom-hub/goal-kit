---
description: Progress tracking and analytics dashboard for project monitoring and insights
scripts:
  sh: .goalkit/scripts/python/progress_tracker.py --format text
  ps: .goalkit/scripts/python/progress_tracker.py --format text
agent_scripts:
  sh: .goalkit/scripts/python/update_agent_context.py __AGENT__
  ps: .goalkit/scripts/python/update_agent_context.py __AGENT__
---

# Progress Tracking Command

**Purpose**: Generate real-time progress reports, analytics, and insights for project monitoring

**When to Use**:

- To check current project status and progress
- To identify goals or milestones that need attention
- To track velocity and predict completion dates
- To generate progress reports for stakeholders
- To save historical progress data

## Quick Prerequisites Check

**BEFORE TRACKING PROGRESS**:

1. **Goal Kit project exists**: Verify `.goalkit/` directory structure
2. **Goals created**: Have goals with milestones to track
3. **Some progress made**: Have milestones or activities to analyze

**If missing**: Create goals and start execution first.

## Quick Progress Analysis Steps

**STEP 1**: Analyze all active goals and their milestones

**STEP 2**: Calculate progress metrics:

- Completion percentages
- Velocity scores (milestones per week)
- Risk assessments
- Estimated completion dates

**STEP 3**: Generate comprehensive progress report

**STEP 4**: Identify goals needing attention

**STEP 5**: Provide actionable recommendations

## Progress Metrics

**Key Performance Indicators**:

- **Completion Rate**: Percentage of milestones achieved
- **Velocity Score**: Milestones completed per week (0-10 scale)
- **Project Health**: Overall project status (excellent/good/concerning/critical)
- **Risk Score**: Project risk level (1-10 scale)
- **Time-based Tracking**: Days since creation and estimated completion

**Goal Status Categories**:

- **Completed**: 100% milestones achieved
- **On Track**: Good velocity, making steady progress
- **At Risk**: Moderate progress, some concerns
- **Behind**: Slow progress, needs attention

## Agent Script Execution Guide

**CRITICAL**: When processing `/goalkit.progress` commands, agents MUST:

### **STEP 1**: Run the progress tracking script

```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/progress_tracker.py --format text
```

### **STEP 2**: If saving for historical tracking, include save option

```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/progress_tracker.py --save --format text
```

### **STEP 3**: Parse progress results for insights

- **Extract completion percentages** and velocity scores
- **Identify at-risk goals** that need attention
- **Note recommendations** for progress improvement
- **Check project health** indicators

### **STEP 4**: Provide progress-based guidance

- **High Progress**: "Excellent momentum - maintain current approach"
- **Medium Progress**: "Good progress - consider optimizations"
- **Low Progress**: "Needs attention - review and adjust approach"

### **STEP 5**: Update learning system with progress insights

```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/learning_system.py --capture "progress-tracking" "Progress milestone: {PROGRESS_INSIGHT}"
```

## Input Format

```text
/goalkit.progress [options]
```

### Command Options

```text
/goalkit.progress                    # Generate current progress report
/goalkit.progress --save             # Save analytics for historical tracking
/goalkit.progress --json             # Output in JSON format for integration
```

## Output

The command generates:

- **Project Summary**: Overall completion and health metrics
- **Goal Details**: Individual goal progress and status
- **Velocity Analysis**: Progress speed and trends
- **Risk Assessment**: Identification of problem areas
- **Recommendations**: Specific actions to improve progress

### Progress Data Collection

**Automatic Analysis**:

1. **Goal Discovery**: Find all active goals in `.goalkit/goals/`
2. **Milestone Analysis**: Count completed vs total milestones
3. **Date Calculation**: Determine creation dates and progress age
4. **Velocity Computation**: Calculate completion speed
5. **Risk Assessment**: Identify stalled or slow-moving goals

## Progress Components

### 1. Project-Level Analytics

- **Total Goals**: Number of active goals
- **Completion Overview**: Goals completed vs in progress
- **Overall Health**: Project-wide status assessment
- **Velocity Trends**: Project speed and momentum
- **Risk Profile**: Overall project risk factors

### 2. Individual Goal Tracking

- **Goal Status**: Current completion percentage
- **Milestone Progress**: Detailed milestone completion
- **Age Tracking**: Days since goal creation
- **Velocity Score**: Individual goal speed (0-10)
- **Completion Estimates**: Predicted completion dates

### 3. Risk Identification

- **Stalled Goals**: Goals with no recent progress
- **Slow Velocity**: Goals progressing too slowly
- **High-Risk Goals**: Goals with concerning patterns
- **Resource Bottlenecks**: Areas needing attention

### 4. Predictive Analytics

- **Completion Forecasting**: Estimated completion dates
- **Trend Analysis**: Progress acceleration/deceleration
- **Risk Prediction**: Likelihood of goal achievement
- **Resource Planning**: Timeline and effort estimation

## Integration with Other Commands

### Progress in Workflow

- **After `/goalkit.milestones`**: Establish progress baseline
- **During `/goalkit.execute`**: Track ongoing progress
- **Before Major Decisions**: Assess current status
- **Stakeholder Updates**: Generate progress reports

### Progress-Driven Decisions

```text
/goalkit.goal → Create goal
/goalkit.milestones → Define milestones
/goalkit.execute → Start execution
/goalkit.progress → Track progress
[If behind schedule] → Adjust approach or scope
[If on track] → Continue execution
```

## Best Practices

### Regular Progress Tracking

- **Weekly Reviews**: Regular progress assessment
- **Milestone Checkpoints**: Validate milestone completion
- **Trend Monitoring**: Track velocity and health trends
- **Risk Management**: Address issues before they become critical

### Progress Interpretation

- **High Velocity (7-10)**: Excellent progress, maintain momentum
- **Medium Velocity (4-6)**: Good progress, monitor for improvements
- **Low Velocity (1-3)**: Concerning progress, investigate and address
- **Zero Velocity**: Stalled, requires immediate attention

### Progress Improvement Strategies

1. **Identify Bottlenecks**: Find what's slowing progress
2. **Resource Adjustment**: Reallocate time and attention
3. **Scope Refinement**: Adjust goals if needed
4. **Process Improvement**: Enhance execution methods
5. **Team Coordination**: Improve collaboration and communication

## Common Progress Patterns

### Healthy Project Patterns

- **Steady Velocity**: Consistent progress over time
- **Increasing Completion**: Accelerating milestone achievement
- **Risk Reduction**: Decreasing risk scores over time
- **On-Time Delivery**: Meeting estimated completion dates

### Concerning Project Patterns

- **Velocity Decline**: Slowing progress over time
- **Stalled Goals**: Long periods without milestone completion
- **Increasing Risk**: Growing number of at-risk goals
- **Missed Estimates**: Consistently missing completion predictions

### Recovery Patterns

- **Intervention Success**: Progress improvement after adjustments
- **Risk Mitigation**: Successful resolution of problem areas
- **Velocity Recovery**: Return to healthy progress speeds
- **Team Learning**: Process improvements leading to better results

## Examples

### Example 1: Regular Progress Check

```text
/goalkit.progress
```

**Output**: Current project status, goal progress, velocity scores, and recommendations

### Example 2: Historical Tracking

```text
/goalkit.progress --save
```

**Output**: Progress report plus saved analytics data for trend analysis

### Example 3: Stakeholder Reporting

```text
/goalkit.progress --json
```

**Output**: JSON format suitable for integration with reporting tools or dashboards

## Agent Integration

### Progress-Aware Assistance

**CRITICAL**: Agents should use progress data for intelligent guidance:

1. **Context-Aware Recommendations**: Base suggestions on current progress status
2. **Risk-Based Prioritization**: Focus attention on at-risk goals
3. **Velocity-Optimized Planning**: Suggest realistic timelines based on current speed
4. **Predictive Guidance**: Use completion estimates for planning

### Automated Progress Integration

- **Post-Milestone Updates**: Automatically update progress after milestone completion
- **Regular Check-Ins**: Periodic progress analysis during execution
- **Trend Alerts**: Notify when progress patterns change significantly
- **Success Celebrations**: Highlight achievement of major milestones

## Progress Visualization

### Visual Indicators

- **🟢 Excellent Health**: Strong progress, low risk
- **🟡 Good Health**: Acceptable progress, monitor
- **🟠 Concerning Health**: Needs attention, some risks
- **🔴 Critical Health**: Immediate action required

### Progress Symbols

- **✅ Completed**: Goal/milestone fully achieved
- **🚀 On Track**: Making excellent progress
- **⚠️ At Risk**: Progress slower than expected
- **🐌 Behind**: Significantly delayed or stalled

## Key Benefits

- **Progress Visibility**: Clear view of project status and momentum
- **Early Warning System**: Identify problems before they become critical
- **Data-Driven Decisions**: Make decisions based on actual progress data
- **Stakeholder Communication**: Generate reports for team and stakeholder updates
- **Continuous Improvement**: Track improvements in velocity and efficiency

## Critical Rules

✅ **DO**: Run progress checks regularly during execution
✅ **DO**: Address at-risk and behind goals promptly
✅ **DO**: Use progress data for decision-making
✅ **DO**: Save historical data for trend analysis
❌ **DON'T**: Ignore concerning progress patterns
❌ **DON'T**: Proceed without understanding current status
❌ **DON'T**: Make decisions without progress context

## Next Steps Integration

**After `/goalkit.progress`**:

- **Excellent Progress**: Continue current approach, maintain momentum
- **Good Progress**: Monitor trends, consider minor optimizations
- **Concerning Progress**: Review and adjust goals or approaches
- **Critical Progress**: Immediate intervention required, consider scope changes

**Progress-Driven Workflow**:

1. Check progress → 2. Assess status → 3. Address issues → 4. Continue execution → 5. Track improvements
