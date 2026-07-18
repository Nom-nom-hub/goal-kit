"""CLI commands for exporting Goal Kit data in multiple formats."""

from pathlib import Path
from typing import Optional
import json

from rich.console import Console
from rich.panel import Panel
import typer

from ..exporters import ExportManager
from ..tasks import TaskTracker
from ..reporting import ReportGenerator


def show_banner() -> None:
    """Show a simple banner."""
    console = Console()
    console.print()


def _load_flat_metrics(project_dir: Path) -> dict:
    """Load and aggregate metrics from the metrics history file.

    Reads metrics from `.goalkit/metrics_history.json` and returns
    a flat dict of metric_name -> most_recent_value.

    Args:
        project_dir: Path to the Goal Kit project

    Returns:
        Dict of metric name to latest value
    """
    flat_metrics = {}
    history_file = project_dir / ".goalkit" / "metrics_history.json"

    if history_file.exists():
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                records = json.load(f)

            for record in records:
                metric_name = record.get("metric_name", "unknown")
                value = record.get("value")
                if metric_name not in flat_metrics:
                    flat_metrics[metric_name] = value
                else:
                    # Keep the most recent value
                    flat_metrics[metric_name] = value
        except Exception:
            pass

    return flat_metrics


app = typer.Typer(help="Export project data in multiple formats")


@app.command()
def tasks(
    project_path: str = typer.Option(
        ".", help="Path to the Goal Kit project"
    ),
    format: str = typer.Option(
        "csv", "--format", "-f",
        help="Export format: csv, json, markdown, text"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o",
        help="Output file (if not specified, prints to stdout)"
    ),
) -> None:
    """Export task list in specified format.
    
    Exports all tasks from the project in the chosen format.
    """
    show_banner()
    console = Console()

    project_dir = Path(project_path)
    if not (project_dir / ".goalkit").exists():
        console.print("[red]Error:[/red] Not a Goal Kit project", style="bold")
        raise typer.Exit(1)

    try:
        tracker = TaskTracker(project_dir)
        all_tasks = tracker.get_all_tasks()

        manager = ExportManager()
        exported_data = manager.export_tasks(all_tasks, format=format)

        if output:
            output_path = Path(output)
            output_path.write_text(exported_data)
            console.print(f"[green]✓[/green] Exported {len(all_tasks)} tasks to [cyan]{output}[/cyan]")
        else:
            console.print(exported_data)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)


@app.command()
def metrics(
    project_path: str = typer.Option(
        ".", help="Path to the Goal Kit project"
    ),
    format: str = typer.Option(
        "csv", "--format", "-f",
        help="Export format: csv, json, markdown, text"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o",
        help="Output file (if not specified, prints to stdout)"
    ),
) -> None:
    """Export project metrics in specified format.
    
    Exports custom metrics and performance data.
    """
    show_banner()
    console = Console()

    project_dir = Path(project_path)
    if not (project_dir / ".goalkit").exists():
        console.print("[red]Error:[/red] Not a Goal Kit project", style="bold")
        raise typer.Exit(1)

    try:
        flat_metrics = _load_flat_metrics(project_dir)

        if not flat_metrics:
            console.print("[yellow]No metrics found in project[/yellow]")
            return

        manager = ExportManager()
        exported_data = manager.export_metrics(flat_metrics, format=format)

        if output:
            output_path = Path(output)
            output_path.write_text(exported_data)
            console.print(f"[green]✓[/green] Exported {len(flat_metrics)} metrics to [cyan]{output}[/cyan]")
        else:
            console.print(exported_data)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)


@app.command()
def all(
    project_path: str = typer.Option(
        ".", help="Path to the Goal Kit project"
    ),
    format: str = typer.Option(
        "json", "--format", "-f",
        help="Export format: json, markdown"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o",
        help="Output file (if not specified, prints to stdout)"
    ),
) -> None:
    """Export complete project data (tasks, report, and metrics).
    
    Creates a comprehensive export containing all project data.
    """
    show_banner()
    console = Console()

    project_dir = Path(project_path)
    if not (project_dir / ".goalkit").exists():
        console.print("[red]Error:[/red] Not a Goal Kit project", style="bold")
        raise typer.Exit(1)

    try:
        tracker = TaskTracker(project_dir)
        generator = ReportGenerator(project_dir)

        all_tasks = tracker.get_all_tasks()
        try:
            report_obj = generator.generate_summary_report()
        except Exception:
            report_obj = generator.generate_weekly_report()

        flat_metrics = _load_flat_metrics(project_dir)

        manager = ExportManager()

        if format == "json":
            # JSON export with all data
            
            export_data = {
                "tasks": json.loads(manager.export_tasks(all_tasks, "json")),
                "report": json.loads(manager.export_report(report_obj, "json")),
                "metrics": flat_metrics,
            }
            exported_data = json.dumps(export_data, indent=2)
        elif format == "markdown":
            # Markdown export with sections
            sections = [
                "# Complete Project Export",
                "",
                "## Tasks",
                "",
                manager.export_tasks(all_tasks, "markdown"),
                "",
                "## Report",
                "",
                manager.export_report(report_obj, "markdown"),
                "",
                "## Metrics",
                "",
                manager.export_metrics(flat_metrics, "markdown"),
            ]
            exported_data = "\n".join(sections)
        else:
            console.print(f"[red]Error:[/red] Format '{format}' not supported for 'all' command (use json or markdown)")
            raise typer.Exit(1)

        if output:
            output_path = Path(output)
            output_path.write_text(exported_data)
            console.print(f"[green]✓[/green] Exported complete project to [cyan]{output}[/cyan]")
        else:
            console.print(exported_data)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)


@app.command()
def formats() -> None:
    """Show available export formats."""
    show_banner()
    console = Console()

    formats_info = [
        "[bold cyan]Available Export Formats[/bold cyan]",
        "",
        "[bold]CSV[/bold] - Comma-separated values",
        "  - Best for: Spreadsheets, data analysis",
        "  - Commands: export tasks, export report, export metrics",
        "",
        "[bold]JSON[/bold] - JavaScript Object Notation",
        "  - Best for: APIs, data interchange, programmatic processing",
        "  - Commands: export tasks, export report, export metrics, export all",
        "",
        "[bold]Markdown[/bold] - Formatted text document",
        "  - Best for: Documentation, reports, sharing",
        "  - Commands: export tasks, export report, export metrics, export all",
        "",
        "[bold]Text[/bold] - Plain text format",
        "  - Best for: Simple viewing, email, plain text",
        "  - Commands: export tasks, export report, export metrics",
    ]

    panel = Panel("\n".join(formats_info), border_style="cyan", padding=(1, 2))
    console.print(panel)
