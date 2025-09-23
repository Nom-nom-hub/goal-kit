# Goal-Dev-Spec Template System

This document provides a comprehensive overview of the Goal-Dev-Spec template system, detailing the available templates and how to use them effectively in your projects.

## Overview

The Goal-Dev-Spec template system provides structured templates for creating consistent and comprehensive project artifacts. The system includes both YAML templates for programmatic processing and Markdown templates for human-readable documentation.

## Template Directory Structure

```
templates/
├── project-types/
│   ├── web-application/
│   │   ├── goal-template.yaml
│   │   ├── spec-template.yaml
│   │   ├── plan-template.yaml
│   │   └── tasks-template.yaml
│   ├── mobile-application/
│   │   ├── goal-template.yaml
│   │   ├── spec-template.yaml
│   │   ├── plan-template.yaml
│   │   └── tasks-template.yaml
│   ├── data-science/
│   │   ├── goal-template.yaml
│   │   ├── spec-template.yaml
│   │   ├── plan-template.yaml
│   │   └── tasks-template.yaml
│   ├── api-service/
│   │   ├── goal-template.yaml
│   │   ├── spec-template.yaml
│   │   ├── plan-template.yaml
│   │   └── tasks-template.yaml
│   └── generic/
│       ├── goal-template.yaml
│       ├── spec-template.yaml
│       ├── plan-template.yaml
│       └── tasks-template.yaml
├── components/
│   ├── authentication/
│   ├── user-management/
│   ├── reporting/
│   └── notifications/
├── workflows/
│   ├── development/
│   ├── testing/
│   ├── deployment/
│   └── maintenance/
├── md/
│   ├── commands/
│   ├── goal-template.md
│   ├── spec-template.md
│   ├── plan-template.md
│   └── tasks-template.md
└── yaml/
    ├── goal-template.yaml
    ├── spec-template.yaml
    ├── plan-template.yaml
    └── tasks-template.yaml
```

## YAML Templates

YAML templates provide structured data formats for programmatic processing and validation.

### Goal Template (yaml/goal-template.yaml)

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

### Specification Template (yaml/spec-template.yaml)

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

### Plan Template (yaml/plan-template.yaml)

```yaml
id: ""
goal_id: ""
spec_id: ""
title: ""
description: ""
tasks: []
timeline: ""
resources: []
risks: []
dependencies: []
created_at: ""
updated_at: ""
status: "draft"  # draft, planned, in_progress, completed
metadata: {}
```

### Tasks Template (yaml/tasks-template.yaml)

```yaml
id: ""
plan_id: ""
title: ""
description: ""
status: "todo"  # todo, in_progress, completed, blocked
priority: "medium"  # low, medium, high, critical
assignee: ""
due_date: ""
dependencies: []
created_at: ""
updated_at: ""
metadata: {}
```

## Markdown Templates

Markdown templates provide human-readable formats with structured sections for comprehensive documentation.

### Goal Template (md/goal-template.md)

```markdown
# [Goal Title]

## Description
[Detailed description of the goal]

## Objectives
- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

## Success Criteria
- [ ] Success criterion 1
- [ ] Success criterion 2
- [ ] Success criterion 3

## Dependencies
- [ ] Dependency 1
- [ ] Dependency 2

## Related Goals
- [ ] Related goal 1
- [ ] Related goal 2

## Priority
[low/medium/high/critical]

## Status
[draft/planned/in_progress/completed/blocked]

## Owner
[Owner name]

## Tags
- tag1
- tag2

## Metadata
- Created: [Date]
- Updated: [Date]
```

### Specification Template (md/spec-template.md)

```markdown
# [Specification Title]

## Description
[Detailed description of the specification]

## User Stories
### Story 1
**As a** [user type]
**I want** [feature]
**So that** [benefit]

### Story 2
**As a** [user type]
**I want** [feature]
**So that** [benefit]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Functional Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Non-Functional Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Constraints
- [ ] Constraint 1
- [ ] Constraint 2

## Assumptions
- [ ] Assumption 1
- [ ] Assumption 2

## Out of Scope
- [ ] Item 1
- [ ] Item 2

## Status
[draft/reviewed/approved/implemented]

## Metadata
- Created: [Date]
- Updated: [Date]
```

## Project Type Templates

### Web Application Templates

Templates specifically designed for web application development projects.

#### Goal Template (project-types/web-application/goal-template.yaml)
```yaml
id: ""
title: ""
description: ""
objectives: 
  - "Develop responsive user interface"
  - "Implement secure authentication"
  - "Ensure cross-browser compatibility"
success_criteria: 
  - "Application loads in under 2 seconds"
  - "Passes security audit"
  - "Works on all supported browsers"
dependencies: []
related_goals: []
priority: "medium"
status: "draft"
created_at: ""
updated_at: ""
owner: ""
tags: ["web", "frontend", "backend"]
metadata: 
  project_type: "web-application"
  tech_stack: 
    - "React"
    - "Node.js"
    - "MongoDB"
```

#### Specification Template (project-types/web-application/spec-template.yaml)
```yaml
id: ""
goal_id: ""
title: ""
description: ""
user_stories: 
  - "As a user, I want to register for an account so that I can access the application"
  - "As a user, I want to log in to my account so that I can access my data"
  - "As a user, I want to reset my password so that I can regain access if I forget it"
acceptance_criteria: 
  - "User can successfully register with valid information"
  - "User can log in with correct credentials"
  - "User can reset password via email"
functional_requirements: 
  - "User registration form with validation"
  - "Login authentication"
  - "Password reset functionality"
non_functional_requirements: 
  - "Response time under 1 second"
  - "Support for latest 2 browser versions"
  - "99.9% uptime"
constraints: 
  - "Must comply with GDPR"
  - "Must support mobile devices"
assumptions: 
  - "Users have access to email"
  - "Users have modern browsers"
out_of_scope: 
  - "Social media integration"
  - "Multi-language support"
created_at: ""
updated_at: ""
status: "draft"
metadata: 
  project_type: "web-application"
```

### Mobile Application Templates

Templates specifically designed for mobile application development projects.

#### Goal Template (project-types/mobile-application/goal-template.yaml)
```yaml
id: ""
title: ""
description: ""
objectives: 
  - "Develop native mobile application"
  - "Implement offline functionality"
  - "Ensure app store compliance"
success_criteria: 
  - "Application installs successfully"
  - "Passes app store review"
  - "Achieves 4.5+ star rating"
dependencies: []
related_goals: []
priority: "medium"
status: "draft"
created_at: ""
updated_at: ""
owner: ""
tags: ["mobile", "ios", "android"]
metadata: 
  project_type: "mobile-application"
  platforms: 
    - "iOS"
    - "Android"
```

### Data Science Templates

Templates specifically designed for data science projects.

#### Goal Template (project-types/data-science/goal-template.yaml)
```yaml
id: ""
title: ""
description: ""
objectives: 
  - "Develop predictive model"
  - "Validate model accuracy"
  - "Deploy model to production"
success_criteria: 
  - "Model achieves 90%+ accuracy"
  - "Model processes data in real-time"
  - "Model deployed successfully"
dependencies: []
related_goals: []
priority: "medium"
status: "draft"
created_at: ""
updated_at: ""
owner: ""
tags: ["data-science", "machine-learning", "analytics"]
metadata: 
  project_type: "data-science"
  tools: 
    - "Python"
    - "TensorFlow"
    - "Jupyter"
```

### API Service Templates

Templates specifically designed for API service development projects.

#### Goal Template (project-types/api-service/goal-template.yaml)
```yaml
id: ""
title: ""
description: ""
objectives: 
  - "Develop RESTful API"
  - "Implement authentication and authorization"
  - "Ensure API documentation"
success_criteria: 
  - "API responds in under 100ms"
  - "Passes security audit"
  - "Complete API documentation"
dependencies: []
related_goals: []
priority: "medium"
status: "draft"
created_at: ""
updated_at: ""
owner: ""
tags: ["api", "rest", "microservice"]
metadata: 
  project_type: "api-service"
  protocols: 
    - "REST"
    - "GraphQL"
```

## Component Templates

Reusable templates for common components that can be used across different project types.

### Authentication Component Templates

Templates for implementing authentication systems.

#### Specification Template (components/authentication/spec-template.yaml)
```yaml
id: ""
goal_id: ""
title: "User Authentication System"
description: "Specification for implementing a secure user authentication system"
user_stories: 
  - "As a user, I want to register for an account so that I can access the application"
  - "As a user, I want to log in to my account so that I can access my data"
  - "As a user, I want to reset my password so that I can regain access if I forget it"
acceptance_criteria: 
  - "User can successfully register with valid information"
  - "User can log in with correct credentials"
  - "User can reset password via email"
functional_requirements: 
  - "User registration form with validation"
  - "Login authentication"
  - "Password reset functionality"
  - "Session management"
non_functional_requirements: 
  - "Password encryption"
  - "Rate limiting for login attempts"
  - "Secure token storage"
constraints: 
  - "Must comply with security standards"
  - "Must support OAuth 2.0"
assumptions: 
  - "Users have access to email"
  - "System has secure database"
out_of_scope: 
  - "Biometric authentication"
  - "Two-factor authentication"
created_at: ""
updated_at: ""
status: "draft"
metadata: 
  component: "authentication"
```

## Workflow Templates

Templates for defining common development workflows.

### Development Workflow Template (workflows/development/workflow-template.yaml)
```yaml
id: ""
name: "Development Workflow"
description: "Standard development workflow for feature implementation"
steps:
  - name: "Planning"
    description: "Define requirements and create plan"
    duration: "2 days"
  - name: "Development"
    description: "Implement feature"
    duration: "5 days"
  - name: "Testing"
    description: "Test implementation"
    duration: "2 days"
  - name: "Review"
    description: "Code review and feedback"
    duration: "1 day"
  - name: "Deployment"
    description: "Deploy to production"
    duration: "1 day"
roles:
  - "Developer"
  - "Tester"
  - "Reviewer"
tools:
  - "Git"
  - "CI/CD pipeline"
  - "Testing framework"
```

## Using Templates

### Creating Artifacts from Templates

To create a new artifact from a template:

1. Copy the appropriate template file
2. Fill in the required fields
3. Customize as needed for your specific use case
4. Save in the appropriate directory

### Customizing Templates

Templates can be customized for specific project needs:

1. **Add project-specific fields**: Add fields that are relevant to your project
2. **Modify existing sections**: Adjust sections to match your workflow
3. **Create new template types**: Develop templates for unique project requirements

### Template Validation

Templates are validated to ensure they meet the required structure:

1. **Required fields**: All required fields must be present
2. **Data types**: Fields must contain the correct data types
3. **Status values**: Status fields must use predefined values
4. **Priority values**: Priority fields must use predefined values

## Best Practices

1. **Use appropriate templates**: Select templates that match your project type and requirements

2. **Customize as needed**: Modify templates to fit your specific project needs

3. **Maintain consistency**: Keep templates consistent across the project

4. **Update templates**: Regularly update templates to reflect changes in best practices

5. **Document template changes**: Keep documentation of any template modifications

6. **Version control templates**: Use version control to track template changes

7. **Share templates**: Share useful templates with the team

8. **Validate artifacts**: Use template validation to ensure quality

The template system provides a solid foundation for creating consistent and comprehensive project artifacts while allowing for customization to meet specific project needs.