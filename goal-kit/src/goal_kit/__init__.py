#!/usr/bin/env python3
"""
Goal-Kit CLI - Goal-Driven Development Toolkit

Usage:
    uvx goal-kit init <goal-name>
    uvx goal-kit define "Build a web application"
    uvx goal-kit milestone
    uvx goal-kit achieve

Or install globally:
    uv tool install --from goal-kit
    goal-kit init <goal-name>
    goal-kit define "Build a web application"
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from typer.core import TyperGroup

# Constants
BANNER = """
 ██████╗  ██████╗ ███████╗ ██████╗ ██╗   ██╗██╗██╗     ██████╗
██╔════╝ ██╔═══██╗██╔════╝██╔═══██╗██║   ██║██║██║     ██╔══██╗
██║  ███╗██║   ██║█████╗  ██║   ██║██║   ██║██║██║     ██║  ██║
██║   ██║██║   ██║██╔══╝  ██║   ██║╚██╗ ██╔╝██║██║     ██║  ██║
╚██████╔╝╚██████╔╝██║     ╚██████╔╝ ╚████╔╝ ██║███████╗██████╔╝
 ╚═════╝  ╚═════╝ ╚═╝      ╚═════╝   ╚═══╝  ╚═╝╚══════╝╚═════╝
"""

TAGLINE = "Goal-Driven Development Toolkit - Transform Ideas into Achievements"

console = Console()


class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""

    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="goal-kit",
    help="Goal-Driven Development Toolkit for transforming ideas into achievements",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)


def show_banner():
    """Display the ASCII art banner."""
    # Create gradient effect with different colors
    banner_lines = BANNER.strip().split('\n')
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)

    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()


@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided."""
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center("[dim]Run 'goal-kit --help' for usage information[/dim]"))
        console.print()


def get_goal_directory(goal_name: str = None) -> Path:
    """Get the goal directory path."""
    if goal_name:
        return Path.cwd() / goal_name
    else:
        # Try to find existing goal directory in current directory
        goal_dirs = [d for d in Path.cwd().iterdir() if d.is_dir() and (d / "goal.json").exists()]
        if goal_dirs:
            return goal_dirs[0]
        else:
            # Create a default goal directory
            return Path.cwd() / "goal_project"


def load_goal_data(goal_path: Path) -> Dict[str, Any]:
    """Load goal data from goal.json file."""
    goal_file = goal_path / "goal.json"
    if goal_file.exists():
        with open(goal_file, 'r') as f:
            return json.load(f)
    return {}


def save_goal_data(goal_path: Path, data: Dict[str, Any]) -> None:
    """Save goal data to goal.json file."""
    goal_file = goal_path / "goal.json"
    with open(goal_file, 'w') as f:
        json.dump(data, f, indent=2)


@app.command()
def init(
    goal_name: str = typer.Argument(None, help="Name for your new goal project"),
    here: bool = typer.Option(False, "--here", help="Initialize goal project in the current directory"),
    force: bool = typer.Option(False, "--force", help="Force overwrite when using --here"),
):
    """
    Initialize a new goal project.

    This command will:
    1. Create a new goal project directory (or use current directory with --here)
    2. Set up the basic goal structure with goal.json
    3. Create milestone and achievement tracking directories
    4. Initialize progress tracking

    Examples:
        goal-kit init "Build a web application"
        goal-kit init my-goal-project
        goal-kit init --here
        goal-kit init --here --force
    """
    show_banner()

    if here and goal_name:
        console.print("[red]Error:[/red] Cannot specify both goal name and --here flag")
        raise typer.Exit(1)

    if not here and not goal_name:
        console.print("[red]Error:[/red] Must specify either a goal name or use --here flag")
        raise typer.Exit(1)

    # Determine goal directory
    if here:
        goal_path = Path.cwd()
        goal_display_name = Path.cwd().name

        # Check if current directory has any files
        existing_items = list(goal_path.iterdir())
        if existing_items:
            console.print(f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)")
            console.print("[yellow]Goal files will be merged with existing content[/yellow]")
            if force:
                console.print("[cyan]--force supplied: skipping confirmation and proceeding[/cyan]")
            else:
                response = typer.confirm("Do you want to continue?")
                if not response:
                    console.print("[yellow]Operation cancelled[/yellow]")
                    raise typer.Exit(0)
    else:
        goal_path = Path(goal_name).resolve()
        goal_display_name = goal_name

        # Check if goal directory already exists
        if goal_path.exists():
            error_panel = Panel(
                f"Directory '[cyan]{goal_name}[/cyan]' already exists\n"
                "Please choose a different goal name or remove the existing directory.",
                title="[red]Directory Conflict[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    # Create formatted setup info
    current_dir = Path.cwd()

    setup_lines = [
        "[cyan]Goal-Kit Project Setup[/cyan]",
        "",
        f"{'Goal Project':<15} [green]{goal_display_name}[/green]",
        f"{'Working Path':<15} [dim]{current_dir}[/dim]",
    ]

    if not here:
        setup_lines.append(f"{'Target Path':<15} [dim]{goal_path}[/dim]")

    console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))

    # Create goal directory if not using current directory
    if not here:
        goal_path.mkdir(parents=True)

    # Create basic directory structure
    milestones_dir = goal_path / "milestones"
    achievements_dir = goal_path / "achievements"
    templates_dir = goal_path / "templates"

    milestones_dir.mkdir(exist_ok=True)
    achievements_dir.mkdir(exist_ok=True)
    templates_dir.mkdir(exist_ok=True)

    # Create goal.json configuration
    goal_data = {
        "name": goal_display_name,
        "description": "",
        "created_at": datetime.now().isoformat(),
        "status": "defined",
        "progress": 0,
        "milestones": [],
        "achievements": [],
        "metadata": {}
    }

    save_goal_data(goal_path, goal_data)

    # Create milestone tracking file
    milestones_file = milestones_dir / "README.md"
    milestones_file.write_text("# Milestones\n\nThis directory contains your goal milestones.\n")

    # Create achievement tracking file
    achievements_file = achievements_dir / "README.md"
    achievements_file.write_text("# Achievements\n\nThis directory contains your goal achievements.\n")

    console.print("\n[bold green]Goal project initialized successfully![/bold green]")

    # Next steps
    steps_lines = []
    if not here:
        steps_lines.append(f"1. Go to the goal project folder: [cyan]cd {goal_name}[/cyan]")
        step_num = 2
    else:
        steps_lines.append("1. You're already in the goal project directory!")
        step_num = 2

    steps_lines.append(f"{step_num}. Define your goal: [cyan]goal-kit define \"Your goal description\"[/cyan]")
    steps_lines.append(f"{step_num + 1}. Create milestones: [cyan]goal-kit milestone[/cyan]")
    steps_lines.append(f"{step_num + 2}. Track progress: [cyan]goal-kit progress[/cyan]")

    steps_panel = Panel("\n".join(steps_lines), title="Next Steps", border_style="cyan", padding=(1, 2))
    console.print()
    console.print(steps_panel)


@app.command()
def define(
    description: str = typer.Argument(..., help="Natural language description of your goal"),
    priority: str = typer.Option("medium", "--priority", help="Goal priority: low, medium, high, critical"),
    deadline: str = typer.Option(None, "--deadline", help="Goal deadline in YYYY-MM-DD format"),
    category: str = typer.Option(None, "--category", help="Goal category for organization"),
):
    """
    Define a goal with natural language description.

    This command will:
    1. Parse the natural language description
    2. Create a structured goal definition
    3. Set goal metadata (priority, deadline, category)
    4. Update the goal.json configuration

    Examples:
        goal-kit define "Build a web application with user authentication"
        goal-kit define "Learn Python machine learning" --priority high
        goal-kit define "Launch startup MVP" --deadline 2024-12-31 --priority critical
        goal-kit define "Write a book" --category "writing" --priority medium
    """
    show_banner()

    goal_path = get_goal_directory()
    goal_data = load_goal_data(goal_path)

    if not goal_data:
        console.print("[red]Error:[/red] No goal project found. Run 'goal-kit init' first.")
        raise typer.Exit(1)

    # Validate priority
    valid_priorities = ["low", "medium", "high", "critical"]
    if priority not in valid_priorities:
        console.print(f"[red]Error:[/red] Invalid priority '{priority}'. Choose from: {', '.join(valid_priorities)}")
        raise typer.Exit(1)

    # Validate and parse deadline
    deadline_date = None
    if deadline:
        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Error:[/red] Invalid deadline format. Use YYYY-MM-DD format (e.g., 2024-12-31)")
            raise typer.Exit(1)

    # Update goal data
    goal_data["description"] = description
    goal_data["priority"] = priority
    goal_data["category"] = category or "general"

    if deadline_date:
        goal_data["deadline"] = deadline_date.isoformat()

    goal_data["status"] = "defined"
    goal_data["defined_at"] = datetime.now().isoformat()

    # Save updated goal data
    save_goal_data(goal_path, goal_data)

    # Display goal definition
    console.print("\n[bold green]Goal defined successfully![/bold green]")

    goal_panel = Panel(
        f"[bold]{goal_data['name']}[/bold]\n\n{description}",
        title="Goal Definition",
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(goal_panel)

    # Show goal metadata
    metadata_table = Table(title="Goal Metadata")
    metadata_table.add_column("Property", style="cyan")
    metadata_table.add_column("Value", style="white")

    metadata_table.add_row("Priority", priority)
    metadata_table.add_row("Category", goal_data["category"])
    if deadline_date:
        metadata_table.add_row("Deadline", deadline_date.strftime("%Y-%m-%d"))
    metadata_table.add_row("Status", "Defined")
    metadata_table.add_row("Created", datetime.fromisoformat(goal_data["created_at"]).strftime("%Y-%m-%d %H:%M"))

    console.print(metadata_table)

    console.print("\n[dim]Next steps:[/dim]")
    console.print("• Run [cyan]goal-kit milestone[/cyan] to plan your milestones")
    console.print("• Run [cyan]goal-kit progress[/cyan] to track your progress")


@app.command()
def milestone(
    name: str = typer.Option(None, "--name", help="Milestone name"),
    description: str = typer.Option(None, "--desc", help="Milestone description"),
    add: bool = typer.Option(False, "--add", help="Add a new milestone interactively"),
    list: bool = typer.Option(False, "--list", help="List all milestones"),
):
    """
    Manage goal milestones.

    This command provides milestone planning and management capabilities:
    1. Interactive milestone creation
    2. Milestone listing and tracking
    3. Milestone progress updates

    Examples:
        goal-kit milestone --add
        goal-kit milestone --list
        goal-kit milestone --name "Setup project structure" --desc "Create basic directory structure"
    """
    show_banner()

    goal_path = get_goal_directory()
    goal_data = load_goal_data(goal_path)

    if not goal_data:
        console.print("[red]Error:[/red] No goal project found. Run 'goal-kit init' first.")
        raise typer.Exit(1)

    milestones_dir = goal_path / "milestones"

    if list:
        # List all milestones
        console.print(f"\n[bold cyan]Milestones for: {goal_data['name']}[/bold cyan]")

        if not goal_data.get("milestones"):
            console.print("[yellow]No milestones defined yet.[/yellow]")
            console.print("Run [cyan]goal-kit milestone --add[/cyan] to create your first milestone.")
            return

        milestone_table = Table(title="Project Milestones")
        milestone_table.add_column("ID", style="cyan", width=3)
        milestone_table.add_column("Name", style="white")
        milestone_table.add_column("Status", style="green")
        milestone_table.add_column("Description", style="dim")

        for i, milestone in enumerate(goal_data["milestones"], 1):
            status = milestone.get("status", "pending")
            status_display = {
                "pending": "[yellow]Pending[/yellow]",
                "in_progress": "[cyan]In Progress[/cyan]",
                "completed": "[green]Completed[/green]",
                "cancelled": "[red]Cancelled[/red]"
            }.get(status, status)

            milestone_table.add_row(
                str(i),
                milestone["name"],
                status_display,
                milestone.get("description", "")
            )

        console.print(milestone_table)

    elif add or name:
        # Add new milestone
        if not name:
            console.print("\n[bold]Create New Milestone[/bold]")
            name = typer.prompt("Milestone name")
            description = typer.prompt("Description (optional)", default="")

        # Create milestone data
        milestone_data = {
            "id": len(goal_data.get("milestones", [])) + 1,
            "name": name,
            "description": description,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "achievements": []
        }

        # Add to goal data
        if "milestones" not in goal_data:
            goal_data["milestones"] = []

        goal_data["milestones"].append(milestone_data)
        save_goal_data(goal_path, goal_data)

        # Create milestone file
        milestone_file = milestones_dir / f"{milestone_data['id']:02d}-{name.lower().replace(' ', '-')}.md"
        milestone_content = f"""# {name}

**Status:** Pending
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Description
{description}

## Achievements
- [ ] Milestone defined

## Notes
"""

        milestone_file.write_text(milestone_content)

        console.print(f"\n[green]✓[/green] Milestone '{name}' created successfully!")
        console.print(f"[dim]Milestone file:[/dim] {milestone_file}")

    else:
        # Show help
        console.print("[cyan]Usage examples:[/cyan]")
        console.print("  goal-kit milestone --add")
        console.print("  goal-kit milestone --list")
        console.print("  goal-kit milestone --name 'Setup project' --desc 'Initial setup'")


@app.command()
def progress():
    """
    Show goal progress dashboard.

    This command displays:
    1. Overall goal progress
    2. Milestone completion status
    3. Achievement tracking
    4. Progress metrics and insights
    """
    show_banner()

    goal_path = get_goal_directory()
    goal_data = load_goal_data(goal_path)

    if not goal_data:
        console.print("[red]Error:[/red] No goal project found. Run 'goal-kit init' first.")
        raise typer.Exit(1)

    console.print(f"\n[bold cyan]Progress Dashboard: {goal_data['name']}[/bold cyan]")

    # Goal overview
    status_color = {
        "defined": "blue",
        "in_progress": "cyan",
        "completed": "green",
        "on_hold": "yellow",
        "cancelled": "red"
    }.get(goal_data.get("status", "defined"), "white")

    overview_table = Table(title="Goal Overview")
    overview_table.add_column("Property", style="cyan")
    overview_table.add_column("Value", style="white")

    overview_table.add_row("Status", f"[{status_color}]{goal_data.get('status', 'unknown').title()}[/{status_color}]")
    overview_table.add_row("Progress", f"{goal_data.get('progress', 0)}%")
    overview_table.add_row("Created", datetime.fromisoformat(goal_data["created_at"]).strftime("%Y-%m-%d %H:%M"))

    if goal_data.get("defined_at"):
        overview_table.add_row("Defined", datetime.fromisoformat(goal_data["defined_at"]).strftime("%Y-%m-%d %H:%M"))

    console.print(overview_table)

    # Milestones progress
    milestones = goal_data.get("milestones", [])
    if milestones:
        completed_milestones = sum(1 for m in milestones if m.get("status") == "completed")
        total_milestones = len(milestones)
        milestone_progress = (completed_milestones / total_milestones) * 100 if total_milestones > 0 else 0

        progress_table = Table(title="Milestone Progress")
        progress_table.add_column("Metric", style="cyan")
        progress_table.add_column("Value", style="white")

        progress_table.add_row("Total Milestones", str(total_milestones))
        progress_table.add_row("Completed", f"{completed_milestones} ({milestone_progress:.1f}%)")

        console.print(progress_table)

        # List milestones
        milestone_table = Table(title="Milestones")
        milestone_table.add_column("Name", style="white")
        milestone_table.add_column("Status", style="green")
        milestone_table.add_column("Description", style="dim")

        for milestone in milestones:
            status = milestone.get("status", "pending")
            status_display = {
                "pending": "[yellow]Pending[/yellow]",
                "in_progress": "[cyan]In Progress[/cyan]",
                "completed": "[green]Completed[/green]",
                "cancelled": "[red]Cancelled[/red]"
            }.get(status, status)

            milestone_table.add_row(
                milestone["name"],
                status_display,
                milestone.get("description", "")
            )

        console.print(milestone_table)

    console.print("\n[dim]Next steps:[/dim]")
    console.print("• Run [cyan]goal-kit milestone --add[/cyan] to add more milestones")
    console.print("• Run [cyan]goal-kit achieve[/cyan] to track achievements")


@app.command()
def achieve(
    milestone_id: int = typer.Option(None, "--milestone", help="Milestone ID to add achievement to"),
    description: str = typer.Option(None, "--desc", help="Achievement description"),
    add: bool = typer.Option(False, "--add", help="Add a new achievement interactively"),
):
    """
    Track goal achievements.

    This command helps you:
    1. Add new achievements to milestones
    2. Track completed work
    3. Update progress metrics

    Examples:
        goal-kit achieve --add
        goal-kit achieve --milestone 1 --desc "Completed user authentication"
    """
    show_banner()

    goal_path = get_goal_directory()
    goal_data = load_goal_data(goal_path)

    if not goal_data:
        console.print("[red]Error:[/red] No goal project found. Run 'goal-kit init' first.")
        raise typer.Exit(1)

    achievements_dir = goal_path / "achievements"

    if add or (milestone_id and description):
        if not milestone_id:
            milestones = goal_data.get("milestones", [])
            if not milestones:
                console.print("[red]Error:[/red] No milestones found. Create milestones first with 'goal-kit milestone --add'")
                raise typer.Exit(1)

            console.print("\n[bold]Select Milestone[/bold]")
            for i, milestone in enumerate(milestones, 1):
                console.print(f"{i}. {milestone['name']}")

            milestone_id = typer.prompt("Milestone number", type=int)

            if milestone_id < 1 or milestone_id > len(milestones):
                console.print(f"[red]Error:[/red] Invalid milestone number. Choose 1-{len(milestones)}")
                raise typer.Exit(1)

        if not description:
            description = typer.prompt("Achievement description")

        # Get the milestone
        milestone = goal_data["milestones"][milestone_id - 1]

        # Create achievement data
        achievement_data = {
            "id": len(milestone.get("achievements", [])) + 1,
            "description": description,
            "completed_at": datetime.now().isoformat(),
            "milestone_id": milestone_id
        }

        # Add to milestone
        if "achievements" not in milestone:
            milestone["achievements"] = []

        milestone["achievements"].append(achievement_data)

        # Add to global achievements
        if "achievements" not in goal_data:
            goal_data["achievements"] = []

        goal_data["achievements"].append(achievement_data)

        # Save updated goal data
        save_goal_data(goal_path, goal_data)

        # Create achievement file
        achievement_file = achievements_dir / f"achievement-{achievement_data['id']:03d}.md"
        achievement_content = f"""# Achievement: {description}

**Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Milestone:** {milestone['name']}

## Details
This achievement contributes to the milestone: "{milestone['name']}"

## Impact
- Progress towards goal completion
- Milestone advancement
"""

        achievement_file.write_text(achievement_content)

        console.print(f"\n[green]✓[/green] Achievement '{description}' recorded successfully!")
        console.print(f"[dim]Achievement file:[/dim] {achievement_file}")

        # Update milestone status if all achievements are complete
        total_achievements = len(milestone.get("achievements", []))
        if total_achievements > 0:
            milestone["status"] = "completed"

        save_goal_data(goal_path, goal_data)

    else:
        # Show achievements
        achievements = goal_data.get("achievements", [])
        if not achievements:
            console.print("[yellow]No achievements recorded yet.[/yellow]")
            console.print("Run [cyan]goal-kit achieve --add[/cyan] to record your first achievement.")
            return

        console.print(f"\n[bold cyan]Achievements for: {goal_data['name']}[/bold cyan]")

        achievement_table = Table(title="Goal Achievements")
        achievement_table.add_column("ID", style="cyan", width=3)
        achievement_table.add_column("Description", style="white")
        achievement_table.add_column("Milestone", style="green")
        achievement_table.add_column("Completed", style="dim")

        for achievement in achievements:
            milestone_name = "Unknown"
            for milestone in goal_data.get("milestones", []):
                if milestone["id"] == achievement.get("milestone_id"):
                    milestone_name = milestone["name"]
                    break

            completed_date = datetime.fromisoformat(achievement["completed_at"]).strftime("%Y-%m-%d %H:%M")

            achievement_table.add_row(
                str(achievement["id"]),
                achievement["description"],
                milestone_name,
                completed_date
            )

        console.print(achievement_table)


@app.command()
def complete():
    """
    Mark goal as completed.

    This command will:
    1. Validate all milestones are completed
    2. Update goal status to completed
    3. Generate completion summary
    4. Create completion report
    """
    show_banner()

    goal_path = get_goal_directory()
    goal_data = load_goal_data(goal_path)

    if not goal_data:
        console.print("[red]Error:[/red] No goal project found. Run 'goal-kit init' first.")
        raise typer.Exit(1)

    milestones = goal_data.get("milestones", [])
    achievements = goal_data.get("achievements", [])

    if not milestones:
        console.print("[yellow]No milestones defined. Define milestones first with 'goal-kit milestone --add'[/yellow]")
        return

    # Check completion status
    completed_milestones = sum(1 for m in milestones if m.get("status") == "completed")
    total_milestones = len(milestones)

    if completed_milestones < total_milestones:
        console.print(f"[yellow]Goal not ready for completion.[/yellow]")
        console.print(f"Completed: {completed_milestones}/{total_milestones} milestones")

        if typer.confirm("Mark as completed anyway?"):
            pass  # Continue with completion
        else:
            return

    # Update goal status
    goal_data["status"] = "completed"
    goal_data["completed_at"] = datetime.now().isoformat()
    goal_data["final_progress"] = 100

    # Calculate total achievements
    total_achievements = len(achievements)

    save_goal_data(goal_path, goal_data)

    # Create completion report
    completion_report = goal_path / "completion-report.md"
    report_content = f"""# Goal Completion Report

## Goal Summary
**Goal:** {goal_data['name']}
**Description:** {goal_data.get('description', 'No description provided')}
**Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Statistics
- **Total Milestones:** {total_milestones}
- **Completed Milestones:** {completed_milestones}
- **Total Achievements:** {total_achievements}
- **Completion Rate:** {completed_milestones/total_milestones*100:.1f}%

## Journey Timeline
- **Started:** {datetime.fromisoformat(goal_data['created_at']).strftime('%Y-%m-%d %H:%M')}
- **Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Achievements Summary
{chr(10).join(f"- {a['description']}" for a in achievements[:10])}
{'' if len(achievements) <= 10 else f'... and {len(achievements) - 10} more achievements'}

---
*Congratulations on completing your goal! This report has been generated by Goal-Kit.*
"""

    completion_report.write_text(report_content)

    # Display completion summary
    console.print("\n[bold green]🎉 Goal Completed Successfully! 🎉[/bold green]")

    completion_panel = Panel(
        f"[bold]{goal_data['name']}[/bold] has been marked as completed!\n\n"
        f"📊 {completed_milestones}/{total_milestones} milestones completed\n"
        f"🏆 {total_achievements} achievements recorded\n\n"
        f"📄 Report saved to: {completion_report.name}",
        title="Completion Summary",
        border_style="green",
        padding=(1, 2)
    )
    console.print(completion_panel)

    console.print("\n[dim]You can now:[/dim]")
    console.print("• Start a new goal with [cyan]goal-kit init[/cyan]")
    console.print("• Review your journey in the completion report")
    console.print("• Share your success with others!")


def main():
    app()


if __name__ == "__main__":
    main()