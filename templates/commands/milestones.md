---
description: Create measurable milestones and progress indicators for achieving goals.
scripts:
  sh: scripts/bash/setup-milestones.sh --json
  ps: scripts/powershell/setup-milestones.ps1 -Json
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

# /goalkit.milestones Command

## AI AGENT INSTRUCTIONS

When processing `/goalkit.milestones` requests, follow this structured approach:

### Goal Discovery (First Step)
1. **Locate Associated Goal**: Search for the goal that milestones will support
   - Use `glob(path="PROJECT_ROOT/.goalkit/goals", pattern="**")` to discover goals
   - Use `list_directory(path="PROJECT_ROOT/.goalkit/goals")` to enumerate goal directories
   - If user specified a goal, locate that specific goal directory
   - If multiple goals exist, ask user to clarify which goal needs milestones
   - If no goals exist, inform user that goals must be created first

### Input Analysis
1. **Break Goals into Progress Steps**: Convert goal outcomes into measurable milestone definitions
2. **Define Learning Objectives**: Identify what should be learned or validated at each milestone
3. **Create Validation Criteria**: Establish clear success indicators for each milestone
4. **Sequence for Learning**: Order milestones to validate riskiest assumptions first

### Processing Framework
- Focus on learning and validation, not just implementation activities
- Create milestones that demonstrate measurable progress toward goals
- Include clear success criteria and measurement approaches for each milestone
- Ensure milestones build on each other and align with chosen strategies

### Output Structure
Use the template sections below to structure your response. Create 3-5 milestones that progressively validate the goal with increasing confidence and learning.

---

## Overview

The `/goalkit.milestones` command breaks goals into measurable progress steps that demonstrate movement toward goal achievement. Unlike tasks that focus on implementation activities, milestones focus on learning and validation.

## Purpose

This command creates a milestone plan that:
- Breaks goals into measurable progress indicators
- Focuses on learning and hypothesis validation
- Provides clear indicators of goal progress
- Enables adaptive execution based on results

## When to Use

Use `/goalkit.milestones` when:
- You have a well-defined goal with selected strategy
- You need to break the goal into achievable progress steps
- You want to establish clear validation points
- You're ready to plan execution with learning focus

## Input Format

```
/goalkit.milestones [description of milestone structure and measurement approach]
```

### Example Input

```
/goalkit.milestones Create milestones that validate the task management approach:
1. Core concept validation with paper prototypes
2. Technical feasibility with working prototype
3. User value validation with small user group
4. Business model validation with broader rollout
Focus on learning at each step and measurable progress indicators.
```

## Output

The command generates:
- `goals/[###-goal-name]/milestones.md` - Comprehensive milestone plan
- Measurement framework for tracking progress
- Learning objectives for each milestone
- Foundation for adaptive execution

### Agent File Creation Instructions

When processing `/goalkit.milestones` commands, AI agents should:
1. Locate the appropriate goal directory in the `goals/` folder (the most recently created or specified goal)
2. Create the `milestones.md` file inside that goal directory
3. Use the current date in YYYY-MM-DD format for the "Date" field
4. Write the complete milestone plan using the template structure below
5. Reference the associated goal and strategy in the document header
6. After creating the milestones file, inform the user that the milestone plan has been completed and suggest next steps using `/goalkit.execute`

### File Creation Process
- **Locate Directory**: `goals/[###-goal-name]/` (most recent goal or specified goal)
- **Create File**: `goals/[###-goal-name]/milestones.md` with the milestone content
- **Template**: Use the structure provided in the "Milestone Components" section below

## Milestone Components

### 1. Milestone Definition Framework
- **Measurable Outcomes**: Clear indicators of milestone achievement
- **Learning Objectives**: What to discover at each milestone
- **Value Delivery**: User/business value at each step
- **Implementation Approaches**: Different ways to achieve the milestone

### 2. Progress Tracking Framework
- **Overall Progress Metrics**: How to measure goal advancement
- **Milestone Health Indicators**: Signs of milestone success or trouble
- **Adaptation Triggers**: When to adjust approach or sequence

### 3. Review Process
- **Milestone Review Cadence**: Regular assessment schedule
- **Review Framework**: What to evaluate at each review
- **Decision Framework**: How to adapt based on results

### 4. Success Validation
- **Milestone Success Criteria**: When milestone is considered complete
- **Goal Progress Indicators**: How milestone advances the goal
- **Learning Quality Assessment**: How to evaluate insights gained

## Key Differences from Spec-Driven Development

| Spec-Driven | Goal-Driven |
|-------------|-------------|
| Detailed task breakdowns | Measurable milestone definitions |
| Implementation activity focus | Learning and validation focus |
| Linear task execution | Adaptive milestone progression |
| Specification compliance | Outcome and learning validation |

## Integration with Other Commands

### Before Using `/goalkit.milestones`
- **`/goalkit.vision`**: Provides guiding principles for milestone design
- **`/goalkit.goal`**: Defines the goal milestones should advance
- **`/goalkit.strategies`**: Provides strategy context for milestone planning

### After Using `/goalkit.milestones`
- **`/goalkit.execute`**: Implement milestones with learning and adaptation

## Best Practices

### Milestone Design
- **Measurable Outcomes**: Each milestone should have clear success indicators
- **Independent Value**: Milestones should deliver standalone value
- **Learning Focus**: Every milestone should test key hypotheses
- **Progressive Validation**: Early milestones validate riskiest assumptions

### Progress Tracking
- **Multiple Indicators**: Use several metrics to validate each milestone
- **Regular Assessment**: Review progress at appropriate intervals
- **Adaptation Readiness**: Plan how to adjust based on results
- **Stakeholder Communication**: Keep stakeholders informed of progress

### Learning Integration
- **Hypothesis Testing**: Frame milestones as assumption validation
- **Insight Capture**: Document what works and what doesn't
- **Pattern Recognition**: Identify trends across milestones
- **Knowledge Transfer**: Apply learning to subsequent milestones

## Common Milestone Patterns

### Risk-Reduction Milestones
- **Technical Risk Validation**: Prove technical approach feasibility
- **User Experience Validation**: Confirm user interaction patterns
- **Business Model Validation**: Test revenue or adoption assumptions
- **Integration Validation**: Ensure solution works in real environment

### Value-Delivery Milestones
- **Core Value Milestones**: Deliver fundamental user benefit
- **Enhancement Milestones**: Add incremental improvements
- **Scale Milestones**: Expand to broader user base
- **Optimization Milestones**: Improve existing functionality

### Learning Milestones
- **Exploration Milestones**: Test new approaches or technologies
- **Comparison Milestones**: Evaluate different strategy options
- **Optimization Milestones**: Improve based on user feedback
- **Innovation Milestones**: Introduce novel capabilities

## Validation and Adaptation

### Milestone Review Process
- **Completion Review**: Assess if milestone achieved intended outcomes
- **Learning Review**: Document insights and discoveries
- **Strategy Review**: Evaluate if current approach remains valid
- **Planning Review**: Adjust subsequent milestones based on learning

### Adaptation Framework
- **Continue**: When milestones validate current approach
- **Adjust**: When milestones suggest minor modifications
- **Pivot**: When milestones indicate major strategy change needed
- **Pause**: When external factors require reassessment

## Examples

### Example 1: User Onboarding Milestone Plan
```
/goalkit.milestones For user onboarding improvement:
1. Onboarding flow clarity (measure comprehension)
2. Value proposition validation (measure early engagement)
3. Feature discovery optimization (measure feature usage)
4. Long-term retention improvement (measure sustained usage)
Each milestone should validate key onboarding hypotheses.
```

### Example 2: Performance Improvement Milestone Plan
```
/goalkit.milestones For application performance:
1. Baseline measurement and bottleneck identification
2. Critical path optimization (measure core interaction speed)
3. Secondary optimization (measure overall responsiveness)
4. Scale validation (measure performance under load)
Focus on measurable speed and responsiveness improvements.
```

### Example 3: Feature Development Milestone Plan
```
/goalkit.milestones For new feature development:
1. Core concept validation (measure user interest)
2. Technical feasibility demonstration (measure implementation possibility)
3. User experience validation (measure usability and satisfaction)
4. Business value confirmation (measure adoption and retention)
Each milestone should demonstrate clear progress toward feature goals.