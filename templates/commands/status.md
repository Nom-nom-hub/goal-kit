---
description: Display project status, health score, completion percentage, goal progress, and milestone tracking for the Goalkit project.
handoffs: []
scripts: {}
---

## User Input

```text
$ARGUMENTS
```

## Outline

The `/goalkit.status` command shows a comprehensive overview of the current project state.

1. **Display project overview**:
   - Project name and AI assistant type
   - Current phase (setup, active, execution, complete)
   - Overall completion percentage with color coding
   - Health score (0-100) with color coding
   - Insights, concerns, and strengths

2. **List active goals** with:
   - Goal name
   - Phase
   - Progress percentage
   - Success criteria count
   - Metrics defined indicator

3. **Show milestone summary**:
   - Completed vs total milestones
   - Overall milestone progress

4. **Verbose mode** (`--verbose`/`-v`):
   - Health score breakdown (completion, metrics, criteria, phase progress)
   - Project metadata (path, agent, created date)

5. **JSON mode** (`--json`):
   - All data in structured JSON format for programmatic use

## When to Use

- **Daily check**: Quick status overview during active work
- **Before decision points**: Review health before pivoting
- **Stakeholder updates**: Share project health metrics
- **After milestones**: Verify progress is reflected correctly

## Options

- `--verbose`, `-v`: Show detailed analysis and health score breakdown
- `--json`: Output results as JSON for programmatic processing
- `[project_path]`: Path to goal-kit project (defaults to current directory)
