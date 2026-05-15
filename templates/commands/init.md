---
description: Initialize a new Goal Kit project. Sets up project structure, AI assistant configuration, git repo, and downloads the latest templates.
handoffs:
  - label: Vision
    agent: goalkit.vision
    prompt: Establish project vision and principles
    send: true
scripts:
  sh: scripts/bash/create-new-goal.sh --json "{PROJECT_NAME}"
  ps: scripts/powershell/create-new-goal.ps1 -Json "{PROJECT_NAME}"
---

## User Input

- **Project Name**: Name for the new project directory (or use `--here` for current directory)
- **AI Assistant**: Claude, Gemini, Copilot, Cursor, Qwen, OpenCode, Codex, Windsurf, Kilocode, or Q
- **Script Type**: Shell (bash/zsh) or PowerShell

## Execution Flow

1. **Pre-flight Checks** (2 min)
   - Validate project name (no special chars, reserved names)
   - Check disk space (≥100MB) and path writeability
   - Check for git availability

2. **Select AI Assistant** (1 min)
   - Default: copilot; user can choose from all supported agents
   - Optionally verify agent CLI is installed (skip with `--ignore-agent-tools`)

3. **Template Download** (1 min)
   - Fetch latest release from GitHub (or use `--skip-tls` for self-signed certs)
   - Download and extract template archive
   - Copy scripts and command templates to `.goalkit/`

4. **Finalization** (1 min)
   - Create agent-specific config files (`.claude/`, `.github/`, etc.)
   - Initialize git repo (skip with `--no-git`)
   - Ensure scripts are executable

## Output

- `.goalkit/` directory with project configuration
- Agent-specific command files for `/goalkit.*` commands
- Initial git commit (if git available)
- "Next Steps" guide showing available slash commands
