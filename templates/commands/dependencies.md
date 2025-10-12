# /goalkit.dependencies Command

## AI AGENT INSTRUCTIONS

When processing `/goalkit.dependencies` requests, follow this structured approach:

### Input Analysis
1. **Identify Goal Dependencies**: Extract dependencies that specifically impact goal achievement from user input
2. **Map Dependency Types**: Categorize dependencies by type (internal, external, technical, business, etc.)
3. **Assess Criticality**: Determine the impact of each dependency on goal success criteria
4. **Evaluate Risk Factors**: Identify potential risks associated with each dependency for goal achievement

### Processing Framework
- Focus on dependencies that directly impact goal success rather than general project dependencies
- Generate dependency maps that clearly show goal achievement pathways
- Create risk assessments specific to how dependencies affect goal timelines
- Establish contingency plans that maintain goal achievement despite dependency challenges

### Output Structure
Use the template sections below to structure your response. Ensure alignment with existing project goals and maintain consistency with goal-driven development principles.

---

## Overview

The `/goalkit.dependencies` command maps and manages dependencies between goals, milestones, and tasks to optimize project flow and identify critical paths for goal achievement. This command creates dependency frameworks specifically focused on ensuring goal success rather than just managing project tasks.

## Purpose

This command creates dependency management frameworks that:
- Identify dependencies that directly impact goal achievement
- Map pathways to successful goal completion with clear sequence requirements
- Assess risks associated with goal-critical dependencies
- Create contingency plans that maintain goal success despite dependency challenges

## When to Use

Use `/goalkit.dependencies` when:
- Planning complex projects with multiple interrelated goals
- Establishing milestone sequences and prerequisites for goal achievement
- Identifying critical path and potential bottlenecks for goal delivery
- Coordinating work among different team members or teams to achieve goals
- Adjusting plans due to changes in one area affecting goal achievement
- Evaluating how external factors might impact goal success
- Optimizing resource allocation to support critical goal dependencies

## Input Format

```
/goalkit.dependencies
Goal: [Reference to specific goal and its success criteria]
Internal Dependencies: [Dependencies within the project that affect goal achievement]
External Dependencies: [Dependencies on other projects, teams, vendors, or external factors]
Sequence Requirements: [What must be completed in sequence to achieve the goal]
Parallel Opportunities: [What can be done simultaneously to accelerate goal achievement]
Critical Path: [Sequence of dependent activities that determines goal delivery timeline]
Risk Areas: [Dependencies that pose risks to goal achievement]
Contingency Plans: [What to do if key dependencies fail or are delayed]
Dependency Owners: [Who is responsible for managing each dependency]
```

### Example Input

```
/goalkit.dependencies
Goal: Implement secure user authentication with 99.9% uptime
Internal Dependencies: Database schema updates, security module development, UI components
External Dependencies: Third-party identity provider API, security audit approval, infrastructure setup
Sequence Requirements: Security module completion before UI integration
Parallel Opportunities: UI development can happen simultaneously with backend development
Critical Path: Infrastructure setup -> security module -> UI integration -> security audit
Risk Areas: Third-party API availability, security audit timeline, infrastructure provisioning
Contingency Plans: Alternative authentication provider if primary fails, internal audit if external delayed
Dependency Owners: Infrastructure team, security architect, frontend team lead
```

## Output

The command generates:
- Goal-focused dependency map showing all relationships that impact goal achievement
- Critical path analysis specifically for goal delivery timeline
- Risk assessment for each dependency's impact on goal success
- Recommendations for optimizing dependency management for goal achievement
- Contingency plans for maintaining goal success despite dependency challenges
- Responsibility assignments for managing goal-critical dependencies

## Dependency Components

### 1. Goal-Centric Dependency Mapping
- **Direct Impact Dependencies**: Dependencies that directly affect goal success criteria
- **Relationship Classification**: Clear categorization of dependency types and impacts
- **Dependency Strength**: Assessment of how strongly each dependency affects goal achievement
- **Timeline Implications**: How each dependency influences goal delivery schedule

### 2. Critical Path Analysis for Goals
- **Goal-Delivery Path**: Sequence of activities that determines goal achievement timeline
- **Bottleneck Identification**: Activities that could delay goal delivery
- **Timeline Optimization**: Opportunities to compress goal achievement timeline
- **Impact Assessment**: How delays in critical activities affect goal success

### 3. Dependency Risk Management
- **Risk Prioritization**: Identification of dependencies with highest risk to goal success
- **Mitigation Strategies**: Specific approaches to reduce dependency risks
- **Early Warning Indicators**: Signs that indicate potential dependency issues
- **Escalation Procedures**: When and how to escalate dependency-related risks

### 4. Optimization Strategies
- **Dependency Reduction**: Opportunities to eliminate or minimize dependencies
- **Parallel Execution**: Ways to execute dependent activities simultaneously
- **Resource Allocation**: Optimized resource distribution across dependencies
- **Alternative Pathways**: Backup approaches for goal achievement

## Key Differences from Traditional Dependency Management

| Traditional Dependency Management | Goal-Driven Dependency Management |
|-----------------------------------|-----------------------------------|
| Task completion dependencies | Goal achievement dependencies |
| General project sequencing | Goal-focused critical path |
| Resource allocation by availability | Resource allocation by goal impact |
| Dependency tracking for tasks | Dependency tracking for outcomes |

## Integration with Other Commands

### Before Using `/goalkit.dependencies`
- **`/goalkit.goal`**: Dependencies must align with and support specific goal success criteria
- **`/goalkit.milestones`**: Dependencies may affect milestone sequences and timing
- **`/goalkit.risk`**: Dependencies directly contribute to project risk profile

### After Using `/goalkit.dependencies`
- **`/goalkit.schedule`**: Dependencies inform project scheduling and timeline planning
- **`/goalkit.plan`**: Dependencies integrated into detailed execution planning
- **`/goalkit.execute`**: Implementation follows dependency sequences and management plans
- **`/goalkit.track`**: Dependencies monitored alongside goal progress metrics

## Best Practices

### For Goal-Focused Dependency Analysis
- **Success Impact Focus**: Identify only dependencies that directly impact goal success
- **Clear Relationships**: Map dependencies with clear explanations of how they affect goals
- **Quantified Impact**: Assess the specific impact of each dependency on goal achievement
- **Stakeholder Alignment**: Ensure dependency management aligns with stakeholder expectations

### For Critical Path Management
- **Goal-Driven Paths**: Focus on the path that most directly impacts goal delivery
- **Bottleneck Recognition**: Identify and address activities that slow goal achievement
- **Timeline Sensitivity**: Understand how delays in critical activities affect goal success
- **Optimization Opportunities**: Continuously look for ways to improve the critical path

### For Risk Management
- **Dependency Risk Assessment**: Evaluate how each dependency could impact goal success
- **Mitigation Planning**: Create specific plans to reduce dependency risks
- **Monitoring Systems**: Implement systems to detect dependency issues early
- **Contingency Development**: Develop backup plans for critical dependencies

## Common Dependency Patterns

### Technical Dependency Patterns
- Architecture dependencies that affect goal implementation
- Component dependencies that determine integration sequence
- Resource dependencies that impact development pace
- Infrastructure dependencies that enable goal functionality

### External Dependency Patterns
- Third-party service dependencies and their impact on goal delivery
- Regulatory approval dependencies affecting goal validation
- Vendor dependencies and their potential impact on timelines
- Stakeholder dependencies and decision timing requirements

### Organizational Dependency Patterns
- Team availability dependencies affecting goal progress
- Budget approval dependencies impacting goal scope
- Resource allocation dependencies affecting goal execution
- Communication dependencies affecting coordination

## Dependency Evolution Process

### Initial Dependency Mapping
- Comprehensive identification of all dependencies affecting goal achievement
- Classification of dependencies by type and impact level
- Assessment of dependency criticality to goal success
- Initial risk evaluation for each identified dependency

### Ongoing Dependency Management
- Regular updates to dependency maps as project evolves
- Adjustment of critical path based on actual progress
- Refinement of risk assessments based on experience
- Optimization of dependency management approaches

## Examples

### Example 1: Feature Development Dependencies
```
/goalkit.dependencies
Goal: Implement real-time data visualization with 95% accuracy
Internal Dependencies: Data processing pipeline, visualization components, performance optimization
External Dependencies: Third-party charting library, data source availability, cloud infrastructure
Sequence Requirements: Data pipeline completion before visualization integration
Parallel Opportunities: UI design can happen simultaneously with backend development
Critical Path: Infrastructure setup -> data pipeline -> visualization engine -> accuracy validation
Risk Areas: Third-party library limitations, data source reliability, performance constraints
Contingency Plans: Alternative charting library, data caching strategy, performance fallback
Dependency Owners: Data engineering team, frontend team, cloud infrastructure team
```

### Example 2: System Migration Dependencies
```
/goalkit.dependencies
Goal: Migrate legacy user database with zero data loss and minimal downtime
Internal Dependencies: Data schema conversion, API compatibility, testing environment setup
External Dependencies: Vendor support for old system, hardware provisioning, security clearance
Sequence Requirements: Schema conversion must complete before data transfer
Parallel Opportunities: Testing environment setup while schema conversion happens
Critical Path: Schema mapping -> data validation -> transfer execution -> compatibility testing
Risk Areas: Data integrity during transfer, API compatibility, vendor support availability
Contingency Plans: Rollback procedures, parallel operation mode, extended support contract
Dependency Owners: Database team, migration specialists, security team
```