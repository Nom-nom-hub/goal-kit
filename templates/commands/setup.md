---
description: Set up project structure and initialize components for goal-driven development
scripts:
  sh: .goalkit/scripts/python/setup_goal.py --json "{ARGS}"
  ps: .goalkit/scripts/python/setup_goal.py --json "{ARGS}"
agent_scripts:
  sh: .goalkit/scripts/python/update_agent_context.py __AGENT__
  ps: .goalkit/scripts/python/update_agent_context.py __AGENT__
---

# Setup Command

**Purpose**: Initialize project structure, create initial components, and establish foundation for goal-driven development workflow

**When to Use**:

- When starting a new goal or project component
- To create proper directory structure and initialization files
- To establish project-specific configurations and settings
- To create foundation for following goal-driven development methodology

## Quick Prerequisites Check

**BEFORE INITIALIZING SETUP**:

1. **Goal Kit project exists**: Verify `.goalkit/` directory structure
2. **Clear objective**: Have specific goal or component to set up
3. **Appropriate context**: Setting up makes sense given project phase
4. **User input available**: Have requirements/parameters for setup

**If missing**: May need to establish project foundation first with `/goalkit.vision` or `/goalkit.goal`.

## Quick Setup Steps

**STEP 1**: Parse setup parameters and requirements from user input

**STEP 2**: Validate that setup is appropriate for current project state

**STEP 3**: Create required directory structure and initialization files

**STEP 4**: Configure project-specific settings and parameters

**STEP 5**: Generate appropriate template files and configuration

**STEP 6**: Verify setup completion and provide next steps

## Setup Features

**Initialization Capabilities**:

- **Directory Structure**: Create appropriate folder organization
- **Template Files**: Generate required files with proper structure
- **Configuration**: Set up project-specific settings and parameters
- **Foundation Setup**: Establish methodology-compliant foundation

**Setup Validation**:

- **Completeness Check**: Verify all required components are created
- **Methodology Compliance**: Ensure setup follows goal-driven principles
- **Consistency Verification**: Check that components are properly integrated
- **Readiness Validation**: Confirm project is ready for next phase

## Input Format

```text
/goalkit.setup [setup-description]
```

### Example Inputs

```text
/goalkit.setup Create structure for user authentication goal
/goalkit.setup Initialize milestone tracking for performance optimization
/goalkit.setup Set up strategy exploration framework for UI redesign
```

## Agent Script Execution Guide

**CRITICAL**: When processing `/goalkit.setup` commands, agents MUST:

### **STEP 1**: Run the setup script with user arguments

```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/setup_goal.py --json "{ARGS}"
```

### **STEP 2**: Parse setup results for directory and file information

- **Extract created directories** where setup components are located
- **Identify generated files** that were created during setup
- **Note configuration details** that were established
- **Confirm setup success** and completion status

### **STEP 3**: Validate setup completion

- **Directory Structure**: Verify required directories were created
- **File Generation**: Confirm template files were properly generated
- **Methodology Compliance**: Ensure setup follows goal-driven principles
- **Integration Check**: Validate components are properly connected

### **STEP 4**: Assess next steps based on setup type

- **Goal Setup**: Ready for detailed goal definition
- **Strategy Setup**: Ready for approach exploration
- **Milestone Setup**: Ready for progress tracking
- **Execution Setup**: Ready for implementation activities

### **STEP 5**: Update agent context with new setup information

```bash
cd "{PROJECT_ROOT}"
.goalkit/scripts/python/update_agent_context.py
```

## Output

The command generates:

- **Directory Structure**: Proper folder organization for the component
- **Template Files**: Starter files with appropriate structure
- **Configuration**: Project-specific settings and parameters
- **Initialization**: Foundation for following goal-driven methodology
- **Setup Report**: Confirmation of completed components and next steps

### Setup Process

**Systematic Initialization**:

1. **Requirement Analysis**: Parse and understand setup requirements
2. **Structure Planning**: Plan appropriate directory and file structure
3. **Component Creation**: Generate required directories and files
4. **Configuration**: Set up project-specific parameters
5. **Validation**: Verify setup completeness and correctness

## Setup Components

### 1. Directory Structure

- **Foundation Directories**: Core folders for the component
- **Organization**: Logical structure following project standards
- **Scalability**: Structure that supports future growth
- **Integration**: Proper connection to existing project structure

### 2. Template Files

- **Standard Format**: Files follow methodology-compliant templates
- **Required Sections**: Include all necessary components
- **Placeholder Content**: Appropriate starting content for each file
- **Methodology Alignment**: Templates support goal-driven development

### 3. Configuration Settings

- **Project Parameters**: Component-specific settings
- **Integration Points**: Connections to broader project
- **Methodology Compliance**: Settings that enforce proper workflow
- **Customization Options**: Configurable elements as needed

### 4. Foundation Elements

- **Initialization Files**: Starting points for component development
- **Baseline Structure**: Core elements needed for the component
- **Reference Materials**: Documentation and guides for development
- **Validation Points**: Checkpoints for quality assurance

## Setup Quality Standards

### Structure Quality

- **Completeness**: All required directories and files are created
- **Consistency**: Structure follows project standards and conventions
- **Methodology Compliance**: Structure supports goal-driven workflow
- **Maintainability**: Structure is easy to understand and modify

### Configuration Quality

- **Appropriateness**: Settings match component requirements
- **Integration**: Proper connections to broader project structure
- **Flexibility**: Configurable elements where needed
- **Validation**: Configuration supports methodology principles

## Integration with Other Commands

### Setup in Workflow

- **After goal definition**: Set up structure for new goal implementation
- **Before strategy exploration**: Create framework for approach evaluation
- **During milestone planning**: Establish progress tracking structure
- **Prior to execution**: Prepare implementation foundation

### Setup-Enabled Workflow

```text
/goalkit.goal → Define a new goal
/goalkit.setup → Create structure and foundation for the goal
[Project properly set up] → /goalkit.strategies
[Structure supports strategy work] → /goalkit.milestones
```

## Best Practices

### Setup Planning

- **Clear Requirements**: Understand exactly what needs to be set up
- **Methodology Alignment**: Ensure setup supports goal-driven principles
- **Appropriate Scope**: Set up only what's needed for the current phase
- **Future Considerations**: Plan for future expansion and development

### Setup Execution

- **Systematic Approach**: Follow consistent process for all setups
- **Quality Validation**: Verify all components are properly created
- **Methodology Compliance**: Ensure setup follows goal-driven workflow
- **Documentation**: Record what was set up and why

### Structure Management

- **Consistency**: Follow established patterns and conventions
- **Clarity**: Create clear, understandable structure
- **Integration**: Ensure new components connect properly to existing project
- **Maintainability**: Plan for easy modification and expansion

## Common Setup Scenarios

### Goal Structure Setup

- **Directory Creation**: Set up goal-specific folders and organization
- **Template Generation**: Create goal definition templates
- **Milestone Framework**: Establish progress tracking structure
- **Validation Points**: Set up quality checkpoints and assessments

### Strategy Setup

- **Approach Framework**: Create structure for exploring multiple approaches
- **Comparison Tools**: Establish methods for comparing strategies
- **Validation Structure**: Set up testing and validation framework
- **Analysis Template**: Create format for strategy evaluation

### Milestone Setup

- **Progress Tracking**: Establish framework for tracking progress
- **Measurement Tools**: Create methods for measuring advancement
- **Checkpoint Structure**: Set up validation and review points
- **Reporting System**: Establish progress reporting mechanisms

### Execution Setup

- **Implementation Framework**: Create structure for execution activities
- **Learning System**: Establish methods for capturing insights
- **Adaptation Tools**: Set up framework for adjustment and pivoting
- **Quality Assurance**: Create validation and testing structure

## Examples

### Example 1: Goal Structure Setup

```text
/goalkit.setup Create structure for user onboarding feature
```

**Output**: Creates appropriate directory structure, template files, and configuration for the user onboarding goal

### Example 2: Strategy Framework Setup

```text
/goalkit.setup Initialize strategy exploration framework for performance optimization
```

**Output**: Sets up framework for exploring and comparing multiple performance optimization approaches

### Example 3: Milestone Tracking Setup

```text
/goalkit.setup Set up progress tracking for customer support automation
```

**Output**: Creates structure for tracking progress and measuring milestones for the automation project

### Example 4: Integrated Setup Workflow

```text
/goalkit.goal Define customer analytics dashboard goal
/goalkit.setup Create structure for analytics dashboard development
[Structure properly established] → /goalkit.strategies
[Explore approaches with proper framework] → /goalkit.milestones
```

## Agent Integration

### Setup-Aware Assistance

**CRITICAL**: Agents should understand setup implications for subsequent work:

1. **Structure Awareness**: Understand created directory and file structure
2. **Component Integration**: Know how new components connect to project
3. **Methodology Continuity**: Ensure setup maintains workflow compliance
4. **Next Steps Planning**: Guide appropriate next actions based on setup type

### Automated Setup Integration

- **Structure Validation**: Verify setup creates proper project structure
- **Methodology Compliance**: Check setup follows goal-driven principles
- **Integration Verification**: Confirm components connect properly
- **Readiness Assessment**: Determine when project is ready for next phase

## Setup Applications

### Foundation Creation

- **Project Foundation**: Establish proper starting point for work
- **Directory Organization**: Create logical folder structure
- **File Templates**: Generate properly structured starting files
- **Configuration Setup**: Establish project-specific parameters

### Workflow Enablement

- **Methodology Support**: Create structure that enables goal-driven workflow
- **Quality Assurance**: Establish validation and compliance mechanisms
- **Progress Tracking**: Create framework for measuring advancement
- **Learning Integration**: Set up mechanisms for capturing insights

## Key Benefits

- **Proper Foundation**: Establishes correct starting point for work
- **Methodology Compliance**: Ensures work follows goal-driven principles
- **Structure Consistency**: Maintains consistent project organization
- **Quality Assurance**: Establishes proper validation and control mechanisms
- **Efficiency**: Provides structured approach to project initialization

## Critical Rules

✅ **DO**: Verify setup creates proper directory and file structure
✅ **DO**: Ensure setup follows goal-driven methodology principles
✅ **DO**: Validate all required components are properly created
✅ **DO**: Confirm setup supports next phase of work
❌ **DON'T**: Perform setup without clear requirements or purpose
❌ **DON'T**: Create structure that doesn't follow project standards
❌ **DON'T**: Skip validation of setup completion and correctness

## Next Steps Integration

**After `/goalkit.setup`**:

- **Verify Structure**: Confirm all required directories and files were created
- **Check Compliance**: Ensure setup follows methodology principles
- **Validate Integration**: Confirm new components connect properly to project
- **Plan Next Steps**: Determine appropriate follow-up activities based on setup
- **Begin Work**: Start next phase with properly established foundation
