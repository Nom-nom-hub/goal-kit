"""
Common utilities for Goal Kit Python scripts
"""
import os
import subprocess
import sys
import datetime
from pathlib import Path


def write_colored(message, color="white"):
    """
    Write colored output to the console
    """
    colors = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "cyan": "\033[36m",
        "magenta": "\033[35m",
        "white": "\033[37m",
        "reset": "\033[0m"
    }
    
    color_code = colors.get(color.lower(), colors["white"])
    reset_code = colors["reset"]
    print(f"{color_code}{message}{reset_code}")


def write_info(message):
    """Write info message in blue"""
    write_colored(f"[INFO] {message}", "blue")


def write_success(message):
    """Write success message in green"""
    write_colored(f"[SUCCESS] {message}", "green")


def write_warning(message):
    """Write warning message in yellow"""
    write_colored(f"[WARNING] {message}", "yellow")


def write_error(message):
    """Write error message in red"""
    write_colored(f"[ERROR] {message}", "red")


def write_step(message):
    """Write step message in cyan"""
    write_colored(f"[STEP] {message}", "cyan")


def write_goal(message):
    """Write goal message in magenta"""
    write_colored(f"[GOAL] {message}", "magenta")


def test_command_exists(command):
    """
    Check if a command exists in the system
    """
    try:
        subprocess.run([command, "--version"], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def test_git_repo():
    """
    Check if we're in a git repository
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            check=True,
            cwd=os.getcwd()
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_git_root():
    """
    Get the root directory of the current git repository
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            cwd=os.getcwd()
        )
        return result.stdout.decode().strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def test_prerequisites():
    """
    Check if required tools are installed
    """
    missing_tools = []
    
    if not test_command_exists("git"):
        missing_tools.append("git")
    
    if not test_command_exists("uv"):
        missing_tools.append("uv")
    
    if missing_tools:
        write_error(f"Missing required tools: {', '.join(missing_tools)}")
        write_info("Please install the missing tools and try again.")
        sys.exit(1)
    
    write_success("All prerequisites are installed")


def new_goal_branch(goal_name):
    """
    Create a new branch for the current goal
    """
    branch_name = goal_name
    
    # Check if branch already exists
    try:
        result = subprocess.run(
            ["git", "branch", "-a"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        existing_branches = result.stdout
        
        if branch_name in existing_branches:
            write_info(f"Branch {branch_name} already exists, switching to it")
            subprocess.run(["git", "checkout", branch_name], check=True)
        else:
            write_info(f"Creating new branch: {branch_name}")
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    except subprocess.CalledProcessError:
        write_error(f"Failed to create or switch to branch: {branch_name}")
        sys.exit(1)
    
    return branch_name


def update_agent_context():
    """
    Update the agent context file with current goal information
    """
    project_root = get_git_root()
    
    # Look for agent-specific context files
    context_files = [
        "CLAUDE.md",
        ".claude/context.md",
        "GEMINI.md", 
        ".gemini/context.md",
        "CURSOR.md",
        ".cursor/context.md",
        "QWEN.md",
        ".qwen/context.md",
        "WINDSURF.md",
        ".windsurf/context.md",
        "KILOCODE.md",
        ".kilocode/context.md",
        "ROO.md",
        ".roo/context.md",
        "CODEBUDDY.md",
        ".codebuddy/context.md",
        "Q.md",
        ".amazonq/context.md",
        "OPENCODE.md",
        "AUGMENT.md",
        ".augment/context.md"
    ]

    for context_file in context_files:
        full_path = os.path.join(project_root, context_file)
        if os.path.exists(full_path):
            write_info(f"Updating context in {context_file}")
            
            # Count active goals
            goals_dir = os.path.join(project_root, "goals")
            active_goals = 0
            if os.path.exists(goals_dir):
                active_goals = len([d for d in os.listdir(goals_dir) 
                                   if os.path.isdir(os.path.join(goals_dir, d))])
            
            # Get current branch
            try:
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                    text=True
                )
                current_branch = result.stdout.strip()
            except subprocess.CalledProcessError:
                current_branch = "unknown"
            
            context_content = f"""# Goal Kit Project Context

**Project**: {os.path.basename(project_root)}
**Branch**: {current_branch}
**Active Goals**: {active_goals}
**Updated**: {datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}

## 🎯 Goal-Driven Development Status

This project uses Goal-Driven Development methodology. Focus on:
- Measurable outcomes over feature specifications
- Multiple strategy exploration before implementation
- Learning and adaptation during execution
- Success metrics validation

## 📋 Available Commands

### Core Commands
- **/goalkit.vision** - Establish project vision and principles
- **/goalkit.goal** - Define goals and success criteria
- **/goalkit.strategies** - Explore implementation strategies
- **/goalkit.milestones** - Create measurable milestones
- **/goalkit.execute** - Execute with learning and adaptation


## 🚀 Project Vision

"""

            # Add vision content if it exists
            vision_path = os.path.join(project_root, ".goalkit", "vision.md")
            if os.path.exists(vision_path):
                with open(vision_path, 'r', encoding='utf-8') as f:
                    vision_content = f.read()
                    # Just take the first few lines of the vision
                    lines = vision_content.split('\n')[:10]
                    for line in lines:
                        if not line.startswith('#'):
                            context_content += f"{line}\n"

            context_content += f"""

## 🎯 Active Goals

"""

            # Add goal information if goals exist
            if os.path.exists(goals_dir):
                goal_dirs = [d for d in os.listdir(goals_dir) 
                            if os.path.isdir(os.path.join(goals_dir, d))]
                if goal_dirs:
                    context_content += "Recent goals:\n"
                    # Take first 3 goals
                    for goal_dir in goal_dirs[:3]:
                        goal_path = os.path.join(goals_dir, goal_dir)
                        goal_file = os.path.join(goal_path, "goal.md")
                        if os.path.exists(goal_file):
                            with open(goal_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                                # Look for goal statement
                                lines = content.split('\n')
                                goal_statement = "Goal definition in progress"
                                for line in lines:
                                    if "Goal Statement" in line:
                                        goal_statement = line.replace("Goal Statement:", "").strip()
                                        break
                                context_content += f"- **{goal_dir}**: {goal_statement}\n"
                else:
                    context_content += "No active goals yet. Use /goalkit.goal to create your first goal.\n"
            else:
                context_content += "No active goals yet. Use /goalkit.goal to create your first goal.\n"

            context_content += """
## 📊 Development Principles

Remember these core principles:
1. **Outcome-First**: Prioritize user and business outcomes
2. **Strategy Flexibility**: Multiple valid approaches exist for any goal
3. **Measurement-Driven**: Progress must be measured and validated
4. **Learning Integration**: Treat implementation as hypothesis testing
5. **Adaptive Planning**: Change course based on evidence

## 🔧 Next Recommended Actions

"""

            # Add recommendations based on goal status
            if not os.path.exists(goals_dir) or len(os.listdir(goals_dir)) == 0:
                context_content += """1. Use /goalkit.vision to establish project vision
2. Use /goalkit.goal to define first goal
"""
            else:
                context_content += """1. Review active goals in goals/ directory
2. Use /goalkit.strategies to explore implementation approaches
3. Use /goalkit.milestones to plan measurable progress steps
"""

            context_content += """
---

*This context is automatically updated by update-agent-context.py. Last updated: """ + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """*

"""

            # Write the context file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(context_content)
            
            return

    write_warning("No agent context file found to update")


def test_goal_context():
    """
    Validate that we're in a goal directory
    """
    current_dir = os.getcwd()

    # Check if we're in a goals subdirectory
    if "goals" not in current_dir:
        write_error("Not in a goal directory")
        write_info("Please navigate to a goal directory (e.g., goals/001-user-authentication/)")
        sys.exit(1)

    # Check for required goal files
    required_files = ["goal.md"]
    for file in required_files:
        if not os.path.exists(file):
            write_error(f"Missing required file: {file}")
            sys.exit(1)

    write_success("Goal context validated")


def test_goal_methodology_completion(goal_dir=None):
    """
    Check if the current goal has completed all required methodology steps
    """
    if goal_dir is None:
        goal_dir = os.getcwd()
    
    goal_file = os.path.join(goal_dir, "goal.md")
    strategies_file = os.path.join(goal_dir, "strategies.md")
    milestones_file = os.path.join(goal_dir, "milestones.md")
    execution_file = os.path.join(goal_dir, "execution.md")
    
    completed_steps = 0
    total_steps = 4  # goal, strategies, milestones, execution
    
    goal_dir_name = os.path.basename(goal_dir)
    write_info(f"Checking methodology completion for goal: {goal_dir_name}")
    
    # Check if goal.md exists and has content
    if os.path.exists(goal_file):
        with open(goal_file, 'r', encoding='utf-8') as f:
            goal_content = f.read()
        # Basic check: does the goal have success metrics defined?
        if "Success Metrics" in goal_content and "Target:" in goal_content:
            write_success("✓ Goal definition complete with success metrics")
            completed_steps += 1
        else:
            write_warning("⚠ Goal definition needs success metrics with specific targets")
    else:
        write_error("Missing goal.md file")
    
    # Check if strategies.md exists and has content
    if os.path.exists(strategies_file):
        with open(strategies_file, 'r', encoding='utf-8') as f:
            strategies_content = f.read()
        if "Strategy" in strategies_content and "Validation" in strategies_content:
            write_success("✓ Strategies defined with validation approaches")
            completed_steps += 1
        else:
            write_warning("⚠ Strategies need validation approaches and success criteria")
    else:
        write_warning("⚠ No strategies.md found - consider using /goalkit.strategies")
    
    # Check if milestones.md exists and has content
    if os.path.exists(milestones_file):
        with open(milestones_file, 'r', encoding='utf-8') as f:
            milestones_content = f.read()
        if "Milestone" in milestones_content and "Success Indicators" in milestones_content:
            write_success("✓ Milestones defined with success indicators")
            completed_steps += 1
        else:
            write_warning("⚠ Milestones need success indicators and measurement approaches")
    else:
        write_warning("⚠ No milestones.md found - consider using /goalkit.milestones")
    
    # Check if execution.md exists and has content
    if os.path.exists(execution_file):
        with open(execution_file, 'r', encoding='utf-8') as f:
            execution_content = f.read()
        if "Execution" in execution_content and "Strategy" in execution_content:
            write_success("✓ Execution plan defined with strategy")
            completed_steps += 1
        else:
            write_warning("⚠ Execution plan may need more detail")
    else:
        write_warning("⚠ No execution.md found - consider using /goalkit.execute")
    
    completion_percent = round((completed_steps / total_steps) * 100)
    write_info(f"Methodology completion: {completion_percent}% ({completed_steps} of {total_steps} steps)")
    
    if completed_steps == total_steps:
        write_success("[CHECK] All methodology steps completed! Ready for execution.")
        return True
    else:
        write_warning("[WARN] Some methodology steps are incomplete. We recommend completing all steps before execution.")
        write_info("Consider using the following commands to complete missing steps:")
        
        if not os.path.exists(strategies_file):
            write_step("1. /goalkit.strategies - Explore implementation strategies")
        
        if not os.path.exists(milestones_file):
            write_step("2. /goalkit.milestones - Create measurable milestones")
        
        if not os.path.exists(execution_file):
            write_step("3. /goalkit.execute - Execute with learning and adaptation")
        
        return False


def get_current_goal_name():
    """
    Get the goal name from current directory
    """
    return os.path.basename(os.getcwd())


def show_goal_summary(goal_dir):
    """
    Print a summary of the current goal
    """
    goal_file = os.path.join(goal_dir, "goal.md")
    if os.path.exists(goal_file):
        write_info("Current Goal Summary:")
        print()
        
        with open(goal_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        for line in lines:
            if "Goal Statement" in line or "Success Metrics" in line:
                print(line)


def set_goal_environment(goal_dir):
    """
    Setup environment variables for goal development
    """
    project_root = get_git_root()
    goal_name = os.path.basename(goal_dir)

    # Set environment variables
    os.environ['GOAL_KIT_PROJECT_ROOT'] = project_root
    os.environ['GOAL_KIT_GOAL_DIR'] = goal_dir
    os.environ['GOAL_KIT_GOAL_NAME'] = goal_name

    write_info("Goal environment configured")
    write_info(f"  Project Root: {project_root}")
    write_info(f"  Goal Directory: {goal_dir}")
    write_info(f"  Goal Name: {goal_name}")