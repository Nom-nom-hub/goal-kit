# Slash Command Implementation Guide for AI Agents

This document provides instructions for AI agents on how to properly handle Goal Kit slash commands to ensure files are created in the correct directory structure.

## Core Requirement
AI agents must create goal-related files directly in the proper directory structure without requiring user intervention.

## Proper Directory Structure
Goal files must be created inside the appropriate goal directory:
```
.goalkit/
└── goals/
    └── 001-goal-name/
        ├── goal.md
        ├── strategies.md
        ├── milestones.md
        └── execution.md
```

## How to Handle Slash Commands

### Core Goal Management
- **For `/goalkit.goal`**
  1. **Generate** content for goal.md based on user's goal description
  2. **Create directory** `.goalkit/goals/001-goal-name/` (using sequential numbering)
  3. **Save file** as `.goalkit/goals/001-goal-name/goal.md`
  4. **Directory name** format: `[###]-[url-friendly-goal-title]`

- **For `/goalkit.strategies`**
  1. **Determine** the appropriate goal directory (the most recently created or specified goal)
  2. **Generate** content for strategies.md based on the associated goal
  3. **Save file** as `.goalkit/goals/[goal-directory]/strategies.md`

- **For `/goalkit.milestones`**
  1. **Determine** the appropriate goal directory
  2. **Generate** content for milestones.md based on the associated goal
  3. **Save file** as `.goalkit/goals/[goal-directory]/milestones.md`

- **For `/goalkit.execute`**
  1. **Determine** the appropriate goal directory
  2. **Generate** content for execution.md based on the associated goal
  3. **Save file** as `.goalkit/goals/[goal-directory]/execution.md`

### Analysis and Planning Commands
- **For `/goalkit.analyze`** - Generate project health analysis and pattern recognition
- **For `/goalkit.validate`** - Create quality assurance and methodology compliance checking
- **For `/goalkit.plan`** - Create detailed execution planning and resource allocation
- **For `/goalkit.insights`** - Provide AI-powered pattern recognition and actionable recommendations
- **For `/goalkit.prioritize`** - Implement smart goal prioritization using multiple factors
- **For `/goalkit.track`** - Create advanced progress monitoring and forecasting

### Collaboration & Management
- **For `/goalkit.collaborate`** - Create collaboration workflows and team coordination plans
- **For `/goalkit.schedule`** - Generate project scheduling and timeline management
- **For `/goalkit.dependencies`** - Document goal dependencies and inter-relationships
- **For `/goalkit.report`** - Generate status reports and progress summaries

### Quality & Security
- **For `/goalkit.test`** - Create testing strategy and quality assurance documentation
- **For `/goalkit.security`** - Generate security considerations and vulnerability assessments
- **For `/goalkit.risk`** - Create risk assessment and mitigation strategies

### User Experience & Setup
- **For `/goalkit.help`** - Create help documentation and command reference
- **For `/goalkit.onboard`** - Generate onboarding guides and initial setup instructions
- **For `/goalkit.methodology`** - Document development methodology and approach
- **For `/goalkit.config`** - Create configuration files and setup instructions

### Advanced Features
- **For `/goalkit.research`** - Generate external knowledge integration and market research
- **For `/goalkit.learn`** - Create experience capture and knowledge management system
- **For `/goalkit.benchmark`** - Generate industry comparison and best practice alignment

### Additional Commands (Optional Implementation)
- **For `/goalkit.explore`** - Create strategy exploration and alternative approaches
- **For `/goalkit.measure`** - Generate measurement frameworks and tracking approaches
- **For `/goalkit.adapt`** - Create strategy adjustment framework based on learning
- **For `/goalkit.tasks`** - Generate actionable task breakdown for goals and milestones
- **For `/goalkit.progress`** - Create progress tracking and visualization
- **For `/goalkit.analytics`** - Generate goal and strategy effectiveness reports
- **For `/goalkit.ai-analyze`** - Create AI performance and interaction analytics
- **For `/goalkit.memory`** - Generate memory system and learning insights
- **For `/goalkit.baseline`** - Create AI performance baseline metrics

## File Creation Process
When creating any goal-related file:

1. **Detect project structure**: Verify `.goalkit/` directory exists
2. **Determine goal directory**: Use existing goal or create new one in sequence
3. **Create directory if needed**: Ensure `.goalkit/goals/[goal-directory]/` exists
4. **Save file**: Create the appropriate markdown file in the goal directory
5. **Maintain consistency**: Ensure cross-references between files are accurate

## Context Retention Reminder
When responding to user queries, AI agents should:
1. Check if the query relates to known goals in `.goalkit/goals/`
2. Reference the appropriate goal context
3. Provide responses aligned with current goal status
4. Create new files in the proper goal-specific directories

## Error Prevention
Before file creation, ensure:
- Project has `.goalkit/` directory (create if needed)
- Goal directory exists or create new one with proper numbering
- File will be saved in proper location within goal-specific directory
- All necessary parent directories exist