# /goalkit.risk Command

## AI AGENT INSTRUCTIONS

When processing `/goalkit.risk` requests, follow this structured approach:

### Input Analysis
1. **Identify Goal Risks**: Extract risks that specifically threaten goal achievement from user input
2. **Assess Risk Impact**: Evaluate how each risk could affect goal success criteria
3. **Determine Risk Probability**: Assess likelihood of each risk occurring based on context
4. **Map Mitigation Strategies**: Identify potential approaches to reduce risk impact or probability

### Processing Framework
- Focus on risks that directly threaten goal achievement rather than general project risks
- Generate quantified risk assessments with clear probability and impact measures
- Create specific mitigation plans tied to goal success criteria
- Establish monitoring procedures for early risk detection

### Output Structure
Use the template sections below to structure your response. Ensure alignment with existing project goals and maintain consistency with goal-driven development principles.

---

## Overview

The `/goalkit.risk` command identifies, assesses, and creates mitigation plans for project risks that could impact goal achievement. This command creates a comprehensive risk management framework focused specifically on achieving measurable goals.

## Purpose

This command creates risk management strategies that:
- Identify risks that directly threaten goal achievement
- Quantify risk probability and impact on goal success criteria
- Establish specific mitigation and contingency plans
- Create monitoring systems for early risk detection and response

## When to Use

Use `/goalkit.risk` when:
- Beginning a new goal or project to identify potential threats
- Planning implementation strategies to address potential challenges
- During milestone planning to identify potential blockers
- When adapting strategies based on emerging risks
- Before committing to timeline or resource estimates
- Conducting regular goal progress assessments
- Preparing for major goal or milestone transitions

## Input Format

```
/goalkit.risk
Goal: [Reference to specific goal being assessed for risks]
Risk Categories: [Technical, business, resource, timeline, external factors]
Probability: [How likely each risk is to occur - Low/Medium/High or percentage]
Impact: [What happens to goal achievement if each risk materializes]
Mitigation: [How to reduce probability or impact of each risk]
Contingency: [What to do if each risk occurs despite mitigation efforts]
Owner: [Who is responsible for monitoring each risk]
Review Frequency: [How often to reassess risks and mitigation strategies]
```

### Example Input

```
/goalkit.risk
Goal: Improve mobile app performance with 40% faster load times
Risk Categories: Technical, resource, external dependencies
Probability: Performance gains may be limited by device capabilities (High)
Impact: Goal may not be achieved on older devices, affecting overall success metrics
Mitigation: Implement progressive performance optimization based on device capability
Contingency: Adjust success metrics to account for device-specific performance targets
Owner: Lead mobile developer
Review Frequency: Bi-weekly during implementation, weekly during testing
```

## Output

The command generates:
- Comprehensive risk register with all goal-threatening risks identified
- Risk matrix showing probability vs. impact for each identified risk
- Detailed mitigation and contingency plans linked to goal success criteria
- Risk monitoring procedures with early warning indicators
- Integration with goal tracking and adaptation processes

## Risk Management Components

### 1. Risk Identification
- **Technical Risks**: Architecture, performance, scalability, security concerns affecting goals
- **Resource Risks**: Availability, skills, changes in team that threaten goal achievement
- **Timeline Risks**: Unrealistic expectations, dependencies affecting goal delivery
- **Business Risks**: Changing requirements, market conditions affecting goal relevance
- **External Risks**: Third-party dependencies, regulations that could block goal achievement

### 2. Risk Assessment
- **Probability Evaluation**: Likelihood of each risk occurring based on project context
- **Impact Analysis**: Effect of each risk on goal success criteria and metrics
- **Risk Scoring**: Quantified measure combining probability and impact
- **Risk Prioritization**: Ranking of risks by their threat level to goal achievement

### 3. Mitigation Strategies
- **Prevention Measures**: Actions to reduce the probability of risks occurring
- **Impact Reduction**: Actions to minimize the effect of risks on goal achievement
- **Risk Acceptance**: Criteria for accepting certain risks without mitigation
- **Escalation Procedures**: When and how to escalate high-risk situations

### 4. Monitoring Framework
- **Early Warning Indicators**: Signs that specific risks are materializing
- **Review Schedule**: Regular assessment intervals for risk status
- **Reporting Mechanisms**: How risk status is communicated to stakeholders
- **Adaptation Triggers**: Conditions that prompt strategy changes due to risks

## Key Differences from Traditional Risk Management

| Traditional Risk Management | Goal-Driven Risk Management |
|----------------------------|-----------------------------|
| General project risks | Goal-threatening risks |
| Task completion impact | Goal achievement impact |
| Standard mitigation approaches | Goal-specific mitigation strategies |
| Periodic risk reviews | Continuous goal-focused monitoring |

## Integration with Other Commands

### Before Using `/goalkit.risk`
- **`/goalkit.goal`**: Risk assessment must align with specific goal success criteria
- **`/goalkit.strategies`**: Risks may influence strategy selection and implementation
- **`/goalkit.milestones`**: Risk assessment should consider milestone-specific threats

### After Using `/goalkit.risk`
- **`/goalkit.plan`**: Risk mitigation plans integrated into execution planning
- **`/goalkit.execute`**: Implementation accounts for identified risks and mitigation plans
- **`/goalkit.track`**: Risk indicators monitored alongside goal progress metrics
- **`/goalkit.adapt`**: Risk realization triggers strategy adaptation based on contingency plans

## Best Practices

### For Risk Identification
- **Goal-Focused**: Identify only risks that threaten specific goal achievement
- **Comprehensive Coverage**: Consider all risk categories that could impact the goal
- **Stakeholder Input**: Gather risk perspectives from all goal stakeholders
- **Historical Review**: Consider risks that affected similar goals in the past

### For Risk Assessment
- **Quantified Measures**: Use specific probabilities and measurable impacts
- **Goal Relevance**: Focus on how risks affect goal success criteria
- **Realistic Evaluation**: Base assessments on actual project context and constraints
- **Regular Updates**: Adjust assessments as new information becomes available

### For Mitigation Planning
- **Goal-Specific**: Create mitigation plans tailored to specific goal requirements
- **Actionable Steps**: Ensure all mitigation plans contain concrete, implementable actions
- **Resource Allocation**: Assign appropriate resources to high-priority risk mitigation
- **Contingency Preparation**: Develop ready-to-execute contingency plans for high-impact risks

## Common Risk Patterns

### Technology Adoption Risks
- New technology learning curve affecting goal timeline
- Integration challenges with existing systems
- Performance not meeting expectations
- Scalability limitations emerging later

### Resource Dependency Risks
- Key team member unavailability
- Insufficient expertise for goal-specific requirements
- Competing priorities affecting goal commitment
- Budget constraints limiting goal achievement options

### External Dependency Risks
- Third-party service reliability
- Regulatory changes affecting goal approach
- Market condition changes making goal less relevant
- Vendor support or capability changes

## Risk Evolution Process

### Initial Risk Assessment
- Comprehensive identification of all potential goal-threatening risks
- Baseline probability and impact assessments
- Initial mitigation strategy development
- Assignment of risk ownership and monitoring responsibilities

### Ongoing Risk Management
- Regular updates to probability and impact assessments
- Adjustment of mitigation strategies based on goal progress
- Addition of newly identified risks
- Retirement of risks that are no longer relevant

## Examples

### Example 1: Feature Development Risk Assessment
```
/goalkit.risk
Goal: Implement real-time collaboration feature with 95% reliability
Risk Categories: Technical, performance, complexity
Probability: Architecture complexity may cause delays (Medium)
Impact: Goal may not be achieved within 3-month timeline, affecting product launch
Mitigation: Implement feature in phases, starting with basic real-time functionality
Contingency: Launch with limited collaboration features, expand based on user feedback
Owner: Technical lead
Review Frequency: Weekly during implementation, bi-weekly during testing
```

### Example 2: Performance Optimization Risk Assessment
```
/goalkit.risk
Goal: Reduce API response time by 60% to improve user experience
Risk Categories: Technical, dependency, resource
Probability: Database optimization may require more time than allocated (High)
Impact: Goal may not be achieved, affecting user satisfaction metrics
Mitigation: Implement caching layer as an alternative approach to performance gains
Contingency: Adjust goal to 40% improvement if database optimization proves too complex
Owner: Backend team lead
Review Frequency: Bi-weekly during implementation, weekly during performance testing
```