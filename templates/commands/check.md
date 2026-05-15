---
description: Verify that all required tools and dependencies are installed for the Goalkit project.
handoffs: []
scripts: {}
---

## User Input

```text
$ARGUMENTS
```

## Outline

The `/goalkit.check` command verifies the development environment is properly set up.

1. **Run the check**: Execute the check command to verify tool availability:
   - Runs automatically when user types `/goalkit.check`
   - Checks for: git, AI assistant CLI tools, VS Code variants
   - Reports results for each tool

2. **Review results**:
   - Green checkmarks indicate installed tools
   - Red X marks indicate missing tools
   - Tips provided for missing critical tools

3. **Take action on findings**:
   - If all tools pass → Environment is ready
   - If git is missing → Recommend installing git
   - If no AI assistants found → Recommend installing an AI assistant
   - If specific agent is missing → Recommend installing that agent

## When to Use

- **First time setup**: After `goalkit init`, verify the environment
- **Environment changes**: After switching machines or reinstalling tools
- **Troubleshooting**: Before debugging tool-specific issues
- **CI/CD validation**: Ensure build agents have required tools
