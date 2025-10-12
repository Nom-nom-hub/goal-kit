# Goal Kit Agent Configuration

**Project**: [PROJECT_NAME]
**Created**: [DATE]
**Goal-Driven Development**: Enabled

## 🤖 AI Agent Setup

This file configures your AI agent for goal-driven development with Goal Kit.

### Supported Agents

| Agent | Setup Command | Configuration |
|-------|---------------|---------------|
| **Claude Code** | `claude init` | `.claude/` directory |
| **GitHub Copilot** | VS Code Extension | `.github/` policies |
| **Cursor** | `cursor setup` | `.cursor/` config |
| **Windsurf** | `windsurf init` | `.windsurf/` workspace |
| **Kilo Code** | `kilo setup` | `.kilocode/` settings |

## 🎯 Goal-Driven Development Commands

### Core Commands
- **`/goalkit.vision`** - Establish project vision and principles
- **`/goalkit.goal`** - Define goals and success criteria
- **`/goalkit.strategies`** - Explore implementation strategies
- **`/goalkit.milestones`** - Create measurable milestones
- **`/goalkit.execute`** - Execute with learning and adaptation

### Enhancement Commands
- **`/goalkit.explore`** - Dive deeper into strategy options
- **`/goalkit.measure`** - Define measurement frameworks
- **`/goalkit.adapt`** - Adjust strategies based on learning

## 📋 Development Workflow

### 1. Project Setup
```bash
# Initialize project with vision
/goalkit.vision [project vision and principles]

# Create first goal
/goalkit.goal [goal description and success criteria]
```

### 2. Strategy Development
```bash
# Explore implementation approaches
/goalkit.strategies [strategy exploration request]

# Define measurable milestones
/goalkit.milestones [milestone planning request]
```

### 3. Adaptive Execution
```bash
# Execute with learning focus
/goalkit.execute [execution approach and learning focus]

# Adapt based on results
/goalkit.adapt [adaptation requirements]
```

## 🔧 Agent-Specific Configuration

### Claude Code Setup
```bash
# In your project directory with Claude Code
/goalkit.vision Create project vision...
/goalkit.goal Define first goal...
```

### Cursor Setup
```bash
# In Cursor IDE
/goalkit.vision [project vision]
/goalkit.goal [goal definition]
```

### VS Code with GitHub Copilot
```bash
# In VS Code with Copilot extension
/goalkit.vision [project vision]
/goalkit.goal [goal definition]
```

## 📁 Project Structure

```
project/
├── .goalkit/
│   └── vision.md              # Project vision and principles
├── goals/
│   ├── 001-user-onboarding/   # First goal
│   │   ├── goal.md           # Goal definition
│   │   ├── strategies.md     # Strategy exploration
│   │   ├── milestones.md     # Measurable milestones
│   │   ├── execution.md      # Adaptive execution guide
│   │   └── exploration.md    # In-depth analysis and exploration
│   └── 002-user-engagement/   # Second goal
│       └── goal.md
└── src/                      # Implementation code
```

## 🛠️ Agent File Operations

When handling Goal Kit slash commands, AI agents should perform these file operations:

1. **`/goalkit.vision`**: Create or update `.goalkit/vision.md`
2. **`/goalkit.goal`**: Create `goals/[###-goal-name]/goal.md` directory and file
3. **`/goalkit.strategies`**: Create `goals/[###-goal-name]/strategies.md` in the relevant goal directory
4. **`/goalkit.milestones`**: Create `goals/[###-goal-name]/milestones.md` in the relevant goal directory
5. **`/goalkit.execute`**: Create `goals/[###-goal-name]/execution.md` in the relevant goal directory
6. **`/goalkit.explore`**: May update or create `goals/[###-goal-name]/exploration.md` if exploration is goal-specific

### Required Tools for File Creation
- Use `write_file` or `edit` commands to create and modify files
- Use appropriate directory creation commands if needed
- Ensure proper file extensions (.md for markdown documents)
- Follow the naming conventions: `[###-goal-name]` with leading zeros for directory names

## 🎯 Goal-Driven Principles

### Focus Areas
- **Outcome-First**: Prioritize user and business outcomes
- **Multiple Strategies**: Explore different approaches to goals
- **Measurable Progress**: Define clear success indicators
- **Learning Integration**: Treat implementation as hypothesis testing
- **Adaptive Planning**: Change course based on evidence

### Success Metrics
- **User Outcomes**: Measurable user benefits achieved
- **Business Value**: Quantifiable business impact delivered
- **Learning Quality**: Insights gained and documented
- **Process Improvement**: Development practices enhanced

## 🚀 Quick Start Commands

### For New Projects
```bash
/goalkit.vision Create vision for [project type] focused on [user outcomes] with [business goals]
/goalkit.goal [specific goal] with success criteria: [metrics]
```

### For Existing Goals
```bash
/goalkit.strategies Explore [technical|UX|implementation] strategies for [goal]
/goalkit.milestones Create milestones that validate [hypotheses] and measure [outcomes]
```

## 📊 Progress Tracking

### Goal Status Indicators
- **Draft**: Goal definition in progress
- **Active**: Strategy exploration and milestone planning
- **Executing**: Implementation with measurement and learning
- **Complete**: Success criteria met and validated
- **On Hold**: Temporarily paused for strategic reasons

### Learning Documentation
- **Technical Insights**: Implementation approaches and patterns
- **User Feedback**: Behavior patterns and preference data
- **Process Learning**: Development methodology improvements
- **Risk Management**: Issues encountered and mitigation strategies

## 🔄 Review Cadence

### Daily Standup
- What milestone actions were completed?
- What learning was captured?
- What adjustments are needed?

### Weekly Review
- Are strategies producing expected outcomes?
- Do milestones need adjustment?
- Is progress toward goal achievement on track?

### Monthly Assessment
- Are goals still relevant and valuable?
- Should strategies be adapted or changed?
- What broader learning applies to future goals?

---

*This agent configuration file helps set up your AI coding environment for goal-driven development. Update it as your project evolves and new agents are added.*