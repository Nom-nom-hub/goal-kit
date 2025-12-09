"""Display project status and health information.

This module provides the /goalkit.status command which displays
comprehensive information about a Goal Kit project's current state.
"""

from pathlib import Path
from typing import Optional
import json

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..analyzer import ProjectAnalyzer, AnalysisResult


def status(
    project_path: Optional[Path] = None,
    verbose: bool = False,
    json_output: bool = False,
) -> None:
    """Display project status and health information.
    
    Shows project metadata, completion status, health score, and
    phase information. Optionally displays verbose details or JSON output.
    
    Args:
        project_path: Path to goal-kit project. If None, uses current directory.
        verbose: Show detailed analysis including all goals and metrics.
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
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        return
    
    if json_output:
        _output_json(result, console)
    else:
        _output_formatted(result, console, verbose)


def _output_json(result: AnalysisResult, console: Console) -> None:
    """Output analysis result as JSON.
    
    Args:
        result: Analysis result to output
        console: Rich console for output
    """
    output = {
        "project": {
            "name": result.project.name,
            "path": str(result.project.path),
            "agent": result.project.agent,
            "created_at": result.project.created_at.isoformat() if result.project.created_at else None,
        },
        "status": {
            "phase": result.phase,
            "completion_percent": result.completion_percent,
            "health_score": result.health_score,
        },
        "milestones": {
            "total": result.milestone_count,
            "completed": result.completed_milestones,
        },
        "goals": {
            "total": len(result.goals),
            "details": [
                {
                    "id": goal.id,
                    "name": goal.name,
                    "phase": goal.phase,
                    "completion": goal.completion_percent,
                    "criteria_count": goal.success_criteria_count,
                    "has_metrics": goal.metrics_defined,
                }
                for goal in result.goals
            ],
        },
    }
    console.print_json(data=output)


def _output_formatted(result: AnalysisResult, console: Console, verbose: bool = False) -> None:
    """Output analysis result as formatted text.
    
    Args:
        result: Analysis result to output
        console: Rich console for output
        verbose: Show detailed information
    """
    # Header with project info
    header = f"[bold blue]{result.project.name}[/bold blue]"
    if result.project.agent != "unknown":
        header += f" [dim]({result.project.agent})[/dim]"
    
    console.print(Panel(header, expand=False))
    
    # Status section
    status_text = f"""
[bold]Phase:[/bold] {_format_phase(result.phase)}
[bold]Completion:[/bold] {_format_percentage(result.completion_percent)}
[bold]Health:[/bold] {_format_health_score(result.health_score)}
"""
    console.print(Panel(status_text, title="Status", expand=False))
    
    # Goals summary
    console.print(f"\n[bold cyan]Goals ({len(result.goals)})[/bold cyan]")
    if result.goals:
        goals_table = Table(show_header=True, header_style="bold magenta")
        goals_table.add_column("Name", style="cyan")
        goals_table.add_column("Phase", style="yellow")
        goals_table.add_column("Progress", style="green")
        goals_table.add_column("Criteria")
        goals_table.add_column("Metrics", style="blue")
        
        for goal in result.goals:
            metrics_indicator = "✓" if goal.metrics_defined else "✗"
            goals_table.add_row(
                goal.name,
                goal.phase,
                f"{goal.completion_percent}%",
                str(goal.success_criteria_count),
                metrics_indicator,
            )
        
        console.print(goals_table)
    else:
        console.print("[dim]No goals found[/dim]")
    
    # Milestones summary
    if result.milestone_count > 0:
        milestone_progress = (
            f"{result.completed_milestones}/{result.milestone_count} completed"
        )
        console.print(f"\n[bold cyan]Milestones:[/bold cyan] {milestone_progress}")
    
    # Verbose output
    if verbose:
        _output_verbose(result, console)


def _output_verbose(result: AnalysisResult, console: Console) -> None:
    """Output verbose analysis details.
    
    Args:
        result: Analysis result
        console: Rich console for output
    """
    console.print("\n[bold yellow]Detailed Analysis[/bold yellow]")
    
    # Project metadata
    metadata = f"""
[bold]Project Location:[/bold] {result.project.path}
[bold]Agent:[/bold] {result.project.agent}
[bold]Created:[/bold] {result.project.created_at.strftime('%Y-%m-%d %H:%M') if result.project.created_at else 'Unknown'}
"""
    console.print(Panel(metadata, title="Project Info", expand=False))
    
    # Health score breakdown
    if result.health_score > 0:
        health_details = f"""
[bold]Overall Score:[/bold] {result.health_score}/100

[dim]Score based on:[/dim]
- [bold]Completion (40%):[/bold] {result.completion_percent:.1f}%
- [bold]Metrics (30%):[/bold] {_count_with_metrics(result.goals)}/{len(result.goals)} goals
- [bold]Criteria (20%):[/bold] {_count_with_criteria(result.goals)}/{len(result.goals)} goals
- [bold]Phase Progress (10%):[/bold] {_avg_phase_score(result.goals):.0f}%
"""
        console.print(Panel(health_details, title="Health Score Details", expand=False))


def _format_phase(phase: str) -> str:
    """Format phase name with color.
    
    Args:
        phase: Phase string
        
    Returns:
        Colored phase string
    """
    phase_colors = {
        "setup": "[yellow]Setup[/yellow]",
        "active": "[cyan]Active[/cyan]",
        "execution": "[green]Execution[/green]",
        "complete": "[bold green]Complete[/bold green]",
    }
    return phase_colors.get(phase, phase)


def _format_percentage(percent: float) -> str:
    """Format percentage with color based on value.
    
    Args:
        percent: Percentage value
        
    Returns:
        Colored percentage string
    """
    if percent >= 75:
        return f"[green]{percent}%[/green]"
    elif percent >= 50:
        return f"[yellow]{percent}%[/yellow]"
    else:
        return f"[red]{percent}%[/red]"


def _format_health_score(score: float) -> str:
    """Format health score with color based on value.
    
    Args:
        score: Health score (0-100)
        
    Returns:
        Colored health score string
    """
    if score >= 70:
        return f"[green]{score}/100[/green]"
    elif score >= 40:
        return f"[yellow]{score}/100[/yellow]"
    else:
        return f"[red]{score}/100[/red]"


def _count_with_metrics(goals) -> int:
    """Count goals with metrics defined.
    
    Args:
        goals: List of Goal objects
        
    Returns:
        Count of goals with metrics
    """
    return sum(1 for g in goals if g.metrics_defined)


def _count_with_criteria(goals) -> int:
    """Count goals with success criteria.
    
    Args:
        goals: List of Goal objects
        
    Returns:
        Count of goals with criteria
    """
    return sum(1 for g in goals if g.success_criteria_count > 0)


def _avg_phase_score(goals) -> float:
    """Calculate average phase progression score.
    
    Args:
        goals: List of Goal objects
        
    Returns:
        Average phase score (0-100)
    """
    if not goals:
        return 0.0
    
    phase_scores = {
        "vision": 10,
        "goal": 20,
        "strategies": 40,
        "milestones": 60,
        "execute": 80,
        "done": 100,
    }
    
    total = sum(phase_scores.get(g.phase, 50) for g in goals)
    return total / len(goals)
