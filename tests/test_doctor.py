"""
Tests for the 'goalkit doctor' command (issue #106).

Tests cover:
- Healthy project reports no issues (exit 0)
- Missing .goalkit structure is detected and fixed with --fix
- Goals missing required sections are flagged (not auto-fixed)
- Non-executable scripts are detected and fixed with --fix
- Template drift (missing/drifted) is detected; missing restored with --fix
"""

import os
import stat
from pathlib import Path

import pytest
from typer.testing import CliRunner

from goalkit import app


def make_project(base: Path, healthy: bool = True) -> Path:
    """Build a scratch goalkit project under base. Returns project path."""
    proj = base / "proj"
    gk = proj / ".goalkit"
    (gk / "goals" / "001-test").mkdir(parents=True)
    (gk / "scripts" / "bash").mkdir(parents=True)
    (gk / "templates").mkdir(parents=True)
    (gk / "workflows").mkdir(parents=True)

    goal_md = gk / "goals" / "001-test" / "goal.md"
    if healthy:
        goal_md.write_text(
            "# Test Goal\n\n## Summary\nA summary.\n\n"
            "## Key Stakeholders\n- Me\n\n## User Stories\n- As a user\n"
        )
    else:
        goal_md.write_text("# Test Goal\n\nNo required sections here.\n")

    script = gk / "scripts" / "bash" / "test.sh"
    script.write_text("#!/bin/bash\necho hi\n")
    os.chmod(script, 0o755 if healthy else 0o644)
    return proj


class TestDoctorHealthy:
    def test_healthy_project_exits_zero(self, tmp_path):
        proj = make_project(tmp_path, healthy=True)
        # Seed templates so drift check passes (copy one packaged file)
        from goalkit.commands.doctor import _packaged_files

        for rel, src in _packaged_files().items():
            dest = proj / ".goalkit" / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(src.read_bytes())

        runner = CliRunner()
        result = runner.invoke(app, ["doctor", str(proj)])
        assert result.exit_code == 0, result.output
        assert "healthy" in result.output.lower()


class TestDoctorStructure:
    def test_missing_goalkit_detected(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        runner = CliRunner()
        result = runner.invoke(app, ["doctor", str(proj)])
        assert result.exit_code == 1
        assert ".goalkit" in result.output

    def test_fix_creates_missing_dirs(self, tmp_path):
        proj = tmp_path / "proj"
        (proj / ".goalkit").mkdir(parents=True)
        runner = CliRunner()
        result = runner.invoke(app, ["doctor", str(proj), "--fix"])
        assert (proj / ".goalkit" / "goals").is_dir()
        assert (proj / ".goalkit" / "scripts").is_dir()
        assert (proj / ".goalkit" / "templates").is_dir()
        assert (proj / ".goalkit" / "workflows").is_dir()


class TestDoctorGoals:
    def test_goal_missing_sections_flagged(self, tmp_path):
        proj = make_project(tmp_path, healthy=False)
        runner = CliRunner()
        result = runner.invoke(app, ["doctor", str(proj)])
        assert result.exit_code == 1
        assert "missing sections" in result.output.lower()

    def test_fix_does_not_repair_goal_content(self, tmp_path):
        proj = make_project(tmp_path, healthy=False)
        runner = CliRunner()
        runner.invoke(app, ["doctor", str(proj), "--fix"])
        goal_md = proj / ".goalkit" / "goals" / "001-test" / "goal.md"
        # --fix must not touch goal content
        assert "## Summary" not in goal_md.read_text()


class TestDoctorScripts:
    @pytest.mark.skipif(os.name == "nt", reason="POSIX permissions only")
    def test_non_executable_script_detected(self, tmp_path):
        proj = make_project(tmp_path, healthy=False)
        runner = CliRunner()
        result = runner.invoke(app, ["doctor", str(proj)])
        assert "not executable" in result.output.lower()

    @pytest.mark.skipif(os.name == "nt", reason="POSIX permissions only")
    def test_fix_makes_scripts_executable(self, tmp_path):
        proj = make_project(tmp_path, healthy=False)
        runner = CliRunner()
        runner.invoke(app, ["doctor", str(proj), "--fix"])
        script = proj / ".goalkit" / "scripts" / "bash" / "test.sh"
        assert script.stat().st_mode & stat.S_IXUSR


class TestDoctorDrift:
    def test_missing_templates_detected(self, tmp_path):
        proj = make_project(tmp_path, healthy=True)
        runner = CliRunner()
        result = runner.invoke(app, ["doctor", str(proj)])
        assert result.exit_code == 1
        assert "missing" in result.output.lower()

    def test_fix_restores_missing_templates(self, tmp_path):
        proj = make_project(tmp_path, healthy=True)
        runner = CliRunner()
        runner.invoke(app, ["doctor", str(proj), "--fix"])
        assert (proj / ".goalkit" / "templates" / "goal-template.md").is_file()
        assert (proj / ".goalkit" / "workflows").is_dir()

    def test_drifted_template_reported_not_overwritten(self, tmp_path):
        proj = make_project(tmp_path, healthy=True)
        drifted = proj / ".goalkit" / "templates" / "goal-template.md"
        drifted.write_text("# Customized by user\n")
        runner = CliRunner()
        result = runner.invoke(app, ["doctor", str(proj), "--fix"])
        assert "drifted" in result.output.lower()
        # --fix must never overwrite customized templates
        assert drifted.read_text() == "# Customized by user\n"
