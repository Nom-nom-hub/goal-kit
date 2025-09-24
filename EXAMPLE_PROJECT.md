# Goal Kit Example: Simple Calculator API

## Introduction

This example demonstrates how to use Goal Kit in a real project. This is a step-by-step guide showing how to implement a simple calculator API using the goal-driven development approach.

## Prerequisites

Before starting, ensure you have:
- Python 3.11+ installed
- uv package manager installed (`pip install uv`)
- Git installed
- An AI coding assistant (like Qwen Code, Claude, Cursor, etc.)

## Step-by-Step Workflow

### 1. Initialize the Project

```bash
# Install Goal CLI
uv tool install goal-cli --from git+https://github.com/nom-nom-hub/goal-dev-kit.git

# Initialize a new project
goal init calculator-api
cd calculator-api
```

### 2. Using the AI Coding Assistant

This is the key step that was not clearly explained before. You need to open this project in an AI coding assistant environment like:
- Qwen Code IDE
- Cursor
- Claude Desktop/Plugin
- GitHub Copilot Chat
- etc.

Once you open the project in one of these environments, the AI assistant will recognize and respond to the slash commands.

### 3. Example Session with an AI Assistant

Let's walk through an example session using the AI assistant:

**In your AI coding assistant (e.g., Qwen Code), type:**

```
/constitution Create principles focused on simplicity, maintainability, and robust error handling
```

The AI will then create a constitution file with project principles.

**Then type:**

```
/goals Build a simple calculator API that performs basic operations (add, subtract, multiply, divide) via HTTP endpoints. The API should be lightweight, fast, and handle errors gracefully.
```

**Then:**
```
/clarify
```

**Then:**
```
/strategize Compare different approaches: Node.js with Express, Python with Flask/FastAPI, Go with Gin, or Rust with Actix
```

**Then:**
```
/plan Use Python with FastAPI for the calculator API, including validation, error handling, and basic authentication
```

**Then:**
```
/tasks
```

**Then:**
```
/analyze
```

**Finally:**
```
/implement
```

## How It Actually Works

1. **`goal init`** creates basic project structure with `.goals`, `.strategies`, and `.plans` directories
2. **The AI assistant** (Qwen Code, Claude, etc.) understands the goal-driven development methodology and responds to slash commands
3. **Slash commands** are special directives that the AI assistant recognizes and processes according to the goal-driven methodology
4. **The AI** generates code, documentation, and project artifacts based on the goal-driven process

## The Key Insight

The slash commands don't work in a regular command line terminal - they only work within AI coding assistants that are specifically designed to recognize and process these commands. The `goal init` command creates the basic project structure, then the AI assistant provides the goal-driven functionality when you use slash commands.

## Alternative: CLI-Only Usage

The current CLI implementation provides basic functionality. The full goal-driven development experience with slash commands requires an AI coding assistant:

```bash
# After initialization with CLI
goal goals
goal clarify  
goal strategize
goal plan
goal tasks
goal implement
```

But the full goal-driven experience with advanced slash commands (`/constitution`, `/analyze`, etc.) requires an AI coding environment that understands the goal-driven methodology.