# /tasks Command
*Generate actionable tasks from implementation plans*

## Overview
The `/tasks` command transforms detailed implementation plans into specific, actionable tasks that can be assigned to team members and tracked through completion.

## When to Use
- After implementation plans are created with `/plan`
- When you need to break down work into manageable tasks
- Before assigning work to team members
- When creating sprint or iteration backlogs

## Usage
```
/tasks [PLAN_FILE] [OUTPUT_FORMAT]
```

**Options:**
- `markdown`: Task list in markdown format (default)
- `json`: Structured JSON format for tools
- `csv`: Comma-separated values for spreadsheets

**Examples:**
```
/tasks plans/user-authentication-plan.md
```

```
/tasks plans/payment-integration-plan.md json
```

## What It Does
1. **Analyzes implementation plan** to extract work items
2. **Breaks down into specific tasks** with clear deliverables
3. **Adds task metadata** including estimates and dependencies
4. **Generates task hierarchy** with phases and priorities
5. **Creates task tracking document** in `tasks/[FEATURE_NAME]/tasks.md`
6. **Provides assignment recommendations** based on task types

## Task Structure
Generated task documents include:
- **Task hierarchy** organized by implementation phases
- **Task descriptions** with specific deliverables
- **Priority levels** (Critical, High, Medium, Low)
- **Time estimates** for effort planning
- **Dependencies** between related tasks
- **Assignment suggestions** based on skills required
- **Success criteria** for task completion

## Task Generation Process
1. **Plan Analysis**: Parse the implementation plan structure
2. **Task Decomposition**: Break phases into specific tasks
3. **Dependency Mapping**: Identify task relationships
4. **Priority Assignment**: Order tasks by importance and sequence
5. **Resource Estimation**: Add time and skill requirements
6. **Validation**: Ensure all plan elements have corresponding tasks

## Best Practices
- **Be specific**: Each task should have a clear, verifiable outcome
- **Keep tasks small**: Aim for 2-8 hour tasks when possible
- **Include context**: Add enough detail for task execution
- **Consider dependencies**: Sequence tasks in logical order
- **Add acceptance criteria**: Define what "done" means for each task
- **Balance workload**: Distribute tasks across team capabilities

## Examples

### User Authentication Tasks
```
/tasks plans/user-authentication-plan.md
```

Generates tasks like:
- Set up authentication service infrastructure
- Implement user registration endpoint
- Create login/logout functionality
- Add password reset mechanism
- Implement session management
- Add user profile management
- Create authentication middleware
- Write unit tests for auth components

### Mobile App Tasks
```
/tasks plans/mobile-app-plan.md
```

Generates tasks like:
- Set up React Native development environment
- Configure navigation structure
- Implement user onboarding screens
- Create core app screens and components
- Add local data storage
- Implement push notifications
- Add offline synchronization
- Performance optimization and testing

## Task Prioritization
- **Critical**: Must be done first, project blockers
- **High**: Important for core functionality
- **Medium**: Enhances user experience
- **Low**: Nice-to-have features

## Next Steps
After generating tasks with `/tasks`:
1. **Review task list** for completeness and accuracy
2. **Assign tasks** to team members based on skills
3. **Set up tracking** system (GitHub issues, project boards, etc.)
4. **Use `/implement`** to track progress and completion
5. **Update tasks** as work progresses and new requirements emerge
6. **Use `/analyze`** to ensure task alignment with goals

## Troubleshooting
- **Tasks too vague**: Add more specific acceptance criteria
- **Too many tasks**: Group related tasks or defer non-essential ones
- **Unclear dependencies**: Review plan structure and add missing links
- **Imbalanced workload**: Redistribute tasks across team members
- **Missing skills**: Identify training needs or external resources
- **Timeline issues**: Adjust scope or add buffer time for complex tasks