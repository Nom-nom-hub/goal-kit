<div align="center">
    <h1>🎯 Goal Kit</h1>
    <h3><em>Build software by focusing on outcomes, not specifications.</em></h3>
</div>

<p align="center">
    <strong>Original research and development by Goal Kit. Attribution appreciated but not required.</strong>
</p>

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

Use **`/goalkit.execute`** to begin implementation with continuous learning and adaptation. This command helps structure your execution approach, focusing on measurable progress and evidence-based adjustments.

```bash
/goalkit.execute
```

### 7. Collaborate and coordinate (New!)

Use **`/goalkit.collaborate`** to coordinate work between multiple agents or maintain consistency in single-agent environments. This command creates collaboration plans that track dependencies, communication, and progress across development activities.

```bash
/goalkit.collaborate Coordinate work between frontend and backend development
```

### 8. Persona Management (Advanced!)

Switch between specialized agent personas for different development tasks. The agent can take on specific roles like GitHub specialist, milestone planner, strategy explorer, QA specialist, or documentation expert.

```bash
/goalkit.persona [persona-name]  # Switch to a specific persona
/goalkit.persona github          # Switch to GitHub specialist mode
/goalkit.persona milestone       # Switch to milestone planning mode
/goalkit.persona strategy        # Switch to strategy exploration mode
/goalkit.persona qa             # Switch to quality assurance mode
/goalkit.persona documentation   # Switch to documentation mode
/goalkit.persona general         # Return to general mode (default)
```

When you switch to a specific persona, the agent will:
- Apply specialized knowledge and best practices for that role
- Focus on the specific responsibilities of that persona
- Use role-appropriate terminology and approaches
- Follow persona-specific guidelines and standards

### 9. Recommended Persona Workflows

The persona system works best when you switch to the most appropriate role for your current task:

**For Goal Creation**: Use the general agent or strategy explorer persona
**For Strategy Exploration**: Use the strategy explorer persona for deep technical analysis
**For Milestone Planning**: Use the milestone planner persona for measurable outcomes
**For Implementation**: Either stay as general agent or switch to specialized personas as needed
**For Code Review**: Switch to the QA specialist persona for quality focus
**For Repository Management**: Use the GitHub specialist persona for version control
**For Documentation**: Use the documentation specialist persona for clear docs

Personas help ensure you apply the right expertise at the right time while maintaining overall project consistency.

## 🤖 Supported AI Agents

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

## 🎯 Goal Discovery for AI Agents

When using Goal Kit with AI coding agents, agents now follow a systematic approach to discover existing goals:

1. **Goal Discovery Process**: When processing commands that reference goals, AI agents will:
   - Use filesystem tools to search for goals in the `.goalkit/goals/` directory
   - Enumerate available goals when needed
   - Ask for clarification when goal references are ambiguous
   - Guide users to create new goals when none exist

2. **Enhanced Documentation**: For complete details on goal discovery mechanisms, see `templates/agent_goal_discovery.md`

3. **Improved User Experience**: This enhancement ensures AI agents can help users work with existing goals more effectively, even when the `.goalkit/` directory is git-ignored.

## 🔧 Goalkeeper CLI Reference

The `goalkeeper` command supports the following options:

### Commands

| Command           | Description                                                    |
|-------------------|----------------------------------------------------------------|
| `init`            | Initialize a new Goalkeeper project from the latest template  |
| `check`           | Check for installed tools (`git`, `claude`, `gemini`, `code`/`code-insiders`, `cursor-agent`, `windsurf`, `qwen`, `opencode`, `codex`) |

### `goalkeeper init` Arguments & Options

| Argument/Option        | Type     | Description                                                                  |
|------------------------|----------|------------------------------------------------------------------------------|
| `<project-name>`       | Argument | Name for your new project directory (optional if using `--here`, or use `.` for current directory) |
| `--ai`                 | Option   | AI assistant to use: `claude`, `gemini`, `copilot`, `cursor`, `qwen`, `opencode`, `codex`, `windsurf`, `kilocode`, `auggie`, `roo`, or `q` |
| `--script`             | Option   | Script variant to use: `sh` (bash/zsh) or `ps` (PowerShell) - both now use Python for cross-platform compatibility                 |
| `--ignore-agent-tools` | Flag     | Skip checks for AI agent tools like Claude Code                             |
| `--no-git`             | Flag     | Skip git repository initialization                                          |
| `--here`               | Flag     | Initialize project in the current directory instead of creating a new one   |
| `--force`              | Flag     | Force merge/overwrite when initializing in current directory (skip confirmation) |
| `--skip-tls`           | Flag     | Skip SSL/TLS verification (not recommended)                                 |
| `--debug`              | Flag     | Enable detailed debug output for troubleshooting                            |
| `--github-token`       | Option   | GitHub token for API requests (or set GH_TOKEN/GITHUB_TOKEN env variable)  |





### Available Slash Commands

After running `goalkeeper init`, your AI coding agent will have access to these **core slash commands** for comprehensive goal-driven development:

#### 🚀 Core Workflow Commands

Essential commands for the complete Goal-Driven Development workflow:

| Command                  | Description                                                           |
|--------------------------|-----------------------------------------------------------------------|
| `/goalkit.vision`        | Create or update project vision, values, and success criteria        |
| `/goalkit.goal`          | Define goals and desired outcomes (focus on why, not how)            |
| `/goalkit.strategies`    | Explore multiple implementation strategies for achieving goals        |
| `/goalkit.milestones`    | Generate measurable milestones and progress indicators               |
| `/goalkit.execute`       | Execute implementation with flexibility to adapt and learn           |
| `/goalkit.collaborate`   | Coordinate work between agents or maintain consistency across sessions |

#### 🤝 Coordination Commands

Commands for coordinating work between multiple agents or maintaining consistency:

| Command                  | Description                                                           |
|--------------------------|-----------------------------------------------------------------------|
| `/goalkit.collaborate`   | Set up coordination between agents or maintain self-consistency      |

#### 👤 Persona Management Commands

Commands for managing specialized agent personas for different development tasks:

| Command                  | Description                                                           |
|--------------------------|-----------------------------------------------------------------------|
| `/goalkit.persona [name]`| Switch between specialized agent personas (github, milestone, strategy, qa, documentation) |

#### 🤖 Persona Roles Available

The system supports specialized agent personas for different development tasks:

| Persona | Specialization | Primary Focus |
|---------|---------------|---------------|
| General Agent | Default role | All aspects of goal-driven development |
| GitHub/Git Specialist | Version control | Repository management, branching, PRs |
| Milestone Planner | Planning | Breaking goals into measurable milestones |
| Strategy Explorer | Research & Analysis | Exploring implementation approaches |
| Quality Assurance | Testing & Validation | Quality metrics, testing strategies |
| Documentation Specialist | Documentation | Creating and maintaining project docs |

#### 🔄 Persona Switching Tips

- **Context Switching**: Personas help you apply specialized knowledge at the right time
- **Progress Continuity**: Switching personas maintains project context while changing focus
- **Quality Gating**: Use QA persona for reviews before merging
- **Documentation Focus**: Use Documentation persona when creating user-facing materials
- **Technical Analysis**: Use Strategy Explorer for deep technical approach evaluation

## 🚀 AI Agent Integration

Goal Kit now includes enhanced AI agent integration for more effective slash command processing:

### Enhanced Command Templates
All slash command templates (`/goalkit.vision`, `/goalkit.goal`, etc.) now include:
- **Clear AI processing instructions** for consistent, high-quality responses
- **Structured input/output frameworks** for reliable AI agent parsing
- **Agent-specific optimizations** tailored to different AI capabilities
- **Built-in validation criteria** ensuring methodology compliance

### 🎨 Professional UI/UX Guidelines
Goal Kit now includes comprehensive UI/UX design standards to ensure agents create professional, accessible interfaces:
- **Visual Consistency**: Guidelines for typography, spacing, color palettes, and component design
- **Accessibility Standards**: WCAG 2.1 AA compliance requirements for inclusive design
- **Professional Aesthetics**: Standards for visual hierarchy, whitespace, and design quality
- **User Experience**: Guidelines for error handling, form design, and navigation patterns

### AI Agent Optimization
- **Claude**: Optimized for thoughtful, detailed analysis (4-6 principles)
- **GitHub Copilot**: Optimized for practical, concise implementation (3-5 principles)
- **Gemini**: Optimized for creative, exploratory approaches (3-5 principles)
- **Cursor**: Optimized for focused, direct implementation (3-4 principles)
- **Qwen**: Optimized for comprehensive, detailed coverage (4-6 principles)

### Quality Assurance
- **Response validation** ensures AI outputs meet Goal Kit standards
- **Methodology compliance** checking for outcome-focused language
- **Consistency monitoring** across all generated documents
- **Performance tracking** for continuous improvement

### ⚡ Smart Task Processing
- **Task Complexity Assessment**: Intelligent evaluation of whether tasks need full methodology or direct implementation
- **Efficient Handling**: Simple tasks like "enhanced header" now use direct implementation avoiding unnecessary complexity
- **Smart Workflow**: AI agents determine optimal approach based on task requirements

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
  <strong>Goal Kit transforms software development from task execution to outcome achievement. DUH!</strong>
</p>

<p align="center">
  <a href="https://github.com/Nom-nom-hub/goal-kit/issues">Report Bug</a> · <a href="https://github.com/Nom-nom-hub/goal-kit/issues">Request Feature</a> · <a href="https://github.com/Nom-nom-hub/goal-kit/discussions">Ask Question</a>
</p>