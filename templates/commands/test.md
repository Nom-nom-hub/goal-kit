# /goalkit.test Command

## AI AGENT INSTRUCTIONS

When processing `/goalkit.test` requests, follow this structured approach:

### Input Analysis
1. **Identify Goal Success Criteria**: Extract specific success metrics and validation requirements from user input
2. **Map Testing Strategy**: Determine appropriate testing approaches that validate goal achievement
3. **Assess Coverage Needs**: Identify what aspects of the goal require validation through testing
4. **Define Quality Gates**: Establish acceptance criteria for goal achievement based on test results

### Processing Framework
- Focus on tests that validate specific goal success criteria
- Generate comprehensive testing strategies aligned with outcome measurement
- Create specific test scenarios that validate goal achievement
- Establish quality standards that support measurable outcomes

### Output Structure
Use the template sections below to structure your response. Ensure alignment with existing project goals and maintain consistency with goal-driven development principles.

---

## Overview

The `/goalkit.test` command designs and verifies testing strategies that support specific goals and validate success criteria achievement. This command creates comprehensive testing approaches focused on measuring and ensuring goal success rather than just validating implementation details.

## Purpose

This command creates testing strategies that:
- Validate specific goal success criteria and metrics
- Establish quality standards aligned with desired outcomes
- Create test coverage that verifies goal achievement
- Define acceptance criteria for milestone validation

## When to Use

Use `/goalkit.test` when:
- Planning implementation of a goal to ensure it meets success criteria
- Defining acceptance criteria for milestones and deliverables
- Establishing quality assurance procedures for goal achievement
- Validating that implementation meets success criteria
- Creating test coverage aligned with business outcomes
- Setting up quality gates for goal validation
- Planning test automation that supports goal measurement

## Input Format

```
/goalkit.test
Goal: [Reference to specific goal being tested and its success criteria]
Test Types: [Unit, integration, end-to-end, performance, security, user experience, etc.]
Coverage: [What aspects of the goal need testing to validate success]
Scenarios: [Specific test scenarios that directly validate goal success criteria]
Tools: [Testing tools and frameworks to use for goal validation]
Metrics: [How to measure both test effectiveness and goal achievement]
Automation: [Which tests should be automated for continuous goal validation]
Quality Gates: [Acceptance criteria that must be met for goal validation]
```

### Example Input

```
/goalkit.test
Goal: Improve mobile app performance with 50% faster load times and 99.9% uptime
Test Types: Performance, stress, reliability, user experience
Coverage: App loading times across different network conditions and devices, system reliability under load
Scenarios: App launch time measurement, sustained usage scenarios, peak load situations
Tools: JMeter for performance testing, custom monitoring for uptime tracking
Metrics: Load time measurements, uptime percentage, user session success rate
Automation: Automated performance regression testing, continuous uptime monitoring
Quality Gates: Load time < 3 seconds on 95% of devices, 99.9% uptime maintained
```

## Output

The command generates:
- Comprehensive testing strategy aligned with specific goal validation
- Test plan covering all goal success criteria
- Specific test case definitions that validate goal achievement
- Tool recommendations and setup guidance for goal validation
- Quality gates and acceptance criteria for goal achievement
- Monitoring and validation procedures for ongoing goal verification

## Testing Strategy Components

### 1. Goal-Aligned Test Strategy
- **Success Criteria Validation**: Tests specifically designed to validate goal metrics
- **Outcome-Focused Testing**: Testing approach focused on measuring outcomes rather than features
- **Risk-Based Prioritization**: Testing priorities based on risk to goal achievement
- **Quality Standards**: Established standards that ensure goal success is achieved

### 2. Test Planning Framework
- **Test Type Selection**: Appropriate test types for validating specific goal success criteria
- **Coverage Requirements**: What aspects need testing to validate goal achievement
- **Integration Validation**: How different components work together to achieve the goal
- **Performance and Security**: Testing requirements for goal-specific performance and security needs

### 3. Test Case Development
- **Goal Validation Scenarios**: Test cases that directly validate goal achievement
- **Edge Cases and Error Conditions**: Testing for boundary conditions that affect goal success
- **Performance Benchmarks**: Validation of goal-specific performance requirements
- **User Experience Validation**: Testing that validates goal success from user perspective

### 4. Implementation and Execution
- **Tool Recommendations**: Suggested testing tools and frameworks for goal validation
- **Environment Setup**: Testing environment configuration for accurate goal validation
- **Automation Strategy**: Which tests to automate for continuous goal validation
- **Continuous Integration**: How testing integrates with ongoing goal achievement validation

## Key Differences from Traditional Testing

| Traditional Testing | Goal-Driven Testing |
|---------------------|---------------------|
| Feature-focused test cases | Goal achievement-focused validation |
| Implementation coverage | Success criteria validation |
| Defect identification | Outcome verification |
| Standard quality metrics | Goal-specific quality gates |

## Integration with Other Commands

### Before Using `/goalkit.test`
- **`/goalkit.goal`**: Testing strategy must align with and validate specific goal success criteria
- **`/goalkit.milestones`**: Tests support milestone acceptance criteria
- **`/goalkit.measure`**: Testing metrics align with defined measurement approach

### After Using `/goalkit.test`
- **`/goalkit.execute`**: Implementation follows testing strategy and quality gates
- **`/goalkit.track`**: Test results contribute to goal achievement monitoring
- **`/goalkit.validate`**: Testing is part of broader validation approach
- **`/goalkit.adapt`**: Test results may inform strategy adaptation for goal achievement

## Best Practices

### For Goal-Aligned Testing
- **Success Criteria Focus**: Ensure every test case directly relates to goal validation
- **Measurable Outcomes**: Design tests that provide quantifiable validation of goal achievement
- **User-Centric Validation**: Test from the user perspective to validate goal success
- **Comprehensive Coverage**: Validate all dimensions of goal success criteria

### For Test Strategy Development
- **Goal-Specific Approach**: Create testing strategy tailored to specific goal requirements
- **Risk-Based Prioritization**: Focus testing on the most critical aspects for goal achievement
- **Continuous Validation**: Implement ongoing testing to monitor goal achievement
- **Quality Gate Definition**: Establish clear acceptance criteria for goal validation

### For Implementation
- **Tool Alignment**: Select testing tools that can validate specific goal metrics
- **Environment Accuracy**: Ensure testing environment reflects real-world goal conditions
- **Automation Strategy**: Automate tests that continuously validate goal achievement
- **Monitoring Integration**: Integrate testing results with goal tracking systems

## Common Testing Patterns

### Performance Goal Testing
- Baseline measurements and performance benchmarks
- Load testing aligned with goal requirements
- Performance regression testing
- Real-world usage scenario validation

### User Experience Goal Testing
- User journey validation that leads to goal achievement
- Usability testing focused on goal outcomes
- A/B testing to validate goal-achieving approaches
- User satisfaction measurements

### Reliability Goal Testing
- Stress testing to validate reliability goals
- Error handling and recovery validation
- Recovery time objective (RTO) validation
- Availability and uptime monitoring

### Security Goal Testing
- Security control validation that supports goal security requirements
- Penetration testing aligned with goal security needs
- Compliance validation for security goals
- Privacy requirement testing

## Validation and Iteration

### Testing Strategy Review Process
- **Regular Assessment**: Evaluate testing approach effectiveness for goal validation
- **Metric Alignment**: Ensure tests continue to validate relevant goal metrics
- **Coverage Validation**: Verify testing covers all important aspects of goal achievement
- **Stakeholder Feedback**: Gather feedback on validation effectiveness

### Testing Strategy Evolution
- **Adaptive Approach**: Modify testing based on what most effectively validates goals
- **Tool Optimization**: Adjust tools based on validation effectiveness
- **Quality Gate Refinement**: Improve acceptance criteria based on experience
- **Automation Enhancement**: Expand automation for better goal validation

## Examples

### Example 1: Performance Testing Strategy
```
/goalkit.test
Goal: Reduce API response time by 60% to improve user experience
Test Types: Performance, load, stress, integration
Coverage: All API endpoints that directly impact user experience, system under various load conditions
Scenarios: Peak usage simulation, average usage patterns, gradual load increases
Tools: k6 for performance testing, New Relic for monitoring
Metrics: API response time percentiles, throughput, error rates
Automation: Automated performance regression testing on each deployment
Quality Gates: 95% of requests < 200ms, 99% availability during business hours
```

### Example 2: User Experience Testing Strategy
```
/goalkit.test
Goal: Increase user onboarding completion by 40% through simplified process
Test Types: User experience, A/B testing, usability, integration
Coverage: Onboarding flow, user journey completion, error handling, cross-platform consistency
Scenarios: New user onboarding process, error recovery, different user personas
Tools: Hotjar for user behavior analysis, Google Analytics for conversion tracking
Metrics: Onboarding completion rate, time to complete onboarding, user satisfaction scores
Automation: Automated UI testing, A/B test monitoring
Quality Gates: 65% onboarding completion rate, <5 minutes average completion time
```