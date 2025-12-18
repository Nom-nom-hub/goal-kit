"""
Helper functions for Goalkeeper CLI.

This module contains utility functions extracted from the main CLI module
to improve code organization and maintainability.
"""

import os
import sys
import subprocess
import json
import shutil
import zipfile
import tempfile
from pathlib import Path
from typing import Optional, Tuple, Any

import typer
import httpx
import readchar
import ssl
import truststore
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn

# ============================================================================
# UI & Input Helpers
# ============================================================================


class StepTracker:
    """Track and render hierarchical steps without emojis, similar to Claude Code tree output.
    Supports live auto-refresh via an attached refresh callback.
    """

    def __init__(self, title: str):
        self.title = title
        self.steps = []  # list of dicts: {key, label, status, detail}
        self.status_order = {"pending": 0, "running": 1, "done": 2, "error": 3, "skipped": 4}
        self._refresh_cb = None  # callable to trigger UI refresh

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append({"key": key, "label": label, "status": "pending", "detail": ""})
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return

        self.steps.append({"key": key, "label": key, "status": status, "detail": detail})
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            status = step["status"]
            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                # Entire line light gray (pending)
                if detail_text:
                    line = f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                # Label white, detail (if any) light gray in parentheses
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree


def get_key():
    """Get a single keypress in a cross-platform way using readchar."""
    key = readchar.readkey()

    if key == readchar.key.UP or key == readchar.key.CTRL_P:
        return "up"
    if key == readchar.key.DOWN or key == readchar.key.CTRL_N:
        return "down"

    if key == readchar.key.ENTER:
        return "enter"

    if key == readchar.key.ESC:
        return "escape"

    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key


def select_with_arrows(
    console: Console,
    options: dict,
    prompt_text: str = "Select an option",
    default_key: Optional[str] = None,
) -> str:
    """
    Interactive selection using arrow keys with Rich Live display.

    Args:
        console: Rich Console instance
        options: Dict with keys as option keys and values as descriptions
        prompt_text: Text to show above the options
        default_key: Default option key to start with

    Returns:
        Selected option key
    """
    option_keys = list(options.keys())
    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0

    selected_key = None

    def create_selection_panel():
        """Create the selection panel with current selection highlighted."""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")

        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
            else:
                table.add_row(" ", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")

        table.add_row("", "")
        table.add_row("", "[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]")

        return Panel(
            table,
            title=f"[bold]{prompt_text}[/bold]",
            border_style="cyan",
            padding=(1, 2),
        )

    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(
            create_selection_panel(), console=console, transient=True, auto_refresh=False
        ) as live:
            while True:
                try:
                    key = get_key()
                    if key == "up":
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == "down":
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == "enter":
                        selected_key = option_keys[selected_index]
                        break
                    elif key == "escape":
                        console.print("\n[yellow]Selection cancelled[/yellow]")
                        raise typer.Exit(1)

                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        console.print("\n[red]Selection failed.[/red]")
        raise typer.Exit(1)

    return selected_key


# ============================================================================
# JSON & File Helpers
# ============================================================================


def merge_json_files(existing_path: Path, new_content: dict, verbose: bool = False) -> dict:
    """Merge new JSON content into existing JSON file.

    Performs a deep merge where:
    - New keys are added
    - Existing keys are preserved unless overwritten by new content
    - Nested dictionaries are merged recursively
    - Lists and other values are replaced (not merged)

    Args:
        existing_path: Path to existing JSON file
        new_content: New JSON content to merge in
        verbose: Whether to print merge details

    Returns:
        Merged JSON content as dict
    """
    try:
        with open(existing_path, "r", encoding="utf-8") as f:
            existing_content = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is invalid, just use new content
        return new_content

    def deep_merge(base: dict, update: dict) -> dict:
        """Recursively merge update dict into base dict."""
        result = base.copy()
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                result[key] = deep_merge(result[key], value)
            else:
                # Add new key or replace existing value
                result[key] = value
        return result

    merged = deep_merge(existing_content, new_content)

    if verbose:
        console = Console()
        console.print(f"[cyan]Merged JSON file:[/cyan] {existing_path.name}")

    return merged


def handle_vscode_settings(
    console: Console, sub_item, dest_file, rel_path, verbose=False, tracker=None
) -> None:
    """Handle merging or copying of .vscode/settings.json files."""

    def log(message, color="green"):
        if verbose and not tracker:
            console.print(f"[{color}]{message}[/] {rel_path}")

    try:
        with open(sub_item, "r", encoding="utf-8") as f:
            new_settings = json.load(f)

        if dest_file.exists():
            merged = merge_json_files(dest_file, new_settings, verbose=verbose and not tracker)
            with open(dest_file, "w", encoding="utf-8") as f:
                json.dump(merged, f, indent=4)
                f.write("\n")
            log("Merged:", "green")
        else:
            shutil.copy2(sub_item, dest_file)
            log("Copied (no existing settings.json):", "blue")

    except Exception as e:
        log(f"Warning: Could not merge, copying instead: {e}", "yellow")
        shutil.copy2(sub_item, dest_file)


# ============================================================================
# Git Helpers
# ============================================================================


def is_git_repo(path: Optional[Path] = None) -> bool:
    """Check if the specified path is inside a git repository."""
    if path is None:
        path = Path.cwd()

    if not path.is_dir():
        return False

    try:
        # Use git command to check if inside a work tree
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def init_git_repo(
    console: Console, project_path: Path, quiet: bool = False
) -> Tuple[bool, Optional[str]]:
    """Initialize a git repository in the specified path.

    Args:
        console: Rich Console instance
        project_path: Path to initialize git repository in
        quiet: if True suppress console output (tracker handles status)

    Returns:
        Tuple of (success: bool, error_message: Optional[str])
    """
    try:
        original_cwd = Path.cwd()
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True, text=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Goalkeeper template"],
            check=True,
            capture_output=True,
            text=True,
        )
        if not quiet:
            console.print("[green]✓[/green] Git repository initialized")
        return True, None

    except subprocess.CalledProcessError as e:
        error_msg = f"Command: {' '.join(e.cmd)}\nExit code: {e.returncode}"
        if e.stderr:
            error_msg += f"\nError: {e.stderr.strip()}"
        elif e.stdout:
            error_msg += f"\nOutput: {e.stdout.strip()}"

        if not quiet:
            console.print(f"[red]Error initializing git repository:[/red] {e}")
        return False, error_msg
    finally:
        os.chdir(original_cwd)


# ============================================================================
# Tool Management Helpers
# ============================================================================


def check_tool(
    tool: str, claude_local_path: Path, tracker: Optional[StepTracker] = None
) -> bool:
    """Check if a tool is installed. Optionally update tracker.

    Args:
        tool: Name of the tool to check
        claude_local_path: Path to check for Claude CLI (special case)
        tracker: Optional StepTracker to update with results

    Returns:
        True if tool is found, False otherwise
    """
    # Special handling for Claude CLI after `claude migrate-installer`
    # The migrate-installer command REMOVES the original executable from PATH
    # and creates an alias at ~/.claude/local/claude instead
    # This path should be prioritized over other claude executables in PATH
    if tool == "claude":
        if claude_local_path.exists() and claude_local_path.is_file():
            if tracker:
                tracker.complete(tool, "available")
            return True

    found = shutil.which(tool) is not None

    if tracker:
        if found:
            tracker.complete(tool, "available")
        else:
            tracker.error(tool, "not found")

    return found


# ============================================================================
# Validation Helpers
# ============================================================================


def validate_project_name(project_name: str) -> Tuple[bool, Optional[str]]:
    """Validate a project name for safety and usability.
    
    Args:
        project_name: The proposed project name
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not project_name or not project_name.strip():
        return False, "Project name cannot be empty"
    
    # Check for invalid characters
    invalid_chars = set('<>:"|?*\\/')
    if any(char in project_name for char in invalid_chars):
        return False, f"Project name contains invalid characters: {', '.join(invalid_chars)}"
    
    # Check for reserved names (Windows)
    reserved_names = {'con', 'prn', 'aux', 'nul', 'com1', 'com2', 'lpt1', 'lpt2'}
    if project_name.lower() in reserved_names:
        return False, f"'{project_name}' is a reserved name on Windows"
    
    # Check length
    if len(project_name) > 255:
        return False, "Project name is too long (max 255 characters)"
    
    return True, None


def check_disk_space(path: Path, min_mb: int = 100) -> Tuple[bool, Optional[str]]:
    """Check if there's enough disk space at the given path.
    
    Args:
        path: Path to check disk space for
        min_mb: Minimum required space in MB
        
    Returns:
        Tuple of (has_space, error_message)
    """
    try:
        # Get the root of the path
        root = Path(path).anchor if os.name == 'nt' else '/'
        
        # Get disk usage
        if hasattr(os, 'statvfs'):  # Unix-like systems
            stat = os.statvfs(root)
            free_bytes = stat.f_bavail * stat.f_frsize
        else:  # Windows
            import shutil as sh
            _, _, free_bytes = sh.disk_usage(root)
        
        free_mb = free_bytes / (1024 * 1024)
        if free_mb < min_mb:
            return False, f"Insufficient disk space: {free_mb:.1f}MB available, {min_mb}MB required"
        
        return True, None
    except Exception as e:
        # Don't fail on disk space check - just warn
        return True, None


def is_goal_kit_project(project_path: Optional[Path] = None) -> bool:
    """Check if the specified path is a Goal Kit project.

    Args:
        project_path: Path to check. If None, uses current directory.

    Returns:
        True if the path is a Goal Kit project, False otherwise.
    """
    if project_path is None:
        project_path = Path.cwd()

    goalkit_dir = project_path / ".goalkit"
    return goalkit_dir.exists() and goalkit_dir.is_dir()


def load_project_context(project_path: Optional[Path] = None) -> Optional[dict]:
    """Load the current project context if in a Goal Kit project.

    Args:
        project_path: Path to check. If None, uses current directory.

    Returns:
        Dictionary with project context information, or None if not in a Goal Kit project.
    """
    if project_path is None:
        project_path = Path.cwd()

    if not is_goal_kit_project(project_path):
        return None

    try:
        from .analyzer import ProjectAnalyzer
        analyzer = ProjectAnalyzer(project_path)
        result = analyzer.analyze()

        # Create a simplified context representation
        context = {
            "is_goal_kit_project": True,
            "project_name": result.project.name,
            "project_path": str(result.project.path),
            "phase": result.phase,
            "health_score": result.health_score,
            "completion_percent": result.completion_percent,
            "total_goals": len(result.goals),
            "total_milestones": result.milestone_count,
            "completed_milestones": result.completed_milestones,
            "goals": [
                {
                    "id": goal.id,
                    "name": goal.name,
                    "phase": goal.phase,
                    "completion_percent": goal.completion_percent,
                    "has_metrics": goal.metrics_defined,
                    "success_criteria_count": goal.success_criteria_count
                }
                for goal in result.goals
            ]
        }
        return context
    except Exception:
        # If we can't load the context for any reason, return None
        # This could happen if project files are corrupted or missing
        return None


def check_path_writable(path: Path) -> Tuple[bool, Optional[str]]:
    """Check if a path is writable.

    Args:
        path: Path to check

    Returns:
        Tuple of (is_writable, error_message)
    """
    try:
        # Check if parent exists and is writable
        if path.exists():
            test_file = path / ".goalkit_write_test"
        else:
            parent = path.parent
            if not parent.exists():
                try:
                    parent.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    return False, f"Cannot create parent directory: {e}"
            test_file = parent / ".goalkit_write_test"

        # Try to write a test file
        try:
            test_file.write_text("test")
            test_file.unlink()
            return True, None
        except PermissionError:
            return False, f"Permission denied: cannot write to {test_file.parent}"
        except Exception as e:
            return False, f"Cannot write to path: {e}"
    except Exception as e:
        return False, f"Cannot check path writeability: {e}"
