---
description: Manage intelligent, adaptive context based on project state and progress
scripts:
  sh: .goalkit/scripts/python/smart_context_manager.py --format text
  ps: .goalkit/scripts/python/smart_context_manager.py --format text
agent_scripts:
  sh: .goalkit/scripts/python/update_agent_context.py __AGENT__
  ps: .goalkit/scripts/python/update_agent_context.py __AGENT__
---

## Smart Context Management Command

**Purpose**: Dynamically manage agent context that adapts to current project state, phase, and priorities for intelligent assistance

**When to Use**:
- To update agent context based on current project phase and status
- When project phase changes (vision → goals → strategies → milestones → execution)
- To ensure agents have current, relevant context for intelligent assistance
- To optimize agent guidance based on project health and priorities

## Quick Prerequisites Check

**BEFORE INITIALIZING SMART CONTEXT**:
1. **Goal Kit project exists**: Verify `.goalkit/` directory structure
2. **Project has meaningful content**: Have vision, goals, or other components for context
3. **Current project state**: Have up-to-date project information for context generation
4. **Context update need**: Have changes or state evolution requiring context updates

**If missing**: Context manager can still establish baseline context for new projects.

## Quick Context Setup Steps

**STEP 1**: Analyze current project state and phase

**STEP 2**: Assess project health and progress status

**STEP 3**: Generate intelligent context based on current priorities

**STEP 4**: Update all relevant agent context files

**STEP 5**: Validate context relevance and accuracy

**STEP 6**: Monitor effectiveness of updated context

## Smart Context Features

**Intelligence Capabilities**:
- **Phase Detection**: Automatically determine current project phase
- **Health Assessment**: Evaluate project status and potential risks
- **Priority Identification**: Highlight current focus areas and priorities
- **Adaptive Content**: Context that changes based on project evolution

**Context Management**:
- **Multi-Platform Updates**: Update context across all agent platforms
- **Intelligent Prioritization**: Focus on most relevant information
- **Dynamic Refresh**: Automatically update when project state changes significantly
- **Quality Assurance**: Ensure context accuracy and relevance

## Input Format

```
/goalkit.smart [options]
```

### Command Options

```
/goalkit.smart                    # Update context with current project intelligence
/goalkit.smart --analyze-only     # Analyze state without updating context files
/goalkit.smart --detailed         # Generate detailed context analysis
/goalkit.smart --json             # Output analysis in JSON format
/goalkit.smart --refresh          # Force refresh of all context components
```

## Agent Script Execution Guide

**CRITICAL**: When processing `/goalkit.smart` commands, agents MUST:

### **STEP 1**: Run the smart context manager script
```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/smart_context_manager.py --format text
```

### **STEP 2**: If analysis-only mode requested
```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/smart_context_manager.py --analyze-only --format text
```

### **STEP 3**: Parse context intelligence results
- **Extract current phase** for context prioritization
- **Note project health** for risk awareness
- **Identify active goals** for focus areas
- **Review recommendations** for next steps

### **STEP 4**: Assess context quality
- **Relevance**: Ensure context matches current project needs
- **Accuracy**: Verify context reflects actual project state
- **Completeness**: Confirm context includes necessary information
- **Timeliness**: Ensure context is up-to-date with latest changes

### **STEP 5**: Update agent context with intelligence results
```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/update_agent_context.py
```

## Output

The command generates:
- **Context Analysis**: Current project state and phase assessment
- **Updated Context Files**: Refreshed agent context across all platforms
- **Priority Updates**: Current focus areas and recommendations
- **Risk Assessment**: Current project risks and concerns
- **Smart Recommendations**: Context-aware suggestions for next steps

### Context Management Process

**Intelligent Analysis and Update**:
1. **State Detection**: Determine current project phase and status
2. **Health Assessment**: Evaluate overall project health and risks
3. **Priority Identification**: Set focus areas based on current needs
4. **Context Generation**: Create adaptive context for current state
5. **Multi-Platform Update**: Apply context across all agent platforms

## Context Components

### 1. Project State Intelligence
- **Current Phase**: Vision, goal creation, strategy, milestone, or execution
- **Project Health**: Overall assessment of project status and risks
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

## Context Intelligence Standards

### State Detection Accuracy
- **Phase Recognition**: Correctly identify current project phase
- **Health Assessment**: Accurate evaluation of project status
- **Priority Setting**: Proper identification of focus areas
- **Risk Identification**: Clear understanding of potential issues

### Context Quality
- **Relevance**: Context matches current project needs
- **Accuracy**: Context reflects actual project state
- **Timeliness**: Context is current and up-to-date
- **Actionability**: Context enables intelligent decision-making

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
/goalkit.smart → Update with vision-focused context
/goalkit.goal → Create goals
/goalkit.smart → Update with goal-focused context
[Continue workflow with intelligent context]
```

## Best Practices

### Context Management
- **Regular Updates**: Update context regularly, especially after major changes
- **Phase Transitions**: Update context when moving between major phases
- **Status Changes**: Update when project health or status changes significantly
- **Quality Assurance**: Verify context accuracy and relevance

### Intelligent Assistance
- **Adaptive Behavior**: Change agent behavior based on current context
- **Priority Awareness**: Focus on what matters most right now
- **Risk Consciousness**: Be aware of current project risks
- **Progress Optimization**: Suggest actions that improve project outcomes

### Context Optimization
- **Relevance Focus**: Include only information necessary for current phase
- **Clarity and Structure**: Ensure context is clear and actionable
- **Evolution Tracking**: Keep context aligned with project evolution
- **Learning Integration**: Include lessons learned in context

## Common Context Scenarios

### Phase-Specific Context
- **Vision Phase**: Focus on foundational principles and long-term thinking
- **Goal Creation**: Emphasis on specific, measurable outcomes
- **Strategy Phase**: Exploration of multiple approaches and analysis
- **Execution Phase**: Focus on measurement, learning, and adaptation

### Health-Based Context
- **Excellent Health**: Maintain momentum, continue current approach
- **Good Health**: Monitor trends, consider optimizations
- **Concerning Health**: Focus on risk mitigation and improvement
- **Critical Health**: Immediate intervention and course correction

### Priority-Driven Context
- **Goal-Driven**: Prioritize activities supporting active goals
- **Risk-Driven**: Focus on risk mitigation and stability
- **Progress-Driven**: Emphasize momentum and velocity
- **Quality-Driven**: Prioritize quality and validation

## Examples

### Example 1: Regular Context Update
```
/goalkit.smart
```
**Output**: Analyzes current state and updates all agent context files with intelligent, adaptive context

### Example 2: Analysis-Only Mode
```
/goalkit.smart --analyze-only
```
**Output**: Provides context analysis and recommendations without updating files

### Example 3: Detailed Context Analysis
```
/goalkit.smart --detailed
```
**Output**: Comprehensive context analysis with deep insights

### Example 4: Context Integration with Validation
```
/goalkit.goal Create user engagement goal
/goalkit.validate
/goalkit.smart --analyze-only
[Review context recommendations]
/goalkit.smart
[Agent now has updated context for goal-focused assistance]
```

## Agent Integration

### Context-Aware Intelligence
**CRITICAL**: Agents should leverage smart context for enhanced assistance:

1. **Dynamic Adaptation**: Change behavior based on current project phase
2. **Priority Awareness**: Focus on what matters most right now
3. **Risk Consciousness**: Be aware of current project risks
4. **Progress Integration**: Use progress data for better recommendations

### Automated Context Management
- **Trigger-Based Updates**: Update context after major changes
- **Scheduled Refreshes**: Regular context updates for active projects
- **Event-Driven Updates**: Update when specific milestones are reached
- **Quality-Triggered Updates**: Update when validation results change significantly

## Context Applications

### Intelligent Assistance
- **Phase-Appropriate Actions**: Different assistance for different phases
- **Quality Enforcement**: Use context to maintain quality standards
- **Progress Optimization**: Suggest actions that improve project velocity
- **Risk Mitigation**: Avoid actions that increase current risks

### Decision Support
- **Context-Based Prioritization**: Focus on priorities set by context
- **Risk-Aware Decisions**: Consider current risks in decision-making
- **Phase-Appropriate Approaches**: Use context-appropriate methods
- **Learning Integration**: Apply lessons learned from context

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

**After `/goalkit.smart`**:
- **Context Analysis**: Review current project state and priorities
- **Priority Alignment**: Ensure current work aligns with context priorities
- **Risk Consideration**: Address any context-identified risks
- **Recommendation Implementation**: Consider context suggestions for next steps
- **Context-Driven Workflow**: Align actions with context-aware priorities