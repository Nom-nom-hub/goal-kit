# Goal Kit Scripts

This directory contains Python scripts for the Goal Kit methodology to complement the main CLI.

## Python Scripts

- `check-prerequisites.py` - Checks if required tools are installed
- `common.py` - Common utilities for other scripts
- `create_new_goal.py` - Creates a new goal in a Goal Kit project
- `setup_goal.py` - Sets up the environment for a specific goal
- `setup_milestones.py` - Sets up milestone planning in a Goal Kit project
- `setup_strategy.py` - Sets up strategy analysis in a Goal Kit project
- `setup_collaboration.py` - Sets up collaboration planning in a Goal Kit project
- `manage_personas.py` - Manages agent personas in a Goal Kit project
- `update_agent_context.py` - Updates agent context files with current goal info
- `validate_methodology.py` - Validates methodology completion for goals
- `validate_goals.py` - Goal validation script that checks for:
  - Required sections in goal files
  - Filled-out elements (not just placeholders)
  - Measurable success metrics
  - Proper structure and content

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

### For direct script usage:
```bash
# Using Python script directly
python scripts/python/create_new_goal.py "Standard goal creation"

# Or on some systems
python3 scripts/python/create_new_goal.py "Standard goal creation"
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