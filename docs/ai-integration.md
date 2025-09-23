# AI Integration

Goal-Dev-Spec integrates with multiple AI agents to help generate and refine your specifications:

- **Claude Code** - Anthropic's coding assistant
- **Gemini CLI** - Google's AI assistant
- **GitHub Copilot** - AI pair programmer
- **Cursor** - AI-first code editor
- **Qwen Code** - Alibaba's coding assistant
- **opencode** - Open-source coding assistant
- **Codex CLI** - OpenAI's coding assistant
- **Windsurf** - AI-powered IDE
- **Kilo Code** - AI development platform
- **Auggie CLI** - Augmented coding assistant

## During Project Initialization

During project initialization, you'll be prompted to select your preferred AI agent:

```bash
goal init my-project
```

Each agent has its own strengths and integration capabilities.

## AI Commands

Goal-Dev-Spec provides several AI-assisted commands:

```bash
# Generate code for a specification using AI assistance
goal code generate SPEC_ID

# Review existing code with AI assistance
goal code review FILE_PATH

# Refactor code with AI assistance
goal code refactor FILE_PATH

# Explain code functionality with AI assistance
goal code explain FILE_PATH
```