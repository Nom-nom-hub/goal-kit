"""CLI commands for multi-project aggregation and workspace management."""

from pathlib import Path
from typing import Optional
import json

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import typer

from ..aggregation import AggregationEngine


def show_banner() -> None:
    """Show a simple banner."""
    console = Console()
    console.print()


app = typer.Typer(help="Manage multiple projects in a workspace")


@app.command()
def list(
    workspace_path: str = typer.Option(
        ".", help="Path to the workspace directory"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output format (text, json)"
    ),
) -> None:
    """List all projects in the workspace.
    
    Discovers and displays all Goal Kit projects found in the workspace.
    """
    show_banner()
    console = Console()

    workspace_dir = Path(workspace_path)
    if not workspace_dir.exists():
        console.print("[red]Error:[/red] Workspace directory not found", style="bold")
        raise typer.Exit(1)

    try:
        engine = AggregationEngine(workspace_dir)
        projects = engine.discover_projects()

        if output == "json":
            result = {
                "project_count": len(projects),
                "projects": [
                    {
                        "name": p.name,
                        "path": str(p.path),
                        "task_count": p.task_count,
                        "completed_tasks": p.completed_tasks,
                        "completion_rate": round(p.completion_rate, 1),
                        "health_score": round(p.health_score, 1),
                    }
                    for p in projects
                ],
            }
            console.print_json(data=result)
        else:
            if not projects:
                console.print("[yellow]No projects found in workspace[/yellow]")
            else:
                table = Table(title="Workspace Projects", show_header=True, header_style="bold")
                table.add_column("Name", style="cyan")
                table.add_column("Tasks", justify="right", style="green")
                table.add_column("Completed", justify="right", style="blue")
                table.add_column("Completion %", justify="right")
                table.add_column("Health", justify="right")

                for project in projects:
                    table.add_row(
                        project.name,
                        str(project.task_count),
                        str(project.completed_tasks),
                        f"{project.completion_rate:.1f}%",
                        f"{project.health_score:.1f}",
                    )

                console.print(table)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)


@app.command()
def report(
    workspace_path: str = typer.Option(
        ".", help="Path to the workspace directory"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output format (text, json)"
    ),
) -> None:
    """Generate an aggregated report across all projects.
    
    Combines metrics and insights from all projects in the workspace.
    """
    show_banner()
    console = Console()

    workspace_dir = Path(workspace_path)
    if not workspace_dir.exists():
        console.print("[red]Error:[/red] Workspace directory not found", style="bold")
        raise typer.Exit(1)

    try:
        engine = AggregationEngine(workspace_dir)
        agg_report = engine.aggregate_reports()

        if output == "json":
            result = {
                "generated_at": agg_report.generated_at.isoformat(),
                "project_count": agg_report.project_count,
                "total_tasks": agg_report.total_tasks,
                "total_completed": agg_report.total_completed,
                "overall_completion_rate": round(agg_report.overall_completion_rate, 1),
                "overall_health_score": round(agg_report.overall_health_score, 1),
                "task_distribution": agg_report.task_distribution,
                "health_scores": {k: round(v, 1) for k, v in agg_report.health_scores.items()},
            }
            console.print_json(data=result)
        else:
            # Text output
            lines = [
                f"[bold]Workspace Aggregation Report[/bold]",
                f"Generated: {agg_report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                f"[bold cyan]Summary[/bold cyan]",
                f"  Projects: {agg_report.project_count}",
                f"  Total Tasks: {agg_report.total_tasks}",
                f"  Completed: {agg_report.total_completed}",
                f"  Overall Completion: {agg_report.overall_completion_rate:.1f}%",
                f"  Overall Health: {agg_report.overall_health_score:.1f}",
                "",
            ]

            if agg_report.health_scores:
                lines.append("[bold cyan]Health Scores by Project[/bold cyan]")
                for name, score in sorted(agg_report.health_scores.items()):
                    lines.append(f"  {name}: {score:.1f}")
                lines.append("")

            if agg_report.task_distribution:
                lines.append("[bold cyan]Task Distribution[/bold cyan]")
                for status, count in agg_report.task_distribution.items():
                    lines.append(f"  {status}: {count}")

            panel = Panel("\n".join(lines), border_style="cyan", padding=(1, 2))
            console.print(panel)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)


@app.command()
def compare(
    workspace_path: str = typer.Option(
        ".", help="Path to the workspace directory"
    ),
    metric: str = typer.Option(
        "completion_rate", "--metric", "-m",
        help="Metric to rank by: completion_rate, health_score, task_count"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output format (text, json)"
    ),
) -> None:
    """Compare projects side-by-side or ranked by metric.
    
    Shows projects ranked by the specified metric (completion rate, health score, or task count).
    """
    show_banner()
    console = Console()

    workspace_dir = Path(workspace_path)
    if not workspace_dir.exists():
        console.print("[red]Error:[/red] Workspace directory not found", style="bold")
        raise typer.Exit(1)

    try:
        engine = AggregationEngine(workspace_dir)
        ranking = engine.get_project_ranking(metric=metric)

        if not ranking:
            console.print("[yellow]No projects found[/yellow]")
            return

        if output == "json":
            result = {
                "metric": metric,
                "ranking": [
                    {
                        "rank": i + 1,
                        "name": name,
                        "value": round(value, 1),
                    }
                    for i, (name, value) in enumerate(ranking)
                ]
            }
            console.print_json(data=result)
        else:
            # Text output with ranking
            metric_label = metric.replace("_", " ").title()
            table = Table(title=f"Project Ranking by {metric_label}", show_header=True, header_style="bold")
            table.add_column("Rank", justify="right", style="cyan")
            table.add_column("Project", style="green")
            table.add_column(metric_label, justify="right")

            for i, (name, value) in enumerate(ranking, 1):
                table.add_row(
                    str(i),
                    name,
                    f"{value:.1f}" if isinstance(value, float) else str(int(value)),
                )

            console.print(table)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)


@app.command()
def summary(
    workspace_path: str = typer.Option(
        ".", help="Path to the workspace directory"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output format (text, json)"
    ),
) -> None:
    """Display workspace summary statistics.
    
    Shows high-level metrics about the entire workspace.
    """
    show_banner()
    console = Console()

    workspace_dir = Path(workspace_path)
    if not workspace_dir.exists():
        console.print("[red]Error:[/red] Workspace directory not found", style="bold")
        raise typer.Exit(1)

    try:
        engine = AggregationEngine(workspace_dir)
        summary_data = engine.get_workspace_summary()

        if output == "json":
            console.print_json(data=summary_data)
        else:
            # Text output
            panel_text = (
                f"[bold cyan]Workspace Summary[/bold cyan]\n\n"
                f"Workspace: [cyan]{summary_data['workspace_path']}[/cyan]\n"
                f"Projects: {summary_data['project_count']}\n"
                f"Total Tasks: {summary_data['total_tasks']}\n"
                f"Completed: {summary_data['total_completed']}\n"
                f"Completion Rate: {summary_data['overall_completion_rate']:.1f}%\n"
                f"Overall Health: {summary_data['overall_health_score']:.1f}\n"
                f"Generated: {summary_data['generated_at']}"
            )
            panel = Panel(panel_text, border_style="cyan", padding=(1, 2))
            console.print(panel)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)
