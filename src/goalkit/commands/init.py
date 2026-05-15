"""Project initialization command."""

import os
import sys
import shutil
import shlex
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.live import Live

from ..agents import AgentRegistry, get_agent
from ..templates import TemplateManager
from ..helpers import (
    StepTracker,
    select_with_arrows,
    validate_project_name,
    check_disk_space,
    check_path_writable,
    check_tool,
    init_git_repo,
)

console = Console()

# Get Claude's local path for tool detection
CLAUDE_LOCAL_PATH = Path.home() / ".claude" / "local" / "claude"

# Script type choices
SCRIPT_TYPE_CHOICES = {
    "sh": "POSIX Shell (bash/zsh) - downloads shell-based templates",
    "ps": "PowerShell - downloads PowerShell-based templates",
}


def create_agent_file(project_path: Path, ai_assistant: str) -> None:
    """Create a customized agent file using the agent file template."""
    import datetime

    # Read the agent file template
    template_path = Path(__file__).parent.parent.parent / "templates" / "agent-file-template.md"
    if not template_path.exists():
        return  # Skip if template doesn't exist

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
    except Exception:
        return  # Skip if can't read template

    # Replace placeholders with actual project information
    project_name = project_path.name
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Basic replacements
    content = template_content.replace("[PROJECT NAME]", project_name)
    content = content.replace("[DATE]", current_date)

    # For now, set placeholder content for dynamic sections
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

    # Add strict workflow enforcement
    workflow_enforcement = """

## 🚨 STRICT WORKFLOW ENFORCEMENT

**🛑 STOP AFTER EACH COMMAND - ONE AT A TIME**

**FORBIDDEN AGENT BEHAVIORS:**
- ❌ Creating goals automatically after vision
- ❌ Starting coding after vision creation
- ❌ Chaining commands without user input
- ❌ Skipping methodology steps

**ALLOWED SEQUENCE:**
- `/goalkit.vision` → Create vision → **🛑 STOP**
- User runs `/goalkit.goal` → Create goal → **🛑 STOP**
- User runs `/goalkit.strategies` → Explore strategies → **🛑 STOP**
- User runs `/goalkit.milestones` → Create milestones → **🛑 STOP**
- User runs `/goalkit.execute` → Implement → Continue
"""
    content = content.replace(
        "*This guide is automatically created by goalkeeper init. It provides essential guidance for agents working on this Goal Kit project.*",
        workflow_enforcement
        + "\n*This guide is automatically created by goalkeeper init. It provides essential guidance for agents working on this Goal Kit project.*",
    )

    # Define agent-specific file names and locations
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

    # Create all appropriate agent files for the selected agent
    for file_location in file_locations:
        file_path = project_path / file_location
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            continue


def create_agent_config(project_path: Path, selected_ai: str) -> None:
    """Create agent-specific configuration files and directories."""
    from ..agents import AGENT_CONFIG

    # Ensure .goalkit/goals directory exists
    goalkit_dir = project_path / ".goalkit"
    goalkit_dir.mkdir(parents=True, exist_ok=True)
    goals_dir = goalkit_dir / "goals"
    goals_dir.mkdir(parents=True, exist_ok=True)

    # Define the agent folder mapping
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

    # Check if agent requires CLI
    agent_config = AGENT_CONFIG.get(selected_ai)
    requires_cli = agent_config and agent_config.get("requires_cli", False)

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

    # Copy templates - look for agent-specific first, fallback to generic
    agent_specific_template_dir = (
        Path(__file__).parent.parent.parent / "templates" / selected_ai / folder_name
    )
    if agent_specific_template_dir.exists():
        for template_file in agent_specific_template_dir.iterdir():
            if template_file.is_file() and template_file.suffix == ".md":
                dest_path = agent_commands_dir / template_file.name
                shutil.copy2(template_file, dest_path)
    else:
        # Fallback to generic commands templates
        commands_source_dir = Path(__file__).parent.parent.parent / "templates" / "commands"
        if commands_source_dir.exists():
            for command_file in commands_source_dir.iterdir():
                if command_file.is_file() and command_file.suffix == ".md":
                    dest_path = agent_commands_dir / command_file.name
                    shutil.copy2(command_file, dest_path)

        # Special handling for Copilot
        if selected_ai == "copilot":
            vscode_settings_source = (
                Path(__file__).parent.parent.parent / "templates" / "vscode-settings.json"
            )
            if vscode_settings_source.exists():
                vscode_dir = project_path / ".vscode"
                vscode_dir.mkdir(parents=True, exist_ok=True)
                dest_path = vscode_dir / "settings.json"
                shutil.copy2(vscode_settings_source, dest_path)

    # Create the main agent file
    create_agent_file(project_path, selected_ai)


def init(
    project_name: Optional[str] = typer.Argument(
        None,
        help="Name for your new project directory (optional if using --here, or use '.' for current directory)",
    ),
    ai_assistant: Optional[str] = typer.Option(
        None, "--ai", help="AI assistant to use: claude, gemini, copilot, cursor, qwen, opencode, codex, windsurf, kilocode, auggie or q"
    ),
    script_type: Optional[str] = typer.Option(
        None, "--script", help="Script type to use: sh or ps"
    ),
    ignore_agent_tools: bool = typer.Option(
        False, "--ignore-agent-tools", help="Skip checks for AI agent tools like Claude Code"
    ),
    no_git: bool = typer.Option(
        False, "--no-git", help="Skip git repository initialization"
    ),
    here: bool = typer.Option(
        False, "--here", help="Initialize project in the current directory instead of creating a new one"
    ),
    force: bool = typer.Option(
        False, "--force", help="Force merge/overwrite when using --here (skip confirmation)"
    ),
    skip_tls: bool = typer.Option(
        False, "--skip-tls", help="Skip SSL/TLS verification (not recommended)"
    ),
    debug: bool = typer.Option(
        False, "--debug", help="Show verbose diagnostic output for network and extraction failures"
    ),
    github_token: Optional[str] = typer.Option(
        None,
        "--github-token",
        help="GitHub token to use for API requests (or set GH_TOKEN or GITHUB_TOKEN environment variable)",
    ),
) -> None:
    """Initialize a new Goalkeeper project from the latest template.
    
    This command will:
    1. Check that required tools are installed (git is optional)
    2. Let you choose your AI assistant
    3. Download the appropriate template from GitHub
    4. Extract the template to a new project directory or current directory
    5. Initialize a fresh git repository (if not --no-git and no existing repo)
    6. Optionally set up AI assistant commands
    
    Examples:
        goalkeeper init my-project
        goalkeeper init my-project --ai claude
        goalkeeper init my-project --ai copilot --no-git
        goalkeeper init --ignore-agent-tools my-project
        goalkeeper init . --ai claude
        goalkeeper init .
        goalkeeper init --here --ai claude
        goalkeeper init --here
        goalkeeper init --here --force
    """
    from .. import show_banner, AGENT_CONFIG, download_and_extract_template, copy_scripts_to_goalkit, copy_templates_to_goalkit, ensure_executable_scripts
    import httpx
    import ssl
    import truststore

    show_banner()

    if project_name == ".":
        here = True
        project_name = None

    if here and project_name:
        console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
        raise typer.Exit(1)

    if not here and not project_name:
        console.print(
            "[red]Error:[/red] Must specify either a project name, use '.' for current directory, or use --here flag"
        )
        raise typer.Exit(1)

    # Validate project name
    if not here and project_name:
        is_valid, error_msg = validate_project_name(project_name)
        if not is_valid:
            error_panel = Panel(
                f"Invalid project name: {error_msg}",
                title="[red]Invalid Project Name[/red]",
                border_style="red",
                padding=(1, 2),
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()

        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(
                f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)"
            )
            console.print(
                "[yellow]Template files will be merged with existing content and may overwrite existing files[/yellow]"
            )
            if force:
                console.print(
                    "[cyan]--force supplied: skipping confirmation and proceeding with merge[/cyan]"
                )
            else:
                response = typer.confirm("Do you want to continue?")
                if not response:
                    console.print("[yellow]Operation cancelled[/yellow]")
                    raise typer.Exit(0)
    else:
        project_path = Path(project_name or ".").resolve()
        if project_path.exists():
            error_panel = Panel(
                f"Directory '[cyan]{project_name}[/cyan]' already exists\n"
                "Please choose a different project name or remove the existing directory.",
                title="[red]Directory Conflict[/red]",
                border_style="red",
                padding=(1, 2),
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    current_dir = Path.cwd()

    # Check disk space
    has_space, space_msg = check_disk_space(project_path, min_mb=100)
    if not has_space:
        console.print(f"[yellow]Warning:[/yellow] {space_msg}")

    # Check path writeability
    is_writable, write_msg = check_path_writable(project_path if here else project_path.parent)
    if not is_writable:
        error_panel = Panel(
            write_msg,
            title="[red]Permission Error[/red]",
            border_style="red",
            padding=(1, 2),
        )
        console.print()
        console.print(error_panel)
        raise typer.Exit(1)

    setup_lines = [
        "[cyan]Goalkeeper Project Setup[/cyan]",
        "",
        f"{'Project':<15} [green]{project_path.name}[/green]",
        f"{'Working Path':<15} [dim]{current_dir}[/dim]",
    ]

    if not here:
        setup_lines.append(f"{'Target Path':<15} [dim]{project_path}[/dim]")

    console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))

    # Check for git
    should_init_git = False
    if not no_git:
        should_init_git = check_tool("git", CLAUDE_LOCAL_PATH)
        if not should_init_git:
            console.print("[yellow]Git not found - will skip repository initialization[/yellow]")

    # Select AI assistant
    if ai_assistant:
        if ai_assistant not in AGENT_CONFIG:
            console.print(
                f"[red]Error:[/red] Invalid AI assistant '{ai_assistant}'. Choose from: {', '.join(AGENT_CONFIG.keys())}"
            )
            raise typer.Exit(1)
        selected_ai = ai_assistant
    else:
        ai_choices = {key: config["name"] for key, config in AGENT_CONFIG.items()}
        selected_ai = select_with_arrows(console, ai_choices, "Choose your AI assistant:", "copilot")

    # Check agent tools
    if not ignore_agent_tools:
        agent_config = AGENT_CONFIG.get(selected_ai)
        if agent_config and agent_config["requires_cli"]:
            install_url = agent_config["install_url"]
            if not check_tool(selected_ai, CLAUDE_LOCAL_PATH):
                error_panel = Panel(
                    f"[cyan]{selected_ai}[/cyan] not found\n"
                    f"Install from: [cyan]{install_url}[/cyan]\n"
                    f"{agent_config['name']} is required to continue with this project type.\n\n"
                    "Tip: Use [cyan]--ignore-agent-tools[/cyan] to skip this check",
                    title="[red]Agent Detection Error[/red]",
                    border_style="red",
                    padding=(1, 2),
                )
                console.print()
                console.print(error_panel)
                raise typer.Exit(1)

    # Select script type
    if script_type:
        if script_type not in SCRIPT_TYPE_CHOICES:
            console.print(
                f"[red]Error:[/red] Invalid script type '{script_type}'. Choose from: {', '.join(SCRIPT_TYPE_CHOICES.keys())}"
            )
            raise typer.Exit(1)
        selected_script = script_type
    else:
        default_script = "ps" if os.name == "nt" else "sh"
        try:
            selected_script = select_with_arrows(
                console, SCRIPT_TYPE_CHOICES, "Choose script type (or press Enter)", default_script
            )
        except (EOFError, KeyboardInterrupt):
            selected_script = default_script

    console.print(f"[cyan]Selected AI assistant:[/cyan] {selected_ai}")
    console.print(f"[cyan]Selected script type:[/cyan] {selected_script}")

    # Create tracker
    tracker = StepTracker("Initialize Goalkeeper Project")

    tracker.add("precheck", "Check required tools")
    tracker.complete("precheck", "ok")
    tracker.add("ai-select", "Select AI assistant")
    tracker.complete("ai-select", f"{selected_ai}")
    tracker.add("script-select", "Select script type")
    tracker.complete("script-select", selected_script)
    for key, label in [
        ("fetch", "Fetch latest release"),
        ("download", "Download template"),
        ("extract", "Extract template"),
        ("zip-list", "Archive contents"),
        ("extracted-summary", "Extraction summary"),
        ("chmod", "Ensure scripts executable"),
        ("copy-scripts", "Copy scripts"),
        ("copy-templates", "Copy templates"),
        ("cleanup", "Cleanup"),
        ("git", "Initialize git repository"),
        ("final", "Finalize"),
    ]:
        tracker.add(key, label)

    git_error_message = None

    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            verify = not skip_tls
            ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT) if verify else False
            local_client = httpx.Client(verify=ssl_context)

            download_and_extract_template(
                project_path,
                selected_ai,
                selected_script,
                here,
                verbose=False,
                tracker=tracker,
                client=local_client,
                debug=debug,
                github_token=github_token,
            )

            # Create agent-specific configuration
            create_agent_config(project_path, selected_ai)

            # Copy scripts and templates
            copy_scripts_to_goalkit(project_path, selected_script, tracker=tracker)
            copy_templates_to_goalkit(project_path, tracker=tracker)

            # Create agent file
            create_agent_file(project_path, selected_ai)

            ensure_executable_scripts(project_path, tracker=tracker)

            # Initialize git
            if not no_git:
                tracker.start("git")
                if should_init_git:
                    success, error_msg = init_git_repo(console, project_path, quiet=True)
                    if success:
                        tracker.complete("git", "initialized")
                    else:
                        tracker.error("git", "init failed")
                        git_error_message = error_msg
                else:
                    tracker.skip("git", "git not available")
            else:
                tracker.skip("git", "--no-git flag")

            tracker.complete("final", "project ready")
        except Exception as e:
            tracker.error("final", str(e))
            console.print(Panel(f"Initialization failed: {e}", title="Failure", border_style="red"))
            if debug:
                _env_pairs = [
                    ("Python", sys.version.split()[0]),
                    ("Platform", sys.platform),
                    ("CWD", str(Path.cwd())),
                ]
                _label_width = max(len(k) for k, _ in _env_pairs)
                env_lines = [
                    f"{k.ljust(_label_width)} → [bright_black]{v}[/bright_black]"
                    for k, v in _env_pairs
                ]
                console.print(Panel("\n".join(env_lines), title="Debug Environment", border_style="magenta"))
            if not here and project_path.exists():
                shutil.rmtree(project_path)
            raise typer.Exit(1)

    console.print(tracker.render())
    console.print("\n[bold green]Project ready.[/bold green]")

    # Show git error if initialization failed
    if git_error_message:
        console.print()
        git_error_panel = Panel(
            f"[yellow]Warning:[/yellow] Git repository initialization failed\n\n"
            f"{git_error_message}\n\n"
            f"[dim]You can initialize git manually later with:\n"
            f"[cyan]cd {project_path if not here else '.'}[/cyan]\n"
            f"[cyan]git init[/cyan]\n"
            f"[cyan]git add .[/cyan]\n"
            f"[cyan]git commit -m \"Initial commit\"[/cyan]",
            title="[red]Git Initialization Failed[/red]",
            border_style="red",
            padding=(1, 2),
        )
        console.print(git_error_panel)

    # Agent folder security notice
    agent_config = AGENT_CONFIG.get(selected_ai)
    if agent_config:
        agent_folder = agent_config["folder"]
        security_notice = Panel(
            f"Some agents may store credentials, auth tokens, or other identifying and private artifacts in the agent folder within your project.\n"
            f"Consider adding [cyan]{agent_folder}[/cyan] (or parts of it) to [cyan].gitignore[/cyan] to prevent accidental credential leakage.",
            title="[yellow]Agent Folder Security[/yellow]",
            border_style="yellow",
            padding=(1, 2),
        )
        console.print()
        console.print(security_notice)

    # Next steps
    steps_lines = []
    if not here:
        steps_lines.append(f"1. Go to the project folder: [cyan]cd {project_name}[/cyan]")
        step_num = 2
    else:
        steps_lines.append("1. You're already in the project directory!")
        step_num = 2

    # Codex-specific setup
    if selected_ai == "codex":
        codex_path = project_path / ".codex"
        quoted_path = shlex.quote(str(codex_path))
        if os.name == "nt":
            cmd = f"setx CODEX_HOME {quoted_path}"
        else:
            cmd = f"export CODEX_HOME={quoted_path}"
        steps_lines.append(
            f"{step_num}. Set [cyan]CODEX_HOME[/cyan] environment variable before running Codex: [cyan]{cmd}[/cyan]"
        )
        step_num += 1

    steps_lines.append(f"{step_num}. Start using slash commands with your AI agent:")
    steps_lines.append("   [cyan]/goalkit.vision[/] - Establish project vision and principles")
    steps_lines.append("   [cyan]/goalkit.goal[/] - Define goals and success criteria")
    steps_lines.append("   [cyan]/goalkit.strategies[/] - Explore implementation strategies")
    steps_lines.append("   [cyan]/goalkit.milestones[/] - Create measurable milestones")
    steps_lines.append("   [cyan]/goalkit.execute[/] - Execute with learning and adaptation")
    steps_lines.append("   [cyan]/goalkit.tasks[/] - Generate detailed implementation tasks")
    steps_lines.append("   [cyan]/goalkit.taskstoissues[/] - Convert tasks to GitHub issues")
    steps_lines.append("   [cyan]/goalkit.report[/] - Generate progress reports and insights")
    steps_lines.append("   [cyan]/goalkit.review[/] - Conduct project reviews and retrospectives")

    steps_panel = Panel("\n".join(steps_lines), title="Next Steps", border_style="cyan", padding=(1, 2))
    console.print()
    console.print(steps_panel)
