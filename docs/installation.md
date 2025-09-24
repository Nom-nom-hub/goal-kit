# Installation Guide

## Prerequisites

- **Linux/macOS** (or Windows; PowerShell scripts now supported without WSL)
- AI coding agent: [Claude Code](https://www.anthropic.com/claude-code), [GitHub Copilot](https://code.visualstudio.com/), [Gemini CLI](https://github.com/google-gemini/gemini-cli), [Cursor](https://cursor.sh/), [Qwen Code](https://github.com/QwenLM/qwen-code), [opencode](https://opencode.ai/), [Codex CLI](https://github.com/openai/codex), [Windsurf](https://windsurf.com/), [DeepSeek Coder](https://github.com/deepseek-ai/DeepSeek-Coder), [Tabnine AI](https://www.tabnine.com/), [Grok xAI](https://github.com/xai-org/grok), or [CodeWhisperer](https://aws.amazon.com/codewhisperer)
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Installation

### Initialize a New Project

The easiest way to get started is to initialize a new project:

```bash
uvx --from git+https://github.com/Nom-nom-hub/goal-kit.git goal init <PROJECT_NAME>
```

Or initialize in the current directory:

```bash
uvx --from git+https://github.com/github/goal-dev-kit.git goal init --here
```

### Specify AI Agent

You can proactively specify your AI agent during initialization:

```bash
uvx --from git+https://github.com/github/goal-dev-kit.git goal init <project_name> --ai claude
uvx --from git+https://github.com/github/goal-dev-kit.git goal init <project_name> --ai gemini
uvx --from git+https://github.com/github/goal-dev-kit.git goal init <project_name> --ai copilot
uvx --from git+https://github.com/github/goal-dev-kit.git goal init <project_name> --ai cursor
uvx --from git+https://github.com/github/goal-dev-kit.git goal init <project_name> --ai deepseek
uvx --from git+https://github.com/github/goal-dev-kit.git goal init <project_name> --ai grok
```

### Specify Script Type (Shell vs PowerShell)

All automation scripts now have both Bash (`.sh`) and PowerShell (`.ps1`) variants.

Auto behavior:
- Windows default: `ps`
- Other OS default: `sh`
- Interactive mode: you'll be prompted unless you pass `--script`

Force a specific script type:
```bash
uvx --from git+https://github.com/github/goal-dev-kit.git goal init <project_name> --script sh
uvx --from git+https://github.com/github/goal-dev-kit.git goal init <project_name> --script ps
```

### Ignore Agent Tools Check

If you prefer to get the templates without checking for the right tools:

```bash
uvx --from git+https://github.com/github/goal-dev-kit.git goal init <project_name> --ai claude --ignore-agent-tools
```

## Verification

After initialization, you should see the following commands available in your AI agent:
- `/goals` - Define project goals
- `/clarify` - Clarify and validate goals
- `/strategize` - Develop implementation strategies
- `/plan` - Create technical implementation plans
- `/tasks` - Generate actionable tasks
- `/implement` - Execute implementation

The `.goal/scripts` directory will contain both `.sh` and `.ps1` scripts.

## Troubleshooting

### Git Credential Manager on Linux

If you're having issues with Git authentication on Linux, you can install Git Credential Manager:

```bash
#!/usr/bin/env bash
set -e
echo "Downloading Git Credential Manager v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "Installing Git Credential Manager..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "Configuring Git to use GCM..."
git config --global credential.helper manager
echo "Cleaning up..."
rm gcm-linux_amd64.2.6.1.deb
```

## Next Steps

1. **Set up your project principles** with `/constitution`
2. **Define your goals** with `/goals`
3. **Clarify requirements** with `/clarify`
4. **Develop strategies** with `/strategize`
5. **Plan implementation** with `/plan`
6. **Execute development** with `/tasks` and `/implement`