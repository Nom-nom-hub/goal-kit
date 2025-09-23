# Commands Reference

## `goal init`

Initialize a new goal-dev-spec project with advanced features.

```bash
goal init [OPTIONS] [PROJECT_NAME]
```

Options:
- `--ai TEXT`: AI assistant to use (claude, gemini, copilot, cursor, qwen, opencode, codex, windsurf, kilocode, or auggie)
- `--script TEXT`: Script type to use (sh or ps)
- `--no-git`: Skip git repository initialization
- `--force`: Force creation even if directory exists
- `--here`: Initialize project in the current directory instead of creating a new one

## `goal create`

Create a new goal specification with predictive analytics.

```bash
goal create [OPTIONS] GOAL_DESCRIPTION
```

Creates a new goal with the specified description and automatically generates a corresponding feature specification.

## `goal plan`

Create an implementation plan for a goal.

```bash
goal plan [OPTIONS] GOAL_ID
```

Generates an implementation plan for the specified goal, including tasks, timeline, and resource requirements.

## `goal tasks`

Generate task breakdown for implementation.

```bash
goal tasks [OPTIONS] PLAN_ID
```

Breaks down an implementation plan into actionable tasks with assignees, due dates, and dependencies.

## `goal list`

List all goals in the project.

```bash
goal list [OPTIONS]
```

Displays all goals in the current project with their status and creation dates.

## `goal show`

Show details of a specific goal.

```bash
goal show [OPTIONS] GOAL_ID
```

Displays detailed information about a specific goal, including objectives, success criteria, and dependencies.

## `goal track`

Track progress of goals and tasks with enhanced analytics.

```bash
goal track [OPTIONS]
```

Shows progress tracking information for all goals and tasks in the project.

## `goal governance`

Manage project governance, compliance, and quality assurance.

```bash
goal governance [OPTIONS] ACTION
```

Actions: init, report, validate, compliance, security, quality, performance, reviews, version