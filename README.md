<div align="center">
    <img src="./media/logo_small.webp"/>
    <h1>🎯 Goal-Driven Development Kit</h1>
    <h3><em>Build software that achieves meaningful outcomes.</em></h3>
</div>

<p align="center">
    <strong>An innovative approach to software development that starts with clear goals and outcomes, ensuring every technical decision directly supports meaningful results.</strong>
</p>

[![Release](https://github.com/nom-nom-hub/goal-dev-spec/actions/workflows/release.yml/badge.svg)](https://github.com/nom-nom-hub/goal-dev-spec/actions/workflows/release.yml)

---

## Table of Contents

- [🤔 What is Goal-Driven Development?](#-what-is-goal-driven-development)
- [⚡ Get started](#-get-started)
- [📽️ Video Overview](#️-video-overview)
- [🤖 Supported AI Agents](#-supported-ai-agents)
- [🔧 Goal CLI Reference](#-goal-cli-reference)
- [📚 Core philosophy](#-core-philosophy)
- [🌟 Development phases](#-development-phases)
- [🎯 Key differences from Spec-Driven Development](#-key-differences-from-spec-driven-development)
- [🔧 Prerequisites](#-prerequisites)
- [📖 Learn more](#-learn-more)
- [📋 Detailed process](#-detailed-process)
- [🔍 Troubleshooting](#-troubleshooting)
- [👥 Maintainers](#-maintainers)
- [💬 Support](#-support)
- [🙏 Acknowledgements](#-acknowledgements)
- [📄 License](#-license)

## 🤔 What is Goal-Driven Development?

Goal-Driven Development **flips the traditional approach** by starting with desired outcomes rather than technical specifications. Instead of defining what to build and how, we first establish what we want to achieve and why, then determine the best approach to reach those goals.

## ⚡ Get started

### 1. Install Goal CLI

Choose your preferred installation method:

#### Option 1: Persistent Installation (Recommended)

Install once and use everywhere:

```bash
uv tool install goal-cli --from git+https://github.com/nom-nom-hub/goal-dev-kit.git
```

Then use the tool directly:

```bash
goal init <PROJECT_NAME>
goal check
```

#### Option 2: One-time Usage

Run directly without installing:

```bash
uvx --from git+https://github.com/Nom-nom-hub/goal-dev-spec.git goal init <PROJECT_NAME>
```

**Benefits of persistent installation:**

- Tool stays installed and available in PATH
- No need to create shell aliases
- Better tool management with `uv tool list`, `uv tool upgrade`, `uv tool uninstall`
- Cleaner shell configuration

### 2. Establish project principles

Use the **`/constitution`** command to create your project's governing principles and development guidelines that will guide all subsequent development.

```bash
/constitution Create principles focused on goal achievement, outcome measurement, stakeholder alignment, and iterative validation
```

### 3. Define your goals

Use the **`/goals`** command to describe what outcomes you want to achieve. Focus on the **what** and **why**, not the technical implementation.

```bash
/goals Build a team productivity platform that helps remote teams collaborate effectively, track project progress, and maintain work-life balance through smart scheduling and workload management
```

### 4. Clarify and validate goals

Use the **`/clarify`** command to resolve any ambiguities and ensure goals are achievable.

```bash
/clarify
```

### 5. Develop implementation strategy

Use the **`/strategize`** command to evaluate different approaches for achieving your goals.

```bash
/strategize We want to use modern web technologies with real-time collaboration features, focusing on user experience and scalability for growing teams
```

### 6. Create technical implementation plan

Use the **`/plan`** command to provide detailed technical specifications based on your chosen strategy.

```bash
/plan The application uses React with TypeScript frontend, Node.js backend with WebSocket support, PostgreSQL database, and Docker for deployment
```

### 7. Break down into tasks

Use **`/tasks`** to create an actionable task list from your implementation plan.

```bash
/tasks
```

### 8. Execute implementation

Use **`/implement`** to execute all tasks and build your feature according to the plan.

```bash
/implement
```

For detailed step-by-step instructions, see our [comprehensive guide](./goal-driven.md).

## 📽️ Video Overview

Want to see Goal-Driven Development in action? Watch our [video overview](https://www.youtube.com/watch?v=a9eR1xsfvHg&pp=0gcJCckJAYcqIYzv)!

[![Goal-Driven Development video header](./media/spec-kit-video-header.jpg)](https://www.youtube.com/watch?v=a9eR1xsfvHg&pp=0gcJCckJAYcqIYzv)

## 🤖 Supported AI Agents

| Agent                                                     | Support | Notes                                             |
|-----------------------------------------------------------|---------|---------------------------------------------------|
| [Claude Code](https://www.anthropic.com/claude-code)      | ✅ |                                                   |
| [GitHub Copilot](https://code.visualstudio.com/)          | ✅ |                                                   |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | ✅ |                                                   |
| [Cursor](https://cursor.sh/)                              | ✅ |                                                   |
| [Qwen Code](https://github.com/QwenLM/qwen-code)          | ✅ |                                                   |
| [opencode](https://opencode.ai/)                          | ✅ |                                                   |
| [Windsurf](https://windsurf.com/)                         | ✅ |                                                   |
| [Kilo Code](https://github.com/Kilo-Org/kilocode)         | ✅ |                                                   |
| [Auggie CLI](https://docs.augmentcode.com/cli/overview)   | ✅ |                                                   |
| [Roo Code](https://roocode.com/)                          | ✅ |                                                   |
| [DeepSeek Coder](https://github.com/deepseek-ai/DeepSeek-Coder) | ✅ |                                                   |
| [Tabnine AI](https://www.tabnine.com/)                    | ✅ |                                                   |
| [Grok xAI](https://github.com/xai-org/grok)              | ✅ |                                                   |
| [CodeWhisperer](https://aws.amazon.com/codewhisperer)     | ✅ |                                                   |
| [Codex CLI](https://github.com/openai/codex)              | ⚠️ | Codex [does not support](https://github.com/openai/codex/issues/2890) custom arguments for slash commands.  |

## 🔧 Goal CLI Reference

The `goal` command supports the following options:

### Commands

| Command     | Description                                                    |
|-------------|----------------------------------------------------------------|
| `init`      | Initialize a new Goal-Driven Development project from the latest template      |
| `check`     | Check for installed tools (`git`, `claude`, `gemini`, `code`/`code-insiders`, `cursor-agent`, `windsurf`, `qwen`, `opencode`, `codex`, `deepseek`, `tabnine`, `grok`, `codewhisperer`) |

### `goal init` Arguments & Options

| Argument/Option        | Type     | Description                                                                  |
|------------------------|----------|------------------------------------------------------------------------------|
| `<project-name>`       | Argument | Name for your new project directory (optional if using `--here`)            |
| `--ai`                 | Option   | AI assistant to use: `claude`, `gemini`, `copilot`, `cursor`, `qwen`, `opencode`, `codex`, `windsurf`, `kilocode`, `auggie`, `roo`, `deepseek`, `tabnine`, `grok`, or `codewhisperer` |
| `--script`             | Option   | Script variant to use: `sh` (bash/zsh) or `ps` (PowerShell)                 |
| `--ignore-agent-tools` | Flag     | Skip checks for AI agent tools like Claude Code                             |
| `--no-git`             | Flag     | Skip git repository initialization                                          |
| `--here`               | Flag     | Initialize project in the current directory instead of creating a new one   |
| `--force`              | Flag     | Force merge/overwrite when using `--here` in a non-empty directory (skip confirmation) |
| `--skip-tls`           | Flag     | Skip SSL/TLS verification (not recommended)                                 |
| `--debug`              | Flag     | Enable detailed debug output for troubleshooting                            |
| `--github-token`       | Option   | GitHub token for API requests (or set GH_TOKEN/GITHUB_TOKEN env variable)  |

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

# Initialize with DeepSeek support
goal init my-project --ai deepseek

# Initialize with Grok support
goal init my-project --ai grok

# Initialize in current directory
goal init --here --ai copilot

# Force merge into current (non-empty) directory without confirmation
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

After running `goal init`, your AI coding agent will have access to these slash commands for goal-driven development:

| Command         | Description                                                           |
|-----------------|-----------------------------------------------------------------------|
| `/constitution` | Create or update project governing principles and development guidelines |
| `/goals`        | Define project goals and objectives (outcomes-focused)               |
| `/clarify`      | Clarify underspecified areas (must be run before `/strategize`)      |
| `/strategize`   | Develop implementation strategies aligned with goals                 |
| `/plan`         | Create technical implementation plans based on chosen strategy       |
| `/tasks`        | Generate actionable task lists for implementation                     |
| `/analyze`      | Cross-artifact consistency & coverage analysis (run after /tasks, before /implement) |
| `/implement`    | Execute all tasks to build the feature according to the plan         |

### Environment Variables

| Variable         | Description                                                                                    |
|------------------|------------------------------------------------------------------------------------------------|
| `GOAL_FEATURE`   | Override feature detection for non-Git repositories. Set to the feature directory name (e.g., `001-team-productivity`) to work on a specific feature when not using Git branches.<br/>**Must be set in the context of the agent you're working with prior to using `/strategize` or follow-up commands. |

## 📚 Core philosophy

Goal-Driven Development is a structured process that emphasizes:

- **Outcome-first development** where goals define the "_what_" and "_why_" before the "_how_"
- **Goal-oriented planning** using measurable objectives and success criteria
- **Strategy-focused approach** rather than one-dimensional technical specifications
- **Stakeholder alignment** ensuring all work serves user needs and business objectives
- **Iterative validation** continuously ensuring implementation supports defined goals

## 🌟 Development phases

| Phase | Focus | Key Activities |
|-------|-------|----------------|
| **Goal Definition** | Establish objectives | <ul><li>Define clear, measurable goals</li><li>Identify key stakeholders and impact areas</li><li>Create success criteria and validation methods</li><li>Align on desired outcomes before technical work</li></ul> |
| **Strategy Development** | Explore approaches | <ul><li>Evaluate multiple implementation strategies</li><li>Consider technical feasibility and goal alignment</li><li>Assess risks and develop mitigation plans</li><li>Select optimal approach with clear justification</li></ul> |
| **Technical Planning** | Detailed design | <ul><li>Create technical specifications aligned with strategy</li><li>Plan implementation phases and milestones</li><li>Define testing and validation approaches</li><li>Prepare for execution</li></ul> |
| **Implementation** | Build and validate | <ul><li>Execute according to plans and tasks</li><li>Continuously validate against goals</li><li>Adjust course as needed while maintaining goal alignment</li><li>Deliver outcomes that achieve objectives</li></ul> |

## 🎯 Key differences from Spec-Driven Development

### Goal-Driven vs Spec-Driven

| Aspect | Spec-Driven Development | Goal-Driven Development |
|--------|------------------------|-------------------------|
| **Starting Point** | Technical specifications | Desired outcomes and objectives |
| **Focus** | What to build and how | What to achieve and why |
| **Validation** | Does it match the spec? | Does it achieve the goals? |
| **Flexibility** | Changes require spec updates | Course corrections maintain goal alignment |
| **Stakeholder Communication** | Technical requirements | Business outcomes and value |
| **Success Measurement** | Feature completeness | Goal achievement and impact |

### Benefits of Goal-Driven Development

1. **Clear Purpose**: Every technical decision ties back to specific objectives
2. **Better Alignment**: Stakeholders focus on outcomes rather than implementation details
3. **Increased Flexibility**: Multiple approaches can achieve the same goals
4. **Measurable Success**: Clear criteria for determining project success
5. **Reduced Waste**: Less likely to build features that don't serve real needs
6. **Improved Communication**: Focus on value and outcomes rather than technical jargon

## 🔧 Prerequisites

- **Linux/macOS** (or WSL2 on Windows)
- AI coding agent: [Claude Code](https://www.anthropic.com/claude-code), [GitHub Copilot](https://code.visualstudio.com/), [Gemini CLI](https://github.com/google-gemini/gemini-cli), [Cursor](https://cursor.sh/), [Qwen CLI](https://github.com/QwenLM/qwen-code), [opencode](https://opencode.ai/), [Codex CLI](https://github.com/openai/codex), [Windsurf](https://windsurf.com/), [DeepSeek Coder](https://github.com/deepseek-ai/DeepSeek-Coder), [Tabnine AI](https://www.tabnine.com/), [Grok xAI](https://github.com/xai-org/grok), or [CodeWhisperer](https://aws.amazon.com/codewhisperer)
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

If you encounter issues with an agent, please open an issue so we can refine the integration.

## 📖 Learn more

- **[Complete Goal-Driven Development Methodology](./goal-driven.md)** - Deep dive into the full process
- **[Detailed Walkthrough](#-detailed-process)** - Step-by-step implementation guide

---

## 📋 Detailed process

<details>
<summary>Click to expand the detailed step-by-step walkthrough</summary>

You can use the Goal CLI to bootstrap your project, which will bring in the required artifacts in your environment. Run:

```bash
goal init <project_name>
```

Or initialize in the current directory:

```bash
goal init --here
# Skip confirmation when the directory already has files
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
goal init <project_name> --ai deepseek
goal init <project_name> --ai tabnine
goal init <project_name> --ai grok
# Or in current directory:
goal init --here --ai claude
goal init --here --ai codex
# Force merge into a non-empty current directory
goal init --here --force --ai claude
```

The CLI will check if you have Claude Code, Gemini CLI, Cursor CLI, Qwen CLI, opencode, Codex CLI, DeepSeek, Tabnine, Grok, or CodeWhisperer installed. If you do not, or you prefer to get the templates without checking for the right tools, use `--ignore-agent-tools` with your command:

```bash
goal init <project_name> --ai claude --ignore-agent-tools
```

### **STEP 1:** Establish project principles

Go to the project folder and run your AI agent. In our example, we're using `claude`.

You will know that things are configured correctly if you see the `/constitution`, `/goals`, `/strategize`, `/plan`, `/tasks`, and `/implement` commands available.

The first step should be establishing your project's governing principles using the `/constitution` command. This helps ensure consistent decision-making throughout all subsequent development phases:

```text
/constitution Create principles focused on goal achievement, outcome measurement, stakeholder alignment, and iterative validation. Include governance for how these principles should guide technical decisions and implementation choices.
```

This step creates or updates the `/memory/constitution.md` file with your project's foundational guidelines that the AI agent will reference during goal definition, strategy development, planning, and implementation phases.

### **STEP 2:** Define project goals

With your project principles established, you can now define the goals and objectives. Use the `/goals` command and then provide the desired outcomes for the project you want to develop.

> [!IMPORTANT]
> Be as explicit as possible about **what outcomes you want to achieve** and **why they're important**. **Do not focus on the tech stack at this point**.

An example prompt:

```text
/goals Develop TeamSync, a remote team productivity platform. It should help distributed teams stay aligned,
track project progress, maintain work-life balance through smart scheduling, and improve collaboration effectiveness.
Teams should be able to set up projects, assign tasks with clear ownership, track progress in real-time,
and get insights into team productivity patterns. The goal is to reduce miscommunication by 40%,
improve project delivery predictability by 25%, and increase team satisfaction scores by 30%.
Success will be measured through user engagement metrics, project completion rates, and team feedback surveys.
```

After this prompt is entered, you should see your AI agent kick off the goal definition and validation process. The agent will also trigger some of the built-in scripts to set up the repository.

Once this step is completed, you should have a new branch created (e.g., `001-teamsync-goals`), as well as a new goals document in the `goals/001-teamsync` directory.

The produced goals document should contain a set of objectives, success criteria, stakeholder analysis, and validation methods.

At this stage, your project folder contents should resemble the following:

```text
├── memory
│   └── constitution.md
├── scripts
│   ├── check-prerequisites.sh
│   ├── common.sh
│   ├── create-new-feature.sh
│   ├── setup-plan.sh
│   └── update-claude-md.sh
├── goals
│   └── 001-teamsync
│       └── goal.md
└── templates
    ├── goal-template.md
    ├── strategy-template.md
    └── tasks-template.md
```

### **STEP 3:** Goal clarification (required before strategy development)

With the baseline goals created, you can go ahead and clarify any requirements that were not captured properly within the first attempt.

You should run the structured clarification workflow **before** creating implementation strategies to reduce rework downstream.

Preferred order:
1. Use `/clarify` (structured) – sequential, coverage-based questioning that records answers in a Clarifications section.
2. Optionally follow up with ad-hoc free-form refinement if something still feels vague.

If you intentionally want to skip clarification (e.g., spike or exploratory prototype), explicitly state that so the agent doesn't block on missing clarifications.

Example free-form refinement prompt (after `/clarify` if still needed):

```text
For the TeamSync platform, we want to support teams of 5-50 people across different time zones.
The platform should help with both synchronous collaboration (like quick standups) and asynchronous
work (like progress updates and task assignments). Users should be able to set their working hours
preferences and the system should suggest optimal meeting times. We also want to track metrics like
response times to messages, task completion velocity, and meeting effectiveness.
```

You should also ask your AI agent to validate the **Review & Acceptance Checklist**, checking off the things that are validated/pass the requirements, and leave the ones that are not unchecked. The following prompt can be used:

```text
Read the review and acceptance checklist, and check off each item in the checklist if the goal definition meets the criteria. Leave it empty if it does not.
```

It's important to use the interaction with your AI agent as an opportunity to clarify and ask questions around the goals - **do not treat its first attempt as final**.

### **STEP 4:** Develop implementation strategies

You can now develop strategies for achieving your goals. You can use the `/strategize` command that is built into the project template with a prompt like this:

```text
For TeamSync, we want to evaluate different technical approaches. Consider: 1) A modern web application
with real-time features using React frontend and Node.js backend, 2) A mobile-first approach with
React Native for cross-platform support, 3) A desktop application using Electron for rich features.
Evaluate based on development speed, user experience, scalability needs, and team capabilities.
```

The output of this step will include strategy evaluation documents, with your directory tree resembling this:

```text
.
├── memory
│   └── constitution.md
├── scripts
│   ├── check-prerequisites.sh
│   ├── common.sh
│   ├── create-new-feature.sh
│   ├── setup-plan.sh
│   └── update-claude-md.sh
├── goals
│   └── 001-teamsync
│       └── goal.md
├── strategies
│   └── 001-teamsync
│       ├── approach-1-web-app.md
│       ├── approach-2-mobile-first.md
│       ├── approach-3-desktop.md
│       ├── comparison.md
│       └── strategy.md
└── templates
    ├── goal-template.md
    ├── strategy-template.md
    └── tasks-template.md
```

Check the strategy documents to ensure that the approaches align with your goals and team capabilities. You can ask your AI agent to refine them if any of the components stand out, or even have it check the locally-installed version of the platform/framework you want to use.

### **STEP 5:** Plan technical implementation

With your strategy defined, you can now create detailed technical plans. Use the `/plan` command:

```text
Based on our web application strategy for TeamSync, we want to use React with TypeScript for the frontend,
Node.js with Express for the backend, PostgreSQL for the database, and WebSocket integration for real-time features.
Include authentication with JWT, responsive design, and comprehensive testing strategies.
```

This will create detailed implementation plans and technical specifications.

### **STEP 6:** Implementation

Once ready, use the `/implement` command to execute your implementation plan:

```text
/implement
```

The `/implement` command will:
- Validate that all prerequisites are in place (constitution, goals, strategy, and tasks)
- Parse the task breakdown from `tasks.md`
- Execute tasks in the correct order, respecting dependencies and parallel execution markers
- Follow the TDD approach defined in your task plan
- Provide progress updates and handle errors appropriately

> [!IMPORTANT]
> The AI agent will execute local CLI commands (such as `npm`, `git`, etc.) - make sure you have the required tools installed on your machine.

Once the implementation is complete, test the application and resolve any runtime errors that may not be visible in CLI logs (e.g., browser console errors). You can copy and paste such errors back to your AI agent for resolution.

</details>

---

## 🔍 Troubleshooting

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

## 👥 Maintainers

- Your Name ([@nom-nom-hubname](https://github.com/nom-nom-hubname))
- Development Team

## 💬 Support

For support, please open a [GitHub issue](https://github.com/github/goal-dev-kit/issues/new). We welcome bug reports, feature requests, and questions about using Goal-Driven Development.

## 🙏 Acknowledgements

This project builds upon the excellent work of the [Spec Kit](https://github.com/nom-nom-hub/goal-dev-spec) project and extends it with goal-driven development principles.

## 📄 License

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](./LICENSE) file for the full terms.