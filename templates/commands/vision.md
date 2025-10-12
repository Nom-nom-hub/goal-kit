# /goalkit.vision Command

## AI AGENT INSTRUCTIONS

When processing `/goalkit.vision` requests, follow this structured approach:

### Input Analysis
1. **Extract Core Purpose**: Identify the fundamental mission and desired outcomes from user input
2. **Define Success Metrics**: Convert user descriptions into specific, measurable success criteria
3. **Generate Principles**: Create actionable guiding principles with clear AI application guidance
4. **Align Goals**: Ensure generated goals support the vision and have measurable outcomes

### Processing Framework
- Focus on outcomes over implementation details
- Generate specific, quantifiable success metrics (percentages, timeframes, user counts)
- Create 4-6 actionable principles that guide AI decision-making
- Ensure vision provides foundation for goal-driven development workflow

### Output Structure
Use the template sections below to structure your response. Maintain consistency with existing project context and ensure all sections are populated with actionable content.

---

## Overview

The `/goalkit.vision` command establishes your project's foundational vision, values, and success criteria that will guide all subsequent goal-driven development activities.

## Purpose

This command creates or updates the project's vision document that serves as the foundation for all goal-driven development. Unlike traditional project charters or requirements documents, the vision focuses on outcomes, success metrics, and guiding principles rather than specific features or implementations.

## When to Use

Use `/goalkit.vision` when:
- Starting a new project
- Major strategic shifts in project direction
- Need to realign team around core outcomes
- Establishing principles for goal-driven development

## Input Format

```
/goalkit.vision [description of project vision, values, and success criteria]
```

### Example Input

```
/goalkit.vision Create a vision for a personal productivity application focused on helping users achieve their most important goals with minimal friction. The vision should emphasize user autonomy, measurable progress, and flexible achievement strategies. Include principles for measuring success through user outcomes rather than feature adoption, and establish guidelines for adapting based on user feedback and learning.
```

## Output

The command generates:
- `.goalkit/vision.md` - Complete project vision document
- Project structure optimized for goal-driven development
- Foundation for all subsequent goal definitions

### Agent File Creation Instructions

When processing `/goalkit.vision` commands, AI agents should:
1. Create or update the `.goalkit/vision.md` file in the project root
2. Use the current date in YYYY-MM-DD format for the "Created" field
3. Write the complete vision document using the template structure below
4. After creating the vision file, inform the user that the vision has been established and suggest creating the first goal using `/goalkit.goal`

### File Creation Process
- **Create/Update File**: `.goalkit/vision.md` with the vision content
- **Template**: Use the structure provided in the "Vision Components" section below

## Vision Components

### 1. Project Purpose
- **Core Mission**: Fundamental reason the project exists
- **Vision Statement**: Inspirational description of desired future state
- **Target Outcomes**: Specific outcomes the project seeks to achieve

### 2. Success Metrics
- **Primary Indicators**: Must-achieve success measures
- **Secondary Indicators**: Valuable but not required outcomes
- **Learning Goals**: What to discover through the project

### 3. Guiding Principles
- **Outcome-First Thinking**: Prioritize user/business outcomes over technical preferences
- **Measurable Progress**: All work contributes to measurable success metrics
- **Strategy Flexibility**: Multiple valid approaches exist for any goal
- **Learning Integration**: Implementation as hypothesis testing
- **Adaptive Planning**: Plans as hypotheses, not contracts

### 4. Project Goals
- High-level goals with clear success criteria
- Prioritized based on outcome impact
- Structured for strategy exploration

### 5. Project Scope
- What's included and explicitly excluded
- Outcome-focused boundaries
- Flexibility for learning-based adjustments

## Key Differences from Spec-Driven Development

| Spec-Driven | Goal-Driven |
|-------------|-------------|
| Detailed requirements upfront | High-level outcomes and success criteria |
| Single implementation path | Multiple strategy exploration |
| Feature-focused planning | Outcome-focused milestones |
| Implementation precision | Learning and adaptation |

## Integration with Other Commands

The vision created by `/goalkit.vision` serves as the foundation for:
- **`/goalkit.goal`**: Individual goals must align with project vision
- **`/goalkit.strategies`**: Strategy exploration guided by vision principles
- **`/goalkit.milestones`**: Milestones measured against vision success criteria
- **`/goalkit.execute`**: Execution aligned with vision values and principles

## Best Practices

### Vision Creation
- **Collaborative Input**: Involve key stakeholders in vision development
- **Outcome-Focused Language**: Describe what users achieve, not what features exist
- **Measurable Success**: Define how you'll know the vision is achieved
- **Flexible Principles**: Allow for learning and adaptation

### Vision Evolution
- **Regular Review**: Reassess vision relevance quarterly
- **Learning Integration**: Update based on project learning
- **Stakeholder Alignment**: Maintain stakeholder support for vision
- **Documentation**: Keep vision document current and accessible

## Common Patterns

### Startup Projects
- Focus on user acquisition and engagement metrics
- Emphasize rapid learning and iteration
- Include innovation and market validation goals

### Enterprise Projects
- Focus on business process improvement and efficiency
- Emphasize compliance and risk management
- Include organizational learning objectives

### Open Source Projects
- Focus on community building and contribution quality
- Emphasize sustainability and maintainer experience
- Include ecosystem impact goals