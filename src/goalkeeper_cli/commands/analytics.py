"""CLI commands for analytics, trends, and forecasting.

Provides commands for:
- Burndown chart visualization
- Velocity tracking
- Trend analysis
- Completion forecasting
- Automated insights
"""

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from goalkeeper_cli.analytics import AnalyticsEngine
from goalkeeper_cli.models import GoalkitProject
from goalkeeper_cli.prediction import PredictionEngine

app = typer.Typer(help="Analytics, trends, and forecasting")
console = Console()


def _get_goalkit_path() -> Path:
    """Get the .goalkit directory path."""
    return Path.cwd() / ".goalkit"


@app.command()
def burndown(
    goal_id: Optional[str] = typer.Argument(
        None, help="Goal ID (uses first goal if not specified)"
    ),
    days: int = typer.Option(14, help="Number of days to show"),
    output: str = typer.Option(
        "text", help="Output format (text, json)"
    ),
) -> None:
    """Display burndown chart for a goal."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    # Load project
    project = GoalkitProject(goalkit_path)

    # Use first goal if not specified
    if not goal_id:
        goals = project.get_goals()
        if not goals:
            console.print("[red]Error: No goals found[/red]")
            raise typer.Exit(1)
        goal_id = goals[0].id

    # Get analytics
    analytics = AnalyticsEngine(goalkit_path)
    burndown_data = analytics.get_burndown_data(goal_id)

    if not burndown_data:
        console.print(
            "[yellow]Insufficient data for burndown chart[/yellow]"
        )
        raise typer.Exit(1)

    if output == "json":
        result = {
            "goal_id": goal_id,
            "dates": burndown_data.dates,
            "ideal_remaining": burndown_data.ideal_remaining,
            "actual_remaining": burndown_data.actual_remaining,
            "completed_count": burndown_data.completed_count,
        }
        console.print_json(data=result)
    else:
        console.print(f"\n[bold]Burndown Chart - {goal_id}[/bold]")
        console.print(burndown_data.chart_ascii)


@app.command()
def velocity(
    goal_id: Optional[str] = typer.Argument(
        None, help="Goal ID (uses first goal if not specified)"
    ),
    periods: int = typer.Option(4, help="Number of periods to analyze"),
    output: str = typer.Option(
        "text", help="Output format (text, json)"
    ),
) -> None:
    """Show velocity metrics for a goal."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    # Load project
    project = GoalkitProject(goalkit_path)

    # Use first goal if not specified
    if not goal_id:
        goals = project.get_goals()
        if not goals:
            console.print("[red]Error: No goals found[/red]")
            raise typer.Exit(1)
        goal_id = goals[0].id

    # Get analytics
    analytics = AnalyticsEngine(goalkit_path)
    velocity_metrics = analytics.get_velocity_metrics(goal_id, periods)

    if not velocity_metrics:
        console.print(
            "[yellow]Insufficient data for velocity metrics[/yellow]"
        )
        raise typer.Exit(1)

    if output == "json":
        result = {
            "goal_id": goal_id,
            "periods": velocity_metrics.periods,
            "tasks_completed": velocity_metrics.tasks_completed,
            "average_velocity": velocity_metrics.average_velocity,
            "trend": velocity_metrics.trend,
            "momentum": velocity_metrics.momentum,
        }
        console.print_json(data=result)
    else:
        # Create table
        table = Table(title=f"Velocity Metrics - {goal_id}")
        table.add_column("Period", style="cyan")
        table.add_column("Tasks Completed", style="green")

        for period, completed in zip(
            velocity_metrics.periods, velocity_metrics.tasks_completed
        ):
            table.add_row(period, str(completed))

        console.print(table)

        # Summary
        emoji = "📈" if velocity_metrics.trend == "improving" else (
            "📉" if velocity_metrics.trend == "declining" else "➡️"
        )
        console.print(
            f"\n{emoji} Average Velocity: {velocity_metrics.average_velocity:.1f} "
            f"tasks/period"
        )
        console.print(f"Trend: {velocity_metrics.trend.upper()}")
        console.print(
            f"Momentum: {velocity_metrics.momentum:+.2f}"
        )


@app.command()
def trends(
    goal_id: Optional[str] = typer.Argument(
        None, help="Goal ID (uses first goal if not specified)"
    ),
    output: str = typer.Option(
        "text", help="Output format (text, json)"
    ),
) -> None:
    """Analyze trends in goal progress."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    # Load project
    project = GoalkitProject(goalkit_path)

    # Use first goal if not specified
    if not goal_id:
        goals = project.get_goals()
        if not goals:
            console.print("[red]Error: No goals found[/red]")
            raise typer.Exit(1)
        goal_id = goals[0].id

    # Get analytics
    analytics = AnalyticsEngine(goalkit_path)
    trend = analytics.get_trend_analysis(goal_id)

    if not trend:
        console.print(
            "[yellow]Insufficient data for trend analysis[/yellow]"
        )
        raise typer.Exit(1)

    if output == "json":
        result = {
            "goal_id": goal_id,
            "slope": trend.slope,
            "intercept": trend.intercept,
            "r_squared": trend.r_squared,
            "direction": trend.direction,
            "velocity_change": trend.velocity_change,
            "momentum_score": trend.momentum_score,
        }
        console.print_json(data=result)
    else:
        direction_emoji = (
            "🟢" if trend.direction == "positive"
            else "🔴" if trend.direction == "negative"
            else "⚪"
        )

        panel = Panel(
            f"[bold]Trend Analysis - {goal_id}[/bold]\n\n"
            f"Direction: {direction_emoji} {trend.direction.upper()}\n"
            f"Slope: {trend.slope:.3f} tasks/day\n"
            f"Fit Quality (R²): {trend.r_squared:.3f}\n"
            f"Momentum: {trend.momentum_score:+.2f}",
            title="Trend Analysis",
        )
        console.print(panel)


@app.command()
def forecast(
    goal_id: Optional[str] = typer.Argument(
        None, help="Goal ID (uses first goal if not specified)"
    ),
    deadline: Optional[str] = typer.Option(
        None, help="Deadline date (YYYY-MM-DD)"
    ),
    output: str = typer.Option(
        "text", help="Output format (text, json)"
    ),
) -> None:
    """Forecast goal completion date."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    # Load project
    project = GoalkitProject(goalkit_path)

    # Use first goal if not specified
    if not goal_id:
        goals = project.get_goals()
        if not goals:
            console.print("[red]Error: No goals found[/red]")
            raise typer.Exit(1)
        goal_id = goals[0].id

    # Get forecast
    analytics = AnalyticsEngine(goalkit_path)
    forecast_data = analytics.forecast_completion(goal_id, deadline)

    if not forecast_data:
        console.print(
            "[yellow]Insufficient data for forecasting[/yellow]"
        )
        raise typer.Exit(1)

    if output == "json":
        result = {
            "goal_id": goal_id,
            "estimated_date": forecast_data.estimated_date,
            "confidence": forecast_data.confidence,
            "probability": forecast_data.probability,
            "low_estimate": forecast_data.low_estimate,
            "high_estimate": forecast_data.high_estimate,
            "days_remaining": forecast_data.days_remaining,
            "tasks_remaining": forecast_data.tasks_remaining,
            "required_velocity": forecast_data.required_velocity,
        }
        console.print_json(data=result)
    else:
        # Determine emoji based on probability
        if forecast_data.probability > 0.8:
            emoji = "✅"
            status = "On Track"
        elif forecast_data.probability > 0.5:
            emoji = "⚠️"
            status = "At Risk"
        else:
            emoji = "🚨"
            status = "High Risk"

        panel = Panel(
            f"[bold]Completion Forecast - {goal_id}[/bold]\n\n"
            f"{emoji} Status: {status}\n\n"
            f"Estimated: {forecast_data.estimated_date}\n"
            f"Range: {forecast_data.low_estimate} → {forecast_data.high_estimate}\n"
            f"Confidence: {forecast_data.confidence:.1%}\n"
            f"Success Probability: {forecast_data.probability:.1%}\n\n"
            f"Tasks Remaining: {forecast_data.tasks_remaining}\n"
            f"Required Velocity: {forecast_data.required_velocity:.1f} tasks/day",
            title="Forecast",
        )
        console.print(panel)


@app.command()
def insights(
    goal_id: Optional[str] = typer.Argument(
        None, help="Goal ID (uses first goal if not specified)"
    ),
    output: str = typer.Option(
        "text", help="Output format (text, json)"
    ),
) -> None:
    """Generate automated insights about goal progress."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    # Load project
    project = GoalkitProject(goalkit_path)

    # Use first goal if not specified
    if not goal_id:
        goals = project.get_goals()
        if not goals:
            console.print("[red]Error: No goals found[/red]")
            raise typer.Exit(1)
        goal_id = goals[0].id

    # Get insights
    analytics = AnalyticsEngine(goalkit_path)
    insights_list = analytics.generate_insights(goal_id)

    if output == "json":
        result = {
            "goal_id": goal_id,
            "insights": insights_list,
        }
        console.print_json(data=result)
    else:
        console.print(f"\n[bold]Insights - {goal_id}[/bold]\n")

        for i, insight in enumerate(insights_list, 1):
            console.print(f"{i}. {insight}")


def show_banner() -> None:
    """Show analytics app banner."""
    pass
