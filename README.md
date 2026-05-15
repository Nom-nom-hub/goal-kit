# 🎯 Goalkit

Goal-Driven Development tool for AI agents. Work with markdown files and scripts - no external AI APIs required.

[![GitHub Release](https://img.shields.io/github/v/release/Nom-nom-hub/goal-kit?color=brightgreen&sort=semver)](https://github.com/Nom-nom-hub/goal-kit/releases/latest)
[![License](https://img.shields.io/github/license/Nom-nom-hub/goal-kit.svg?color=blue)](https://github.com/Nom-nom-hub/goal-kit/blob/main/LICENSE)

---

## Quick Start

### 1. Install

```bash
uv tool install --from git+https://github.com/Nom-nom-hub/goal-kit.git goalkit
```

### 2. Initialize Project

```bash
goalkit init my-project
cd my-project
```

### 3. Define Vision

```bash
.goalkit/scripts/bash/create-vision.sh "Your project vision"
```

---

## What is Goalkit?

Goalkit helps AI agents work on projects using Goal-Driven Development:
- All data stored in **markdown files** (`.goalkit/`)
- All automation via **bash/powershell scripts** (`.goalkit/scripts/`)
- No external dependencies - works offline

### Core Workflow

| Step | Command | Purpose |
|------|---------|---------|
| 1 | `goalkit init` | Initialize project |
| 2 | `.goalkit/scripts/bash/create-vision.sh` | Define vision |
| 3 | `.goalkit/scripts/bash/create-new-goal.sh` | Create goal |
| 4 | `.goalkit/scripts/bash/setup-strategy.sh` | Explore strategies |
| 5 | `.goalkit/scripts/bash/setup-milestones.sh` | Plan milestones |
| 6 | `.goalkit/scripts/bash/setup-execution.sh` | Execute |

---

## Templates (6 Core)

Goalkit uses simple markdown templates:
- `templates/vision-template.md`
- `templates/goal-template.md`
- `templates/lite-goal-template.md`
- `templates/strategies-template.md`
- `templates/milestones-template.md`
- `templates/execution-template.md`

---

## Supported AI Agents

Works with any AI agent that reads markdown:
- Claude (Code, CLI)
- Cursor
- Copilot
- Gemini
- opencode
- Any agent with file access

---

## Installation

### uv (Recommended)

```bash
uv tool install --from git+https://github.com/Nom-nom-hub/goal-kit.git goalkit
```

### pip

```bash
pip install git+https://github.com/Nom-nom-hub/goal-kit.git
```

---

## Project Structure

After `goalkit init`:

```
my-project/
├── .goalkit/
│   ├── vision.md
│   └── goals/
│       └── 001-goal-name/
│           ├── goal.md
│           ├── strategies.md
│           ├── milestones.md
│           └── execution.md
├── CLAUDE.md
└── ... (your code)
```

---

## Commands

```bash
goalkit init <project>     # Initialize new project
goalkit status              # Show project status with insights
goalkit goals               # List all goals
goalkit milestones          # Show milestone progress
```

---

## Key Features

- ✅ Pure markdown-based workflow
- ✅ No external AI API calls
- ✅ Cross-platform (Linux, macOS, Windows)
- ✅ Works with any AI agent
- ✅ 6 simple templates
- ✅ Git integrated

---

## Why Goalkit?

Instead of complex tooling, goalkit gives AI agents:
1. **Vision** - Why are we building this?
2. **Goals** - What does success look like?
3. **Strategies** - Multiple ways to get there
4. **Milestones** - Measurable progress steps
5. **Execution** - Adaptive implementation

All stored in simple markdown files that any agent can read and update.

---

## Documentation

- [CHANGELOG](./CHANGELOG.md) - Version history

---

**Goalkit**: Focus on outcomes, not implementation details.