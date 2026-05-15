---
description: Manage task dependencies, critical path analysis, and dependency graph visualization for project tasks.
handoffs: []
scripts: {}
---

## User Input

```text
$ARGUMENTS
```

## Outline

The `/goalkit.dependencies` command manages task dependencies with several subcommands:

### `goalkit dependencies blocking`
Show tasks that are blocking other work:
- Lists incomplete tasks that have other tasks depending on them
- Shows task ID, title, and number of blocked tasks
- Use `--output json` for machine-readable output

### `goalkit dependencies critical-path`
Show the critical path (longest dependency chain):
- Displays the sequence of tasks that determine minimum project duration
- Shows each task with estimated hours and status
- Total estimated hours for the critical path
- Use `--output json` for machine-readable output

### `goalkit dependencies graph`
Show the dependency graph:
- Displays all task dependencies
- Use `--task TASK_ID` to filter for a specific task
- Shows dependency chains and relationships

### `goalkit dependencies add <task_id> <depends_on>`
Add a dependency between tasks:
- Makes `task_id` depend on `depends_on`
- Validates no circular dependencies are created

### `goalkit dependencies remove <task_id>`
Remove the dependency from a task.

## When to Use

- **Planning phase**: Understand task ordering requirements
- **Before execution**: Identify blocking tasks to prioritize
- **Status checks**: Find what's blocking progress
- **Schedule estimation**: Critical path analysis for timeline
