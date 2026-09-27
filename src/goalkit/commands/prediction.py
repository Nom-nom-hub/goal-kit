"""CLI commands for predictive goal analytics.

Exposes the PredictionEngine as user-facing commands:
- predict completion: estimated completion date with confidence
- predict risk: deadline risk assessment
- predict velocity: required velocity to meet a deadline
- predict scenarios: what-if scenario comparison
"""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from goalkit.prediction import PredictionEngine

app = typer.Typer(help="Deadline risk, required velocity, and what-if scenarios")
console = Console()


def _get_goalkit_path() -> Path:
    """Get the .goalkit directory path."""
    return Path.cwd() / ".goalkit"


def _resolve_goal_id(goal_id: Optional[str]) -> str:
    """Resolve goal ID, falling back to the first available goal.

    Returns:
        Resolved goal ID string

    Raises:
        typer.Exit(1) if no goals found or .goalkit not found
    """
    if goal_id:
        return goal_id

    goalkit_path = _get_goalkit_path()
    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    # Try goals.json first
    goals_json = goalkit_path / "goals.json"
    if goals_json.exists():
        try:
            with open(goals_json) as f:
                goals_data = json.load(f)
            if isinstance(goals_data, list) and goals_data:
                first = goals_data[0]
                if isinstance(first, dict) and "id" in first:
                    return first["id"]
        except (json.JSONDecodeError, IndexError):
            pass

    # Try goals directory as fallback
    goals_dir = goalkit_path / "goals"
    if goals_dir.exists():
        goal_files = sorted(goals_dir.glob("*.md"))
        if goal_files:
            return goal_files[0].stem

    console.print("[red]Error: No goals found. Please specify a goal ID.[/red]")
    raise typer.Exit(1)


@app.command()
def completion(
    goal_id: Optional[str] = typer.Argument(
        None, help="Goal ID (uses first goal if not specified)"
    ),
    confidence: float = typer.Option(
        0.95, "--confidence", "-c", min=0.0, max=1.0, help="Confidence level (0-1)"
    ),
    output: str = typer.Option("text", help="Output format (text, json)"),
) -> None:
    """Estimate goal completion date with a confidence interval."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    goal_id = _resolve_goal_id(goal_id)

    engine = PredictionEngine(goalkit_path)
    estimated_date = engine.estimate_completion_date(goal_id, confidence=confidence)

    if not estimated_date:
        console.print("[yellow]Insufficient data to estimate completion date[/yellow]")
        console.print("[dim]Record task progress over a few days first (goalkit analytics)[/dim]")
        raise typer.Exit(1)

    if output == "json":
        result = {
            "goal_id": goal_id,
            "estimated_date": estimated_date,
            "confidence": confidence,
        }
        console.print_json(data=result)
    else:
        console.print(
            Panel(
                f"[bold]Estimated completion:[/bold] {estimated_date}\n"
                f"[bold]Confidence level:[/bold] {confidence:.0%}",
                title=f"🔮 Completion Forecast — {goal_id}",
                border_style="cyan",
            )
        )


@app.command()
def risk(
    goal_id: Optional[str] = typer.Argument(
        None, help="Goal ID (uses first goal if not specified)"
    ),
    deadline: str = typer.Option(..., "--deadline", "-d", help="Deadline date (YYYY-MM-DD)"),
    output: str = typer.Option("text", help="Output format (text, json)"),
) -> None:
    """Assess the risk of missing a deadline."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    goal_id = _resolve_goal_id(goal_id)

    engine = PredictionEngine(goalkit_path)
    assessment = engine.assess_deadline_risk(goal_id, deadline)

    if not assessment:
        console.print("[yellow]Insufficient data to assess deadline risk[/yellow]")
        console.print("[dim]Record task progress over a few days first (goalkit analytics)[/dim]")
        raise typer.Exit(1)

    if output == "json":
        result = {"goal_id": goal_id, **asdict(assessment)}
        console.print_json(data=result)
    else:
        risk_color = "red" if assessment.at_risk else "green"
        risk_label = "Yes" if assessment.at_risk else "No"
        console.print(
            Panel(
                f"[bold]At risk:[/bold] {risk_label}\n"
                f"[bold]Risk score:[/bold] {assessment.risk_score:.2f}\n"
                f"[bold]Days until deadline:[/bold] {assessment.days_until_deadline}\n"
                f"[bold]Current velocity:[/bold] {assessment.current_velocity:.2f} tasks/day\n"
                f"[bold]Required velocity:[/bold] {assessment.required_velocity:.2f} tasks/day\n\n"
                f"{assessment.recommendation}",
                title=f"⚠️  Deadline Risk — {goal_id}",
                border_style=risk_color,
            )
        )


@app.command()
def velocity(
    goal_id: Optional[str] = typer.Argument(
        None, help="Goal ID (uses first goal if not specified)"
    ),
    deadline: str = typer.Option(..., "--deadline", "-d", help="Deadline date (YYYY-MM-DD)"),
    output: str = typer.Option("text", help="Output format (text, json)"),
) -> None:
    """Calculate the velocity needed to meet a deadline."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    goal_id = _resolve_goal_id(goal_id)

    engine = PredictionEngine(goalkit_path)
    required = engine.calculate_required_velocity(goal_id, deadline)

    if not required:
        console.print("[yellow]Insufficient data to calculate required velocity[/yellow]")
        console.print("[dim]Record task progress over a few days first (goalkit analytics)[/dim]")
        raise typer.Exit(1)

    if output == "json":
        result = {"goal_id": goal_id, **asdict(required)}
        console.print_json(data=result)
    else:
        feasibility = (
            "[green]Feasible[/green] at current pace"
            if required.feasible
            else "[red]Not feasible[/red] at current pace"
        )
        console.print(
            Panel(
                f"[bold]Tasks remaining:[/bold] {required.tasks_remaining}\n"
                f"[bold]Days available:[/bold] {required.days_available}\n"
                f"[bold]Required pace:[/bold] {required.required_per_day:.2f} tasks/day "
                f"({required.required_per_week:.1f}/week)\n"
                f"[bold]Current pace:[/bold] {required.current_velocity:.2f} tasks/day\n"
                f"[bold]Contingency buffer:[/bold] {required.buffer_days} days\n\n"
                f"{feasibility}",
                title=f"🏃 Required Velocity — {goal_id}",
                border_style="cyan",
            )
        )


@app.command()
def scenarios(
    goal_id: Optional[str] = typer.Argument(
        None, help="Goal ID (uses first goal if not specified)"
    ),
    deadline: str = typer.Option(..., "--deadline", "-d", help="Deadline date (YYYY-MM-DD)"),
    output: str = typer.Option("text", help="Output format (text, json)"),
) -> None:
    """Compare what-if scenarios for meeting a deadline."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    goal_id = _resolve_goal_id(goal_id)

    engine = PredictionEngine(goalkit_path)
    results = engine.compare_scenarios(goal_id, deadline)

    if not results:
        console.print("[yellow]Insufficient data to run scenario analysis[/yellow]")
        console.print("[dim]Record task progress over a few days first (goalkit analytics)[/dim]")
        raise typer.Exit(1)

    if output == "json":
        console.print_json(
            data={
                "goal_id": goal_id,
                "deadline": deadline,
                "scenarios": [asdict(r) for r in results],
            }
        )
    else:
        table = Table(title=f"🔮 What-If Scenarios — {goal_id} (deadline {deadline})")
        table.add_column("Scenario", style="bold")
        table.add_column("Projected Completion")
        table.add_column("Success Probability")
        table.add_column("Risk Level")
        table.add_column("Cost")

        risk_styles = {"low": "green", "medium": "yellow", "high": "red"}
        for r in results:
            style = risk_styles.get(r.risk_level, "white")
            table.add_row(
                r.scenario_name,
                r.completion_date,
                f"{r.probability:.0%}",
                f"[{style}]{r.risk_level}[/{style}]",
                r.additional_resource_cost,
            )

        console.print(table)
