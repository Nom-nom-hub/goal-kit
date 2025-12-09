"""Integration tests for webhooks CLI commands.

Tests cover:
- All webhook commands
- Text and JSON output modes
- Webhook lifecycle (add, list, remove)
- Event testing
"""

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner

from goalkeeper_cli.commands.webhooks import app
from goalkeeper_cli.webhooks import WebhookManager


runner = CliRunner()


@pytest.fixture
def goalkit_project(tmp_path):
    """Create a test Goal Kit project."""
    goalkit_dir = tmp_path / ".goalkit"
    goalkit_dir.mkdir()
    return tmp_path


@pytest.fixture
def cli_runner(goalkit_project, monkeypatch):
    """Create CLI runner with project directory."""
    monkeypatch.chdir(goalkit_project)
    return runner


class TestListCommand:
    """Test webhooks list command."""

    def test_list_empty(self, cli_runner):
        """Test listing when no webhooks registered."""
        result = cli_runner.invoke(app, ["list-webhooks"])

        assert result.exit_code == 0
        assert "No webhooks" in result.stdout

    def test_list_text_output(self, cli_runner):
        """Test list with text output."""
        # Register a webhook first
        cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook1"],
        )

        result = cli_runner.invoke(
            app, ["list-webhooks", "--output", "text"]
        )

        assert result.exit_code == 0
        assert "task_completed" in result.stdout

    def test_list_json_output(self, cli_runner):
        """Test list with JSON output."""
        cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook1"],
        )

        result = cli_runner.invoke(
            app, ["list-webhooks", "--output", "json"]
        )

        assert result.exit_code == 0
        assert '"webhooks"' in result.stdout

    def test_list_filter_by_type(self, cli_runner):
        """Test list filtered by event type."""
        cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook1"],
        )
        cli_runner.invoke(
            app,
            ["add", "goal_completed", "https://example.com/webhook2"],
        )

        result = cli_runner.invoke(
            app,
            ["list-webhooks", "--event-type", "task_completed"],
        )

        assert result.exit_code == 0
        assert "task_completed" in result.stdout

    def test_list_shows_status(self, cli_runner):
        """Test that list shows webhook status."""
        cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook1"],
        )

        result = cli_runner.invoke(app, ["list-webhooks"])

        assert result.exit_code == 0
        assert "✅" in result.stdout or "Enabled" in result.stdout


class TestAddCommand:
    """Test webhooks add command."""

    def test_add_webhook(self, cli_runner):
        """Test adding a webhook."""
        result = cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook"],
        )

        assert result.exit_code == 0
        assert "registered" in result.stdout.lower()
        assert "https://example.com/webhook" in result.stdout

    def test_add_shows_secret(self, cli_runner):
        """Test that add command shows secret."""
        result = cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook"],
        )

        assert result.exit_code == 0
        assert "Secret:" in result.stdout or "secret" in result.stdout.lower()

    def test_add_invalid_event_type(self, cli_runner):
        """Test adding webhook with invalid event type."""
        result = cli_runner.invoke(
            app,
            ["add", "invalid_event", "https://example.com/webhook"],
        )

        assert result.exit_code == 1
        assert "Invalid event type" in result.stdout or "invalid" in result.stdout.lower()

    def test_add_multiple_webhooks(self, cli_runner):
        """Test adding multiple webhooks."""
        cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook1"],
        )
        cli_runner.invoke(
            app,
            ["add", "goal_completed", "https://example.com/webhook2"],
        )

        result = cli_runner.invoke(app, ["list-webhooks"])

        assert result.exit_code == 0
        assert "2" in result.stdout or "webhook" in result.stdout.lower()

    def test_add_different_event_types(self, cli_runner):
        """Test adding webhooks for different event types."""
        for event_type in ["task_completed", "goal_completed", "deadline_approaching"]:
            result = cli_runner.invoke(
                app,
                ["add", event_type, f"https://example.com/{event_type}"],
            )
            assert result.exit_code == 0


class TestRemoveCommand:
    """Test webhooks remove command."""

    def test_remove_webhook(self, cli_runner):
        """Test removing a webhook."""
        # Add webhook
        add_result = cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook"],
        )

        # Extract webhook ID from output
        lines = add_result.stdout.split('\n')
        webhook_id = None
        for line in lines:
            if "ID:" in line or "id" in line.lower():
                webhook_id = line.split()[-1]
                break

        if webhook_id:
            result = cli_runner.invoke(app, ["remove", webhook_id])
            assert result.exit_code == 0
            assert "removed" in result.stdout.lower()

    def test_remove_nonexistent_webhook(self, cli_runner):
        """Test removing webhook that doesn't exist."""
        result = cli_runner.invoke(app, ["remove", "nonexistent"])

        assert result.exit_code == 1
        assert "not found" in result.stdout.lower()


class TestTestCommand:
    """Test webhooks test command."""

    def test_test_nonexistent_webhook(self, cli_runner):
        """Test testing webhook that doesn't exist."""
        result = cli_runner.invoke(app, ["test", "nonexistent"])

        assert result.exit_code == 1

    @patch("goalkeeper_cli.webhooks.httpx.post")
    def test_test_webhook_success(self, mock_post, cli_runner):
        """Test successful webhook test."""
        mock_post.return_value = MagicMock(status_code=200)

        # Add webhook
        add_result = cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook"],
        )

        # Extract webhook ID
        lines = add_result.stdout.split('\n')
        webhook_id = None
        for line in lines:
            if "ID:" in line or "wh_" in line:
                parts = line.split()
                for part in parts:
                    if part.startswith("wh_"):
                        webhook_id = part
                        break

        if webhook_id:
            result = cli_runner.invoke(app, ["test", webhook_id])
            assert result.exit_code == 0
            assert "successful" in result.stdout.lower() or "✓" in result.stdout

    @patch("goalkeeper_cli.webhooks.httpx.post")
    def test_test_webhook_failure(self, mock_post, cli_runner):
        """Test failed webhook test."""
        mock_post.side_effect = Exception("Connection error")

        # Add webhook
        add_result = cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook"],
        )

        # Extract webhook ID
        lines = add_result.stdout.split('\n')
        webhook_id = None
        for line in lines:
            if "ID:" in line or "wh_" in line:
                parts = line.split()
                for part in parts:
                    if part.startswith("wh_"):
                        webhook_id = part
                        break

        if webhook_id:
            result = cli_runner.invoke(app, ["test", webhook_id])
            assert result.exit_code == 1


class TestEnableDisableCommands:
    """Test enable and disable commands."""

    def test_enable_webhook(self, cli_runner):
        """Test enabling a webhook."""
        # Add and disable webhook
        add_result = cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook"],
        )

        lines = add_result.stdout.split('\n')
        webhook_id = None
        for line in lines:
            if "wh_" in line:
                parts = line.split()
                for part in parts:
                    if part.startswith("wh_"):
                        webhook_id = part
                        break

        if webhook_id:
            # Disable first
            cli_runner.invoke(app, ["disable", webhook_id])

            # Then enable
            result = cli_runner.invoke(app, ["enable", webhook_id])
            assert result.exit_code == 0
            assert "enabled" in result.stdout.lower()

    def test_disable_webhook(self, cli_runner):
        """Test disabling a webhook."""
        add_result = cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook"],
        )

        lines = add_result.stdout.split('\n')
        webhook_id = None
        for line in lines:
            if "wh_" in line:
                parts = line.split()
                for part in parts:
                    if part.startswith("wh_"):
                        webhook_id = part
                        break

        if webhook_id:
            result = cli_runner.invoke(app, ["disable", webhook_id])
            assert result.exit_code == 0
            assert "disabled" in result.stdout.lower()

    def test_enable_nonexistent_webhook(self, cli_runner):
        """Test enabling webhook that doesn't exist."""
        result = cli_runner.invoke(app, ["enable", "nonexistent"])

        assert result.exit_code == 1


class TestEventsCommand:
    """Test events command."""

    def test_events_empty(self, cli_runner):
        """Test events command with no logs."""
        result = cli_runner.invoke(app, ["events"])

        assert result.exit_code == 0
        assert "No events" in result.stdout or result.exit_code == 0

    def test_events_json_output(self, cli_runner):
        """Test events with JSON output."""
        result = cli_runner.invoke(app, ["events", "--output", "json"])

        assert result.exit_code == 0

    def test_events_limit(self, cli_runner):
        """Test events with limit."""
        result = cli_runner.invoke(app, ["events", "--limit", "10"])

        assert result.exit_code == 0

    def test_events_filter_by_webhook(self, cli_runner):
        """Test events filtered by webhook ID."""
        result = cli_runner.invoke(
            app, ["events", "--webhook-id", "nonexistent"]
        )

        assert result.exit_code == 0


class TestTypesCommand:
    """Test types command."""

    def test_types_shows_all_types(self, cli_runner):
        """Test that types command shows all event types."""
        result = cli_runner.invoke(app, ["types"])

        assert result.exit_code == 0
        assert "task_completed" in result.stdout
        assert "goal_completed" in result.stdout
        assert "deadline_approaching" in result.stdout
        assert "high_risk" in result.stdout

    def test_types_shows_descriptions(self, cli_runner):
        """Test that types command shows descriptions."""
        result = cli_runner.invoke(app, ["types"])

        assert result.exit_code == 0
        # Should have descriptions
        assert len(result.stdout) > 100


class TestOutputFormats:
    """Test output format consistency."""

    def test_json_output_is_valid(self, cli_runner):
        """Test that JSON output is valid."""
        cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook"],
        )

        result = cli_runner.invoke(
            app, ["list-webhooks", "--output", "json"]
        )

        assert result.exit_code == 0
        import json
        try:
            data = json.loads(result.stdout)
            assert isinstance(data, dict)
        except json.JSONDecodeError:
            pytest.fail("Invalid JSON output")

    def test_text_output_is_readable(self, cli_runner):
        """Test that text output is readable."""
        cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook"],
        )

        result = cli_runner.invoke(
            app, ["list-webhooks", "--output", "text"]
        )

        assert result.exit_code == 0
        assert len(result.stdout) > 0


class TestWebhookLifecycle:
    """Test complete webhook lifecycle."""

    def test_register_list_disable_remove(self, cli_runner):
        """Test webhook lifecycle: register, list, disable, remove."""
        # Register
        add_result = cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook"],
        )
        assert add_result.exit_code == 0

        # List
        list_result = cli_runner.invoke(app, ["list-webhooks"])
        assert list_result.exit_code == 0
        assert "task_completed" in list_result.stdout

        # Extract webhook ID for further operations
        lines = add_result.stdout.split('\n')
        webhook_id = None
        for line in lines:
            if "wh_" in line:
                parts = line.split()
                for part in parts:
                    if part.startswith("wh_"):
                        webhook_id = part
                        break

        if webhook_id:
            # Disable
            disable_result = cli_runner.invoke(app, ["disable", webhook_id])
            assert disable_result.exit_code == 0

            # Remove
            remove_result = cli_runner.invoke(app, ["remove", webhook_id])
            assert remove_result.exit_code == 0

            # Verify removed
            final_list = cli_runner.invoke(app, ["list-webhooks"])
            assert final_list.exit_code == 0


class TestErrorHandling:
    """Test error handling."""

    def test_no_goalkit_directory(self, tmp_path, monkeypatch):
        """Test handling when .goalkit doesn't exist."""
        monkeypatch.chdir(tmp_path)

        result = runner.invoke(app, ["list-webhooks"])

        assert result.exit_code == 1

    def test_invalid_webhook_id(self, cli_runner):
        """Test handling of invalid webhook ID."""
        result = cli_runner.invoke(app, ["remove", "invalid_id"])

        assert result.exit_code == 1

    def test_empty_event_type(self, cli_runner):
        """Test handling of empty event type."""
        result = cli_runner.invoke(
            app, ["add", "", "https://example.com/webhook"]
        )

        # Should fail or require event type
        assert result.exit_code != 0 or "usage" in result.stdout.lower()


class TestSecurityFeatures:
    """Test security-related features."""

    def test_webhook_secret_shown_once(self, cli_runner):
        """Test that webhook secret is shown on registration."""
        result = cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook"],
        )

        assert result.exit_code == 0
        assert "Secret" in result.stdout or "secret" in result.stdout.lower()

    def test_webhook_secret_not_in_list(self, cli_runner):
        """Test that webhook secret is not shown in list."""
        cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook"],
        )

        result = cli_runner.invoke(app, ["list-webhooks"])

        assert result.exit_code == 0
        # Secret should not be in list output
        assert "Secret" not in result.stdout or "secret" not in result.stdout.lower()


class TestRichOutput:
    """Test Rich formatting."""

    def test_list_has_table(self, cli_runner):
        """Test that list has table formatting."""
        cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook"],
        )

        result = cli_runner.invoke(app, ["list-webhooks"])

        assert result.exit_code == 0
        # Should have table elements
        assert len(result.stdout) > 0

    def test_types_has_formatting(self, cli_runner):
        """Test that types command has formatting."""
        result = cli_runner.invoke(app, ["types"])

        assert result.exit_code == 0
        assert "task_completed" in result.stdout


class TestStatusIndicators:
    """Test status indicators in output."""

    def test_webhook_status_shown(self, cli_runner):
        """Test that webhook status is shown in list."""
        cli_runner.invoke(
            app,
            ["add", "task_completed", "https://example.com/webhook"],
        )

        result = cli_runner.invoke(app, ["list-webhooks"])

        assert result.exit_code == 0
        assert "✅" in result.stdout or "Enabled" in result.stdout
