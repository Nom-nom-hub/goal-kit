# Goal Kit Scripts

This directory contains shell and PowerShell scripts for the Goal Kit methodology to complement the main CLI.

## Available Scripts

### Bash Scripts (bash/)
- `common.sh` - Common utilities and helper functions
- `create-new-goal.sh` - Creates a new goal in a Goal Kit project
- `create-vision.sh` - Creates a project vision document
- `setup-strategy.sh` - Sets up strategy analysis for a goal
- `setup-milestones.sh` - Sets up milestone planning for a goal
- `setup-execution.sh` - Sets up execution planning
- `create-tasks.sh` - Creates task lists from strategies
- `create-report.sh` - Generates progress reports
- `create-review.sh` - Creates project review documents
- `update-agent-context.sh` - Updates agent context files with current goal info

### PowerShell Scripts (powershell/)
- `common.ps1` - Common utilities and helper functions
- `create-new-goal.ps1` - Creates a new goal in a Goal Kit project
- `create-vision.ps1` - Creates a project vision document
- `setup-strategy.ps1` - Sets up strategy analysis for a goal
- `setup-milestones.ps1` - Sets up milestone planning for a goal
- `setup-execution.ps1` - Sets up execution planning
- `create-tasks.ps1` - Creates task lists from strategies
- `create-report.ps1` - Generates progress reports
- `create-review.ps1` - Creates project review documents
- `update-agent-context.ps1` - Updates agent context files with current goal info

## Key Features

1. **Project Automation** - Scripts to automate common Goal Kit tasks
2. **Cross-platform Support** - Works on Unix/Linux/Mac (bash) and Windows (PowerShell)
3. **JSON Output** - Scripts output JSON for easy parsing and integration
4. **Goal Management** - Create, update, and manage goals and related artifacts

## Usage

### Creating a New Goal (Bash)
```bash
cd .goalkit
bash scripts/bash/create-new-goal.sh --json "Your goal description"
```

### Creating a New Goal (PowerShell)
```powershell
cd .goalkit
& ".\scripts\powershell\create-new-goal.ps1" -Json "Your goal description"
```

### Creating Vision (Bash)
```bash
bash .goalkit/scripts/bash/create-vision.sh --json
```

### Creating Vision (PowerShell)
```powershell
& ".\.goalkit\scripts\powershell\create-vision.ps1" -Json
```

## Validation Requirements

The goal validation system ensures all goals meet these requirements:
- All required sections are present
- Placeholder content is replaced with actual content
- Success metrics have quantifiable targets
- Users and stakeholders are properly identified
- Testable hypotheses are defined
- Proper structure is maintained

This enhances Goal-Driven Development by ensuring that all goals meet the quality standards needed for effective outcome-focused development.