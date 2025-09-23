# Goal-Dev-Spec CLI Reference

This document provides a comprehensive reference for all CLI commands available in the Goal-Dev-Spec system, including detailed usage information, options, and examples.

## Overview

The Goal-Dev-Spec CLI provides a complete set of tools for managing goal-driven development projects. It includes commands for project initialization, goal creation, planning, task management, progress tracking, and advanced features like governance, analytics, and AI integration.

## Installation

Before using the CLI, install the package:

```bash
pip install -e .
```

Or run directly without installation:

```bash
python -m goal_cli
```

## Global Options

All commands support these global options:

- `--version` or `-v`: Show the version and exit
- `--help` or `-h`: Show help message and exit

## Commands

### `goal init` - Initialize a New Project

Initialize a new Goal-Dev-Spec project with advanced features.

#### Usage

```bash
goal init [OPTIONS] [PROJECT_NAME]
```

#### Options

- `--ai TEXT`: AI assistant to use (claude, gemini, copilot, cursor, qwen, opencode, codex, windsurf, kilocode, or auggie)
- `--script TEXT`: Script type to use (sh or ps)
- `--no-git`: Skip git repository initialization
- `--force` or `-f`: Force creation even if directory exists
- `--here`: Initialize project in the current directory instead of creating a new one

#### Examples

```bash
# Create a new project with interactive AI selection
goal init my-project

# Create a project with a specific AI assistant
goal init my-project --ai claude

# Initialize in the current directory
goal init --here

# Skip git initialization
goal init my-project --no-git
```

#### Features

- Interactive AI assistant selection
- Cross-platform script type selection
- Enhanced progress tracking with ETA
- Real-time notifications
- Template file creation
- Git repository initialization
- Security notifications for AI agent folders

### `goal create` - Create a New Goal

Create a new goal specification with predictive analytics.

#### Usage

```bash
goal create [OPTIONS] GOAL_DESCRIPTION
```

#### Arguments

- `GOAL_DESCRIPTION`: Description of the goal to create. This should be a clear, concise statement of what you want to accomplish.

#### Examples

```bash
# Create a goal with a descriptive title
goal create "Implement user authentication system with login, registration, and password reset"

# Create a goal for API development
goal create "Develop RESTful API for user management with CRUD operations"
```

#### Features

- Automatic goal ID generation
- Predictive analytics for complexity analysis
- Estimated completion time calculation
- Risk factor identification
- Automatic feature specification creation
- Enhanced goal specification with metadata

### `goal plan` - Create Implementation Plan

Create an implementation plan for a goal.

#### Usage

```bash
goal plan [OPTIONS] GOAL_ID
```

#### Arguments

- `GOAL_ID`: ID of the goal to create a plan for. You can find goal IDs using `goal list`.

#### Examples

```bash
# Create a plan for a specific goal
goal plan goal-abc123

# Create a plan with custom timeline
goal plan goal-xyz789
```

### `goal tasks` - Generate Task Breakdown

Generate task breakdown for implementation.

#### Usage

```bash
goal tasks [OPTIONS] PLAN_ID
```

#### Arguments

- `PLAN_ID`: ID of the plan to generate tasks for. You can find plan IDs in the plans directory.

#### Examples

```bash
# Generate tasks for a specific plan
goal tasks plan-def456

# Generate tasks with custom priority
goal tasks plan-ghi789
```

### `goal list` - List All Goals

List all goals in the project.

#### Usage

```bash
goal list [OPTIONS]
```

#### Examples

```bash
# List all goals in the current project
goal list
```

#### Output

Displays a table with:
- Goal ID
- Title
- Creation date

### `goal show` - Show Goal Details

Show details of a specific goal.

#### Usage

```bash
goal show [OPTIONS] GOAL_ID
```

#### Arguments

- `GOAL_ID`: ID of the goal to show. You can find goal IDs using `goal list`.

#### Examples

```bash
# Show details of a specific goal
goal show goal-abc123
```

#### Output

Displays detailed information:
- Goal title
- Status and priority
- Full description
- Objectives
- Dependencies

### `goal track` - Track Progress

Track progress of goals and tasks with enhanced analytics.

#### Usage

```bash
goal track [OPTIONS]
```

#### Examples

```bash
# Track project progress
goal track
```

#### Features

- Overall project progress with completion percentage
- Goal completion status with complexity analysis
- Risk factor aggregation
- Detailed progress visualization
- Estimated completion times

### `goal governance` - Manage Governance

Manage project governance, compliance, and quality assurance.

#### Usage

```bash
goal governance [OPTIONS] ACTION
```

#### Arguments

- `ACTION`: Action to perform (init, report, validate, compliance, security, quality, performance, reviews, version)

#### Options

- `--type` or `-t`: Type of artifact for validation
- `--id` or `-i`: ID of artifact for validation

#### Examples

```bash
# Initialize project constitution
goal governance init

# Generate comprehensive governance report
goal governance report

# Validate a specific goal
goal governance validate --type goal --id goal-abc123

# Check compliance with standards
goal governance compliance

# Scan for security vulnerabilities
goal governance security
```

### `goal analytics` - Predictive Analytics

Access predictive analytics features.

#### Usage

```bash
goal analytics [OPTIONS] COMMAND
```

#### Commands

- `analyze-goal GOAL_ID`: Analyze a specific goal with predictive analytics
- `project-insights`: Get insights about the entire project
- `risk-assessment`: Perform comprehensive risk assessment
- `resource-planning`: Get resource allocation recommendations

#### Examples

```bash
# Analyze a specific goal
goal analytics analyze-goal goal-abc123

# Get project-wide insights
goal analytics project-insights

# Perform risk assessment
goal analytics risk-assessment
```

### `goal quality` - Quality Assurance

Manage quality assurance features.

#### Usage

```bash
goal quality [OPTIONS] COMMAND
```

#### Commands

- `validate-artifact TYPE ID`: Validate a specific artifact
- `run-checks`: Run all quality checks
- `generate-report`: Generate quality assurance report
- `set-thresholds`: Set quality thresholds

#### Examples

```bash
# Validate a goal
goal quality validate-artifact goal goal-abc123

# Run all quality checks
goal quality run-checks

# Generate quality report
goal quality generate-report
```

### `goal test` - Testing Integration

Manage testing integration features.

#### Usage

```bash
goal test [OPTIONS] COMMAND
```

#### Commands

- `generate-plan`: Generate test plan for a goal
- `run-tests`: Run tests for the project
- `coverage-report`: Generate test coverage report
- `integration-status`: Check testing integration status

#### Examples

```bash
# Generate test plan for a goal
goal test generate-plan goal-abc123

# Run all tests
goal test run-tests

# Generate coverage report
goal test coverage-report
```

### `goal monitor` - Real-time Monitoring

Monitor project progress and performance.

#### Usage

```bash
goal monitor [OPTIONS] COMMAND
```

#### Commands

- `live-dashboard`: Start live monitoring dashboard
- `performance-metrics`: Show performance metrics
- `alert-history`: Show alert history
- `set-thresholds`: Set monitoring thresholds

#### Examples

```bash
# Start live monitoring dashboard
goal monitor live-dashboard

# Show performance metrics
goal monitor performance-metrics

# Show alert history
goal monitor alert-history
```

### `goal automate` - Automation Features

Manage automation workflows.

#### Usage

```bash
goal automate [OPTIONS] COMMAND
```

#### Commands

- `setup-workflow`: Set up automation workflow
- `run-workflow`: Run a specific workflow
- `schedule-task`: Schedule an automated task
- `workflow-status`: Check workflow status

#### Examples

```bash
# Set up a deployment workflow
goal automate setup-workflow deployment

# Run a specific workflow
goal automate run-workflow ci-cd

# Schedule a task
goal automate schedule-task "0 2 * * *" backup-project

# Check workflow status
goal automate workflow-status
```

### `goal script` - Cross-Platform Scripting

Manage cross-platform scripts.

#### Usage

```bash
goal script [OPTIONS] COMMAND
```

#### Commands

- `create`: Create a new cross-platform script
- `run`: Run a specific script
- `list`: List available scripts
- `validate`: Validate script compatibility

#### Examples

```bash
# Create a new script
goal script create setup-environment

# Run a specific script
goal script run build-project

# List all scripts
goal script list

# Validate script compatibility
goal script validate deploy.sh
```

### `goal code` - AI Code Generation

Generate code using AI assistants.

#### Usage

```bash
goal code [OPTIONS] COMMAND
```

#### Commands

- `generate`: Generate code for a specification
- `review`: Review existing code
- `refactor`: Refactor code with AI assistance
- `explain`: Explain code functionality

#### Examples

```bash
# Generate code for a specification
goal code generate spec-def456

# Review existing code
goal code review src/main.py

# Refactor code
goal code refactor src/legacy.py

# Explain code
goal code explain src/complex-algorithm.py
```

### `goal docs` - Documentation Generation

Generate project documentation.

#### Usage

```bash
goal docs [OPTIONS] COMMAND
```

#### Commands

- `generate`: Generate documentation for the project
- `update`: Update existing documentation
- `validate`: Validate documentation quality
- `publish`: Publish documentation

#### Examples

```bash
# Generate project documentation
goal docs generate

# Update existing documentation
goal docs update

# Validate documentation quality
goal docs validate

# Publish documentation
goal docs publish
```

### `goal cicd` - CI/CD Integration

Manage CI/CD pipeline integration.

#### Usage

```bash
goal cicd [OPTIONS] COMMAND
```

#### Commands

- `setup-pipeline`: Set up CI/CD pipeline
- `run-pipeline`: Run CI/CD pipeline
- `pipeline-status`: Check pipeline status
- `configure`: Configure pipeline settings

#### Examples

```bash
# Set up CI/CD pipeline
goal cicd setup-pipeline

# Run CI/CD pipeline
goal cicd run-pipeline

# Check pipeline status
goal cicd pipeline-status

# Configure pipeline settings
goal cicd configure
```

### `goal deps` - Dependency Management

Manage project dependencies.

#### Usage

```bash
goal deps [OPTIONS] COMMAND
```

#### Commands

- `analyze`: Analyze project dependencies
- `update`: Update dependencies
- `audit`: Audit dependencies for vulnerabilities
- `lock`: Generate dependency lock file

#### Examples

```bash
# Analyze project dependencies
goal deps analyze

# Update dependencies
goal deps update

# Audit dependencies for vulnerabilities
goal deps audit

# Generate dependency lock file
goal deps lock
```

### `goal scaffold` - Project Scaffolding

Generate project scaffolding.

#### Usage

```bash
goal scaffold [OPTIONS] COMMAND
```

#### Commands

- `project`: Scaffold a new project
- `component`: Scaffold a new component
- `module`: Scaffold a new module
- `template`: Scaffold from a template

#### Examples

```bash
# Scaffold a new project
goal scaffold project web-application

# Scaffold a new component
goal scaffold component user-authentication

# Scaffold a new module
goal scaffold module reporting

# Scaffold from a template
goal scaffold template api-service
```

### `goal perf` - Performance Optimization

Manage performance optimization features.

#### Usage

```bash
goal perf [OPTIONS] COMMAND
```

#### Commands

- `analyze`: Analyze performance bottlenecks
- `optimize`: Optimize project performance
- `benchmark`: Run performance benchmarks
- `report`: Generate performance report

#### Examples

```bash
# Analyze performance bottlenecks
goal perf analyze

# Optimize project performance
goal perf optimize

# Run performance benchmarks
goal perf benchmark

# Generate performance report
goal perf report
```

### `goal secure` - Security Scanning

Perform security scanning and vulnerability assessment.

#### Usage

```bash
goal secure [OPTIONS] COMMAND
```

#### Commands

- `scan`: Scan for security vulnerabilities
- `audit`: Perform security audit
- `report`: Generate security report
- `fix`: Apply security fixes

#### Examples

```bash
# Scan for security vulnerabilities
goal secure scan

# Perform security audit
goal secure audit

# Generate security report
goal secure report

# Apply security fixes
goal secure fix
```

## Environment Variables

The CLI supports several environment variables for configuration:

- `GOAL_AI_AGENT`: Default AI agent to use
- `GOAL_SCRIPT_TYPE`: Default script type (sh or ps)
- `GOAL_DISABLE_ANALYTICS`: Disable predictive analytics features
- `GOAL_DISABLE_GIT`: Disable automatic git initialization

## Configuration Files

The CLI uses several configuration files:

- `goal.yaml`: Main project configuration file
- `.goal/config/project.yaml`: Project-level configuration
- `.goal/config/agents.yaml`: AI agent configurations
- `.goal/config/teams.yaml`: Team structure and permissions

## Exit Codes

The CLI uses standard exit codes:

- `0`: Success
- `1`: General error
- `2`: Invalid usage or arguments
- `3`: Configuration error
- `4`: File or directory error
- `5`: Network or API error

## Examples

### Complete Project Workflow

```bash
# Initialize a new project
goal init my-web-app --ai claude

# Navigate to the project directory
cd my-web-app

# Create a goal for user authentication
goal create "Implement user authentication system with login, registration, and password reset"

# List goals to get the ID
goal list

# Create an implementation plan
goal plan goal-abc123

# Generate tasks
goal tasks plan-def456

# Track progress
goal track

# Generate documentation
goal docs generate
```

### Governance Workflow

```bash
# Initialize project constitution
goal governance init

# Validate a goal
goal governance validate --type goal --id goal-abc123

# Check compliance
goal governance compliance

# Scan for security issues
goal governance security

# Generate governance report
goal governance report
```

### Analytics Workflow

```bash
# Analyze a specific goal
goal analytics analyze-goal goal-abc123

# Get project insights
goal analytics project-insights

# Perform risk assessment
goal analytics risk-assessment

# Get resource planning recommendations
goal analytics resource-planning
```

## Best Practices

1. **Start with clear goals**: Use descriptive goal descriptions that clearly state what you want to accomplish.

2. **Use predictive analytics**: Leverage the built-in analytics to understand project complexity and timelines.

3. **Track progress regularly**: Use the `track` command to monitor project progress and identify potential issues early.

4. **Leverage AI integration**: Use the AI code generation features to accelerate development.

5. **Maintain governance**: Regularly validate artifacts and check compliance to ensure project quality.

6. **Automate workflows**: Set up automation workflows to reduce manual tasks and improve consistency.

7. **Document everything**: Use the documentation generation features to maintain comprehensive project documentation.

## Troubleshooting

### Common Issues

1. **"Not in a goal-dev-spec project directory"**: Run `goal init` first to create a project.

2. **"Goal with ID not found"**: Use `goal list` to see available goal IDs.

3. **AI assistant not found**: Install the required AI assistant tool or choose a different assistant.

4. **Permission errors**: Ensure you have write permissions in the project directory.

### Getting Help

For additional help, use:
- `goal --help` for general help
- `goal <command> --help` for command-specific help
- Check the documentation files in the `docs/` directory