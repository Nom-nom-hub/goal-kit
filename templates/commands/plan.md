# /plan Command
*Create detailed technical implementation plans from strategy*

## Overview
The `/plan` command transforms high-level strategies into detailed technical implementation plans. This includes specific tasks, timelines, dependencies, and resource requirements.

## When to Use
- After strategies are defined with `/strategize`
- When you need to break down work into actionable tasks
- Before starting implementation work
- When creating project timelines and milestones

## Usage
```
/plan [STRATEGY_FILE] [DETAIL_LEVEL]
```

**Options:**
- `basic`: High-level phases only
- `standard`: Moderate detail with timelines (default)
- `detailed`: Comprehensive plan with all aspects

**Examples:**
```
/plan strategies/user-authentication-strategy.md
```

```
/plan strategies/payment-system-strategy.md detailed
```

## What It Does
1. **Analyzes strategy document** to understand approach and goals
2. **Breaks down into phases** with specific deliverables
3. **Identifies dependencies** between different components
4. **Estimates timelines** and resource requirements
5. **Creates risk assessments** with mitigation strategies
6. **Generates detailed plan** in `plans/[FEATURE_NAME]/implementation-plan.md`
7. **Creates task breakdown** ready for `/tasks` command

## Plan Structure
The generated plan document includes:
- **Project overview** and strategic alignment
- **Implementation phases** with specific deliverables
- **Technical architecture** and component breakdown
- **Resource requirements** and team assignments
- **Timeline estimates** with milestones
- **Risk assessment** and mitigation strategies
- **Success criteria** for each phase

## Planning Process
1. **Strategy Review**: Understand the chosen technical approach
2. **Scope Definition**: Break down into manageable phases
3. **Task Identification**: List all required implementation tasks
4. **Dependency Mapping**: Identify task relationships and prerequisites
5. **Resource Planning**: Determine team, tools, and infrastructure needs
6. **Risk Analysis**: Identify potential issues and mitigation plans
7. **Timeline Creation**: Establish realistic schedules and milestones

## Best Practices
- **Start with MVP scope**: Focus on core functionality first
- **Be realistic**: Account for team capacity and technical complexity
- **Include buffer time**: Plan for unexpected delays and debugging
- **Consider dependencies**: Sequence tasks in logical order
- **Document assumptions**: Make technical assumptions explicit
- **Plan for testing**: Include time for quality assurance

## Examples

### Basic Implementation Plan
```
/plan strategies/user-authentication-strategy.md basic
```

Generates:
- Phase 1: Setup authentication infrastructure
- Phase 2: Implement core authentication flows
- Phase 3: Add security measures and testing
- Phase 4: Integration and deployment

### Detailed Implementation Plan
```
/plan strategies/e-commerce-platform-strategy.md detailed
```

Generates:
- Detailed component breakdown
- Specific API endpoints and data models
- Integration points with external services
- Security and performance considerations
- Testing strategy for each component
- Deployment and monitoring plans

## Next Steps
After creating plans with `/plan`:
1. **Review the implementation plan** for feasibility
2. **Use `/tasks`** to generate actionable task lists
3. **Assign tasks** to team members
4. **Use `/implement`** to track progress
5. **Use `/analyze`** to validate plan alignment
6. **Update plans** as implementation progresses

## Troubleshooting
- **Plan seems overwhelming**: Break into smaller, focused phases
- **Unclear dependencies**: Use `/analyze` to identify missing connections
- **Resource conflicts**: Adjust timelines or scope to match capacity
- **Technical uncertainty**: Add research spikes to early phases
- **Timeline too aggressive**: Add buffer time and review estimates