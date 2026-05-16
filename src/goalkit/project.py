"""
Project initialization logic for Goal Kit.

Handles agent configuration file creation, agent file generation,
and project directory setup.
"""

import datetime
import shutil
from pathlib import Path

from .agents import AGENT_CONFIG


def create_agent_file(project_path: Path, ai_assistant: str) -> None:
    """Create a customized agent file using the agent file template."""
    # Read the agent file template
    template_path = Path(__file__).parent.parent.parent / "templates" / "agent-file-template.md"
    if not template_path.exists():
        return  # Skip if template doesn't exist

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except Exception:
        return  # Skip if can't read template

    project_name = project_path.name
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    content = template_content.replace("[PROJECT NAME]", project_name)
    content = content.replace("[DATE]", current_date)
    content = content.replace("[AGENT]", ai_assistant)

    content = content.replace(
        "[EXTRACTED FROM ALL GOAL.MD FILES]",
        "No goals created yet. Use /goalkit.goal to create your first goal.",
    )
    content = content.replace(
        "[ACTUAL STRUCTURE FROM GOALS]",
        "Project structure will be populated as goals are created.",
    )
    content = content.replace(
        "[EXTRACTED FROM STRATEGIES.MD]",
        "No strategies defined yet. Use /goalkit.strategies after creating goals.",
    )
    content = content.replace(
        "[EXTRACTED FROM MILESTONES.MD]",
        "No milestones defined yet. Use /goalkit.milestones after defining strategies.",
    )
    content = content.replace(
        "[EXTRACTED FROM EXECUTION.MD]",
        "No execution plans yet. Use /goalkit.execute after creating milestones.",
    )
    content = content.replace(
        "[LAST 3 COMPLETED MILESTONES AND OUTCOMES]",
        "No completed milestones yet.",
    )

    scripts_section = """\n
## Available Scripts

The following scripts are available in `.goalkit/scripts/bash/` and `.goalkit/scripts/powershell/`:

| Script | Purpose |
|--------|---------|
| `create-new-goal.sh` | Create a new goal branch and initialize goal file |
| `create-vision.sh` | Initialize vision file structure |
| `create-tasks.sh` | Generate detailed implementation tasks |
| `create-report.sh` | Generate progress and insight reports |
| `create-review.sh` | Conduct project review and retrospective |
| `setup-strategy.sh` | Explore multiple strategic approaches |
| `setup-milestones.sh` | Create measurable milestone checkpoints |
| `setup-execution.sh` | Execute with learning and adaptation |
| `setup-metrics.sh` | Define and track project metrics |
| `setup-quality-assurance.sh` | Define quality standards and testing strategy |
| `setup-security-review.sh` | Conduct security assessment of goal deliverables |
| `setup-risk-register.sh` | Identify, assess, and track risks |
| `setup-compliance-checklist.sh` | Regulatory compliance verification |
| `setup-detailed-retrospective.sh` | Comprehensive retrospective analysis |
| `update-agent-context.sh` | Update agent-specific context files |

**How to use:** Each script is invoked by its corresponding slash command (`/goalkit.goal` → `create-new-goal.sh`).

**Note:** PowerShell equivalents exist with `.ps1` extension in `.goalkit/scripts/powershell/`.
"""
    content = content.replace("## \U0001f527 Next Recommended Actions", scripts_section + "\n## \U0001f527 Next Recommended Actions")

    workflow_enforcement = """\n
## \U0001f6a8 STRICT WORKFLOW ENFORCEMENT

**\U0001f6d1 STOP AFTER EACH COMMAND - ONE AT A TIME**

**FORBIDDEN AGENT BEHAVIORS:**
- \u274c Creating goals automatically after vision
- \u274c Starting coding after vision creation
- \u274c Chaining commands without user input
- \u274c Skipping methodology steps

**ALLOWED SEQUENCE:**
- `/goalkit.vision` \u2192 Create vision \u2192 **\U0001f6d1 STOP**
- User runs `/goalkit.goal` \u2192 Create goal \u2192 **\U0001f6d1 STOP**
- User runs `/goalkit.strategies` \u2192 Explore strategies \u2192 **\U0001f6d1 STOP**
- User runs `/goalkit.milestones` \u2192 Create milestones \u2192 **\U0001f6d1 STOP**
- User runs `/goalkit.execute` \u2192 Implement \u2192 Continue
"""
    content = content.replace(
        "*This guide is automatically created by goalkit init. It provides essential guidance for agents working on this Goal Kit project.*",
        workflow_enforcement + "\n*This guide is automatically created by goalkit init. It provides essential guidance for agents working on this Goal Kit project.*",
    )

    agent_file_locations = {
        "claude": [".claude/goal-kit-guide.md"],
        "gemini": [".gemini/goal-kit-guide.md"],
        "cursor": [".cursor/goal-kit-guide.md"],
        "copilot": [".github/goal-kit-guide.md"],
        "qwen": [".qwen/goal-kit-guide.md"],
        "windsurf": [".windsurf/goal-kit-guide.md"],
        "kilocode": [".kilocode/goal-kit-guide.md"],
        "auggie": [".augment/goal-kit-guide.md"],
        "roo": [".roo/goal-kit-guide.md"],
        "codex": [".codex/goal-kit-guide.md"],
        "opencode": ["goal-kit-guide.md"],
        "q": [".amazonq/goal-kit-guide.md"],
    }

    file_locations = agent_file_locations.get(ai_assistant, [f"{ai_assistant.upper()}.md"])

    for file_location in file_locations:
        file_path = project_path / file_location
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception:
            continue


def create_agent_config(project_path: Path, selected_ai: str) -> None:
    """Create agent-specific configuration files and directories."""
    # Ensure .goalkit/goals directory exists
    goalkit_dir = project_path / ".goalkit"
    goalkit_dir.mkdir(parents=True, exist_ok=True)
    goals_dir = goalkit_dir / "goals"
    goals_dir.mkdir(parents=True, exist_ok=True)

    agent_folder_map = {
        "claude": ".claude/",
        "gemini": ".gemini/",
        "cursor": ".cursor/",
        "qwen": ".qwen/",
        "opencode": ".opencode/",
        "codex": ".codex/",
        "windsurf": ".windsurf/",
        "kilocode": ".kilocode/",
        "auggie": ".augment/",
        "copilot": ".github/",
        "roo": ".roo/",
        "q": ".amazonq/",
    }

    agent_folder = agent_folder_map.get(selected_ai)
    if not agent_folder:
        return

    agent_config = AGENT_CONFIG.get(selected_ai)

    # Path to agent template directory
    agent_template_path = Path(__file__).parent.parent.parent / "agent_templates" / selected_ai

    # Create agent config directory
    agent_config_dir = project_path / agent_folder.strip("/")
    agent_config_dir.mkdir(parents=True, exist_ok=True)

    # Copy agent template if it exists
    if agent_template_path.exists():
        for item in agent_template_path.iterdir():
            dest_path = agent_config_dir / item.name
            if item.is_file():
                shutil.copy2(item, dest_path)
            elif item.is_dir():
                shutil.copytree(item, dest_path, dirs_exist_ok=True)

    # Define folder structure for each agent type
    agent_folder_structure = {
        "claude": "commands",
        "gemini": "commands",
        "cursor": "commands",
        "qwen": "commands",
        "opencode": "command",
        "windsurf": "workflows",
        "codex": "prompts",
        "kilocode": "workflows",
        "auggie": "commands",
        "roo": "commands",
        "codebuddy": "commands",
        "copilot": "prompts",
        "q": "prompts",
    }

    folder_name = agent_folder_structure.get(selected_ai, "commands")
    agent_commands_dir = agent_config_dir / folder_name
    agent_commands_dir.mkdir(parents=True, exist_ok=True)

    # Copy templates
    templates_dir = Path(__file__).parent.parent.parent / "templates"
    agent_specific_template_dir = templates_dir / selected_ai / folder_name
    if agent_specific_template_dir.exists():
        for template_file in agent_specific_template_dir.iterdir():
            if template_file.is_file() and template_file.suffix == ".md":
                dest_path = agent_commands_dir / template_file.name
                shutil.copy2(template_file, dest_path)
    else:
        commands_source_dir = templates_dir / "commands"
        if commands_source_dir.exists():
            for command_file in commands_source_dir.iterdir():
                if command_file.is_file() and command_file.suffix == ".md":
                    dest_path = agent_commands_dir / command_file.name
                    shutil.copy2(command_file, dest_path)

        # Special handling for Copilot VS Code settings
        if selected_ai == "copilot":
            vscode_settings_source = templates_dir / "vscode-settings.json"
            if vscode_settings_source.exists():
                vscode_dir = project_path / ".vscode"
                vscode_dir.mkdir(parents=True, exist_ok=True)
                dest_path = vscode_dir / "settings.json"
                shutil.copy2(vscode_settings_source, dest_path)

    # Create the main agent file
    create_agent_file(project_path, selected_ai)
