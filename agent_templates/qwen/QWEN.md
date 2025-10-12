# Goal Kit for Qwen Code - Comprehensive Guide

## Introduction
Goal Kit for Qwen Code enables goal-driven development that emphasizes measurable outcomes and continuous learning. This guide provides comprehensive instructions for leveraging Qwen Code to achieve specific project goals through structured, evidence-based development practices.

## Core Commands and Usage

### 0. Goal Discovery Framework
When processing any command that involves specific goals, Qwen Code should first try to discover existing goals:

```
Goal Discovery Process:
1. Use glob() to search for goals in .goalkit/goals/ directory
2. Use list_directory() to enumerate available goal directories
3. If user references a specific goal, attempt to locate it
4. If multiple goals exist, ask user to specify which one
5. If no goals exist, inform user and suggest creating a new goal
```

### 1. Vision Command (`/goalkit.vision`)
Establish your project foundation with a clear vision:

```
/goalkit.vision
Project: [Name of your project]
Vision Statement: [1-2 sentences describing the desired end state]
Core Principles: [3-5 guiding principles for the project]
Success Metrics: [Quantifiable measures of project success]
Stakeholders: [Key people impacted by or involved in the project]
Timeline: [High-level project timeline with key phases]
```

After receiving this command, Qwen Code will:
1. Create or update the `.goalkit/vision.md` file in the project root
2. Use the current date in YYYY-MM-DD format for the "Created" field
3. Write the complete vision document using the template structure
4. Inform the user that the vision has been established and suggest creating the first goal using `/goalkit.goal`

### 2. Goal Definition Command (`/goalkit.goal`)
Define specific, measurable goals that support your vision:

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

After receiving this command, Qwen Code should:
1. Create a new directory in the `goals/` folder using the format: `[###-goal-name]` where `###` is a number with leading zeros (e.g., `001-improve-testing`)
2. Create the goal.md file inside the created directory
3. Use the current date in YYYY-MM-DD format for the "Created" field
4. Use the directory name as the "Goal Branch" identifier
5. Write the complete goal definition using the template structure
6. Inform the user that the goal has been created and suggest next steps using `/goalkit.strategies` and `/goalkit.milestones`

### 3. Strategy Exploration Command (`/goalkit.strategies`)
Explore multiple implementation strategies for each goal:

```
/goalkit.strategies
Goal: [Reference to specific goal]
Strategy Options:
  Option 1: [Full description of first approach]
    - Pros: [Advantages of this approach]
    - Cons: [Disadvantages of this approach]
    - Implementation Difficulty: [Relative difficulty rating]
    - Maintenance Complexity: [Expected long-term maintenance needs]
  Option 2: [Full description of second approach]
    - Pros: [Advantages of this approach]
    - Cons: [Disadvantages of this approach]
    - Implementation Difficulty: [Relative difficulty rating]
    - Maintenance Complexity: [Expected long-term maintenance needs]
  Option 3: [Full description of third approach]
    - Pros: [Advantages of this approach]
    - Cons: [Disadvantages of this approach]
    - Implementation Difficulty: [Relative difficulty rating]
    - Maintenance Complexity: [Expected long-term maintenance needs]

Evaluation Framework:
- Technical Feasibility
- Resource Requirements
- Time-to-Completion
- Risk Assessment
- Scalability Potential
- Team Alignment

Recommendation: [Your recommended approach with detailed reasoning]
```

After receiving this command, Qwen Code should:
1. Locate the appropriate goal directory in the `goals/` folder (the most recently created or specified goal)
2. Create the `strategies.md` file inside that goal directory
3. Use the current date in YYYY-MM-DD format for the "Date" field
4. Write the complete strategy analysis using the template structure
5. Reference the associated goal in the document header
6. Inform the user that the strategy analysis has been completed and suggest next steps using `/goalkit.milestones`

### 4. Milestone Planning Command (`/goalkit.milestones`)
Break goals into measurable, time-bound milestones:

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

After receiving this command, Qwen Code should:
1. Locate the appropriate goal directory in the `goals/` folder (the most recently created or specified goal)
2. Create the `milestones.md` file inside that goal directory
3. Use the current date in YYYY-MM-DD format for the "Date" field
4. Write the complete milestone plan using the template structure
5. Reference the associated goal and strategy in the document header
6. Inform the user that the milestone plan has been completed and suggest next steps using `/goalkit.execute`

### 5. Execution Command (`/goalkit.execute`)
Begin implementation with continuous learning and adaptation:

```
/goalkit.execute
Goal: [Reference to specific goal]
Current Milestone: [Which milestone you're currently working on]
Selected Strategy: [The strategy chosen from strategies phase]
Daily Focus: [Specific tasks for the current day]
Success Indicator: [How you'll know today's work was productive]
Learning Objective: [What you hope to learn during execution]
Adaptation Plan: [How you'll handle unexpected challenges]
```

After receiving this command, Qwen Code should:
1. Locate the appropriate goal directory in the `goals/` folder (the most recently created or specified goal)
2. Create the `execution.md` file inside that goal directory
3. Use the current date in YYYY-MM-DD format for the "Date" field
4. Write the complete execution plan using the template structure
5. Reference the associated goal, strategy, and milestones in the document header
6. Inform the user that the execution plan has been completed and suggest beginning implementation

## Advanced Usage Patterns

### Pattern 1: Goal Hierarchy and Dependencies
For complex projects, establish goal hierarchies:

```
/goalkit.goal-hierarchy
Main Goal: [High-level objective]
Sub-goal 1: [Supporting goal 1]
  - Depends on: [Dependencies for this sub-goal]
  - Supports: [How it supports main goal]
Sub-goal 2: [Supporting goal 2]
  - Depends on: [Dependencies for this sub-goal]
  - Supports: [How it supports main goal]
Sub-goal 3: [Supporting goal 3]
  - Depends on: [Dependencies for this sub-goal]
  - Supports: [How it supports main goal]

Relationship Map: [How sub-goals interact and support each other]
Critical Path: [Sequence of goals that determines project timeline]
```

### Pattern 2: Evidence-Based Decision Framework
Make decisions based on collected evidence:

```
Based on the following evidence, recommend the next course of action:

Evidence Collected:
- Performance Metrics: [Relevant performance data]
- User Feedback: [Input from stakeholders or users]
- Technical Findings: [Technical discoveries or challenges]
- Resource Utilization: [How resources are being used]

Goal Context:
- Current Goal: [Goal being pursued]
- Current Strategy: [Current approach being used]
- Success Criteria: [How success is measured]

Provide analysis considering:
1. How evidence supports or challenges current approach
2. Alternative strategies to consider
3. Recommended changes to approach
4. Additional evidence needed for decision
5. Implementation plan for changes
```

### Pattern 3: Continuous Learning Integration
Incorporate learning and adaptation into the development process:

```
/goalkit.learn
Goal: [Current goal being pursued]
What We Tried: [Previous approach or solution]
What We Observed: [Actual results vs. expected results]
What This Means: [Analysis of the difference]
What We'll Try Next: [Adapted approach based on learning]
Success Measurement: [How we'll verify the new approach works]
Timeline: [When to evaluate the new approach]
```

## Working with Code Implementation

### Pre-Implementation Architecture Design
Before writing code, use Qwen Code for architectural planning:

```
Based on goal "[specific goal]" and strategy "[selected strategy]", design an architecture that:

1. Meets the goal's success criteria
2. Aligns with project principles
3. Considers identified risks
4. Optimizes for future scalability
5. Uses appropriate technologies for the team's expertise

Include:
- High-level system architecture
- Component relationships
- Data flow design
- Interface definitions
- Security considerations
- Performance requirements
- Testing strategy
- Deployment considerations
```

### Code-Goal Alignment Verification
Ensure all code contributes directly to goals:

```
Analyze the following code for alignment with goal "[specific goal]":

Code to Review:
[code content]

Evaluate based on:
1. Direct contribution to goal achievement
2. Efficiency of implementation approach
3. Adherence to project principles
4. Maintainability and extensibility
5. Performance characteristics
6. Security implications
7. Test coverage requirements

Provide specific recommendations for improvement.
```

## Measurement and Tracking

### Daily Progress Tracking
Start each development day with goal-focused planning:

```
/goalkit.daily-plan
Date: [Current date]
Goal Focus: [Which goal is today's focus]
Yesterday's Progress: [Brief summary of yesterday's achievements]
Today's Objectives: [Specific tasks that advance the goal]
Success Criteria for Today: [How we'll know today was productive]
Potential Blockers: [Anticipated challenges]
Required Resources: [What's needed for today's work]
Timeline Check: [How today's work fits in overall timeline]
```

### Weekly Goal Review
Conduct comprehensive weekly assessments:

```
/goalkit.weekly-review
Week of: [Date range]
Goal Status: [Status of each active goal]
Milestones Achieved: [Milestones completed this week]
Milestones In Progress: [Milestones being worked on]
Milestones At Risk: [Milestones facing challenges]
Evidence Gathered: [Key data collected this week]
Lessons Learned: [Key insights from the week]
Adjustments Made: [Changes to approach or strategy]
Next Week Priorities: [Focus areas for upcoming week]
Resource Reallocations: [Changes to resource allocation]
```

## Troubleshooting Common Challenges

### Challenge 1: Unclear or Vague Goals
When goals lack specificity:

```
Help clarify and strengthen this goal by making it more specific and measurable:

Goal: [Current goal description]
Context: [Background information and constraints]
Stakeholder Expectations: [What stakeholders expect]
Current Success Metrics: [How success is currently defined]
Available Resources: [Resources available for this goal]

Transform this into a SMART goal with:
- Specific: [Clear and unambiguous]
- Measurable: [Quantifiable success criteria]
- Achievable: [Realistic given constraints]
- Relevant: [Aligned with broader vision]
- Time-bound: [Clear timeline and milestones]
```

### Challenge 2: Strategy Selection Paralysis
When faced with multiple viable strategies:

```
Compare these strategies for achieving goal "[specific goal]":

Strategy A: [Detailed strategy description]
- Advantages: [Key benefits]
- Disadvantages: [Key challenges]
- Resource Requirements: [Time, people, technology needed]
- Risk Profile: [Potential risks and mitigation strategies]
- Success Probability: [Likelihood of success]

Strategy B: [Different strategy approach]
- Advantages: [Key benefits]
- Disadvantages: [Key challenges]
- Resource Requirements: [Time, people, technology needed]
- Risk Profile: [Potential risks and mitigation strategies]
- Success Probability: [Likelihood of success]

Strategy C: [Alternative strategy approach]
- Advantages: [Key benefits]
- Disadvantages: [Key challenges]
- Resource Requirements: [Time, people, technology needed]
- Risk Profile: [Potential risks and mitigation strategies]
- Success Probability: [Likelihood of success]

Provide a comparative analysis with weighted recommendations based on:
- Goal alignment
- Resource efficiency
- Risk tolerance
- Timeline requirements
- Team capabilities
```

### Challenge 3: Stalled Progress
When milestones aren't progressing:

```
Analyze the challenges preventing progress on milestone "[specific milestone]":

Current Status: [Where things stand now]
Timeline: [When this should have been completed]
Planned vs. Actual: [What was planned vs. what actually happened]
Blockers Identified: [Specific obstacles preventing progress]
Resource Gaps: [Missing resources or capabilities]
External Dependencies: [Things waiting on others]
Internal Issues: [Internal problems affecting progress]

For each blocker, provide:
- Root cause analysis
- Impact assessment
- Potential solutions
- Estimated resolution time
- Resource requirements for solution
- Risk mitigation strategies
```

## Integration with Development Workflow

### Version Control with Goal Alignment
Connect Git workflows with goal achievement:

```
Write Git commit messages that clearly connect to goals and milestones:

Goal: [Specific goal being advanced]
Milestone: [Specific milestone being achieved]
What Changed: [Brief technical description]
How This Advances Goal: [Connection to goal achievement]
Success Indicator: [How this brings us closer to success]

Format: "[GOAL-XX] [Milestone] Description of change and goal impact"
Example: "[USER-LOGIN-01] Implement Authentication Milestone 1: Create login form with validation"
```

### Testing Strategy Aligned with Goals
Ensure testing verifies goal achievement:

```
Create a comprehensive test suite that verifies goal "[specific goal]" is being achieved:

Unit Tests: [Tests for individual components]
- Test 1: [Tests specific functionality aligned with goal]
- Test 2: [Tests another aspect aligned with goal]
- Test 3: [Tests another aspect aligned with goal]

Integration Tests: [Tests for component interactions]
- Test 1: [Tests how components work together toward goal]
- Test 2: [Tests another interaction toward goal]
- Test 3: [Tests another interaction toward goal]

End-to-End Tests: [Tests that verify goal achievement]
- Test 1: [User workflow that demonstrates goal success]
- Test 2: [Alternative workflow toward goal success]
- Test 3: [Edge case workflow for goal success]

Success Metrics for Tests:
- Code coverage: [Minimum coverage percentage]
- Performance benchmarks: [Speed, resource usage requirements]
- Error rate: [Acceptable failure rate]
- User satisfaction: [How tests relate to user goals]
```

## Best Practices for Goal-Driven Development

### 1. Goal-First Design
Always start with the goal before designing solutions:

```
Before designing [feature/system/component], confirm alignment with goal:

Goal Connection: [How this directly supports the goal]
Success Impact: [How this moves us closer to success]
Alternative Approaches: [Why this approach was chosen]
Risk Assessment: [Potential risks to goal achievement]
Success Metrics: [How we'll measure this contribution]
```

### 2. Evidence-Based Adjustments
Use collected data to inform approach changes:

```
Based on evidence X, Y, and Z, adjust the approach to goal "[specific goal]":

Current Evidence:
- Evidence 1: [Specific data point]
- Evidence 2: [Specific data point]
- Evidence 3: [Specific data point]

Impact on Goal: [How evidence affects goal achievement]
Proposed Adjustment: [Specific change to approach]
Expected Improvement: [How adjustment improves goal achievement]
Measurement Plan: [How to verify adjustment effectiveness]
Timeline for Evaluation: [When to assess results]
```

### 3. Continuous Goal Review
Regularly verify that goals remain relevant and achievable:

```
/goalkit.goal-review
Goal: [Specific goal to review]
Original Context: [Why this goal was set]
Current Context: [Current situation and constraints]
Goal Relevance: [Is this goal still important?]
Goal Feasibility: [Is this goal still achievable?]
Success Criteria Validity: [Are the measures still appropriate?]
Resource Alignment: [Do resources still match goal scope?]
Timeline Appropriateness: [Is the timeline realistic?]
Recommendations: [Keep, modify, or abandon the goal?]
```

## Conclusion
Goal Kit for Qwen Code transforms development from a task-oriented activity into an outcome-focused discipline. By consistently applying these patterns, you ensure that every coding effort directly contributes to measurable goals, while maintaining the flexibility to adapt based on evidence and learning.

Remember: Every line of code should serve the goal, every decision should be evidence-based, and every milestone should be measurable. This approach leads to more focused, efficient, and successful development outcomes.

The key to success is consistency in applying these patterns and continuous alignment between your development activities and your desired outcomes.