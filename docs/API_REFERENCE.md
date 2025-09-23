# Goal-Dev-Spec API Documentation

This document provides comprehensive API documentation for developers who want to extend the Goal-Dev-Spec tool with custom functionality, integrations, or plugins.

## Overview

The Goal-Dev-Spec API provides a set of Python classes, functions, and interfaces that allow developers to extend the tool's functionality. The API is organized into modules that correspond to the tool's core features.

## Core Modules

### goal_cli Package Structure

```
goal_cli/
├── __init__.py
├── __main__.py
├── goals.py
├── specs.py
├── plans.py
├── tasks.py
├── ui_components.py
├── analytics.py
├── governance.py
├── quality.py
├── testing.py
├── monitoring.py
├── automation.py
├── cicd.py
├── dependencies.py
├── documentation.py
├── performance.py
├── security.py
└── agents.py
```

## Goal Management API

### GoalManager Class

The `GoalManager` class provides methods for managing goals.

#### Import

```python
from goal_cli.goals import GoalManager
```

#### Constructor

```python
goal_manager = GoalManager(project_path: Path)
```

**Parameters:**
- `project_path` (Path): The path to the project directory

#### Methods

##### create_goal

Create a new goal with the specified description.

```python
goal_id = goal_manager.create_goal(description: str) -> str
```

**Parameters:**
- `description` (str): The description of the goal

**Returns:**
- `str`: The ID of the created goal

**Example:**
```python
goal_manager = GoalManager(Path("/path/to/project"))
goal_id = goal_manager.create_goal("Implement user authentication system")
print(f"Created goal with ID: {goal_id}")
```

##### create_goal_from_data

Create a new goal from structured data.

```python
goal_id = goal_manager.create_goal_from_data(goal_data: dict) -> str
```

**Parameters:**
- `goal_data` (dict): The goal data in dictionary format

**Returns:**
- `str`: The ID of the created goal

**Example:**
```python
goal_data = {
    "title": "User Authentication",
    "description": "Implement user authentication system",
    "objectives": ["Register users", "Authenticate users", "Reset passwords"],
    "priority": "high"
}
goal_id = goal_manager.create_goal_from_data(goal_data)
```

##### get_goal

Retrieve a goal by its ID.

```python
goal = goal_manager.get_goal(goal_id: str) -> dict
```

**Parameters:**
- `goal_id` (str): The ID of the goal to retrieve

**Returns:**
- `dict`: The goal data, or None if not found

**Example:**
```python
goal = goal_manager.get_goal("goal-abc123")
if goal:
    print(f"Goal title: {goal['title']}")
```

##### list_goals

List all goals in the project.

```python
goals = goal_manager.list_goals() -> list
```

**Returns:**
- `list`: A list of goal dictionaries with basic information

**Example:**
```python
goals = goal_manager.list_goals()
for goal in goals:
    print(f"ID: {goal['id']}, Title: {goal['title']}")
```

##### update_goal

Update an existing goal.

```python
success = goal_manager.update_goal(goal_id: str, updates: dict) -> bool
```

**Parameters:**
- `goal_id` (str): The ID of the goal to update
- `updates` (dict): The updates to apply to the goal

**Returns:**
- `bool`: True if the update was successful, False otherwise

**Example:**
```python
updates = {"status": "in_progress", "priority": "critical"}
success = goal_manager.update_goal("goal-abc123", updates)
```

##### delete_goal

Delete a goal by its ID.

```python
success = goal_manager.delete_goal(goal_id: str) -> bool
```

**Parameters:**
- `goal_id` (str): The ID of the goal to delete

**Returns:**
- `bool`: True if the deletion was successful, False otherwise

**Example:**
```python
success = goal_manager.delete_goal("goal-abc123")
```

## Specification Management API

### SpecManager Class

The `SpecManager` class provides methods for managing specifications.

#### Import

```python
from goal_cli.specs import SpecManager
```

#### Constructor

```python
spec_manager = SpecManager(project_path: Path)
```

**Parameters:**
- `project_path` (Path): The path to the project directory

#### Methods

##### create_spec

Create a new specification for a goal.

```python
spec_id = spec_manager.create_spec(goal_id: str, title: str, description: str) -> str
```

**Parameters:**
- `goal_id` (str): The ID of the goal this specification is for
- `title` (str): The title of the specification
- `description` (str): The description of the specification

**Returns:**
- `str`: The ID of the created specification

**Example:**
```python
spec_manager = SpecManager(Path("/path/to/project"))
spec_id = spec_manager.create_spec("goal-abc123", "Auth Spec", "Authentication specification")
```

##### get_spec

Retrieve a specification by its ID.

```python
spec = spec_manager.get_spec(spec_id: str) -> dict
```

**Parameters:**
- `spec_id` (str): The ID of the specification to retrieve

**Returns:**
- `dict`: The specification data, or None if not found

##### list_specs

List all specifications in the project.

```python
specs = spec_manager.list_specs() -> list
```

**Returns:**
- `list`: A list of specification dictionaries with basic information

##### update_spec

Update an existing specification.

```python
success = spec_manager.update_spec(spec_id: str, updates: dict) -> bool
```

**Parameters:**
- `spec_id` (str): The ID of the specification to update
- `updates` (dict): The updates to apply to the specification

**Returns:**
- `bool`: True if the update was successful, False otherwise

##### delete_spec

Delete a specification by its ID.

```python
success = spec_manager.delete_spec(spec_id: str) -> bool
```

**Parameters:**
- `spec_id` (str): The ID of the specification to delete

**Returns:**
- `bool`: True if the deletion was successful, False otherwise

## Analytics API

### PredictiveAnalyticsEngine Class

The `PredictiveAnalyticsEngine` class provides predictive analytics capabilities.

#### Import

```python
from goal_cli.analytics import PredictiveAnalyticsEngine
```

#### Constructor

```python
analytics_engine = PredictiveAnalyticsEngine(project_path: Path)
```

**Parameters:**
- `project_path` (Path): The path to the project directory

#### Methods

##### analyze_goal_complexity

Analyze the complexity of a goal.

```python
complexity = analytics_engine.analyze_goal_complexity(goal_data: dict) -> dict
```

**Parameters:**
- `goal_data` (dict): The goal data to analyze

**Returns:**
- `dict`: Complexity analysis results

**Example:**
```python
analytics_engine = PredictiveAnalyticsEngine(Path("/path/to/project"))
goal = goal_manager.get_goal("goal-abc123")
complexity = analytics_engine.analyze_goal_complexity(goal)
print(f"Complexity score: {complexity['total_score']}")
```

##### estimate_completion_time

Estimate the completion time for a goal.

```python
estimate = analytics_engine.estimate_completion_time(goal_data: dict) -> int
```

**Parameters:**
- `goal_data` (dict): The goal data to analyze

**Returns:**
- `int`: Estimated completion time in days

##### identify_risk_factors

Identify risk factors for a goal.

```python
risks = analytics_engine.identify_risk_factors(goal_data: dict) -> list
```

**Parameters:**
- `goal_data` (dict): The goal data to analyze

**Returns:**
- `list`: List of identified risk factors

##### enhance_goal_with_analytics

Enhance a goal with predictive analytics data.

```python
enhanced_goal = analytics_engine.enhance_goal_with_analytics(goal_data: dict) -> dict
```

**Parameters:**
- `goal_data` (dict): The goal data to enhance

**Returns:**
- `dict`: Goal data enhanced with analytics metadata

## Governance API

### GovernanceSystem Class

The `GovernanceSystem` class provides governance and compliance functionality.

#### Import

```python
from goal_cli.governance import GovernanceSystem
```

#### Constructor

```python
governance_system = GovernanceSystem(project_path: Path)
```

**Parameters:**
- `project_path` (Path): The path to the project directory

#### Methods

##### initialize_project_constitution

Initialize the project constitution.

```python
constitution_path = governance_system.initialize_project_constitution(project_name: str) -> Path
```

**Parameters:**
- `project_name` (str): The name of the project

**Returns:**
- `Path`: Path to the created constitution file

##### validate_artifact

Validate an artifact against governance rules.

```python
validation_result = governance_system.validate_artifact(artifact_type: str, artifact_data: dict) -> dict
```

**Parameters:**
- `artifact_type` (str): The type of artifact (goal, spec, plan, task)
- `artifact_data` (dict): The artifact data to validate

**Returns:**
- `dict`: Validation results

##### check_compliance

Check compliance with standards and regulations.

```python
compliance_results = governance_system.check_compliance(project_data: dict) -> dict
```

**Parameters:**
- `project_data` (dict): The project data to check

**Returns:**
- `dict`: Compliance results

##### check_security_policies

Check security policy compliance.

```python
security_results = governance_system.check_security_policies(project_data: dict) -> dict
```

**Parameters:**
- `project_data` (dict): The project data to check

**Returns:**
- `dict`: Security compliance results

## Quality Assurance API

### QualityAssuranceSystem Class

The `QualityAssuranceSystem` class provides quality assurance functionality.

#### Import

```python
from goal_cli.quality import QualityAssuranceSystem
```

#### Constructor

```python
qa_system = QualityAssuranceSystem(project_path: Path)
```

**Parameters:**
- `project_path` (Path): The path to the project directory

#### Methods

##### validate_artifact_quality

Validate the quality of an artifact.

```python
quality_result = qa_system.validate_artifact_quality(artifact_type: str, artifact_data: dict) -> dict
```

**Parameters:**
- `artifact_type` (str): The type of artifact (goal, spec, plan, task)
- `artifact_data` (dict): The artifact data to validate

**Returns:**
- `dict`: Quality validation results

##### run_quality_checks

Run all quality checks for the project.

```python
check_results = qa_system.run_quality_checks() -> dict
```

**Returns:**
- `dict`: Results of all quality checks

##### generate_quality_report

Generate a quality assurance report.

```python
report = qa_system.generate_quality_report() -> str
```

**Returns:**
- `str`: Quality assurance report in markdown format

## Testing Integration API

### TestingSystem Class

The `TestingSystem` class provides testing integration functionality.

#### Import

```python
from goal_cli.testing import TestingSystem
```

#### Constructor

```python
testing_system = TestingSystem(project_path: Path)
```

**Parameters:**
- `project_path` (Path): The path to the project directory

#### Methods

##### generate_test_plan

Generate a test plan for a goal.

```python
test_plan = testing_system.generate_test_plan(goal_id: str) -> dict
```

**Parameters:**
- `goal_id` (str): The ID of the goal to generate a test plan for

**Returns:**
- `dict`: Test plan data

##### run_tests

Run all tests for the project.

```python
test_results = testing_system.run_tests() -> dict
```

**Returns:**
- `dict`: Test execution results

##### generate_coverage_report

Generate a test coverage report.

```python
coverage_report = testing_system.generate_coverage_report() -> dict
```

**Returns:**
- `dict`: Test coverage report data

## Monitoring API

### MonitoringSystem Class

The `MonitoringSystem` class provides monitoring functionality.

#### Import

```python
from goal_cli.monitoring import MonitoringSystem
```

#### Constructor

```python
monitoring_system = MonitoringSystem(project_path: Path)
```

**Parameters:**
- `project_path` (Path): The path to the project directory

#### Methods

##### start_monitoring

Start monitoring project progress.

```python
monitoring_system.start_monitoring()
```

##### stop_monitoring

Stop monitoring project progress.

```python
monitoring_system.stop_monitoring()
```

##### get_performance_metrics

Get current performance metrics.

```python
metrics = monitoring_system.get_performance_metrics() -> dict
```

**Returns:**
- `dict`: Current performance metrics

##### generate_alert

Generate an alert based on metrics.

```python
alert = monitoring_system.generate_alert(metric: str, threshold: float) -> dict
```

**Parameters:**
- `metric` (str): The metric to check
- `threshold` (float): The threshold value

**Returns:**
- `dict`: Alert information if threshold is exceeded

## Automation API

### AutomationSystem Class

The `AutomationSystem` class provides automation functionality.

#### Import

```python
from goal_cli.automation import AutomationSystem
```

#### Constructor

```python
automation_system = AutomationSystem(project_path: Path)
```

**Parameters:**
- `project_path` (Path): The path to the project directory

#### Methods

##### setup_workflow

Set up an automation workflow.

```python
workflow_id = automation_system.setup_workflow(workflow_config: dict) -> str
```

**Parameters:**
- `workflow_config` (dict): The workflow configuration

**Returns:**
- `str`: The ID of the created workflow

##### run_workflow

Run a specific workflow.

```python
result = automation_system.run_workflow(workflow_id: str) -> dict
```

**Parameters:**
- `workflow_id` (str): The ID of the workflow to run

**Returns:**
- `dict`: Workflow execution results

##### schedule_task

Schedule an automated task.

```python
task_id = automation_system.schedule_task(cron_expression: str, task_config: dict) -> str
```

**Parameters:**
- `cron_expression` (str): The cron expression for scheduling
- `task_config` (dict): The task configuration

**Returns:**
- `str`: The ID of the scheduled task

## CI/CD Integration API

### CICDSystem Class

The `CICDSystem` class provides CI/CD integration functionality.

#### Import

```python
from goal_cli.cicd import CICDSystem
```

#### Constructor

```python
cicd_system = CICDSystem(project_path: Path)
```

**Parameters:**
- `project_path` (Path): The path to the project directory

#### Methods

##### setup_pipeline

Set up a CI/CD pipeline.

```python
pipeline_id = cicd_system.setup_pipeline(pipeline_config: dict) -> str
```

**Parameters:**
- `pipeline_config` (dict): The pipeline configuration

**Returns:**
- `str`: The ID of the created pipeline

##### run_pipeline

Run a CI/CD pipeline.

```python
result = cicd_system.run_pipeline(pipeline_id: str) -> dict
```

**Parameters:**
- `pipeline_id` (str): The ID of the pipeline to run

**Returns:**
- `dict`: Pipeline execution results

##### get_pipeline_status

Get the status of a pipeline.

```python
status = cicd_system.get_pipeline_status(pipeline_id: str) -> dict
```

**Parameters:**
- `pipeline_id` (str): The ID of the pipeline to check

**Returns:**
- `dict`: Pipeline status information

## Dependency Management API

### DependencyManager Class

The `DependencyManager` class provides dependency management functionality.

#### Import

```python
from goal_cli.dependencies import DependencyManager
```

#### Constructor

```python
dep_manager = DependencyManager(project_path: Path)
```

**Parameters:**
- `project_path` (Path): The path to the project directory

#### Methods

##### analyze_dependencies

Analyze project dependencies.

```python
analysis = dep_manager.analyze_dependencies() -> dict
```

**Returns:**
- `dict`: Dependency analysis results

##### update_dependencies

Update project dependencies.

```python
result = dep_manager.update_dependencies() -> dict
```

**Returns:**
- `dict`: Dependency update results

##### audit_dependencies

Audit dependencies for vulnerabilities.

```python
audit_results = dep_manager.audit_dependencies() -> dict
```

**Returns:**
- `dict`: Dependency audit results

## Documentation Generation API

### DocumentationSystem Class

The `DocumentationSystem` class provides documentation generation functionality.

#### Import

```python
from goal_cli.documentation import DocumentationSystem
```

#### Constructor

```python
docs_system = DocumentationSystem(project_path: Path)
```

**Parameters:**
- `project_path` (Path): The path to the project directory

#### Methods

##### generate_documentation

Generate project documentation.

```python
docs_system.generate_documentation() -> str
```

**Returns:**
- `str`: Path to generated documentation

##### update_documentation

Update existing documentation.

```python
docs_system.update_documentation() -> str
```

**Returns:**
- `str`: Path to updated documentation

##### validate_documentation

Validate documentation quality.

```python
validation_result = docs_system.validate_documentation() -> dict
```

**Returns:**
- `dict`: Documentation validation results

## Performance Optimization API

### PerformanceSystem Class

The `PerformanceSystem` class provides performance optimization functionality.

#### Import

```python
from goal_cli.performance import PerformanceSystem
```

#### Constructor

```python
perf_system = PerformanceSystem(project_path: Path)
```

**Parameters:**
- `project_path` (Path): The path to the project directory

#### Methods

##### analyze_performance

Analyze performance bottlenecks.

```python
analysis = perf_system.analyze_performance() -> dict
```

**Returns:**
- `dict`: Performance analysis results

##### optimize_performance

Optimize project performance.

```python
optimization_result = perf_system.optimize_performance() -> dict
```

**Returns:**
- `dict`: Performance optimization results

##### run_benchmarks

Run performance benchmarks.

```python
benchmark_results = perf_system.run_benchmarks() -> dict
```

**Returns:**
- `dict`: Benchmark results

## Security Scanning API

### SecuritySystem Class

The `SecuritySystem` class provides security scanning functionality.

#### Import

```python
from goal_cli.security import SecuritySystem
```

#### Constructor

```python
security_system = SecuritySystem(project_path: Path)
```

**Parameters:**
- `project_path` (Path): The path to the project directory

#### Methods

##### scan_vulnerabilities

Scan for security vulnerabilities.

```python
scan_results = security_system.scan_vulnerabilities() -> dict
```

**Returns:**
- `dict`: Vulnerability scan results

##### audit_security

Perform security audit.

```python
audit_results = security_system.audit_security() -> dict
```

**Returns:**
- `dict`: Security audit results

##### generate_security_report

Generate security report.

```python
report = security_system.generate_security_report() -> str
```

**Returns:**
- `str`: Security report in markdown format

## AI Agent Integration API

### AgentManager Class

The `AgentManager` class provides AI agent integration functionality.

#### Import

```python
from goal_cli.agents import AgentManager
```

#### Constructor

```python
agent_manager = AgentManager(project_path: Path, agent_type: str)
```

**Parameters:**
- `project_path` (Path): The path to the project directory
- `agent_type` (str): The type of AI agent to use

#### Methods

##### generate_code

Generate code using the AI agent.

```python
code = agent_manager.generate_code(specification: dict) -> str
```

**Parameters:**
- `specification` (dict): The specification to generate code from

**Returns:**
- `str`: Generated code

##### review_code

Review code using the AI agent.

```python
review = agent_manager.review_code(code: str) -> dict
```

**Parameters:**
- `code` (str): The code to review

**Returns:**
- `dict`: Code review results

##### refactor_code

Refactor code using the AI agent.

```python
refactored_code = agent_manager.refactor_code(code: str) -> str
```

**Parameters:**
- `code` (str): The code to refactor

**Returns:**
- `str`: Refactored code

##### explain_code

Explain code functionality using the AI agent.

```python
explanation = agent_manager.explain_code(code: str) -> str
```

**Parameters:**
- `code` (str): The code to explain

**Returns:**
- `str`: Code explanation

## UI Components API

### UI Components

The `ui_components` module provides reusable UI components for CLI applications.

#### Import

```python
from goal_cli.ui_components import (
    show_banner,
    BannerGroup,
    StepTracker,
    select_with_arrows,
    get_user_input,
    validate_project_name
)
```

#### Functions

##### show_banner

Display the ASCII art banner.

```python
show_banner()
```

##### select_with_arrows

Provide an interactive selection interface with arrow keys.

```python
selected = select_with_arrows(choices: dict, prompt: str, default: str) -> str
```

**Parameters:**
- `choices` (dict): Dictionary of choices
- `prompt` (str): Prompt to display
- `default` (str): Default selection

**Returns:**
- `str`: Selected choice

##### get_user_input

Get user input with validation.

```python
user_input = get_user_input(prompt: str, default: str, validator: callable) -> str
```

**Parameters:**
- `prompt` (str): Prompt to display
- `default` (str): Default value
- `validator` (callable): Validation function

**Returns:**
- `str`: User input

##### StepTracker

Track steps in a process.

```python
tracker = StepTracker(name: str, total_steps: int)
```

**Parameters:**
- `name` (str): Name of the process
- `total_steps` (int): Total number of steps

**Methods:**
- `add(step_id: str, description: str)`: Add a step
- `start(step_id: str, message: str)`: Start a step
- `complete(step_id: str, message: str)`: Complete a step
- `error(step_id: str, message: str)`: Mark a step as errored
- `skip(step_id: str, message: str)`: Skip a step

## Extending the CLI

### Adding New Commands

To add new commands to the CLI, you can integrate them with the main Typer app:

```python
from goal_cli import app

@app.command()
def my_new_command(
    param1: str = typer.Argument(..., help="First parameter"),
    param2: bool = typer.Option(False, "--flag", "-f", help="A boolean flag")
):
    """
    Description of my new command.
    """
    # Implementation here
    pass
```

### Integrating with Main CLI

To integrate your module with the main CLI, create an integration function:

```python
# In your module file (e.g., my_module.py)
import typer

def integrate_my_module_with_main_cli(app: typer.Typer) -> typer.Typer:
    """
    Integrate my module with the main CLI app.
    """
    app.add_typer(my_new_command_app, name="my-module")
    return app

# In __init__.py
from .my_module import integrate_my_module_with_main_cli

def main():
    # ... existing integrations ...
    app = integrate_my_module_with_main_cli(app)
    app()
```

## Best Practices for Extensions

1. **Follow Naming Conventions**: Use consistent naming for classes, functions, and variables
2. **Handle Errors Gracefully**: Implement proper error handling and user feedback
3. **Maintain Compatibility**: Ensure your extensions work with existing functionality
4. **Document Your Code**: Provide clear documentation for your API extensions
5. **Test Thoroughly**: Write tests for your extensions
6. **Use Type Hints**: Provide type hints for better code clarity and IDE support
7. **Follow Project Structure**: Adhere to the existing project organization
8. **Respect Configuration**: Use existing configuration systems when possible

## Example Extension

Here's a complete example of how to create a simple extension:

```python
# my_extension.py
import typer
from pathlib import Path
from typing import Optional

from goal_cli.goals import GoalManager

app = typer.Typer()

@app.command()
def summarize_goals(
    project_path: Path = typer.Option(".", "--path", "-p", help="Project path")
):
    """
    Summarize all goals in the project.
    """
    try:
        goal_manager = GoalManager(project_path)
        goals = goal_manager.list_goals()
        
        if not goals:
            typer.echo("No goals found in this project.")
            return
        
        typer.echo(f"Found {len(goals)} goals:")
        for goal in goals:
            typer.echo(f"  - {goal['title']} ({goal['status']})")
            
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(1)

def integrate_with_main_cli(app: typer.Typer) -> typer.Typer:
    """
    Integrate the extension with the main CLI.
    """
    app.add_typer(summarize_goals_app, name="summary")
    return app
```

This API documentation provides developers with the information they need to extend the Goal-Dev-Spec tool with custom functionality, integrations, or plugins.