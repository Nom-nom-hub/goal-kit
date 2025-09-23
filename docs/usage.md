# Usage

## Quick Start

```bash
# Initialize a new project
goal init my-project

# Create your first goal
cd my-project
goal create "Implement user authentication"

# List your goals
goal list

# View details of a specific goal
goal show <goal-id>

# Track progress
goal track
```

## Project Initialization

```bash
# Create a new project
goal init my-awesome-project

# Initialize in current directory
goal init --here

# Skip git initialization
goal init my-project --no-git

# Force creation even if directory exists
goal init my-project --force
```

## Goal Management

```bash
# Create a goal
goal create "Implement feature X with requirements Y and Z"

# List all goals
goal list

# View goal details
goal show <goal-id>

# Create an implementation plan
goal plan <goal-id>

# Generate tasks for a plan
goal tasks <plan-id>

# Track project progress
goal track
```

## Advanced Features

Goal-Dev-Spec includes many advanced features:

- **AI Integration**: Automatically select and use AI assistants during initialization
- **Analytics**: Get predictive analytics for your goals
- **Governance**: Enforce project standards and compliance
- **Automation**: Create and run automated workflows
- **Cross-platform Scripts**: Generate both bash and PowerShell scripts