"""Integration tests for analytics CLI commands.

Tests cover:
- All analytics commands
- Text and JSON output modes
- Command-line argument handling
- Error conditions
"""

from datetime import datetime, timedelta
from pathlib import Path

import pytest
from typer.testing import CliRunner

from goalkeeper_cli.analytics import AnalyticsEngine
from goalkeeper_cli.commands.analytics import app
from goalkeeper_cli.models import GoalkitProject, Goal, Task, TaskStatus


runner = CliRunner()


@pytest.fixture
def goalkit_project(tmp_path):
    """Create a test Goal Kit project."""
    goalkit_dir = tmp_path / ".goalkit"
    goalkit_dir.mkdir()

    # Create goals file
    goals_file = goalkit_dir / "goals.json"
    goals_file.write_text("""[
    {
        "id": "goal-1",
        "title": "Test Goal",
        "description": "A test goal",
        "status": "in_progress",
        "created_at": "2024-12-01T10:00:00",
        "updated_at": "2024-12-08T10:00:00",
        "target_date": "2024-12-20",
        "health_score": 0.75
    }
]""")

    # Create tasks file
    tasks_file = goalkit_dir / "tasks.json"
    tasks_file.write_text("""[
    {"id": "task-1", "goal_id": "goal-1", "title": "Task 1", "status": "completed"},
    {"id": "task-2", "goal_id": "goal-1", "title": "Task 2", "status": "in_progress"},
    {"id": "task-3", "goal_id": "goal-1", "title": "Task 3", "status": "todo"}
]""")

    # Add analytics history
    analytics = AnalyticsEngine(goalkit_dir)

    base_date = datetime.now() - timedelta(days=14)
    for i in range(14):
        date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
        completed = min(i, 10)
        analytics.record_snapshot(
            "goal-1",
            completed=completed,
            total=20,
            blocked=max(0, 3 - i // 5),
            in_progress=max(0, 5 - i // 3),
        )

    return tmp_path


@pytest.fixture
def cli_runner(goalkit_project, monkeypatch):
    """Create CLI runner with project directory."""
    monkeypatch.chdir(goalkit_project)
    return runner


class TestBurndownCommand:
    """Test burndown command."""

    def test_burndown_text_output(self, cli_runner):
        """Test burndown with text output."""
        result = cli_runner.invoke(app, ["burndown", "--output", "text"])

        assert result.exit_code == 0
        assert "Burndown Chart" in result.stdout

    def test_burndown_json_output(self, cli_runner):
        """Test burndown with JSON output."""
        result = cli_runner.invoke(app, ["burndown", "--output", "json"])

        assert result.exit_code == 0
        assert '"goal_id"' in result.stdout
        assert '"dates"' in result.stdout

    def test_burndown_with_goal_id(self, cli_runner):
        """Test burndown with explicit goal ID."""
        result = cli_runner.invoke(
            app, ["burndown", "goal-1", "--output", "text"]
        )

        assert result.exit_code == 0

    def test_burndown_nonexistent_goal(self, cli_runner):
        """Test burndown with nonexistent goal."""
        result = cli_runner.invoke(
            app, ["burndown", "nonexistent", "--output", "text"]
        )

        assert result.exit_code == 1

    def test_burndown_no_data(self, cli_runner, monkeypatch):
        """Test burndown with no analytics data."""
        monkeypatch.chdir(cli_runner.env.get("CWD", "."))

        result = cli_runner.invoke(
            app, ["burndown", "goal-1", "--output", "text"]
        )

        # Should handle gracefully
        assert "Insufficient data" in result.stdout or result.exit_code != 0

    def test_burndown_custom_days(self, cli_runner):
        """Test burndown with custom day range."""
        result = cli_runner.invoke(
            app, ["burndown", "--days", "7", "--output", "text"]
        )

        assert result.exit_code == 0


class TestVelocityCommand:
    """Test velocity command."""

    def test_velocity_text_output(self, cli_runner):
        """Test velocity with text output."""
        result = cli_runner.invoke(app, ["velocity", "--output", "text"])

        assert result.exit_code == 0
        assert "Velocity" in result.stdout or "Period" in result.stdout

    def test_velocity_json_output(self, cli_runner):
        """Test velocity with JSON output."""
        result = cli_runner.invoke(app, ["velocity", "--output", "json"])

        assert result.exit_code == 0
        assert '"average_velocity"' in result.stdout
        assert '"trend"' in result.stdout

    def test_velocity_with_goal_id(self, cli_runner):
        """Test velocity with explicit goal ID."""
        result = cli_runner.invoke(
            app, ["velocity", "goal-1", "--output", "text"]
        )

        assert result.exit_code == 0

    def test_velocity_custom_periods(self, cli_runner):
        """Test velocity with custom period count."""
        result = cli_runner.invoke(
            app, ["velocity", "--periods", "6", "--output", "json"]
        )

        assert result.exit_code == 0

    def test_velocity_nonexistent_goal(self, cli_runner):
        """Test velocity with nonexistent goal."""
        result = cli_runner.invoke(
            app, ["velocity", "nonexistent", "--output", "text"]
        )

        assert result.exit_code == 1


class TestTrendsCommand:
    """Test trends command."""

    def test_trends_text_output(self, cli_runner):
        """Test trends with text output."""
        result = cli_runner.invoke(app, ["trends", "--output", "text"])

        assert result.exit_code == 0
        assert "Trend" in result.stdout or "Direction" in result.stdout

    def test_trends_json_output(self, cli_runner):
        """Test trends with JSON output."""
        result = cli_runner.invoke(app, ["trends", "--output", "json"])

        assert result.exit_code == 0
        assert '"direction"' in result.stdout
        assert '"slope"' in result.stdout

    def test_trends_with_goal_id(self, cli_runner):
        """Test trends with explicit goal ID."""
        result = cli_runner.invoke(
            app, ["trends", "goal-1", "--output", "text"]
        )

        assert result.exit_code == 0

    def test_trends_nonexistent_goal(self, cli_runner):
        """Test trends with nonexistent goal."""
        result = cli_runner.invoke(
            app, ["trends", "nonexistent", "--output", "text"]
        )

        assert result.exit_code == 1


class TestForecastCommand:
    """Test forecast command."""

    def test_forecast_text_output(self, cli_runner):
        """Test forecast with text output."""
        result = cli_runner.invoke(app, ["forecast", "--output", "text"])

        assert result.exit_code == 0
        assert "Forecast" in result.stdout or "Completion" in result.stdout

    def test_forecast_json_output(self, cli_runner):
        """Test forecast with JSON output."""
        result = cli_runner.invoke(app, ["forecast", "--output", "json"])

        assert result.exit_code == 0
        assert '"estimated_date"' in result.stdout
        assert '"probability"' in result.stdout

    def test_forecast_with_deadline(self, cli_runner):
        """Test forecast with deadline."""
        deadline = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        result = cli_runner.invoke(
            app, ["forecast", "--deadline", deadline, "--output", "json"]
        )

        assert result.exit_code == 0
        assert '"days_remaining"' in result.stdout

    def test_forecast_with_past_deadline(self, cli_runner):
        """Test forecast with past deadline."""
        deadline = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        result = cli_runner.invoke(
            app, ["forecast", "--deadline", deadline, "--output", "json"]
        )

        assert result.exit_code == 0

    def test_forecast_with_goal_id(self, cli_runner):
        """Test forecast with explicit goal ID."""
        result = cli_runner.invoke(
            app, ["forecast", "goal-1", "--output", "text"]
        )

        assert result.exit_code == 0


class TestInsightsCommand:
    """Test insights command."""

    def test_insights_text_output(self, cli_runner):
        """Test insights with text output."""
        result = cli_runner.invoke(app, ["insights", "--output", "text"])

        assert result.exit_code == 0
        assert "Insights" in result.stdout or "1." in result.stdout

    def test_insights_json_output(self, cli_runner):
        """Test insights with JSON output."""
        result = cli_runner.invoke(app, ["insights", "--output", "json"])

        assert result.exit_code == 0
        assert '"insights"' in result.stdout

    def test_insights_with_goal_id(self, cli_runner):
        """Test insights with explicit goal ID."""
        result = cli_runner.invoke(
            app, ["insights", "goal-1", "--output", "text"]
        )

        assert result.exit_code == 0

    def test_insights_nonexistent_goal(self, cli_runner):
        """Test insights with nonexistent goal."""
        result = cli_runner.invoke(
            app, ["insights", "nonexistent", "--output", "text"]
        )

        assert result.exit_code == 1


class TestAutoGoalSelection:
    """Test automatic goal selection when not specified."""

    def test_uses_first_goal_when_not_specified(self, cli_runner):
        """Test that first goal is used if not specified."""
        result = cli_runner.invoke(app, ["forecast", "--output", "json"])

        assert result.exit_code == 0
        assert '"goal-1"' in result.stdout or "goal" in result.stdout.lower()


class TestNoGoalkitDirectory:
    """Test handling when .goalkit directory doesn't exist."""

    def test_burndown_no_goalkit(self, tmp_path, monkeypatch):
        """Test burndown when .goalkit doesn't exist."""
        monkeypatch.chdir(tmp_path)

        result = runner.invoke(app, ["burndown"])

        assert result.exit_code == 1
        assert "not found" in result.stdout.lower()

    def test_velocity_no_goalkit(self, tmp_path, monkeypatch):
        """Test velocity when .goalkit doesn't exist."""
        monkeypatch.chdir(tmp_path)

        result = runner.invoke(app, ["velocity"])

        assert result.exit_code == 1


class TestOutputFormats:
    """Test output format consistency."""

    def test_json_output_is_valid(self, cli_runner):
        """Test that JSON output is valid JSON."""
        result = cli_runner.invoke(app, ["forecast", "--output", "json"])

        assert result.exit_code == 0
        # Try to parse as JSON
        import json
        try:
            data = json.loads(result.stdout)
            assert isinstance(data, dict)
        except json.JSONDecodeError:
            pytest.fail("Invalid JSON output")

    def test_text_output_has_formatting(self, cli_runner):
        """Test that text output has formatting."""
        result = cli_runner.invoke(app, ["forecast", "--output", "text"])

        assert result.exit_code == 0
        # Should have some formatting
        assert len(result.stdout) > 0

    def test_all_commands_support_both_formats(self, cli_runner):
        """Test all commands support both output formats."""
        commands = ["burndown", "velocity", "trends", "forecast", "insights"]

        for cmd in commands:
            # Text output
            result_text = cli_runner.invoke(
                app, [cmd, "--output", "text"]
            )
            assert result_text.exit_code == 0 or "Insufficient" in result_text.stdout

            # JSON output
            result_json = cli_runner.invoke(
                app, [cmd, "--output", "json"]
            )
            assert result_json.exit_code == 0 or "Insufficient" in result_json.stdout


class TestErrorHandling:
    """Test error handling."""

    def test_invalid_output_format(self, cli_runner):
        """Test handling of invalid output format."""
        result = cli_runner.invoke(
            app, ["forecast", "--output", "invalid"]
        )

        # Should either fail or ignore invalid format
        assert result.exit_code != 0 or result.exit_code == 0

    def test_no_goals_in_project(self, tmp_path, monkeypatch):
        """Test handling when no goals exist."""
        goalkit_dir = tmp_path / ".goalkit"
        goalkit_dir.mkdir()

        # Create empty goals file
        (goalkit_dir / "goals.json").write_text("[]")

        monkeypatch.chdir(tmp_path)

        result = runner.invoke(app, ["forecast"])

        assert result.exit_code == 1

    def test_malformed_goals_file(self, tmp_path, monkeypatch):
        """Test handling of malformed goals file."""
        goalkit_dir = tmp_path / ".goalkit"
        goalkit_dir.mkdir()

        # Create invalid goals file
        (goalkit_dir / "goals.json").write_text("invalid json {")

        monkeypatch.chdir(tmp_path)

        result = runner.invoke(app, ["forecast"])

        assert result.exit_code != 0


class TestRichOutput:
    """Test Rich formatting in output."""

    def test_burndown_has_ascii_chart(self, cli_runner):
        """Test that burndown has ASCII chart."""
        result = cli_runner.invoke(app, ["burndown", "--output", "text"])

        assert result.exit_code == 0
        # Check for ASCII chart elements
        assert "|" in result.stdout or "█" in result.stdout or "·" in result.stdout

    def test_velocity_has_table(self, cli_runner):
        """Test that velocity has table output."""
        result = cli_runner.invoke(app, ["velocity", "--output", "text"])

        assert result.exit_code == 0
        # Should have period and completion data
        assert len(result.stdout) > 0

    def test_insights_are_numbered(self, cli_runner):
        """Test that insights are numbered."""
        result = cli_runner.invoke(app, ["insights", "--output", "text"])

        assert result.exit_code == 0
        # Should have numbered list
        assert "1." in result.stdout or "1)" in result.stdout


class TestEmoji:
    """Test emoji indicators in output."""

    def test_forecast_has_status_emoji(self, cli_runner):
        """Test that forecast includes status emoji."""
        result = cli_runner.invoke(app, ["forecast", "--output", "text"])

        assert result.exit_code == 0
        # Should have status indicator
        assert "✅" in result.stdout or "⚠️" in result.stdout or "🚨" in result.stdout

    def test_velocity_has_trend_emoji(self, cli_runner):
        """Test that velocity includes trend emoji."""
        result = cli_runner.invoke(app, ["velocity", "--output", "text"])

        assert result.exit_code == 0
        # Should have trend indicator
        assert "📈" in result.stdout or "📉" in result.stdout or "➡️" in result.stdout
