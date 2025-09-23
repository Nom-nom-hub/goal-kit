# Goal-Dev-Spec User Guides and Tutorials

This document provides comprehensive user guides and tutorials for common workflows with the Goal-Dev-Spec tool, designed to help users get started quickly and use the tool effectively.

## Overview

These guides and tutorials cover common workflows and scenarios for using Goal-Dev-Spec, from initial setup to advanced usage patterns. Each guide builds upon the previous knowledge and demonstrates how to use the tool effectively for various development scenarios.

## Quick Start Guide

### Getting Started

This guide will help you set up Goal-Dev-Spec and create your first project.

#### Prerequisites

- Python 3.7 or higher
- pip package manager
- Git (recommended)
- Your preferred AI assistant tool (optional but recommended)

#### Installation

Install Goal-Dev-Spec using pip:

```bash
# Clone the repository or download the source
pip install -e .
```

Or run directly without installation:

```bash
# Run directly from the source directory
python -m goal_cli
```

#### Initialize Your First Project

1. Create a new project:

```bash
goal init my-first-project
```

2. The interactive setup will guide you through:
   - Selecting an AI assistant
   - Choosing script type (bash or PowerShell)
   - Creating directory structure
   - Initializing git repository

3. Navigate to your project:

```bash
cd my-first-project
```

4. Create your first goal:

```bash
goal create "Implement user authentication with login and registration"
```

5. List your goals:

```bash
goal list
```

6. View goal details:

```bash
goal show <goal-id>
```

### Complete Project Workflow

This tutorial demonstrates a complete workflow from goal creation to implementation tracking.

#### Step 1: Initialize the Project

```bash
goal init authentication-service --ai claude
cd authentication-service
```

#### Step 2: Create Goals

```bash
# Create the main authentication goal
goal create "Implement secure user authentication service with JWT tokens and role-based access control"

# Create additional goals
goal create "Implement user registration with email verification"
goal create "Implement password reset functionality"
goal create "Implement OAuth2 integration with Google and GitHub"
```

#### Step 3: Analyze Goals with Analytics

```bash
# Get project insights
goal analytics project-insights

# Analyze specific goals
goal analytics analyze-goal <goal-id>
```

#### Step 4: Create Implementation Plans

```bash
# Get goal IDs
goal list

# Create plans for each goal
goal plan <goal-id-1>
goal plan <goal-id-2>
goal plan <goal-id-3>
goal plan <goal-id-4>
```

#### Step 5: Generate Tasks

```bash
# Create tasks for each plan
goal tasks <plan-id-1>
goal tasks <plan-id-2>
goal tasks <plan-id-3>
goal tasks <plan-id-4>
```

#### Step 6: Track Progress

```bash
# View detailed goal information
goal show <goal-id>

# Track overall project progress
goal track
```

## Common Workflows

### Web Application Development

This guide shows how to use Goal-Dev-Spec for web application development projects.

#### Project Setup

1. Initialize the project with web-appropriate templates:

```bash
goal init web-application --ai claude
cd web-application
```

2. Create the main web application goal:

```bash
goal create "Build responsive web application with React frontend and Node.js backend API"
```

#### Frontend Development Workflow

1. Create frontend-specific goals:

```bash
goal create "Implement React components for user dashboard with responsive design"
goal create "Create authentication forms with validation and error handling"
goal create "Build data visualization components with charts and graphs"
```

2. Generate specifications:

```bash
# Each goal automatically creates a specification
# You can enhance specifications if needed
```

3. Use AI assistance for development:

```bash
# Generate code based on specifications
goal code generate <spec-id>

# Review existing code
goal code review src/components/Dashboard.jsx
```

#### Backend Development Workflow

1. Create backend-specific goals:

```bash
goal create "Implement JWT-based authentication API endpoints"
goal create "Create RESTful API endpoints for user management"
goal create "Design and implement database schema for user data"
```

2. Use governance features:

```bash
# Initialize governance
goal governance init

# Check compliance
goal governance compliance

# Validate artifacts
goal governance validate --type goal --id <goal-id>
```

#### Quality Assurance

1. Set up quality checks:

```bash
# Run quality checks
goal quality run-checks

# Generate quality report
goal quality generate-report

# Run tests
goal test run-tests

# Generate coverage report
goal test coverage-report
```

### API Service Development

This guide demonstrates using Goal-Dev-Spec for API service development.

#### Project Setup

```bash
goal init api-service --ai gemini
cd api-service
```

#### API Design Workflow

1. Create API design goals:

```bash
goal create "Design RESTful API for e-commerce platform with CRUD operations for products"
goal create "Implement GraphQL API for customer data with complex querying capabilities"
goal create "Create API documentation and specifications following OpenAPI standards"
```

#### Implementation Planning

1. Plan each API component:

```bash
goal plan <api-design-goal-id>
goal plan <graphql-goal-id>
goal plan <documentation-goal-id>
```

2. Generate tasks:

```bash
goal tasks <plan-id-1>
goal tasks <plan-id-2>
goal tasks <plan-id-3>
```

#### Testing Strategy

1. Generate test plans:

```bash
goal test generate-plan <goal-id>
```

2. Run comprehensive tests:

```bash
goal test run-tests
```

3. Monitor API performance:

```bash
goal monitor performance-metrics
```

### Data Science Project

This guide shows how to use Goal-Dev-Spec for data science projects.

#### Project Setup

```bash
goal init data-science-project --ai qwen
cd data-science-project
```

#### Data Science Workflow

1. Create data science goals:

```bash
goal create "Develop machine learning model to predict customer churn with 90%+ accuracy"
goal create "Create data pipeline for real-time customer behavior analysis"
goal create "Build interactive dashboard for data visualization and reporting"
```

2. Plan data science processes:

```bash
goal plan <ml-model-goal-id>
goal plan <data-pipeline-goal-id>
goal plan <dashboard-goal-id>
```

#### Model Development

1. Use AI assistance for model development:

```bash
goal code generate <spec-id>
```

2. Track model performance:

```bash
goal analytics project-insights
```

3. Ensure quality with governance:

```bash
goal governance quality
```

### Mobile Application Development

This guide covers using Goal-Dev-Spec for mobile application development.

#### Project Setup

```bash
goal init mobile-app --ai cursor
cd mobile-app
```

#### Mobile App Workflow

1. Create mobile-specific goals:

```bash
goal create "Develop native iOS application with Swift and SwiftUI"
goal create "Create cross-platform React Native app with native performance"
goal create "Implement offline-first architecture with local data synchronization"
```

2. Plan mobile development:

```bash
goal plan <ios-app-goal-id>
goal plan <react-native-goal-id>
goal plan <offline-architecture-goal-id>
```

3. Generate platform-specific tasks:

```bash
goal tasks <plan-id>
```

## Advanced Tutorials

### Integration with AI Agents

This tutorial demonstrates how to effectively integrate and use different AI agents.

#### Setting Up AI Agent Integration

1. During project initialization, select your preferred AI agent:

```bash
goal init ai-integration --ai claude
```

2. Or specify the agent in configuration:

```yaml
# goal.yaml
project:
  name: "AI Integration Project"
  
settings:
  default_agent: "claude"
```

#### Using AI for Code Generation

1. Generate code based on specifications:

```bash
goal code generate <spec-id>
```

2. Review and refactor existing code:

```bash
goal code review src/main.py
goal code refactor src/legacy.py
```

3. Explain complex code blocks:

```bash
goal code explain src/complex-algorithm.py
```

#### Leveraging AI for Specification Creation

1. Create goals with AI assistance for detailed specifications:

```bash
goal create "Implement secure payment processing with Stripe integration and fraud detection"
```

2. Use AI to enhance specifications:

```bash
# The system automatically applies predictive analytics during goal creation
```

### Governance and Compliance Tutorial

This tutorial covers implementing governance and compliance in your projects.

#### Setting Up Governance

1. Initialize governance system:

```bash
goal governance init
```

2. Review the generated constitution:

```yaml
# .goal/governance/constitution.yaml
project:
  name: "My Project"
  version: "1.0.0"
  description: "Project description"
  
governance:
  approvers:
    - name: "Lead Developer"
      role: "Technical Lead"
    - name: "Product Manager"
      role: "Product Lead"
  
  policies:
    - name: "Coding Standards"
      description: "Adherence to coding standards and best practices"
      required: true
    - name: "Security Policies"
      description: "Compliance with security policies and practices"
      required: true
```

#### Compliance Checking

1. Check overall compliance:

```bash
goal governance compliance
```

2. Validate specific artifacts:

```bash
goal governance validate --type goal --id <goal-id>
```

3. Run security scans:

```bash
goal governance security
```

4. Generate governance reports:

```bash
goal governance report
```

### Quality Assurance Workflow

This tutorial demonstrates setting up and using quality assurance features.

#### Quality Gate Setup

1. Set quality thresholds:

```bash
goal quality set-thresholds
```

2. Run quality checks:

```bash
goal quality run-checks
```

3. Generate quality reports:

```bash
goal quality generate-report
```

#### Testing Integration

1. Generate test plans:

```bash
goal test generate-plan <goal-id>
```

2. Run comprehensive tests:

```bash
goal test run-tests
```

3. Check test coverage:

```bash
goal test coverage-report
```

### Automation and CI/CD Tutorial

This tutorial shows how to set up automation and CI/CD pipelines.

#### Setting Up Workflows

1. Set up an automation workflow:

```bash
goal automate setup-workflow deployment
```

2. Schedule regular tasks:

```bash
goal automate schedule-task "0 2 * * *" backup-project
```

3. Run workflows:

```bash
goal automate run-workflow deployment
```

#### CI/CD Pipeline Setup

1. Set up a CI/CD pipeline:

```bash
goal cicd setup-pipeline github-actions
```

2. Check pipeline status:

```bash
goal cicd pipeline-status
```

3. Run pipeline manually:

```bash
goal cicd run-pipeline main
```

## Best Practices

### Project Organization

1. **Start with clear goals**: Define specific, measurable goals before implementation
2. **Use consistent naming**: Follow naming conventions for goals and specifications
3. **Maintain project structure**: Keep artifacts in their appropriate directories
4. **Document decisions**: Use the template system for comprehensive documentation
5. **Regular reviews**: Conduct regular reviews of goals and specifications

### Quality Management

1. **Set quality gates early**: Establish quality standards at the beginning
2. **Automate validation**: Use automated quality checks and validation
3. **Maintain test coverage**: Ensure adequate test coverage for all components
4. **Review regularly**: Conduct regular code and specification reviews
5. **Track metrics**: Monitor quality metrics over time

### Team Collaboration

1. **Define roles and responsibilities**: Use governance features to define team roles
2. **Establish approval processes**: Set up approval workflows for important changes
3. **Maintain communication**: Use notification features to keep team informed
4. **Share knowledge**: Use the documentation system to share project knowledge
5. **Track progress**: Use progress tracking to keep everyone aligned

### Tool Integration

1. **Leverage AI agents**: Use AI assistance to accelerate development
2. **Set up automation**: Automate repetitive tasks and workflows
3. **Integrate CI/CD**: Set up continuous integration and deployment
4. **Monitor continuously**: Use monitoring features to track performance
5. **Secure processes**: Implement security scanning and compliance checking

## Troubleshooting Common Issues

### Goal Creation Issues

**Problem**: Goal creation fails with validation errors
**Solution**: Ensure goal descriptions are detailed and specific

```bash
# Instead of a vague description:
goal create "Build app"

# Use a specific description:
goal create "Build React web application with user authentication and CRUD operations for blog posts"
```

### Governance Validation Failures

**Problem**: Governance validation fails
**Solution**: Check that all required fields are present in artifacts

### Quality Check Failures

**Problem**: Quality checks fail
**Solution**: Address issues identified in quality reports before proceeding

### Automation Workflow Issues

**Problem**: Automation workflows fail
**Solution**: Check workflow configuration and ensure all required resources are available

## Getting Help

### Command Help

For detailed help on any command:

```bash
goal --help                 # General help
goal <command> --help      # Command-specific help
goal <command> <subcommand> --help  # Subcommand help
```

### Documentation

- Check the documentation files in the `docs/` directory
- Review configuration files in the project's `.goal/` directory
- Look up specific feature documentation based on the API reference

### Troubleshooting Commands

```bash
# Check project structure
ls -la

# Verify installation
python -c "from goal_cli import main; print('Installation OK')"

# Check for errors in the most recently created artifacts
goal list
```

These user guides and tutorials should provide a comprehensive foundation for using Goal-Dev-Spec effectively across various project types and scenarios.