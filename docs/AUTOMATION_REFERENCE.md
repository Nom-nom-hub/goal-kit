# Goal-Dev-Spec Automation and CI/CD Integration

This document provides a comprehensive overview of the Goal-Dev-Spec automation and CI/CD integration features, detailing how to automate workflows and integrate with continuous integration and deployment pipelines.

## Overview

The Goal-Dev-Spec automation system provides powerful tools for automating repetitive tasks, managing workflows, and integrating with CI/CD pipelines. The system includes features for workflow automation, task scheduling, pipeline management, and deployment automation.

## Automation System Components

### Automation Framework

The automation framework includes:

```
.goal/automation/
├── workflows/
├── scheduled-tasks/
├── pipelines/
└── deployment/
```

### CI/CD Integration

The CI/CD integration supports:

```
.cicd/
├── pipelines/
├── templates/
├── configs/
└── scripts/
```

### Automation CLI Commands

The automation system is accessible through CLI commands:

- `goal automate setup-workflow`: Set up automation workflow
- `goal automate run-workflow`: Run a specific workflow
- `goal automate schedule-task`: Schedule an automated task
- `goal automate workflow-status`: Check workflow status

## CLI Commands

### `goal automate setup-workflow` - Setup Workflow

Set up an automation workflow.

#### Usage

```bash
goal automate setup-workflow WORKFLOW_NAME
```

#### Features

- Interactive workflow configuration
- Template-based setup
- Validation of workflow configuration
- Integration with existing workflows

#### Examples

```bash
# Set up a deployment workflow
goal automate setup-workflow deployment

# Set up a testing workflow
goal automate setup-workflow testing

# Set up a custom workflow
goal automate setup-workflow custom-process
```

#### Interactive Process

```
Setting up workflow: deployment
Workflow Type:
↑ Basic Deployment
  Advanced Deployment
  Custom Workflow
  Cancel

Workflow Name: deployment
Trigger:
↑ Manual
  Git Push
  Scheduled
  Webhook

Steps:
1. Build Application
2. Run Tests
3. Deploy to Staging
4. Run Integration Tests
5. Deploy to Production

Save workflow? [Y/n]: Y
Workflow saved to: .goal/automation/workflows/deployment.yaml
```

### `goal automate run-workflow` - Run Workflow

Run a specific workflow.

#### Usage

```bash
goal automate run-workflow WORKFLOW_NAME
```

#### Features

- Execution of predefined workflows
- Real-time progress tracking
- Error handling and recovery
- Logging and reporting

#### Examples

```bash
# Run a deployment workflow
goal automate run-workflow deployment

# Run a testing workflow
goal automate run-workflow testing

# Run with specific parameters
goal automate run-workflow deployment --env production
```

#### Output

```
Running workflow: deployment
Starting step 1: Build Application
✓ Build completed successfully (Duration: 2m 15s)

Starting step 2: Run Tests
✓ Tests passed (Duration: 1m 30s)

Starting step 3: Deploy to Staging
✓ Deployment to staging successful (Duration: 45s)

Starting step 4: Run Integration Tests
✓ Integration tests passed (Duration: 2m 5s)

Starting step 5: Deploy to Production
✓ Deployment to production successful (Duration: 1m 10s)

Workflow completed successfully!
Total Duration: 8m 5s
```

### `goal automate schedule-task` - Schedule Task

Schedule an automated task.

#### Usage

```bash
goal automate schedule-task CRON_EXPRESSION TASK_COMMAND
```

#### Features

- Cron-based scheduling
- Task parameterization
- Schedule management
- Notification system

#### Examples

```bash
# Schedule a daily backup
goal automate schedule-task "0 2 * * *" "backup-project"

# Schedule weekly reports
goal automate schedule-task "0 0 * * 1" "generate-weekly-report"

# Schedule with parameters
goal automate schedule-task "*/30 * * * *" "check-system-status --detailed"
```

#### Output

```
Scheduling task: backup-project
Cron Expression: 0 2 * * *
Next Run: 2025-01-16 02:00:00

Task scheduled successfully!
Task ID: task-backup-20250115-1200
```

### `goal automate workflow-status` - Workflow Status

Check the status of workflows.

#### Usage

```bash
goal automate workflow-status [WORKFLOW_NAME]
```

#### Features

- Real-time status monitoring
- Execution history
- Performance metrics
- Error tracking

#### Examples

```bash
# Check status of all workflows
goal automate workflow-status

# Check status of specific workflow
goal automate workflow-status deployment
```

#### Output

```
Workflow Status Report
Generated: 2025-01-15 14:30:00

Active Workflows:
- deployment: Running (Started: 14:25:00, Step: 3/5)
- testing: Completed (Finished: 14:15:00, Duration: 3m 45s)
- backup: Scheduled (Next Run: 2025-01-16 02:00:00)

Recent Executions:
- deployment: Success (Duration: 8m 5s)
- testing: Success (Duration: 3m 45s)
- code-quality: Failed (Error: Test coverage below threshold)
```

## Workflow Management

### Workflow Configuration

Workflows are defined in `.goal/automation/workflows/`:

```yaml
# .goal/automation/workflows/deployment.yaml
workflow:
  name: "deployment"
  description: "Deploy application to staging and production"
  version: "1.0.0"
  
  trigger:
    type: "manual"
    conditions: []
  
  steps:
    - name: "build"
      description: "Build the application"
      action: "execute-script"
      script: "scripts/build.sh"
      timeout: 300
      
    - name: "test"
      description: "Run unit tests"
      action: "execute-script"
      script: "scripts/test.sh"
      timeout: 600
      
    - name: "deploy-staging"
      description: "Deploy to staging environment"
      action: "deploy"
      environment: "staging"
      timeout: 300
      
    - name: "integration-test"
      description: "Run integration tests"
      action: "execute-script"
      script: "scripts/integration-test.sh"
      timeout: 900
      
    - name: "deploy-production"
      description: "Deploy to production environment"
      action: "deploy"
      environment: "production"
      timeout: 300
  
  notifications:
    on_success:
      - type: "email"
        recipients: ["team@example.com"]
        template: "deployment-success"
        
    on_failure:
      - type: "slack"
        channel: "#deployments"
        template: "deployment-failure"
        
    on_start:
      - type: "slack"
        channel: "#deployments"
        template: "deployment-started"
```

### Workflow Execution

Workflow execution follows this process:

1. **Trigger**: Workflow is triggered by defined conditions
2. **Validation**: Workflow configuration is validated
3. **Execution**: Steps are executed in sequence
4. **Monitoring**: Progress is monitored in real-time
5. **Notification**: Status updates are sent
6. **Reporting**: Execution results are recorded

### Workflow Templates

Predefined workflow templates are available:

```yaml
# .goal/automation/templates/testing.yaml
template:
  name: "testing"
  description: "Run comprehensive test suite"
  
  steps:
    - name: "unit-tests"
      action: "execute-script"
      script: "scripts/unit-tests.sh"
      
    - name: "integration-tests"
      action: "execute-script"
      script: "scripts/integration-tests.sh"
      
    - name: "e2e-tests"
      action: "execute-script"
      script: "scripts/e2e-tests.sh"
      
    - name: "performance-tests"
      action: "execute-script"
      script: "scripts/performance-tests.sh"
      
    - name: "security-tests"
      action: "execute-script"
      script: "scripts/security-tests.sh"
      
    - name: "generate-report"
      action: "execute-script"
      script: "scripts/generate-test-report.sh"
```

## Task Scheduling

### Cron Expression Support

The scheduling system supports standard cron expressions:

```
* * * * * *
│ │ │ │ │ │
│ │ │ │ │ └── Day of week (0-7, where 0 and 7 are Sunday)
│ │ │ │ └──── Month (1-12)
│ │ │ └────── Day of month (1-31)
│ │ └──────── Hour (0-23)
│ └────────── Minute (0-59)
└──────────── Second (0-59, optional)
```

### Scheduled Task Configuration

Scheduled tasks are defined in `.goal/automation/scheduled-tasks/`:

```yaml
# .goal/automation/scheduled-tasks/daily-backup.yaml
scheduled-task:
  name: "daily-backup"
  description: "Perform daily backup of project data"
  cron: "0 2 * * *"
  
  command:
    type: "script"
    path: "scripts/backup.sh"
    parameters:
      - "--full"
      - "--compress"
      
  environment:
    BACKUP_DIR: "/backups"
    RETENTION_DAYS: "30"
    
  notifications:
    on_success:
      - type: "email"
        recipients: ["admin@example.com"]
        
    on_failure:
      - type: "email"
        recipients: ["admin@example.com"]
      - type: "slack"
        channel: "#alerts"
```

### Task Management

Task management features include:

- **Scheduling**: Define when tasks should run
- **Execution**: Run tasks automatically or manually
- **Monitoring**: Track task execution status
- **History**: Maintain execution history
- **Notifications**: Send status updates

## CI/CD Integration

### `goal cicd setup-pipeline` - Setup Pipeline

Set up a CI/CD pipeline.

#### Usage

```bash
goal cicd setup-pipeline PIPELINE_TYPE
```

#### Features

- Pipeline template selection
- Interactive configuration
- Integration with popular CI/CD platforms
- Validation of pipeline configuration

#### Examples

```bash
# Set up GitHub Actions pipeline
goal cicd setup-pipeline github-actions

# Set up GitLab CI pipeline
goal cicd setup-pipeline gitlab-ci

# Set up Jenkins pipeline
goal cicd setup-pipeline jenkins
```

### `goal cicd run-pipeline` - Run Pipeline

Run a CI/CD pipeline.

#### Usage

```bash
goal cicd run-pipeline PIPELINE_NAME
```

#### Features

- Pipeline execution
- Real-time progress tracking
- Log streaming
- Status reporting

#### Examples

```bash
# Run the main pipeline
goal cicd run-pipeline main

# Run with specific branch
goal cicd run-pipeline main --branch feature/new-feature

# Run with parameters
goal cicd run-pipeline main --param environment=staging
```

### `goal cicd pipeline-status` - Pipeline Status

Check the status of CI/CD pipelines.

#### Usage

```bash
goal cicd pipeline-status [PIPELINE_NAME]
```

#### Features

- Pipeline status monitoring
- Execution history
- Performance metrics
- Error tracking

#### Examples

```bash
# Check status of all pipelines
goal cicd pipeline-status

# Check status of specific pipeline
goal cicd pipeline-status main
```

### `goal cicd configure` - Configure Pipeline

Configure pipeline settings.

#### Usage

```bash
goal cicd configure
```

#### Features

- Interactive configuration
- Environment variable management
- Secret management
- Pipeline customization

#### Examples

```bash
# Configure pipeline settings
goal cicd configure
```

## Pipeline Configuration

### GitHub Actions Pipeline

GitHub Actions pipeline configuration:

```yaml
# .github/workflows/main.yaml
name: Main Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        
    - name: Run tests
      run: |
        python -m pytest
        
    - name: Build application
      run: |
        python setup.py build
        
    - name: Deploy to staging
      if: github.ref == 'refs/heads/main'
      run: |
        ./scripts/deploy-staging.sh
        
    - name: Deploy to production
      if: github.ref == 'refs/heads/main' && github.event_name == 'push'
      run: |
        ./scripts/deploy-production.sh
```

### GitLab CI Pipeline

GitLab CI pipeline configuration:

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  PYTHON_VERSION: "3.9"

before_script:
  - pip install -r requirements.txt

test:
  stage: test
  script:
    - python -m pytest
  only:
    - main
    - merge_requests

build:
  stage: build
  script:
    - python setup.py build
  only:
    - main

deploy-staging:
  stage: deploy
  script:
    - ./scripts/deploy-staging.sh
  only:
    - main
  environment:
    name: staging

deploy-production:
  stage: deploy
  script:
    - ./scripts/deploy-production.sh
  only:
    - main
  when: manual
  environment:
    name: production
```

## Deployment Automation

### Deployment Configuration

Deployment configurations are stored in `.goal/automation/deployment/`:

```yaml
# .goal/automation/deployment/staging.yaml
deployment:
  name: "staging"
  description: "Staging environment deployment"
  
  target:
    type: "server"
    host: "staging.example.com"
    port: 22
    user: "deploy"
    
  steps:
    - name: "prepare"
      action: "execute-remote"
      command: "mkdir -p /app/staging"
      
    - name: "upload"
      action: "upload-files"
      source: "dist/"
      destination: "/app/staging/"
      
    - name: "install-dependencies"
      action: "execute-remote"
      command: "pip install -r /app/staging/requirements.txt"
      
    - name: "restart-service"
      action: "execute-remote"
      command: "systemctl restart myapp-staging"
      
  rollback:
    steps:
      - name: "restore-previous"
        action: "execute-remote"
        command: "cp -r /app/staging-backup/* /app/staging/"
        
      - name: "restart-service"
        action: "execute-remote"
        command: "systemctl restart myapp-staging"
```

### Deployment Process

The deployment process includes:

1. **Preparation**: Environment setup and validation
2. **Build**: Application build and packaging
3. **Upload**: Transfer files to target environment
4. **Installation**: Dependency installation and configuration
5. **Activation**: Service restart and activation
6. **Verification**: Health checks and validation
7. **Rollback**: Automatic rollback on failure

## Best Practices

1. **Define Clear Workflows**: Create well-defined workflows for common processes
2. **Use Templates**: Leverage templates for consistent workflow creation
3. **Monitor Execution**: Regularly monitor workflow and task execution
4. **Handle Failures**: Implement proper error handling and rollback procedures
5. **Secure Secrets**: Properly manage secrets and sensitive information
6. **Document Processes**: Maintain documentation for automation workflows
7. **Test Thoroughly**: Test workflows in safe environments before production use
8. **Version Control**: Keep automation configurations in version control

## Integration with Development Workflow

The automation system integrates with the development workflow:

1. **CI/CD Pipelines**: Automated testing and deployment
2. **Scheduled Tasks**: Regular maintenance and reporting
3. **Workflow Automation**: Complex process automation
4. **Deployment**: Automated deployment to environments
5. **Monitoring**: Continuous monitoring of automated processes

## Troubleshooting

### Common Issues

1. **Workflow Failures**: Check logs and implement proper error handling
2. **Scheduling Problems**: Verify cron expressions and system time
3. **Deployment Issues**: Validate deployment configurations and permissions
4. **CI/CD Integration**: Ensure proper authentication and access

### Getting Help

For additional help with automation and CI/CD features:
- Use `goal automate --help` and `goal cicd --help` for command-specific help
- Check the automation documentation in the `docs/` directory
- Review automation configurations in the `.goal/automation/` directory
- Examine CI/CD configurations in the appropriate platform directories