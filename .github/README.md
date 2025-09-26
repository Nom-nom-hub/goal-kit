<div align="center">
    <h1>🎯 Goal Kit</h1>
    <h3><em>Guide your AI agents to achieve development goals faster.</em></h3>
</div>

<p align="center">
    <strong>An effort to help developers leverage AI agents to accomplish specific development goals through structured goal-driven development.</strong>
</p>

[![Release](https://github.com/Nom-nom-hub/goal-dev-spec/actions/workflows/release.yml/badge.svg)](https://github.com/Nom-nom-hub/goal-dev-spec/actions/workflows/release.yml)
[![CI](https://github.com/Nom-nom-hub/goal-dev-spec/actions/workflows/ci.yml/badge.svg)](https://github.com/Nom-nom-hub/goal-dev-spec/actions/workflows/ci.yml)
[![Docs](https://github.com/Nom-nom-hub/goal-dev-spec/actions/workflows/docs.yml/badge.svg)](https://github.com/Nom-nom-hub/goal-dev-spec/actions/workflows/docs.yml)

---

## Table of Contents

- [🤔 What is Goal-Driven Development?](#-what-is-goal-driven-development)
- [⚡ Get started](#-get-started)
- [🤖 Supported AI Agents](#-supported-ai-agents)
- [🔧 Goal Kit CLI Reference](#-goal-kit-cli-reference)
- [📚 Core philosophy](#-core-philosophy)
- [🎯 Key features](#-key-features)
- [🔧 Prerequisites](#-prerequisites)
- [📖 Learn more](#-learn-more)
- [📋 Detailed process](#-detailed-process)
- [🔍 Troubleshooting](#-troubleshooting)
- [👥 Maintainers](#-maintainers)
- [📄 License](#-license)

## 🤔 What is Goal-Driven Development?

Goal-Driven Development takes a structured approach to software development where developers define clear, specific goals for AI agents to achieve. Unlike traditional task-based approaches, Goal-Driven Development focuses on defining the desired end state and allows AI agents to determine the best approach to reach that goal within established constraints and guidelines.

This methodology helps ensure that AI agents stay focused on the intended outcome while providing flexibility in how they accomplish the goal. The approach emphasizes:

- Clear goal definition before implementation
- Structured milestone-based progress tracking
- Context-rich templates for AI understanding

## ⚡ Get started

### 1. Install Goal Kit

Choose your preferred installation method:

#### Option 1: Persistent Installation (Recommended)

Install once and use everywhere:

```bash
uv tool install goal-kit-cli --from git+https://github.com/Nom-nom-hub/goal-kit.git
```

Then use the tool directly:

```bash
goal init <PROJECT_NAME>
goal setup
```

#### Option 2: One-time Usage

Run directly without installing:

```bash
uvx --from git+https://github.com/Nom-nom-hub/goal-kit.git goal init <PROJECT_NAME>
```

**Benefits of persistent installation:**

- Tool stays installed and available in PATH
- No need to create shell aliases
- Better tool management with `uv tool list`, `uv tool upgrade`, `uv tool uninstall`
- Cleaner shell configuration

### 2. Define your development goals

Use the **`/goal`** command to describe what you want to accomplish. Focus on the **what** and **why**, not the tech stack.

```bash
/goal Create a photo album management application that allows users to organize their photos by date, with albums that can be reorganized by dragging and dropping on the main page. Photos should be displayed in a tile interface within each album.
```

### 3. Set constraints and requirements

Use the **`/constraints`** command to define technical and business constraints.

```bash
/constraints The application should use vanilla JavaScript, HTML, and CSS with minimal external dependencies. Store photo metadata in a local SQLite database. Focus on performance and maintainability.
```

### 4. Break down the goal into milestones

Use the **`/milestones`** command to define the major phases of your project.

```bash
/milestones
```

### 5. Execute the goal

Use **`/execute`** to begin implementation based on your goals and milestones.

```bash
/execute
```

For detailed step-by-step instructions, see our [comprehensive guide](../goal-driven.md).

## 🤖 Supported AI Agents

| Agent                                                     | Support | Notes                                                                                                      |
| --------------------------------------------------------- | ------- | ---------------------------------------------------------------------------------------------------------- |
| [Claude Code](https://www.anthropic.com/claude-code)      | ✅      | Full support for structured goal-driven development                                                        |
| [GitHub Copilot](https://code.visualstudio.com/)          | ✅      | Integrated with VS Code for seamless coding assistance                                                     |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | ✅      | Multi-modal capabilities for complex goal visualization                                                    |
| [Cursor](https://cursor.sh/)                              | ✅      | Real-time editing with goal-aware context                                                                  |
| [Qwen Code](https://github.com/QwenLM/qwen-code)          | ✅      | Advanced code comprehension and generation                                                                 |
| [opencode](https://opencode.ai/)                          | ✅      | Open-source AI coding assistance                                                                           |
| [Windsurf](https://windsurf.com/)                         | ✅      | Collaborative AI development platform                                                                      |
| [Kilo Code](https://github.com/Kilo-Org/kilocode)         | ✅      | Specialized for code understanding and refactoring                                                         |
| [Auggie CLI](https://docs.augmentcode.com/cli/overview)   | ✅      | Augmented coding with goal tracking                                                                        |
| [Roo Code](https://roocode.com/)                          | ✅      | Project navigation with goal context                                                                       |
| [Codex CLI](https://github.com/openai/codex)              | ⚠️      | Codex [does not support](https://github.com/openai/codex/issues/2890) custom arguments for slash commands. |

## 🔧 Goal Kit CLI Reference

The `goal` command supports the following options:

### Commands

| Command | Description                                                |
| ------- | ---------------------------------------------------------- |
| `init`  | Initialize a new Goal Kit project from the latest template |
| `setup` | Configure Goal Kit for your preferred AI assistant         |
| `check` | Check for installed tools and dependencies                 |

### `goal init` Arguments & Options

| Argument/Option        | Type     | Description                                                                                                                           |
| ---------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `<project-name>`       | Argument | Name for your new project directory (optional if using `--here`, or use `.` for current directory)                                    |
| `--ai`                 | Option   | AI assistant to use: `claude`, `gemini`, `copilot`, `cursor`, `qwen`, `opencode`, `codex`, `windsurf`, `kilocode`, `auggie`, or `roo` |
| `--script`             | Option   | Script variant to use: `sh` (bash/zsh) or `ps` (PowerShell)                                                                           |
| `--ignore-agent-tools` | Flag     | Skip checks for AI agent tools                                                                                                        |
| `--no-git`             | Flag     | Skip git repository initialization                                                                                                    |
| `--here`               | Flag     | Initialize project in the current directory instead of creating a new one                                                             |
| `--force`              | Flag     | Force merge/overwrite when initializing in current directory (skip confirmation)                                                      |
| `--skip-tls`           | Flag     | Skip SSL/TLS verification (not recommended)                                                                                           |
| `--debug`              | Flag     | Enable detailed debug output for troubleshooting                                                                                      |
| `--github-token`       | Option   | GitHub token for API requests (or set GH_TOKEN/GITHUB_TOKEN env variable)                                                             |

### Examples

```bash
# Basic project initialization
goal init my-project

# Initialize with specific AI assistant
goal init my-project --ai claude

# Initialize with Cursor support
goal init my-project --ai cursor

# Initialize with Windsurf support
goal init my-project --ai windsurf

# Initialize with PowerShell scripts (Windows/cross-platform)
goal init my-project --ai copilot --script ps

# Initialize in current directory
goal init . --ai copilot
# or use the --here flag
goal init --here --ai copilot

# Force merge into current (non-empty) directory without confirmation
goal init . --force --ai copilot
# or
goal init --here --force --ai copilot

# Skip git initialization
goal init my-project --ai gemini --no-git

# Enable debug output for troubleshooting
goal init my-project --ai claude --debug

# Use GitHub token for API requests (helpful for corporate environments)
goal init my-project --ai claude --github-token ghp_your_token_here

# Check system requirements
goal check
```

### Available Slash Commands

After running `goal init`, your AI coding agent will have access to these slash commands for structured goal-driven development:

| Command        | Description                                                    |
| -------------- | -------------------------------------------------------------- |
| `/goal`        | Define what you want to accomplish (high-level goal statement) |
| `/constraints` | Define technical, business, and architectural constraints      |
| `/milestones`  | Break down the goal into measurable milestones                 |
| `/context`     | Provide relevant context for the AI to understand the project  |
| `/execute`     | Begin implementation based on the defined goal and milestones  |
| `/review`      | Review progress against milestones and adjust as needed        |
| `/validate`    | Validate that the implementation meets the original goal       |

### Environment Variables

| Variable           | Description                                                                                                                                                                                                                                                                                    |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GOAL_KIT_FEATURE` | Override feature detection for non-Git repositories. Set to the feature directory name (e.g., `001-photo-albums`) to work on a specific goal when not using Git branches.<br/>\*\*Must be set in the context of the agent you're working with prior to using `/execute` or follow-up commands. |

## 📚 Core philosophy

Goal-Driven Development is a structured process that emphasizes:

- **Goal-first development** where clear objectives define the "_what_" before the "_how_"
- **Milestone-based progress tracking** with measurable checkpoints
- **Context-rich AI interactions** that provide comprehensive understanding
- **Flexible implementation approaches** that allow AI agents to determine optimal solutions
- **Structured goal refinement** rather than one-shot code generation

## 🎯 Key features

### Goal Structuring

- Clear goal definition templates
- Constraint documentation
- Milestone tracking
- Progress validation

### AI Agent Integration

- Templates optimized for each supported AI agent
- Platform-specific configurations (Bash and PowerShell)
- Context-aware development workflows
- Consistent interface across providers

### Development Phases Support

| Phase                    | Focus                         | Key Activities                                                                                                                                  |
| ------------------------ | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **New Project Creation** | Goal-based initialization     | <ul><li>Define high-level goals</li><li>Establish constraints</li><li>Create project structure</li><li>Set up development environment</li></ul> |
| **Implementation**       | Goal-driven coding            | <ul><li>Break goals into milestones</li><li>Implement with AI assistance</li><li>Track progress</li></ul>                                       |
| **Validation**           | Goal achievement verification | <ul><li>Review completed work</li><li>Validate against original goals</li><li>Adjust milestones as needed</li></ul>                             |

## 🔧 Prerequisites

- **Linux/macOS** (or WSL2 on Windows)
- AI coding agent: [Claude Code](https://www.anthropic.com/claude-code), [GitHub Copilot](https://code.visualstudio.com/), [Gemini CLI](https://github.com/google-gemini/gemini-cli), [Cursor](https://cursor.sh/), [Qwen CLI](https://github.com/QwenLM/qwen-code), [opencode](https://opencode.ai/), [Codex CLI](https://github.com/openai/codex), or [Windsurf](https://windsurf.com/)
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

If you encounter issues with an agent, please open an issue so we can refine the integration.

## 📖 Learn more

- **[Complete Goal-Driven Development Methodology](../goal-driven.md)** - Deep dive into the full process
- **[Detailed Walkthrough](#-detailed-process)** - Step-by-step implementation guide

---

## 📋 Detailed process

<details>
<summary>Click to expand the detailed step-by-step walkthrough</summary>

You can use the Goal Kit CLI to bootstrap your project, which will bring in the required artifacts in your environment. Run:

```bash
goal init <project_name>
```

Or initialize in the current directory:

```bash
goal init .
# or use the --here flag
goal init --here
# Skip confirmation when the directory already has files
goal init . --force
# or
goal init --here --force
```

You will be prompted to select the AI agent you are using. You can also proactively specify it directly in the terminal:

```bash
goal init <project_name> --ai claude
goal init <project_name> --ai gemini
goal init <project_name> --ai copilot
goal init <project_name> --ai cursor
goal init <project_name> --ai qwen
goal init <project_name> --ai opencode
goal init <project_name> --ai codex
goal init <project_name> --ai windsurf
# Or in current directory:
goal init . --ai claude
goal init . --ai codex
# or use --here flag
goal init --here --ai claude
goal init --here --ai codex
# Force merge into a non-empty current directory
goal init . --force --ai claude
# or
goal init --here --force --ai claude
```

The CLI will check if you have the required AI tools installed. If you do not, or you prefer to get the templates without checking for the right tools, use `--ignore-agent-tools` with your command:

```bash
goal init <project_name> --ai claude --ignore-agent-tools
```

### **STEP 1:** Define your development goal

Go to the project folder and run your AI agent. In our example, we're using `claude`.

You will know that things are configured correctly if you see the `/goal`, `/constraints`, `/milestones`, `/context`, `/execute`, `/review`, and `/validate` commands available.

The first step should be defining your project goal using the `/goal` command:

```text
/goal Build a task management application that allows users to create projects, add team members,
assign tasks, comment and move tasks between boards in Kanban style. The initial version should
include user management with predefined users, sample projects, and Kanban boards with drag-and-drop
functionality.
```

This step creates the foundational goal document that will guide all subsequent development phases.

### **STEP 2:** Establish constraints and requirements

With your goal defined, establish the constraints that will guide implementation. Use the `/constraints` command:

```text
/constraints The application should use vanilla JavaScript, HTML, and CSS with minimal external
dependencies. Use a local SQLite database for storing project and task data. The UI should be
responsive and accessible. Focus on performance and maintainability.
```

### **STEP 3:** Break down the goal into milestones

Use the `/milestones` command to create measurable steps toward your goal:

```text
/milestones
```

The AI will generate appropriate milestones based on your goal and constraints. These create a roadmap for implementation with clear checkpoints.

### **STEP 4:** Provide project context

Use the `/context` command to give the AI more information about your project:

```text
/context Provide information about the project domain, existing codebase, specific requirements,
and any other relevant context for the AI to understand when working toward the goal.
```

### **STEP 5:** Begin implementation

Once you've defined your goal, constraints, milestones, and context, use the `/execute` command to start implementation:

```text
/execute
```

The AI will work through the milestones in order, implementing the features according to your goal and constraints.

During implementation, you can use the `/review` command to check progress against milestones:

```text
/review
```

### **STEP 6:** Validate goal achievement

Once implementation is complete, validate that the solution meets your original goal using the `/validate` command:

```text
/validate
```

This compares the implemented solution against the original goal statement to ensure all requirements have been met.

</details>

---

## 🔍 Troubleshooting

### Git Credential Manager on Linux

If you're having issues with Git authentication on Linux, you can install Git Credential Manager:

```bash
#!/usr/bin/env bash
set -e
echo "Downloading Git Credential Manager..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "Installing Git Credential Manager..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "Configuring Git to use GCM..."
git config --global credential.helper manager
echo "Cleaning up..."
rm gcm-linux_amd64.2.6.1.deb
```

## 👥 Maintainers

- Teck ([@Nom-nom-hub](https://github.com/Nom-nom-hub))

## 📄 License

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](../LICENSE) file for the full terms.
