"""Shared error reporting for the Goalkit CLI.

Commands should fail in one predictable way: a single message on stderr and a
non-zero exit status, so scripts and agents can rely on both.
"""

from __future__ import annotations

from typing import NoReturn

import typer
from rich.console import Console


def fail(message: str, code: int = 1, *, hint: str | None = None) -> NoReturn:
    """Print ``message`` to stderr and exit with ``code``.

    Args:
        message: Human-readable description of the failure.
        code: Process exit status; defaults to 1.
        hint: Optional follow-up line with a suggested fix.

    Raises:
        typer.Exit: Always, so callers do not continue after reporting a failure.
    """
    console = Console(stderr=True)
    console.print(f"[red]Error:[/red] {message}")
    if hint:
        console.print(f"[dim]{hint}[/dim]")
    raise typer.Exit(code)
