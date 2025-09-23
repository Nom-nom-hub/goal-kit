# Goal-Dev-Spec

A goal-driven development specification system using YAML files.

## Table of Contents

- [🤔 What is Goal-Driven Development?](#-what-is-goal-driven-development)
- [⚡ Get started](#-get-started)
- [🤖 Supported AI Agents](#-supported-ai-agents)
- [🔧 Goal CLI Reference](#-goal-cli-reference)
- [📚 Core philosophy](#-core-philosophy)
- [🌟 Development phases](#-development-phases)
- [🔧 Prerequisites](#-prerequisites)
- [📖 Learn more](#-learn-more)
- [👥 Maintainers](#-maintainers)
- [📄 License](#-license)

## 🤔 What is Goal-Driven Development?

Goal-Driven Development flips the script on traditional software development. For decades, code has been king — goals and specifications were just scaffolding we built and discarded once the "real work" of coding began. Goal-Driven Development changes this: **goals become executable**, directly generating working implementations rather than just guiding them.

Instead of starting with implementation details, Goal-Driven Development starts with clear, measurable objectives. Each goal is carefully crafted with:

- **Clear objectives** - What exactly needs to be accomplished
- **Success criteria** - How we'll know when we're done
- **Dependencies** - What other goals or systems this relies on
- **Stakeholders** - Who cares about this goal and why

This approach ensures that every line of code serves a clear purpose and contributes to measurable business outcomes.

## ⚡ Get started

### Option 1: Persistent Installation (Recommended)

Install once and use everywhere:

```bash
pip install -e .
```

Then use the tool directly:

```bash
goal init <PROJECT_NAME>
goal create "<GOAL_DESCRIPTION>"
```

### Option 2: One-time Usage

Run directly without installing:

```bash
python -m goal_cli init <PROJECT_NAME>
```

**Benefits of persistent installation:**

- Tool stays installed and available in PATH
- No need to create shell aliases
- Cleaner shell configuration

## Get started

### 1. Initialize a project

```bash
# Create a new project
goal init my-awesome-project

# Or initialize in the current directory
goal init --here
```

### 2. Create your first goal

```bash
# Navigate to your project
cd my-awesome-project

# Create a goal
goal create "Implement user authentication with login, registration, and password reset"
```

### 3. List and view goals

```bash
# List all goals
goal list

# Show details of a specific goal
goal show <goal-id>
```

### 4. Plan implementation

```bash
# Create an implementation plan for a goal
goal plan <goal-id>

# Generate task breakdown
goal tasks <plan-id>
```

### 5. Track progress

```bash
# Track progress of goals and tasks
goal track
```

## 🤖 Supported AI Agents

Goal-Dev-Spec works with multiple AI agents to help generate and refine your specifications:

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

During project initialization, you'll be prompted to select your preferred AI agent. Each agent has its own strengths and integration capabilities.

## 🔧 Goal CLI Reference

### `init` - Initialize a new Goal-Dev-Spec project

```bash
goal init [OPTIONS] [PROJECT_NAME]
```

Options:
- `--ai TEXT` - AI assistant to use (claude, gemini, copilot, cursor, qwen, opencode, codex, windsurf, kilocode, or auggie)
- `--script TEXT` - Script type to use (sh or ps)
- `--no-git` - Skip git repository initialization
- `--force` - Force creation even if directory exists
- `--here` - Initialize project in the current directory instead of creating a new one

### `create` - Create a new goal specification

```bash
goal create [OPTIONS] GOAL_DESCRIPTION
```

Creates a new goal with the specified description and automatically generates a corresponding feature specification.

### `plan` - Create an implementation plan for a goal

```bash
goal plan [OPTIONS] GOAL_ID
```

Generates an implementation plan for the specified goal, including tasks, timeline, and resource requirements.

### `tasks` - Generate task breakdown for implementation

```bash
goal tasks [OPTIONS] PLAN_ID
```

Breaks down an implementation plan into actionable tasks with assignees, due dates, and dependencies.

### `list` - List all goals in the project

```bash
goal list [OPTIONS]
```

Displays all goals in the current project with their status and creation dates.

### `show` - Show details of a specific goal

```bash
goal show [OPTIONS] GOAL_ID
```

Displays detailed information about a specific goal, including objectives, success criteria, and dependencies.

### `track` - Track progress of goals and tasks

```bash
goal track [OPTIONS]
```

Shows progress tracking information for all goals and tasks in the project.

### Global Options

- `--version` - Show version information
- `--help` - Show help information

## 📚 Core philosophy

Goal-Dev-Spec is built on several core principles:

### 1. Goals First, Code Second
Every software project should start with clearly defined goals before writing any code. This ensures that all development efforts are aligned with business objectives.

### 2. Measurable Success
Each goal must have clear, measurable success criteria. This allows teams to objectively determine when a goal has been achieved.

### 3. Stakeholder Alignment
Goals should clearly identify who benefits from their completion and why. This ensures that development efforts create real value.

### 4. Dependency Management
Complex projects require careful dependency tracking. Goal-Dev-Spec helps identify and manage goal dependencies to prevent blocking issues.

### 5. AI-Assisted Development
Modern AI tools can significantly accelerate the specification and implementation process. Goal-Dev-Spec integrates with multiple AI agents to leverage these capabilities.

## 🌟 Development phases

Goal-Dev-Spec guides teams through a structured development process:

### Phase 1: Goal Definition
- Define clear, measurable objectives
- Identify success criteria
- Determine stakeholders
- Map dependencies

### Phase 2: Specification Creation
- Generate detailed feature specifications
- Define user scenarios and acceptance criteria
- Identify functional and non-functional requirements

### Phase 3: Implementation Planning
- Create implementation plans
- Estimate effort and timeline
- Allocate resources
- Identify risks

### Phase 4: Task Breakdown
- Break plans into actionable tasks
- Assign owners and due dates
- Define dependencies
- Track progress

### Phase 5: Execution and Tracking
- Execute tasks
- Monitor progress
- Adjust plans as needed
- Measure success

## 🔧 Prerequisites

Before using Goal-Dev-Spec, ensure you have:

- Python 3.7 or higher
- pip package manager
- Git (optional, but recommended)
- Your preferred AI agent tool (optional, but recommended)

For AI agent integration, install the corresponding tool:

- Claude Code: [Installation Guide](https://docs.anthropic.com/en/docs/claude-code/setup)
- Gemini CLI: [Installation Guide](https://github.com/google-gemini/gemini-cli)
- Qwen Code: [Installation Guide](https://github.com/QwenLM/qwen-code)
- opencode: [Installation Guide](https://opencode.ai)
- Codex CLI: [Installation Guide](https://github.com/openai/codex)
- Auggie CLI: [Installation Guide](https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli)

## 📖 Learn more

### Project Structure

```
my-project/
├── goal.yaml              # Project configuration
├── .goal/                 # All goal-dev-spec files in one place
│   ├── goals/             # Goal specifications
│   │   ├── goals.yaml     # Goals index
│   │   └── <goal-id>/     # Individual goal directory
│   │       └── goal.yaml  # Goal specification
│   ├── specs/             # Feature specifications
│   │   └── <spec-id>/     # Individual spec directory
│   │       └── spec.yaml  # Feature specification
│   ├── plans/             # Implementation plans
│   ├── tasks/             # Task breakdowns
│   ├── templates/         # Templates (YAML and Markdown)
│   │   ├── md/            # Markdown templates
│   │   │   ├── commands/  # AI command templates
│   │   │   ├── goal-template.md
│   │   │   ├── spec-template.md
│   │   │   ├── plan-template.md
│   │   │   └── tasks-template.md
│   │   ├── goal-template.yaml # YAML goal template
│   │   ├── spec-template.yaml # YAML spec template
│   │   ├── plan-template.yaml # YAML plan template
│   │   └── tasks-template.yaml # YAML tasks template
│   └── agents/            # AI agent configurations
│       ├── claude/        # Claude configurations
│       └── gemini/        # Gemini configurations
├── scripts/               # Helper scripts
│   ├── bash/              # Bash scripts
│   └── powershell/        # PowerShell scripts
```

### Template System

Goal-Dev-Spec provides both YAML and Markdown templates for different use cases:

- **YAML templates** - For programmatic processing and validation
- **Markdown templates** - For human-readable specifications with execution flows and checklists

Both template types include structured sections to ensure comprehensive specification creation.

## 👥 Maintainers

- Kaiden - Lead Developer

## 📄 License

MIT License

Copyright (c) 2025 Goal-Dev-Spec Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.