"""CLI contract tests: failures must be visible to scripts and agents.

Anything that cannot produce a result has to exit non-zero and say why on
stderr; stdout stays reserved for requested output.
"""

import json

import pytest
from typer.testing import CliRunner

from goalkit import app

runner = CliRunner()

PROJECT_COMMANDS = [
    ["status"],
    ["milestones"],
    ["metrics"],
    ["tasks"],
    ["report"],
    ["insights"],
]


@pytest.mark.parametrize("args", PROJECT_COMMANDS, ids=[c[0] for c in PROJECT_COMMANDS])
def test_command_fails_outside_project(tmp_path, monkeypatch, args):
    """Every project command exits 1 when there is no .goalkit directory."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, args)

    assert result.exit_code == 1
    assert "Not a goal-kit project" in result.stderr
    assert "Not a goal-kit project" not in result.stdout
    assert "Traceback" not in result.stderr


def test_successful_command_exits_zero(goalkit_project):
    """A readable project still succeeds."""
    result = runner.invoke(app, ["status"])

    assert result.exit_code == 0
    assert "Not a goal-kit project" not in result.stderr


def test_json_failure_keeps_stdout_clean(tmp_path, monkeypatch):
    """--json failures must not print prose to stdout."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["status", "--json"])

    assert result.exit_code == 1
    assert result.stdout == ""
    assert "Not a goal-kit project" in result.stderr


def test_json_goal_error_is_machine_readable(goalkit_project):
    """A missing goal in JSON mode returns JSON plus a non-zero exit."""
    result = runner.invoke(app, ["metrics", "--json", "--goal", "does-not-exist"])

    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    assert "error" in payload
    assert "does-not-exist" in payload["error"]


def test_invalid_status_filter_exits_nonzero(goalkit_project):
    """A bad --status value is a user error, not an empty result."""
    result = runner.invoke(app, ["tasks", "--status", "not-a-status"])

    assert result.exit_code == 1
    assert "Invalid status" in result.stderr


def test_invalid_severity_filter_exits_nonzero(goalkit_project):
    """A bad --severity value is a user error, not an empty result."""
    result = runner.invoke(app, ["insights", "--severity", "not-a-severity"])

    assert result.exit_code == 1
    assert "Invalid severity" in result.stderr
