# Goalify CLI - Goal-Driven Development with AI Integration

Goalify is a command-line tool that enables goal-driven development methodology with AI assistant integration. It creates agent-specific configuration files that allow AI coding assistants to understand and process goal-driven development slash commands.

## Installation and Setup

```bash
uv tool install .
```

This installs the `goalify` command.

## Quick Start

To create a project with Qwen Code integration:

```bash
goalify init my-project --ai qwen
cd my-project
```

This creates:
- Project structure with `.goals/`, `.strategies/`, `.plans/` directories
- Agent configuration in `.qwen/commands/` with TOML files for slash commands
- Templates and documentation for goal-driven development

## How It Works

1. **Agent Configuration**: When you run `goalify init --ai [agent]`, it creates agent-specific command configuration files
2. **Command Formats**: 
   - Qwen/Gemini: TOML format in `.qwen/commands/` or `.gemini/commands/`
   - Claude/Cursor: Markdown format in `.claude/commands/` or `.cursor/commands/`
3. **Slash Commands**: AI assistants use these configuration files to understand commands like `/goals`, `/strategize`, etc.
4. **Goal-Driven Flow**: Follow the methodology: constitution → goals → clarify → strategize → plan → tasks → analyze → implement

## Supported AI Agents

- Qwen Code (`.qwen/commands/` - TOML format)
- Claude Code (`.claude/commands/` - Markdown format) 
- Cursor (`.cursor/commands/` - Markdown format)
- Gemini CLI (`.gemini/commands/` - TOML format)
- And many others...

## Using with AI Assistants

After initialization with your chosen AI agent:

1. Open the project in your AI coding environment (Qwen Code, Claude, Cursor, etc.)
2. Use slash commands like `/goals`, `/strategize`, `/plan`, etc.
3. The AI assistant will process these commands based on the configuration files
4. Files will be created in appropriate directories (`.goals/`, `.strategies/`, etc.)

## CLI vs AI Assistant Commands

- **Terminal CLI**: `goalify init`, `goalify check`, `goalify goals` (basic file listing)
- **AI Assistant**: `/goals`, `/strategize`, `/plan` (full goal-driven workflow with AI assistance)

## Commands Available

- `/constitution` - Create project principles and guidelines
- `/goals` - Define project outcomes and objectives  
- `/clarify` - Refine and validate requirements
- `/strategize` - Evaluate implementation approaches
- `/plan` - Create technical implementation plans
- `/tasks` - Generate actionable tasks
- `/analyze` - Check consistency and alignment
- `/implement` - Execute implementation

## Workflow

The complete workflow follows goal-driven development methodology:
1. Establish project constitution and principles
2. Define clear goals and outcomes
3. Clarify requirements and resolve ambiguities
4. Strategize and evaluate approaches
5. Plan technical implementation
6. Break down into tasks
7. Analyze consistency
8. Implement according to plan