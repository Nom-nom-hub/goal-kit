"""CLI command for task management and tracking.

Provides task listing, filtering, and status display functionality.
"""

from pathlib import Path
from typing import Optional, List
import json
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..tasks import TaskTracker, TaskStats
from ..models import TaskStatus


def tasks_command(
    path: Optional[str] = None,
    goal_id: Optional[str] = None,
    status: Optional[str] = None,
    json_output: bool = False,
) -> None:
    """Display and manage project tasks.

    Args:
        path: Project path (defaults to current directory).
        goal_id: Filter tasks by goal ID.
        status: Filter tasks by status (todo, in_progress, completed).
        json_output: Output as JSON instead of formatted text.
    """
    project_path = Path(path or ".")
    console = Console()

    try:
        tracker = TaskTracker(project_path)
    except Exception as e:
        console.print(f"[red]Error loading tasks: {e}[/red]")
        return

    tasks = tracker.get_all_tasks()

    # Apply filters
    if goal_id:
        tasks = [t for t in tasks if t.goal_id == goal_id]

    if status:
        try:
            status_enum = TaskStatus(status)
            tasks = [t for t in tasks if t.status == status_enum]
        except ValueError:
            console.print(
                f"[red]Invalid status: {status}. Use: todo, in_progress, completed[/red]"
            )
            return

    # Get statistics
    if goal_id:
        stats = tracker.get_task_stats_by_goal(goal_id)
    else:
        stats = tracker.get_task_stats()

    if json_output:
        _output_json(tasks, stats, console)
    else:
        _output_formatted(tasks, stats, console)


def _output_formatted(tasks: List, stats: TaskStats, console: Console) -> None:
    """Output tasks in formatted text display.

    Args:
        tasks: List of tasks to display.
        stats: Aggregated task statistics.
        console: Rich console for output.
    """
    # Statistics panel
    stats_text = f"""Total Tasks: {stats.total_tasks}
Completed: {stats.completed_tasks} ({stats.completion_percent:.1f}%)
In Progress: {stats.in_progress_tasks}
To Do: {stats.todo_tasks}

Estimated Hours: {stats.total_estimated_hours:.1f}
Completed Hours: {stats.completed_hours:.1f}
In Progress Hours: {stats.in_progress_hours:.1f}"""

    console.print(Panel(stats_text, title="[bold]Task Statistics[/bold]"))

    if not tasks:
        console.print("[yellow]No tasks found[/yellow]")
        return

    # Tasks table
    table = Table(title="Tasks")
    table.add_column("Task ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Goal", style="blue")
    table.add_column("Status", style="green")
    table.add_column("Est. Hours", style="yellow")
    table.add_column("Created", style="dim")

    for task in sorted(tasks, key=lambda t: t.created_at, reverse=True):
        status_color = _get_status_color(task.status)
        status_display = f"[{status_color}]{task.status.value}[/{status_color}]"

        table.add_row(
            task.id[:8],
            task.title,
            task.goal_id[:8],
            status_display,
            f"{task.estimated_hours:.1f}",
            task.created_at.strftime("%Y-%m-%d"),
        )

    console.print(table)


def _output_json(tasks: List, stats: TaskStats, console: Console) -> None:
    """Output tasks as JSON.

    Args:
        tasks: List of tasks to display.
        stats: Aggregated task statistics.
        console: Rich console for output.
    """
    output = {
        "statistics": {
            "total_tasks": stats.total_tasks,
            "completed_tasks": stats.completed_tasks,
            "in_progress_tasks": stats.in_progress_tasks,
            "todo_tasks": stats.todo_tasks,
            "completion_percent": round(stats.completion_percent, 2),
            "total_estimated_hours": round(stats.total_estimated_hours, 2),
            "completed_hours": round(stats.completed_hours, 2),
            "in_progress_hours": round(stats.in_progress_hours, 2),
            "tasks_by_goal": stats.tasks_by_goal,
            "tasks_by_status": stats.tasks_by_status,
        },
        "tasks": [
            {
                "id": task.id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "estimated_hours": task.estimated_hours,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "completed_at": task.completed_at.isoformat()
                if task.completed_at
                else None,
            }
            for task in sorted(tasks, key=lambda t: t.created_at, reverse=True)
        ],
    }

    console.print(json.dumps(output, indent=2))


def _get_status_color(status: TaskStatus) -> str:
    """Get color for task status.

    Args:
        status: The task status.

    Returns:
        Color name for Rich console.
    """
    color_map = {
        TaskStatus.TODO: "yellow",
        TaskStatus.IN_PROGRESS: "cyan",
        TaskStatus.COMPLETED: "green",
    }
    return color_map.get(status, "white")
