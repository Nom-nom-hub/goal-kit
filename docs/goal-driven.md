---
layout: default
title: Goal Kit - Goal-Driven Development Toolkit
---

# Goal Kit - Goal-Driven Development Toolkit

## What is Goal-Driven Development?

Goal-Driven Development **focuses on outcomes over specifications**. While Spec-Driven Development creates detailed specifications that generate specific implementations, Goal-Driven Development starts with high-level goals and explores multiple strategies to achieve them.

### Key Differences from Spec-Driven Development:

| Spec-Driven Development | Goal-Driven Development |
|------------------------|------------------------|
| Detailed specifications upfront | High-level goals and outcomes |
| Single implementation path | Multiple strategies exploration |
| Requirements-focused | Metrics and success-focused |
| Implementation precision | Outcome flexibility |

## Key Commands

### Core Commands

Essential commands for the Goal-Driven Development workflow:

- **`/goalkit.vision`** - Create or update project vision, values, and success criteria
- **`/goalkit.goal`** - Define goals and desired outcomes (focus on why, not how)
- **`/goalkit.strategies`** - Explore multiple implementation strategies for achieving goals
- **`/goalkit.milestones`** - Generate measurable milestones and progress indicators
- **`/goalkit.execute`** - Execute implementation with flexibility to adapt and learn

### Optional Commands

Additional commands for enhanced exploration and validation:



## Supported AI Agents

Goal Kit supports 12 different AI agents:

- Claude Code
- GitHub Copilot
- Gemini CLI
- Cursor
- Qwen Code
- opencode
- Codex CLI
- Windsurf
- Kilo Code
- Auggie CLI
- Roo Code
- Amazon Q Developer CLI

## Development phases

1. **Vision Setting** - Establish purpose
2. **Goal Definition** - Outcomes over specs
3. **Strategy Exploration** - Multiple approaches
4. **Milestone Planning** - Measurable progress
5. **Adaptive Execution** - Learning implementation

## Key Principles

### Goals over Specifications
- Focus on outcomes and success criteria
- Define what success looks like before how to achieve it
- Keep goals high-level and flexible

### Multiple Strategies
- Explore different approaches to achieve each goal
- Consider various technical and user experience patterns
- Evaluate trade-offs and risks openly

## Quick Installation

```bash
uv tool install goalkeeper-cli --from git+https://github.com/Nom-nom-hub/goal-kit.git
```

Then use the tool directly:

```bash
goalkeeper init <PROJECT_NAME>
goalkeeper check
```

For more detailed information, see the full documentation.