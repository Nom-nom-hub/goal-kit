---
description: Execute goals with learning, measurement, and adaptation. Requires completed goal, strategies, and milestones.
agent_scripts:
  sh: .goalkit/scripts/python/update_agent_context.py __AGENT__
  ps: .goalkit/scripts/python/update_agent_context.py __AGENT__
---

## Quick Prerequisites Check

**BEFORE EXECUTING**:
1. **Goal exists**: Check `goals/` directory for goal files
2. **Strategies defined**: Verify `strategies.md` in goal directory
3. **Milestones created**: Verify `milestones.md` in goal directory

**If missing any**: Tell user to complete full sequence first.

## Simple vs Complex Assessment

- **Simple tasks** (direct implementation): "fix styling", "update header", "add margin"
- **Complex goals** (use methodology): features with measurable outcomes

## Quick Execution Steps

**STEP 1**: Identify the goal to execute (most recent or specified)

**STEP 2**: Review the goal's strategies and milestones

**STEP 3**: Create `execution.md` in the goal directory with:
- Current milestone focus
- Measurement framework
- Learning loop process
- Adaptation triggers

**STEP 4**: Implement with daily learning and weekly adaptation

**STEP 5**: Document all insights and learnings

## Key Execution Mindset

- **Test hypotheses** rather than follow rigid plans
- **Measure and adapt** based on real results
- **Document learnings** for future decisions
- **Stay flexible** to change approaches when needed

## Critical Rules

✅ **DO**: Focus on learning and adaptation
✅ **DO**: Measure progress with defined metrics
✅ **DO**: Document insights and knowledge gained
✅ **DO**: Be ready to pivot based on evidence
❌ **DON'T**: Follow rigid, untested plans
❌ **DON'T**: Ignore measurement and feedback
❌ **DON'T**: Skip documentation of learnings

## Overview

The `/goalkit.execute` command implements milestones with continuous learning, measurement, and adaptation. Unlike implementation that follows rigid plans, execution focuses on hypothesis testing and flexible adaptation.

## Purpose

This command creates an adaptive execution framework that:
- Implements milestones with learning and measurement focus
- Provides framework for daily learning loops
- Enables data-driven adaptation and pivots
- Documents insights and knowledge gained

## When to Use

Use `/goalkit.execute` when:
- You have defined milestones with clear success criteria
- You're ready to implement with measurement and learning
- You want to maintain flexibility to adapt based on results
- You need structured approach to hypothesis testing

## Input Format

```
/goalkit.execute [description of execution approach and learning focus]
```

### Example Input

```
/goalkit.execute Implement the first milestone with daily measurement and weekly adaptation reviews. Focus on learning from user feedback and being willing to pivot strategies based on results. Document all insights and maintain flexibility for approach changes.
```

## Output

The command generates:
- `goals/[###-goal-name]/execution.md` - Adaptive execution guide
- Measurement framework for tracking progress
- Learning capture system for insights
- Adaptation framework for strategy changes

### Agent File Creation Instructions

When processing `/goalkit.execute` commands, AI agents should:
1. Locate the appropriate goal directory in the `goals/` folder (the most recently created or specified goal)
2. Create the `execution.md` file inside that goal directory
3. Use the current date in YYYY-MM-DD format for the "Date" field
4. Write the complete execution plan using the template structure below
5. Reference the associated goal, strategy, and milestones in the document header
6. After creating the execution file, inform the user that the execution plan has been completed and suggest beginning implementation

### File Creation Process
- **Locate Directory**: `goals/[###-goal-name]/` (most recent goal or specified goal)
- **Create File**: `goals/[###-goal-name]/execution.md` with the execution content
- **Template**: Use the structure provided in the "Execution Components" section below

## Execution Components

### 1. Execution Strategy
- **Current Milestone Focus**: Which milestone is being executed
- **Hypothesis Testing**: What assumptions are being validated
- **Success Criteria**: How to know milestone is achieved
- **Alternative Approaches**: Backup plans if primary approach fails

### 2. Measurement Framework
- **Key Metrics**: What to measure during execution
- **Measurement Methods**: How to collect data
- **Success Thresholds**: When milestone is considered successful
- **Learning Indicators**: Signs of valuable insights

### 3. Learning Loop Process
- **Daily Learning Loop**: Build-measure-learn cycle
- **Weekly Learning Loop**: Strategic review and adaptation
- **Progress Assessment**: Regular evaluation of advancement
- **Insight Documentation**: Capture of learnings and discoveries

### 4. Adaptation Framework
- **Progress Indicators**: Signs that current approach is working
- **Warning Indicators**: Early signs of problems
- **Pivot Decision Process**: Framework for changing approach
- **Strategy Switch Options**: Alternative approaches available

## Key Differences from Spec-Driven Development

| Spec-Driven | Goal-Driven |
|-------------|-------------|
| Rigid plan execution | Adaptive hypothesis testing |
| Implementation compliance focus | Learning and outcome focus |
| Linear task completion | Flexible milestone progression |
| Specification-driven changes | Evidence-based adaptations |

## Integration with Other Commands

### Before Using `/goalkit.execute`
- **`/goalkit.vision`**: Provides principles for execution decisions
- **`/goalkit.goal`**: Defines outcomes to achieve through execution
- **`/goalkit.strategies`**: Provides approach options for execution
- **`/goalkit.milestones`**: Defines what to execute and measure

### After Using `/goalkit.execute`
- **`/goalkit.execute`**: Continue execution with adaptation based on learning
- **Goal Completion**: When all milestones are complete, consider the goal achieved

## Best Practices

### Execution Mindset
- **Hypothesis Testing**: Treat implementation as experiment
- **Learning Orientation**: Focus on insights over just completion
- **Adaptation Readiness**: Be willing to change course based on evidence
- **Documentation Discipline**: Capture all significant learnings

### Daily Execution
- **Structured Days**: Clear goals and measurement for each day
- **Progress Tracking**: Regular assessment of advancement
- **Obstacle Management**: Clear process for addressing blockers
- **Insight Capture**: Document learnings as they occur

### Measurement and Learning
- **Relevant Metrics**: Track what matters for goal achievement
- **Regular Review**: Assess progress at appropriate intervals
- **Pattern Recognition**: Identify trends and insights
- **Knowledge Sharing**: Communicate learnings to stakeholders

## Common Execution Patterns

### Learning-Focused Execution
- **Hypothesis-Driven Development**: Each day tests specific assumptions
- **Measurement-First**: Define success criteria before implementation
- **Feedback Integration**: Incorporate user and stakeholder input
- **Insight Documentation**: Capture all learnings systematically

### Adaptive Execution
- **Progress Monitoring**: Regular assessment of milestone advancement
- **Pivot Readiness**: Framework for changing approaches when needed
- **Risk Management**: Active monitoring and mitigation of issues
- **Stakeholder Communication**: Regular updates on progress and learnings

### Knowledge Capture Patterns
- **Daily Summaries**: Brief documentation of daily progress and insights
- **Weekly Reviews**: Strategic assessment of progress and direction
- **Milestone Reflections**: Comprehensive learning capture at milestone completion
- **Pattern Documentation**: Identification of repeatable insights

## Risk Management During Execution

### Risk Monitoring
- **Daily Risk Check**: Identify new risks as they emerge
- **Progress Risk Assessment**: Evaluate if current trajectory will achieve goals
- **External Risk Monitoring**: Track factors outside the project
- **Risk Documentation**: Maintain current risk register

### Risk Response
- **Mitigation Execution**: Implement planned risk responses
- **Contingency Planning**: Develop backups for critical risks
- **Risk Communication**: Keep stakeholders informed of risk status
- **Risk Review**: Regular reassessment of risk likelihood and impact

## Success Validation

### Milestone Completion
- **Success Criteria Met**: All defined success indicators achieved
- **Learning Objectives Accomplished**: Key insights documented
- **Value Delivered**: Clear user or business benefit provided
- **No Critical Issues**: No significant problems discovered

### Goal Progress
- **Measurable Advancement**: Clear progress toward goal achievement
- **Learning Integration**: Insights applied to subsequent work
- **Strategy Validation**: Current approach confirmed as effective
- **Stakeholder Alignment**: Continued support for the goal

## Examples

### Example 1: Feature Development Execution
```
/goalkit.execute Implement user onboarding with daily user feedback measurement and weekly strategy adaptation. Focus on learning what helps users understand and adopt the feature. Be ready to pivot UX approach based on user behavior data.
```

### Example 2: Platform Migration Execution
```
/goalkit.execute Execute data migration with continuous validation and rollback readiness. Measure system stability and user impact daily. Have clear pivot points for reverting to old system if issues arise.
```

### Example 3: Process Improvement Execution
```
/goalkit.execute Implement new development process with team feedback collection and productivity measurement. Focus on learning what improves developer experience and code quality. Adapt process based on team input and metric improvements.
```

## Key rules

- Focus on learning and adaptation rather than rigid plan execution
- Implement with continuous measurement and validation
- Establish clear feedback loops for adjustment
- Document insights and knowledge gained throughout execution
- **START**: After `/goalkit.execute`, you may begin implementation with learning loops
- **CONTINUE**: This is the only command where ongoing work is allowed