"""CLI commands for task dependency management."""

from pathlib import Path
from typing import Optional
import json

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
import typer

from ..dependencies import DependencyTracker
from ..tasks import TaskTracker


def show_banner() -> None:
    """Show a simple banner."""
    console = Console()
    console.print()


app = typer.Typer(help="Manage task dependencies and critical paths")


@app.command()
def blocking(
    project_path: str = typer.Option(
        ".", help="Path to the Goal Kit project"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output format (text, json)"
    ),
) -> None:
    """Show tasks that are blocking other work.
    
    Displays tasks that:
    - Are not yet completed
    - Have other incomplete tasks depending on them
    """
    show_banner()
    console = Console()

    project_dir = Path(project_path)
    if not (project_dir / ".goalkit").exists():
        console.print("[red]Error:[/red] Not a Goal Kit project", style="bold")
        raise typer.Exit(1)

    try:
        tracker = TaskTracker(project_dir)
        dep_tracker = DependencyTracker(project_dir, tracker)

        blocking_tasks = dep_tracker.get_blocking_tasks()

        if output == "json":
            # JSON output
            all_tasks = tracker.get_all_tasks()
            task_map = {t.id: t for t in all_tasks}
            
            result = {
                "blocking_tasks": [
                    {
                        "id": task_id,
                        "title": task_map[task_id].title if task_id in task_map else "Unknown",
                        "dependent_count": len(dep_tracker.get_dependents(task_id)),
                    }
                    for task_id in blocking_tasks
                ]
            }
            console.print_json(data=result)
        else:
            # Text output
            if not blocking_tasks:
                console.print("[yellow]No blocking tasks[/yellow]")
            else:
                table = Table(title="Blocking Tasks", show_header=True, header_style="bold")
                table.add_column("Task ID", style="cyan")
                table.add_column("Title", style="green")
                table.add_column("Blocked Tasks", justify="right")

                all_tasks = tracker.get_all_tasks()
                task_map = {t.id: t for t in all_tasks}

                for task_id in blocking_tasks:
                    task = task_map.get(task_id)
                    if task:
                        dependents = dep_tracker.get_dependents(task_id)
                        table.add_row(
                            task_id[:8],
                            task.title,
                            str(len(dependents)),
                        )

                console.print(table)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)


@app.command()
def critical_path(
    project_path: str = typer.Option(
        ".", help="Path to the Goal Kit project"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output format (text, json)"
    ),
) -> None:
    """Show the critical path (longest dependency chain).
    
    Displays the tasks that must be completed sequentially and have the
    longest total duration. Completing these tasks determines the minimum
    project completion time.
    """
    show_banner()
    console = Console()

    project_dir = Path(project_path)
    if not (project_dir / ".goalkit").exists():
        console.print("[red]Error:[/red] Not a Goal Kit project", style="bold")
        raise typer.Exit(1)

    try:
        tracker = TaskTracker(project_dir)
        dep_tracker = DependencyTracker(project_dir, tracker)

        critical_path_tasks = dep_tracker.get_critical_path()

        if output == "json":
            # JSON output
            result = {
                "critical_path": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "status": t.status.value,
                        "estimated_hours": t.estimated_hours,
                    }
                    for t in critical_path_tasks
                ]
            }
            console.print_json(data=result)
        else:
            # Text output
            if not critical_path_tasks:
                console.print("[yellow]No critical path (no dependencies)[/yellow]")
            else:
                # Create tree visualization
                tree = Tree("[bold]Critical Path[/bold]")
                
                total_hours = sum(t.estimated_hours for t in critical_path_tasks)
                
                for i, task in enumerate(critical_path_tasks):
                    status_icon = "✓" if task.status.value == "completed" else "○"
                    task_node = tree.add(
                        f"{status_icon} {task.title} ({task.estimated_hours}h)"
                    )
                    if i < len(critical_path_tasks) - 1:
                        tree.add("↓")

                tree.label += f" [bold blue]Total: {total_hours}h[/bold blue]"
                console.print(tree)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)


@app.command()
def graph(
    project_path: str = typer.Option(
        ".", help="Path to the Goal Kit project"
    ),
    task_id: Optional[str] = typer.Option(
        None, "--task", "-t", help="Show only dependencies for this task"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output format (text, json)"
    ),
) -> None:
    """Show the dependency graph.
    
    Displays all task dependencies as a directed graph.
    """
    show_banner()
    console = Console()

    project_dir = Path(project_path)
    if not (project_dir / ".goalkit").exists():
        console.print("[red]Error:[/red] Not a Goal Kit project", style="bold")
        raise typer.Exit(1)

    try:
        tracker = TaskTracker(project_dir)
        dep_tracker = DependencyTracker(project_dir, tracker)

        if task_id:
            # Show dependencies for a specific task
            path = dep_tracker.get_path_for_task(task_id)
            
            if output == "json":
                result = {
                    "task_id": task_id,
                    "dependency_path": [
                        {"id": t.id, "title": t.title, "status": t.status.value}
                        for t in path
                    ]
                }
                console.print_json(data=result)
            else:
                if path:
                    tree = Tree(f"[bold]Dependencies for {path[-1].title}[/bold]")
                    for task in path[:-1]:
                        tree.add(f"{task.title} ({task.id[:8]})")
                    console.print(tree)
                else:
                    console.print(f"[yellow]Task {task_id} not found[/yellow]")
        else:
            # Show full graph
            graph_data = dep_tracker.get_dependency_graph()
            
            if output == "json":
                console.print_json(data=graph_data)
            else:
                # Text visualization
                all_tasks = tracker.get_all_tasks()
                task_map = {t.id: t for t in all_tasks}

                tasks_with_deps = [
                    task_id for task_id, deps in graph_data.items() if deps
                ]

                if not tasks_with_deps:
                    console.print("[yellow]No dependencies defined[/yellow]")
                else:
                    table = Table(
                        title="Dependency Graph", show_header=True, header_style="bold"
                    )
                    table.add_column("Task", style="cyan")
                    table.add_column("Depends On", style="green")

                    for task_id in tasks_with_deps:
                        task = task_map.get(task_id)
                        deps = graph_data[task_id]
                        
                        if task and deps:
                            dep_task = task_map.get(deps[0])
                            table.add_row(
                                task.title,
                                dep_task.title if dep_task else "Unknown",
                            )

                    console.print(table)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)


@app.command()
def add(
    task_id: str = typer.Argument(..., help="Task that will depend on another"),
    depends_on: str = typer.Argument(..., help="Task that must be completed first"),
    project_path: str = typer.Option(
        ".", help="Path to the Goal Kit project"
    ),
) -> None:
    """Add a dependency between tasks.
    
    Makes task_id depend on depends_on (i.e., depends_on must be completed
    before task_id can be started).
    """
    show_banner()
    console = Console()

    project_dir = Path(project_path)
    if not (project_dir / ".goalkit").exists():
        console.print("[red]Error:[/red] Not a Goal Kit project", style="bold")
        raise typer.Exit(1)

    try:
        tracker = TaskTracker(project_dir)
        dep_tracker = DependencyTracker(project_dir, tracker)

        result = dep_tracker.add_dependency(task_id, depends_on)

        if result:
            task = tracker.get_task(task_id)
            dep_task = tracker.get_task(depends_on)
            console.print(
                f"[green]✓[/green] {task.title} now depends on {dep_task.title}"
            )
        else:
            console.print(
                "[red]Error:[/red] Could not add dependency (may create cycle)",
                style="bold",
            )
            raise typer.Exit(1)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)


@app.command()
def remove(
    task_id: str = typer.Argument(..., help="Task to remove dependency from"),
    project_path: str = typer.Option(
        ".", help="Path to the Goal Kit project"
    ),
) -> None:
    """Remove a dependency from a task."""
    show_banner()
    console = Console()

    project_dir = Path(project_path)
    if not (project_dir / ".goalkit").exists():
        console.print("[red]Error:[/red] Not a Goal Kit project", style="bold")
        raise typer.Exit(1)

    try:
        tracker = TaskTracker(project_dir)
        dep_tracker = DependencyTracker(project_dir, tracker)

        result = dep_tracker.remove_dependency(task_id)

        if result:
            task = tracker.get_task(task_id)
            console.print(f"[green]✓[/green] Removed dependency from {task.title}")
        else:
            console.print(
                f"[yellow]⚠[/yellow] Task {task_id} not found or had no dependency"
            )

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        raise typer.Exit(1)
