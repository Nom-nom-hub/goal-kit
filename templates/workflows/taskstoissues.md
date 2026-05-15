---
description: Convert existing tasks into actionable, dependency-ordered GitHub issues for the goal based on available execution artifacts.
tools: ['github/github-mcp-server/issue_write']
scripts:
  sh: scripts/bash/create-tasks.sh --json
  ps: scripts/powershell/create-tasks.ps1 -Json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse GOAL_DIR and AVAILABLE_DOCS list. Extract tasks document path. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load and validate execution context**:
   - Read goal.md, strategies.md, execution.md (or tasks.md if using task-only workflow)
   - Verify tasks.md exists and contains task breakdown table
   - Extract task list with owners, effort estimates, DoD criteria

3. **Validate Tasks Alignment**:
   - Confirm all tasks trace back to execution phases or strategy
   - Verify task dependencies are documented
   - ERROR if critical tasks missing or misaligned

4. **Get repository information**:
   - Run: `git config --get remote.origin.url`
   - **ONLY PROCEED IF THE REMOTE IS A GITHUB URL**
   - Confirm repository matches user's intended target

5. **Validate GitHub Issue Metadata**:
   - Confirm each task has clear acceptance criteria (DoD)
   - Verify task titles are actionable and specific
   - Ensure effort estimates are reasonable (1-5 days per task)
   - ERROR if critical metadata missing or unmeasurable

6. **Create GitHub Issues**:
   - For each task in the task list (in dependency order):
     - Use GitHub MCP server to create a new issue
     - Include: task title, acceptance criteria (DoD), effort estimate, owner assignment
     - Link related issues based on dependencies documented in tasks.md
   - Report issue creation summary with links

**CRITICAL SAFETY RULE**: Do not create issues in repositories that do not match the git remote URL. Validate the remote matches user intent before creating any issues.