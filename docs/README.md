# Goal-Dev-Spec Documentation

## Overview

Goal-Dev-Spec is a goal-driven development specification system that uses YAML files for structured specifications. It provides a systematic approach to defining goals, creating specifications, planning implementations, and tracking progress.

## Key Concepts

### Goals
Goals represent high-level objectives that you want to achieve. Each goal has:
- A unique ID
- A descriptive title
- A detailed description
- Objectives to achieve
- Success criteria
- Dependencies on other goals
- Priority and status tracking

### Specifications
Specifications define the detailed requirements for implementing a goal. Each specification includes:
- User stories
- Acceptance criteria
- Functional and non-functional requirements
- Constraints and assumptions

### Plans
Plans outline the technical approach for implementing a specification:
- Technical approach
- Architecture design
- Integration points
- Deployment strategy

### Tasks
Tasks break down plans into actionable items:
- Individual task definitions
- Dependencies between tasks
- Estimated durations
- Assignees

## Installation

```bash
pip install goal-dev-spec
```

## Quick Start

1. Initialize a new project:
   ```bash
   goal init my-project
   cd my-project
   ```

2. Create your first goal:
   ```bash
   goal create "Implement user authentication system"
   ```

3. List all goals:
   ```bash
   goal list
   ```

4. Show details of a specific goal:
   ```bash
   goal show <goal-id>
   ```

## Commands

### `goal init`
Initialize a new goal-dev-spec project.

```bash
goal init <project-name> [--force]
```

Options:
- `--force`: Force creation even if directory exists

### `goal create`
Create a new goal specification.

```bash
goal create "<goal-description>"
```

### `goal plan`
Create an implementation plan for a goal.

```bash
goal plan <goal-id>
```

### `goal tasks`
Generate task breakdown for implementation.

```bash
goal tasks <plan-id>
```

### `goal list`
List all goals in the project.

```bash
goal list
```

### `goal show`
Show details of a specific goal.

```bash
goal show <goal-id>
```

### `goal track`
Track progress of goals and tasks.

```bash
goal track
```

## Project Structure

```
my-project/
├── goal.yaml              # Project configuration
├── .goal/                 # All goal-dev-spec files in one place
│   ├── goals/             # Goal specifications
│   │   ├── goals.yaml     # Goals index
│   │   └── <goal-id>/     # Individual goal directory
│   │       └── goal.yaml  # Goal specification
│   ├── specs/             # Feature specifications
│   │   └── <spec-id>/     # Individual spec directory
│   │       └── spec.yaml  # Feature specification
│   ├── plans/             # Implementation plans
│   ├── tasks/             # Task breakdowns
│   ├── templates/         # YAML templates
│   └── agents/            # AI agent configurations
│       ├── claude/        # Claude configurations
│       └── gemini/        # Gemini configurations
├── scripts/               # Helper scripts
│   ├── bash/              # Bash scripts
│   └── powershell/        # PowerShell scripts
```

## YAML Templates

### Goal Template
```yaml
id: ""
title: ""
description: ""
objectives: []
success_criteria: []
dependencies: []
related_goals: []
priority: "medium"  # low, medium, high, critical
status: "draft"  # draft, planned, in_progress, completed, blocked
created_at: ""
updated_at: ""
owner: ""
tags: []
metadata: {}
```

### Specification Template
```yaml
id: ""
goal_id: ""
title: ""
description: ""
user_stories: []
acceptance_criteria: []
functional_requirements: []
non_functional_requirements: []
constraints: []
assumptions: []
out_of_scope: []
created_at: ""
updated_at: ""
status: "draft"  # draft, reviewed, approved, implemented
metadata: {}
```

## Integration with AI Agents

Goal-Dev-Spec supports integration with various AI agents:
- Claude Code
- Gemini CLI
- Qwen Code
- And more

Agent configurations are stored in the `agents/` directory, with each agent having its own subdirectory containing configuration files and command templates.

## Best Practices

1. **Start with clear goals**: Define specific, measurable goals with clear success criteria.

2. **Break down complex goals**: Use dependencies to create a hierarchy of related goals.

3. **Detailed specifications**: Create comprehensive specifications before implementation.

4. **Regular tracking**: Use the tracking features to monitor progress and identify blockers.

5. **Leverage AI agents**: Use AI agents to help generate and refine specifications.

## Contributing

We welcome contributions to Goal-Dev-Spec! Please see our contributing guidelines for more information.