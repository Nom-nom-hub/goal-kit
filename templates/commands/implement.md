# /implement Command
*Execute implementation tasks and track progress*

## Overview
The `/implement` command helps execute the tasks defined in your implementation plan and tracks progress throughout the development process. This command bridges planning and execution.

## When to Use
- When you have tasks defined with `/tasks`
- During active development and implementation phases
- When tracking progress on assigned work
- For creating implementation logs and documentation
- When collaborating on task completion

## Usage
```
/implement [TASKS_FILE] [PHASE]
```

**Options:**
- `--interactive`: Interactive progress tracking (default)
- `--no-interactive`: Batch update mode
- `--phase`: Focus on specific implementation phase
- `--assignee`: Filter tasks by assignee
- `--status`: Filter by task status (pending, in-progress, completed)

**Examples:**
```
/implement tasks/user-authentication-tasks.md
```

```
/implement tasks/mobile-app-tasks.md --phase development
```

## What It Does
1. **Loads task definitions** from the specified tasks file
2. **Tracks task status** and progress updates
3. **Records implementation details** and decisions made
4. **Generates progress reports** with completion metrics
5. **Creates implementation logs** in `implementation/[FEATURE_NAME]_log.md`
6. **Updates task status** as work progresses
7. **Identifies blockers** and issues during implementation

## Implementation Process
1. **Task Review**: Examine tasks and current status
2. **Progress Tracking**: Update task completion status
3. **Detail Recording**: Capture implementation specifics
4. **Issue Identification**: Note problems and blockers
5. **Decision Documentation**: Record technical decisions made
6. **Progress Reporting**: Generate status updates
7. **Completion Validation**: Verify task completion criteria

## Implementation Tracking
The command tracks:
- **Task status**: Pending, In Progress, Completed, Blocked, Cancelled
- **Time estimates**: Original estimates vs actual time spent
- **Dependencies**: Prerequisite tasks and blocking relationships
- **Assignees**: Who is responsible for each task
- **Priority levels**: Critical, High, Medium, Low priority tasks
- **Progress notes**: Detailed implementation notes and decisions

## Best Practices
- **Update frequently**: Record progress regularly, not just at completion
- **Be specific**: Include concrete details about what was implemented
- **Note decisions**: Document why certain approaches were chosen
- **Identify blockers**: Clearly mark tasks that are stuck and why
- **Celebrate progress**: Acknowledge completed work and milestones
- **Share updates**: Keep team informed of progress and issues

## Examples

### Interactive Implementation Tracking
```
/implement tasks/user-authentication-tasks.md
```

Features:
- Step-by-step task completion
- Detailed progress notes for each task
- Blockers and issues tracking
- Implementation decision documentation
- Completion validation

### Phase-Focused Implementation
```
/implement tasks/e-commerce-platform-tasks.md --phase checkout-flow
```

Focuses on:
- Tasks specific to checkout flow implementation
- Progress tracking for that phase
- Dependencies between checkout components
- Integration testing progress
- User experience implementation notes

### Batch Status Update
```
/implement tasks/api-integration-tasks.md --no-interactive
```

For:
- Quick status updates
- Bulk task completion marking
- Progress summary generation
- Team progress reporting
- Milestone tracking

## Task Status Management
- **Pending**: Not yet started
- **In Progress**: Currently being worked on
- **Completed**: Successfully finished
- **Blocked**: Cannot proceed due to dependencies or issues
- **Cancelled**: No longer needed or replaced

## Implementation Documentation
The command generates detailed logs including:
- **Task completion details**: What was actually implemented
- **Technical decisions**: Why certain approaches were chosen
- **Challenges encountered**: Problems faced and how they were resolved
- **Code changes**: Summary of what was modified or added
- **Testing approach**: How completion was validated
- **Next steps**: Follow-up tasks or dependencies

## Next Steps
After implementation sessions with `/implement`:
1. **Review progress logs** for completeness and accuracy
2. **Update task status** in the main task document
3. **Share updates** with team members
4. **Address blockers** identified during implementation
5. **Plan next implementation session** based on priorities
6. **Use `/analyze`** to check overall project alignment
7. **Schedule follow-up** for dependent tasks

## Troubleshooting
- **Tasks unclear**: Go back to `/tasks` to add more detail
- **Progress stuck**: Use `/analyze` to identify systemic issues
- **Team coordination**: Share implementation logs regularly
- **Overloaded team members**: Rebalance task assignments
- **Quality concerns**: Add testing and review checkpoints
- **Scope creep**: Reference goals and plans to stay focused

## Integration with Other Commands
Implementation tracking helps:
- **Validate plans** (`/plan`): Ensure plans are realistic and achievable
- **Update tasks** (`/tasks`): Reflect actual progress and adjustments needed
- **Inform analysis** (`/analyze`): Provide real-world progress data
- **Guide goals** (`/goals`): Show what's achievable vs. aspirational
- **Refine strategies** (`/strategize`): Surface what works and what doesn't

## Progress Metrics
The command tracks and reports:
- **Completion rate**: Percentage of tasks finished
- **Velocity**: Tasks completed over time
- **Blocker frequency**: How often tasks get stuck
- **Quality indicators**: Issues found and resolved
- **Team productivity**: Individual and team progress patterns