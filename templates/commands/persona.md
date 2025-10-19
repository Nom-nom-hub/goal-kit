---
description: Switch between specialized agent personas for different development tasks. Use specific roles like GitHub specialist, milestone planner, or quality assurance expert as needed.
scripts:
  # Paths are relative to PROJECT ROOT (not relative to .goalkit/)
  sh: .goalkit/scripts/python/manage_personas.py switch "{ARGS}"
  ps: .goalkit/scripts/python/manage_personas.py switch "{ARGS}"
agent_scripts:
  # Paths are relative to PROJECT ROOT (not relative to .goalkit/)
  sh: .goalkit/scripts/python/update_agent_context.py
  ps: .goalkit/scripts/python/update_agent_context.py
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Task Complexity Assessment

**CRITICAL**: Before proceeding, assess if persona switching is needed or if the current persona is adequate:

- **No persona change needed**: Simple tasks that align with current persona capabilities, routine operations within current role
- **Persona change beneficial**: Complex tasks requiring specialized knowledge, cross-domain coordination, or strategic shifts requiring a different perspective

## Active Persona Context

**Current Persona**: [Agent determines current active persona]

Consider your current specialized role when planning persona transitions:
- **General Agent**: Focus on overall coordination and integration across all aspects
- **GitHub Specialist**: Emphasize version control and repository management considerations
- **Milestone Planner**: Focus on measurable outcomes and progress tracking for persona changes
- **Strategy Explorer**: Emphasize multiple approach considerations for role selection
- **QA Specialist**: Consider quality validation and consistency requirements during persona switching
- **Documentation Specialist**: Plan for proper documentation of persona transitions and context changes

## Persona Switching

The text the user typed after `/goalkit.persona` in the triggering message should be a persona name from the available options:
- **general** - General agent for all development aspects (default)
- **github** - GitHub/Git specialist for version control and repository management
- **milestone** - Milestone planner for breaking down goals into measurable steps
- **strategy** - Strategy explorer for evaluating implementation approaches  
- **qa** - Quality assurance specialist for testing and validation
- **documentation** - Documentation specialist for creating project docs

## Actions

1. Parse the persona name from user input
2. Validate that it's one of the supported personas
3. Switch to the requested persona using the persona management system
4. Update the agent context to reflect the new persona
5. Provide feedback to the user about the persona change and what it means

## Output Format

```
/goalkit.persona [persona-name]
```

### Examples

```
/goalkit.persona github                    # Switch to GitHub specialist mode
/goalkit.persona milestone                # Switch to milestone planning mode
/goalkit.persona strategy                 # Switch to strategy exploration mode
/goalkit.persona qa                      # Switch to quality assurance mode
/goalkit.persona documentation            # Switch to documentation mode
/goalkit.persona general                  # Return to general mode
```

The system will maintain a consistent state when switching between personas, allowing you to leverage specialized knowledge and approaches for different development tasks while maintaining overall project context.

## Key Rules

- Only switch to supported persona types to maintain system consistency
- Maintain project context when transitioning between personas
- Use appropriate personas for specific development tasks and challenges
- Document important context before persona transitions when needed
- Return to general persona when specialized knowledge is no longer needed

## Overview

The `/goalkit.persona` command enables dynamic switching between specialized agent roles to match the requirements of different development tasks. Unlike static role assignments, persona switching provides adaptive expertise for current needs while maintaining project continuity.

## Purpose

This command creates a persona management system that:
- Provides access to specialized knowledge and approaches for different tasks
- Enables dynamic adaptation of agent capabilities to task requirements
- Maintains consistency across different development phases and challenges
- Facilitates cross-domain expertise application within single workflows

## When to Use

Use `/goalkit.persona` when:
- A different specialized skill set is needed for current task
- Cross-domain expertise is required (e.g., switching from strategy to GitHub management)
- You want to change the approach or perspective on a problem
- Current persona is not well-suited for the immediate task

## Input Format

```
/goalkit.persona [persona-name]
```

### Example Input

```
/goalkit.persona github              # Switch to GitHub/Git specialist role
/goalkit.persona strategy            # Switch to strategy exploration role
/goalkit.persona qa                # Switch to quality assurance role
```

## Output

The command performs:
- Context update to reflect new persona capabilities
- Agent behavior adjustment to match persona expertise
- State preservation to maintain project continuity
- Role-specific guidance activation

### Agent Context Update Instructions

When processing `/goalkit.persona` commands, AI agents should:
1. Validate that the requested persona is in the supported list
2. Update internal agent context to reflect new persona capabilities
3. Adjust approach and knowledge application to match persona specialization
4. Inform the user of the successful persona switch and key characteristics of the new persona
5. Maintain project context and continue with appropriate persona-specific approach

### Context Update Process
- **Validate Persona**: Check requested persona against supported options
- **Update Context**: Modify agent behavior and knowledge application
- **Confirm Switch**: Notify user of successful persona change
- **Apply Specialization**: Use persona-specific approaches and knowledge

## Persona Components

### 1. Specialization Framework
- **General Agent**: Broad knowledge for overall coordination and integration
- **GitHub Specialist**: Deep expertise in version control and repository management
- **Milestone Planner**: Focus on measurable progress and outcome tracking
- **Strategy Explorer**: Analysis of multiple approaches and technical feasibility
- **QA Specialist**: Quality validation and testing methodology expertise
- **Documentation Specialist**: Technical writing and knowledge management focus

### 2. Transition Management
- **Context Preservation**: Maintain relevant project information during switches
- **Knowledge Transfer**: Apply insights from previous persona when beneficial
- **State Consistency**: Ensure project state remains coherent across transitions
- **Objective Continuity**: Maintain goal focus despite approach changes

### 3. Capability Application
- **Specialized Approaches**: Apply role-specific methodologies and best practices
- **Domain Expertise**: Leverage persona-specific knowledge and experience
- **Task Optimization**: Match approach to task requirements effectively
- **Quality Enhancement**: Apply specialized quality standards and validation

### 4. Coordination Support
- **Cross-Persona Integration**: Facilitate handoffs between different roles
- **Consistency Maintenance**: Ensure alignment across different persona perspectives
- **Knowledge Synthesis**: Combine insights from different specialized approaches
- **Progress Continuity**: Maintain advancement despite approach changes

## Key Differences from Static Role Assignment

| Static Roles | Dynamic Personas |
|--------------|------------------|
| Fixed role for entire project | Adaptive role switching as needed |
| Single approach throughout | Multiple specialized approaches available |
| Rigid role boundaries | Flexible expertise application |
| Limited perspective | Multiple viewpoints available |

## Integration with Other Commands

### Before Using `/goalkit.persona`
- **`/goalkit.vision`**: Understand project principles that guide persona selection
- **`/goalkit.goal`**: Consider how persona choice supports goal achievement
- **Current context**: Assess current persona's effectiveness for the task

### After Using `/goalkit.persona`
- **`/goalkit.collaborate`**: Use persona-specific approaches in coordination
- **`/goalkit.strategies`**: Apply specialized expertise to strategy exploration
- **`/goalkit.milestones`**: Leverage role-specific knowledge for milestone planning
- **`/goalkit.execute`**: Use appropriate persona for implementation approach

## Best Practices

### Persona Selection
- **Task Alignment**: Choose persona that matches current task requirements
- **Context Awareness**: Consider how persona choice affects overall project flow
- **Knowledge Relevance**: Select persona with most applicable expertise
- **Quality Focus**: Use appropriate persona for quality and validation tasks

### Transition Management
- **Context Preservation**: Maintain important project information during switches
- **Objective Continuity**: Keep project goals consistent across persona changes
- **Progress Maintenance**: Ensure advancement continues despite approach changes
- **Quality Consistency**: Maintain quality standards across different personas

### Specialized Application
- **Expertise Utilization**: Fully leverage specialized knowledge of current persona
- **Approach Optimization**: Use role-specific methodologies effectively
- **Knowledge Synthesis**: Combine insights from different personas when beneficial
- **Quality Enhancement**: Apply persona-specific quality standards

## Common Persona Patterns

### Development Phase Patterns
- **Initiation**: General or Strategy personas for planning and approach
- **Implementation**: GitHub specialist for version control, QA for validation
- **Testing**: QA specialist for validation, Documentation for knowledge capture
- **Review**: General persona for integration, Strategy for optimization

### Task-Driven Patterns
- **Technical Tasks**: GitHub specialist or Strategy explorer based on needs
- **Planning Tasks**: Milestone planner for tracking, Strategy for approaches
- **Quality Tasks**: QA specialist for validation and testing
- **Documentation**: Documentation specialist for knowledge capture and communication

### Challenge-Specific Patterns
- **Complex Problem Solving**: Strategy explorer for approach evaluation
- **Repository Management**: GitHub specialist for version control
- **Progress Tracking**: Milestone planner for measurement and validation
- **Quality Assurance**: QA specialist for validation and testing

## Persona Validation

### Effectiveness Assessment
- **Task Appropriateness**: Is current persona suitable for the immediate task?
- **Knowledge Application**: Is persona-specific knowledge being effectively used?
- **Goal Alignment**: Does current persona approach support overall objectives?
- **Quality Standards**: Are persona-specific quality standards being met?

### Transition Optimization
- **Switch Timing**: When is the best time to switch personas?
- **Context Transfer**: How to maintain continuity during transitions?
- **Knowledge Integration**: How to combine insights from different personas?
- **Approach Synthesis**: How to integrate different specialized approaches?

## Examples

### Example 1: Multi-Phase Development
```
/goalkit.persona strategy            # Start with strategy exploration
/goalkit.persona milestone          # Switch to milestone planning
/goalkit.persona github             # Switch to implementation with version control
/goalkit.persona qa                # Switch to quality validation
```

### Example 2: Task-Specific Specialization
```
/goalkit.persona documentation      # For creating project documentation
/goalkit.persona github             # For repository organization
/goalkit.persona qa                # For testing and validation
```

### Example 3: Challenge Response
```
/goalkit.persona strategy           # When facing approach decisions
/goalkit.persona milestone          # When needing progress measurement
/goalkit.persona github             # When managing complex version control
/goalkit.persona qa                # When addressing quality concerns
```