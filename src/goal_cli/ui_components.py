#!/usr/bin/env python3
"""
UI components for the goal-dev-spec CLI with advanced features similar to spec-kit
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.table import Table
from rich.tree import Tree
from typer.core import TyperGroup

# For cross-platform keyboard input
try:
    import readchar
    READCHAR_AVAILABLE = True
except ImportError:
    READCHAR_AVAILABLE = False

console = Console()

# ASCII Art Banner
BANNER = """
███████╗ ██████╗  █████╗ ██╗     ██████╗ ███████╗██╗   ██╗
██╔════╝██╔═══██╗██╔══██╗██║     ██╔══██╗██╔════╝╚██╗ ██╔╝
█████╗  ██║   ██║███████║██║     ██║  ██║█████╗   ╚████╔╝
██╔══╝  ██║   ██║██╔══██║██║     ██║  ██║██╔══╝    ╚██╔╝
███████╗╚██████╔╝██║  ██║███████╗██████╔╝███████╗   ██║
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝   ╚═╝
 """

TAGLINE = "GoalDev - Goal-Driven Development Specification Toolkit"

# AI Choices (similar to spec-kit)
AI_CHOICES = {
    "claude": "Claude Code",
    "gemini": "Gemini CLI",
    "copilot": "GitHub Copilot",
    "cursor": "Cursor",
    "qwen": "Qwen Code",
    "opencode": "opencode",
    "codex": "Codex CLI",
    "windsurf": "Windsurf",
    "kilocode": "Kilo Code",
    "auggie": "Auggie CLI",
}

# Script Type Choices
SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh)", "ps": "PowerShell"}

__all__ = [
    "show_banner",
    "BannerGroup", 
    "StepTracker",
    "select_with_arrows",
    "AI_CHOICES",
    "SCRIPT_TYPE_CHOICES",
    "check_tool",
    "is_git_repo",
    "ensure_executable_scripts",
    "_github_token",
    "_github_auth_headers"
]

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
        if not key or not label:
            return  # Skip invalid inputs
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
        if not key or not status:
            return  # Skip invalid inputs
            
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return
        # If not present, add it
        self.steps.append({"key": key, "label": key, "status": status, "detail": detail})
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass  # Silently ignore refresh errors

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            # Circles (unchanged styling)
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

class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""
    
    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)

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

def get_key():
    """Get a single keypress in a cross-platform way using readchar."""
    if not READCHAR_AVAILABLE or not sys.stdin.isatty():
        # Fallback for non-TTY environments or when readchar is not available
        try:
            line = input("Enter selection (or press Enter for default): ")
            if line.strip() == "":
                return 'enter'
            return line
        except (EOFError, KeyboardInterrupt):
            return 'escape'
        
    try:
        key = readchar.readkey()
        
        # Arrow keys
        if key == readchar.key.UP:
            return 'up'
        if key == readchar.key.DOWN:
            return 'down'
        
        # Enter/Return
        if key == readchar.key.ENTER:
            return 'enter'
        
        # Escape
        if key == readchar.key.ESC:
            return 'escape'
            
        # Ctrl+C
        if key == readchar.key.CTRL_C:
            raise KeyboardInterrupt
            
        # For single character input, return the character
        if isinstance(key, str) and len(key) == 1:
            return key.lower()

        return key
    except Exception:
        # Fallback in case of any error
        return 'enter'

def select_with_arrows(options: dict, prompt_text: str = "Select an option", default_key: str = None) -> str:
    """
    Interactive selection using arrow keys with Rich Live display.
    
    Args:
        options: Dict with keys as option keys and values as descriptions
        prompt_text: Text to show above the options
        default_key: Default option key to start with
        
    Returns:
        Selected option key
    """
    if not options:
        raise ValueError("No options provided for selection")
    
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
            padding=(1, 2)
        )
    
    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        
        # Check if we can use interactive selection
        if not READCHAR_AVAILABLE or not sys.stdin.isatty():
            # Fallback to simple input selection
            console.print(f"[bold]{prompt_text}[/bold]")
            for i, key in enumerate(option_keys):
                console.print(f"  {i+1}. [cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
            
            while True:
                try:
                    choice = input(f"Enter choice (1-{len(option_keys)}, or key name): ").strip()
                    
                    # Check if it's a number
                    if choice.isdigit():
                        idx = int(choice) - 1
                        if 0 <= idx < len(option_keys):
                            selected_key = option_keys[idx]
                            break
                    # Check if it's a direct key match
                    elif choice in option_keys:
                        selected_key = choice
                        break
                    # Check if it's empty (default)
                    elif choice == "" and default_key:
                        selected_key = default_key
                        break
                    else:
                        console.print("[yellow]Invalid choice. Please try again.[/yellow]")
                        
                except (EOFError, KeyboardInterrupt):
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)
        else:
            # Use interactive selection with arrows
            with Live(create_selection_panel(), console=console, transient=True, auto_refresh=False) as live:
                while True:
                    try:
                        key = get_key()
                        
                        # Handle numeric input for direct selection
                        if isinstance(key, str) and key.isdigit():
                            idx = int(key) - 1
                            if 0 <= idx < len(option_keys):
                                selected_index = idx
                                selected_key = option_keys[selected_index]
                                break
                        
                        if key == 'up':
                            selected_index = (selected_index - 1) % len(option_keys)
                        elif key == 'down':
                            selected_index = (selected_index + 1) % len(option_keys)
                        elif key == 'enter':
                            selected_key = option_keys[selected_index]
                            break
                        elif key == 'escape':
                            console.print("\n[yellow]Selection cancelled[/yellow]")
                            raise typer.Exit(1)
                        elif isinstance(key, str) and key in option_keys:
                            # Direct key selection
                            selected_key = key
                            break
                        
                        live.update(create_selection_panel(), refresh=True)

                    except KeyboardInterrupt:
                        console.print("\n[yellow]Selection cancelled[/yellow]")
                        raise typer.Exit(1)
                    except Exception as e:
                        console.print(f"\n[yellow]Selection error: {e}. Using default selection.[/yellow]")
                        if default_key and default_key in option_keys:
                            selected_key = default_key
                            break
                        else:
                            selected_key = option_keys[0]
                            break

    run_selection_loop()

    if selected_key is None:
        console.print("\n[red]Selection failed. Using default.[/red]")
        if default_key and default_key in option_keys:
            selected_key = default_key
        else:
            selected_key = option_keys[0]

    # Show the selection to the user
    console.print(f"[green]Selected:[/green] {selected_key} ({options[selected_key]})")
    return selected_key


def get_user_input(prompt: str, default: str = None, validator=None) -> str:
    """
    Get user input with optional validation and default value.
    
    Args:
        prompt: The prompt to display to the user
        default: Default value if user doesn't provide input
        validator: Function to validate input, should raise ValueError for invalid input
        
    Returns:
        Validated user input
    """
    while True:
        try:
            if default:
                user_input = input(f"{prompt} [{default}]: ").strip()
                if not user_input:
                    user_input = default
            else:
                user_input = input(f"{prompt}: ").strip()
            
            # Validate input if validator provided
            if validator:
                try:
                    validator(user_input)
                    return user_input
                except ValueError as e:
                    console.print(f"[red]Invalid input:[/red] {e}")
                    continue
            
            return user_input
        except (EOFError, KeyboardInterrupt):
            console.print("\n[yellow]Input cancelled[/yellow]")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Error reading input:[/red] {e}")
            raise typer.Exit(1)


def validate_project_name(name: str):
    """
    Validate project name - must be non-empty and contain only valid characters.
    
    Args:
        name: Project name to validate
        
    Raises:
        ValueError: If the name is invalid
    """
    if not name:
        raise ValueError("Project name cannot be empty")
    
    # Check for valid characters (alphanumeric, hyphens, underscores)
    import re
    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        raise ValueError("Project name can only contain letters, numbers, hyphens, and underscores")
    
    # Check for reserved names
    reserved_names = [".", "..", "con", "prn", "aux", "nul"] + [f"com{i}" for i in range(1, 10)] + [f"lpt{i}" for i in range(1, 10)]
    if name.lower() in reserved_names:
        raise ValueError(f"'{name}' is a reserved name and cannot be used")


def validate_ai_assistant(ai: str, ai_choices: dict):
    """
    Validate AI assistant selection.
    
    Args:
        ai: AI assistant name to validate
        ai_choices: Dictionary of valid AI choices
        
    Raises:
        ValueError: If the AI assistant is invalid
    """
    if ai not in ai_choices:
        raise ValueError(f"Invalid AI assistant '{ai}'. Choose from: {', '.join(ai_choices.keys())}")

def check_tool(tool: str) -> bool:
    """Check if a tool is installed."""
    if shutil.which(tool):
        return True
    else:
        return False

def is_git_repo(path: Path = None) -> bool:
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


def _github_token(cli_token: str | None = None) -> str | None:
    """Return sanitized GitHub token (cli arg takes precedence) or None."""
    import os
    return ((cli_token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()) or None


def _github_auth_headers(cli_token: str | None = None) -> dict:
    """Return Authorization header dict only when a non-empty token exists."""
    token = _github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}


def ensure_executable_scripts(project_path: Path, tracker: StepTracker | None = None) -> None:
    """Ensure POSIX .sh scripts under scripts/bash (recursively) have execute bits (no-op on Windows)."""
    if os.name == "nt":
        return  # Windows: skip silently
    scripts_root = project_path / "scripts" / "bash"
    if not scripts_root.is_dir():
        return
    failures: list[str] = []
    updated = 0
    for script in scripts_root.rglob("*.sh"):
        try:
            if script.is_symlink() or not script.is_file():
                continue
            try:
                with script.open("rb") as f:
                    if f.read(2) != b"#!":
                        continue
            except Exception:
                continue
            st = script.stat()
            mode = st.st_mode
            if mode & 0o111:
                continue
            new_mode = mode
            if mode & 0o400:
                new_mode |= 0o100
            if mode & 0o040:
                new_mode |= 0o010
            if mode & 0o004:
                new_mode |= 0o001
            if not (new_mode & 0o100):
                new_mode |= 0o100
            os.chmod(script, new_mode)
            updated += 1
        except Exception as e:
            failures.append(f"{script.relative_to(scripts_root)}: {e}")
    if tracker:
        detail = f"{updated} updated" + (f", {len(failures)} failed" if failures else "")
        tracker.add("chmod", "Set script permissions recursively")
        (tracker.error if failures else tracker.complete)("chmod", detail)
    else:
        if updated:
            console.print(f"[cyan]Updated execute permissions on {updated} script(s) recursively[/cyan]")
        if failures:
            console.print("[yellow]Some scripts could not be updated:[/yellow]")
            for f in failures:
                console.print(f"  - {f}")