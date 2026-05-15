"""Display project metrics and health trends.

This module provides the /goalkit.metrics command which displays
custom metrics, health scores, and metric trends.
"""

from pathlib import Path
from typing import Optional
import json

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..analyzer import ProjectAnalyzer
from ..metrics import MetricsTracker


def metrics(
    project_path: Optional[Path] = None,
    goal_id: Optional[str] = None,
    metric_name: Optional[str] = None,
    days: int = 30,
    json_output: bool = False,
) -> None:
    """Display project metrics and health trends.
    
    Shows custom metrics, health scores, trend analysis, and
    project metrics over time. Can be filtered by goal and metric name.
    
    Args:
        project_path: Path to goal-kit project. If None, uses current directory.
        goal_id: Optional goal ID to filter metrics.
        metric_name: Optional metric name to filter.
        days: Number of days for trend analysis (default: 30).
        json_output: Output results as JSON instead of formatted text.
        
    Raises:
        FileNotFoundError: If project_path is not a valid goal-kit project.
    """
    console = Console()
    
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)
    
    try:
        analyzer = ProjectAnalyzer(project_path)
        result = analyzer.analyze()
        tracker = MetricsTracker(project_path)
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        return
    
    if json_output:
        _output_json(result, tracker, goal_id, metric_name, days, console)
    else:
        _output_formatted(result, tracker, goal_id, metric_name, days, console)


def _output_json(result, tracker, goal_id: Optional[str], metric_name: Optional[str], days: int, console: Console) -> None:
    """Output metrics data as JSON.
    
    Args:
        result: Analysis result from ProjectAnalyzer
        tracker: MetricsTracker instance
        goal_id: Optional goal ID filter
        metric_name: Optional metric name filter
        days: Number of days for trends
        console: Rich console for output
    """
    # Get health score
    health = tracker.calculate_health_score(result.goals, result.completion_percent)
    
    # Build metrics data
    metrics_data = []
    
    if goal_id:
        # Filter to single goal
        goal = next((g for g in result.goals if g.id == goal_id), None)
        if not goal:
            console.print_json(data={"error": f"Goal '{goal_id}' not found"})
            return
        
        goals_to_process = [goal]
    else:
        goals_to_process = result.goals
    
    # Get metrics for each goal
    for goal in goals_to_process:
        goal_metrics = tracker.get_metrics_for_goal(goal.id)
        
        metrics_list = []
        for metric_name_key, records in goal_metrics.items():
            if metric_name and metric_name != metric_name_key:
                continue
            
            stats = tracker.get_metric_stats(goal.id, metric_name_key)
            if stats:
                metrics_list.append({
                    "name": metric_name_key,
                    "current_value": stats.current_value,
                    "average_value": round(stats.average_value, 2),
                    "min_value": stats.min_value,
                    "max_value": stats.max_value,
                    "trend": round(stats.trend, 2),
                    "total_records": stats.total_records,
                    "last_measured": stats.last_measured.isoformat() if stats.last_measured else None,
                })
        
        metrics_data.append({
            "goal_id": goal.id,
            "goal_name": goal.name,
            "metrics": metrics_list,
        })
    
    output = {
        "project": {
            "name": result.project.name,
            "path": str(result.project.path),
        },
        "health_score": {
            "overall": health.overall_score,
            "completion": health.completion_score,
            "metrics": health.metrics_score,
            "momentum": health.momentum_score,
            "quality": health.quality_score,
        },
        "goals": metrics_data,
    }
    
    console.print_json(data=output)


def _output_formatted(result, tracker, goal_id: Optional[str], metric_name: Optional[str], days: int, console: Console) -> None:
    """Output metrics data as formatted text.
    
    Args:
        result: Analysis result from ProjectAnalyzer
        tracker: MetricsTracker instance
        goal_id: Optional goal ID filter
        metric_name: Optional metric name filter
        days: Number of days for trends
        console: Rich console for output
    """
    console.print(f"\n[bold blue]{result.project.name}[/bold blue]")
    
    # Get health score
    health = tracker.calculate_health_score(result.goals, result.completion_percent)
    
    # Health score panel
    health_text = f"""
[bold]Overall:[/bold] {_format_score(health.overall_score)}
[bold]Completion:[/bold] {_format_score(health.completion_score)}
[bold]Metrics:[/bold] {_format_score(health.metrics_score)}
[bold]Momentum:[/bold] {_format_score(health.momentum_score)}
[bold]Quality:[/bold] {_format_score(health.quality_score)}
"""
    console.print(Panel(health_text, title="Health Score", expand=False))
    
    # Display goals and their metrics
    if goal_id:
        # Filter to single goal
        goals_to_display = [g for g in result.goals if g.id == goal_id]
        if not goals_to_display:
            console.print(f"[red]Goal '{goal_id}' not found[/red]")
            return
    else:
        goals_to_display = result.goals
    
    if goals_to_display:
        _display_metrics_table(tracker, goals_to_display, metric_name, console)
    else:
        console.print("[dim]No goals found[/dim]")


def _display_metrics_table(tracker, goals, metric_name_filter: Optional[str], console: Console) -> None:
    """Display metrics table for goals.
    
    Args:
        tracker: MetricsTracker instance
        goals: List of goals to display
        metric_name_filter: Optional metric name filter
        console: Rich console for output
    """
    console.print(f"\n[bold cyan]Metrics by Goal[/bold cyan]")
    
    for goal in goals:
        goal_metrics = tracker.get_metrics_for_goal(goal.id)
        
        if not goal_metrics:
            console.print(f"\n[cyan]{goal.name}[/cyan] [dim]No metrics tracked[/dim]")
            continue
        
        # Goal header
        console.print(f"\n[cyan]{goal.name}[/cyan]")
        
        # Metrics table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan", width=20)
        table.add_column("Current", style="green")
        table.add_column("Average", style="yellow")
        table.add_column("Trend", style="cyan")
        table.add_column("Records", style="dim")
        
        for metric_key, records in goal_metrics.items():
            if metric_name_filter and metric_key != metric_name_filter:
                continue
            
            stats = tracker.get_metric_stats(goal.id, metric_key)
            if stats:
                trend_str = _format_trend(stats.trend)
                table.add_row(
                    metric_key,
                    str(stats.current_value) if stats.current_value else "N/A",
                    f"{stats.average_value:.2f}",
                    trend_str,
                    str(stats.total_records),
                )
        
        console.print(table)


def _format_score(score: float) -> str:
    """Format health score with color.
    
    Args:
        score: Score value (0-100)
        
    Returns:
        Colored score string
    """
    if score >= 75:
        return f"[bold green]{score}/100[/bold green]"
    elif score >= 50:
        return f"[yellow]{score}/100[/yellow]"
    else:
        return f"[red]{score}/100[/red]"


def _format_trend(trend: float) -> str:
    """Format trend value with color and arrow.
    
    Args:
        trend: Trend value (-1 to 1)
        
    Returns:
        Colored trend string with direction
    """
    if trend > 0.1:
        return f"[green]↑ {trend:.2f}[/green]"
    elif trend < -0.1:
        return f"[red]↓ {trend:.2f}[/red]"
    else:
        return f"[yellow]→ {trend:.2f}[/yellow]"
