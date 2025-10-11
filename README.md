<div align="center">
    <h1>🎯 Goal Kit</h1>
    <h3><em>Build software by focusing on outcomes, not specifications.</em></h3>
</div>

<p align="center">
    <strong>An effort to allow organizations to focus on business outcomes and user goals rather than writing undifferentiated code with the help of Goal-Driven Development.</strong>
</p>

<p align="center">
   <a href="https://github.com/Nom-nom-hub/goal-kit/releases/latest">
     <img src="https://img.shields.io/github/v/release/Nom-nom-hub/goal-kit?color=brightgreen&sort=semver" alt="GitHub Release">
   </a>
   <a href="https://github.com/Nom-nom-hub/goal-kit/actions/workflows/release.yml">
     <img src="https://img.shields.io/github/actions/workflow/status/Nom-nom-hub/goal-kit/release.yml?branch=main&label=release" alt="Release Workflow">
   </a>
   <a href="https://github.com/Nom-nom-hub/goal-kit/actions/workflows/docs.yml">
     <img src="https://img.shields.io/github/actions/workflow/status/Nom-nom-hub/goal-kit/docs.yml?branch=main&label=docs" alt="Docs Workflow">
   </a>
   <a href="https://github.com/Nom-nom-hub/goal-kit/blob/main/LICENSE">
     <img src="https://img.shields.io/github/license/Nom-nom-hub/goal-kit.svg?color=blue" alt="License">
   </a>
   <a href="https://github.com/Nom-nom-hub/goal-kit/stargazers">
     <img src="https://img.shields.io/github/stars/Nom-nom-hub/goal-kit.svg?color=yellow" alt="GitHub Stars">
   </a>
   <a href="https://github.com/Nom-nom-hub/goal-kit/graphs/contributors">
     <img src="https://img.shields.io/github/contributors/Nom-nom-hub/goal-kit.svg" alt="Contributors">
   </a>
 </p>

<p align="center">
   <img src="https://img.shields.io/badge/The%20Future-✅%20Goal--Driven%20Development-brightgreen?style=for-the-badge&logo=github" alt="The Future - Goal-Driven Development">
 </p>

---

## 🌟 What is Goal-Driven Development?

Goal-Driven Development **focuses on outcomes over specifications**. While Spec-Driven Development creates detailed specifications that generate specific implementations, Goal-Driven Development starts with high-level goals and explores multiple strategies to achieve them.

### Key Differences from Spec-Driven Development:

| Spec-Driven Development | Goal-Driven Development |
|------------------------|------------------------|
| Detailed specifications upfront | High-level goals and outcomes |
| Single implementation path | Multiple strategies exploration |
| Requirements-focused | Metrics and success-focused |
| Implementation precision | Outcome flexibility |

## ⚡ Quick Start

### 1. Install Goalkeeper

Choose your preferred installation method:

#### Option 1: Persistent Installation (Recommended)

Install once and use everywhere:

```bash
uv tool install goalkeeper-cli --from git+https://github.com/Nom-nom-hub/goal-kit.git
```

Then use the tool directly:

```bash
goalkeeper init <PROJECT_NAME>
goalkeeper check
```

#### Option 2: One-time Usage

Run directly without installing:

```bash
uvx --from git+https://github.com/Nom-nom-hub/goal-kit.git goalkeeper init <PROJECT_NAME>
```

### 2. Establish project vision

Use the **`/goalkit.vision`** command to create your project's purpose, values, and success criteria that will guide all subsequent development.

```bash
/goalkit.vision Create a vision focused on user outcomes, business metrics, and flexible achievement strategies
```

### 3. Define goals

Use the **`/goalkit.goal`** command to describe what outcomes you want to achieve. Focus on the **why** and **what success looks like**, not the implementation.

```bash
/goalkit.goal Build an application that helps users achieve [specific outcome] with measurable success criteria
```

### 4. Explore strategies

Use the **`/goalkit.strategies`** command to explore multiple approaches for achieving your goals.

```bash
/goalkit.strategies Consider different technical approaches, user experience patterns, and implementation strategies
```

### 5. Set milestones

Use **`/goalkit.milestones`** to create measurable milestones from your strategies.

```bash
/goalkit.milestones
```

### 6. Execute with flexibility

Use **`/goalkit.execute`** to implement with the ability to adapt based on results and learning.

```bash
/goalkit.execute
```

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
| [Codex CLI](https://github.com/openai/codex)              | ✅ |                                                   |
| [Amazon Q Developer CLI](https://aws.amazon.com/developer/learning/q-developer-cli/) | ⚠️ | Amazon Q Developer CLI [does not support](https://github.com/aws/amazon-q-developer-cli/issues/3064) custom arguments for slash commands. |

## 🔧 Goalkeeper CLI Reference

The `goalkeeper` command supports the following options:

### Commands

| Command           | Description                                                    |
|-------------------|----------------------------------------------------------------|
| `init`            | Initialize a new Goalkeeper project from the latest template  |
| `check`           | Check for installed tools (`git`, `claude`, `gemini`, `code`/`code-insiders`, `cursor-agent`, `windsurf`, `qwen`, `opencode`, `codex`) |
| `ai-analytics`    | Display AI agent performance analytics and interaction insights |
| `memory-status`   | Display memory system status and learning insights             |
| `learn-extract`   | Extract learnings from completed goals and add to memory      |
| `memory-insights` | Get AI-powered insights from project memory and learning data |
| `memory-patterns` | Analyze patterns in project memory for continuous improvement |

### `goalkeeper init` Arguments & Options

| Argument/Option        | Type     | Description                                                                  |
|------------------------|----------|------------------------------------------------------------------------------|
| `<project-name>`       | Argument | Name for your new project directory (optional if using `--here`, or use `.` for current directory) |
| `--ai`                 | Option   | AI assistant to use: `claude`, `gemini`, `copilot`, `cursor`, `qwen`, `opencode`, `codex`, `windsurf`, `kilocode`, `auggie`, `roo`, or `q` |
| `--script`             | Option   | Script variant to use: `sh` (bash/zsh) or `ps` (PowerShell)                 |
| `--ignore-agent-tools` | Flag     | Skip checks for AI agent tools like Claude Code                             |
| `--no-git`             | Flag     | Skip git repository initialization                                          |
| `--here`               | Flag     | Initialize project in the current directory instead of creating a new one   |
| `--force`              | Flag     | Force merge/overwrite when initializing in current directory (skip confirmation) |
| `--skip-tls`           | Flag     | Skip SSL/TLS verification (not recommended)                                 |
| `--debug`              | Flag     | Enable detailed debug output for troubleshooting                            |
| `--github-token`       | Option   | GitHub token for API requests (or set GH_TOKEN/GITHUB_TOKEN env variable)  |

### `goalkeeper ai-analytics` Arguments & Options

| Argument/Option | Type     | Description                                                                  |
|-----------------|----------|------------------------------------------------------------------------------|
| `--agent`       | Option   | Filter analytics by specific AI agent (e.g., `claude`, `copilot`)           |
| `--days`        | Option   | Number of days to analyze (default: 30)                                     |
| `--format`      | Option   | Output format: `table` (default), `json`, or `csv`                          |

### Memory System Commands

| Command             | Description                                                                  |
|---------------------|------------------------------------------------------------------------------|
| `memory-status`     | Display memory system status and learning insights                           |
| `learn-extract`     | Extract learnings from completed goals and add to memory system              |
| `memory-insights`   | Get AI-powered insights from project memory and learning data                |
| `memory-patterns`   | Analyze patterns in project memory for continuous improvement               |

### `goalkeeper memory-status` Arguments & Options

| Argument/Option | Type     | Description                                                                  |
|-----------------|----------|------------------------------------------------------------------------------|
| `--details`     | Flag     | Show detailed memory statistics and insights                                 |

### `goalkeeper learn-extract` Arguments & Options

| Argument/Option | Type     | Description                                                                  |
|-----------------|----------|------------------------------------------------------------------------------|
| `<goal-name>`   | Argument | Name of the completed goal to extract learnings from                        |
| `--score`       | Option   | Success score 1-10 (default: 7)                                             |

### `goalkeeper memory-insights` Arguments & Options

| Argument/Option | Type     | Description                                                                  |
|-----------------|----------|------------------------------------------------------------------------------|
| `--patterns`    | Flag     | Include pattern analysis in insights (default: true)                        |

### `goalkeeper memory-patterns` Arguments & Options

| Argument/Option | Type     | Description                                                                  |
|-----------------|----------|------------------------------------------------------------------------------|
| `--type`        | Option   | Pattern type: success, failure, or process (default: success)                |

### Available Slash Commands

After running `goalkeeper init`, your AI coding agent will have access to these **18 powerful slash commands** for comprehensive goal-driven development:

#### 🚀 Core Workflow Commands

Essential commands for the complete Goal-Driven Development workflow:

| Command                  | Description                                                           |
|--------------------------|-----------------------------------------------------------------------|
| `/goalkit.vision`        | Create or update project vision, values, and success criteria        |
| `/goalkit.goal`          | Define goals and desired outcomes (focus on why, not how)            |
| `/goalkit.strategies`    | Explore multiple implementation strategies for achieving goals        |
| `/goalkit.milestones`    | Generate measurable milestones and progress indicators               |
| `/goalkit.plan`          | Create detailed execution plans with resource allocation             |
| `/goalkit.execute`       | Execute implementation with flexibility to adapt and learn            |

#### 🔍 Analysis & Intelligence Commands

Advanced commands for project analysis, insights, and optimization:

| Command                  | Description                                                           |
|--------------------------|-----------------------------------------------------------------------|
| `/goalkit.analyze`       | Comprehensive project health analysis and pattern recognition        |
| `/goalkit.validate`      | Quality assurance and methodology compliance checking                |
| `/goalkit.insights`      | AI-powered pattern recognition and actionable recommendations        |
| `/goalkit.prioritize`    | Smart goal prioritization using multiple factors                     |
| `/goalkit.track`         | Advanced progress monitoring and forecasting                         |

#### 📊 Research & Learning Commands

Commands for external knowledge integration and continuous improvement:

| Command                  | Description                                                           |
|--------------------------|-----------------------------------------------------------------------|
| `/goalkit.research`      | External knowledge integration and market research                   |
| `/goalkit.learn`         | Experience capture and knowledge management                          |
| `/goalkit.benchmark`     | Industry comparison and best practice alignment                     |

#### 🛠️ Enhancement Commands

Additional commands for enhanced exploration and validation:

| Command              | Description                                                           |
|----------------------|-----------------------------------------------------------------------|
| `/goalkit.tasks`     | Generate actionable tasks from milestones and goals                  |
| `/goalkit.explore`   | Explore alternative approaches and what-if scenarios                 |
| `/goalkit.measure`   | Define success metrics and measurement approaches                    |
| `/goalkit.adapt`     | Adapt strategies based on results and learning                       |

## 🚀 AI Agent Integration

Goal Kit now includes enhanced AI agent integration for more effective slash command processing:

### Enhanced Command Templates
All slash command templates (`/goalkit.vision`, `/goalkit.goal`, etc.) now include:
- **Clear AI processing instructions** for consistent, high-quality responses
- **Structured input/output frameworks** for reliable AI agent parsing
- **Agent-specific optimizations** tailored to different AI capabilities
- **Built-in validation criteria** ensuring methodology compliance

### AI Agent Optimization
- **Claude**: Optimized for thoughtful, detailed analysis (4-6 principles)
- **GitHub Copilot**: Optimized for practical, concise implementation (3-5 principles)
- **Gemini**: Optimized for creative, exploratory approaches (3-5 principles)
- **Cursor**: Optimized for focused, direct implementation (3-4 principles)
- **Qwen**: Optimized for comprehensive, detailed coverage (4-6 principles)

### Performance Analytics
Monitor AI agent effectiveness with the new `goalkeeper ai-analytics` command:
- Track success rates across different AI agents
- Monitor response quality scores and validation compliance
- Identify which agents work best for specific command types
- Analyze interaction patterns and improvement opportunities

### 🧠 Intelligent Memory System
**Project Learning Capture:**
- Auto-extract learnings when goals complete
- Pattern recognition for common success factors
- Template updates based on what works in practice

**AI Session Context:**
- Conversation memory - remembers what was discussed
- Decision tracking - records AI suggestions and outcomes
- Preference learning - adapts to user and agent preferences

**Cross-Project Insights:**
- Similar project matching - finds relevant past experiences
- Best practice evolution - improves templates based on outcomes
- Risk pattern detection - early warning for common failure modes

### Quality Assurance
- **Response validation** ensures AI outputs meet Goal Kit standards
- **Methodology compliance** checking for outcome-focused language
- **Consistency monitoring** across all generated documents
- **Performance tracking** for continuous improvement
- **Memory system integrity** ensuring learning data quality

## 📚 Core philosophy

Goal-Driven Development is a structured process that emphasizes:

- **Outcome-driven development** where goals define the "_what_" before exploring "_how_"
- **Flexible strategy exploration** with multiple paths to achieve goals
- **Measurable success criteria** rather than detailed requirements
- **Adaptive execution** that learns and adjusts based on results
- **Exploration over prescription** with multiple implementation approaches

## 🎯 Development phases

| Phase | Focus | Key Activities |
|-------|-------|----------------|
| **Vision Setting** | Establish purpose | <ul><li>Define project vision and values</li><li>Set success criteria and metrics</li><li>Establish guiding principles</li></ul> |
| **Goal Definition** | Outcomes over specs | <ul><li>Define high-level goals</li><li>Focus on user and business outcomes</li><li>Set measurable success criteria</li></ul> |
| **Strategy Exploration** | Multiple approaches | <ul><li>Explore diverse implementation strategies</li><li>Consider different technical approaches</li><li>Evaluate trade-offs and risks</li></ul> |
| **Milestone Planning** | Measurable progress | <ul><li>Break goals into measurable milestones</li><li>Define progress indicators</li><li>Set up tracking and measurement</li></ul> |
| **Adaptive Execution** | Learning implementation | <ul><li>Implement with flexibility</li><li>Learn from results and feedback</li><li>Adapt strategies as needed</li></ul> |

## 🔧 Prerequisites

- **Linux/macOS** (or WSL2 on Windows)
- AI coding agent: [Claude Code](https://www.anthropic.com/claude-code), [GitHub Copilot](https://code.visualstudio.com/), [Gemini CLI](https://github.com/google-gemini/gemini-cli), [Cursor](https://cursor.sh/), [Qwen CLI](https://github.com/QwenLM/qwen-code), [opencode](https://opencode.ai/), [Codex CLI](https://github.com/openai/codex), [Windsurf](https://windsurf.com/), or [Amazon Q Developer CLI](https://aws.amazon.com/developer/learning/q-developer-cli/)
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## 📖 Learn more

- **[Complete Goal-Driven Development Methodology](./goal-driven.md)** - Deep dive into the full process
- **[Goal vs Spec-Driven Development](./comparison.md)** - Understanding the key differences

---

## 📋 Key Principles

### Goals over Specifications
- Focus on outcomes and success criteria
- Define what success looks like before how to achieve it
- Keep goals high-level and flexible

### Multiple Strategies
- Explore different approaches to achieve each goal
- Consider various technical and user experience patterns
- Evaluate trade-offs and risks openly

### Measurable Progress
- Define clear success metrics for each goal
- Set up measurable milestones and indicators
- Track progress with data and feedback

### Adaptive Execution
- Implement with flexibility to learn and adjust
- Be willing to pivot strategies based on results
- Embrace experimentation and iteration

### Learning Focus
- Treat implementation as a learning process
- Use results and feedback to improve approaches
- Document what works and what doesn't for future goals

---

<p align="center">
  <strong>Goal Kit transforms software development from task execution to outcome achievement.</strong>
</p>

<p align="center">
  <a href="https://github.com/Nom-nom-hub/goal-kit/issues">Report Bug</a> · <a href="https://github.com/Nom-nom-hub/goal-kit/issues">Request Feature</a> · <a href="https://github.com/Nom-nom-hub/goal-kit/discussions">Ask Question</a>
</p>