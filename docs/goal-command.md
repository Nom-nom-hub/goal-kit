---
layout: default
title: Goal Command - Goal Kit Documentation
---

# Goal Command (`/goalkit.goal`)

## Overview

The Goal command defines specific, measurable goals that support your project vision. It ensures that all development efforts are aligned with desired outcomes and provides clear success criteria for measuring progress.

## Purpose

The `/goalkit.goal` command is essential for:

- Defining specific, measurable goals that align with the project vision
- Establishing clear success criteria for each goal
- Setting priorities for development efforts
- Identifying dependencies between goals
- Estimating effort required for each goal
- Assessing risk levels associated with each goal

## Usage

```
/goalkit.goal
Goal Name: [Clear, specific name for the goal]
Description: [Detailed description of what needs to be achieved]
Success Criteria: [Specific, measurable conditions that define success]
Priority: [High/Medium/Low - or use numerical ranking]
Dependencies: [Other goals or resources this goal depends on]
Estimated Effort: [Time and resources required]
Risk Level: [Low/Medium/High - with brief risk summary]
```

## Key Components

### Goal Name
A clear, specific name that captures the essence of what the goal aims to achieve. This should be outcome-focused rather than implementation-focused.

### Description
A detailed description of what needs to be achieved, including context and background information that helps understand the goal's purpose.

### Success Criteria
Specific, measurable conditions that define what success looks like for this goal. These should be quantitative and verifiable.

### Priority
The relative importance of this goal compared to others, helping with resource allocation and scheduling decisions.

### Dependencies
Other goals or resources that this goal depends on, helping identify potential bottlenecks or sequencing requirements.

### Estimated Effort
The time and resources required to achieve the goal, useful for planning and resource allocation.

### Risk Level
Assessment of potential risks associated with achieving the goal, helping with contingency planning.

## Best Practices

- Make sure goals are aligned with the project vision established with `/goalkit.vision`
- Define success criteria that are specific, measurable, and outcome-focused
- Consider dependencies between goals when setting priorities
- Regularly review and update goals as new information becomes available
- Make sure goals are achievable within the available time and resources
- Use quantitative measures wherever possible in success criteria

## Example

```
/goalkit.goal
Goal Name: Implement Secure User Authentication
Description: Build a secure authentication system that allows users to register, log in, and recover passwords with high security and usability.
Success Criteria: 99.9% login success rate, sub-3 second response time, zero security breaches, 4.5+/5 user satisfaction score.
Priority: High
Dependencies: Database schema design, Security policy approval
Estimated Effort: 3 developers for 4 weeks
Risk Level: Medium - complexity of security implementation requires careful design and testing
```

## Integration with Goal-Driven Development

Goals defined with `/goalkit.goal` serve as the foundation for strategy exploration and milestone planning. They translate the high-level vision into specific, measurable outcomes that can be pursued through multiple implementation approaches. Goals ensure that all development efforts contribute directly to achieving the desired project outcomes.