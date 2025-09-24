# Goal Kit Usage Guide

## Overview
Goal Kit is a goal-driven development framework that helps you build software by starting with clear outcomes rather than technical specifications. This guide shows you exactly how to get started with Qwen CLI.

## Prerequisites
- Python 3.11+ installed
- uv package manager: `pip install uv`
- Git installed
- Qwen CLI or another supported AI agent

## Quick Setup

### 1. Install Goal CLI
```bash
uv tool install goal-cli --from git+https://github.com/nom-nom-hub/goal-dev-kit.git
```

### 2. Create a New Project
```bash
# Create and initialize a new project
goal init my-project
```

### 3. Navigate to Your Project
```bash
cd my-project
```

## Using Goalify with AI Coding Assistants

Once your project is set up, you'll use these special slash commands in an AI coding assistant environment (like Qwen Code, Claude Code, Cursor, etc.), **not** in a regular command line terminal.

The slash commands only work in AI coding assistants that are specifically configured to recognize and process them based on the goal-driven methodology.

After running `goalify init my-project --ai qwen` (or claude, cursor, etc.), the appropriate configuration files are created in `.qwen/commands/`, `.claude/commands/`, etc. Open your project directory in an AI coding assistant, where you'll then use these slash commands:

### The 8-Step Goal-Driven Process

1. **`/constitution`** - Establish project principles
   ```
   /constitution Create principles focused on outcome measurement and iterative validation
   ```

2. **`/goals`** - Define what outcomes you want to achieve
   ```
   /goals Build a web application that helps users manage their tasks efficiently
   ```

3. **`/clarify`** - Resolve any ambiguities in your goals
   ```
   /clarify
   ```

4. **`/strategize`** - Evaluate different implementation approaches
   ```
   /strategize Compare React vs Vue for frontend, Node vs Python for backend
   ```

5. **`/plan`** - Create technical implementation plans
   ```
   /plan Use React frontend with Node.js backend and PostgreSQL database
   ```

6. **`/tasks`** - Generate actionable task lists
   ```
   /tasks
   ```

7. **`/analyze`** - Check consistency across all artifacts (recommended)
   ```
   /analyze
   ```

8. **`/implement`** - Execute the implementation plan
   ```
   /implement
   ```

## Complete Example Workflow

Here's how to run a complete goal-driven development session:

1. **In your terminal:**
   ```bash
   goal init my-todo-app
   cd my-todo-app
   ```

2. **In AI Coding Assistant (Qwen Code, Claude, Cursor, etc.):**
   - Use goal-driven development workflow with AI (the AI should recognize commands like `/goals`, `/strategize`, etc.)
   - `/goals Create a todo app that helps users organize tasks with categories and due dates`
   - `/clarify` (address any questions the AI asks)
   - `/strategize Compare different architecture options for the todo app`
   - `/plan Use React frontend with Express backend and SQLite`
   - `/tasks` (review and approve the task breakdown)
   - `/implement` (build the application)
   - Other potential commands like `/constitution` and `/analyze` would be recognized by advanced AI assistants following the goal-driven methodology

## What Happens Behind the Scenes

When you use `goal init --ai qwen`, the tool creates:

- Project directory structure with `.goals`, `.strategies`, and `.plans` folders
- Template files that guide your AI agent through the goal-driven process
- Configuration that enables slash commands in your Qwen environment
- Memory and documentation files to track your progress

## Troubleshooting

- **Slash commands not recognized**: Make sure you ran `goal init --ai qwen` and are in the correct project directory
- **"Command not found" errors**: Ensure Goal CLI is properly installed via uv
- **AI agent not responding**: Verify your Qwen CLI is properly configured and running

## Next Steps

- Read the [complete methodology guide](./goal-driven.md) to understand the philosophy
- Explore advanced options with `goal --help`
- Check the [detailed process documentation](./README.md#-detailed-process) for complex projects