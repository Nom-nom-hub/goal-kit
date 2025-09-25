# Goal-Kit

**Goal-Driven Development Toolkit - Transform Ideas into Achievements**

Goal-Kit is a comprehensive CLI tool that transforms spec-kit's proven patterns into goal-driven development. It provides a structured approach to goal management, milestone planning, and achievement tracking.

## Features

- 🎯 **Goal Management**: Define and track goals with natural language descriptions
- 📊 **Progress Tracking**: Visual progress dashboards with milestone completion
- 🏆 **Achievement System**: Track accomplishments and celebrate wins
- 📅 **Milestone Planning**: Break down goals into manageable milestones
- 🎨 **Rich Terminal UI**: Beautiful, informative command-line interface
- 📁 **Project Organization**: Structured directory layout for goal projects
- 📋 **Completion Reports**: Generate detailed completion summaries

## Installation

### Using uv (Recommended)

```bash
# Install as a tool
uv tool install --from goal-kit

# Or install from the current directory during development
uv tool install --from .
```

### Using pip

```bash
# Install from PyPI (when available)
pip install goal-kit

# Or install from local directory
pip install -e .
```

## Quick Start

### 1. Initialize a Goal Project

```bash
# Create a new goal project
goal-kit init "Build a web application"

# Or initialize in current directory
goal-kit init --here
```

### 2. Define Your Goal

```bash
# Define your goal with natural language
goal-kit define "Build a full-stack web application with user authentication"

# Add priority and deadline
goal-kit define "Launch startup MVP" --priority critical --deadline 2024-12-31
```

### 3. Plan Milestones

```bash
# Create milestones interactively
goal-kit milestone --add

# Or create specific milestones
goal-kit milestone --name "Setup project structure" --desc "Create basic directory structure"
goal-kit milestone --name "Implement authentication" --desc "Build user login and registration"
```

### 4. Track Progress

```bash
# View progress dashboard
goal-kit progress

# List all milestones
goal-kit milestone --list
```

### 5. Record Achievements

```bash
# Add achievements interactively
goal-kit achieve --add

# Or add to specific milestone
goal-kit achieve --milestone 1 --desc "Completed user authentication system"
```

### 6. Complete Your Goal

```bash
# Mark goal as completed
goal-kit complete
```

## Commands

### `goal-kit init`

Initialize a new goal project directory structure.

**Options:**

- `--here`: Initialize in current directory
- `--force`: Force overwrite when using `--here`

### `goal-kit define`

Define a goal with natural language description.

**Options:**

- `--priority`: Set priority (low, medium, high, critical)
- `--deadline`: Set deadline (YYYY-MM-DD format)
- `--category`: Set category for organization

### `goal-kit milestone`

Manage goal milestones.

**Options:**

- `--add`: Add a new milestone interactively
- `--list`: List all milestones
- `--name`: Milestone name
- `--desc`: Milestone description

### `goal-kit achieve`

Track goal achievements.

**Options:**

- `--add`: Add a new achievement interactively
- `--milestone`: Milestone ID to add achievement to
- `--desc`: Achievement description

### `goal-kit progress`

Show goal progress dashboard with metrics and insights.

### `goal-kit complete`

Mark goal as completed and generate completion report.

## Project Structure

```
goal-project/
├── goal.json              # Goal configuration and metadata
├── milestones/            # Milestone tracking files
│   ├── README.md
│   ├── 01-setup-project.md
│   └── 02-implement-auth.md
├── achievements/          # Achievement tracking files
│   ├── README.md
│   └── achievement-001.md
├── templates/             # Goal-specific templates
└── completion-report.md   # Generated completion report
```

## Goal States

Goals progress through these states:

1. **Defined**: Goal has been created and described
2. **In Progress**: Active work is being done
3. **Completed**: Goal has been successfully finished
4. **On Hold**: Temporarily paused
5. **Cancelled**: No longer being pursued

## Examples

### Example Goal: "Write a Book"

```bash
# Initialize
goal-kit init "Write a Book"

# Define with details
goal-kit define "Write and publish a 50,000-word technical book on Python" \
  --priority high \
  --deadline 2024-06-01 \
  --category "writing"

# Add milestones
goal-kit milestone --add  # Outline chapters
goal-kit milestone --add  # Write first draft
goal-kit milestone --add  # Edit and revise
goal-kit milestone --add  # Design cover
goal-kit milestone --add  # Format and publish

# Track achievements
goal-kit achieve --milestone 1 --desc "Completed chapter outlines"
goal-kit achieve --milestone 2 --desc "Finished first draft of chapters 1-3"

# Monitor progress
goal-kit progress

# Complete the goal
goal-kit complete
```

## Contributing

Goal-Kit is built on spec-kit's proven patterns and follows similar architectural principles:

- **CLI Framework**: Uses Typer for command-line interface
- **UI Components**: Rich terminal UI for beautiful output
- **Progress Tracking**: StepTracker for hierarchical progress display
- **Project Structure**: Consistent directory organization

## License

This project follows the same license as spec-kit.

## Related Tools

- **spec-kit**: The foundation CLI tool that inspired Goal-Kit
- **Specify CLI**: Spec-driven development toolkit
- **Rich**: Python library for rich text and beautiful formatting in the terminal
- **Typer**: Python library for building powerful CLIs

---

_Goal-Kit - Because every great achievement starts with a clear goal and a structured plan._
