# Goal Kit Scripts

These scripts are called **internally by your AI agent** when you use `/goalkit.*` commands. They create and update markdown files in the `.goalkit/` directory.

You normally don't need to run these directly — just tell your agent what you want.

## Available Scripts

### Bash Scripts (bash/)
- `common.sh` — Common utilities and helper functions
- `create-new-goal.sh` — Creates a new goal in a Goal Kit project
- `create-vision.sh` — Creates a project vision document
- `setup-strategy.sh` — Sets up strategy analysis for a goal
- `setup-milestones.sh` — Sets up milestone planning for a goal
- `setup-execution.sh` — Sets up execution planning
- `create-tasks.sh` — Creates task lists from strategies
- `create-report.sh` — Generates progress reports
- `create-review.sh` — Creates project review documents
- `update-agent-context.sh` — Updates agent context files with current goal info

### PowerShell Scripts (powershell/)
- `common.ps1` — Common utilities and helper functions
- `create-new-goal.ps1` — Creates a new goal in a Goal Kit project
- `create-vision.ps1` — Creates a project vision document
- `setup-strategy.ps1` — Sets up strategy analysis for a goal
- `setup-milestones.ps1` — Sets up milestone planning for a goal
- `setup-execution.ps1` — Sets up execution planning
- `create-tasks.ps1` — Creates task lists from strategies
- `create-report.ps1` — Generates progress reports
- `create-review.ps1` — Creates project review documents
- `update-agent-context.ps1` — Updates agent context files with current goal info

## How Agents Use These Scripts

When you tell your agent `/goalkit.goal`, it runs the corresponding script internally. You don't need to call the script yourself.

Scripts output JSON for agent parsing. For example:

```json
{ "status": "success", "goal_path": ".goalkit/goals/001-user-auth/goal.md" }
```

## Agent Mapping

| Slash Command | Script Called |
|---------------|---------------|
| `/goalkit.vision` | `create-vision.sh` / `create-vision.ps1` |
| `/goalkit.goal` | `create-new-goal.sh` / `create-new-goal.ps1` |
| `/goalkit.strategies` | `setup-strategy.sh` / `setup-strategy.ps1` |
| `/goalkit.milestones` | `setup-milestones.sh` / `setup-milestones.ps1` |
| `/goalkit.execute` | `setup-execution.sh` / `setup-execution.ps1` |
| `/goalkit.tasks` | `create-tasks.sh` / `create-tasks.ps1` |
| `/goalkit.report` | `create-report.sh` / `create-report.ps1` |
| `/goalkit.review` | `create-review.sh` / `create-review.ps1` |

## Running Scripts Directly (Troubleshooting)

If your agent can't run scripts, you can run them manually as a fallback:

```bash
# From project root
bash .goalkit/scripts/bash/create-new-goal.sh --json "Your goal description"
```

PowerShell:
```powershell
& ".\goalkit\scripts\powershell\create-new-goal.ps1" -Json "Your goal description"
```

## Key Features

1. **Project Automation** — Scripts to automate common Goal Kit tasks
2. **Cross-platform Support** — Works on Unix/Linux/Mac (bash) and Windows (PowerShell)
3. **JSON Output** — Scripts output JSON for easy parsing by AI agents
4. **Goal Management** — Create, update, and manage goals and related artifacts
