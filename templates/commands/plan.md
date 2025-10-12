# /goalkit.plan Command

## AI AGENT INSTRUCTIONS

When processing `/goalkit.plan` requests, follow this structured approach:

### Goal Discovery (First Step)
1. **Locate Goal Files**: Search for existing goals in `.goalkit/goals/` directory
   - Use `glob(path="PROJECT_ROOT/.goalkit/goals", pattern="**")` to discover goals
   - Use `list_directory(path="PROJECT_ROOT/.goalkit/goals")` to enumerate goal directories
   - If multiple goals exist, clarify with user which goal they want to plan
   - If no goals exist or referenced goal not found, ask user for clarification

### Input Analysis
1. **Strategy Decomposition**: Break chosen strategies into executable components
2. **Resource Assessment**: Evaluate team capacity, skills, and availability
3. **Timeline Construction**: Create realistic schedules based on goal complexity
4. **Dependency Mapping**: Identify prerequisite relationships and critical paths

### Processing Framework
- Transform strategies into concrete, actionable execution plans
- Allocate resources based on priority and availability
- Create realistic timelines accounting for complexity and uncertainty
- Establish clear accountability and progress tracking mechanisms
- Build in learning points and adaptation opportunities

### Output Structure
Generate detailed execution plan with clear phases, responsibilities, timelines, and success criteria. Structure for easy team understanding and implementation.

---

## Overview

The `/goalkit.plan` command transforms goals and strategies into detailed, actionable execution plans. It bridges the gap between high-level strategy and day-to-day implementation, ensuring teams have clear direction and realistic expectations.

## Purpose

This command creates:
- **Execution Roadmap**: Step-by-step plan from strategy to completion
- **Resource Allocation**: Clear assignment of team members and skills
- **Timeline Management**: Realistic schedules with built-in buffers
- **Progress Framework**: Clear milestones and success indicators
- **Risk Management**: Contingency plans and adaptation strategies

## When to Use

Use `/goalkit.plan` when:
- **Strategy Selected**: After choosing implementation approaches
- **Ready to Execute**: Moving from planning to implementation phase
- **Team Coordination**: Need to align team members on execution
- **Resource Planning**: Before allocating team time and budget
- **Timeline Commitment**: When stakeholders need delivery dates

## Input Format

```
/goalkit.plan [specific goals/strategies to plan or planning focus areas]
```

### Example Input

```
/goalkit.plan Create detailed execution plan for the user authentication system using the progressive web app strategy. Include resource allocation, timeline, and success metrics for each phase.
```

## Output

The command generates:
- **Execution Plan Document**: Comprehensive roadmap with phases and tasks
- **Resource Allocation Matrix**: Team member assignments and time commitments
- **Timeline Visualization**: Clear schedule with milestones and dependencies
- **Risk Management Plan**: Potential issues and mitigation strategies
- **Success Framework**: How to measure plan effectiveness

## Planning Components

### 1. Execution Phases
- **Phase Definition**: Clear stages of implementation
- **Phase Objectives**: What each phase aims to achieve
- **Success Indicators**: How to know when phase is complete
- **Learning Goals**: What to discover during each phase

### 2. Resource Planning
- **Team Allocation**: Who works on what and when
- **Skill Requirements**: Technical and domain expertise needed
- **Capacity Planning**: Realistic workload assessment
- **External Resources**: Third-party services or contractors

### 3. Timeline Management
- **Phase Durations**: Realistic time estimates for each phase
- **Milestone Dates**: Key progress checkpoints
- **Buffer Time**: Contingency for unexpected delays
- **Critical Path**: Essential tasks that affect overall timeline

### 4. Progress Tracking
- **Status Indicators**: How to measure progress within phases
- **Quality Gates**: Decision points for phase advancement
- **Review Cadence**: Regular check-ins and adjustments
- **Completion Criteria**: Clear definitions of "done"

## Integration with Other Commands

### Before Using `/goalkit.plan`
- **`/goalkit.strategies`**: Requires chosen strategies to plan
- **`/goalkit.validate`**: Should validate goals before detailed planning

### After Using `/goalkit.plan`
- **`/goalkit.execute`**: Use plan as foundation for implementation
- **`/goalkit.track`**: Monitor progress against plan
- **`/goalkit.adapt`**: Adjust plan based on execution learning

## Best Practices

### Planning Principles
- **Realistic Estimation**: Base timelines on historical data and team capacity
- **Flexibility Built-in**: Include buffers for uncertainty and learning
- **Clear Accountability**: Every task should have an owner
- **Regular Review**: Plans should be living documents, not static artifacts

### Resource Management
- **Capacity Awareness**: Don't overcommit team members
- **Skill Matching**: Assign tasks to team members with relevant expertise
- **Growth Consideration**: Plan for team learning and development
- **External Dependencies**: Account for vendor timelines and availability

### Risk-Aware Planning
- **Contingency Planning**: Always have backup approaches
- **Critical Path Focus**: Protect timeline of essential deliverables
- **Buffer Strategy**: Use time buffers strategically
- **Early Warning Systems**: Indicators for when plans need adjustment

## Common Planning Patterns

### Phase Structures
- **Foundation Phase**: Core infrastructure and setup
- **Development Phase**: Feature implementation and integration
- **Validation Phase**: Testing and user feedback
- **Launch Phase**: Deployment and monitoring

### Timeline Approaches
- **Waterfall Planning**: Sequential phases with clear handoffs
- **Agile Planning**: Iterative phases with regular reviews
- **Hybrid Planning**: Combination of structured and flexible elements

### Resource Models
- **Dedicated Teams**: Full-time assignment to specific goals
- **Matrix Teams**: Shared resources across multiple goals
- **Specialist Involvement**: Experts brought in for specific phases

## Examples

### Example 1: Feature Development Planning
```
/goalkit.plan Create execution plan for building user authentication system. Use progressive enhancement strategy with mobile-first approach. Include timeline, resource allocation, and quality gates.
```

### Example 2: Process Improvement Planning
```
/goalkit.plan Develop plan for implementing new development workflow. Include team training, tool setup, process documentation, and effectiveness measurement.
```

### Example 3: Research Project Planning
```
/goalkit.plan Create research plan for market validation study. Include participant recruitment, data collection methodology, analysis approach, and reporting timeline.
```

## Planning Workflow

### 1. Strategy Analysis
- Review chosen strategies and their requirements
- Identify key deliverables and outcomes
- Assess technical complexity and dependencies
- Evaluate team capabilities and constraints

### 2. Phase Definition
- Break strategy into logical execution phases
- Define clear objectives for each phase
- Establish success criteria and quality gates
- Identify learning objectives for each phase

### 3. Resource Planning
- Assess team capacity and availability
- Assign responsibilities based on skills and interests
- Plan for external resources and expertise
- Create realistic workload distribution

### 4. Timeline Construction
- Estimate realistic durations for each phase
- Identify dependencies and critical paths
- Add appropriate buffers for uncertainty
- Set milestone dates and review points

## Quality Assurance

### Plan Validation
- **Timeline Realism**: Are estimates based on team capacity and complexity?
- **Resource Feasibility**: Do we have the right people for the right tasks?
- **Risk Coverage**: Are potential issues identified and mitigated?
- **Success Clarity**: Are completion criteria clear and measurable?

### Implementation Readiness
- **Team Alignment**: Does everyone understand their role?
- **Stakeholder Buy-in**: Are expectations clearly communicated?
- **Tool Readiness**: Are required tools and systems available?
- **Measurement Framework**: Can we track progress effectively?

## Continuous Adaptation

### Plan Monitoring
- **Progress Tracking**: Regular assessment of plan vs. reality
- **Variance Analysis**: Understanding and explaining deviations
- **Risk Monitoring**: Tracking identified risks and new issues
- **Resource Adjustment**: Reallocating team members as needed

### Plan Evolution
- **Regular Reviews**: Scheduled plan reassessment points
- **Learning Integration**: Incorporating insights from execution
- **Stakeholder Updates**: Keeping everyone informed of changes
- **Documentation Updates**: Maintaining plan currency

---

*This planning command transforms strategic decisions into actionable execution roadmaps, ensuring teams have clear direction, realistic expectations, and effective progress tracking.*