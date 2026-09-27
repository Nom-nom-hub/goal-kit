"""Integration tests for prediction CLI commands.

Tests cover:
- predict completion / risk / velocity / scenarios commands
- Text and JSON output modes
- Goal ID resolution and error conditions
"""

import json
import re
from datetime import datetime, timedelta

import pytest
from typer.testing import CliRunner

from goalkit.analytics import AnalyticsEngine
from goalkit.commands.prediction import app

runner = CliRunner()


@pytest.fixture
def goalkit_project(tmp_path):
    """Create a test Goal Kit project with analytics history."""
    goalkit_dir = tmp_path / ".goalkit"
    goalkit_dir.mkdir()

    (goalkit_dir / "goals.json").write_text(
        """[
    {
        "id": "goal-1",
        "title": "Test Goal",
        "status": "in_progress",
        "created_at": "2024-12-01T10:00:00",
        "updated_at": "2024-12-08T10:00:00"
    }
]"""
    )
    (goalkit_dir / "tasks.json").write_text(
        """[
    {"id": "task-1", "goal_id": "goal-1", "title": "Task 1", "status": "completed"},
    {"id": "task-2", "goal_id": "goal-1", "title": "Task 2", "status": "completed"},
    {"id": "task-3", "goal_id": "goal-1", "title": "Task 3", "status": "in_progress"}
]"""
    )

    analytics = AnalyticsEngine(goalkit_dir)
    base_date = datetime.now() - timedelta(days=10)
    for i in range(10):
        analytics.record_snapshot(
            "goal-1",
            completed=i + 1,
            total=20,
            blocked=0,
            in_progress=max(0, 5 - i // 2),
            date=(base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
        )

    return tmp_path


@pytest.fixture
def cli_runner(goalkit_project, monkeypatch):
    """Create CLI runner with project directory."""
    monkeypatch.chdir(goalkit_project)
    return runner


def _deadline(days: int) -> str:
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")


class TestCompletionCommand:
    """Test predict completion command."""

    def test_text_output(self, cli_runner):
        result = cli_runner.invoke(app, ["completion", "--output", "text"])
        assert result.exit_code == 0
        assert "completion" in result.stdout.lower()
        assert "Estimated completion" in result.stdout

    def test_json_output(self, cli_runner):
        result = cli_runner.invoke(app, ["completion", "--output", "json"])
        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert data["goal_id"] == "goal-1"
        assert "estimated_date" in data
        assert data["confidence"] == 0.95

    def test_custom_confidence(self, cli_runner):
        result = cli_runner.invoke(
            app, ["completion", "--confidence", "0.5", "--output", "json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert data["confidence"] == 0.5

    def test_explicit_goal_id(self, cli_runner):
        result = cli_runner.invoke(app, ["completion", "goal-1", "--output", "text"])
        assert result.exit_code == 0

    def test_nonexistent_goal(self, cli_runner):
        result = cli_runner.invoke(app, ["completion", "nonexistent", "--output", "text"])
        assert result.exit_code == 1

    def test_no_goalkit_dir(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["completion"])
        assert result.exit_code == 1
        assert "not found" in result.stdout.lower()


class TestRiskCommand:
    """Test predict risk command."""

    def test_text_output(self, cli_runner):
        result = cli_runner.invoke(app, ["risk", "--deadline", _deadline(30)])
        assert result.exit_code == 0
        assert "Risk score" in result.stdout

    def test_json_output(self, cli_runner):
        result = cli_runner.invoke(
            app, ["risk", "--deadline", _deadline(30), "--output", "json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert data["goal_id"] == "goal-1"
        assert "at_risk" in data
        assert "risk_score" in data
        assert "recommendation" in data

    def test_deadline_required(self, cli_runner):
        result = cli_runner.invoke(app, ["risk"])
        assert result.exit_code != 0

    def test_nonexistent_goal(self, cli_runner):
        result = cli_runner.invoke(app, ["risk", "nonexistent", "--deadline", _deadline(7)])
        assert result.exit_code == 1


class TestVelocityCommand:
    """Test predict velocity command."""

    def test_text_output(self, cli_runner):
        result = cli_runner.invoke(app, ["velocity", "--deadline", _deadline(14)])
        assert result.exit_code == 0
        assert "Required pace" in result.stdout

    def test_json_output(self, cli_runner):
        result = cli_runner.invoke(
            app, ["velocity", "--deadline", _deadline(14), "--output", "json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert "required_per_day" in data
        assert "feasible" in data
        assert data["tasks_remaining"] == 10

    def test_past_deadline(self, cli_runner):
        result = cli_runner.invoke(
            app, ["velocity", "--deadline", _deadline(-1), "--output", "json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert data["feasible"] is False

    def test_nonexistent_goal(self, cli_runner):
        result = cli_runner.invoke(
            app, ["velocity", "nonexistent", "--deadline", _deadline(7)]
        )
        assert result.exit_code == 1


class TestScenariosCommand:
    """Test predict scenarios command."""

    def test_text_output_table(self, cli_runner, monkeypatch):
        # Widen console so Rich doesn't wrap scenario names mid-word
        monkeypatch.setenv("COLUMNS", "200")
        result = cli_runner.invoke(app, ["scenarios", "--deadline", _deadline(14)])
        assert result.exit_code == 0
        for name in (
            "Increase Velocity by 20%",
            "Reduce Scope by 20%",
            "2x Parallel Work",
            "Extend Deadline by 2 Weeks",
        ):
            assert name in result.stdout

    def test_json_output(self, cli_runner):
        result = cli_runner.invoke(
            app, ["scenarios", "--deadline", _deadline(14), "--output", "json"]
        )
        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert data["goal_id"] == "goal-1"
        assert len(data["scenarios"]) == 4

    def test_nonexistent_goal(self, cli_runner):
        result = cli_runner.invoke(
            app, ["scenarios", "nonexistent", "--deadline", _deadline(7)]
        )
        assert result.exit_code == 1


class TestOutputFormats:
    """Test output format consistency."""

    def test_json_is_parseable(self, cli_runner):
        result = cli_runner.invoke(
            app, ["completion", "--output", "json"]
        )
        assert result.exit_code == 0
        parsed = json.loads(result.stdout)
        assert isinstance(parsed, dict)
