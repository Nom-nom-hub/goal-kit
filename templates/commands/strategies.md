---
description: Explore multiple implementation strategies for achieving goals.
scripts:
  sh: scripts/bash/setup-strategy.sh --json
  ps: scripts/powershell/setup-strategy.ps1 -Json
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

# /goalkit.strategies Command

## AI AGENT INSTRUCTIONS

When processing `/goalkit.strategies` requests, follow this structured approach:

### Goal Discovery (First Step)
1. **Locate Associated Goal**: Search for the goal that strategies will support
   - Use `glob(path="PROJECT_ROOT/.goalkit/goals", pattern="**")` to discover goals
   - Use `list_directory(path="PROJECT_ROOT/.goalkit/goals")` to enumerate goal directories
   - If user specified a goal, locate that specific goal directory
   - If multiple goals exist, ask user to clarify which goal needs strategies
   - If no goals exist, inform user that goals must be created first

### Input Analysis
1. **Identify Strategy Dimensions**: Extract technical, UX, and implementation approaches from user input
2. **Generate Multiple Options**: Create 2-3 viable strategies for each dimension (technical, UX, implementation)
3. **Evaluate Trade-offs**: Compare strategies across feasibility, effort, risk, and learning potential
4. **Recommend Starting Point**: Suggest initial strategy with clear rationale and fallback options

### Processing Framework
- Explore multiple valid approaches (not just one "correct" solution)
- Evaluate strategies against goal success criteria and vision principles
- Consider technical feasibility, user experience quality, and business impact
- Frame strategies as testable hypotheses with clear validation criteria

### Output Structure
Use the template sections below to structure your response. Provide balanced exploration of options with evidence-based recommendations and clear next steps.

---

## Overview

The `/goalkit.strategies` command explores multiple implementation approaches for achieving your defined goals. Unlike planning that focuses on a single solution, strategies emphasize exploration and comparison of different approaches.

## Purpose

This command creates a comprehensive strategy exploration document that:
- Identifies multiple valid approaches to achieve each goal
- Compares strategies across technical, UX, and business dimensions
- Evaluates risks and mitigation approaches
- Provides foundation for informed strategy selection

## When to Use

Use `/goalkit.strategies` when:
- You have a well-defined goal with clear success criteria
- You want to explore different approaches before committing
- You need to evaluate trade-offs between different strategies
- You're ready to select an approach for milestone planning

## Input Format

```
/goalkit.strategies [description of different approaches to consider and dimensions to explore]
```

### Example Input

```
/goalkit.strategies For the task management goal, explore these strategies:
1. Technical: Progressive Web App vs Native Mobile vs Desktop Application
2. UX: Kanban-style vs Time-blocking vs AI-powered organization
3. Implementation: Big bang release vs Iterative feature rollout vs MVP-first
Consider trade-offs in development complexity, user adoption barriers, and maintenance overhead.
```

## Output

The command generates:
- `goals/[###-goal-name]/strategies.md` - Comprehensive strategy analysis
- Strategy comparison framework for informed decision-making
- Risk assessment and mitigation plans for each strategy
- Foundation for milestone planning and execution

### Agent File Creation Instructions

When processing `/goalkit.strategies` commands, AI agents should:
1. Locate the appropriate goal directory in the `goals/` folder (the most recently created or specified goal)
2. Create the `strategies.md` file inside that goal directory
3. Use the current date in YYYY-MM-DD format for the "Date" field
4. Write the complete strategy analysis using the template structure below
5. Reference the associated goal in the document header
6. After creating the strategies file, inform the user that the strategy analysis has been completed and suggest next steps using `/goalkit.milestones`

### File Creation Process
- **Locate Directory**: `goals/[###-goal-name]/` (most recent goal or specified goal)
- **Create File**: `goals/[###-goal-name]/strategies.md` with the strategy content
- **Template**: Use the structure provided in the "Strategy Components" section below

## Strategy Components

### 1. Strategy Exploration Framework
- **Technical Strategy Options**: Different technologies and architectures
- **User Experience Strategies**: Various approaches to user interaction
- **Implementation Strategies**: Different development and rollout approaches

### 2. Strategy Comparison Matrix
- **Technical Feasibility**: How practical each strategy is to implement
- **User Experience Quality**: How well each strategy serves users
- **Development Effort**: Resources required for each strategy
- **Risk Level**: Potential issues and their likelihood
- **Learning Potential**: What each strategy can teach

### 3. Recommended Starting Strategy
- **Primary Recommendation**: Which strategy to try first
- **Rationale**: Evidence-based reasoning for the choice
- **Success Criteria**: How to validate if the strategy works
- **Fallback Options**: Alternative strategies if primary fails

### 4. Validation Experiments
- **Critical Assumption Tests**: Experiments to validate strategy assumptions
- **Measurement Plan**: How to evaluate strategy effectiveness
- **Success Thresholds**: When strategy is considered successful

## Key Differences from Spec-Driven Development

| Spec-Driven | Goal-Driven |
|-------------|-------------|
| Single technical implementation plan | Multiple strategy exploration |
| Detailed technical specifications | Strategy comparison and evaluation |
| One "correct" architectural approach | Multiple valid technical strategies |
| Implementation-focused planning | Learning-focused strategy testing |

## Integration with Other Commands

### Before Using `/goalkit.strategies`
- **`/goalkit.vision`**: Provides guiding principles for strategy evaluation
- **`/goalkit.goal`**: Defines the goal and success criteria for strategies

### After Using `/goalkit.strategies`
- **`/goalkit.milestones`**: Create measurable milestones for chosen strategy
- **`/goalkit.execute`**: Implement chosen strategy with adaptation framework

## Best Practices

### Strategy Exploration
- **Multiple Perspectives**: Consider technical, UX, and business viewpoints
- **Trade-off Analysis**: Explicitly evaluate pros and cons
- **Risk Assessment**: Identify potential failure modes upfront
- **Learning Focus**: Frame strategies as learning opportunities

### Strategy Selection
- **Evidence-Based Choice**: Use goal metrics to evaluate strategies
- **Start Simple**: Begin with lowest-risk, highest-learning strategy
- **Fallback Planning**: Always have alternative strategies ready
- **Adaptation Readiness**: Plan how to pivot if strategy fails

### Strategy Documentation
- **Clear Rationale**: Document why each strategy was considered
- **Comparison Criteria**: Make evaluation framework explicit
- **Risk Documentation**: Capture potential issues and mitigations
- **Learning Capture**: Document what was learned from each strategy

## Common Strategy Patterns

### Technical Strategy Patterns
- **Progressive Enhancement**: Start simple, add complexity based on user feedback
- **Platform Prioritization**: Web-first, then native mobile/desktop
- **Integration vs Build**: Use existing tools vs custom development
- **Monolith vs Microservices**: Single system vs distributed architecture

### UX Strategy Patterns
- **Guided vs Free-form**: Structured workflows vs user customization
- **Automation vs Manual**: AI assistance vs user control
- **Social vs Individual**: Community features vs personal focus
- **Simple vs Feature-rich**: Minimal interface vs comprehensive tools

### Implementation Strategy Patterns
- **MVP vs Full Feature**: Start with core functionality vs complete solution
- **Iterative vs Big Bang**: Gradual rollout vs single launch
- **Internal vs External**: Build in-house vs use external services
- **Custom vs Off-the-shelf**: Custom development vs existing solutions

## Strategy Validation

### Validation Experiments
- **Technical Validation**: Prove technical approach feasibility
- **UX Validation**: Test user experience effectiveness
- **Business Validation**: Confirm business model viability
- **Integration Validation**: Ensure strategy works in real environment

### Measurement and Learning
- **Strategy Metrics**: Track strategy-specific success indicators
- **Comparative Analysis**: Evaluate strategies against each other
- **Learning Documentation**: Capture insights for future strategies
- **Pivot Triggers**: Define when to switch strategies

## Examples

### Example 1: E-commerce Strategy Exploration
```
/goalkit.strategies For improving product discovery, explore:
1. Technical: Elasticsearch vs AI recommendations vs Hybrid approach
2. UX: Search-first vs Browse-first vs Guided discovery
3. Implementation: Gradual rollout vs Feature flags vs A/B testing
Focus on conversion impact, user satisfaction, and technical scalability.
```

### Example 2: Developer Tool Strategy Exploration
```
/goalkit.strategies For reducing context switching, consider:
1. Technical: VS Code extension vs Standalone app vs Browser extension
2. UX: Always-visible vs On-demand vs AI-triggered assistance
3. Implementation: Open source vs Commercial vs Freemium model
Evaluate based on developer adoption, productivity impact, and maintenance effort.
```

### Example 3: Mobile App Strategy Exploration
```
/goalkit.strategies For habit building app, explore:
1. Technical: React Native vs Flutter vs Native iOS/Android
2. UX: Gamification vs Social accountability vs Data-driven insights
3. Implementation: Mobile-first vs Web companion vs API-first
Consider user engagement, retention, and cross-platform compatibility.