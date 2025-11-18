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
uv tool install --from git+https://github.com/Nom-nom-hub/goal-kit.git goalkeeper
```

### 2. Initialize Project

```bash
goalkeeper init my-project
cd my-project
```

### 3. Use 5 Core Commands

```bash
# 1️⃣ Establish vision and principles
/goalkit.vision

# 2️⃣ Define measurable goals (outcomes, not tasks)
/goalkit.goal Build user authentication with measurable success metrics

# 3️⃣ Explore multiple strategies
/goalkit.strategies

# 4️⃣ Create measurable milestones
/goalkit.milestones

# 5️⃣ Execute with learning and adaptation
/goalkit.execute
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

### The 5 Core Commands

| # | Command | Purpose | Focus |
|---|---------|---------|-------|
| 1️⃣ | `/goalkit.vision` | Project principles | Why we're building this |
| 2️⃣ | `/goalkit.goal` | Measurable outcomes | What success looks like |
| 3️⃣ | `/goalkit.strategies` | Multiple approaches | How we might achieve it |
| 4️⃣ | `/goalkit.milestones` | Progress checkpoints | Breaking into steps |
| 5️⃣ | `/goalkit.execute` | Adaptive implementation | Building with learning |

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
uv tool install --from git+https://github.com/Nom-nom-hub/goal-kit.git goalkeeper
```

From local repo:
```bash
uv tool install --from . goalkeeper
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
uv run --from git+https://github.com/Nom-nom-hub/goal-kit.git goalkeeper init my-project
```

For detailed installation instructions, see [Installation Guide](./docs/installation.md).

---

## 📚 Documentation

- **[Quick Start Guide](./docs/quickstart.md)** - 5-minute getting started
- **[Installation Guide](./docs/installation.md)** - Detailed install instructions for all platforms
- **[Troubleshooting Guide](./docs/troubleshooting.md)** - Solutions for common issues
- **[Goal-Driven Development](./docs/goal-driven.md)** - Complete methodology guide
- **[Comparison with Spec-Driven](./docs/comparison.md)** - Key differences explained
- **[Practical Examples](./docs/examples.md)** - Real-world use cases

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

- ✅ **5 focused commands** for complete workflow
- ✅ **Works with all major AI agents**
- ✅ **Cross-platform** (Linux, macOS, Windows)
- ✅ **Git integrated** for branch management
- ✅ **Measurable outcomes** over tasks
- ✅ **Multiple strategy exploration** built-in
- ✅ **Learning-focused** execution
- ✅ **Easy installation** with uv

---

## 🚀 Next Steps

1. **Install**: `uv tool install --from . goalkeeper`
2. **Initialize**: `goalkeeper init my-project`
3. **Get Started**: Read [Quick Start Guide](./docs/quickstart.md)
4. **Learn**: Read [Goal-Driven Development](./docs/goal-driven.md)

---

**Ready to focus on outcomes instead of specifications?** Start with the [Quick Start Guide](./docs/quickstart.md).
