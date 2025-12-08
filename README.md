# 🎯 Goal Kit

## *Build software by focusing on outcomes, not specifications.*

Goal Kit transforms software development from task execution to outcome achievement using Goal-Driven Development methodology.

[![GitHub Release](https://img.shields.io/github/v/release/Nom-nom-hub/goal-kit?color=brightgreen&sort=semver)](https://github.com/Nom-nom-hub/goal-kit/releases/latest)
[![Release Workflow](https://img.shields.io/github/actions/workflow/status/Nom-nom-hub/goal-kit/release.yml?branch=main&label=release)](https://github.com/Nom-nom-hub/goal-kit/actions/workflows/release.yml)
[![License](https://img.shields.io/github/license/Nom-nom-hub/goal-kit.svg?color=blue)](https://github.com/Nom-nom-hub/goal-kit/blob/main/LICENSE)

---

## ⚡ Quick Start (5 minutes)

### 1. Install

```bash
uv tool install --from git+https://github.com/Nom-nom-hub/goal-kit.git goalkeeper-cli
```

### 2. Initialize Project

```bash
goalkeeper init my-project
cd my-project
```

### 3. Use 9 Goal Kit Commands

**Core workflow** (vision → goal → strategy → milestones → execution):
```bash
/goalkit.vision          # Establish vision and principles
/goalkit.goal            # Define measurable goals
/goalkit.strategies      # Explore multiple strategies
/goalkit.milestones      # Create measurable milestones
/goalkit.execute         # Execute with learning
```

**Extended workflow** (execution → tasks → metrics → review):
```bash
/goalkit.tasks           # Break down into detailed tasks
/goalkit.report          # Generate progress reports
/goalkit.review          # Conduct retrospectives
/goalkit.taskstoissues   # Convert tasks to GitHub issues
```

Done! Your workflow is set up.

For the **5-minute walkthrough**, see [Quick Start Guide](./docs/quickstart.md).

---

## 🌟 What is Goal-Driven Development?

Goal-Driven Development **focuses on outcomes over specifications**:

| Aspect | Spec-Driven | Goal-Driven |
|--------|------------|------------|
| **Starting Point** | Detailed specs | High-level goals |
| **Focus** | Requirements | Outcomes |
| **Strategy** | Single approach | Multiple approaches |
| **Success** | Specification compliance | Goal achievement |

### The 9 Goal Kit Commands

**Core Workflow** (Always Use):

| # | Command | Purpose | Focus |
|---|---------|---------|-------|
| 1️⃣ | `/goalkit.vision` | Project principles | Why we're building this |
| 2️⃣ | `/goalkit.goal` | Measurable outcomes | What success looks like |
| 3️⃣ | `/goalkit.strategies` | Multiple approaches | How we might achieve it |
| 4️⃣ | `/goalkit.milestones` | Progress checkpoints | Breaking into steps |
| 5️⃣ | `/goalkit.execute` | Adaptive implementation | Building with learning |

**Extended Workflow** (As Needed):

| # | Command | Purpose | Focus |
|---|---------|---------|-------|
| 6️⃣ | `/goalkit.tasks` | Task breakdown | Breaking execution into detailed work |
| 7️⃣ | `/goalkit.report` | Progress metrics | Measuring achievement and trends |
| 8️⃣ | `/goalkit.review` | Retrospective | Assessing achievement and learning |
| 9️⃣ | `/goalkit.taskstoissues` | GitHub integration | Converting tasks to issues |

---

## 📁 What Gets Created

After `goalkeeper init`:

```
my-project/
├── .goalkit/
│   ├── vision.md                  # Project vision
│   └── goals/
│       └── 001-goal-name/
│           ├── goal.md            # Goal definition
│           ├── strategies.md       # Implementation approaches
│           ├── milestones.md       # Progress checkpoints
│           └── execution.md        # Implementation plan
├── CLAUDE.md                       # Agent context
├── CURSOR.md                       # Agent context
└── ... (your code)
```

---

## 🤖 Supported AI Agents

Works with all major AI coding assistants:

- Claude Code
- GitHub Copilot  
- Google Gemini
- Cursor
- Qwen Code
- Windsurf
- Kilo Code
- Amazon Q
- opencode
- And others

---

## 🚀 Installation Options

### Option 1: uv (Recommended)

From GitHub:
```bash
uv tool install --from git+https://github.com/Nom-nom-hub/goal-kit.git goalkeeper-cli
```

From local repo:
```bash
uv tool install --from . goalkeeper-cli
```

### Option 2: pip

```bash
pip install git+https://github.com/Nom-nom-hub/goal-kit.git
```

Or locally:
```bash
pip install -e .
```

### Option 3: One-Time Usage

```bash
uv run --from git+https://github.com/Nom-nom-hub/goal-kit.git goalkeeper-cli init my-project
```

For detailed installation instructions, see [Installation Guide](./docs/installation.md).

---

## 📚 Documentation

### Getting Started
- **[Quick Start Guide](./docs/quickstart.md)** - 5-minute getting started
- **[Quick Reference Card](./docs/quick-reference.md)** - 📋 One-page cheat sheet (print and keep handy!)
- **[Installation Guide](./docs/installation.md)** - Detailed install instructions for all platforms
- **[Agent & VSCode Setup](./AGENT_AND_VSCODE_SETUP.md)** - Setup AI agents and development environment

### Learning & Reference
- **[Goal-Driven Development](./docs/goal-driven.md)** - Complete methodology guide
- **[Workflow Guide](./docs/workflow-guide.md)** - 🔄 State machine, decision trees, and workflow patterns
- **[Common Mistakes](./docs/common-mistakes.md)** - ❌ Avoid these pitfalls when starting
- **[Comparison with Spec-Driven](./docs/comparison.md)** - Key differences explained
- **[Practical Examples](./docs/examples.md)** - Real-world use cases

### Guides & Troubleshooting
- **[Troubleshooting Guide](./docs/troubleshooting.md)** - Solutions for common issues
- **[Agent File Guide](./templates/agent-file-template.md)** - Guide for AI agents using Goal Kit

### Change History
- **[Changelog](./CHANGELOG.md)** - Version history and release notes

---

## 💡 Core Principles

### 1. Goals Over Specs
Focus on outcomes, not implementation details

### 2. Multiple Strategies
Always explore multiple valid approaches

### 3. Measurable Success
Define clear metrics before building

### 4. Adaptive Execution
Be willing to pivot based on evidence

### 5. Learning Integration
Treat implementation as hypothesis testing

---

## 🎯 Typical Workflow

```
1. Define Vision
   ↓
2. Create Goal (with success metrics)
   ↓
3. Explore Strategies (3+ approaches)
   ↓
4. Plan Milestones (measurable steps)
   ↓
5. Execute (with continuous learning)
   ↓
6. Measure Results
   ↓
7. Repeat for next goal
```

---

## 🔧 Prerequisites

- **Python**: 3.8+
- **Git**: For version control
- **OS**: Linux, macOS, or Windows
- **uv**: For package management (optional but recommended)

---

## 🆘 Getting Help

- **Issues**: [Report on GitHub](https://github.com/Nom-nom-hub/goal-kit/issues)
- **Questions**: [Ask in Discussions](https://github.com/Nom-nom-hub/goal-kit/discussions)
- **Troubleshooting**: [Read Troubleshooting Guide](./docs/troubleshooting.md)

---

## ✨ Key Features

- ✅ **9 commands** for complete workflow (vision → goal → strategies → milestones → execute → tasks → report → review)
- ✅ **Works with all major AI agents** (Claude, Copilot, Cursor, Gemini, etc.)
- ✅ **Cross-platform** (Linux, macOS, Windows)
- ✅ **Git integrated** for branch management
- ✅ **Measurable outcomes** over tasks
- ✅ **Multiple strategy exploration** built-in
- ✅ **Learning-focused** execution
- ✅ **Easy installation** with uv
- ✅ **VSCode optimized** with settings templates and recommended extensions
- ✅ **Agent integration guides** included in box

---

## 🤖 Working with AI Agents

Goal Kit includes built-in support for AI agents like Claude, Cursor, and Copilot:

1. **Copy agent template**: Use `templates/agent-file-template.md` to create `CLAUDE.md` (or other agents)
2. **Share with agent**: Provide the customized agent file when asking for Goal Kit help
3. **Agent executes**: The agent follows the methodology guides automatically
4. **VSCode integration**: Developers review and refine with optimized editor settings

See [Agent & VSCode Setup](./AGENT_AND_VSCODE_SETUP.md) for complete instructions.

---

## 💻 VSCode Integration

Goal Kit provides optimized VSCode configuration:

- **Auto-formatting** for Python (Black), Markdown, JSON
- **100-character ruler** for consistent code style
- **GitLens integration** for tracking goal milestones
- **Recommended extensions** for development (15+ tools)
- **File nesting** shows goal document relationships in Explorer

Setup in 2 steps:
```bash
cp templates/.vscode-settings-template.json .vscode/settings.json
cp templates/.vscode-extensions-template.json .vscode/extensions.json
```

VSCode will automatically suggest installing recommended extensions.

---

## 🚀 Next Steps

1. **Install**: `uv tool install --from . goalkeeper-cli`
2. **Initialize**: `goalkeeper init my-project`
3. **Get Started**: Read [Quick Start Guide](./docs/quickstart.md)
4. **Learn**: Read [Goal-Driven Development](./docs/goal-driven.md)

---

**Ready to focus on outcomes instead of specifications?** Start with the [Quick Start Guide](./docs/quickstart.md).
