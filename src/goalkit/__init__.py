#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "rich",
#     "platformdirs",
#     "readchar",
#     "httpx",
# ]
# ///
"""
Goalkit CLI - Setup and monitoring tool for Goal-Driven Development

The main workflow is driven through your AI agent via slash commands:
    /goalkit.vision    /goalkit.goal    /goalkit.strategies
    /goalkit.milestones  /goalkit.execute  /goalkit.tasks

This CLI handles setup and monitoring:
    goalkit init <project-name>
    goalkit init .
    goalkit init --here
    goalkit status
    goalkit check
"""

import os
import subprocess
import sys
import zipfile
import tempfile
import shutil
import shlex
import json
from pathlib import Path
from typing import Optional, Tuple
import datetime

import typer
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.align import Align
from rich.live import Live
from typer.core import TyperGroup

import ssl
import truststore

# Import helpers
from .helpers import (
    StepTracker,
    get_key,
    select_with_arrows,
    merge_json_files,
    handle_vscode_settings,
    is_git_repo,
    init_git_repo,
    check_tool,
    validate_project_name,
    check_disk_space,
    check_path_writable,
    load_project_context,
)

# Import commands
from .commands.status import status as status_command
from .commands.milestones import milestones as milestones_command
from .commands.metrics import metrics as metrics_command
from .commands.tasks import tasks_command
from .commands.reporting import report_command, insights_command
from .commands.dependencies import app as dependencies_app
from .commands.aggregation import app as aggregation_app
from .commands.export import app as export_app
from .commands.analytics import app as analytics_app
from .commands.webhooks import app as webhooks_app

ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = httpx.Client(verify=ssl_context)

def _github_token(cli_token: str | None = None) -> str | None:
    """Return sanitized GitHub token (cli arg takes precedence) or None."""
    return ((cli_token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()) or None

def _github_auth_headers(cli_token: str | None = None) -> dict:
    """Return Authorization header dict only when a non-empty token exists."""
    token = _github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}

# Agent configuration with name, folder, install URL, and CLI tool requirement
AGENT_CONFIG = {
    "copilot": {
        "name": "GitHub Copilot",
        "folder": ".github/",
        "install_url": None,  # IDE-based, no CLI check needed
        "requires_cli": False,
    },
    "claude": {
        "name": "Claude Code",
        "folder": ".claude/",
        "install_url": "https://docs.anthropic.com/en/docs/claude-code/setup",
        "requires_cli": True,
    },
    "gemini": {
        "name": "Gemini CLI",
        "folder": ".gemini/",
        "install_url": "https://github.com/google-gemini/gemini-cli",
        "requires_cli": True,
    },
    "cursor": {
        "name": "Cursor",
        "folder": ".cursor/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "qwen": {
        "name": "Qwen Code",
        "folder": ".qwen/",
        "install_url": "https://github.com/QwenLM/qwen-code",
        "requires_cli": True,
    },
    "opencode": {
        "name": "opencode",
        "folder": ".opencode/",
        "install_url": "https://opencode.ai",
        "requires_cli": True,
    },
    "codex": {
        "name": "Codex CLI",
        "folder": ".codex/",
        "install_url": "https://github.com/openai/codex",
        "requires_cli": True,
    },
    "windsurf": {
        "name": "Windsurf",
        "folder": ".windsurf/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "kilocode": {
        "name": "Kilo Code",
        "folder": ".kilocode/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "auggie": {
        "name": "Auggie CLI",
        "folder": ".augment/",
        "install_url": "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli",
        "requires_cli": True,
    },
    "codebuddy": {
        "name": "CodeBuddy",
        "folder": ".codebuddy/",
        "install_url": "https://www.codebuddy.ai/cli",
        "requires_cli": True,
    },
    "roo": {
        "name": "Roo Code",
        "folder": ".roo/",
        "install_url": None,  # IDE-based
        "requires_cli": False,
    },
    "q": {
        "name": "Amazon Q Developer CLI",
        "folder": ".amazonq/",
        "install_url": "https://aws.amazon.com/developer/learning/q-developer-cli/",
        "requires_cli": True,
    },
}

SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh) - downloads shell-based templates", "ps": "PowerShell - downloads PowerShell-based templates"}

CLAUDE_LOCAL_PATH = Path.home() / ".claude" / "local" / "claude"

BANNER = """
 ######    #######     ###    ##             ##    ## #### ######## 
##    ##  ##     ##   ## ##   ##             ##   ##   ##     ##    
##        ##     ##  ##   ##  ##             ##  ##    ##     ##    
##   #### ##     ## ##     ## ##             #####     ##     ##    
##    ##  ##     ## ######### ##             ##  ##    ##     ##    
##    ##  ##     ## ##     ## ##             ##   ##   ##     ##    
 ######    #######  ##     ## ########       ##    ## ####    ## 
"""

TAGLINE = "Goal Kit - Goal-Driven Development Toolkit"

console = Console()

class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""

    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="goalkit",
    help="Goal-Driven Development tool for AI agents. Use /goalkit.* commands through your AI agent for the main workflow.",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)

# Wire in sub-command apps
app.add_typer(dependencies_app, name="dependencies", help="Manage task dependencies and critical paths")
app.add_typer(aggregation_app, name="projects", help="Manage multiple projects in a workspace")
app.add_typer(export_app, name="export", help="Export project data in multiple formats")
app.add_typer(analytics_app, name="analytics", help="Analytics, trends, and forecasting")
app.add_typer(webhooks_app, name="webhooks", help="Webhook management and event notifications")

def show_banner():
    """Display the ASCII art banner."""
    banner_lines = BANNER.strip().split('\n')
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)

    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()
    # Also display project context if in a Goal Kit project
    display_project_context()

@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided."""
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" in sys.argv:
        show_banner()
        console.print(Align.center("[dim]Run 'goalkit --help' for usage information[/dim]"))
        console.print()

def run_command(cmd: list[str], check_return: bool = True, capture: bool = False, shell: bool = False) -> Optional[str]:
    """Run a shell command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(cmd, check=check_return, capture_output=True, text=True, shell=shell)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]Error running command:[/red] {' '.join(cmd)}")
            console.print(f"[red]Exit code:[/red] {e.returncode}")
            if hasattr(e, 'stderr') and e.stderr:
                console.print(f"[red]Error output:[/red] {e.stderr}")
            raise
        return None


def display_project_context():
    """Display project context if in a Goal Kit project."""
    context = load_project_context()
    if context:
        # Create a panel showing project status
        status_text = f"""
[bold]Project:[/bold] {context['project_name']}
[bold]Phase:[/bold] {context['phase'].title()}
[bold]Health Score:[/bold] {context['health_score']}/100
[bold]Completion:[/bold] {context['completion_percent']}%

[bold]Goals:[/bold] {context['total_goals']} | [bold]Milestones:[/bold] {context['completed_milestones']}/{context['total_milestones']}
"""
        console.print(Panel(status_text, title="[green]Goal Kit Project Detected[/green]", border_style="green"))

        # List goals if available
        if context['goals']:
            console.print(f"\n[bold cyan]Active Goals ({len(context['goals'])}):[/bold cyan]")
            for goal in context['goals']:
                console.print(f"  • [cyan]{goal['name']}[/cyan] - {goal['phase']} ({goal['completion_percent']}%)")





def download_template_from_github(ai_assistant: str, download_dir: Path, *, script_type: str = "sh", verbose: bool = True, show_progress: bool = True, client: Optional[httpx.Client] = None, debug: bool = False, github_token: Optional[str] = None) -> Tuple[Path, dict]:
    repo_owner = "Nom-nom-hub"
    repo_name = "goal-kit"
    if client is None:
        client = httpx.Client(verify=ssl_context)

    if verbose:
        console.print("[cyan]Fetching latest release information...[/cyan]")
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    try:
        response = client.get(
            api_url,
            timeout=30,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        )
        status = response.status_code
        if status != 200:
            msg = f"GitHub API returned {status} for {api_url}"
            if debug:
                msg += f"\nResponse headers: {response.headers}\nBody (truncated 500): {response.text[:500]}"
            raise RuntimeError(msg)
        try:
            release_data = response.json()
        except ValueError as je:
            raise RuntimeError(f"Failed to parse release JSON: {je}\nRaw (truncated 400): {response.text[:400]}")
    except Exception as e:
        # Re-raise as RuntimeError to be caught by the caller
        # Don't call typer.Exit here - let the caller handle display and exit
        raise RuntimeError(f"Failed to fetch GitHub releases: {str(e)}") from e

    assets = release_data.get("assets", [])
    pattern = f"goal-kit-template-{ai_assistant}-{script_type}"
    matching_assets = [
        asset for asset in assets
        if pattern in asset["name"] and asset["name"].endswith(".zip")
    ]

    asset = matching_assets[0] if matching_assets else None

    if asset is None:
        # Try fallback to any available template for agents without specific templates
        # Look for any goal-kit-template-*.zip file
        fallback_assets = [
            asset for asset in assets
            if asset["name"].startswith("goal-kit-template-") and asset["name"].endswith(".zip")
        ]
        if fallback_assets:
            asset = fallback_assets[0]  # Use the first available template
            if verbose:
                console.print(f"[yellow]No specific template for {ai_assistant}, using fallback template: {asset['name']}[/yellow]")
        else:
            asset_names = [a.get('name', '?') for a in assets]
            msg = f"No matching release asset found for {ai_assistant} (expected pattern: {pattern})\nAvailable: {', '.join(asset_names)}"
            raise RuntimeError(msg)

    download_url = asset["browser_download_url"]
    filename = asset["name"]
    file_size = asset["size"]

    if verbose:
        console.print(f"[cyan]Found template:[/cyan] {filename}")
        console.print(f"[cyan]Size:[/cyan] {file_size:,} bytes")
        console.print(f"[cyan]Release:[/cyan] {release_data['tag_name']}")

    zip_path = download_dir / filename
    if verbose:
        console.print(f"[cyan]Downloading template...[/cyan]")

    try:
        with client.stream(
            "GET",
            download_url,
            timeout=60,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        ) as response:
            if response.status_code != 200:
                body_sample = response.text[:400]
                raise RuntimeError(f"Download failed with {response.status_code}\nHeaders: {response.headers}\nBody (truncated): {body_sample}")
            total_size = int(response.headers.get('content-length', 0))
            with open(zip_path, 'wb') as f:
                if total_size == 0:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        f.write(chunk)
                else:
                    if show_progress:
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                            console=console,
                        ) as progress:
                            task = progress.add_task("Downloading...", total=total_size)
                            downloaded = 0
                            for chunk in response.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                                downloaded += len(chunk)
                                progress.update(task, completed=downloaded)
                    else:
                        for chunk in response.iter_bytes(chunk_size=8192):
                            f.write(chunk)
    except Exception as e:
        detail = str(e)
        if zip_path.exists():
            zip_path.unlink()
        raise RuntimeError(f"Error downloading template: {detail}") from e
    if verbose:
        console.print(f"Downloaded: {filename}")
    metadata = {
        "filename": filename,
        "size": file_size,
        "release": release_data["tag_name"],
        "asset_url": download_url
    }
    return zip_path, metadata

def create_agent_file(project_path: Path, ai_assistant: str):
    """Create a customized agent file using the agent file template."""
    import datetime

    # Read the agent file template
    template_path = Path(__file__).parent.parent.parent / "templates" / "agent-file-template.md"
    if not template_path.exists():
        return  # Skip if template doesn't exist

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except Exception:
        return  # Skip if can't read template

    # Replace placeholders with actual project information
    project_name = project_path.name
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Basic replacements
    content = template_content.replace("[PROJECT NAME]", project_name)
    content = content.replace("[DATE]", current_date)
    content = content.replace("[AGENT]", ai_assistant)

    # For now, set placeholder content for dynamic sections
    # These would be populated by the update_agent_context.py script later
    content = content.replace("[EXTRACTED FROM ALL GOAL.MD FILES]", "No goals created yet. Use /goalkit.goal to create your first goal.")
    content = content.replace("[ACTUAL STRUCTURE FROM GOALS]", "Project structure will be populated as goals are created.")
    content = content.replace("[EXTRACTED FROM STRATEGIES.MD]", "No strategies defined yet. Use /goalkit.strategies after creating goals.")
    content = content.replace("[EXTRACTED FROM MILESTONES.MD]", "No milestones defined yet. Use /goalkit.milestones after defining strategies.")
    content = content.replace("[EXTRACTED FROM EXECUTION.MD]", "No execution plans yet. Use /goalkit.execute after creating milestones.")
    content = content.replace("[LAST 3 COMPLETED MILESTONES AND OUTCOMES]", "No completed milestones yet.")

    # Add available scripts section
    scripts_section = """
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

**How to use:** Each script is invoked by its corresponding slash command (`/goalkit.goal` → `create-new-goal.sh`). Do not run scripts manually unless explicitly instructed by a workflow or the user.

**Workflow scripts** (referenced by `.goalkit/workflows/` files): `setup-quality-assurance.sh`, `setup-security-review.sh`, `setup-risk-register.sh`, `setup-compliance-checklist.sh`, `setup-detailed-retrospective.sh` — these are used when a workflow guide mentions them. Follow the workflow instructions step by step.

**Note:** PowerShell equivalents exist with `.ps1` extension in `.goalkit/scripts/powershell/`.
"""
    content = content.replace("## 🔧 Next Recommended Actions", scripts_section + "\n## 🔧 Next Recommended Actions")

    # Add strict workflow enforcement to agent files
    # Insert after the "## 🔧 Next Recommended Actions" section
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
    # Insert the workflow enforcement before the end of the file
    content = content.replace("*This guide is automatically created by goalkit init. It provides essential guidance for agents working on this Goal Kit project.*",
                             workflow_enforcement + "\n*This guide is automatically created by goalkit init. It provides essential guidance for agents working on this Goal Kit project.*")

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
        "opencode": ["goal-kit-guide.md"],  # Root level for opencode
        "q": [".amazonq/goal-kit-guide.md"]
    }

    file_locations = agent_file_locations.get(ai_assistant, [f"{ai_assistant.upper()}.md"])

    # Create all appropriate agent files for the selected agent
    for file_location in file_locations:
        file_path = project_path / file_location
        try:
            # Make sure parent directories exist
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write the agent file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception:
            # If we can't create a specific file, continue - it's not critical for initialization
            continue


def create_agent_context_file(project_path: Path, ai_assistant: str):
    """Create agent context files with Goal Kit commands based on the selected AI assistant."""
    import datetime
    import os

    # Define the agent context files patterns based on the selected agent
    # Following the same patterns as in update-agent-context.sh and update-agent-context.py
    agent_context_files = {
        "claude": [
            "CLAUDE.md",
            ".claude/context.md"
        ],
        "gemini": [
            "GEMINI.md",
            ".gemini/context.md"
        ],
        "cursor": [
            "CURSOR.md",
            ".cursor/context.md"
        ],
        "copilot": [
            ".vscode/context.md"  # VSCode specific location
        ],
        "qwen": [
            "QWEN.md",
            ".qwen/context.md"
        ],
        "windsurf": [
            "WINDSURF.md",
            ".windsurf/context.md"
        ],
        "kilocode": [
            "KILOCODE.md",
            ".kilocode/context.md"
        ],
        "auggie": [
            ".augment/context.md"  # Based on the pattern from create-release-packages.sh
        ],
        "roo": [
            "ROO.md",
            ".roo/context.md"
        ],
        "codex": [
            ".codex/context.md"
        ],
        "opencode": [
            "OPENCODE.md"
        ]
    }

    # Get the appropriate context file names for the selected agent
    context_file_names = agent_context_files.get(ai_assistant, ["CLAUDE.md"])

    project_name = project_path.name

    # Determine script type based on OS
    is_windows = os.name == "nt"
    if is_windows:
        vision_note = "(create vision.md manually in `.goalkit/goals/`)"
        goal_script = r".\\.goalkit\\scripts\\powershell\\create-new-goal.ps1"
        strategies_script = r".\\.goalkit\\scripts\\powershell\\setup-strategy.ps1"
        milestones_script = r".\\.goalkit\\scripts\\powershell\\setup-milestones.ps1"
        execute_script = r".\\.goalkit\\scripts\\powershell\\setup-execution.ps1"
        script_type_name = "PowerShell"
    else:
        vision_note = "(create vision.md manually in `.goalkit/goals/`)"
        goal_script = "./.goalkit/scripts/bash/create-new-goal.sh"
        strategies_script = "./.goalkit/scripts/bash/setup-strategy.sh"
        milestones_script = "./.goalkit/scripts/bash/setup-milestones.sh"
        execute_script = "./.goalkit/scripts/bash/setup-execution.sh"
        script_type_name = "Bash"

    # Create content for the agent context file
    # Create content for the agent context file
    context_content = f"""# 🎯 Goal-Driven Development (GDD) Framework

**Project**: {project_name}
**Agent**: {ai_assistant}
**Protocol**: GDD v1.0 (Strict Enforcement)

## 📜 The GDD Constitution
This project operates under the **Goal-Driven Development Constitution** (found in `memory/constitution.md`). You are required to read and adhere to its principles for every task.

## 🚦 Strict Workflow Enforcement
To ensure professional-grade outcomes, you must follow the **One-Command-At-A-Time** protocol. Do not chain commands or proceed to implementation without explicit milestone approval.

### 1. The Core Sequence
| Command | Action | Agent Requirement |
| :--- | :--- | :--- |
| **`/goalkit.vision`** | Define "North Star" | Run `{script_type_name.upper()}` script → Create `vision.md` → **STOP** |
| **`/goalkit.goal`** | Set Outcomes | Run `{goal_script}` → Define metrics → **STOP** |
| **`/goalkit.strategies`** | Compare Paths | Run `{strategies_script}` → Compare 3+ approaches → **STOP** |
| **`/goalkit.milestones`** | Plan Progress | Run `{milestones_script}` → Define measurable steps → **STOP** |
| **`/goalkit.execute`** | Adaptive Build | Run `{execute_script}` → Build & Measure → **ITERATE** |

### 🛑 CRITICAL RULES
1.  **NEVER "Vibe-Code"**: Every line of code must be traceable to a specific milestone in a validated strategy.
2.  **OUTCOMES > FEATURES**: If the user asks for a "feature," translate it into a "goal" (outcome) first.
3.  **TECH-FREE GOALS**: Goal definitions must not mention specific technologies (e.g., "Use React"). Technologies belong in **Strategies**.
4.  **NO MANUAL FILE CREATION**: Always use the provided `{script_type_name}` scripts to maintain project structure.
5.  **MANDATORY PIVOTING**: If metrics are not being met during execution, you MUST stop and propose a strategy pivot.

---

*This context is automatically created by goalkit init. Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    # Create all appropriate context files for the selected agent
    for context_file_name in context_file_names:
        context_file_path = project_path / context_file_name
        try:
            # Make sure parent directories exist
            context_file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write the context file
            with open(context_file_path, 'w', encoding='utf-8') as f:
                f.write(context_content)
        except Exception:
            # If we can't create a specific file, continue - it's not critical for initialization
            continue

def download_and_extract_template(project_path: Path, ai_assistant: str, script_type: str, is_current_dir: bool = False, *, verbose: bool = True, tracker: Optional[StepTracker] = None, client: Optional[httpx.Client] = None, debug: bool = False, github_token: Optional[str] = None) -> Path:
    """Download the latest release and extract it to create a new project.
    Returns project_path. Uses tracker if provided (with keys: fetch, download, extract, cleanup)
    """
    current_dir = Path.cwd()

    if tracker:
        tracker.start("fetch", "contacting GitHub API")
    try:
        zip_path, meta = download_template_from_github(
            ai_assistant,
            current_dir,
            script_type=script_type,
            verbose=verbose and tracker is None,
            show_progress=(tracker is None),
            client=client,
            debug=debug,
            github_token=github_token
        )
        if tracker:
            tracker.complete("fetch", f"release {meta['release']} ({meta['size']:,} bytes)")
            tracker.add("download", "Download template")
            tracker.complete("download", meta['filename'])
    except Exception as e:
        if tracker:
            tracker.error("fetch", str(e))
        else:
            if verbose:
                console.print(f"[red]Error downloading template:[/red] {e}")
        raise

    if tracker:
        tracker.add("extract", "Extract template")
        tracker.start("extract")
    elif verbose:
        console.print("Extracting template...")

    try:
        if not is_current_dir:
            project_path.mkdir(parents=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_contents = zip_ref.namelist()
            if tracker:
                tracker.start("zip-list")
                tracker.complete("zip-list", f"{len(zip_contents)} entries")
            elif verbose:
                console.print(f"[cyan]ZIP contains {len(zip_contents)} items[/cyan]")

            if is_current_dir:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    zip_ref.extractall(temp_path)

                    extracted_items = list(temp_path.iterdir())
                    if tracker:
                        tracker.start("extracted-summary")
                        tracker.complete("extracted-summary", f"temp {len(extracted_items)} items")
                    elif verbose:
                        console.print(f"[cyan]Extracted {len(extracted_items)} items to temp location[/cyan]")

                    source_dir = temp_path
                    if len(extracted_items) == 1 and extracted_items[0].is_dir():
                        source_dir = extracted_items[0]
                        if tracker:
                            tracker.add("flatten", "Flatten nested directory")
                            tracker.complete("flatten")
                        elif verbose:
                            console.print(f"[cyan]Found nested directory structure[/cyan]")

                    for item in source_dir.iterdir():
                        dest_path = project_path / item.name
                        if item.is_dir():
                            if dest_path.exists():
                                if verbose and not tracker:
                                    console.print(f"[yellow]Merging directory:[/yellow] {item.name}")
                                for sub_item in item.rglob('*'):
                                    if sub_item.is_file():
                                        rel_path = sub_item.relative_to(item)
                                        dest_file = dest_path / rel_path
                                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                                        # Special handling for .vscode/settings.json - merge instead of overwrite
                                        if dest_file.name == "settings.json" and dest_file.parent.name == ".vscode":
                                            handle_vscode_settings(console, sub_item, dest_file, rel_path, verbose, tracker)
                                        else:
                                            shutil.copy2(sub_item, dest_file)
                            else:
                                shutil.copytree(item, dest_path)
                        else:
                            if dest_path.exists() and verbose and not tracker:
                                console.print(f"[yellow]Overwriting file:[/yellow] {item.name}")
                            shutil.copy2(item, dest_path)
                    if verbose and not tracker:
                        console.print(f"[cyan]Template files merged into current directory[/cyan]")
            else:
                zip_ref.extractall(project_path)

                extracted_items = list(project_path.iterdir())
                if tracker:
                    tracker.start("extracted-summary")
                    tracker.complete("extracted-summary", f"{len(extracted_items)} top-level items")
                elif verbose:
                    console.print(f"[cyan]Extracted {len(extracted_items)} items to {project_path}:[/cyan]")
                    for item in extracted_items:
                        console.print(f"  - {item.name} ({'dir' if item.is_dir() else 'file'})")

                if len(extracted_items) == 1 and extracted_items[0].is_dir():
                    nested_dir = extracted_items[0]
                    temp_move_dir = project_path.parent / f"{project_path.name}_temp"

                    shutil.move(str(nested_dir), str(temp_move_dir))

                    project_path.rmdir()

                    shutil.move(str(temp_move_dir), str(project_path))
                    if tracker:
                        tracker.add("flatten", "Flatten nested directory")
                        tracker.complete("flatten")
                    elif verbose:
                        console.print(f"[cyan]Flattened nested directory structure[/cyan]")

        # Create agent context file based on selected AI assistant
        create_agent_context_file(project_path, ai_assistant)

    except Exception as e:
        if tracker:
            tracker.error("extract", str(e))
        else:
            if verbose:
                console.print(f"[red]Error extracting template:[/red] {e}")
                if debug:
                    console.print(Panel(str(e), title="Extraction Error", border_style="red"))

        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)
    else:
        if tracker:
            tracker.complete("extract")
    finally:
        if tracker:
            tracker.add("cleanup", "Remove temporary archive")

        if zip_path.exists():
            zip_path.unlink()
            if tracker:
                tracker.complete("cleanup")
            elif verbose:
                console.print(f"Cleaned up: {zip_path.name}")

    return project_path

def copy_scripts_to_goalkit(project_path: Path, selected_script: str, tracker: StepTracker | None = None) -> None:
    """Copy script files from the source location to .goalkit/scripts/ based on selected script type"""
    # During init, we need to copy from the CLI source location, not the project
    cli_source_dir = Path(__file__).parent.parent.parent  # project root (goal-kit/goal-kit)
    scripts_source = cli_source_dir / "scripts"
    scripts_dest = project_path / ".goalkit" / "scripts"

    if not scripts_source.exists() or not scripts_source.is_dir():
        if tracker:
            tracker.add("copy-scripts", "Copy scripts")
            tracker.skip("copy-scripts", f"source not found: {scripts_source}")
        return

    try:
        # Create destination directory
        scripts_dest.mkdir(parents=True, exist_ok=True)

        # Copy all script subdirectories
        copied_count = 0
        for sub_dir in scripts_source.iterdir():
            if sub_dir.is_dir():
                dest_sub_dir = scripts_dest / sub_dir.name
                if dest_sub_dir.exists():
                    shutil.rmtree(dest_sub_dir)  # Remove existing to ensure clean copy
                shutil.copytree(sub_dir, dest_sub_dir)
                if sub_dir.name in ['bash', 'powershell']:  # Count only the specific script types
                    copied_count += len(list(sub_dir.glob('*')))

        if tracker:
            tracker.add("copy-scripts", "Copy scripts")
            tracker.complete("copy-scripts", f"copied {copied_count} scripts")
        else:
            console.print(f"[cyan]Copied scripts to .goalkit/scripts/[/cyan]")

    except Exception as e:
        if tracker:
            tracker.add("copy-scripts", "Copy scripts")
            tracker.error("copy-scripts", str(e))
        else:
            console.print(f"[red]Error copying scripts: {e}[/red]")


def copy_templates_to_goalkit(project_path: Path, tracker: StepTracker | None = None) -> None:
    """Copy template files from the source location to .goalkit/templates/"""
    # During init, we need to copy from the CLI source location, not the project
    cli_source_dir = Path(__file__).parent.parent.parent  # project root (goal-kit/goal-kit)
    templates_source = cli_source_dir / "templates"
    templates_dest = project_path / ".goalkit" / "templates"

    if not templates_source.exists() or not templates_source.is_dir():
        if tracker:
            tracker.add("copy-templates", "Copy templates")
            tracker.skip("copy-templates", f"source not found: {templates_source}")
        return

    try:
        # Create destination directory
        templates_dest.mkdir(parents=True, exist_ok=True)

        # Copy all template files (but not the commands subdirectory which is handled separately)
        copied_count = 0
        for template_file in templates_source.iterdir():
            if template_file.is_file() and template_file.suffix == ".md" and template_file.name != "agent-file-template.md":
                dest_file = templates_dest / template_file.name
                shutil.copy2(template_file, dest_file)
                copied_count += 1

        if tracker:
            tracker.add("copy-templates", "Copy templates")
            tracker.complete("copy-templates", f"copied {copied_count} templates")
        else:
            console.print(f"[cyan]Copied {copied_count} templates to .goalkit/templates/[/cyan]")

    except Exception as e:
        if tracker:
            tracker.add("copy-templates", "Copy templates")
            tracker.error("copy-templates", str(e))
        else:
            console.print(f"[red]Error copying templates: {e}[/red]")


def copy_workflows_to_goalkit(project_path: Path, tracker: StepTracker | None = None) -> None:
    """Copy workflow template files from the source location to .goalkit/workflows/"""
    cli_source_dir = Path(__file__).parent.parent.parent  # project root (goal-kit/goal-kit)
    workflows_source = cli_source_dir / "templates" / "workflows"
    workflows_dest = project_path / ".goalkit" / "workflows"

    if not workflows_source.exists() or not workflows_source.is_dir():
        if tracker:
            tracker.add("copy-workflows", "Copy workflow templates")
            tracker.skip("copy-workflows", f"source not found: {workflows_source}")
        return

    try:
        workflows_dest.mkdir(parents=True, exist_ok=True)
        copied_count = 0
        for wf_file in workflows_source.iterdir():
            if wf_file.is_file() and wf_file.suffix == ".md":
                dest_file = workflows_dest / wf_file.name
                shutil.copy2(wf_file, dest_file)
                copied_count += 1

        if tracker:
            tracker.add("copy-workflows", "Copy workflow templates")
            tracker.complete("copy-workflows", f"copied {copied_count} workflows")
    except Exception as e:
        if tracker:
            tracker.add("copy-workflows", "Copy workflow templates")
            tracker.error("copy-workflows", str(e))


def ensure_executable_scripts(project_path: Path, tracker: StepTracker | None = None) -> None:
    """Ensure POSIX .sh scripts under .goalkit/scripts (recursively) have execute bits (no-op on Windows)."""
    if os.name == "nt":
        return  # Windows: skip silently
    scripts_root = project_path / ".goalkit" / "scripts"
    if not scripts_root.is_dir():
        return
    failures: list[str] = []
    updated = 0
    for script in scripts_root.rglob("*.sh"):
        try:
            if script.is_symlink() or not script.is_file():
                continue
            try:
                with script.open("rb") as f:
                    if f.read(2) != b"#!":
                        continue
            except Exception:
                continue
            st = script.stat(); mode = st.st_mode
            if mode & 0o111:
                continue
            new_mode = mode
            if mode & 0o400: new_mode |= 0o100
            if mode & 0o040: new_mode |= 0o010
            if mode & 0o004: new_mode |= 0o001
            if not (new_mode & 0o100):
                new_mode |= 0o100
            os.chmod(script, new_mode)
            updated += 1
        except Exception as e:
            failures.append(f"{script.relative_to(scripts_root)}: {e}")
    if tracker:
        detail = f"{updated} updated" + (f", {len(failures)} failed" if failures else "")
        tracker.add("chmod", "Set script permissions recursively")
        (tracker.error if failures else tracker.complete)("chmod", detail)
    else:
        if updated:
            console.print(f"[cyan]Updated execute permissions on {updated} script(s) recursively[/cyan]")
        if failures:
            console.print("[yellow]Some scripts could not be updated:[/yellow]")
            for f in failures:
                console.print(f"  - {f}")

def create_agent_config(project_path: Path, selected_ai: str) -> None:
    """Create agent-specific configuration files and directories."""
    import shutil

    # Ensure .goalkit/goals directory exists for storing goal files
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
        "q": ".amazonq/"
    }

    # Get the agent folder name
    agent_folder = agent_folder_map.get(selected_ai)
    if not agent_folder:
        return  # Skip if agent is not in the map

    # Check if this agent requires CLI (and thus should get commands folder)
    agent_config = AGENT_CONFIG.get(selected_ai)
    requires_cli = agent_config and agent_config.get("requires_cli", False) if agent_config else False

    # Path to the agent template directory
    agent_template_path = Path(__file__).parent.parent.parent / "agent_templates" / selected_ai

    # Create agent configuration directory
    agent_config_dir = project_path / agent_folder.strip("/")  # Remove trailing slash
    agent_config_dir.mkdir(parents=True, exist_ok=True)

    # If agent template exists, copy it to the project
    if agent_template_path.exists():
        # Copy all files from the agent template directory
        for item in agent_template_path.iterdir():
            dest_path = agent_config_dir / item.name
            if item.is_file():
                shutil.copy2(item, dest_path)
            elif item.is_dir():
                shutil.copytree(item, dest_path, dirs_exist_ok=True)

    # Create agent-specific command/workflow/prompt folders
    # Define the correct folder structure for each agent type
    agent_folder_structure = {
        "claude": "commands",
        "gemini": "commands",
        "cursor": "commands",
        "qwen": "commands",
        "opencode": "command",  # Note: singular "command" not "commands"
        "windsurf": "workflows",
        "codex": "prompts",
        "kilocode": "workflows",
        "auggie": "commands",
        "roo": "commands",
        "codebuddy": "commands",
        "copilot": "prompts",
        "q": "prompts"
    }

    # Get the correct folder name for this agent
    folder_name = agent_folder_structure.get(selected_ai, "commands")
    agent_commands_dir = agent_config_dir / folder_name
    agent_commands_dir.mkdir(parents=True, exist_ok=True)

    # Copy templates - ensure all agents get appropriate templates
    # First, look for agent-specific templates if they exist
    agent_specific_template_dir = Path(__file__).parent.parent.parent / "templates" / selected_ai / folder_name
    if agent_specific_template_dir.exists():
        # Use agent-specific templates for this folder type
        for template_file in agent_specific_template_dir.iterdir():
            if template_file.is_file() and template_file.suffix == ".md":
                dest_path = agent_commands_dir / template_file.name
                shutil.copy2(template_file, dest_path)
    else:
        # Use the commands templates as a fallback for ALL agent types
        # This ensures that even agents expecting "workflows" or "prompts"
        # still get the core command templates if no specific templates exist
        commands_source_dir = Path(__file__).parent.parent.parent / "templates" / "commands"
        if commands_source_dir.exists():
            for command_file in commands_source_dir.iterdir():
                if command_file.is_file() and command_file.suffix == ".md":
                    dest_path = agent_commands_dir / command_file.name
                    shutil.copy2(command_file, dest_path)

        # Special handling for VS Code settings for Copilot
        if selected_ai == "copilot":
            vscode_settings_source = Path(__file__).parent.parent.parent / "templates" / "vscode-settings.json"
            if vscode_settings_source.exists():
                vscode_dir = project_path / ".vscode"
                vscode_dir.mkdir(parents=True, exist_ok=True)
                dest_path = vscode_dir / "settings.json"
                shutil.copy2(vscode_settings_source, dest_path)

    # Create the main agent file with project-specific guidance
    create_agent_file(project_path, selected_ai)

@app.command()
def init(
    project_name: Optional[str] = typer.Argument(None, help="Name for your new project directory (optional if using --here, or use '.' for current directory)"),
    ai_assistant: Optional[str] = typer.Option(None, "--ai", help="AI assistant to use: claude, gemini, copilot, cursor, qwen, opencode, codex, windsurf, kilocode, auggie or q"),
    script_type: Optional[str] = typer.Option(None, "--script", help="Script type to use: sh or ps"),
    ignore_agent_tools: bool = typer.Option(False, "--ignore-agent-tools", help="Skip checks for AI agent tools like Claude Code"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    here: bool = typer.Option(False, "--here", help="Initialize project in the current directory instead of creating a new one"),
    force: bool = typer.Option(False, "--force", help="Force merge/overwrite when using --here (skip confirmation)"),
    skip_tls: bool = typer.Option(False, "--skip-tls", help="Skip SSL/TLS verification (not recommended)"),
    debug: bool = typer.Option(False, "--debug", help="Show verbose diagnostic output for network and extraction failures"),
    github_token: Optional[str] = typer.Option(None, "--github-token", help="GitHub token to use for API requests (or set GH_TOKEN or GITHUB_TOKEN environment variable)"),
):
    """Initialize a new Goalkit project from the latest template.

    This command will:
    1. Check that required tools are installed (git is optional)
    2. Let you choose your AI assistant
    3. Download the appropriate template from GitHub
    4. Extract the template to a new project directory or current directory
    5. Initialize a fresh git repository (if not --no-git and no existing repo)
    6. Optionally set up AI assistant commands

    Examples:
goalkit init my-project

        goalkit init my-project --ai claude

        goalkit init my-project --ai copilot --no-git

        goalkit init --ignore-agent-tools my-project

        goalkit init . --ai claude         # Initialize in current directory

        goalkit init .                     # Initialize in current directory (interactive AI selection)

        goalkit init --here --ai claude    # Alternative syntax for current directory

        goalkit init --here --ai codex

        goalkit init --here --ai codebuddy

        goalkit init --here

        goalkit init --here --force  # Skip confirmation when current directory not empty
    """

    show_banner()

    if project_name == ".":
        here = True
        project_name = None  # Clear project_name to use existing validation logic

    if here and project_name:
        console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
        raise typer.Exit(1)

    if not here and not project_name:
        console.print("[red]Error:[/red] Must specify either a project name, use '.' for current directory, or use --here flag")
        raise typer.Exit(1)

    # Validate project name before proceeding
    if not here and project_name:
        is_valid, error_msg = validate_project_name(project_name)
        if not is_valid:
            error_panel = Panel(
                f"Invalid project name: {error_msg}",
                title="[red]Invalid Project Name[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()

        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)")
            console.print("[yellow]Template files will be merged with existing content and may overwrite existing files[/yellow]")
            if force:
                console.print("[cyan]--force supplied: skipping confirmation and proceeding with merge[/cyan]")
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
                padding=(1, 2)
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
            padding=(1, 2)
        )
        console.print()
        console.print(error_panel)
        raise typer.Exit(1)

    setup_lines = [
        "[cyan]Goalkit Project Setup[/cyan]",
        "",
        f"{'Project':<15} [green]{project_path.name}[/green]",
        f"{'Working Path':<15} [dim]{current_dir}[/dim]",
    ]

    if not here:
        setup_lines.append(f"{'Target Path':<15} [dim]{project_path}[/dim]")

    console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))

    should_init_git = False
    if not no_git:
        should_init_git = check_tool("git", CLAUDE_LOCAL_PATH)
        if not should_init_git:
            console.print("[yellow]Git not found - will skip repository initialization[/yellow]")

    if ai_assistant:
        if ai_assistant not in AGENT_CONFIG:
            console.print(f"[red]Error:[/red] Invalid AI assistant '{ai_assistant}'. Choose from: {', '.join(AGENT_CONFIG.keys())}")
            raise typer.Exit(1)
        selected_ai = ai_assistant
    else:
        # Create options dict for selection (agent_key: display_name)
        ai_choices = {key: config["name"] for key, config in AGENT_CONFIG.items()}
        selected_ai = select_with_arrows(
            console,
            ai_choices, 
            "Choose your AI assistant:", 
            "copilot"
        )

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
                    padding=(1, 2)
                )
                console.print()
                console.print(error_panel)
                raise typer.Exit(1)

    if script_type:
        if script_type not in SCRIPT_TYPE_CHOICES:
            console.print(f"[red]Error:[/red] Invalid script type '{script_type}'. Choose from: {', '.join(SCRIPT_TYPE_CHOICES.keys())}")
            raise typer.Exit(1)
        selected_script = script_type
    else:
        default_script = "ps" if os.name == "nt" else "sh"

        # Always attempt interactive selection, don't rely on isatty() check after previous interaction
        # This ensures script type selection works even after the AI assistant selection
        try:
            selected_script = select_with_arrows(console, SCRIPT_TYPE_CHOICES, "Choose script type (or press Enter)", default_script)
        except (EOFError, KeyboardInterrupt):
            # If interactive selection fails, use default
            selected_script = default_script

    console.print(f"[cyan]Selected AI assistant:[/cyan] {selected_ai}")
    console.print(f"[cyan]Selected script type:[/cyan] {selected_script}")

    tracker = StepTracker("Initialize Goalkit Project")

    global _goalkit_tracker_active
    _goalkit_tracker_active = True

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
        ("copy-workflows", "Copy workflow templates"),
        ("cleanup", "Cleanup"),
        ("git", "Initialize git repository"),
        ("final", "Finalize")
    ]:
        tracker.add(key, label)

    # Track git error message outside Live context so it persists
    git_error_message = None

    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            verify = not skip_tls
            local_ssl_context = ssl_context if verify else False
            local_client = httpx.Client(verify=local_ssl_context)

            download_and_extract_template(project_path, selected_ai, selected_script, here, verbose=False, tracker=tracker, client=local_client, debug=debug, github_token=github_token)

            # Create agent-specific configuration and commands folders
            create_agent_config(project_path, selected_ai)

            # Copy scripts to .goalkit/scripts/
            copy_scripts_to_goalkit(project_path, selected_script, tracker=tracker)

            # Copy templates to .goalkit/templates/
            copy_templates_to_goalkit(project_path, tracker=tracker)

            # Copy workflow templates to .goalkit/workflows/
            copy_workflows_to_goalkit(project_path, tracker=tracker)

            # Create the main agent file with project-specific guidance
            create_agent_file(project_path, selected_ai)

            ensure_executable_scripts(project_path, tracker=tracker)

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
                env_lines = [f"{k.ljust(_label_width)} → [bright_black]{v}[/bright_black]" for k, v in _env_pairs]
                console.print(Panel("\n".join(env_lines), title="Debug Environment", border_style="magenta"))
            if not here and project_path.exists():
                shutil.rmtree(project_path)
            raise typer.Exit(1)
        finally:
            pass

    console.print(tracker.render())
    console.print("\n[bold green]Project ready.[/bold green]")
    
    # Show git error details if initialization failed
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
            padding=(1, 2)
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
            padding=(1, 2)
        )
        console.print()
        console.print(security_notice)

    steps_lines = []
    if not here:
        steps_lines.append(f"1. Go to the project folder: [cyan]cd {project_name}[/cyan]")
        step_num = 2
    else:
        steps_lines.append("1. You're already in the project directory!")
        step_num = 2

    # Add Codex-specific setup step if needed
    if selected_ai == "codex":
        codex_path = project_path / ".codex"
        quoted_path = shlex.quote(str(codex_path))
        if os.name == "nt":  # Windows
            cmd = f"setx CODEX_HOME {quoted_path}"
        else:  # Unix-like systems
            cmd = f"export CODEX_HOME={quoted_path}"
        
        steps_lines.append(f"{step_num}. Set [cyan]CODEX_HOME[/cyan] environment variable before running Codex: [cyan]{cmd}[/cyan]")
        step_num += 1

    steps_lines.append(f"{step_num}. Start using slash commands with your AI agent:")

    steps_lines.append("   [cyan]/goalkit.vision[/] - Establish project vision and principles")
    steps_lines.append("   [cyan]/goalkit.goal[/] - Define goals and success criteria")
    steps_lines.append("   [cyan]/goalkit.strategies[/] - Explore implementation strategies")
    steps_lines.append("   [cyan]/goalkit.milestones[/] - Create measurable milestones")
    steps_lines.append("   [cyan]/goalkit.execute[/] - Execute with learning and adaptation")
    steps_lines.append("   [cyan]/goalkit.tasks[/] - Generate detailed implementation tasks")
    steps_lines.append("   [cyan]/goalkit.taskstoissues[/] - Convert tasks to GitHub issues (see .goalkit/workflows/taskstoissues.md)")
    steps_lines.append("   [cyan]/goalkit.report[/] - Generate progress reports and insights")
    steps_lines.append("   [cyan]/goalkit.review[/] - Conduct project reviews and retrospectives")

    steps_panel = Panel("\n".join(steps_lines), title="Next Steps", border_style="cyan", padding=(1,2))
    console.print()
    console.print(steps_panel)

@app.command()
def check():
    """Check that all required tools are installed."""
    show_banner()
    console.print("[bold]Checking for installed tools...[/bold]\n")

    tracker = StepTracker("Check Available Tools")

    tracker.add("git", "Git version control")
    git_ok = check_tool("git", CLAUDE_LOCAL_PATH, tracker=tracker)
    
    agent_results = {}
    for agent_key, agent_config in AGENT_CONFIG.items():
        agent_name = agent_config["name"]
        
        tracker.add(agent_key, agent_name)
        agent_results[agent_key] = check_tool(agent_key, CLAUDE_LOCAL_PATH, tracker=tracker)
    
    # Check VS Code variants (not in agent config)
    tracker.add("code", "Visual Studio Code")
    code_ok = check_tool("code", CLAUDE_LOCAL_PATH, tracker=tracker)
    
    tracker.add("code-insiders", "Visual Studio Code Insiders")
    code_insiders_ok = check_tool("code-insiders", CLAUDE_LOCAL_PATH, tracker=tracker)

    console.print(tracker.render())

    console.print("\n[bold green]Goalkit CLI is ready to use![/bold green]")

    if not git_ok:
        console.print("[dim]Tip: Install git for repository management[/dim]")

    if not any(agent_results.values()):
        console.print("[dim]Tip: Install an AI assistant for the best experience[/dim]")

@app.command()
def status(
    project_path: Optional[str] = typer.Argument(None, help="Path to goal-kit project"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed analysis"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Display project status and health information."""
    show_banner()
    project_path_obj = Path(project_path) if project_path else None
    status_command(project_path=project_path_obj, verbose=verbose, json_output=json_output)


@app.command()
def milestones(
    project_path: Optional[str] = typer.Argument(None, help="Path to goal-kit project"),
    goal_id: Optional[str] = typer.Option(None, "--goal", "-g", help="Filter by goal ID"),
    completed_only: bool = typer.Option(False, "--completed", "-c", help="Show only completed milestones"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Display milestone progress and execution history."""
    show_banner()
    project_path_obj = Path(project_path) if project_path else None
    milestones_command(
        project_path=project_path_obj,
        goal_id=goal_id,
        completed_only=completed_only,
        json_output=json_output,
    )


@app.command()
def metrics(
    project_path: Optional[str] = typer.Argument(None, help="Path to goal-kit project"),
    goal_id: Optional[str] = typer.Option(None, "--goal", "-g", help="Filter by goal ID"),
    metric_name: Optional[str] = typer.Option(None, "--metric", "-m", help="Filter by metric name"),
    days: int = typer.Option(30, "--days", "-d", help="Number of days for trend analysis"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Display project metrics and health trends."""
    show_banner()
    project_path_obj = Path(project_path) if project_path else None
    metrics_command(
        project_path=project_path_obj,
        goal_id=goal_id,
        metric_name=metric_name,
        days=days,
        json_output=json_output,
    )


@app.command()
def tasks(
    project_path: Optional[str] = typer.Argument(None, help="Path to goal-kit project"),
    goal_id: Optional[str] = typer.Option(None, "--goal", "-g", help="Filter by goal ID"),
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status (todo, in_progress, completed)"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Display and manage project tasks."""
    show_banner()
    tasks_command(
        path=project_path,
        goal_id=goal_id,
        status=status,
        json_output=json_output,
    )


@app.command()
def report(
    project_path: Optional[str] = typer.Argument(None, help="Path to goal-kit project"),
    report_type: str = typer.Option("summary", "--type", "-t", help="Report type (summary, weekly, monthly)"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Display project reports and metrics."""
    show_banner()
    report_command(
        path=project_path,
        report_type=report_type,
        json_output=json_output,
    )


@app.command()
def insights(
    project_path: Optional[str] = typer.Argument(None, help="Path to goal-kit project"),
    report_type: str = typer.Option("summary", "--type", "-t", help="Report type (summary, weekly, monthly)"),
    severity: Optional[str] = typer.Option(None, "--severity", "-s", help="Filter by severity (info, warning, alert)"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Display actionable insights based on project data."""
    show_banner()
    insights_command(
        path=project_path,
        report_type=report_type,
        severity=severity,
        json_output=json_output,
    )

def main():
    app()

if __name__ == "__main__":
    main()