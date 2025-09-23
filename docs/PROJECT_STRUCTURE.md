# Goal-Dev-Spec Project Structure and Organization

This document provides a comprehensive overview of the Goal-Dev-Spec project structure and organization, detailing each directory and file's purpose within the system.

## Overview

The Goal-Dev-Spec project structure is designed to support complex software development projects with a focus on goal-driven development, governance, and collaboration. The structure separates concerns while maintaining clear relationships between different aspects of the project.

## Root Directory Structure

```
[project-name]/
├── .goal/                    # Core Goal-Dev-Spec files
├── src/                     # Source code (when applicable)
├── tests/                   # Test files
├── docs/                    # Documentation
├── assets/                  # Media and static assets
├── scripts/                 # Automation scripts
├── teams/                   # Team-specific configurations
├── .environments/           # Environment management
├── .workflows/             # Workflow configurations
├── goal.yaml               # Project configuration
├── README.md               # Project overview
├── CONTRIBUTING.md         # Contribution guidelines
├── CHANGELOG.md            # Version history
└── LICENSE                 # License information
```

## Detailed Directory Descriptions

### .goal/ - Core Goal-Dev-Spec Files

The `.goal` directory contains all Goal-Dev-Spec artifacts, organized by purpose:

#### config/
Project-level configuration files including:
- `project.yaml` - Main project configuration
- `agents.yaml` - AI agent configurations
- `teams.yaml` - Team structure and permissions
- `workflows.yaml` - Workflow definitions

#### goals/
Individual goal specifications, each in its own directory:
```
.goals/
├── goal-abc123/
│   ├── goal.yaml
│   ├── metadata.yaml
│   └── history/
└── goal-xyz789/
    ├── goal.yaml
    ├── metadata.yaml
    └── history/
```

#### specs/
Feature specifications linked to goals:
```
.specs/
├── spec-def456/
│   ├── spec.yaml
│   ├── requirements.yaml
│   └── validation/
└── spec-ghi789/
    ├── spec.yaml
    ├── requirements.yaml
    └── validation/
```

#### plans/
Implementation plans for goals:
```
.plans/
├── plan-jkl012/
│   ├── plan.yaml
│   ├── timeline.yaml
│   ├── resources.yaml
│   └── risks.yaml
└── plan-mno345/
    ├── plan.yaml
    ├── timeline.yaml
    ├── resources.yaml
    └── risks.yaml
```

#### tasks/
Task breakdowns from plans:
```
.tasks/
├── task-pqr678/
│   ├── task.yaml
│   ├── progress.yaml
│   └── comments/
└── task-stu901/
    ├── task.yaml
    ├── progress.yaml
    └── comments/
```

#### templates/
Template system with multiple formats and project types:
- `md/` - Markdown templates for human-readable specifications
- `yaml/` - YAML templates for programmatic processing
- `project-types/` - Predefined templates for different project types

#### agents/
AI agent-specific configurations:
- Agent settings and preferences
- Custom prompts and instructions
- Integration configurations

#### analytics/
Predictive analytics data:
- Historical project data
- Performance metrics
- Predictive models

#### governance/
Governance artifacts for compliance and quality assurance:
- Policies and standards
- Audit records
- Compliance checklists
- Security assessments
- Review records

#### environments/
Environment-specific configurations:
- Development, staging, production settings
- Environment variables
- Configuration overrides

#### workflows/
Defined workflows for project processes:
- Custom workflow definitions
- Automation scripts
- Integration configurations

#### reports/
Generated reports for project tracking:
- Progress reports
- Analytics reports
- Governance reports
- Compliance reports

### src/ - Source Code

When the project includes implementation, source code is organized by modules or features:
```
src/
├── modules/
│   ├── authentication/
│   ├── user-management/
│   └── reporting/
├── shared/
│   ├── utilities/
│   ├── components/
│   └── services/
└── main.py
```

### tests/ - Test Files

Comprehensive testing structure:
```
tests/
├── unit/
├── integration/
├── e2e/
├── performance/
└── security/
```

### docs/ - Documentation

Structured documentation organized by purpose:
- `architecture/` - System architecture and design decisions
- `guides/` - User and developer guides
- `api/` - API documentation
- `tutorials/` - Step-by-step tutorials

### assets/ - Media and Static Assets

Organized asset management:
- `images/` - Graphics, diagrams, screenshots
- `videos/` - Demonstration videos, tutorials
- `documents/` - PDFs, specs, reference materials
- `fonts/` - Custom fonts

### scripts/ - Automation Scripts

Task automation organized by purpose:
- `setup/` - Project initialization scripts
- `deployment/` - Deployment automation
- `maintenance/` - Maintenance tasks
- `utilities/` - Utility scripts

### teams/ - Team Configurations

Team-specific configurations and resources:
- `engineering/` - Engineering team resources
- `design/` - Design team resources
- `product/` - Product team resources
- `qa/` - QA team resources

### .environments/ - Environment Management

Environment-specific configuration files:
- `.env.development` - Development environment variables
- `.env.staging` - Staging environment variables
- `.env.production` - Production environment variables
- `.env.local` - Local overrides

### .workflows/ - Workflow Configurations

Custom workflow definitions:
- CI/CD configurations
- Automation workflows
- Notification settings

## File Naming Conventions

To ensure consistency and clarity across the project:

1. **Directories**: Use lowercase with hyphens (`user-management`, `api-integration`)
2. **Files**: Use lowercase with hyphens (`user-service.yaml`, `api-spec.md`)
3. **IDs**: Use alphanumeric with hyphens (`goal-abc123`, `spec-def456`)
4. **Dates**: Use ISO 8601 format (`YYYY-MM-DD`)
5. **Versions**: Use semantic versioning (`v1.2.3`)

## Separation of Concerns

The structure clearly separates different concerns:

1. **Specification** - `.goal/` directory
2. **Implementation** - `src/` directory
3. **Testing** - `tests/` directory
4. **Documentation** - `docs/` directory
5. **Assets** - `assets/` directory
6. **Automation** - `scripts/` directory
7. **Configuration** - Various config files and directories
8. **Governance** - `.goal/governance/` directory

This separation ensures that each aspect of the project can be managed independently while maintaining clear relationships between components.

## Project Configuration (goal.yaml)

The main project configuration file contains:

```yaml
project:
  name: "Project Name"
  version: "1.0.0"
  description: "Project description"
  created_at: "2025-01-01"
  updated_at: "2025-01-01"
  
settings:
  default_agent: "claude"
  script_type: "sh"
  enable_analytics: true
  enable_governance: true
  
teams:
  - name: "engineering"
    members: ["user1", "user2"]
  - name: "product"
    members: ["user3"]
    
environments:
  - development
  - staging
  - production
```

## Best Practices

1. **Maintain the structure**: Keep files in their appropriate directories to maintain organization.

2. **Use consistent naming**: Follow the naming conventions for all files and directories.

3. **Document changes**: Update documentation when making significant structural changes.

4. **Version control**: Use version control to track changes to the project structure.

5. **Regular cleanup**: Periodically review and clean up unused files and directories.

6. **Team collaboration**: Use the teams directory to manage team-specific configurations and resources.

7. **Environment management**: Use the environments directory to manage different deployment environments.

8. **Workflow automation**: Use the workflows directory to define and manage automated processes.

This structure provides a solid foundation for managing complex software development projects while maintaining clarity and organization throughout the development lifecycle.