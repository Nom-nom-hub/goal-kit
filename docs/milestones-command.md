---
layout: default
title: Milestones Command - Goal Kit Documentation
---

# Milestones Command (`/goalkit.milestones`)

## Overview

The Milestones command breaks goals into measurable, time-bound milestones that provide clear progress indicators. It ensures that progress toward goals can be tracked and validated through specific, quantifiable achievements.

## Purpose

The `/goalkit.milestones` command is essential for:

- Breaking complex goals into measurable, achievable steps
- Establishing clear acceptance criteria for each milestone
- Defining evidence requirements to verify completion
- Setting realistic timelines for milestone achievement
- Allocating appropriate resources to each milestone
- Creating quantifiable success metrics for progress tracking

## Usage

```
/goalkit.milestones
Goal: [Reference to specific goal]
Milestone 1: [First measurable milestone toward goal]
  - Description: [What exactly will be accomplished]
  - Acceptance Criteria: [Specific conditions that must be met]
  - Evidence Requirements: [How completion will be verified]
  - Timeline: [Target completion date]
  - Resource Allocation: [People, time, tools needed]
  - Success Metrics: [Quantitative measures of success]
Milestone 2: [Second measurable milestone toward goal]
  - Description: [What exactly will be accomplished]
  - Acceptance Criteria: [Specific conditions that must be met]
  - Evidence Requirements: [How completion will be verified]
  - Timeline: [Target completion date]
  - Resource Allocation: [People, time, tools needed]
  - Success Metrics: [Quantitative measures of success]
```

## Key Components

### Milestone Description
A clear explanation of what exactly will be accomplished by completing this milestone. This should be specific and actionable.

### Acceptance Criteria
Specific conditions that must be met for the milestone to be considered complete. These provide objective measures of completion.

### Evidence Requirements
Clear guidelines on how completion will be verified, ensuring that milestone achievement can be objectively measured.

### Timeline
Realistic target completion dates for each milestone, supporting project planning and coordination.

### Resource Allocation
Specific resources needed to complete the milestone, including people, time, tools, and budget.

### Success Metrics
Quantitative measures that indicate milestone success, aligned with the overall goal's success criteria.

## Best Practices

- Ensure milestones are directly tied to achieving the goal's success criteria
- Create measurable milestones that provide objective evidence of progress
- Set realistic timelines based on available resources and complexity
- Balance milestone size - not too small (excessive overhead) or too large (delayed feedback)
- Ensure each milestone provides value even if subsequent milestones change
- Make acceptance criteria specific and testable

## Example

```
/goalkit.milestones
Goal: Implement Secure User Authentication
Milestone 1: Basic registration and login functionality
  - Description: Users can register with email/password and log in to the system
  - Acceptance Criteria: Registration form validates inputs, login verifies credentials, users can access basic features after login
  - Evidence Requirements: Test accounts created successfully, login flow tested with valid/invalid credentials, security audit of credential storage
  - Timeline: Complete by end of week 2
  - Resource Allocation: 1 backend dev, 1 frontend dev, security consultant review
  - Success Metrics: 95% registration success rate, <3 second login response time, zero credential storage in plain text

Milestone 2: Password recovery system
  - Description: Users can securely recover access to their accounts via email
  - Acceptance Criteria: Password reset email sent securely, temporary tokens expire appropriately, new passwords meet security requirements
  - Evidence Requirements: Test password recovery flows, security audit of token generation/expiry, user acceptance testing
  - Timeline: Complete by end of week 4
  - Resource Allocation: 1 backend dev, 1 security consultant
  - Success Metrics: 90% password reset success rate, valid tokens expire within 1 hour, user satisfaction >4.0/5.0

Milestone 3: Multi-factor authentication
  - Description: Add optional two-factor authentication for enhanced security
  - Acceptance Criteria: Users can enable/disable 2FA, authentication works with both password and 2FA token
  - Evidence Requirements: Test 2FA flows, security audit of 2FA implementation, user documentation
  - Timeline: Complete by end of week 6
  - Resource Allocation: 1 backend dev, 1 frontend dev, 1 security consultant
  - Success Metrics: 30% of users enable 2FA option, no security incidents related to 2FA
```

## Integration with Goal-Driven Development

Milestones bridge the gap between high-level goals and day-to-day execution. They provide measurable steps toward achieving the defined goals, allowing for progress tracking and validation. This aligns with the Goal-Driven Development principle of measurable progress and supports adaptive execution by providing clear checkpoints for evaluation and adjustment.