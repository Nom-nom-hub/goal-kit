---
description: Intelligent workflow guidance that assesses task complexity and recommends the optimal development approach.
scripts:
  sh: .goalkit/scripts/python/task_assessor.py --json "{ARGS}"
  ps: .goalkit/scripts/python/task_assessor.py --json "{ARGS}"
agent_scripts:
  sh: .goalkit/scripts/python/workflow_guide.py --task "{ARGS}"
  ps: .goalkit/scripts/python/workflow_guide.py --task "{ARGS}"
---

# Smart Workflow Guidance

**Task**: `{ARGS}`

## Intelligent Assessment Process

1. **Analyze task complexity** using automated assessment
2. **Check current project state** and available shortcuts
3. **Recommend optimal workflow** path
4. **Provide clear next steps** with reasoning

## How It Works

The system automatically determines whether your task needs:

- **Direct execution** (simple tasks like "fix button styling")
- **Basic methodology** (goal → execute)
- **Full methodology** (vision → goal → strategies → milestones → execute)

## Assessment Factors

- **Task keywords** (simple vs complex indicators)
- **Length and structure** (word count, multiple steps)
- **Project context** (existing vision, goals, milestones)
- **Success patterns** (learned from previous work)

## Quick Commands

```bash
# Assess any task
/goalkit.smart Assess task complexity and get recommendations

# Check project status
python scripts/python/status_dashboard.py

# Get workflow guidance
python scripts/python/workflow_guide.py --task "your task description"
```

## Benefits

✅ **Reduces friction** - No more guessing which methodology to use
✅ **Speeds up simple tasks** - Direct execution for straightforward work
✅ **Maintains structure** - Full methodology when complexity requires it
✅ **Learns from experience** - Improves recommendations over time
✅ **Context-aware** - Considers current project state

## For Agents

When processing `/goalkit.smart` commands:

1. Run task assessment to get complexity analysis
2. Check project status for available shortcuts
3. Provide clear recommendation with reasoning
4. Guide user to appropriate next steps
5. **Don't force complex workflows** on simple tasks
