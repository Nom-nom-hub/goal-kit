# /goalkit.goal Command

## AI AGENT INSTRUCTIONS

When processing `/goalkit.goal` requests, follow this structured approach:

### Goal Discovery (First Step)
1. **Locate Existing Goals**: Search for existing goals in `.goalkit/goals/` directory
   - Use `glob(path="PROJECT_ROOT/.goalkit/goals", pattern="**")` to discover existing goals
   - Use `list_directory(path="PROJECT_ROOT/.goalkit/goals")` to enumerate goal directories
   - Determine the next available goal number based on existing goals
   - If user is referencing an existing goal, confirm which one they mean

### Input Analysis
1. **Convert Outcomes to Goals**: Transform user descriptions of desired outcomes into structured goal definitions
2. **Generate Success Metrics**: Create specific, measurable success criteria with targets and timelines
3. **Define Testable Hypotheses**: Frame assumptions as testable hypotheses with clear validation methods
4. **Structure Milestones**: Break goals into measurable progress steps with learning objectives

### Processing Framework
- Focus on user/business outcomes, not implementation features
- Generate 2-3 primary metrics with specific, quantifiable targets (%, $, timeframes, user counts)
- Create testable assumptions in "If we do X, then Y will happen" format
- Ensure each milestone has clear success indicators and validation methods

### Output Structure
Use the template sections below to structure your response. Ensure alignment with existing project vision and maintain consistency with goal-driven development principles.

---

## Overview

The `/goalkit.goal` command defines specific, measurable goals that contribute to your project's vision. Unlike specifications that focus on implementation details, goals focus on outcomes and success metrics.

## Purpose

This command creates focused goal definitions that:
- Define measurable outcomes rather than implementation features
- Establish clear success criteria for validation
- Set up hypotheses for testing through implementation
- Provide foundation for strategy exploration

## When to Use

Use `/goalkit.goal` when:
- You have an established project vision
- You want to pursue a specific outcome or user benefit
- You need to define what "success" looks like for an initiative
- You're ready to explore implementation strategies

## Input Format

```
/goalkit.goal [description of desired outcome and success criteria]
```

### Example Input

```
/goalkit.goal Build a task management system that helps users reduce cognitive load and accomplish more meaningful work. Success criteria: 80% of users report reduced mental effort when managing tasks, 90% of users complete their most important tasks regularly, and 70% improvement in perceived productivity. Focus on user autonomy and flexible organization approaches.
```

## Output

The command generates:
- `goals/[###-goal-name]/goal.md` - Complete goal definition
- `goals/[###-goal-name]/` directory structure for strategies and milestones
- Foundation for strategy exploration and milestone planning

### Agent File Creation Instructions

When processing `/goalkit.goal` commands, AI agents should:
1. Create a new directory in the `goals/` folder using the format: `[###-goal-name]` where `###` is a number with leading zeros (e.g., `001-improve-testing`)
2. Create the goal.md file inside the created directory
3. Use the current date in YYYY-MM-DD format for the "Created" field
4. Use the directory name as the "Goal Branch" identifier
5. Write the complete goal definition using the template structure below
6. After creating the goal file, inform the user that the goal has been created and suggest next steps using `/goalkit.strategies` and `/goalkit.milestones`

### File Creation Process
- **Create Directory**: `goals/[###-goal-name]/` (where ### is incremented from existing goals)
- **Create File**: `goals/[###-goal-name]/goal.md` with the goal content
- **Template**: Use the structure provided in the "Goal Components" section below

## Goal Components

### 1. Goal Overview
- **Goal Statement**: Clear description of desired outcome
- **Context**: Why this goal matters
- **Success Level**: What achievement looks like

### 2. Success Metrics
- **Primary Metrics**: Must-achieve measurements
- **Secondary Metrics**: Valuable additional indicators
- **Measurement Approach**: How to collect and validate metrics

### 3. Target Users & Stakeholders
- **Primary Users**: Who directly benefits
- **Stakeholders**: Who has interest in the outcome
- **Success Indicators**: How each group measures success

### 4. Goal Hypotheses
- **Key Assumptions**: Testable beliefs about the goal
- **Risk Factors**: Potential issues and mitigations
- **Validation Strategy**: How to test assumptions

### 5. Goal Milestones
- **Measurable Progress Steps**: Breaking goal into achievable milestones
- **Learning Objectives**: What to discover at each step
- **Value Delivery**: User/business value at each milestone

## Key Differences from Spec-Driven Development

| Spec-Driven | Goal-Driven |
|-------------|-------------|
| Detailed feature requirements | Measurable outcome definitions |
| Implementation-focused user stories | Outcome-focused success criteria |
| Single "correct" solution path | Multiple strategy exploration |
| Upfront specification precision | Hypothesis-driven learning |

## Integration with Other Commands

### Before Using `/goalkit.goal`
- **`/goalkit.vision`**: Should be completed first to provide context
- **Project Vision**: Goal should align with established vision

### After Using `/goalkit.goal`
- **`/goalkit.strategies`**: Explore multiple approaches to achieve the goal
- **`/goalkit.milestones`**: Break goal into measurable progress steps
- **`/goalkit.execute`**: Implement with learning and adaptation

## Best Practices

### Goal Definition
- **Outcome-Focused Language**: Describe what users achieve, not what features exist
- **Measurable Success**: Define specific, quantifiable success criteria
- **User-Centric**: Focus on user benefits and experiences
- **Business-Aligned**: Connect to clear business value

### Success Criteria
- **Realistic Targets**: Based on industry benchmarks and user research
- **Multiple Indicators**: Use multiple metrics to validate the same outcome
- **Time-Bound**: Define measurement timeframe
- **Collectable**: Ensure metrics can be realistically measured

### Hypothesis Formation
- **Testable Assumptions**: Frame as "If we do X, then Y will happen"
- **Risk Awareness**: Identify potential failure modes upfront
- **Learning Orientation**: Focus on what you'll discover regardless of outcome

## Common Goal Patterns

### User Experience Goals
- Reduce time-to-completion for key tasks
- Improve user satisfaction scores
- Increase feature adoption rates
- Reduce support requests

### Business Outcome Goals
- Increase revenue or conversion rates
- Reduce operational costs
- Improve market positioning
- Enhance competitive advantage

### Technical Capability Goals
- Improve system performance
- Enhance security posture
- Increase development velocity
- Build technical expertise

## Validation and Iteration

### Goal Review Process
- **Regular Assessment**: Review goal relevance and progress
- **Metric Validation**: Ensure success criteria remain relevant
- **Assumption Testing**: Validate or update key hypotheses
- **Stakeholder Alignment**: Maintain support for the goal

### Goal Evolution
- **Refinement**: Clarify goal definition based on learning
- **Expansion**: Grow goal scope based on early success
- **Contraction**: Narrow goal focus if too broad
- **Pivot**: Change direction if assumptions prove wrong

## Examples

### Example 1: Productivity App Goal
```
/goalkit.goal Create a note-taking system that helps users capture and organize information effortlessly. Success criteria: 85% of users actively use the system daily, 90% find information when needed, and 75% report improved knowledge retention. Focus on frictionless capture and intelligent organization.
```

### Example 2: E-commerce Goal
```
/goalkit.goal Improve product discovery to help users find relevant items quickly. Success criteria: 60% increase in conversion rate, 40% reduction in search abandonment, and 80% user satisfaction with discovery experience. Explore personalization and guided discovery approaches.
```

### Example 3: Developer Tool Goal
```
/goalkit.goal Streamline the development workflow to reduce context switching. Success criteria: 50% reduction in time spent switching between tools, 90% of developers report improved focus, and 30% increase in development velocity. Consider integration and automation strategies.