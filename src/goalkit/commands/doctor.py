"""Doctor command for Goalkit CLI — diagnose project health and suggest fixes.

Checks:
1. .goalkit/ directory structure (.goalkit/, goals/, scripts/, templates/, workflows/)
2. Goals for required sections (Summary, Key Stakeholders, User Stories)
3. Script permissions (.sh files under .goalkit/scripts/ must be executable)
4. Template drift (installed templates/workflows vs packaged versions)

Use --fix to auto-resolve fixable issues (missing dirs/files, permissions).
Content drift is reported, never overwritten — templates may be customized.
"""

import hashlib
import os
import stat
from pathlib import Path

import typer
from rich.console import Console

from ..helpers import StepTracker

console = Console()

# Required markdown sections in each goal's goal.md (from goal-template.md)
REQUIRED_GOAL_SECTIONS = ["Summary", "Key Stakeholders", "User Stories"]

# Expected .goalkit subdirectories (created by `goalkit init`)
EXPECTED_DIRS = ["goals", "scripts", "templates", "workflows"]


def _project_root() -> Path:
    """Project root of the installed goalkit package (holds templates/)."""
    return Path(__file__).parent.parent.parent.parent


def _goalkit_dir(project_path: Path) -> Path:
    return project_path / ".goalkit"


def _hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _check_structure(
    project_path: Path, tracker: StepTracker, fix: bool
) -> tuple[int, int]:
    """Validate .goalkit/ directory structure. Returns (ok, fixed)."""
    gk = _goalkit_dir(project_path)
    ok, fixed = 0, 0

    tracker.add("structure", ".goalkit/ directory structure")
    if not gk.is_dir():
        if fix:
            gk.mkdir(parents=True, exist_ok=True)
            tracker.complete("structure", "created missing .goalkit/")
            fixed += 1
        else:
            tracker.error("structure", ".goalkit/ not found — run `goalkit init`")
        return ok, fixed

    missing = [d for d in EXPECTED_DIRS if not (gk / d).is_dir()]
    if not missing:
        tracker.complete("structure", "all expected directories present")
        ok += 1
    elif fix:
        for d in missing:
            (gk / d).mkdir(parents=True, exist_ok=True)
        tracker.complete("structure", f"created missing: {', '.join(missing)}")
        fixed += 1
    else:
        tracker.error("structure", f"missing directories: {', '.join(missing)}")
    return ok, fixed


def _goal_sections(goal_md: Path) -> list[str]:
    """Required sections missing from a goal.md file."""
    try:
        text = goal_md.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return list(REQUIRED_GOAL_SECTIONS)
    return [s for s in REQUIRED_GOAL_SECTIONS if f"## {s}" not in text]


def _check_goals(
    project_path: Path, tracker: StepTracker, fix: bool
) -> tuple[int, int]:
    """Check each goal for goal.md and required sections. Returns (ok, issues)."""
    goals_dir = _goalkit_dir(project_path) / "goals"
    tracker.add("goals", "Goal files and required sections")
    if not goals_dir.is_dir():
        tracker.skip("goals", "no goals directory")
        return 0, 0

    goal_dirs = sorted(p for p in goals_dir.iterdir() if p.is_dir())
    if not goal_dirs:
        tracker.complete("goals", "no goals yet — use /goalkit.goal to create one")
        return 1, 0

    problems: list[str] = []
    for gd in goal_dirs:
        goal_md = gd / "goal.md"
        if not goal_md.is_file():
            problems.append(f"{gd.name}: missing goal.md")
            continue
        missing = _goal_sections(goal_md)
        if missing:
            problems.append(f"{gd.name}: missing sections: {', '.join(missing)}")

    if not problems:
        tracker.complete("goals", f"{len(goal_dirs)} goal(s) healthy")
        return 1, 0
    tracker.error("goals", f"{len(problems)} problem(s) (--fix cannot repair content)")
    for p in problems:
        console.print(f"  [yellow]•[/yellow] {p}")
    return 0, len(problems)


def _check_scripts(
    project_path: Path, tracker: StepTracker, fix: bool
) -> tuple[int, int]:
    """Verify .sh scripts are executable. Returns (ok, fixed)."""
    scripts_root = _goalkit_dir(project_path) / "scripts"
    tracker.add("scripts", "Script permissions")
    if not scripts_root.is_dir():
        tracker.skip("scripts", "no scripts directory")
        return 0, 0
    if os.name == "nt":
        tracker.skip("scripts", "permission check N/A on Windows")
        return 1, 0

    bad: list[Path] = []
    for script in scripts_root.rglob("*.sh"):
        if not script.is_file() or script.is_symlink():
            continue
        header = script.read_bytes()[:2] if script.stat().st_size >= 2 else b""
        if header != b"#!":
            continue
        if not (script.stat().st_mode & stat.S_IXUSR):
            bad.append(script)

    if not bad:
        tracker.complete("scripts", "all scripts executable")
        return 1, 0
    if fix:
        for s in bad:
            mode = s.stat().st_mode
            os.chmod(s, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        tracker.complete("scripts", f"fixed permissions on {len(bad)} script(s)")
        return 0, len(bad)
    tracker.error("scripts", f"{len(bad)} script(s) not executable (use --fix)")
    for s in bad:
        console.print(f"  [yellow]•[/yellow] {s.relative_to(project_path)}")
    return 0, len(bad)


def _packaged_files() -> dict[str, Path]:
    """Map of relative install path -> packaged source path for templates/workflows."""
    root = _project_root()
    out: dict[str, Path] = {}
    tmpl_src = root / "templates"
    if tmpl_src.is_dir():
        for f in tmpl_src.iterdir():
            if f.is_file() and f.suffix == ".md" and f.name != "agent-file-template.md":
                out[f"templates/{f.name}"] = f
    wf_src = tmpl_src / "workflows"
    if wf_src.is_dir():
        for f in wf_src.iterdir():
            if f.is_file() and f.suffix == ".md":
                out[f"workflows/{f.name}"] = f
    return out


def _check_drift(
    project_path: Path, tracker: StepTracker, fix: bool
) -> tuple[int, int]:
    """Detect template drift vs packaged versions. Returns (ok, issues)."""
    gk = _goalkit_dir(project_path)
    tracker.add("drift", "Template drift")
    packaged = _packaged_files()
    if not packaged:
        tracker.skip("drift", "packaged templates not found")
        return 0, 0

    missing: list[str] = []
    drifted: list[str] = []
    for rel, src in sorted(packaged.items()):
        dest = gk / rel
        if not dest.is_file():
            missing.append(rel)
        elif _hash(dest) != _hash(src):
            drifted.append(rel)

    fixed = 0
    if missing and fix:
        import shutil

        for rel in missing:
            dest = gk / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(packaged[rel], dest)
        fixed = len(missing)
        missing = []

    problems = len(missing) + len(drifted)
    if problems == 0:
        msg = "templates in sync"
        if fixed:
            msg += f" ({fixed} restored)"
        tracker.complete("drift", msg)
        return 1, 0

    detail = []
    if missing:
        detail.append(f"{len(missing)} missing")
    if drifted:
        detail.append(f"{len(drifted)} drifted")
    tracker.error("drift", ", ".join(detail))
    for rel in missing:
        console.print(f"  [yellow]•[/yellow] missing: {rel}")
    for rel in drifted:
        console.print(f"  [yellow]•[/yellow] drifted (customized?): {rel}")
    if drifted:
        console.print("  [dim]Drifted templates are reported, never overwritten.[/dim]")
    return 0, problems


def doctor_command(
    project_path: Path | None = None,
    fix: bool = False,
) -> int:
    """Run all health checks. Returns exit code (0 healthy, 1 issues found)."""
    from .. import show_banner

    show_banner()
    path = project_path or Path.cwd()
    console.print("[bold]Diagnosing project health...[/bold]\n")

    tracker = StepTracker("Doctor")
    total_fixed = 0
    total_issues = 0

    ok, fixed = _check_structure(path, tracker, fix)
    total_fixed += fixed
    total_issues += 0 if ok else 1

    ok, _ = _check_goals(path, tracker, fix)
    total_issues += 0 if ok else 1

    ok, fixed = _check_scripts(path, tracker, fix)
    total_fixed += fixed
    total_issues += 0 if ok else 1

    ok, _ = _check_drift(path, tracker, fix)
    total_issues += 0 if ok else 1

    console.print(tracker.render())

    if total_issues == 0:
        console.print("\n[bold green]✓ Project is healthy![/bold green]")
        if total_fixed:
            console.print(f"[dim]Auto-fixed {total_fixed} issue(s).[/dim]")
        return 0

    console.print(f"\n[bold red]✗ Found {total_issues} problem area(s).[/bold red]")
    if not fix:
        console.print(
            "[dim]Tip: run `goalkit doctor --fix` to auto-resolve fixable issues.[/dim]"
        )
    elif total_fixed:
        console.print(f"[dim]Auto-fixed {total_fixed} issue(s).[/dim]")
    return 1


def doctor(
    path: str | None = typer.Argument(None, help="Path to goalkit project"),
    fix: bool = typer.Option(False, "--fix", help="Auto-resolve fixable issues"),
) -> None:
    """Diagnose project health and suggest fixes."""
    project_path = Path(path) if path else None
    code = doctor_command(project_path=project_path, fix=fix)
    raise typer.Exit(code)
