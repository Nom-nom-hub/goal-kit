# Slash Command Implementation Guide for AI Agents

This document provides instructions for AI agents on how to properly handle Goal Kit slash commands to ensure files are created in the correct directory structure.

## Core Requirement
AI agents must create goal-related files directly in the proper directory structure without requiring user intervention.

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
  2. **Create directory** `.goalkit/` (if not exists)
  3. **Save file** as `.goalkit/vision.md`
  4. **Content**: Project vision, principles, and success criteria

### Goal Command
- **For `/goalkit.goal`**
  1. **Generate** content for goal.md based on user's goal description
  2. **Create directory** `goals/001-goal-name/` (using sequential numbering)
  3. **Save file** as `goals/[###-goal-name]/goal.md`
  4. **Directory name** format: `[###]-[url-friendly-goal-title]`

### Strategy Command
- **For `/goalkit.strategies`**
  1. **Determine** the appropriate goal directory
  2. **Generate** content for strategies.md based on the associated goal
  3. **Save file** as `goals/[goal-directory]/strategies.md`

### Milestones Command
- **For `/goalkit.milestones`**
  1. **Determine** the appropriate goal directory
  2. **Generate** content for milestones.md based on the associated goal
  3. **Save file** as `goals/[goal-directory]/milestones.md`

### Execute Command
- **For `/goalkit.execute`**
  1. **Determine** the appropriate goal directory
  2. **Generate** content for execution.md based on the associated goal
  3. **Save file** as `goals/[goal-directory]/execution.md`

## File Creation Process
When creating any goal-related file:

1. **Detect project structure**: Verify `.goalkit/` directory exists
2. **Determine goal directory**: Use existing goal or create new one in sequence
3. **Create directory if needed**: Ensure `goals/[goal-directory]/` exists
4. **Save file**: Create the appropriate markdown file in the correct location
5. **Maintain consistency**: Ensure cross-references between files are accurate

## Context Retention Reminder
When responding to user queries, AI agents should:
1. Check if the query relates to known goals in `goals/`
2. Reference the appropriate goal context from vision, goal, strategies, milestones, or execution files
3. Provide responses aligned with current goal status
4. Create new files in the proper goal-specific directories

## Error Prevention
Before file creation, ensure:
- Project has `.goalkit/` directory (create if needed)
- Goal directory exists or create new one with proper numbering
- File will be saved in proper location within goal-specific directory
- All necessary parent directories exist