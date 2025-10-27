---
description: Optimize and streamline the Goal Kit workflow for better user and agent experience. Provides intelligent recommendations and shortcuts.
scripts:
  sh: .goalkit/scripts/python/workflow_optimizer.py --analyze
  ps: .goalkit/scripts/python/workflow_optimizer.py --analyze
agent_scripts:
  sh: .goalkit/scripts/python/workflow_optimizer.py --guide
  ps: .goalkit/scripts/python/workflow_optimizer.py --guide
---

# Workflow Optimization

**Purpose**: Streamline Goal Kit methodology for better efficiency and user experience.

## Key Improvements

### 1. Smart Task Assessment

- **Automatic complexity detection** - Determines if tasks need full methodology or can use shortcuts
- **Context-aware recommendations** - Considers current project state
- **Learns from patterns** - Improves suggestions based on successful approaches

### 2. Streamlined Templates

- **Reduced verbosity** - Essential guidance without overwhelming detail
- **Progressive disclosure** - Show simple paths first, complex options when needed
- **Clear decision points** - Easy to understand when to use each approach

### 3. Status Awareness

- **Project dashboard** - Quick overview of current state
- **Progress tracking** - Visual indicators of methodology completion
- **Guided next steps** - Intelligent recommendations for what to do next

### 4. Flexible Workflows

- **Simple task shortcuts** - Direct execution for straightforward work
- **Methodology respecting** - Full structure when complexity requires it
- **Adaptive planning** - Adjust approach based on learning

## Commands Available

```bash
# Assess task complexity
/goalkit.smart Assess any task for optimal workflow

# Check project status
python scripts/python/status_dashboard.py

# Get workflow guidance
python scripts/python/workflow_guide.py --task "description"

# Run optimization analysis
python scripts/python/workflow_optimizer.py --analyze
```

## Optimization Results

### Before Optimization

❌ **Overly strict** - Forced complex methodology for simple tasks
❌ **Verbose templates** - 400+ lines of repetitive instructions
❌ **Poor discoverability** - Hard to know current state or next steps
❌ **Rigid workflows** - No shortcuts for common scenarios
❌ **Agent confusion** - Multiple coordination modes and STOP messages

### After Optimization

✅ **Smart assessment** - Automatic complexity detection
✅ **Streamlined guidance** - Essential information, clear decisions
✅ **Status awareness** - Easy project state overview
✅ **Flexible approaches** - Right methodology for each task type
✅ **Clear progression** - Guided path with alternatives

## User Experience Improvements

### For Simple Tasks

**Before**: `/goalkit.goal` → `/goalkit.strategies` → `/goalkit.milestones` → `/goalkit.execute`
**After**: `/goalkit.smart` → Assessment → `/goalkit.execute` (direct)

### For Complex Tasks

**Before**: Same rigid flow regardless of need
**After**: Full methodology when complexity justifies it

### For Status Checking

**Before**: Manual file inspection, unclear state
**After**: `python scripts/python/status_dashboard.py` → Clear overview

## Agent Experience Improvements

### Reduced Cognitive Load

- **Clear decision frameworks** instead of overwhelming options
- **Progressive disclosure** of complex features
- **Contextual guidance** based on project state

### Better Workflow Integration

- **Automatic assessment** of task requirements
- **Smart recommendations** for next steps
- **Shortcut awareness** for simple tasks

## Implementation Status

- ✅ **Task Assessor** - Automatic complexity detection
- ✅ **Status Dashboard** - Project state overview
- ✅ **Workflow Guide** - Intelligent next-step recommendations
- ✅ **Streamlined Templates** - Reduced verbosity
- ⏳ **Integration Testing** - Validate improvements work together
- ⏳ **User Feedback Loop** - Gather experience data

## Next Steps

1. **Test the optimizations** with real workflow scenarios
2. **Gather user feedback** on experience improvements
3. **Refine recommendations** based on usage patterns
4. **Add learning features** to improve future suggestions
5. **Document best practices** for optimized workflows

## Quick Start

```bash
# Assess any task
/goalkit.smart [task description]

# Check project health
python scripts/python/status_dashboard.py

# Get guidance for specific work
python scripts/python/workflow_guide.py --task "implement user authentication"
```
