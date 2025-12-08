"""Tool detection command."""

from pathlib import Path
from rich.console import Console

from ..agents import AGENT_CONFIG
from ..helpers import StepTracker, check_tool

console = Console()

# Get Claude's local path for tool detection
CLAUDE_LOCAL_PATH = Path.home() / ".claude" / "local" / "claude"


def check() -> None:
    """Check that all required tools are installed.
    
    This command verifies:
    1. Git version control system
    2. All configured AI assistants
    3. VS Code variants (if installed)
    """
    from .. import show_banner

    show_banner()
    console.print("[bold]Checking for installed tools...[/bold]\n")

    tracker = StepTracker("Check Available Tools")

    # Check git
    tracker.add("git", "Git version control")
    git_ok = check_tool("git", CLAUDE_LOCAL_PATH, tracker=tracker)

    # Check agents
    agent_results = {}
    for agent_key, agent_config in AGENT_CONFIG.items():
        agent_name = agent_config["name"]

        tracker.add(agent_key, agent_name)
        agent_results[agent_key] = check_tool(agent_key, CLAUDE_LOCAL_PATH, tracker=tracker)

    # Check VS Code variants
    tracker.add("code", "Visual Studio Code")
    code_ok = check_tool("code", CLAUDE_LOCAL_PATH, tracker=tracker)

    tracker.add("code-insiders", "Visual Studio Code Insiders")
    code_insiders_ok = check_tool("code-insiders", CLAUDE_LOCAL_PATH, tracker=tracker)

    console.print(tracker.render())

    console.print("\n[bold green]Goalkeeper CLI is ready to use![/bold green]")

    if not git_ok:
        console.print("[dim]Tip: Install git for repository management[/dim]")

    if not any(agent_results.values()):
        console.print("[dim]Tip: Install an AI assistant for the best experience[/dim]")
