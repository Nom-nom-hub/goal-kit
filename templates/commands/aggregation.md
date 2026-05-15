---
description: Manage multiple Goal Kit projects in a workspace. Discover projects, aggregate reports, and compare project metrics.
handoffs:
  - label: Status
    agent: goalkit.status
    prompt: Check the health of a specific project before aggregation
    send: false
  - label: Reporting
    agent: goalkit.reporting
    prompt: Generate detailed report for a specific project
    send: false
scripts:
  sh: ""
  ps: ""
---

## User Input

- **Workspace Path**: Directory containing Goal Kit projects (default: current directory)
- **Action**: List projects, aggregated report, compare by metric, or workspace summary

## Outline

### Execution Flow

1. **Discover Projects** (15 min)
   - Scan workspace directory for `.goalkit` subdirectories
   - Load each project's task and metrics data
   - Compile project list with completion rates and health scores

2. **Aggregate & Compare** (15 min)
   - Calculate overall workspace completion rate and health score
   - Rank projects by selected metric (completion_rate, health_score, task_count)
   - Generate cross-project insights (high/low performers, trends)

3. **Generate Reports** (15 min)
   - Create aggregated workspace report with summary statistics
   - Show task distribution across all projects
   - Identify at-risk projects needing attention

### Validation Gate

- [ ] All projects discovered correctly
- [ ] Aggregation metrics calculated accurately
- [ ] Cross-project comparisons are fair (same metrics used)

### Output

- **List view**: Table of all projects with name, tasks, completion %, health score
- **Report view**: Workspace summary with overall metrics and per-project breakdowns
- **Compare view**: Ranked list of projects by chosen metric
