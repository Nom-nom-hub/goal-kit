# /goalkit.explore Command

## Overview

The `/goalkit.explore` command dives deeper into specific strategy options, alternative approaches, and what-if scenarios for achieving your goals.

## Purpose

This command provides detailed exploration of:
- Alternative implementation approaches
- What-if scenarios and edge cases
- Deeper technical analysis of strategy options
- Comparative evaluation of different approaches

## When to Use

Use `/goalkit.explore` when:
- You need deeper analysis of specific strategy options
- You want to investigate what-if scenarios
- You need to compare alternative approaches in detail
- You're considering pivoting from current strategy

## Input Format

```
/goalkit.explore [specific area to explore or alternative approaches to investigate]
```

### Example Input

```
/goalkit.explore Dive deeper into the mobile-first vs web-first strategy options for user onboarding. Consider edge cases like offline users, different device types, and accessibility requirements.
```

## Output

The command generates:
- Detailed analysis of specific strategy options
- What-if scenario exploration
- Risk-benefit analysis of alternatives
- Recommendations for next steps

### Agent File Creation Instructions

When processing `/goalkit.explore` commands, AI agents should:
1. Determine if the exploration is related to a specific goal in the `goals/` folder
2. If related to a specific goal, consider creating or updating exploration notes in that goal's directory
3. Provide the detailed analysis with clear recommendations
4. If the exploration is significant enough, suggest creating an `exploration.md` file in the relevant goal directory
5. Reference any related goals, strategies, or milestones in the analysis

### File Creation Process
- **Optional File**: `goals/[###-goal-name]/exploration.md` (if exploration is substantial and goal-specific)
- **Template**: Use the structure provided in the "Exploration Areas" section below

## Exploration Areas

### 1. Technical Strategy Deep Dive
- **Architecture Options**: Monolith vs microservices vs serverless
- **Technology Choices**: Different frameworks, libraries, or platforms
- **Scalability Approaches**: Horizontal vs vertical scaling strategies
- **Performance Optimization**: Various performance improvement techniques

### 2. User Experience Exploration
- **User Journey Alternatives**: Different ways users could achieve the goal
- **Interaction Patterns**: Various UI/UX approaches to the same problem
- **Accessibility Scenarios**: How different users with different abilities would use the solution
- **Cross-Platform Consistency**: Ensuring good experience across devices

### 3. Implementation Strategy Analysis
- **Development Approaches**: Waterfall vs agile vs exploratory
- **Team Structures**: Individual vs paired vs mob programming
- **Testing Strategies**: Manual vs automated vs continuous testing
- **Deployment Options**: Various release and deployment strategies

### 4. Risk and Edge Case Exploration
- **Failure Mode Analysis**: What could go wrong and how to mitigate
- **Edge Case Identification**: Unusual but important scenarios
- **Recovery Strategies**: How to recover from various failure modes
- **Contingency Planning**: Backup plans for when primary strategy fails

## Key Differences from Other Commands

| Command | Focus | Output |
|---------|-------|--------|
| **`/goalkit.strategies`** | Broad strategy comparison | High-level strategy options |
| **`/goalkit.explore`** | Deep-dive into specifics | Detailed analysis and scenarios |
| **`/goalkit.milestones`** | Measurable progress steps | Actionable milestone definitions |

## Integration with Other Commands

### Before Using `/goalkit.explore`
- **`/goalkit.strategies`**: Should be completed to identify options for exploration
- **`/goalkit.goal`**: Provides context for what exploration is valuable

### After Using `/goalkit.explore`
- **`/goalkit.strategies`**: Update strategy document with new findings
- **`/goalkit.milestones`**: Refine milestones based on deeper understanding
- **`/goalkit.adapt`**: Use insights to adapt current approach

## Best Practices

### Exploration Planning
- **Focused Scope**: Explore one strategy or scenario at a time
- **Clear Objectives**: Define what you want to learn from the exploration
- **Evidence-Based**: Use data and research to inform exploration
- **Practical Constraints**: Consider real-world limitations and constraints

### Documentation of Findings
- **Clear Conclusions**: Document what was learned
- **Actionable Insights**: Provide specific recommendations
- **Risk Assessment**: Identify new risks discovered during exploration
- **Next Steps**: Define follow-up actions based on findings

## Common Exploration Patterns

### Technical Deep Dives
- Comparing similar tools or frameworks in detail
- Analyzing performance characteristics of different approaches
- Investigating integration complexity with existing systems
- Evaluating long-term maintenance implications

### User Experience Scenarios
- Exploring how different user types would interact with the solution
- Investigating accessibility challenges and solutions
- Analyzing cross-cultural or international usage patterns
- Understanding edge cases and error conditions

### Business Case Analysis
- Detailed cost-benefit analysis of different approaches
- Market research into user preferences and behaviors
- Competitive analysis of similar solutions
- ROI projections for different strategy options

## Examples

### Example 1: Mobile Strategy Exploration
```
/goalkit.explore Compare React Native vs Flutter vs native iOS/Android for the user onboarding goal. Consider development speed, performance, maintenance overhead, and ecosystem maturity. Include analysis of offline capability and cross-platform consistency.
```

### Example 2: Data Strategy Exploration
```
/goalkit.explore Investigate different data storage and processing options for user analytics. Compare traditional databases vs NoSQL vs data warehouses vs real-time streaming. Consider query performance, scalability needs, and data consistency requirements.
```

### Example 3: Team Structure Exploration
```
/goalkit.explore Analyze different team structures for implementing the collaboration features. Compare dedicated teams vs cross-functional vs outsourced development. Consider communication overhead, domain knowledge requirements, and delivery speed.