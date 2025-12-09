"""CLI commands for webhook management.

Provides commands for:
- Registering and managing webhooks
- Testing webhook delivery
- Viewing event logs
- Event type management
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from goalkeeper_cli.webhooks import WebhookEvent, WebhookManager

app = typer.Typer(help="Webhook management and event notifications")
console = Console()

# Supported event types
EVENT_TYPES = {
    "task_completed": "Triggered when a task is completed",
    "goal_completed": "Triggered when a goal is completed",
    "deadline_approaching": "Triggered when deadline is approaching",
    "high_risk": "Triggered when goal enters high-risk status",
}


def _get_goalkit_path() -> Path:
    """Get the .goalkit directory path."""
    return Path.cwd() / ".goalkit"


@app.command()
def list_webhooks(
    event_type: Optional[str] = typer.Option(
        None, help="Filter by event type"
    ),
    output: str = typer.Option(
        "text", help="Output format (text, json)"
    ),
) -> None:
    """List registered webhooks."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    manager = WebhookManager(goalkit_path)
    webhooks = manager.list_webhooks(event_type)

    if not webhooks:
        console.print("[yellow]No webhooks registered[/yellow]")
        raise typer.Exit(0)

    if output == "json":
        result = {
            "webhooks": [
                {
                    "id": w.id,
                    "event_type": w.event_type,
                    "url": w.url,
                    "enabled": w.enabled,
                    "created_at": w.created_at,
                    "last_triggered": w.last_triggered,
                    "failure_count": w.failure_count,
                }
                for w in webhooks
            ]
        }
        console.print_json(data=result)
    else:
        table = Table(title="Registered Webhooks")
        table.add_column("ID", style="cyan")
        table.add_column("Event Type", style="green")
        table.add_column("URL", style="blue")
        table.add_column("Status", style="yellow")
        table.add_column("Created", style="dim")

        for webhook in webhooks:
            status = "✅ Enabled" if webhook.enabled else "❌ Disabled"
            table.add_row(
                webhook.id,
                webhook.event_type,
                webhook.url[:40] + "..." if len(webhook.url) > 40 else webhook.url,
                status,
                webhook.created_at[:10],
            )

        console.print(table)


@app.command()
def add(
    event_type: str = typer.Argument(
        ..., help=f"Event type ({', '.join(EVENT_TYPES.keys())})"
    ),
    url: str = typer.Argument(..., help="Webhook endpoint URL"),
) -> None:
    """Register a new webhook."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    # Validate event type
    if event_type not in EVENT_TYPES:
        console.print(
            f"[red]Invalid event type: {event_type}[/red]"
        )
        console.print(
            f"Valid types: {', '.join(EVENT_TYPES.keys())}"
        )
        raise typer.Exit(1)

    manager = WebhookManager(goalkit_path)

    try:
        webhook = manager.register_webhook(event_type, url)

        console.print(
            f"\n[green]✓ Webhook registered[/green]\n"
        )
        console.print(f"ID:     {webhook.id}")
        console.print(f"Type:   {webhook.event_type}")
        console.print(f"URL:    {webhook.url}")
        console.print(f"Secret: {webhook.secret}")
        console.print(
            "\n[yellow]Store the secret securely - it's used to sign payloads[/yellow]"
        )

    except Exception as e:
        console.print(f"[red]Error registering webhook: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def remove(
    webhook_id: str = typer.Argument(..., help="Webhook ID to remove"),
) -> None:
    """Remove a webhook."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    manager = WebhookManager(goalkit_path)

    if not manager.delete_webhook(webhook_id):
        console.print(f"[red]Webhook not found: {webhook_id}[/red]")
        raise typer.Exit(1)

    console.print(f"[green]✓ Webhook removed: {webhook_id}[/green]")


@app.command()
def test(
    webhook_id: str = typer.Argument(..., help="Webhook ID to test"),
) -> None:
    """Test webhook delivery."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    manager = WebhookManager(goalkit_path)
    webhook = manager.get_webhook(webhook_id)

    if not webhook:
        console.print(f"[red]Webhook not found: {webhook_id}[/red]")
        raise typer.Exit(1)

    console.print(f"\nTesting webhook: {webhook_id}")
    console.print(f"URL: {webhook.url}\n")

    with console.status("[bold green]Sending test event..."):
        success = manager.test_webhook(webhook_id)

    if success:
        console.print("[green]✓ Test successful[/green]")
        console.print("Webhook is reachable and responding")
    else:
        console.print("[red]✗ Test failed[/red]")
        console.print("Check webhook URL and ensure it's accessible")
        raise typer.Exit(1)


@app.command()
def enable(
    webhook_id: str = typer.Argument(..., help="Webhook ID to enable"),
) -> None:
    """Enable a webhook."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    manager = WebhookManager(goalkit_path)

    if not manager.enable_webhook(webhook_id):
        console.print(f"[red]Webhook not found: {webhook_id}[/red]")
        raise typer.Exit(1)

    console.print(f"[green]✓ Webhook enabled: {webhook_id}[/green]")


@app.command()
def disable(
    webhook_id: str = typer.Argument(..., help="Webhook ID to disable"),
) -> None:
    """Disable a webhook."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    manager = WebhookManager(goalkit_path)

    if not manager.disable_webhook(webhook_id):
        console.print(f"[red]Webhook not found: {webhook_id}[/red]")
        raise typer.Exit(1)

    console.print(f"[green]✓ Webhook disabled: {webhook_id}[/green]")


@app.command()
def events(
    webhook_id: Optional[str] = typer.Option(
        None, help="Filter by webhook ID"
    ),
    limit: int = typer.Option(
        20, help="Number of events to show"
    ),
    output: str = typer.Option(
        "text", help="Output format (text, json)"
    ),
) -> None:
    """View webhook event log."""
    goalkit_path = _get_goalkit_path()

    if not goalkit_path.exists():
        console.print("[red]Error: .goalkit directory not found[/red]")
        raise typer.Exit(1)

    manager = WebhookManager(goalkit_path)
    log_entries = manager.get_event_log(webhook_id, limit)

    if not log_entries:
        console.print("[yellow]No events logged[/yellow]")
        raise typer.Exit(0)

    if output == "json":
        result = {"events": log_entries}
        console.print_json(data=result)
    else:
        table = Table(title="Webhook Event Log")
        table.add_column("Timestamp", style="cyan")
        table.add_column("Webhook ID", style="green")
        table.add_column("Event Type", style="blue")
        table.add_column("Status", style="yellow")
        table.add_column("Retries", style="dim")

        for entry in log_entries:
            status_emoji = "✓" if entry.get("success") else "✗"
            status = f"{status_emoji} {entry.get('status', 'N/A')}"

            table.add_row(
                entry.get("timestamp", "")[:19],
                entry.get("webhook_id", "")[:12],
                entry.get("event_type", ""),
                status,
                str(entry.get("retries", 0)),
            )

        console.print(table)


@app.command()
def types() -> None:
    """Show supported event types."""
    console.print("\n[bold]Supported Event Types[/bold]\n")

    for event_type, description in EVENT_TYPES.items():
        console.print(f"  [cyan]{event_type}[/cyan]")
        console.print(f"    {description}\n")


def show_banner() -> None:
    """Show webhooks app banner."""
    pass
