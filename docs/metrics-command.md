---
layout: default
title: Metrics Command - Goal Kit Documentation
---

# Metrics Command (`/goalkit.metrics`)

## Overview

The Metrics command creates a comprehensive measurement plan for tracking goal success criteria. It ensures that all metrics are measurable, actionable, and properly instrumented before implementation begins.

## Purpose

The `/goalkit.metrics` command is essential for:

- Validating that success criteria are measurable and actionable
- Establishing baseline measurements before starting work
- Defining clear instrumentation and data collection methods
- Setting decision thresholds for green/yellow/red zones
- Creating dashboards and reporting mechanisms
- Ensuring metrics drive specific actions and decisions

## Usage

```
/goalkit.metrics
Goal: [Reference to specific goal with success criteria]
```

The command will:
1. Extract all success criteria from the goal.md file
2. Validate each metric against quality checklist (Measurable, Actionable, Leading, Bounded, Valuable)
3. Create a detailed measurement plan with instrumentation specifications
4. Define baseline measurements and target values
5. Set up decision thresholds for taking action based on metric values

## Key Components

### Success Criteria Review
Extracts all success criteria from goal.md and validates their quality using the 5-point checklist:
- **Measurable**: Can data be collected reliably and objectively?
- **Actionable**: Will this metric drive specific decisions?
- **Leading**: Does it predict future success (not just lag)?
- **Bounded**: Is there a clear target and timeframe?
- **Valuable**: Does it connect to user/business outcomes?

### Baseline Measurements
Establishes the current state before starting work, providing a reference point for measuring improvement.

### Instrumentation Plan
Defines exactly how to collect data for each metric:
- What to instrument (events, behaviors, system metrics)
- How to collect (tools, platforms, implementation)
- When to measure (frequency, triggers, duration)
- Who analyzes (responsible person, review frequency)

### Decision Thresholds
Defines what actions to take based on metric values:
- **Green Zone (Success)**: Target met, scale and celebrate
- **Yellow Zone (Warning)**: Needs attention, investigate root cause
- **Red Zone (Failure)**: Goal at risk, pivot or escalate

### Measurement Dashboard
Specifies how metrics will be visualized and monitored, including chart types, update frequency, and access controls.

## Best Practices

- Validate all metrics pass the 5-point quality checklist before implementation
- Measure baselines before starting work to enable accurate comparison
- Ensure instrumentation is testable and verifiable
- Define clear decision thresholds that drive specific actions
- Balance metric types: user behavior, business impact, technical quality, and learning
- Document measurement limitations and caveats
- Plan for metric evolution based on learning

## Example

```
/goalkit.metrics
Goal: Implement Secure User Authentication

Success Criteria from goal.md:
- SC-001: 95% of users successfully complete registration on first attempt
- SC-002: Login response time < 3 seconds for 99% of requests
- SC-003: Zero security incidents related to authentication in first 3 months

Metric Quality Validation:
SC-001 (Registration Success Rate):
✓ Measurable: Track registration attempts vs completions via analytics
✓ Actionable: <90% = investigate UX issues, 90-94% = monitor, ≥95% = success
✓ Leading: Predicts user satisfaction and adoption
✓ Bounded: Target 95%, baseline unknown, deadline 8 weeks
✓ Valuable: Smooth registration drives user adoption

Baseline Measurements:
| Metric | Current Baseline | Measurement Date | Method |
|--------|------------------|------------------|--------|
| SC-001 | No existing system | 2024-01-15 | To be measured after launch |
| SC-002 | No existing system | 2024-01-15 | To be measured after launch |
| SC-003 | No existing system | 2024-01-15 | Security audit after 3 months |

Instrumentation Plan:
SC-001 (Registration Success Rate):
- What: Track registration_started, registration_completed, registration_failed events
- How: Google Analytics + custom event tracking in registration flow
- When: Real-time event tracking, daily aggregation
- Who: Product manager reviews daily, engineering investigates failures

Decision Thresholds:
SC-001 (Registration Success Rate):
| Zone | Threshold | Action |
|------|-----------|--------|
| 🟢 Green | ≥ 95% | Success - document best practices, scale |
| 🟡 Yellow | 90-94% | Monitor - investigate common failure patterns |
| 🔴 Red | < 90% | Urgent - UX review, user interviews, pivot if needed |

Dashboard:
- Tool: Grafana with custom analytics integration
- Update Frequency: Real-time with daily summaries
- Charts: Line chart for trends, funnel chart for registration flow
- Access: Product team, engineering team, stakeholders
```

## Integration with Goal-Driven Development

Metrics are the foundation of Goal-Driven Development's outcome-first approach. By creating a detailed measurement plan before implementation, teams ensure that:

1. Success criteria are truly measurable and actionable
2. Progress can be objectively tracked throughout execution
3. Decisions are data-driven rather than opinion-based
4. Learning is captured through quantitative evidence
5. Pivots are triggered by clear thresholds, not gut feelings

The metrics command bridges the gap between defining goals and executing them, ensuring that "done" is objectively measurable.

## CLI Command

You can also view metrics from the command line:

```bash
# View all project metrics and health score
goalkeeper metrics

# View metrics for a specific goal
goalkeeper metrics --goal 001-user-authentication

# View a specific metric with trends
goalkeeper metrics --goal 001-user-authentication --metric "registration_success_rate"

# View metrics for the last 60 days
goalkeeper metrics --days 60

# Output as JSON for integration
goalkeeper metrics --json
```

## Related Commands

- `/goalkit.goal` - Define goals with success criteria (prerequisite)
- `/goalkit.analytics` - View metrics dashboard and trends
- `/goalkit.report` - Generate progress reports including metrics
- `/goalkit.execute` - Implement with continuous measurement

## Common Mistakes to Avoid

- Creating metrics that can't actually be measured with available tools
- Defining metrics without clear decision thresholds
- Skipping baseline measurements
- Using only lagging indicators (add leading indicators too)
- Making metrics too complex to track consistently
- Not validating instrumentation before starting work
- Forgetting to document measurement limitations

## Tips

- Use the metrics template (`templates/metrics-template.md`) as a comprehensive guide
- Validate metrics with stakeholders before implementation
- Test instrumentation early to ensure data quality
- Review and refine metrics based on learning during execution
- Balance quantitative metrics with qualitative feedback
- Document why each metric was chosen and what it predicts
