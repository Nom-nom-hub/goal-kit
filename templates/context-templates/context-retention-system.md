# Context Retention System for AI Agents

This system enables AI agents to maintain project context across chat sessions by leveraging the Goal Kit markdown structure.

## How It Works

When an AI agent starts a new session in a project with Goal Kit:

1. **Scan Project Directory** for `.goalkit/goals/` folder and any `ai-context.md` file
2. **Load Context Summary** from `ai-context.md` in the project root if it exists
3. **Parse Active Goals** from the goal files listed in the context summary
4. **Read Recent Interaction Logs** if available
5. **Present Current State** to the AI so it can respond with appropriate context

## Context File Locations

- Project context summary: `[project_root]/ai-context.md`
- Goal files: `[project_root]/.goalkit/goals/*/goal.md`
- Strategy files: `[project_root]/.goalkit/goals/*/strategies.md`
- Milestone files: `[project_root]/.goalkit/goals/*/milestones.md`
- Execution files: `[project_root]/.goalkit/goals/*/execution.md`
- Interaction logs: `[project_root]/.goalkit/logs/ai-interaction-*.md` (if implemented)

## Implementation for AI Agents

When an AI agent begins a new session:

```
IF project has `.goalkit/` directory THEN
    1. Load context summary from `ai-context.md` (if exists)
    2. Identify and load active goals from `.goalkit/goals/`
    3. Parse goal metadata including:
        - Goal status (planned, in progress, completed)
        - Current milestone
        - Active strategy
        - Success criteria
    4. Load any recent interaction logs
    5. Combine into context that informs AI responses
END IF
```

## Example Context Summary Format

The ai-context.md file should contain:

```markdown
# AI Context Summary

**Date**: 2025-10-12

## Active Goals
- [001-ai-context-retention](.goalkit/goals/001-ai-context-retention/goal.md) - In Progress
- [002-improve-documentation](.goalkit/goals/002-improve-documentation/goal.md) - Planned

## Active Strategies
- **Goal 001**: Markdown-Based Context Storage Approach
- **Goal 002**: User-Focused Documentation Enhancement

## Current Milestones
- 001: Context Capture and Storage Implementation (due 2025-10-15)
- 002: Documentation Framework Setup (due 2025-10-20)

## Key Information
- **Project**: Goal Kit Framework
- **Team**: Development Team
- **Timeline**: Ongoing
- **Budget**: N/A (Open Source)

## Recent Decisions
1. Using markdown files for context persistence
2. Focusing on goal-based organization
```

## Querying Process

When responding to user queries, AI agents should:

1. Check if the query relates to known goals
2. Reference the appropriate goal context
3. Provide responses aligned with current goal status
4. Update context if new information is provided

## For New Chat Sessions

AI agents should automatically:

1. Detect the presence of a Goal Kit structure
2. Load the current project context
3. Optionally inform the user: "I've loaded your project context with X active goals"
4. Use this context to inform all subsequent responses