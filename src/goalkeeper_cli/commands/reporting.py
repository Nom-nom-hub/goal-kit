"""CLI commands for project reporting and insights.

Provides project summaries, trend analysis, and actionable insights.
"""

from pathlib import Path
from typing import Optional
import json

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..reporting import ReportGenerator, ReportType, InsightSeverity


def report_command(
    path: Optional[str] = None,
    report_type: str = "summary",
    json_output: bool = False,
) -> None:
    """Display project reports.

    Args:
        path: Project path (defaults to current directory).
        report_type: Type of report (summary, weekly, monthly).
        json_output: Output as JSON instead of formatted text.
    """
    project_path = Path(path or ".")
    console = Console()

    try:
        generator = ReportGenerator(project_path)
    except Exception as e:
        console.print(f"[red]Error loading project: {e}[/red]")
        return

    # Generate appropriate report
    try:
        if report_type == "weekly":
            report = generator.generate_weekly_report()
        elif report_type == "monthly":
            report = generator.generate_monthly_report()
        else:
            report = generator.generate_summary_report()
    except Exception as e:
        console.print(f"[red]Error generating report: {e}[/red]")
        return

    if json_output:
        _output_report_json(report, console)
    else:
        _output_report_formatted(report, console)


def insights_command(
    path: Optional[str] = None,
    report_type: str = "summary",
    severity: Optional[str] = None,
    json_output: bool = False,
) -> None:
    """Display project insights.

    Args:
        path: Project path (defaults to current directory).
        report_type: Type of report (summary, weekly, monthly).
        severity: Filter by severity (info, warning, alert).
        json_output: Output as JSON instead of formatted text.
    """
    project_path = Path(path or ".")
    console = Console()

    try:
        generator = ReportGenerator(project_path)
    except Exception as e:
        console.print(f"[red]Error loading project: {e}[/red]")
        return

    # Generate appropriate report
    try:
        if report_type == "weekly":
            report = generator.generate_weekly_report()
        elif report_type == "monthly":
            report = generator.generate_monthly_report()
        else:
            report = generator.generate_summary_report()
    except Exception as e:
        console.print(f"[red]Error generating report: {e}[/red]")
        return

    # Filter insights by severity if specified
    insights = report.insights
    if severity:
        try:
            severity_enum = InsightSeverity(severity)
            insights = [i for i in insights if i.severity == severity_enum]
        except ValueError:
            console.print(
                f"[red]Invalid severity: {severity}. Use: info, warning, alert[/red]"
            )
            return

    if json_output:
        _output_insights_json(insights, console)
    else:
        _output_insights_formatted(insights, console)


def _output_report_formatted(report, console: Console) -> None:
    """Output report in formatted text display.

    Args:
        report: Report object to display.
        console: Rich console for output.
    """
    # Header panel with title and period
    header_text = f"{report.title}\n{report.period_start.strftime('%Y-%m-%d')} to {report.period_end.strftime('%Y-%m-%d')}"
    console.print(Panel(header_text, border_style="cyan", padding=(1, 2)))

    # Summary section
    summary_lines = []
    for key, value in report.summary.items():
        if isinstance(value, float):
            summary_lines.append(f"{key.replace('_', ' ').title()}: {value:.1f}")
        else:
            summary_lines.append(f"{key.replace('_', ' ').title()}: {value}")

    console.print(Panel("\n".join(summary_lines), title="[bold]Summary[/bold]"))

    # Metrics table
    if report.metrics:
        table = Table(title="Metrics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        for metric_name, metric_value in report.metrics.items():
            table.add_row(metric_name.replace("_", " ").title(), f"{metric_value:.2f}")

        console.print(table)

    # Insights section
    if report.insights:
        console.print(Panel("[bold]Insights[/bold]", border_style="yellow"))
        for insight in report.insights:
            severity_color = _get_severity_color(insight.severity)
            console.print(
                f"[{severity_color}]{insight.severity.value.upper()}[/{severity_color}] {insight.title}"
            )
            console.print(f"  {insight.description}")
            if insight.recommendation:
                console.print(f"  [cyan]→ {insight.recommendation}[/cyan]")
            console.print()


def _output_report_json(report, console: Console) -> None:
    """Output report as JSON.

    Args:
        report: Report object to display.
        console: Rich console for output.
    """
    output = {
        "title": report.title,
        "report_type": report.report_type.value,
        "period_start": report.period_start.isoformat(),
        "period_end": report.period_end.isoformat(),
        "summary": report.summary,
        "metrics": report.metrics,
        "insights": [
            {
                "type": insight.type.value,
                "title": insight.title,
                "description": insight.description,
                "severity": insight.severity.value,
                "value": insight.value,
                "recommendation": insight.recommendation,
            }
            for insight in report.insights
        ],
        "generated_at": report.generated_at.isoformat(),
    }

    console.print(json.dumps(output, indent=2))


def _output_insights_formatted(insights, console: Console) -> None:
    """Output insights in formatted text display.

    Args:
        insights: List of insights to display.
        console: Rich console for output.
    """
    if not insights:
        console.print("[yellow]No insights available[/yellow]")
        return

    console.print(Panel(f"[bold]{len(insights)} Insights[/bold]", border_style="cyan"))

    for i, insight in enumerate(insights, 1):
        severity_color = _get_severity_color(insight.severity)
        console.print(
            f"{i}. [{severity_color}]{insight.severity.value.upper()}[/{severity_color}] {insight.title}"
        )
        console.print(f"   Type: {insight.type.value}")
        console.print(f"   {insight.description}")
        if insight.recommendation:
            console.print(f"   → {insight.recommendation}")
        console.print()


def _output_insights_json(insights, console: Console) -> None:
    """Output insights as JSON.

    Args:
        insights: List of insights to display.
        console: Rich console for output.
    """
    output = {
        "count": len(insights),
        "insights": [
            {
                "type": insight.type.value,
                "title": insight.title,
                "description": insight.description,
                "severity": insight.severity.value,
                "value": insight.value,
                "recommendation": insight.recommendation,
            }
            for insight in insights
        ],
    }

    console.print(json.dumps(output, indent=2))


def _get_severity_color(severity: InsightSeverity) -> str:
    """Get color for insight severity.

    Args:
        severity: The insight severity.

    Returns:
        Color name for Rich console.
    """
    color_map = {
        InsightSeverity.INFO: "cyan",
        InsightSeverity.WARNING: "yellow",
        InsightSeverity.ALERT: "red",
    }
    return color_map.get(severity, "white")
