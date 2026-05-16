"""
Goalkit CLI application setup.

Handles Typer app creation, banner display, project context,
GitHub authentication helpers, and command wire-ups.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional
import ssl

import typer
import httpx
import truststore
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from typer.core import TyperGroup

from .helpers import load_project_context

ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = httpx.Client(verify=ssl_context)

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

CLAUDE_LOCAL_PATH = Path.home() / ".claude" / "local" / "claude"

SCRIPT_TYPE_CHOICES = {
    "sh": "POSIX Shell (bash/zsh) - downloads shell-based templates",
    "ps": "PowerShell - downloads PowerShell-based templates",
}


def _github_token(cli_token: str | None = None) -> str | None:
    """Return sanitized GitHub token (cli arg takes precedence) or None."""
    return ((cli_token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()) or None


def _github_auth_headers(cli_token: str | None = None) -> dict:
    """Return Authorization header dict only when a non-empty token exists."""
    token = _github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}


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
    display_project_context()


def display_project_context():
    """Display project context if in a Goal Kit project."""
    context = load_project_context()
    if context:
        status_text = f"""
[bold]Project:[/bold] {context['project_name']}
[bold]Phase:[/bold] {context['phase'].title()}
[bold]Health Score:[/bold] {context['health_score']}/100
[bold]Completion:[/bold] {context['completion_percent']}%

[bold]Goals:[/bold] {context['total_goals']} | [bold]Milestones:[/bold] {context['completed_milestones']}/{context['total_milestones']}
"""
        console.print(Panel(status_text, title="[green]Goal Kit Project Detected[/green]", border_style="green"))

        if context['goals']:
            console.print(f"\n[bold cyan]Active Goals ({len(context['goals'])}):[/bold cyan]")
            for goal in context['goals']:
                console.print(f"  \u2022 [cyan]{goal['name']}[/cyan] - {goal['phase']} ({goal['completion_percent']}%)")


class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""

    def format_help(self, ctx, formatter):
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="goalkit",
    help="Goal-Driven Development tool for AI agents",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)


@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided."""
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" in sys.argv:
        show_banner()
        console.print(Align.center("[dim]Run 'goalkit --help' for usage information[/dim]"))
        console.print()


# ---------------------------------------------------------------------------
# Wire sub-commands from command modules (deferred imports to avoid cycles)
# ---------------------------------------------------------------------------

def _wire_commands():
    """Import and register all CLI commands on the app.

    Called at module bottom so command modules can import from goalkit.app
    without circular dependency issues.
    """
    from .commands.init import init
    from .commands.check import check
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

    # Register top-level commands
    app.command()(init)
    app.command()(check)

    # Register thin wrapper commands
    def status_wrapper(
        project_path: Optional[str] = typer.Argument(None, help="Path to goal-kit project"),
        verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed analysis"),
        json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
    ):
        show_banner()
        project_path_obj = Path(project_path) if project_path else None
        status_command(project_path=project_path_obj, verbose=verbose, json_output=json_output)

    def milestones_wrapper(
        project_path: Optional[str] = typer.Argument(None, help="Path to goal-kit project"),
        goal_id: Optional[str] = typer.Option(None, "--goal", "-g", help="Filter by goal ID"),
        completed_only: bool = typer.Option(False, "--completed", "-c", help="Show only completed milestones"),
        json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
    ):
        show_banner()
        project_path_obj = Path(project_path) if project_path else None
        milestones_command(
            project_path=project_path_obj,
            goal_id=goal_id,
            completed_only=completed_only,
            json_output=json_output,
        )

    def metrics_wrapper(
        project_path: Optional[str] = typer.Argument(None, help="Path to goal-kit project"),
        goal_id: Optional[str] = typer.Option(None, "--goal", "-g", help="Filter by goal ID"),
        metric_name: Optional[str] = typer.Option(None, "--metric", "-m", help="Filter by metric name"),
        days: int = typer.Option(30, "--days", "-d", help="Number of days for trend analysis"),
        json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
    ):
        show_banner()
        project_path_obj = Path(project_path) if project_path else None
        metrics_command(
            project_path=project_path_obj,
            goal_id=goal_id,
            metric_name=metric_name,
            days=days,
            json_output=json_output,
        )

    def tasks_wrapper(
        project_path: Optional[str] = typer.Argument(None, help="Path to goal-kit project"),
        goal_id: Optional[str] = typer.Option(None, "--goal", "-g", help="Filter by goal ID"),
        status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status (todo, in_progress, completed)"),
        json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
    ):
        show_banner()
        tasks_command(
            path=project_path,
            goal_id=goal_id,
            status=status,
            json_output=json_output,
        )

    def report_wrapper(
        project_path: Optional[str] = typer.Argument(None, help="Path to goal-kit project"),
        report_type: str = typer.Option("summary", "--type", "-t", help="Report type (summary, weekly, monthly)"),
        json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
    ):
        show_banner()
        report_command(
            path=project_path,
            report_type=report_type,
            json_output=json_output,
        )

    def insights_wrapper(
        project_path: Optional[str] = typer.Argument(None, help="Path to goal-kit project"),
        report_type: str = typer.Option("summary", "--type", "-t", help="Report type (summary, weekly, monthly)"),
        severity: Optional[str] = typer.Option(None, "--severity", "-s", help="Filter by severity (info, warning, alert)"),
        json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
    ):
        show_banner()
        insights_command(
            path=project_path,
            report_type=report_type,
            severity=severity,
            json_output=json_output,
        )

    app.command(name="status")(status_wrapper)
    app.command(name="milestones")(milestones_wrapper)
    app.command(name="metrics")(metrics_wrapper)
    app.command(name="tasks")(tasks_wrapper)
    app.command(name="report")(report_wrapper)
    app.command(name="insights")(insights_wrapper)

    # Register sub-apps
    app.add_typer(dependencies_app, name="dependencies", help="Manage task dependencies and critical paths")
    app.add_typer(aggregation_app, name="projects", help="Manage multiple projects in a workspace")
    app.add_typer(export_app, name="export", help="Export project data in multiple formats")
    app.add_typer(analytics_app, name="analytics", help="Analytics, trends, and forecasting")
    app.add_typer(webhooks_app, name="webhooks", help="Webhook management and event notifications")


_wire_commands()
