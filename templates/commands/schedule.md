# /goalkit.schedule Command

## AI AGENT INSTRUCTIONS

When processing `/goalkit.schedule` requests, follow this structured approach:

### Input Analysis
1. **Identify Goal Dependencies**: Extract how schedule supports specific project goals from user input
2. **Map Resource Constraints**: Identify team member availability and capacity limitations
3. **Determine Critical Path**: Identify dependencies and sequences that affect goal achievement
4. **Assess Timeline Feasibility**: Evaluate if proposed timeline supports goal success criteria

### Processing Framework
- Focus on goal-aligned scheduling rather than arbitrary deadlines
- Generate realistic timelines based on goal complexity and resource availability
- Identify critical path dependencies that impact goal achievement
- Create monitoring and adjustment procedures for timeline management

### Output Structure
Use the template sections below to structure your response. Ensure alignment with existing project goals and maintain consistency with goal-driven development principles.

---

## Overview

The `/goalkit.schedule` command creates detailed project timelines with dependencies, resource allocation, and milestone tracking. This command generates schedules that directly support goal achievement while accounting for resource constraints and dependencies.

## Purpose

This command creates structured timelines that:
- Align project phases with goal achievement requirements
- Account for resource availability and capacity constraints
- Identify and manage critical path dependencies
- Provide frameworks for progress monitoring and timeline adjustment

## When to Use

Use `/goalkit.schedule` when:
- Planning project execution with specific timeframes aligned to goals
- Managing dependencies between milestones or goals
- Allocating resources across different project phases
- Tracking progress against time-based goal metrics
- Forecasting goal completion based on available resources
- Communicating realistic timelines to stakeholders

## Input Format

```
/goalkit.schedule
Goal: [Reference to specific goal being scheduled]
Timeline: [Overall project duration and key date constraints]
Phases: [Major project phases with duration estimates]
Milestones: [Key milestones with target dates aligned to goals]
Dependencies: [Dependencies between tasks/milestones that affect goal achievement]
Resources: [Team members and their availability/capacity]
Constraints: [Time, resource, or external constraints affecting goal achievement]
```

### Example Input

```
/goalkit.schedule
Goal: Improve user authentication experience with 70% faster login times
Timeline: 3-month timeline with beta release at 2 months, final release at 3 months
Phases: Research (2 weeks), Implementation (6 weeks), Testing (3 weeks), Deployment (1 week)
Milestones: Architecture decision (week 1), Core functionality complete (week 5), Beta testing complete (week 8), Production deployment (week 12)
Dependencies: API authentication changes must be completed before frontend integration
Resources: 2 developers (full-time), 1 designer (part-time), 1 QA engineer (part-time)
Constraints: Major product launch in 4 months, 2 weeks of team vacation time during the period
```

## Output

The command generates:
- Goal-aligned timeline with phases and milestones
- Resource allocation schedule based on goal priorities
- Dependency map with critical path for goal achievement
- Risk assessment for timeline feasibility regarding goal success
- Monitoring and adjustment procedures for timeline management

## Schedule Components

### 1. Goal-Aligned Timeline Structure
- **Phase Definitions**: Major project phases aligned with goal achievement requirements
- **Duration Estimates**: Realistic timeframes based on goal complexity and available resources
- **Buffer Planning**: Contingency time for unexpected challenges that could affect goals
- **Critical Path Analysis**: Sequences of activities that directly impact goal delivery

### 2. Resource Management
- **Capacity Planning**: Matching resource availability to goal timeline requirements
- **Assignment Strategy**: Allocating team members to activities that best support goals
- **Availability Tracking**: Accounting for time off, competing priorities, and capacity constraints
- **Contingency Planning**: Alternative resource strategies if primary resources become unavailable

### 3. Dependency Management
- **Goal Dependencies**: Relationships between activities that affect goal achievement
- **Critical Path Identification**: Sequences that directly impact goal delivery timeline
- **Risk Mitigation**: Strategies to prevent dependency-related delays from affecting goals
- **Parallel Opportunities**: Areas where work can be done simultaneously to support goals faster

### 4. Monitoring Framework
- **Progress Checkpoints**: Regular intervals to assess goal progress against timeline
- **Warning Indicators**: Early signs that timeline may not support goal achievement
- **Adjustment Protocols**: Procedures for modifying timeline when goals are at risk
- **Stakeholder Communication**: Reporting mechanisms for timeline status and changes

## Key Differences from Traditional Scheduling

| Traditional Scheduling | Goal-Driven Scheduling |
|------------------------|------------------------|
| Feature-based deadlines | Outcome-focused timelines |
| Fixed task durations | Flexible phases aligned to goal achievement |
| Resource allocation by availability | Resource allocation by goal impact |
| Linear timeline expectations | Adaptive timelines that accommodate learning |

## Integration with Other Commands

### Before Using `/goalkit.schedule`
- **`/goalkit.goal`**: Schedule must align with goal success criteria and requirements
- **`/goalkit.milestones`**: Timeline should support milestone achievement dates
- **`/goalkit.plan`**: Schedule builds on detailed execution planning

### After Using `/goalkit.schedule`
- **`/goalkit.execute`**: Implementation follows the established timeline
- **`/goalkit.track`**: Progress monitoring against scheduled milestones
- **`/goalkit.adapt`**: Timeline adjustments based on goal achievement progress
- **`/goalkit.dependencies`**: Further detailed dependency analysis if needed

## Best Practices

### For Goal-Aligned Planning
- **Outcome-Focused Timelines**: Design phases around goal achievement rather than feature completion
- **Realistic Estimation**: Account for complexity and learning when estimating duration
- **Buffer Integration**: Include contingency time for unexpected challenges that affect goals
- **Flexibility Recognition**: Acknowledge that timelines may need adjustment as learning occurs

### For Resource Management
- **Goal Priority Alignment**: Assign best resources to activities with highest goal impact
- **Capacity Reality**: Account for actual availability rather than ideal scenarios
- **Skill-Goal Matching**: Match resource strengths to activities that most affect goal achievement
- **Availability Forecasting**: Plan for known absences and competing priorities

### For Dependency Management
- **Goal-Critical Dependencies**: Focus on dependencies that directly impact goal achievement
- **Parallel Work Identification**: Find opportunities to work simultaneously on goal-supporting activities
- **Risk Assessment**: Identify dependencies that could threaten goal achievement
- **Contingency Planning**: Develop alternative paths when critical dependencies are at risk

## Common Scheduling Patterns

### Iterative Development Schedule
- Cycles aligned with milestone achievement rather than fixed sprints
- Regular evaluation points to assess goal progress
- Flexible phase durations that adapt to learning
- Continuous integration with goal validation

### Milestone-Driven Schedule
- Timeline organized around key goal-measuring milestones
- Buffer time between milestones for integration and validation
- Clear decision points for continuing or adjusting goals
- Stakeholder review points aligned with milestone completion

### Resource-Constrained Schedule
- Timeline based on actual resource availability
- Phased goal achievement when resources are limited
- Parallel goal tracks when multiple resources are available
- Realistic delivery windows based on capacity

## Validation and Iteration

### Schedule Review Process
- **Regular Assessment**: Evaluate timeline alignment with goal progress
- **Feasibility Validation**: Ensure current timeline still supports goal achievement
- **Resource Utilization**: Verify resource allocation supports goal priorities
- **Dependency Verification**: Confirm that critical path analysis remains accurate

### Schedule Evolution
- **Adaptive Adjustment**: Modify timeline based on actual progress toward goals
- **Resource Reallocation**: Adjust assignments based on goal impact and availability
- **Phase Refinement**: Improve phase definitions based on execution experience
- **Constraint Recognition**: Identify and address new constraints that affect goals

## Examples

### Example 1: Product Feature Schedule
```
/goalkit.schedule
Goal: Reduce checkout time by 50% to improve conversion rates
Timeline: 8 weeks with prototype at 3 weeks, testing at 6 weeks, production release at 8 weeks
Phases: Research & Design (2 weeks), Frontend Implementation (3 weeks), Backend Integration (2 weeks), Testing & Optimization (1 week)
Milestones: UX prototype complete (week 2), Frontend ready for integration (week 5), Backend integration complete (week 7), Production deployment (week 8)
Dependencies: Backend API changes must be completed before frontend integration
Resources: 1 Frontend developer (full-time), 1 Backend developer (full-time), 1 UX Designer (part-time)
Constraints: Major marketing campaign in 10 weeks requiring performance improvement, 2 days of team off-site during week 4
```

### Example 2: System Migration Schedule
```
/goalkit.schedule
Goal: Migrate legacy system to cloud platform with 99.9% uptime maintenance
Timeline: 16 weeks with proof of concept at 4 weeks, staging completion at 12 weeks, production migration at 16 weeks
Phases: Architecture & Planning (3 weeks), Infrastructure Setup (4 weeks), Data Migration (6 weeks), Testing & Go-Live (3 weeks)
Milestones: Architecture approval (week 3), Infrastructure ready (week 7), Data migration complete (week 13), Production migration (week 16)
Dependencies: Vendor approval for cloud services, completion of data cleanup before migration
Resources: 2 DevOps engineers (full-time), 1 Database specialist (full-time), 1 Security specialist (part-time)
Constraints: Regulatory deadline in 20 weeks, maintenance window limited to weekends, data integrity requirements
```