# Example: Simple Todo App with Goal-Driven Development

This is an example project that demonstrates how to use Goal Kit with AI coding assistants. This project will be used to show the goal-driven development process.

## What This Example Shows

This example demonstrates how to use the Goal Kit framework with AI coding assistants like:
- Qwen Code (the IDE environment that supports slash commands)
- Claude Code
- GitHub Copilot
- Cursor
- Other AI coding environments

## Important: Understanding the AI Agent Context

The slash commands (`/constitution`, `/goals`, etc.) are meant to be used within AI coding assistant environments, NOT in a regular terminal. The AI agent needs to be "aware" of these special commands in order to process them.

## Prerequisites to Run This Example

1. Install Goal CLI: 
   ```
   uv tool install goal-cli --from git+https://github.com/nom-nom-hub/goal-dev-kit.git
   ```

2. Have an AI coding assistant that supports slash commands (like Qwen Code, Claude, Cursor, etc.)

## How to Use This Example

1. Initialize this example project:
   ```
   goal init todo-app
   cd todo-app
   ```

2. Open the project in an AI coding assistant environment (like Qwen Code, Cursor, etc.)

3. In the AI assistant chat/terminal, you can now use slash commands:

   - `/constitution` - Set up project principles
   - `/goals` - Define what you want to build
   - `/clarify` - Clarify requirements
   - `/strategize` - Plan implementation approaches
   - `/plan` - Create technical plan
   - `/tasks` - Generate tasks
   - `/analyze` - Check consistency
   - `/implement` - Execute the implementation

## What Actually Happens

When you use `goal init --ai qwen`, it creates:
- Template files that the AI agent understands
- Configuration that makes the slash commands available
- Project structure following goal-driven methodology

The AI agent interprets these slash commands and follows the goal-driven workflow using the templates and guidelines provided by Goal Kit.

## Troubleshooting

- If slash commands don't work: Make sure you're using an AI coding environment (not regular terminal)
- If commands are not recognized: Ensure you initialized with the correct AI agent option
- If you're using a regular terminal: The slash commands won't work there

## Next Steps

See the USAGE.md file in the main repository for detailed instructions on how to set up your AI coding environment to work with these slash commands.