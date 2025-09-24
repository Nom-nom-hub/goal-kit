#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "rich",
#     "platformdirs",
#     "readchar",
#     "httpx",
#     "pyyaml",
# ]
# ///
"""
Goal CLI - Complete Goal-Driven Development Toolkit

A comprehensive CLI for goal-driven software development workflow:
- Define project goals and objectives
- Clarify and validate goals
- Create implementation strategies
- Generate technical plans
- Create actionable tasks
- Establish project constitution
- Analyze project alignment
- Execute implementation

Core Commands:
    goal goals        Define project objectives
    goal clarify      Clarify and validate goals
    goal strategize   Develop implementation strategies
    goal plan         Create technical implementation plans
    goal tasks        Generate actionable tasks
    goal constitution Establish project principles
    goal analyze      Validate alignment & surface inconsistencies
    goal implement    Execute implementation
    goal init         Initialize new project (legacy)
    goal check        Check available tools

Usage:
    uvx goal-cli.py goals --project my-app
    uvx goal-cli.py strategize --goals goals.md
    uvx goal-cli.py plan --strategy strategy.md
    uvx goal-cli.py tasks --plan plan.md
    uvx goal-cli.py implement --tasks tasks.md

Or install globally:
    uv tool install --from goal-cli.py goal-cli
    goal goals --project my-app
    goal strategize --goals goals.md
    goal implement --tasks tasks.md
"""

import os
import subprocess
import sys
import zipfile
import tempfile
import shutil
import shlex
import json
from pathlib import Path
from typing import Optional, Tuple

import typer
import httpx
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.table import Table
from rich.tree import Tree
from typer.core import TyperGroup

# For cross-platform keyboard input
import readchar
import ssl
import truststore

ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = httpx.Client(verify=ssl_context)

def _github_token(cli_token: str | None = None) -> str | None:
    """Return sanitized GitHub token (cli arg takes precedence) or None."""
    return ((cli_token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()) or None

def _github_auth_headers(cli_token: str | None = None) -> dict:
    """Return Authorization header dict only when a non-empty token exists."""
    token = _github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}

# Constants
AI_CHOICES = {
    "copilot": "GitHub Copilot",
    "claude": "Claude Code",
    "gemini": "Gemini CLI",
    "cursor": "Cursor",
    "qwen": "Qwen Code",
    "opencode": "opencode",
    "codex": "Codex CLI",
    "windsurf": "Windsurf",
    "kilocode": "Kilo Code",
    "auggie": "Auggie CLI",
    "roo": "Roo Code",
    "deepseek": "DeepSeek Coder",
    "tabnine": "Tabnine AI",
    "grok": "Grok xAI",
    "codewhisperer": "CodeWhisperer",
}

# Add script type choices
SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh)", "ps": "PowerShell"}

# ASCII Art Banner
BANNER = """
 #####
#     #  ####    ##   #      # ###### #   #
#       #    #  #  #  #      # #       # #
#  #### #    # #    # #      # #####    #
#     # #    # ###### #      # #        #
#     # #    # #    # #      # #        #
 #####   ####  #    # ###### # #        #
"""

TAGLINE = "Goal-Driven Development Toolkit - Build with Purpose"

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
        # If not present, add it
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

            # Status indicators
            status = step["status"]
            if status == "done":
                symbol = "[green]✓[/green]"
            elif status == "pending":
                symbol = "[dim]○[/dim]"
            elif status == "running":
                symbol = "[cyan]→[/cyan]"
            elif status == "error":
                symbol = "[red]✗[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                # Entire line dimmed (pending)
                if detail_text:
                    line = f"{symbol} [dim]{label} ({detail_text})[/dim]"
                else:
                    line = f"{symbol} [dim]{label}[/dim]"
            else:
                # Label normal, detail (if any) dimmed in parentheses
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [dim]({detail_text})[/dim]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree

MINI_BANNER = """
╔═╗╔═╗╔═╗╔═╗╦╔═╗╦ ╦
╚═╗╠═╝║╣ ║  ║╠╣ ╚╦╝
╚═╝╩  ╚═╝╚═╝╩╚   ╩
"""

def get_key():
    """Get a single keypress in a cross-platform way using readchar."""
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

    return key

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
        with Live(create_selection_panel(), console=console, transient=True, auto_refresh=False) as live:
            while True:
                try:
                    key = get_key()
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

                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        console.print("\n[red]Selection failed.[/red]")
        raise typer.Exit(1)

    return selected_key

console = Console()

class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""

    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)

app = typer.Typer(
    name="goal",
    help="Goal-Driven Development Toolkit - Complete workflow from goals to implementation",
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
    # Show banner only when no subcommand and no help flag
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center("[dim]Run 'goal --help' for usage information[/dim]"))
        console.print()

def run_command(cmd: list[str], check_return: bool = True, capture: bool = False, shell: bool = False) -> Optional[str]:
    """Run a shell command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(cmd, check=check_return, capture_output=True, text=True, shell=shell)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]Error running command:[/red] {' '.join(cmd)}")
            console.print(f"[red]Exit code:[/red] {e.returncode}")
            if hasattr(e, 'stderr') and e.stderr:
                console.print(f"[red]Error output:[/red] {e.stderr}")
            raise
        return None

def check_tool_for_tracker(tool: str, tracker: StepTracker) -> bool:
    """Check if a tool is installed and update tracker."""
    if shutil.which(tool):
        tracker.complete(tool, "available")
        return True
    else:
        tracker.error(tool, "not found")
        return False

def check_tool(tool: str, install_hint: str) -> bool:
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

def init_git_repo(project_path: Path, quiet: bool = False) -> bool:
    """Initialize a git repository in the specified path.
    quiet: if True suppress console output (tracker handles status)
    """
    try:
        original_cwd = Path.cwd()
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit from Goal template"], check=True, capture_output=True)
        if not quiet:
            console.print("[green]✓[/green] Git repository initialized")
        return True

    except subprocess.CalledProcessError as e:
        if not quiet:
            console.print(f"[red]Error initializing git repository:[/red] {e}")
        return False
    finally:
        os.chdir(original_cwd)

def download_template_from_github(ai_assistant: str, download_dir: Path, *, script_type: str = "sh", verbose: bool = True, show_progress: bool = True, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Tuple[Path, dict]:
    repo_owner = "Nom-nom-hub"
    repo_name = "goal-kit"
    if client is None:
        client = httpx.Client(verify=ssl_context)

    if verbose:
        console.print("[cyan]Fetching latest release information...[/cyan]")
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    try:
        response = client.get(
            api_url,
            timeout=30,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        )
        status = response.status_code
        if status != 200:
            msg = f"GitHub API returned {status} for {api_url}"
            if debug:
                msg += f"\nResponse headers: {response.headers}\nBody (truncated 500): {response.text[:500]}"
            raise RuntimeError(msg)
        try:
            release_data = response.json()
        except ValueError as je:
            raise RuntimeError(f"Failed to parse release JSON: {je}\nRaw (truncated 400): {response.text[:400]}")
    except Exception as e:
        console.print(f"[red]Error fetching release information[/red]")
        console.print(Panel(str(e), title="Fetch Error", border_style="red"))
        raise typer.Exit(1)

    # Find the template asset for the specified AI assistant
    assets = release_data.get("assets", [])
    pattern = f"spec-kit-template-{ai_assistant}-{script_type}"
    matching_assets = [
        asset for asset in assets
        if pattern in asset["name"] and asset["name"].endswith(".zip")
    ]

    asset = matching_assets[0] if matching_assets else None

    if asset is None:
        console.print(f"[red]No matching release asset found[/red] for [bold]{ai_assistant}[/bold] (expected pattern: [bold]{pattern}[/bold])")
        asset_names = [a.get('name', '?') for a in assets]
        console.print(Panel("\n".join(asset_names) or "(no assets)", title="Available Assets", border_style="yellow"))
        raise typer.Exit(1)

    download_url = asset["browser_download_url"]
    filename = asset["name"]
    file_size = asset["size"]

    if verbose:
        console.print(f"[cyan]Found template:[/cyan] {filename}")
        console.print(f"[cyan]Size:[/cyan] {file_size:,} bytes")
        console.print(f"[cyan]Release:[/cyan] {release_data['tag_name']}")

    zip_path = download_dir / filename
    if verbose:
        console.print(f"[cyan]Downloading template...[/cyan]")

    try:
        with client.stream(
            "GET",
            download_url,
            timeout=60,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        ) as response:
            if response.status_code != 200:
                body_sample = response.text[:400]
                raise RuntimeError(f"Download failed with {response.status_code}\nHeaders: {response.headers}\nBody (truncated): {body_sample}")
            total_size = int(response.headers.get('content-length', 0))
            with open(zip_path, 'wb') as f:
                if total_size == 0:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        f.write(chunk)
                else:
                    if show_progress:
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                            console=console,
                        ) as progress:
                            task = progress.add_task("Downloading...", total=total_size)
                            downloaded = 0
                            for chunk in response.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                                downloaded += len(chunk)
                                progress.update(task, completed=downloaded)
                    else:
                        for chunk in response.iter_bytes(chunk_size=8192):
                            f.write(chunk)
    except Exception as e:
        console.print(f"[red]Error downloading template[/red]")
        detail = str(e)
        if zip_path.exists():
            zip_path.unlink()
        console.print(Panel(detail, title="Download Error", border_style="red"))
        raise typer.Exit(1)
    if verbose:
        console.print(f"Downloaded: {filename}")
    metadata = {
        "filename": filename,
        "size": file_size,
        "release": release_data["tag_name"],
        "asset_url": download_url
    }
    return zip_path, metadata

def download_and_extract_template(project_path: Path, ai_assistant: str, script_type: str, is_current_dir: bool = False, *, verbose: bool = True, tracker: StepTracker | None = None, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Path:
    """Download the latest release and extract it to create a new project.
    Returns project_path. Uses tracker if provided (with keys: fetch, download, extract, cleanup)
    """
    current_dir = Path.cwd()

    # Step: fetch + download combined
    if tracker:
        tracker.start("fetch", "contacting GitHub API")
    try:
        zip_path, meta = download_template_from_github(
            ai_assistant,
            current_dir,
            script_type=script_type,
            verbose=verbose and tracker is None,
            show_progress=(tracker is None),
            client=client,
            debug=debug,
            github_token=github_token
        )
        if tracker:
            tracker.complete("fetch", f"release {meta['release']} ({meta['size']:,} bytes)")
            tracker.add("download", "Download template")
            tracker.complete("download", meta['filename'])
    except Exception as e:
        if tracker:
            tracker.error("fetch", str(e))
        else:
            if verbose:
                console.print(f"[red]Error downloading template:[/red] {e}")
        raise

    if tracker:
        tracker.add("extract", "Extract template")
        tracker.start("extract")
    elif verbose:
        console.print("Extracting template...")

    try:
        # Create project directory only if not using current directory
        if not is_current_dir:
            project_path.mkdir(parents=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # List all files in the ZIP for debugging
            zip_contents = zip_ref.namelist()
            if tracker:
                tracker.start("zip-list")
                tracker.complete("zip-list", f"{len(zip_contents)} entries")
            elif verbose:
                console.print(f"[cyan]ZIP contains {len(zip_contents)} items[/cyan]")

            # For current directory, extract to a temp location first
            if is_current_dir:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    zip_ref.extractall(temp_path)

                    # Check what was extracted
                    extracted_items = list(temp_path.iterdir())
                    if tracker:
                        tracker.start("extracted-summary")
                        tracker.complete("extracted-summary", f"temp {len(extracted_items)} items")
                    elif verbose:
                        console.print(f"[cyan]Extracted {len(extracted_items)} items to temp location[/cyan]")

                    # Handle GitHub-style ZIP with a single root directory
                    source_dir = temp_path
                    if len(extracted_items) == 1 and extracted_items[0].is_dir():
                        source_dir = extracted_items[0]
                        if tracker:
                            tracker.add("flatten", "Flatten nested directory")
                            tracker.complete("flatten")
                        elif verbose:
                            console.print(f"[cyan]Found nested directory structure[/cyan]")

                    # Copy contents to current directory
                    for item in source_dir.iterdir():
                        dest_path = project_path / item.name
                        if item.is_dir():
                            if dest_path.exists():
                                if verbose and not tracker:
                                    console.print(f"[yellow]Merging directory:[/yellow] {item.name}")
                                # Recursively copy directory contents
                                for sub_item in item.rglob('*'):
                                    if sub_item.is_file():
                                        rel_path = sub_item.relative_to(item)
                                        dest_file = dest_path / rel_path
                                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                                        shutil.copy2(sub_item, dest_file)
                            else:
                                shutil.copytree(item, dest_path)
                        else:
                            if dest_path.exists() and verbose and not tracker:
                                console.print(f"[yellow]Overwriting file:[/yellow] {item.name}")
                            shutil.copy2(item, dest_path)
                    if verbose and not tracker:
                        console.print(f"[cyan]Template files merged into current directory[/cyan]")
            else:
                # Extract directly to project directory (original behavior)
                zip_ref.extractall(project_path)

                # Check what was extracted
                extracted_items = list(project_path.iterdir())
                if tracker:
                    tracker.start("extracted-summary")
                    tracker.complete("extracted-summary", f"{len(extracted_items)} top-level items")
                elif verbose:
                    console.print(f"[cyan]Extracted {len(extracted_items)} items to {project_path}:[/cyan]")
                    for item in extracted_items:
                        console.print(f"  - {item.name} ({'dir' if item.is_dir() else 'file'})")

                # Handle GitHub-style ZIP with a single root directory
                if len(extracted_items) == 1 and extracted_items[0].is_dir():
                    # Move contents up one level
                    nested_dir = extracted_items[0]
                    temp_move_dir = project_path.parent / f"{project_path.name}_temp"
                    # Move the nested directory contents to temp location
                    shutil.move(str(nested_dir), str(temp_move_dir))
                    # Remove the now-empty project directory
                    project_path.rmdir()
                    # Rename temp directory to project directory
                    shutil.move(str(temp_move_dir), str(project_path))
                    if tracker:
                        tracker.add("flatten", "Flatten nested directory")
                        tracker.complete("flatten")
                    elif verbose:
                        console.print(f"[cyan]Flattened nested directory structure[/cyan]")

    except Exception as e:
        if tracker:
            tracker.error("extract", str(e))
        else:
            if verbose:
                console.print(f"[red]Error extracting template:[/red] {e}")
                if debug:
                    console.print(Panel(str(e), title="Extraction Error", border_style="red"))
        # Clean up project directory if created and not current directory
        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)
    else:
        if tracker:
            tracker.complete("extract")
    finally:
        if tracker:
            tracker.add("cleanup", "Remove temporary archive")
        # Clean up downloaded ZIP file
        if zip_path.exists():
            zip_path.unlink()
            if tracker:
                tracker.complete("cleanup")
            elif verbose:
                console.print(f"Cleaned up: {zip_path.name}")

    return project_path

def ensure_executable_scripts(project_path: Path, tracker: StepTracker | None = None) -> None:
    """Ensure POSIX .sh scripts under .goal/scripts (recursively) have execute bits (no-op on Windows)."""
    if os.name == "nt":
        return  # Windows: skip silently
    scripts_root = project_path / ".goal" / "scripts"
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
            st = script.stat(); mode = st.st_mode
            if mode & 0o111:
                continue
            new_mode = mode
            if mode & 0o400: new_mode |= 0o100
            if mode & 0o040: new_mode |= 0o010
            if mode & 0o004: new_mode |= 0o001
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

@app.command()
def init(
    project_name: str = typer.Argument(None, help="Name for your new project directory (optional if using --here)"),
    ai_assistant: str = typer.Option(None, "--ai", help="AI assistant to use: claude, gemini, copilot, cursor, qwen, opencode, codex, windsurf, kilocode, auggie, roo, deepseek, tabnine, grok, codewhisperer"),
    script_type: str = typer.Option(None, "--script", help="Script type to use: sh or ps"),
    ignore_agent_tools: bool = typer.Option(False, "--ignore-agent-tools", help="Skip checks for AI agent tools like Claude Code"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    here: bool = typer.Option(False, "--here", help="Initialize project in the current directory instead of creating a new one"),
    force: bool = typer.Option(False, "--force", help="Force merge/overwrite when using --here (skip confirmation)"),
    skip_tls: bool = typer.Option(False, "--skip-tls", help="Skip SSL/TLS verification (not recommended)"),
    debug: bool = typer.Option(False, "--debug", help="Show verbose diagnostic output for network and extraction failures"),
    github_token: str = typer.Option(None, "--github-token", help="GitHub token to use for API requests (or set GH_TOKEN or GITHUB_TOKEN environment variable)"),
):
    """
    Initialize a new Goal-Driven Development project from the latest template.

    This command will:
    1. Check that required tools are installed (git is optional)
    2. Let you choose your AI assistant (Claude Code, Gemini CLI, GitHub Copilot, Cursor, Qwen Code, opencode, Codex CLI, Windsurf, Kilo Code, Auggie CLI, Roo Code, DeepSeek, Tabnine, Grok, or CodeWhisperer)
    3. Download the appropriate template from GitHub
    4. Extract the template to a new project directory or current directory
    5. Initialize a fresh git repository (if not --no-git and no existing repo)
    6. Optionally set up AI assistant commands

    Examples:
        goal init my-project
        goal init my-project --ai claude
        goal init my-project --ai copilot
        goal init my-project --ai deepseek
        goal init my-project --ai grok --no-git
        goal init my-project --ai cursor
        goal init my-project --ai tabnine
        goal init --ignore-agent-tools my-project
        goal init --here --ai roo
        goal init --here --ai codewhisperer
        goal init --here
        goal init --here --force  # Skip confirmation when current directory not empty
    """
    # Show banner first
    show_banner()

    # Validate arguments
    if here and project_name:
        console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
        raise typer.Exit(1)

    if not here and not project_name:
        console.print("[red]Error:[/red] Must specify either a project name or use --here flag")
        raise typer.Exit(1)

    # Determine project directory
    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()

        # Check if current directory has any files
        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)")
            console.print("[yellow]Template files will be merged with existing content and may overwrite existing files[/yellow]")
            if force:
                console.print("[cyan]--force supplied: skipping confirmation and proceeding with merge[/cyan]")
            else:
                # Ask for confirmation
                response = typer.confirm("Do you want to continue?")
                if not response:
                    console.print("[yellow]Operation cancelled[/yellow]")
                    raise typer.Exit(0)
    else:
        project_path = Path(project_name).resolve()
        # Check if project directory already exists
        if project_path.exists():
            error_panel = Panel(
                f"Directory '[cyan]{project_name}[/cyan]' already exists\n"
                "Please choose a different project name or remove the existing directory.",
                title="[red]Directory Conflict[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    # Create formatted setup info with column alignment
    current_dir = Path.cwd()

    setup_lines = [
        "[cyan]Goal-Driven Project Setup[/cyan]",
        "",
        f"{'Project':<15} [green]{project_path.name}[/green]",
        f"{'Working Path':<15} [dim]{current_dir}[/dim]",
    ]

    # Add target path only if different from working dir
    if not here:
        setup_lines.append(f"{'Target Path':<15} [dim]{project_path}[/dim]")

    console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))

    # Check git only if we might need it (not --no-git)
    # Only set to True if the user wants it and the tool is available
    should_init_git = False
    if not no_git:
        should_init_git = check_tool("git", "https://git-scm.com/downloads")
        if not should_init_git:
            console.print("[yellow]Git not found - will skip repository initialization[/yellow]")

    # AI assistant selection
    if ai_assistant:
        if ai_assistant not in AI_CHOICES:
            console.print(f"[red]Error:[/red] Invalid AI assistant '{ai_assistant}'. Choose from: {', '.join(AI_CHOICES.keys())}")
            raise typer.Exit(1)
        selected_ai = ai_assistant
    else:
        # Use arrow-key selection interface
        selected_ai = select_with_arrows(
            AI_CHOICES,
            "Choose your AI assistant:",
            "copilot"
        )

    # Check agent tools unless ignored
    if not ignore_agent_tools:
        agent_tool_missing = False
        install_url = ""
        if selected_ai == "claude":
            if not check_tool("claude", "https://docs.anthropic.com/en/docs/claude-code/setup"):
                install_url = "https://docs.anthropic.com/en/docs/claude-code/setup"
                agent_tool_missing = True
        elif selected_ai == "gemini":
            if not check_tool("gemini", "https://github.com/google-gemini/gemini-cli"):
                install_url = "https://github.com/google-gemini/gemini-cli"
                agent_tool_missing = True
        elif selected_ai == "qwen":
            if not check_tool("qwen", "https://github.com/QwenLM/qwen-code"):
                install_url = "https://github.com/QwenLM/qwen-code"
                agent_tool_missing = True
        elif selected_ai == "opencode":
            if not check_tool("opencode", "https://opencode.ai"):
                install_url = "https://opencode.ai"
                agent_tool_missing = True
        elif selected_ai == "codex":
            if not check_tool("codex", "https://github.com/openai/codex"):
                install_url = "https://github.com/openai/codex"
                agent_tool_missing = True
        elif selected_ai == "auggie":
            if not check_tool("auggie", "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli"):
                install_url = "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli"
                agent_tool_missing = True
        elif selected_ai == "deepseek":
            if not check_tool("deepseek", "https://github.com/deepseek-ai/DeepSeek-Coder"):
                install_url = "https://github.com/deepseek-ai/DeepSeek-Coder"
                agent_tool_missing = True
        elif selected_ai == "tabnine":
            if not check_tool("tabnine", "https://www.tabnine.com/install"):
                install_url = "https://www.tabnine.com/install"
                agent_tool_missing = True
        elif selected_ai == "grok":
            if not check_tool("grok", "https://github.com/xai-org/grok"):
                install_url = "https://github.com/xai-org/grok"
                agent_tool_missing = True
        elif selected_ai == "codewhisperer":
            if not check_tool("codewhisperer", "https://aws.amazon.com/codewhisperer"):
                install_url = "https://aws.amazon.com/codewhisperer"
                agent_tool_missing = True
        # GitHub Copilot and Cursor checks are not needed as they're typically available in supported IDEs

        if agent_tool_missing:
            error_panel = Panel(
                f"[cyan]{selected_ai}[/cyan] not found\n"
                f"Install with: [cyan]{install_url}[/cyan]\n"
                f"{AI_CHOICES[selected_ai]} is required to continue with this project type.\n\n"
                "Tip: Use [cyan]--ignore-agent-tools[/cyan] to skip this check",
                title="[red]Agent Detection Error[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    # Determine script type (explicit, interactive, or OS default)
    if script_type:
        if script_type not in SCRIPT_TYPE_CHOICES:
            console.print(f"[red]Error:[/red] Invalid script type '{script_type}'. Choose from: {', '.join(SCRIPT_TYPE_CHOICES.keys())}")
            raise typer.Exit(1)
        selected_script = script_type
    else:
        # Auto-detect default
        default_script = "ps" if os.name == "nt" else "sh"
        # Provide interactive selection similar to AI if stdin is a TTY
        if sys.stdin.isatty():
            selected_script = select_with_arrows(SCRIPT_TYPE_CHOICES, "Choose script type (or press Enter)", default_script)
        else:
            selected_script = default_script

    console.print(f"[cyan]Selected AI assistant:[/cyan] {selected_ai}")
    console.print(f"[cyan]Selected script type:[/cyan] {selected_script}")

    # Download and set up project
    # New tree-based progress (no emojis); include earlier substeps
    tracker = StepTracker("Initialize Goal Project")
    # Flag to allow suppressing legacy headings
    sys._goal_tracker_active = True
    # Pre steps recorded as completed before live rendering
    tracker.add("precheck", "Check required tools")
    tracker.complete("precheck", "ok")
    tracker.add("ai-select", "Select AI assistant")
    tracker.complete("ai-select", f"{selected_ai}")
    tracker.add("script-select", "Select script type")
    tracker.complete("script-select", selected_script)
    for key, label in [
        ("fetch", "Fetch latest release"),
        ("download", "Download template"),
        ("extract", "Extract template"),
        ("zip-list", "Archive contents"),
        ("extracted-summary", "Extraction summary"),
        ("chmod", "Ensure scripts executable"),
        ("cleanup", "Cleanup"),
        ("git", "Initialize git repository"),
        ("final", "Finalize")
    ]:
        tracker.add(key, label)

    # Use transient so live tree is replaced by the final static render (avoids duplicate output)
    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            # Create a httpx client with verify based on skip_tls
            verify = not skip_tls
            local_ssl_context = ssl_context if verify else False
            local_client = httpx.Client(verify=local_ssl_context)

            download_and_extract_template(project_path, selected_ai, selected_script, here, verbose=False, tracker=tracker, client=local_client, debug=debug, github_token=github_token)

            # Ensure scripts are executable (POSIX)
            ensure_executable_scripts(project_path, tracker=tracker)

            # Git step
            if not no_git:
                tracker.start("git")
                if is_git_repo(project_path):
                    tracker.complete("git", "existing repo detected")
                elif should_init_git:
                    if init_git_repo(project_path, quiet=True):
                        tracker.complete("git", "initialized")
                    else:
                        tracker.error("git", "init failed")
                else:
                    tracker.skip("git", "git not available")
            else:
                tracker.skip("git", "--no-git flag")

            tracker.complete("final", "project ready")
        except Exception as e:
            tracker.error("final", str(e))
            console.print(Panel(f"Initialization failed: {e}", title="Failure", border_style="red"))
            if debug:
                _env_pairs = [
                    ("Python", sys.version.split()[0]),
                    ("Platform", sys.platform),
                    ("CWD", str(Path.cwd())),
                ]
                _label_width = max(len(k) for k, _ in _env_pairs)
                env_lines = [f"{k.ljust(_label_width)} → [bright_black]{v}[/bright_black]" for k, v in _env_pairs]
                console.print(Panel("\n".join(env_lines), title="Debug Environment", border_style="magenta"))
            if not here and project_path.exists():
                shutil.rmtree(project_path)
            raise typer.Exit(1)
        finally:
            # Force final render
            pass

    # Final static tree (ensures finished state visible after Live context ends)
    console.print(tracker.render())
    console.print("\n[bold green]Project ready.[/bold green]")

    # Agent folder security notice
    agent_folder_map = {
        "claude": ".claude/",
        "gemini": ".gemini/",
        "cursor": ".cursor/",
        "qwen": ".qwen/",
        "opencode": ".opencode/",
        "codex": ".codex/",
        "windsurf": ".windsurf/",
        "kilocode": ".kilocode/",
        "auggie": ".augment/",
        "copilot": ".github/",
        "roo": ".roo/",
        "deepseek": ".deepseek/",
        "tabnine": ".tabnine/",
        "grok": ".grok/",
        "codewhisperer": ".codewhisperer/"
    }

    if selected_ai in agent_folder_map:
        agent_folder = agent_folder_map[selected_ai]
        security_notice = Panel(
            f"Some agents may store credentials, auth tokens, or other identifying and private artifacts in the agent folder within your project.\n"
            f"Consider adding [cyan]{agent_folder}[/cyan] (or parts of it) to [cyan].gitignore[/cyan] to prevent accidental credential leakage.",
            title="[yellow]Agent Folder Security[/yellow]",
            border_style="yellow",
            padding=(1, 2)
        )
        console.print()
        console.print(security_notice)

    # Boxed "Next steps" section
    steps_lines = []
    if not here:
        steps_lines.append(f"1. Go to the project folder: [cyan]cd {project_name}[/cyan]")
        step_num = 2
    else:
        steps_lines.append("1. You're already in the project directory!")
        step_num = 2

    # Add agent-specific setup step if needed
    if selected_ai == "codex":
        codex_path = project_path / ".codex"
        quoted_path = shlex.quote(str(codex_path))
        if os.name == "nt":  # Windows
            cmd = f"setx CODEX_HOME {quoted_path}"
        else:  # Unix-like systems
            cmd = f"export CODEX_HOME={quoted_path}"

        steps_lines.append(f"{step_num}. Set [cyan]CODEX_HOME[/cyan] environment variable before running Codex: [cyan]{cmd}[/cyan]")
        step_num += 1

    steps_lines.append(f"{step_num}. Start using slash commands with your AI agent:")
    steps_lines.append("   2.1 [cyan]/constitution[/] - Establish project principles")
    steps_lines.append("   2.2 [cyan]/goals[/] - Define project goals and objectives")
    steps_lines.append("   2.3 [cyan]/clarify[/] - Clarify and validate goals")
    steps_lines.append("   2.4 [cyan]/strategize[/] - Create implementation strategies")
    steps_lines.append("   2.5 [cyan]/plan[/] - Create technical implementation plans")
    steps_lines.append("   2.6 [cyan]/tasks[/] - Generate actionable tasks")
    steps_lines.append("   2.7 [cyan]/analyze[/] - Validate alignment & surface inconsistencies")
    steps_lines.append("   2.8 [cyan]/implement[/] - Execute implementation")

    steps_panel = Panel("\n".join(steps_lines), title="Next Steps", border_style="cyan", padding=(1,2))
    console.print()
    console.print(steps_panel)

    if selected_ai == "codex":
        warning_text = """[bold yellow]Important Note:[/bold yellow]

Custom prompts do not yet support arguments in Codex. You may need to manually specify additional project instructions directly in prompt files located in [cyan].codex/prompts/[/cyan].

For more information, see: [cyan]https://github.com/openai/codex/issues/2890[/cyan]"""

        warning_panel = Panel(warning_text, title="Slash Commands in Codex", border_style="yellow", padding=(1,2))
        console.print()
        console.print(warning_panel)

@app.command()
def goals(
    project_name: str = typer.Option(None, "--project", help="Project name to set goals for"),
    output: str = typer.Option(None, "--output", help="Output file path for goals"),
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", help="Run in interactive mode")
):
    """Define project goals and objectives."""
    show_banner()

    if not project_name:
        project_name = Path.cwd().name

    console.print(f"[cyan]Setting goals for project:[/cyan] [bold]{project_name}[/bold]")
    console.print()

    if interactive:
        console.print("[bold]What are the main objectives for this project?[/bold]")
        console.print("Enter your project goals (press Enter twice to finish):")
        console.print()

        goals_lines = []
        while True:
            try:
                line = input("> ").strip()
                if not line:
                    break
                goals_lines.append(line)
            except (KeyboardInterrupt, EOFError):
                break

        goals_content = "\n".join(goals_lines)
    else:
        # Read from stdin or use default
        try:
            goals_content = sys.stdin.read().strip()
        except:
            goals_content = f"Define clear objectives for {project_name}"

    if not goals_content:
        console.print("[yellow]No goals provided. Skipping.[/yellow]")
        return

    # Save goals
    if output:
        output_path = Path(output)
    else:
        # Create goals directory and file
        goals_dir = Path.cwd() / "goals"
        goals_dir.mkdir(exist_ok=True)
        output_path = goals_dir / f"{project_name.lower().replace(' ', '_')}_goals.md"

    with open(output_path, 'w') as f:
        f.write(f"# Goals for {project_name}\n\n")
        f.write(goals_content)
        f.write(f"\n\n*Established: {Path.cwd()}*\n")

    console.print(f"[green]✓[/green] Goals saved to: [cyan]{output_path}[/cyan]")


@app.command()
def clarify(
    goals_file: str = typer.Option(None, "--goals", help="Path to goals file to clarify"),
    output: str = typer.Option(None, "--output", help="Output file for clarified goals")
):
    """Clarify and validate project goals."""
    show_banner()

    if not goals_file:
        # Look for goals files in current directory
        goals_files = list(Path.cwd().glob("*goals*.md"))
        if not goals_files:
            console.print("[red]No goals file found.[/red]")
            console.print("Please specify a goals file with --goals or create one with 'goal goals'")
            return
        goals_file = str(goals_files[0])

    goals_path = Path(goals_file)
    if not goals_path.exists():
        console.print(f"[red]Goals file not found:[/red] {goals_file}")
        return

    with open(goals_path, 'r') as f:
        goals_content = f.read()

    console.print("[cyan]Current goals:[/cyan]")
    console.print(Panel(goals_content, border_style="cyan"))
    console.print()

    console.print("[bold]Clarification Questions:[/bold]")
    questions = [
        "Are these goals specific and measurable?",
        "Are these goals achievable with available resources?",
        "Are these goals relevant to the project's purpose?",
        "Are these goals time-bound with clear deadlines?",
        "Do these goals align with stakeholder expectations?"
    ]

    for i, question in enumerate(questions, 1):
        console.print(f"{i}. {question}")
        response = input(f"   [dim](y/n/na):[/dim] ").lower().strip()
        if response in ['n', 'no']:
            console.print(f"   [yellow]⚠️  Consider revising this aspect[/yellow]")

    # Save clarified goals
    if output:
        output_path = Path(output)
    else:
        output_path = goals_path.with_suffix('_clarified.md')

    with open(output_path, 'w') as f:
        f.write(f"# Clarified Goals\n\n*Based on: {goals_path.name}*\n\n")
        f.write(goals_content)
        f.write(f"\n\n## Clarification Notes\n\n*Clarified on: {Path.cwd()}*\n")

    console.print(f"[green]✓[/green] Clarified goals saved to: [cyan]{output_path}[/cyan]")


@app.command()
def strategize(
    goals_file: str = typer.Option(None, "--goals", help="Path to goals file to strategize for"),
    strategy_type: str = typer.Option("technical", "--type", help="Strategy type: technical, business, hybrid"),
    output: str = typer.Option(None, "--output", help="Output file for strategy")
):
    """Develop implementation strategies for project goals."""
    show_banner()

    if not goals_file:
        # Look for goals files in current directory
        goals_files = list(Path.cwd().glob("*goals*.md"))
        if not goals_files:
            console.print("[red]No goals file found.[/red]")
            console.print("Please specify a goals file with --goals or create one with 'goal goals'")
            return
        goals_file = str(goals_files[0])

    goals_path = Path(goals_file)
    if not goals_path.exists():
        console.print(f"[red]Goals file not found:[/red] {goals_file}")
        return

    with open(goals_path, 'r') as f:
        goals_content = f.read()

    console.print(f"[cyan]Strategizing for goals:[/cyan] [bold]{goals_path.name}[/bold]")
    console.print()

    # Strategy templates based on type
    strategy_templates = {
        "technical": [
            "1. Technology Stack Selection",
            "2. Architecture Patterns",
            "3. Development Phases",
            "4. Testing Strategy",
            "5. Deployment Approach",
            "6. Performance Requirements",
            "7. Security Considerations",
            "8. Scalability Planning"
        ],
        "business": [
            "1. Market Analysis",
            "2. Competitive Positioning",
            "3. Revenue Model",
            "4. Go-to-Market Strategy",
            "5. Customer Acquisition",
            "6. Partnership Opportunities",
            "7. Risk Assessment",
            "8. Success Metrics"
        ],
        "hybrid": [
            "1. Business Objectives",
            "2. Technical Requirements",
            "3. Development Roadmap",
            "4. Resource Planning",
            "5. Risk Management",
            "6. Success Criteria",
            "7. Timeline Milestones",
            "8. Stakeholder Alignment"
        ]
    }

    template = strategy_templates.get(strategy_type, strategy_templates["technical"])

    console.print(f"[bold]{strategy_type.upper()} STRATEGY FRAMEWORK:[/bold]")
    console.print()

    strategy_content = f"# {strategy_type.upper()} Strategy\n\n*Based on: {goals_path.name}*\n\n"

    for item in template:
        console.print(f"• {item}")
        response = input(f"   [dim]Details/notes (press Enter to skip):[/dim] ").strip()
        if response:
            strategy_content += f"## {item}\n\n{response}\n\n"

    # Save strategy
    if output:
        output_path = Path(output)
    else:
        strategy_dir = Path.cwd() / "strategies"
        strategy_dir.mkdir(exist_ok=True)
        base_name = goals_path.stem.replace('_goals', '').replace('goals', '')
        output_path = strategy_dir / f"{base_name}_{strategy_type}_strategy.md"

    with open(output_path, 'w') as f:
        f.write(strategy_content)

    console.print(f"[green]✓[/green] Strategy saved to: [cyan]{output_path}[/cyan]")


@app.command()
def plan(
    strategy_file: str = typer.Option(None, "--strategy", help="Path to strategy file to create plan for"),
    detail_level: str = typer.Option("standard", "--detail", help="Detail level: basic, standard, detailed"),
    output: str = typer.Option(None, "--output", help="Output file for plan")
):
    """Create technical implementation plans from strategy."""
    show_banner()

    if not strategy_file:
        # Look for strategy files in current directory
        strategy_files = list(Path.cwd().glob("*strategy*.md"))
        if not strategy_files:
            console.print("[red]No strategy file found.[/red]")
            console.print("Please specify a strategy file with --strategy or create one with 'goal strategize'")
            return
        strategy_file = str(strategy_files[0])

    strategy_path = Path(strategy_file)
    if not strategy_path.exists():
        console.print(f"[red]Strategy file not found:[/red] {strategy_file}")
        return

    with open(strategy_path, 'r') as f:
        strategy_content = f.read()

    console.print(f"[cyan]Creating implementation plan for:[/cyan] [bold]{strategy_path.name}[/bold]")
    console.print()

    # Detail level configurations
    detail_configs = {
        "basic": {
            "phases": ["Planning", "Development", "Testing", "Deployment"],
            "include_timeline": False,
            "include_resources": False,
            "include_risks": False
        },
        "standard": {
            "phases": ["Requirements Analysis", "Design", "Implementation", "Testing", "Deployment", "Maintenance"],
            "include_timeline": True,
            "include_resources": True,
            "include_risks": True
        },
        "detailed": {
            "phases": ["Requirements Analysis", "System Design", "Component Design", "Implementation", "Unit Testing", "Integration Testing", "System Testing", "UAT", "Deployment", "Operations"],
            "include_timeline": True,
            "include_resources": True,
            "include_risks": True
        }
    }

    config = detail_configs.get(detail_level, detail_configs["standard"])

    plan_content = f"# Implementation Plan - {detail_level.upper()}\n\n*Based on: {strategy_path.name}*\n\n"

    for i, phase in enumerate(config["phases"], 1):
        plan_content += f"## {i}. {phase}\n\n"
        plan_content += f"### Objectives\n\n*Define objectives for {phase.lower()} phase*\n\n"

        if config["include_resources"]:
            plan_content += f"### Resources\n\n*Identify required resources*\n\n"

        if config["include_timeline"]:
            plan_content += f"### Timeline\n\n*Estimated duration and milestones*\n\n"

        if config["include_risks"]:
            plan_content += f"### Risks & Mitigations\n\n*Identify potential risks and mitigation strategies*\n\n"

        plan_content += f"### Deliverables\n\n*List expected deliverables*\n\n"

        # Interactive input for each phase
        console.print(f"[bold]{phase} Phase:[/bold]")
        objectives = input("   Objectives: ").strip()
        if objectives:
            plan_content = plan_content.replace(f"*Define objectives for {phase.lower()} phase*", objectives)

        if config["include_resources"]:
            resources = input("   Resources: ").strip()
            if resources:
                plan_content = plan_content.replace("*Identify required resources*", resources)

        console.print()

    # Save plan
    if output:
        output_path = Path(output)
    else:
        plans_dir = Path.cwd() / "plans"
        plans_dir.mkdir(exist_ok=True)
        base_name = strategy_path.stem.replace('_strategy', '').replace('strategy', '')
        output_path = plans_dir / f"{base_name}_implementation_plan.md"

    with open(output_path, 'w') as f:
        f.write(plan_content)

    console.print(f"[green]✓[/green] Implementation plan saved to: [cyan]{output_path}[/cyan]")


@app.command()
def tasks(
    plan_file: str = typer.Option(None, "--plan", help="Path to plan file to generate tasks from"),
    output: str = typer.Option(None, "--output", help="Output file for tasks"),
    format: str = typer.Option("markdown", "--format", help="Output format: markdown, json, csv")
):
    """Generate actionable tasks from implementation plan."""
    show_banner()

    if not plan_file:
        # Look for plan files in current directory
        plan_files = list(Path.cwd().glob("*plan*.md"))
        if not plan_files:
            console.print("[red]No plan file found.[/red]")
            console.print("Please specify a plan file with --plan or create one with 'goal plan'")
            return
        plan_file = str(plan_files[0])

    plan_path = Path(plan_file)
    if not plan_path.exists():
        console.print(f"[red]Plan file not found:[/red] {plan_file}")
        return

    with open(plan_path, 'r') as f:
        plan_content = f.read()

    console.print(f"[cyan]Generating tasks from plan:[/cyan] [bold]{plan_path.name}[/bold]")
    console.print()

    # Extract phases from plan
    import re
    phase_matches = re.findall(r'## \d+\. ([^\n]+)', plan_content)
    phases = [phase.strip() for phase in phase_matches]

    if not phases:
        console.print("[yellow]No phases found in plan. Creating default task structure.[/yellow]")
        phases = ["Planning", "Development", "Testing", "Deployment"]

    tasks_content = f"# Actionable Tasks\n\n*Generated from: {plan_path.name}*\n\n"

    task_id = 1
    for phase in phases:
        tasks_content += f"## {phase}\n\n"

        # Generate default tasks for each phase
        default_tasks = {
            "Planning": ["Requirements gathering", "Design review", "Resource allocation", "Timeline planning"],
            "Development": ["Environment setup", "Core implementation", "Feature development", "Code review"],
            "Testing": ["Unit tests", "Integration tests", "User acceptance testing", "Performance testing"],
            "Deployment": ["Production deployment", "Monitoring setup", "Documentation update", "Handover"]
        }

        phase_tasks = default_tasks.get(phase, [f"Complete {phase.lower()} activities"])

        for task in phase_tasks:
            tasks_content += f"- [ ] **Task {task_id}:** {task}\n"
            task_id += 1

        tasks_content += "\n"

    # Save tasks
    if output:
        output_path = Path(output)
    else:
        tasks_dir = Path.cwd() / "tasks"
        tasks_dir.mkdir(exist_ok=True)
        base_name = plan_path.stem.replace('_plan', '').replace('plan', '')
        output_path = tasks_dir / f"{base_name}_tasks.md"

    with open(output_path, 'w') as f:
        f.write(tasks_content)

    console.print(f"[green]✓[/green] Tasks generated and saved to: [cyan]{output_path}[/cyan]")
    console.print(f"[cyan]Generated {task_id-1} tasks across {len(phases)} phases[/cyan]")


@app.command()
def constitution(
    project_name: str = typer.Option(None, "--project", help="Project name for constitution"),
    principles: str = typer.Option(None, "--principles", help="Core principles (comma-separated)"),
    output: str = typer.Option(None, "--output", help="Output file for constitution")
):
    """Establish project principles and constitution."""
    show_banner()

    if not project_name:
        project_name = Path.cwd().name

    console.print(f"[cyan]Creating constitution for:[/cyan] [bold]{project_name}[/bold]")
    console.print()

    if not principles:
        console.print("[bold]Enter core principles for this project (press Enter twice to finish):[/bold]")
        principles_list = []
        while True:
            try:
                principle = input("> ").strip()
                if not principle:
                    break
                principles_list.append(principle)
            except (KeyboardInterrupt, EOFError):
                break
        principles = ", ".join(principles_list) if principles_list else "Quality, Collaboration, Innovation"

    # Constitution template
    constitution_content = f"""# {project_name} Project Constitution

## Core Principles
{principles}

## Code of Conduct

### Quality Standards
- Write clean, maintainable, and well-documented code
- Follow established coding standards and best practices
- Conduct thorough testing before deployment
- Document changes and decisions appropriately

### Collaboration Guidelines
- Communicate openly and respectfully with team members
- Provide constructive feedback and support
- Share knowledge and learn from others
- Respect diverse perspectives and approaches

### Innovation Practices
- Embrace continuous learning and improvement
- Experiment with new technologies and approaches
- Learn from both successes and failures
- Stay curious and open to new ideas

## Decision Making Framework

When making technical decisions, consider:
1. **Alignment with goals** - Does this support our project objectives?
2. **Long-term impact** - Will this create technical debt or future problems?
3. **Team consensus** - Have we discussed this with relevant stakeholders?
4. **Maintainability** - Can future developers understand and maintain this?

## Success Metrics

- **Quality**: Code review approval rate, test coverage, bug reports
- **Velocity**: Sprint completion rate, feature delivery time
- **Collaboration**: Team satisfaction, knowledge sharing
- **Innovation**: Learning activities, technology adoption

---

*This constitution establishes the foundational principles and practices for the {project_name} project. All team members are expected to understand and follow these guidelines.*

*Established: {Path.cwd()}*
"""

    # Save constitution
    if output:
        output_path = Path(output)
    else:
        constitution_dir = Path.cwd() / "docs"
        constitution_dir.mkdir(exist_ok=True)
        output_path = constitution_dir / f"{project_name.lower().replace(' ', '_')}_constitution.md"

    with open(output_path, 'w') as f:
        f.write(constitution_content)

    console.print(f"[green]✓[/green] Project constitution saved to: [cyan]{output_path}[/cyan]")


@app.command()
def analyze(
    project_path: str = typer.Option(".", "--path", help="Path to project to analyze"),
    include_goals: bool = typer.Option(True, "--include-goals", help="Analyze goal alignment"),
    include_technical: bool = typer.Option(True, "--include-technical", help="Analyze technical consistency"),
    output: str = typer.Option(None, "--output", help="Output file for analysis")
):
    """Validate alignment and surface inconsistencies in project structure."""
    show_banner()

    project_path_obj = Path(project_path).resolve()
    if not project_path_obj.exists():
        console.print(f"[red]Project path not found:[/red] {project_path}")
        return

    console.print(f"[cyan]Analyzing project:[/cyan] [bold]{project_path_obj}[/bold]")
    console.print()

    analysis_results = []
    inconsistencies = []

    # Check project structure
    required_dirs = ["src", "docs", "tests"]
    required_files = ["README.md", "pyproject.toml", "requirements.txt"]

    analysis_results.append("## Project Structure Analysis")

    for dir_name in required_dirs:
        dir_path = project_path_obj / dir_name
        if dir_path.exists():
            analysis_results.append(f"✓ {dir_name}/ directory exists")
        else:
            inconsistencies.append(f"Missing {dir_name}/ directory")
            analysis_results.append(f"✗ {dir_name}/ directory missing")

    for file_name in required_files:
        file_path = project_path_obj / file_name
        if file_path.exists():
            analysis_results.append(f"✓ {file_name} exists")
        else:
            analysis_results.append(f"⚠ {file_name} missing (optional)")

    # Check for goal-driven development artifacts
    if include_goals:
        analysis_results.append("\n## Goal-Driven Development Analysis")

        goals_files = list(project_path_obj.glob("*goals*.md"))
        if goals_files:
            analysis_results.append(f"✓ Goals documentation found ({len(goals_files)} files)")
        else:
            inconsistencies.append("No goals documentation found")
            analysis_results.append("✗ No goals documentation found")

        strategy_files = list(project_path_obj.glob("*strategy*.md"))
        if strategy_files:
            analysis_results.append(f"✓ Strategy documentation found ({len(strategy_files)} files)")
        else:
            inconsistencies.append("No strategy documentation found")
            analysis_results.append("✗ No strategy documentation found")

        plan_files = list(project_path_obj.glob("*plan*.md"))
        if plan_files:
            analysis_results.append(f"✓ Implementation plans found ({len(plan_files)} files)")
        else:
            inconsistencies.append("No implementation plans found")
            analysis_results.append("✗ No implementation plans found")

    # Technical consistency checks
    if include_technical:
        analysis_results.append("\n## Technical Consistency Analysis")

        # Check for Python-specific files
        pyproject_file = project_path_obj / "pyproject.toml"
        setup_file = project_path_obj / "setup.py"

        if pyproject_file.exists():
            analysis_results.append("✓ Using modern pyproject.toml configuration")
        elif setup_file.exists():
            analysis_results.append("⚠ Using legacy setup.py (consider migrating to pyproject.toml)")
        else:
            analysis_results.append("✗ No Python package configuration found")

        # Check for dependency management
        requirements_files = list(project_path_obj.glob("requirements*.txt"))
        if requirements_files:
            analysis_results.append(f"✓ Dependency management via requirements files ({len(requirements_files)} files)")
        else:
            analysis_results.append("⚠ No requirements files found")

    # Summary
    analysis_results.append(f"\n## Summary")
    analysis_results.append(f"Project location: {project_path_obj}")
    analysis_results.append(f"Analysis date: {Path.cwd()}")

    if inconsistencies:
        analysis_results.append(f"\n### Issues Found ({len(inconsistencies)})")
        for issue in inconsistencies:
            analysis_results.append(f"- {issue}")

        analysis_results.append("\n### Recommendations")
        analysis_results.append("- Address the identified inconsistencies")
        analysis_results.append("- Ensure all goal-driven development artifacts are in place")
        analysis_results.append("- Review technical debt and configuration")

    analysis_content = "\n".join(analysis_results)

    # Save analysis
    if output:
        output_path = Path(output)
    else:
        analysis_dir = project_path_obj / "analysis"
        analysis_dir.mkdir(exist_ok=True)
        output_path = analysis_dir / f"project_analysis_{project_path_obj.name}.md"

    with open(output_path, 'w') as f:
        f.write(analysis_content)

    console.print(f"[green]✓[/green] Project analysis saved to: [cyan]{output_path}[/cyan]")

    if inconsistencies:
        console.print(f"[yellow]⚠ Found {len(inconsistencies)} inconsistencies that should be addressed[/yellow]")


@app.command()
def implement(
    tasks_file: str = typer.Option(None, "--tasks", help="Path to tasks file to implement"),
    phase: str = typer.Option(None, "--phase", help="Specific phase to implement"),
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", help="Run in interactive mode"),
    output: str = typer.Option(None, "--output", help="Output file for implementation log")
):
    """Execute implementation tasks and track progress."""
    show_banner()

    if not tasks_file:
        # Look for tasks files in current directory
        tasks_files = list(Path.cwd().glob("*tasks*.md"))
        if not tasks_files:
            console.print("[red]No tasks file found.[/red]")
            console.print("Please specify a tasks file with --tasks or create one with 'goal tasks'")
            return
        tasks_file = str(tasks_files[0])

    tasks_path = Path(tasks_file)
    if not tasks_path.exists():
        console.print(f"[red]Tasks file not found:[/red] {tasks_file}")
        return

    with open(tasks_path, 'r') as f:
        tasks_content = f.read()

    console.print(f"[cyan]Implementing tasks from:[/cyan] [bold]{tasks_path.name}[/bold]")
    console.print()

    # Parse tasks from markdown
    import re
    task_matches = re.findall(r'- \[([ x])\] \*\*Task (\d+):\*\* (.+)', tasks_content)
    tasks = [(task_id, description, completed == 'x') for completed, task_id, description in task_matches]

    if not tasks:
        console.print("[yellow]No tasks found in the file. Creating sample implementation log.[/yellow]")
        tasks = [("1", "Setup development environment", False), ("2", "Implement core functionality", False)]

    # Filter by phase if specified
    if phase:
        phase_lower = phase.lower()
        filtered_tasks = []
        for task_id, description, completed in tasks:
            if phase_lower in description.lower():
                filtered_tasks.append((task_id, description, completed))
        tasks = filtered_tasks
        if not tasks:
            console.print(f"[yellow]No tasks found for phase '{phase}'. Implementing all tasks.[/yellow]")

    implementation_log = f"# Implementation Log\n\n*Based on: {tasks_path.name}*\n\n"

    completed_count = 0
    total_tasks = len(tasks)

    for i, (task_id, description, is_completed) in enumerate(tasks, 1):
        status_symbol = "✓" if is_completed else "○"
        status_color = "green" if is_completed else "yellow"

        console.print(f"[{status_color}]{status_symbol}[/{status_color}] Task {task_id}: {description}")

        if not is_completed:
            if interactive:
                action = input(f"   [dim]Action (complete/skip/notes):[/dim] ").lower().strip()

                if action in ['c', 'complete', 'done', 'y', 'yes']:
                    implementation_log += f"## Task {task_id}: {description}\n\n"
                    implementation_log += f"**Status:** Completed\n"
                    implementation_log += f"**Notes:** Implementation completed successfully\n\n"
                    completed_count += 1
                elif action in ['n', 'notes']:
                    notes = input("   Notes: ").strip()
                    implementation_log += f"## Task {task_id}: {description}\n\n"
                    implementation_log += f"**Status:** In Progress\n"
                    implementation_log += f"**Notes:** {notes}\n\n"
                else:
                    implementation_log += f"## Task {task_id}: {description}\n\n"
                    implementation_log += f"**Status:** Skipped\n"
                    implementation_log += f"**Reason:** User skipped during implementation\n\n"
            else:
                implementation_log += f"## Task {task_id}: {description}\n\n"
                implementation_log += f"**Status:** Pending\n"
                implementation_log += f"**Notes:** Non-interactive mode - manual completion required\n\n"
        else:
            implementation_log += f"## Task {task_id}: {description}\n\n"
            implementation_log += f"**Status:** Already Completed\n"
            implementation_log += f"**Notes:** Task was already marked as complete\n\n"
            completed_count += 1

    # Add summary
    implementation_log += f"## Implementation Summary\n\n"
    implementation_log += f"- Total tasks: {total_tasks}\n"
    implementation_log += f"- Completed: {completed_count}\n"
    implementation_log += f"- Completion rate: {(completed_count/total_tasks)*100:.1f}%\n"
    implementation_log += f"- Date: {Path.cwd()}\n"

    # Save implementation log
    if output:
        output_path = Path(output)
    else:
        logs_dir = Path.cwd() / "implementation"
        logs_dir.mkdir(exist_ok=True)
        base_name = tasks_path.stem.replace('_tasks', '').replace('tasks', '')
        output_path = logs_dir / f"{base_name}_implementation_log.md"

    with open(output_path, 'w') as f:
        f.write(implementation_log)

    console.print(f"\n[green]✓[/green] Implementation log saved to: [cyan]{output_path}[/cyan]")
    console.print(f"[cyan]Completed {completed_count}/{total_tasks} tasks[/cyan]")


@app.command()
def check():
    """Check that all required tools are installed."""
    show_banner()
    console.print("[bold]Checking for installed tools...[/bold]\n")

    tracker = StepTracker("Check Available Tools")

    tracker.add("git", "Git version control")
    tracker.add("claude", "Claude Code CLI")
    tracker.add("gemini", "Gemini CLI")
    tracker.add("qwen", "Qwen Code CLI")
    tracker.add("code", "Visual Studio Code")
    tracker.add("code-insiders", "Visual Studio Code Insiders")
    tracker.add("cursor-agent", "Cursor IDE agent")
    tracker.add("windsurf", "Windsurf IDE")
    tracker.add("kilocode", "Kilo Code IDE")
    tracker.add("opencode", "opencode")
    tracker.add("codex", "Codex CLI")
    tracker.add("auggie", "Auggie CLI")
    tracker.add("roo", "Roo Code CLI")
    tracker.add("deepseek", "DeepSeek Coder CLI")
    tracker.add("tabnine", "Tabnine AI CLI")
    tracker.add("grok", "Grok xAI CLI")
    tracker.add("codewhisperer", "CodeWhisperer CLI")

    git_ok = check_tool_for_tracker("git", tracker)
    claude_ok = check_tool_for_tracker("claude", tracker)
    gemini_ok = check_tool_for_tracker("gemini", tracker)
    qwen_ok = check_tool_for_tracker("qwen", tracker)
    code_ok = check_tool_for_tracker("code", tracker)
    code_insiders_ok = check_tool_for_tracker("code-insiders", tracker)
    cursor_ok = check_tool_for_tracker("cursor-agent", tracker)
    windsurf_ok = check_tool_for_tracker("windsurf", tracker)
    kilocode_ok = check_tool_for_tracker("kilocode", tracker)
    opencode_ok = check_tool_for_tracker("opencode", tracker)
    codex_ok = check_tool_for_tracker("codex", tracker)
    auggie_ok = check_tool_for_tracker("auggie", tracker)
    roo_ok = check_tool_for_tracker("roo", tracker)
    deepseek_ok = check_tool_for_tracker("deepseek", tracker)
    tabnine_ok = check_tool_for_tracker("tabnine", tracker)
    grok_ok = check_tool_for_tracker("grok", tracker)
    codewhisperer_ok = check_tool_for_tracker("codewhisperer", tracker)

    console.print(tracker.render())

    console.print("\n[bold green]Goal CLI is ready to use![/bold green]")

    if not git_ok:
        console.print("[dim]Tip: Install git for repository management[/dim]")
    if not (claude_ok or gemini_ok or cursor_ok or qwen_ok or windsurf_ok or kilocode_ok or opencode_ok or codex_ok or auggie_ok or roo_ok or deepseek_ok or tabnine_ok or grok_ok or codewhisperer_ok):
        console.print("[dim]Tip: Install an AI assistant for the best experience[/dim]")

def main():
    app()

if __name__ == "__main__":
    main()