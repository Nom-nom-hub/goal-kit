# [PROJECT NAME] - Goal-Driven Development Guide

**Auto-generated for agents. Last updated: [DATE]**

## 🎯 Goal-Driven Methodology

### **🚨 CRITICAL: Always follow this 5-step sequence - ONE COMMAND AT A TIME:**

**🛑 AGENTS MUST STOP AFTER EACH COMMAND - WAIT FOR USER**

1. **`/goalkit.vision`** - Establish project vision and principles → **🛑 STOP**
2. **User runs** `/goalkit.goal`** - Define goals with measurable outcomes → **🛑 STOP**
3. **User runs** `/goalkit.strategies`** - Explore multiple implementation approaches → **🛑 STOP**
4. **User runs** `/goalkit.milestones`** - Create measurable progress checkpoints → **🛑 STOP**
5. **User runs** `/goalkit.execute`** - Implement with learning and adaptation → **🛑 STOP**

**❌ FORBIDDEN: DO NOT chain commands automatically**
**❌ FORBIDDEN: DO NOT proceed to coding after vision**
**❌ FORBIDDEN: DO NOT skip steps in the sequence**

### **🔒 WORKFLOW ENFORCEMENT: Script Execution Required**

**🚨 MANDATORY: ALL goal operations MUST use Python scripts FIRST**

**Before ANY goal-related action, you MUST run the appropriate Python script:**

```bash
# For goal creation (ALWAYS run this first)
python scripts/python/create_new_goal.py --json "Your goal description"

# For validation (run before proceeding)
python scripts/python/enhanced_validator.py

# For progress tracking (run during execution)
python scripts/python/progress_tracker.py

# For workflow compliance checking (run anytime)
python scripts/python/workflow_enforcer.py --check
```

**⚠️ CRITICAL VIOLATIONS TO AVOID:**
- ❌ **NEVER manually create goal directories** - This breaks methodology compliance
- ❌ **NEVER skip the --json flag** - Required for proper integration
- ❌ **NEVER bypass script execution** - Scripts handle git branches, file structure, and context updates

### **Simple Tasks vs Complex Goals**
- **Simple tasks** (direct implementation): "fix styling", "update header", "add margin"
- **Complex goals** (use full methodology): features with measurable outcomes (%,$,timeframes,user counts)

## 📋 Available Commands

### Core Workflow Commands
| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/goalkit.vision` | Establish project foundation | Start of new project |
| `/goalkit.goal` | Define measurable goals | After vision is set |
| `/goalkit.strategies` | Explore multiple approaches | After goal is defined |
| `/goalkit.milestones` | Create progress checkpoints | After strategies chosen |
| `/goalkit.execute` | Implement with learning | After milestones created |

### Quality & Progress Commands (New!)
| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/goalkit.validate` | Enhanced validation with quality scoring | After creating components, before proceeding |
| `/goalkit.progress` | Progress tracking and analytics | During execution, stakeholder updates |
| `/goalkit.context` | Smart context management | After major changes, phase transitions |

## 🚨 Critical Rules

### **For Goals:**
✅ **DO**: Focus on measurable outcomes (%, $, timeframes, user counts)
✅ **DO**: Include specific success targets
✅ **DO**: Identify target users and stakeholders
✅ **DO**: **ALWAYS** run the Python script first: `.goalkit/scripts/python/create_new_goal.py --json "{ARGS}"`
❌ **DON'T**: Include implementation details (languages, frameworks, APIs)
❌ **DON'T**: Manually create goal directories - this bypasses proper methodology
❌ **DON'T**: Skip the automated goal creation script

### **For Strategies:**
✅ **DO**: Explore 3+ different approaches
✅ **DO**: Compare feasibility, effort, risk, learning potential
✅ **DO**: Frame as testable hypotheses
❌ **DON'T**: Focus on just one "correct" solution

### **For Milestones:**
✅ **DO**: Create measurable progress indicators
✅ **DO**: Include clear success criteria
✅ **DO**: Focus on learning and validation
❌ **DON'T**: Create implementation task lists

### **For Execution:**
✅ **DO**: Focus on learning and adaptation
✅ **DO**: Measure progress continuously
✅ **DO**: Document insights and knowledge gained
❌ **DON'T**: Follow rigid, untested plans

## 🎯 Active Goals
[EXTRACTED FROM ALL GOAL.MD FILES]

## 📊 Project Status
- **Goals Created**: [Number of goals in .goalkit/goals/ directory]
- **Strategies Defined**: [Number of strategy files]
- **Milestones Set**: [Number of milestone files]
- **Current Branch**: [Current git branch]

## 📋 Goal Creation: Proper Process

**🚨 ENFORCED REQUIREMENT: When creating goals, ALWAYS follow this exact sequence:**

**STEP 1: Run the Python script FIRST (MANDATORY):**
```bash
cd "{PROJECT_ROOT}"
python scripts/python/create_new_goal.py --json "{ARGS}"
```

**⚠️ CRITICAL: The --json flag is REQUIRED for proper workflow integration**

**STEP 2: Parse the JSON output** to get:
- `GOAL_DIR`: Goal directory path (e.g., `.goalkit/goals/001-user-authentication/`)
- `BRANCH_NAME`: Git branch name (e.g., `001-user-authentication`)
- `GOAL_FILE`: Path to goal.md file

**STEP 3: Complete the goal definition** in the script-generated `GOAL_FILE`

**STEP 4: Follow with `/goalkit.strategies`** to explore approaches

**🚨 WORKFLOW VIOLATION CHECKS:**
- **Script Execution Verification**: Workflow enforcer validates script was used
- **Structure Compliance**: Ensures proper directory and file structure
- **Branch Management**: Verifies goal-specific git branch creation
- **Context Updates**: Confirms agent context was properly updated

**⚠️ NEVER manually create goal directories** - this breaks:
- Proper numbering (001-, 002-, etc.)
- Git branch management
- Template structure
- Agent context updates
- **Workflow compliance** (will be detected by enforcer)

## 🔧 Next Recommended Actions

**If no goals exist:**
1. Use `/goalkit.vision` to establish project vision
2. Use `/goalkit.goal` to define first goal

**If goals exist but no strategies:**
1. Use `/goalkit.validate` to check goal quality (7.0+ score required)
2. Use `/goalkit.strategies` to explore approaches

**If strategies exist but no milestones:**
1. Use `/goalkit.validate` to verify strategy quality
2. Use `/goalkit.milestones` to create checkpoints

**If milestones exist:**
1. Use `/goalkit.progress` to check current status
2. Use `/goalkit.execute` to implement with learning

**For ongoing projects:**
- Use `/goalkit.validate` regularly to maintain quality
- Use `/goalkit.progress` to track advancement and identify issues
- Use `/goalkit.context` to keep agent guidance current
- **Run workflow compliance checks**: `python scripts/python/workflow_enforcer.py --check`

## 💡 Agent Best Practices

### **🚨 CRITICAL Workflow Enforcement:**
- **🛑 STOP after each command** - Never chain commands automatically
- **Wait for user input** - Only proceed when user runs next command explicitly
- **One command at a time** - Complete full methodology sequence step by step
- **No automatic progression** - User must trigger each methodology step

### **📊 Enhanced Quality & Progress Integration:**
- **Quality Gates**: Use `/goalkit.validate` to check component quality before proceeding
- **Progress Tracking**: Use `/goalkit.progress` to monitor advancement and identify issues
- **Smart Context**: Use `/goalkit.context` to maintain current project intelligence
- **Learning Capture**: Use `/goalkit.learn` to capture insights and patterns

### **Python Script Development:**
- **Validate syntax**: `python -m py_compile script_name.py` before changes
- **Check git status**: `git status`, `git diff` before modifying
- **Safe editing**: Use targeted edits, not full file overwrites
- **Cross-platform**: Use `os.path` or `pathlib` for file paths
- **Workflow compliance**: Run `python scripts/python/workflow_enforcer.py --check` after script changes

### **Goal Kit Workflow:**
- **Always remind** users of next steps after each command
- **Follow sequence** - don't skip methodology steps
- **Focus on outcomes** - not implementation details
- **Document learnings** - capture insights throughout process
- **🛑 STOP after completion** - Wait for user's next command

### **🚨 FORBIDDEN AGENT BEHAVIORS - DO NOT DO THESE:**

**❌ STOP: Chaining commands automatically**
- ❌ Running `/goalkit.goal` after `/goalkit.vision` without user input
- ❌ Running `/goalkit.strategies` after `/goalkit.goal` automatically
- ❌ Proceeding through multiple methodology steps in one response

**❌ STOP: Starting implementation too early**
- ❌ Creating files or code after vision creation
- ❌ Starting coding without completing full methodology sequence
- ❌ Implementing features before defining goals and strategies

**❌ STOP: Bypassing methodology steps**
- ❌ Skipping the goal creation step
- ❌ Skipping strategy exploration phase
- ❌ Moving directly from vision to execution

**❌ STOP: Violating script execution requirements**
- ❌ Manually creating goal directories (ALWAYS use Python scripts)
- ❌ Skipping the --json flag when running goal creation scripts
- ❌ Bypassing workflow validation and compliance checks
- ❌ Ignoring workflow enforcer recommendations and violations

**✅ ALLOWED: Only these specific actions**
- ✅ Creating vision file after `/goalkit.vision` → **STOP**
- ✅ Running Python scripts with proper --json flags after `/goalkit.goal` → **STOP**
- ✅ Creating strategy files after `/goalkit.strategies` → **STOP**
- ✅ Creating milestone files after `/goalkit.milestones` → **STOP**
- ✅ Starting implementation after `/goalkit.execute` → **Continue with learning**
- ✅ Running workflow compliance checks with `python scripts/python/workflow_enforcer.py --check`

### **Common Pitfalls to Avoid:**
- ❌ Skipping strategy exploration
- ❌ Adding implementation details to goals
- ❌ Creating goals without measurable targets
- ❌ Treating as traditional requirement-driven development
- ❌ **Manually creating goal directories** - Always use the Python script first
- ❌ **Bypassing the automated goal creation process** - This breaks methodology compliance
- ❌ **Skipping the --json flag** - Required for proper workflow integration
- ❌ **Ignoring workflow enforcer violations** - Address compliance issues promptly
- ❌ **Bypassing script execution requirements** - Scripts handle critical automation

## 📚 Key Principles

1. **Outcome-First**: Prioritize user and business outcomes
2. **Strategy Flexibility**: Multiple valid approaches exist for any goal
3. **Measurement-Driven**: Progress must be measured and validated
4. **Learning Integration**: Treat implementation as hypothesis testing
5. **Adaptive Planning**: Change course based on evidence

---

*This guide is automatically created by goalkeeper init. It provides essential guidance for agents working on this Goal Kit project.*