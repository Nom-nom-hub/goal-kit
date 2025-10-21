---
description: Smart context management and intelligent agent guidance updates based on project state
scripts:
  sh: .goalkit/scripts/python/smart_context_manager.py
  ps: .goalkit/scripts/python/smart_context_manager.py
agent_scripts:
  sh: .goalkit/scripts/python/update_agent_context.py __AGENT__
  ps: .goalkit/scripts/python/update_agent_context.py __AGENT__
---

## Smart Context Management Command

**Purpose**: Update agent context files with intelligent, adaptive context based on current project state and progress

**When to Use**:
- After significant project changes or milestone completions
- When project phase changes (vision → goals → strategies → milestones → execution)
- To ensure agents have current, relevant context for assistance
- To update context with latest validation results and progress insights
- Before starting new major work phases

## Quick Prerequisites Check

**BEFORE UPDATING CONTEXT**:
1. **Goal Kit project exists**: Verify `.goalkit/` directory structure
2. **Project has content**: Have vision, goals, or other components created
3. **Recent changes made**: Context should reflect current project state

**If missing**: Create project components first or run when project has meaningful content.

## Quick Context Update Steps

**STEP 1**: Analyze current project state and phase

**STEP 2**: Assess project health and progress status

**STEP 3**: Generate intelligent context based on:
- Current project phase and priorities
- Active goals and their status
- Recent achievements and patterns
- Risk factors and recommendations

**STEP 4**: Update all agent context files with adaptive context

**STEP 5**: Provide context update summary and implications

## Context Intelligence Features

**Dynamic Analysis**:
- **Phase Detection**: Automatically determines current project phase
- **Health Assessment**: Evaluates project health (excellent/good/concerning/critical)
- **Priority Identification**: Sets context priorities based on current needs
- **Risk Analysis**: Identifies current risk factors and concerns

**Adaptive Context**:
- **Phase-Specific Guidance**: Context changes based on project phase
- **Priority-Based Focus**: Highlights what needs attention now
- **Progress-Aware Recommendations**: Suggestions based on current status
- **Quality-Integrated Standards**: Includes current quality requirements

## Input Format

```
/goalkit.context [options]
```

### Command Options

```
/goalkit.context                    # Update context with current project intelligence
/goalkit.context --analyze-only     # Analyze state without updating files
/goalkit.context --json             # Output analysis in JSON format
```

## Agent Script Execution Guide

**CRITICAL**: When processing `/goalkit.context` commands, agents MUST:

### **STEP 1**: Run the smart context analysis script
```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/smart_context_manager.py
```

### **STEP 2**: If analysis-only mode requested
```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/smart_context_manager.py --analyze-only
```

### **STEP 3**: Parse context intelligence results
- **Extract current phase** for context prioritization
- **Note project health** for risk awareness
- **Identify active goals** for focus areas
- **Review recommendations** for next steps

### **STEP 4**: Context files are automatically updated
- **All agent platforms** receive current project intelligence
- **Context includes** phase-specific priorities and recommendations
- **No manual intervention** required for context updates

### **STEP 5**: Provide context-aware user guidance
- **Phase-appropriate assistance** based on current project phase
- **Risk-aware recommendations** considering project health
- **Priority-focused suggestions** based on context priorities

## Output

The command generates:
- **Context Analysis**: Current project state and phase assessment
- **Updated Context Files**: Refreshed agent context across all platforms
- **Priority Updates**: Current focus areas and recommendations
- **Risk Assessment**: Current project risks and concerns
- **Smart Recommendations**: Context-aware suggestions for next steps

### Context Update Process

**Intelligent Analysis**:
1. **Project State Detection**: Determine current phase and status
2. **Health Assessment**: Evaluate overall project health
3. **Goal Analysis**: Review active goals and their progress
4. **Pattern Recognition**: Identify success patterns and achievements
5. **Context Generation**: Create adaptive context for current state

## Context Components

### 1. Project State Intelligence
- **Current Phase**: Vision, goal creation, strategy, milestone, or execution
- **Project Health**: Overall assessment of project status
- **Active Goals**: Number and status of current goals
- **Recent Achievements**: Latest accomplishments and milestones
- **Current Focus**: What should be prioritized now

### 2. Adaptive Priorities
- **Phase-Based Priorities**: Different focus for different project phases
- **Health-Based Adjustments**: Priority changes based on project health
- **Goal-Specific Context**: Context tailored to active goals
- **Risk-Aware Guidance**: Priorities adjusted for current risks

### 3. Smart Recommendations
- **Next Steps**: Immediate actions based on current state
- **Quality Gates**: Validation requirements for current phase
- **Progress Milestones**: Key checkpoints to monitor
- **Risk Mitigation**: Actions to address current concerns

### 4. Context Evolution
- **Dynamic Updates**: Context changes as project progresses
- **Learning Integration**: Context includes lessons learned
- **Pattern Awareness**: Context reflects successful approaches
- **Predictive Elements**: Context anticipates future needs

## Integration with Other Commands

### Context in Workflow
- **After `/goalkit.vision`**: Update with foundation principles and vision focus
- **After `/goalkit.goal`**: Update with goal-specific priorities and metrics
- **After `/goalkit.strategies`**: Update with strategy validation and approach context
- **After `/goalkit.milestones`**: Update with progress tracking and measurement focus
- **During `/goalkit.execute`**: Update with execution priorities and learning focus

### Context-Driven Assistance
```
/goalkit.vision → Create vision
/goalkit.context → Update with vision-focused context
/goalkit.goal → Create goals
/goalkit.context → Update with goal-focused context
[Continue workflow with intelligent context]
```

## Best Practices

### Regular Context Updates
- **Phase Transitions**: Update context when moving between major phases
- **Milestone Completions**: Update after significant achievements
- **Status Changes**: Update when project health changes significantly
- **Weekly Reviews**: Regular context refresh for ongoing projects

### Context Quality Management
- **Relevance**: Ensure context reflects current project reality
- **Completeness**: Include all necessary background and priorities
- **Clarity**: Make context clear and actionable for agents
- **Currency**: Keep context up-to-date with latest project state

### Context Utilization
- **Agent Guidance**: Use context for more intelligent assistance
- **Decision Support**: Base decisions on current project context
- **Priority Setting**: Let context guide what to focus on
- **Risk Awareness**: Use context for risk identification and mitigation

## Common Context Patterns

### Vision Phase Context
- **Foundation Focus**: Establishing project purpose and principles
- **Quality Emphasis**: High standards for foundational components
- **Long-term Thinking**: Strategic, outcome-focused priorities
- **Principle-Based Guidance**: Strong emphasis on methodology compliance

### Goal Creation Context
- **Outcome Focus**: Prioritize measurable user/business outcomes
- **Specificity Requirements**: Need for concrete targets and metrics
- **Validation Readiness**: Prepare for strategy exploration
- **Quality Gates**: High standards for goal definition (7.0+ score)

### Strategy Phase Context
- **Multiple Approaches**: Encourage exploration of 3+ strategies
- **Comparative Analysis**: Focus on feasibility, risk, and learning potential
- **Validation Planning**: Prepare for strategy testing and validation
- **Flexibility Emphasis**: Readiness to pivot based on results

### Execution Phase Context
- **Learning Integration**: Focus on hypothesis testing and adaptation
- **Progress Tracking**: Emphasis on measurement and milestones
- **Risk Management**: Active monitoring and mitigation
- **Knowledge Capture**: Document insights and learnings

## Examples

### Example 1: Regular Context Update
```
/goalkit.context
```
**Output**: Analyzes current state and updates all agent context files with intelligent, adaptive context

### Example 2: Analysis-Only Mode
```
/goalkit.context --analyze-only
```
**Output**: Provides context analysis and recommendations without updating files

### Example 3: Integration with Validation
```
/goalkit.goal Create user engagement goal
/goalkit.validate
/goalkit.context --analyze-only
[Review context recommendations]
/goalkit.context
```

## Agent Integration

### Context-Aware Intelligence
**CRITICAL**: Agents should leverage smart context for enhanced assistance:

1. **Dynamic Adaptation**: Change behavior based on current project phase
2. **Priority Awareness**: Focus on what matters most right now
3. **Risk Consciousness**: Be aware of current project risks
4. **Progress Integration**: Use progress data for better recommendations

### Context-Driven Behaviors
- **Phase-Appropriate Actions**: Different assistance for different phases
- **Quality Enforcement**: Use context to maintain quality standards
- **Progress Optimization**: Suggest actions that improve project velocity
- **Risk Mitigation**: Avoid actions that increase current risks

### Automated Context Management
- **Trigger-Based Updates**: Update context after major changes
- **Scheduled Refreshes**: Regular context updates for active projects
- **Event-Driven Updates**: Update when specific milestones are reached
- **Quality-Triggered Updates**: Update when validation results change significantly

## Context Quality Indicators

### Context Freshness
- **Recent Updates**: Context updated within last 24-48 hours
- **Current Phase**: Context matches actual project phase
- **Accurate Status**: Context reflects real project health and progress
- **Relevant Priorities**: Context highlights appropriate current priorities

### Context Effectiveness
- **Agent Performance**: Better agent assistance with good context
- **Decision Quality**: Better decisions with current context
- **Progress Optimization**: Improved velocity with relevant context
- **Risk Reduction**: Reduced issues with context awareness

## Key Benefits

- **Intelligent Assistance**: Agents provide more relevant, context-aware help
- **Dynamic Adaptation**: Context evolves with project needs and status
- **Progress Optimization**: Context helps focus on what matters most
- **Risk Awareness**: Context includes current risks and mitigation strategies
- **Quality Maintenance**: Context reinforces quality standards and best practices

## Critical Rules

✅ **DO**: Update context regularly, especially after major changes
✅ **DO**: Use context analysis for decision-making
✅ **DO**: Ensure context reflects current project reality
✅ **DO**: Leverage context for more intelligent agent assistance
❌ **DON'T**: Use outdated or stale context for important decisions
❌ **DON'T**: Ignore context recommendations for project priorities
❌ **DON'T**: Make changes without considering current context

## Next Steps Integration

**After `/goalkit.context`**:
- **Context Analysis**: Review current project state and priorities
- **Priority Alignment**: Ensure current work aligns with context priorities
- **Risk Consideration**: Address any context-identified risks
- **Recommendation Implementation**: Consider context suggestions for next steps

**Context-Driven Workflow**:
1. Update context → 2. Review priorities → 3. Align actions → 4. Execute with awareness → 5. Update again after changes