# Goal Kit Scripts

This directory contains scripts for the Goal Kit methodology to complement the main CLI.

## Bash Scripts

- `check-prerequisites.sh` - Checks if required tools are installed
- `common.sh` - Common utilities for other scripts
- `create-new-goal.sh` - Creates a new goal in a Goal Kit project
- `setup-goal.sh` - Sets up the environment for a specific goal
- `update-agent-context.sh` - Updates agent context files with current goal info

- `validate_goals.py` - Goal validation script that checks for:
  - Required sections in goal files
  - Filled-out elements (not just placeholders)
  - Measurable success metrics
  - Proper structure and content

## PowerShell Scripts

- `check-prerequisites.ps1` - Checks if required tools are installed (PowerShell version)
- `common.ps1` - Common utilities for other scripts (PowerShell version)
- `create-new-goal.ps1` - Creates a new goal in a Goal Kit project (PowerShell version)
- `setup-goal.ps1` - Sets up the environment for a specific goal (PowerShell version)
- `update-agent-context.ps1` - Updates agent context files with current goal info (PowerShell version)

## Key Features

1. **Project Automation** - Scripts to automate common Goal Kit tasks
2. **Environment Setup** - Tools to configure the development environment
3. **Validation** - Goal validation system for quality assurance

## Usage

The main CLI now includes enhanced UX features that supersede some script functionality:

### Creating a New Goal
```bash
# Enhanced version with progress indicators (main CLI)
goalkeeper create-goal "Improve user authentication flow"

# Interactive mode
goalkeeper create-goal --interactive "Goal description"

# Dry run to see what would be created
goalkeeper create-goal --dry-run "Add payment system"

# Validate after creation
goalkeeper validate-goal goals/001-improve-user-authentication/goal.md
```

### For legacy script usage (if needed):
```bash
# Using bash script directly
./create-new-goal.sh "Standard goal creation"

# Using PowerShell script directly
.\create-new-goal.ps1 -GoalDescription "Standard goal creation"
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