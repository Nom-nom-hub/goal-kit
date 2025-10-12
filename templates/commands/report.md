# /goalkit.report Command

## AI AGENT INSTRUCTIONS

When processing `/goalkit.report` requests, follow this structured approach:

### Input Analysis
1. **Identify Report Type**: Determine the specific report type and audience from user input
2. **Extract Goal Metrics**: Identify relevant goal achievement metrics to include in the report
3. **Define Time Context**: Establish the time period and frequency for the report
4. **Assess Stakeholder Needs**: Understand the specific information requirements of the report audience

### Processing Framework
- Focus on goal achievement metrics rather than implementation details
- Generate relevant metrics that directly relate to goal success criteria
- Create appropriate visualizations and summaries for the report type
- Include actionable insights and recommendations based on goal progress

### Output Structure
Use the template sections below to structure your response. Ensure alignment with existing project goals and maintain consistency with goal-driven development principles.

---

## Overview

The `/goalkit.report` command generates various project reports (status, progress, forecast, retrospective) based on goal-driven development metrics. This command creates structured reports focused on goal achievement rather than implementation details.

## Purpose

This command creates reports that:
- Track and communicate goal achievement progress
- Provide insights into goal-driven development effectiveness
- Support stakeholder communication with relevant metrics
- Enable data-driven decision making for goal adaptation

## When to Use

Use `/goalkit.report` when:
- Providing stakeholder updates on goal achievement
- Conducting periodic project reviews and assessments
- Forecasting goal completion and resource needs
- Documenting project progress and learnings
- Supporting compliance and governance reporting
- Making data-driven decisions about goal adaptation
- Communicating team performance and goal outcomes

## Input Format

```
/goalkit.report
Report Type: [Status, Progress, Forecast, Retrospective, Executive Summary, Compliance]
Goal: [Reference to specific goal or all goals]
Time Period: [Weekly, Monthly, Quarterly, Project Phase, Custom Range]
Stakeholders: [Who will receive this report and their information needs]
Metrics: [Which goal achievement metrics to include]
Format: [How the report should be formatted - detailed, summary, visual]
```

### Example Input

```
/goalkit.report
Report Type: Progress
Goal: Improve user authentication experience with 70% faster login times
Time Period: Monthly
Stakeholders: Product team, Engineering leadership, UX team
Metrics: Login time improvement percentage, user satisfaction scores, security incidents
Format: Summary with charts, key metrics, and action items
```

## Output

The command generates:
- Structured report based on selected type and audience needs
- Goal achievement metrics and relevant measurements
- Appropriate visualizations and summaries
- Action items and recommendations based on goal progress
- Historical trend analysis for goal metrics
- Stakeholder-specific insights and information

## Report Components

### 1. Report Structure
- **Executive Summary**: High-level overview of goal achievement status
- **Goal Progress**: Detailed metrics related to goal success criteria
- **Key Insights**: Analysis of goal progress and trends
- **Action Items**: Recommended next steps for goal achievement
- **Appendices**: Detailed data and supporting information as needed

### 2. Goal Metrics
- **Primary Metrics**: Core success criteria for goal achievement
- **Secondary Metrics**: Supporting indicators that provide context
- **Trend Analysis**: Historical data showing progress over time
- **Forecasting**: Predictions for future goal achievement based on current trends

### 3. Stakeholder-Specific Content
- **Leadership Reports**: High-level goal achievement and business impact
- **Team Reports**: Detailed progress and technical insights
- **Customer Reports**: User-focused outcomes and satisfaction measures
- **Compliance Reports**: Regulatory or standard adherence metrics

### 4. Actionable Insights
- **Progress Analysis**: Assessment of current goal achievement trajectory
- **Risk Identification**: Potential threats to goal success
- **Opportunity Recognition**: Areas for acceleration or improvement
- **Recommendations**: Specific actions to enhance goal achievement

## Key Differences from Traditional Reporting

| Traditional Reporting | Goal-Driven Reporting |
|----------------------|------------------------|
| Task completion focus | Goal achievement focus |
| Activity-based metrics | Outcome-based metrics |
| Implementation details | Result-oriented information |
| Feature delivery status | Success criteria progress |

## Integration with Other Commands

### Before Using `/goalkit.report`
- **`/goalkit.goal`**: Report metrics must align with specific goal success criteria
- **`/goalkit.track`**: Reports use tracked metrics from ongoing monitoring
- **`/goalkit.measure`**: Reports include metrics defined in measurement approach

### After Using `/goalkit.report`
- **`/goalkit.adapt`**: Reports inform strategy adaptation decisions
- **`/goalkit.learn`**: Reports capture insights and learnings from goal progress
- **`/goalkit.plan`**: Reports inform future planning based on achieved progress
- **`/goalkit.execute`**: Reports guide implementation adjustments based on progress

## Best Practices

### For Report Creation
- **Goal Alignment**: Ensure all metrics directly relate to goal success criteria
- **Audience Focus**: Tailor report content and format to specific stakeholder needs
- **Clarity**: Use clear visualizations and straightforward language
- **Actionability**: Include specific recommendations based on reported data

### For Metric Selection
- **Success-Critical**: Include only metrics that directly measure goal achievement
- **Comprehensive**: Cover all aspects of goal success criteria
- **Measurable**: Ensure metrics are quantifiable and trackable
- **Meaningful**: Select metrics that provide actionable insights

### For Report Distribution
- **Appropriate Frequency**: Match reporting cadence to stakeholder needs and goal timeline
- **Right Stakeholders**: Ensure reports reach all relevant goal stakeholders
- **Clear Access**: Make reports easily accessible to intended audience
- **Follow-up Mechanism**: Provide opportunities for stakeholder questions and feedback

## Common Report Patterns

### Status Report Pattern
- Current goal achievement status
- Recent progress against success criteria
- Upcoming priorities and focus areas
- Identified risks and mitigation status

### Progress Report Pattern
- Accomplishments against success criteria
- Milestone achievements and deliverables
- Performance against timeline expectations
- Quality and outcome metrics
- Lessons learned and process improvements

### Forecast Report Pattern
- Projected goal completion timeline
- Resource requirements for goal completion
- Risk assessment and probability analysis
- Potential challenges and mitigation strategies
- Recommended adjustments to approach

### Retrospective Report Pattern
- What worked well and contributed to goal progress
- What didn't work and lessons learned
- Process improvements identified
- Success metrics analysis and insights
- Future recommendations for goal-driven development

## Report Evolution and Adaptation

### Initial Report Setup
- Define baseline metrics aligned to goal success criteria
- Establish reporting frequency based on goal timeline
- Identify stakeholder information needs
- Set up data collection and visualization systems

### Ongoing Report Improvement
- Refine metrics based on effectiveness in measuring goal achievement
- Adjust reporting format based on stakeholder feedback
- Add new relevant metrics as understanding of goal achievement deepens
- Streamline content to focus on most valuable insights

## Examples

### Example 1: Monthly Progress Report
```
/goalkit.report
Report Type: Progress
Goal: Reduce customer onboarding time by 50% to improve retention
Time Period: October 1-31
Stakeholders: Product team, Customer Success, Executive leadership
Metrics: Onboarding completion time, user retention after onboarding, support ticket volume
Format: Summary dashboard with charts, key metrics, and team insights
```

### Example 2: Quarterly Forecast Report
```
/goalkit.report
Report Type: Forecast
Goal: Increase system performance with 30% faster response times
Time Period: Q4 forecast
Stakeholders: Engineering leadership, Product, QA team
Metrics: Current performance improvements, projected timeline to goal, resource needs
Format: Forecast models with confidence intervals, action plans, and risk assessment
```