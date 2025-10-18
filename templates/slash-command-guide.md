# Slash Command Implementation Guide for AI Agents

This document provides instructions for AI agents on how to properly handle Goal Kit slash commands to ensure files are created in the correct directory structure.

## Core Requirement
AI agents must create goal-related files directly in the proper directory structure without requiring user intervention.

## Task Complexity Assessment
Before starting any development work, AI agents must assess the complexity of the requested task:

### Simple Tasks (Direct Implementation)
Use for small enhancements or fixes that don't need the full methodology:
- Visual improvements (e.g., "enhanced header", "better styling")
- Minor bug fixes
- Small UI adjustments
- Simple configuration changes
- For these tasks, **SKIP** the full goal-driven process and implement directly using `/goalkit.execute` or simple code modifications

### Complex Goals (Full Methodology)
Use the complete 5-step process for substantial features:
- New major functionality
- System architecture changes
- Complex user workflows
- Features requiring measurable success criteria
- When user specifies goals with success metrics

## Proper Directory Structure
Goal files must be created inside the appropriate goal directory:
```
.goalkit/
├── vision.md
└── goals/
    └── 001-goal-name/
        ├── goal.md
        ├── strategies.md
        ├── milestones.md
        └── execution.md
```

## How to Handle Core Slash Commands

### Vision Command
- **For `/goalkit.vision`**
  1. **Generate** content for vision.md based on user's vision statement
  2. **Create directory** `.goalkit/` (if not exists) in the PROJECT ROOT
  3. **Save file** as `.goalkit/vision.md` in the PROJECT ROOT
  4. **Content**: Project vision, principles, and success criteria

### Goal Command
- **For `/goalkit.goal`**
  1. **Generate** content for goal.md based on user's goal description
  2. **Create directory** `.goalkit/goals/001-goal-name/` (using sequential numbering) in the PROJECT ROOT
  3. **Save file** as `.goalkit/goals/[###-goal-name]/goal.md` in the PROJECT ROOT
  4. **Directory name** format: `[###]-[url-friendly-goal-title]`

### Strategy Command
- **For `/goalkit.strategies`**
  1. **Determine** the appropriate goal directory in `.goalkit/goals/`
  2. **Generate** content for strategies.md based on the associated goal
  3. **Save file** as `.goalkit/goals/[goal-directory]/strategies.md` in the PROJECT ROOT

### Milestones Command
- **For `/goalkit.milestones`**
  1. **Determine** the appropriate goal directory in `.goalkit/goals/`
  2. **Generate** content for milestones.md based on the associated goal
  3. **Save file** as `.goalkit/goals/[goal-directory]/milestones.md` in the PROJECT ROOT

### Execute Command
- **For `/goalkit.execute`**
  1. **Determine** the appropriate goal directory in `.goalkit/goals/`
  2. **Generate** content for execution.md based on the associated goal
  3. **Save file** as `.goalkit/goals/[goal-directory]/execution.md` in the PROJECT ROOT

## File Creation Process
When creating any goal-related file:

1. **Detect project structure**: Verify `.goalkit/` directory exists in the PROJECT ROOT
2. **Determine goal directory**: Use existing goal or create new one in sequence in `.goalkit/goals/`
3. **Create directory if needed**: Ensure `.goalkit/goals/[goal-directory]/` exists in the PROJECT ROOT
4. **Save file**: Create the appropriate markdown file in the correct location in the PROJECT ROOT
5. **Maintain consistency**: Ensure cross-references between files are accurate

## Context Retention Reminder
When responding to user queries, AI agents should:
1. Check if the query relates to known goals in `.goalkit/goals/`
2. Reference the appropriate goal context from vision, goal, strategies, milestones, or execution files in `.goalkit/`
3. Provide responses aligned with current goal status
4. Create new files in the proper `.goalkit/goals/` directory structure

## Error Prevention
Before file creation, ensure:
- Project has `.goalkit/` directory in the PROJECT ROOT (create if needed)
- Goal directory exists in `.goalkit/goals/` or create new one with proper numbering
- File will be saved in proper location within `.goalkit/goals/` directory structure
- All necessary parent directories exist in the PROJECT ROOT
- Avoid creating double-prefixed directories like `.goalkit.goalkit/` - always use `.goalkit/` in the PROJECT ROOT