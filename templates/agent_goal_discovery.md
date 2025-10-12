# Goal Discovery for AI Agents

This document provides AI agents with instructions for discovering and working with goals stored in the `.goalkit/` directory, which is typically git-ignored but contains essential goal files.

## Problem Statement

AI agents often struggle to discover existing goals when starting a new conversation because:
1. Goal files are stored in the `.goalkit/goals/` directory
2. This directory is git-ignored for security/privacy reasons
3. Agents have limited visibility into git-ignored directories during conversations

## Solution Approach

AI agents should use the following systematic approach to discover goals:

### 1. File System Exploration Strategy

When a user references a goal but doesn't provide specific details, agents should:

1. Use the `glob` tool to search for goal directories:
   ```
   glob(path="C:\YourProject\.goalkit\goals", pattern="**")
   ```

2. Use the `list_directory` tool to examine the `.goalkit/goals` directory:
   ```
   list_directory(path="C:\YourProject\.goalkit\goals")
   ```

3. Use the `search_file_content` tool to find goal-related information:
   ```
   search_file_content(pattern="goal", include="**/goals/**")
   ```

### 2. User Guidance Strategy

When agents cannot find specific goal information, they should:

1. Politely ask the user for clarification about which goal they want to work with
2. Offer to list available goals if the tools allow discovery
3. Suggest creating a new goal if none exist

### 3. Fallback Discovery Methods

If direct file access fails:

1. Ask the user to specify the goal ID or name
2. Request the user run a `goalkeeper` CLI command to list goals
3. Suggest the user provide the goal information directly

## Implementation Guidelines

### For `/goalkit.plan` Command

When a user requests planning for a specific goal (e.g., "goal 001"):

1. Try to discover existing goals in `.goalkit/goals/` directory
2. If goal 001 exists, proceed with planning
3. If multiple goals exist, ask the user to confirm which one
4. If no goals exist or the specific goal isn't found, ask the user for clarification

### For Other Commands

Apply similar discovery approach for other commands that reference specific goals:
- `/goalkit.execute`
- `/goalkit.milestones`
- `/goalkit.strategies`
- `/goalkit.track`

## Example Discovery Workflow

```
1. Agent receives: "/goalkit.plan goal 001"
2. Agent attempts to discover goals in .goalkit/goals/
3. If goal 001 is found, proceed with planning
4. If not found, ask: "I couldn't find a goal with ID 001 in the .goalkit/goals/ directory. Could you please verify the goal ID? Here are the goals I found: [list goals] or create a new goal first."
5. Once goal is identified, proceed with the requested command
```

## Best Practices for Goal Discovery

1. **Be Transparent**: Always let the user know when you're searching for goal information
2. **Provide Options**: When goals can't be found, offer clear alternatives
3. **Respect Privacy**: Don't expose sensitive goal details that might be in files
4. **Verify Intent**: Confirm with the user when multiple matching goals exist
5. **Error Gracefully**: Handle cases where goal directories don't exist yet

## Integration with Existing Workflows

This discovery mechanism should be integrated into all commands that reference specific goals to ensure consistent user experience across the Goal Kit system.