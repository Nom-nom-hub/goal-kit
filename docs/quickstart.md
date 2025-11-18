---
layout: default
title: Goal Kit Quick Start Guide
---

# Goal Kit Quick Start Guide

Get up and running with Goal-Driven Development in 5 minutes.

## Installation

### Using uv (Recommended)

From GitHub:
```bash
uv tool install --from git+https://github.com/Nom-nom-hub/goal-kit.git goalkeeper
```

From local repo:
```bash
cd /path/to/goal-kit
uv tool install --from . goalkeeper
```

### One-Time Usage

```bash
uv run --from git+https://github.com/Nom-nom-hub/goal-kit.git goalkeeper init my-project
```

### From Source

```bash
git clone https://github.com/Nom-nom-hub/goal-kit.git
cd goal-kit
pip install -e .
```

## Initialize Your Project

After installation, initialize a Goal Kit project:

```bash
# Create and initialize project
goalkeeper init my-awesome-project
cd my-awesome-project
```

This creates:
- `.goalkit/` - Configuration and vision file
- `goals/` - Directory for goal definitions
- Agent-specific context files (CLAUDE.md, etc.)

## Your First Goal (5 Minutes)

### Step 1: Define Your Vision (1 minute)

Ask your AI agent:

```
/goalkit.vision

Create a vision for this project focused on:
- Clear measurable outcomes
- Target users and their needs
- Key success principles
```

### Step 2: Create Your First Goal (2 minutes)

Ask your AI agent:

```
/goalkit.goal Build user authentication

Create a goal with:
- What success looks like (measurable outcomes)
- Who will use it (target users)
- Key metrics to measure success
```

You'll get a goal directory: `.goalkit/goals/001-build-user-authentication/`

### Step 3: Explore Strategies (1 minute)

Ask your AI agent:

```
/goalkit.strategies .goalkit/goals/001-build-user-authentication

Analyze 3-4 different approaches:
- OAuth integration (industry standard)
- Session-based authentication (simpler)
- JWT tokens (stateless option)

Compare on: feasibility, effort, learning potential
```

### Step 4: Create Milestones (1 minute)

Ask your AI agent:

```
/goalkit.milestones .goalkit/goals/001-build-user-authentication

Break into measurable progress steps:
1. Technical approach validation
2. Working prototype
3. User testing
4. Production deployment

Focus on learning at each step.
```

## Start Development

Now you're ready to implement! Ask your AI agent:

```
/goalkit.execute .goalkit/goals/001-build-user-authentication

Implement the first milestone with:
- Daily progress measurement
- Weekly strategy reviews
- Documentation of learnings
- Willingness to pivot if needed
```

## Key Concepts

### Goals vs Tasks

- **Goals**: Measurable outcomes (e.g., "Reduce login time by 50%")
- **Tasks**: Implementation activities (e.g., "Optimize database queries")

Goal Kit focuses on goals. Tasks emerge from strategies.

### The Five Commands

| Command | Purpose | When to Use |
|---------|---------|------------|
| `/goalkit.vision` | Project principles | At project start |
| `/goalkit.goal` | Define measurable outcomes | When starting a feature |
| `/goalkit.strategies` | Explore multiple approaches | Before implementation |
| `/goalkit.milestones` | Create progress checkpoints | After choosing strategy |
| `/goalkit.execute` | Implement with learning | When ready to build |

### Success Metrics

Good goals have **SMART** metrics:

- **Specific**: Exactly what you're measuring
- **Measurable**: Quantifiable (%, time, count)
- **Achievable**: Realistic within timeframe
- **Relevant**: Connected to project outcomes
- **Time-bound**: Clear deadline

❌ Bad: "Make authentication better"
✅ Good: "Reduce login time to <2 seconds for 95% of users"

## Common Workflows

### Simple Feature (Direct Implementation)

For straightforward tasks, you can go direct to execution:

```
/goalkit.goal Add dark mode toggle
/goalkit.execute .goalkit/goals/001-add-dark-mode-toggle
```

### Complex Feature (Full Methodology)

For features with unknowns:

```
/goalkit.goal Implement payment processing
/goalkit.strategies [goal_dir] - Explore Stripe vs Square vs custom
/goalkit.milestones [goal_dir] - Break into validation steps
/goalkit.execute [goal_dir] - Begin implementation
```

### Team Collaboration

1. One person creates the goal with measurable outcomes
2. Team discusses strategies together
3. Teams assign milestones to different people
4. Daily standups share learning, not tasks

## File Structure

```
my-awesome-project/
├── .goalkit/
│   ├── vision.md                    # Project vision & principles
│   └── goals/
│       ├── 001-goal-name/
│       │   ├── goal.md              # Goal definition & success metrics
│       │   ├── strategies.md        # Multiple implementation approaches
│       │   ├── milestones.md        # Progress checkpoints
│       │   └── execution.md         # Implementation plan & learnings
│       └── 002-next-goal/
│           ├── goal.md
│           ├── strategies.md
│           ├── milestones.md
│           └── execution.md
├── CLAUDE.md                        # Agent context (Claude)
├── CURSOR.md                        # Agent context (Cursor)
├── GEMINI.md                        # Agent context (Gemini)
└── ... (source code files)
```

## Tips & Best Practices

### 1. Write Measurable Goals

❌ "Improve user experience"
✅ "Reduce support tickets by 30% through better onboarding"

### 2. Explore Strategies Early

Don't assume the first idea is best. Always explore alternatives.

### 3. Measure Before Implementing

Define success metrics in the goal, not after building.

### 4. Document Learnings

Record what works, what doesn't, and why. This creates organizational knowledge.

### 5. Be Ready to Pivot

If metrics show a strategy isn't working, change course quickly.

### 6. Review Regularly

Weekly reviews prevent you from pursuing failed strategies too long.

## Troubleshooting

### Commands Not Found

Ensure Goal Kit is installed:
```bash
goalkeeper --version
```

### Agent Context Not Updating

Manually trigger context update:

**Linux/macOS:**
```bash
bash scripts/bash/common.sh && update-agent-context
```

**Windows:**
```powershell
. scripts/powershell/common.ps1; Update-AgentContext
```

### Goal Directory Issues

Verify structure:
```bash
ls .goalkit/goals/
```

Each goal directory should have: `goal.md`, `strategies.md`, `milestones.md`, `execution.md`

### Git Branch Problems

Ensure you're in a git repository:
```bash
git status
```

Goal Kit requires git for branch management.

## What's Next?

- 📖 Read [Goal-Driven Development Methodology](./goal-driven.md) for deep dive
- 💡 See [Practical Examples](./examples.md) for real-world scenarios
- 🔍 Check [Command Reference](./toc.md) for detailed docs
- 🤝 Compare with [Traditional Approaches](./comparison.md)

## Need Help?

- Check [Goal Kit GitHub Issues](https://github.com/Nom-nom-hub/goal-kit/issues)
- Read the [Troubleshooting Guide](./troubleshooting.md)
- Review [Examples](./examples.md) for your use case

---

**Ready to transform your development process?** Let's start with your first goal!

Next step: Ask your AI agent to `/goalkit.vision` for your project.
