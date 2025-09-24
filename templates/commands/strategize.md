# /strategize Command
*Develop implementation strategies aligned with project goals*

## Overview
The `/strategize` command creates technical implementation strategies that directly support your defined goals. This bridges the gap between high-level objectives and concrete technical plans.

## When to Use
- After goals are clearly defined with `/goals`
- When you need to evaluate different technical approaches
- Before creating detailed implementation plans
- When considering build vs. buy decisions

## Usage
```
/strategize [STRATEGY_DESCRIPTION]
```

**Examples:**
```
/strategize We want to use a modern web stack with fast development cycles, good user experience, and scalable architecture
```

```
/strategize Focus on mobile-first design with React Native, cloud deployment, and microservices architecture
```

## What It Does
1. **Analyzes your defined goals** to understand requirements
2. **Evaluates multiple technical approaches** against your goals
3. **Creates implementation strategies** with clear rationale
4. **Generates a strategy document** in `strategies/[FEATURE_NAME]/strategy.md`
5. **Assesses risks and dependencies** for each approach
6. **Provides implementation roadmaps** with phases and milestones

## Strategy Structure
The generated strategy document includes:
- **Goals alignment** and approach rationale
- **Technical architecture** and technology stack justification
- **Implementation roadmap** with phases and milestones
- **Risk assessment** with mitigation plans
- **Success criteria** for each implementation phase

## Strategy Development Process
1. **Goal Analysis**: Review and understand the defined goals
2. **Approach Evaluation**: Consider multiple technical solutions
3. **Trade-off Analysis**: Compare approaches based on:
   - Goal alignment
   - Technical feasibility
   - Development effort
   - Risk level
   - Long-term maintainability
4. **Strategy Selection**: Choose the optimal approach with clear justification
5. **Roadmap Creation**: Break down into implementation phases

## Best Practices
- **Stay focused on goals**: Every technical decision should support objectives
- **Consider alternatives**: Always evaluate 2-3 different approaches
- **Think long-term**: Consider maintenance, scalability, and evolution
- **Be realistic**: Account for team capabilities and resource constraints
- **Document trade-offs**: Explain why the chosen approach is optimal

## Examples

### Good Strategy Definition
```
/strategize For our task management app, we want to use a full-stack JavaScript approach with React for the frontend, Node.js/Express for the backend, and MongoDB for data storage. We prefer this because it allows for rapid development, good developer experience, and easy scaling
```

### Strategy with Multiple Options
```
/strategize Evaluate different approaches for our e-commerce platform: 1) Monolithic Rails app, 2) Microservices with Docker, 3) Serverless AWS architecture. Consider development speed, scalability needs, and team expertise
```

### Mobile-First Strategy
```
/strategize Implement a mobile-first approach using React Native for cross-platform compatibility, Firebase for backend services, and focus on offline-first capabilities with local data synchronization
```

## Next Steps
After creating strategies with `/strategize`:
1. **Review the strategy document** for technical feasibility
2. **Refine if needed** based on team capabilities or constraints
3. **Use `/plan`** to create detailed technical implementation plans
4. **Use `/tasks`** to break down into actionable development tasks
5. **Use `/implement`** to execute the development work

## Troubleshooting
- **Strategy doesn't align with goals**: Go back to `/goals` to clarify objectives
- **Too many technical options**: Focus on the approaches that best support your goals
- **Risks seem too high**: Consider simpler approaches or break into phases
- **Unclear trade-offs**: Ask for detailed comparison of alternatives
- **Implementation timeline unclear**: Request more detailed phase breakdowns