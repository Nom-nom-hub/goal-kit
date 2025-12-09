"""Display milestone progress and execution history.

This module provides the /goalkit.milestones command which displays
milestone completion status, execution velocity, and project momentum.
"""

from pathlib import Path
from typing import Optional
import json

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..analyzer import ProjectAnalyzer
from ..execution import ExecutionTracker


def milestones(
    project_path: Optional[Path] = None,
    goal_id: Optional[str] = None,
    completed_only: bool = False,
    json_output: bool = False,
) -> None:
    """Display milestone progress and execution history.
    
    Shows milestone completion status, velocity metrics, momentum score,
    and recent milestone achievements. Can be filtered by goal and
    optionally show only completed milestones.
    
    Args:
        project_path: Path to goal-kit project. If None, uses current directory.
        goal_id: Optional goal ID to filter milestones.
        completed_only: Show only completed milestones.
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
        tracker = ExecutionTracker(project_path)
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        return
    
    if json_output:
        _output_json(result, tracker, goal_id, console)
    else:
        _output_formatted(result, tracker, goal_id, console)


def _output_json(result, tracker, goal_id: Optional[str], console: Console) -> None:
    """Output milestone data as JSON.
    
    Args:
        result: Analysis result from ProjectAnalyzer
        tracker: ExecutionTracker instance
        goal_id: Optional goal ID filter
        console: Rich console for output
    """
    # Get execution stats
    stats = tracker.get_execution_stats(result.goals, result.completion_percent)
    
    # Build milestone data
    milestones_data = []
    
    if goal_id:
        # Filter to single goal
        goal = next((g for g in result.goals if g.id == goal_id), None)
        if not goal:
            console.print_json(data={"error": f"Goal '{goal_id}' not found"})
            return
        
        goals_to_process = [goal]
    else:
        goals_to_process = result.goals
    
    # Get history for each goal
    for goal in goals_to_process:
        history = tracker.get_milestone_history(goal_id=goal.id, limit=100)
        goal_stats = tracker.get_goal_execution_stats(goal.id)
        
        milestones_data.append({
            "goal_id": goal.id,
            "goal_name": goal.name,
            "completed_milestones": goal_stats["completed_milestones"],
            "recent_milestones": goal_stats["recent_milestones"],
            "last_completion": goal_stats["last_completion"],
        })
    
    output = {
        "project": {
            "name": result.project.name,
            "path": str(result.project.path),
        },
        "milestones": {
            "total": stats.total_milestones,
            "completed": stats.completed_milestones,
            "completion_percent": round(stats.completion_percent, 1),
        },
        "velocity": {
            "per_day": round(stats.velocity_per_day, 2),
            "estimated_completion": (
                stats.estimated_completion.isoformat()
                if stats.estimated_completion else None
            ),
        },
        "momentum": {
            "score": round(tracker.get_momentum(days=7), 1),
            "recent_days": 7,
        },
        "goals": milestones_data,
    }
    
    console.print_json(data=output)


def _output_formatted(result, tracker, goal_id: Optional[str], console: Console) -> None:
    """Output milestone data as formatted text.
    
    Args:
        result: Analysis result from ProjectAnalyzer
        tracker: ExecutionTracker instance
        goal_id: Optional goal ID filter
        console: Rich console for output
    """
    console.print(f"\n[bold blue]{result.project.name}[/bold blue]")
    
    # Get execution stats
    stats = tracker.get_execution_stats(result.goals, result.completion_percent)
    
    # Summary panel
    summary = f"""
[bold]Completion:[/bold] {stats.completed_milestones}/{stats.total_milestones} ({stats.completion_percent:.1f}%)
[bold]Velocity:[/bold] {stats.velocity_per_day:.2f} milestones/day
[bold]Momentum:[/bold] {_format_momentum(tracker.get_momentum(days=7))}
"""
    if stats.estimated_completion:
        summary += f"[bold]Est. Completion:[/bold] {stats.estimated_completion.strftime('%Y-%m-%d')}\n"
    
    console.print(Panel(summary, title="Milestone Summary", expand=False))
    
    # Display goals and their milestones
    if goal_id:
        # Filter to single goal
        goals_to_display = [g for g in result.goals if g.id == goal_id]
        if not goals_to_display:
            console.print(f"[red]Goal '{goal_id}' not found[/red]")
            return
    else:
        goals_to_display = result.goals
    
    if goals_to_display:
        _display_milestone_table(tracker, goals_to_display, console)
    else:
        console.print("[dim]No goals found[/dim]")
    
    # Timeline
    timeline = tracker.get_completion_timeline(days=30)
    if timeline:
        _display_timeline(timeline, console)


def _display_milestone_table(tracker, goals, console: Console) -> None:
    """Display milestone completion table for goals.
    
    Args:
        tracker: ExecutionTracker instance
        goals: List of goals to display
        console: Rich console for output
    """
    console.print(f"\n[bold cyan]Milestones by Goal[/bold cyan]")
    
    for goal in goals:
        stats = tracker.get_goal_execution_stats(goal.id)
        completed = stats["completed_milestones"]
        recent = stats["recent_milestones"]
        last = stats["last_completion"]
        
        # Goal header
        goal_info = f"[cyan]{goal.name}[/cyan] "
        if completed > 0:
            goal_info += f"[green]{completed} completed[/green]"
        else:
            goal_info += "[yellow]None completed[/yellow]"
        
        console.print(f"\n{goal_info}")
        
        # Recent milestones table
        if recent:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Milestone", style="cyan", width=30)
            table.add_column("Completed", style="green")
            table.add_column("Notes", style="dim")
            
            for m in recent:
                completed_date = m["completed_at"][:10] if m["completed_at"] else "N/A"
                notes = m.get("notes") or "-"
                table.add_row(
                    m["id"][:25],
                    completed_date,
                    notes[:40],
                )
            
            console.print(table)
        else:
            console.print("[dim]No milestones completed[/dim]")


def _display_timeline(timeline: dict, console: Console) -> None:
    """Display completion timeline chart.
    
    Args:
        timeline: Dictionary mapping date to completion count
        console: Rich console for output
    """
    console.print(f"\n[bold cyan]Recent Activity (30 days)[/bold cyan]")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Date", style="cyan")
    table.add_column("Completions", style="green")
    table.add_column("Chart", style="yellow")
    
    # Sort dates in descending order (most recent first)
    sorted_dates = sorted(timeline.keys(), reverse=True)
    
    for date in sorted_dates[:14]:  # Show last 14 days
        count = timeline[date]
        chart = "█" * min(count, 10)  # Max 10 blocks
        table.add_row(date, str(count), chart)
    
    console.print(table)


def _format_momentum(score: float) -> str:
    """Format momentum score with color and description.
    
    Args:
        score: Momentum score (0-100)
        
    Returns:
        Colored momentum string with description
    """
    if score >= 80:
        return f"[bold green]{score:.0f}/100 (Excellent)[/bold green]"
    elif score >= 60:
        return f"[green]{score:.0f}/100 (Good)[/green]"
    elif score >= 40:
        return f"[yellow]{score:.0f}/100 (Fair)[/yellow]"
    elif score >= 20:
        return f"[orange]{score:.0f}/100 (Low)[/orange]"
    else:
        return f"[red]{score:.0f}/100 (Stalled)[/red]"
