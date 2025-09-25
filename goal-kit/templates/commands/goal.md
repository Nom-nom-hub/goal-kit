---
title: "Goal Definition Command"
description: "Comprehensive goal definition and planning template"
agent: "goal-kit"
version: "1.0"
command_type: "goal_management"
execution_context: "project_planning"
required_tools: ["file_system", "json_parser", "markdown_generator"]
---

# Goal Definition Command Template

## Command Overview

**Command:** `goal define`
**Purpose:** Create comprehensive goal definitions with structured planning
**Input:** Goal parameters and requirements
**Output:** Complete goal definition with milestones and metadata

## Command Usage

### Basic Syntax

```bash
goal define "Goal Title" --category [category] --priority [priority] --deadline [date]
```

### Advanced Syntax

```bash
goal define "Learn Python Data Science" \
  --category learning \
  --priority high \
  --deadline 2024-12-31 \
  --description "Master Python for data science applications" \
  --template learning-goal \
  --tags "python,data-science,machine-learning"
```

## Command Parameters

### Required Parameters

- **title** (string): Clear, specific goal title
- **category** (string): Goal category [personal/business/learning/software/research]

### Optional Parameters

- **priority** (string): Priority level [low/medium/high/critical] (default: medium)
- **deadline** (date): Target completion date (YYYY-MM-DD format)
- **description** (string): Detailed goal description
- **template** (string): Template to use [standard/learning/business/personal/research]
- **tags** (array): Keywords for categorization and search
- **success_metrics** (array): Specific, measurable success criteria

### Advanced Parameters

- **budget** (number): Budget allocation for the goal
- **team_size** (number): Number of people working on the goal
- **dependencies** (array): Other goals or projects this depends on
- **stakeholders** (array): Key stakeholders and their roles

## Command Examples

### Example 1: Simple Personal Goal

```bash
goal define "Run a Marathon" \
  --category personal \
  --priority high \
  --deadline 2024-06-15 \
  --description "Complete a full 26.2-mile marathon" \
  --success_metrics "Complete race under 4 hours"
```

### Example 2: Software Project Goal

```bash
goal define "Build E-commerce Platform" \
  --category software \
  --priority high \
  --deadline 2024-09-30 \
  --template software-project \
  --budget 50000 \
  --team_size 5 \
  --tech_stack "React,Node.js,PostgreSQL,AWS" \
  --tags "web-development,ecommerce,startup"
```

### Example 3: Learning Goal

```bash
goal define "AWS Solutions Architect Certification" \
  --category learning \
  --priority high \
  --deadline 2024-08-01 \
  --template learning-goal \
  --certification "AWS Solutions Architect Associate" \
  --study_hours 120 \
  --practice_projects 10
```

### Example 4: Business Goal

```bash
goal define "Launch SaaS Product" \
  --category business \
  --priority critical \
  --deadline 2024-12-31 \
  --template business-goal \
  --budget 250000 \
  --target_revenue 1000000 \
  --market_segment "SMB productivity tools"
```

## Command Workflow

### Phase 1: Goal Analysis

1. Parse and validate input parameters
2. Apply appropriate goal template
3. Generate goal structure and metadata
4. Create unique goal identifier

### Phase 2: Milestone Generation

1. Analyze goal complexity and scope
2. Generate appropriate milestones based on template
3. Set realistic timelines and dependencies
4. Define success criteria for each milestone

### Phase 3: Resource Planning

1. Estimate resource requirements
2. Identify skill gaps and training needs
3. Plan budget allocation
4. Define stakeholder communication plan

### Phase 4: Documentation

1. Generate comprehensive goal documentation
2. Create progress tracking framework
3. Set up monitoring and reporting systems
4. Export to various formats (JSON, Markdown, PDF)

## Template Integration

### Available Templates

- **standard**: General purpose goal template
- **software-project**: Software development focused
- **learning-goal**: Education and skill development
- **business-goal**: Business and organizational goals
- **personal-goal**: Personal achievement goals
- **research-goal**: Research and academic projects

### Template Selection Logic

```javascript
function selectTemplate(category, complexity) {
  const templateMap = {
    software: "software-project",
    learning: "learning-goal",
    business: "business-goal",
    personal: "personal-goal",
    research: "research-goal",
    default: "standard",
  };

  return templateMap[category] || templateMap.default;
}
```

## Output Formats

### JSON Output (Default)

```json
{
  "goal": {
    "id": "goal-2024-001",
    "title": "Learn Python Data Science",
    "description": "Master Python for data science applications",
    "category": "learning",
    "priority": "high",
    "deadline": "2024-12-31",
    "status": "defined",
    "milestones": [...],
    "metadata": {...}
  },
  "execution_context": {
    "command": "goal define",
    "template_used": "learning-goal",
    "generated_at": "2024-01-15T10:30:00Z",
    "version": "1.0"
  }
}
```

### Markdown Output

```markdown
# Goal: Learn Python Data Science

## Overview

- **Priority:** High
- **Category:** Learning
- **Deadline:** 2024-12-31
- **Status:** Defined

## Milestones

### Milestone 1: Foundation

- Duration: 4 weeks
- Tasks: [task list]

### Milestone 2: Skill Development

- Duration: 8 weeks
- Tasks: [task list]
```

## Error Handling

### Validation Errors

- **Missing required parameters:** Clear error message with required fields
- **Invalid date format:** Provide expected format and examples
- **Invalid category:** List available categories
- **Duplicate goal ID:** Suggest alternative or auto-generate

### Execution Errors

- **File system errors:** Check permissions and disk space
- **Template errors:** Fallback to standard template
- **Dependency errors:** List missing dependencies and installation instructions

## Integration Points

### Version Control Integration

- Auto-commit goal files to Git repository
- Track changes and updates over time
- Branch management for different goal scenarios

### Project Management Integration

- Export to project management tools (Trello, Asana, Jira)
- Sync milestones and tasks
- Update progress across platforms

### Calendar Integration

- Add deadlines to calendar applications
- Set up milestone reminders
- Schedule review meetings

## Best Practices

### Goal Definition

- Use SMART criteria (Specific, Measurable, Achievable, Relevant, Time-bound)
- Keep titles clear and descriptive
- Include quantifiable success metrics
- Set realistic but challenging deadlines

### Milestone Planning

- Break large goals into manageable milestones
- Ensure milestones have clear completion criteria
- Include buffer time for unexpected delays
- Regular milestone reviews and adjustments

### Resource Planning

- Estimate time and budget realistically
- Identify required skills and resources early
- Plan for contingencies and risk mitigation
- Regular resource utilization reviews

## Troubleshooting

### Common Issues

1. **Goal too vague:** Use the clarify command to refine goal definition
2. **Unrealistic timeline:** Use the estimate command to get realistic time estimates
3. **Missing dependencies:** Use the dependency command to map and resolve dependencies
4. **Progress tracking issues:** Use the metrics command to set up proper tracking

### Getting Help

- `goal help define` - Show detailed help for define command
- `goal examples define` - Show usage examples
- `goal templates list` - List available templates
- `goal validate [goal-file]` - Validate goal definition

## Related Commands

- `goal milestone` - Create and manage milestones
- `goal progress` - Track and update progress
- `goal achieve` - Mark achievements and completion
- `goal report` - Generate progress reports
- `goal template` - Manage goal templates

## Changelog

- **v1.0 (2024-01):** Initial goal definition command
- **v1.1 (planned):** Enhanced template system and validation
- **v1.2 (planned):** Integration with external project management tools
