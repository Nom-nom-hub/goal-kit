# /goalkit.tasks Command

## Overview

The `/goalkit.tasks` command creates actionable tasks that break down goals and milestones into specific, implementable work items. Unlike milestones that focus on outcomes, tasks focus on concrete activities and deliverables.

## Purpose

This command creates a task breakdown that:
- Converts goals and milestones into specific work items
- Provides clear, actionable steps for implementation
- Enables progress tracking at the activity level
- Supports both development and non-development activities

## When to Use

Use `/goalkit.tasks` when:
- You have established goals and milestones
- You need to break work into implementable steps
- You want to track detailed progress on goal execution
- You're ready to assign and execute specific work items

## Input Format

```
/goalkit.tasks [description of task breakdown approach and focus areas]
```

### Example Input

```
/goalkit.tasks Create specific tasks for the user onboarding milestone:
1. Design user interview questions and recruit participants
2. Conduct user research sessions and analyze findings
3. Create interactive prototype based on research insights
4. Develop onboarding flow implementation plan
5. Build core onboarding features with analytics
6. Create user testing protocol and conduct tests
Focus on actionable deliverables and clear success criteria for each task.
```

## Output

The command generates:
- `goals/[###-goal-name]/tasks.md` - Comprehensive task breakdown
- `goals/[###-goal-name]/checklist.md` - Actionable checklist for execution
- Task tracking framework for progress monitoring

## Task Components

### 1. Task Definition Framework
- **Clear Deliverables**: Specific outputs or outcomes for each task
- **Actionable Steps**: Concrete activities that can be executed
- **Success Criteria**: How to determine when task is complete
- **Time Estimates**: Realistic effort estimation for planning

### 2. Task Organization
- **Priority Levels**: P0 (critical), P1 (high), P2 (medium), P3 (low)
- **Dependencies**: What tasks must be completed first
- **Categories**: Development, Design, Research, Testing, Documentation
- **Assignment**: Who should work on each task

### 3. Progress Tracking
- **Status Levels**: Not Started, In Progress, Review, Testing, Complete
- **Progress Indicators**: Clear completion criteria
- **Blockers**: Issues preventing task completion
- **Notes**: Important context and learnings

## Key Differences from Goal-Driven Development

| Milestone Focus | Task Focus |
|-----------------|------------|
| Outcome validation | Activity execution |
| Learning objectives | Deliverable completion |
| Progress measurement | Work tracking |
| Strategy validation | Implementation execution |

## Integration with Other Commands

### Before Using `/goalkit.tasks`
- **`/goalkit.vision`**: Provides context for task relevance
- **`/goalkit.goal`**: Defines what tasks should achieve
- **`/goalkit.strategies`**: Provides approach context for tasks
- **`/goalkit.milestones`**: Defines the milestones tasks support

### After Using `/goalkit.tasks`
- **`/goalkit.execute`**: Execute tasks with learning and adaptation
- **`/goalkit.measure`**: Track task completion and progress
- **`/goalkit.adapt`**: Adjust tasks based on execution learning

## Best Practices

### Task Definition
- **Specific Actions**: Use action verbs (build, design, research, test)
- **Clear Deliverables**: Define concrete outputs for each task
- **Measurable Completion**: Establish clear "done" criteria
- **Realistic Scope**: Keep tasks to 1-5 days of focused work

### Task Organization
- **Logical Grouping**: Group related tasks together
- **Dependency Clarity**: Make prerequisite relationships explicit
- **Priority Alignment**: Ensure P0/P1 tasks align with milestones
- **Resource Consideration**: Consider team capacity and skills

### Progress Management
- **Regular Updates**: Update task status frequently
- **Blocker Escalation**: Raise issues preventing progress
- **Completion Validation**: Ensure tasks meet quality standards
- **Learning Capture**: Document insights and adaptations

## Common Task Categories

### Development Tasks
- **Feature Implementation**: Build specific functionality
- **Code Refactoring**: Improve existing code structure
- **Performance Optimization**: Enhance system performance
- **Bug Fixes**: Resolve identified issues

### Design Tasks
- **User Research**: Conduct user interviews and studies
- **Interface Design**: Create visual designs and prototypes
- **User Testing**: Validate designs with users
- **Design Systems**: Build reusable design components

### Research Tasks
- **Market Research**: Analyze competitive landscape
- **Technical Research**: Evaluate technology options
- **User Research**: Understand user needs and behaviors
- **Feasibility Studies**: Assess implementation possibilities

### Testing & Quality Tasks
- **Test Planning**: Define testing strategy and coverage
- **Manual Testing**: Execute test cases manually
- **Automated Testing**: Build automated test suites
- **Quality Assurance**: Ensure standards compliance

### Documentation Tasks
- **Technical Documentation**: Document system architecture
- **User Documentation**: Create user guides and help
- **Process Documentation**: Define team processes
- **Knowledge Transfer**: Share learnings with team

## Task Lifecycle Management

### Task States
- **Not Started**: Task identified but not yet begun
- **In Progress**: Active work on the task
- **Review**: Task complete, awaiting validation
- **Testing**: Task in testing or quality assurance
- **Complete**: Task finished and validated

### State Transitions
- **Clear Criteria**: Define when to move between states
- **Quality Gates**: Ensure tasks meet standards before completion
- **Stakeholder Review**: Involve relevant people in validation
- **Documentation**: Record decisions and changes

## Examples

### Example 1: Feature Development Task Breakdown
```
/goalkit.tasks For user authentication feature:
1. Design authentication flow and user experience
2. Set up authentication service architecture
3. Implement core login/registration functionality
4. Add password reset and account management
5. Create user profile management system
6. Implement security measures and validation
7. Write comprehensive tests for all auth features
Focus on security, usability, and comprehensive testing.
```

### Example 2: Research Project Task Breakdown
```
/goalkit.tasks For market research initiative:
1. Define research objectives and scope
2. Design research methodology and questions
3. Recruit research participants
4. Conduct research sessions and collect data
5. Analyze findings and identify patterns
6. Synthesize insights into actionable recommendations
7. Present findings to stakeholders
Emphasize data quality and actionable insights.
```

### Example 3: Process Improvement Task Breakdown
```
/goalkit.tasks For development process optimization:
1. Analyze current development workflow
2. Identify bottlenecks and inefficiencies
3. Research best practices and tools
4. Design improved process framework
5. Pilot new process with small team
6. Gather feedback and iterate on process
7. Roll out improvements to full team
Focus on measurable efficiency gains and team adoption.
```

## Task Dependencies and Sequencing

### Dependency Types
- **Hard Dependencies**: Tasks that must be completed before others
- **Soft Dependencies**: Tasks that should be completed before others
- **Resource Dependencies**: Tasks requiring specific people or tools
- **External Dependencies**: Tasks waiting on outside factors

### Sequencing Strategies
- **Critical Path**: Focus on tasks that unblock others
- **Parallel Execution**: Run independent tasks simultaneously
- **Risk Mitigation**: Tackle high-risk tasks early
- **Value Delivery**: Prioritize tasks that deliver user value

## Quality Assurance for Tasks

### Completion Standards
- **Deliverable Quality**: Meets defined quality criteria
- **Documentation**: Properly documented for maintenance
- **Testing**: Passes required tests and validation
- **Review**: Approved by relevant stakeholders

### Validation Methods
- **Code Review**: Peer review of implementation
- **User Testing**: Validation with target users
- **Performance Testing**: Verification of performance requirements
- **Integration Testing**: Confirmation of system compatibility

## Learning and Adaptation

### Task-Level Learning
- **Unexpected Challenges**: Document difficulties encountered
- **Solution Approaches**: Record how problems were solved
- **Time Estimation Accuracy**: Track estimation vs. actual effort
- **Quality Outcomes**: Assess deliverable quality and impact

### Process Improvement
- **Recurring Patterns**: Identify common task types and challenges
- **Efficiency Opportunities**: Find ways to streamline similar tasks
- **Skill Development**: Identify team learning opportunities
- **Tool Effectiveness**: Evaluate tool and process utility

## Integration with Project Management

### Task Management Tools
- **Issue Trackers**: Integration with tools like Jira, GitHub Issues
- **Kanban Boards**: Visual task organization and flow
- **Time Tracking**: Effort monitoring and capacity planning
- **Progress Reporting**: Status updates for stakeholders

### Team Coordination
- **Assignment Clarity**: Clear ownership of each task
- **Communication Channels**: Defined ways to collaborate
- **Meeting Cadence**: Regular check-ins on task progress
- **Escalation Paths**: Clear process for blocked tasks

---

*This task framework supports effective execution of goals and milestones by breaking work into manageable, trackable activities. Regular review and adaptation ensures tasks remain aligned with goal outcomes and team capacity.*