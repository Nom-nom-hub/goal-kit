"""Tests for models module."""

import pytest
from datetime import datetime
from pathlib import Path
from goalkeeper_cli.models import Project, Goal, Milestone, Task, TemplateMetadata


class TestProject:
    """Tests for Project model."""

    def test_project_creation(self):
        """Test creating a project."""
        now = datetime.now()
        proj = Project(
            name="test-project",
            path=Path("/tmp/test-project"),
            agent="claude",
            created_at=now,
        )
        assert proj.name == "test-project"
        assert proj.path == Path("/tmp/test-project")
        assert proj.agent == "claude"
        assert proj.created_at == now

    def test_project_with_health_score(self):
        """Test project with health score."""
        now = datetime.now()
        proj = Project(
            name="test",
            path=Path("/tmp/test"),
            agent="copilot",
            created_at=now,
            health_score=85.5,
        )
        assert proj.health_score == 85.5

    def test_project_health_score_optional(self):
        """Test project health score is optional."""
        now = datetime.now()
        proj = Project(
            name="test",
            path=Path("/tmp/test"),
            agent="claude",
            created_at=now,
        )
        assert proj.health_score is None


class TestGoal:
    """Tests for Goal model."""

    def test_goal_creation(self):
        """Test creating a goal."""
        goal = Goal(
            id="goal-001",
            name="Complete authentication",
            phase="execute",
            completion_percent=50,
            success_criteria_count=3,
            metrics_defined=True,
        )
        assert goal.id == "goal-001"
        assert goal.name == "Complete authentication"
        assert goal.phase == "execute"
        assert goal.completion_percent == 50
        assert goal.success_criteria_count == 3
        assert goal.metrics_defined is True

    def test_goal_phases(self):
        """Test goal with different phases."""
        phases = ["vision", "goal", "strategies", "milestones", "execute", "done"]
        for phase in phases:
            goal = Goal(
                id=f"goal-{phase}",
                name="Test",
                phase=phase,
                completion_percent=0,
                success_criteria_count=1,
                metrics_defined=False,
            )
            assert goal.phase == phase

    def test_goal_completion_percent(self):
        """Test goal completion percentage ranges."""
        for percent in [0, 25, 50, 75, 100]:
            goal = Goal(
                id="goal",
                name="Test",
                phase="execute",
                completion_percent=percent,
                success_criteria_count=1,
                metrics_defined=False,
            )
            assert goal.completion_percent == percent


class TestMilestone:
    """Tests for Milestone model."""

    def test_milestone_creation(self):
        """Test creating a milestone."""
        milestone = Milestone(
            id="m1",
            name="Phase 1: Setup",
            description="Initial project setup",
            completed=False,
        )
        assert milestone.id == "m1"
        assert milestone.name == "Phase 1: Setup"
        assert milestone.description == "Initial project setup"
        assert milestone.completed is False

    def test_milestone_with_due_date(self):
        """Test milestone with due date."""
        due = datetime(2025, 12, 31)
        milestone = Milestone(
            id="m1",
            name="Phase 1",
            description="Setup",
            completed=False,
            due_date=due,
        )
        assert milestone.due_date == due

    def test_milestone_completed(self):
        """Test completed milestone."""
        milestone = Milestone(
            id="m1",
            name="Phase 1",
            description="Setup",
            completed=True,
        )
        assert milestone.completed is True


class TestTask:
    """Tests for Task model."""

    def test_task_creation(self):
        """Test creating a task."""
        task = Task(
            id="t1",
            title="Implement login",
            description="Add user authentication",
            milestone_id="m1",
            completed=False,
        )
        assert task.id == "t1"
        assert task.title == "Implement login"
        assert task.description == "Add user authentication"
        assert task.milestone_id == "m1"
        assert task.completed is False

    def test_task_with_priority(self):
        """Test task with priority."""
        for priority in ["low", "medium", "high"]:
            task = Task(
                id="t1",
                title="Test",
                description="Description",
                milestone_id="m1",
                completed=False,
                priority=priority,
            )
            assert task.priority == priority

    def test_task_with_assignment(self):
        """Test task assigned to someone."""
        task = Task(
            id="t1",
            title="Test",
            description="Description",
            milestone_id="m1",
            completed=False,
            assigned_to="alice",
        )
        assert task.assigned_to == "alice"

    def test_task_with_due_date(self):
        """Test task with due date."""
        due = datetime(2025, 12, 25)
        task = Task(
            id="t1",
            title="Test",
            description="Description",
            milestone_id="m1",
            completed=False,
            due_date=due,
        )
        assert task.due_date == due


class TestTemplateMetadata:
    """Tests for TemplateMetadata model."""

    def test_metadata_creation(self):
        """Test creating template metadata."""
        meta = TemplateMetadata(
            filename="goal-kit-template-claude-sh.zip",
            size=1024000,
            release="v1.0.0",
            asset_url="https://github.com/Nom-nom-hub/goal-kit/releases/download/v1.0.0/goal-kit-template-claude-sh.zip",
        )
        assert meta.filename == "goal-kit-template-claude-sh.zip"
        assert meta.size == 1024000
        assert meta.release == "v1.0.0"
        assert "v1.0.0" in meta.asset_url

    def test_metadata_attributes(self):
        """Test all metadata attributes."""
        meta = TemplateMetadata(
            filename="template.zip",
            size=2048,
            release="v2.0.0",
            asset_url="https://example.com/template.zip",
        )
        assert hasattr(meta, "filename")
        assert hasattr(meta, "size")
        assert hasattr(meta, "release")
        assert hasattr(meta, "asset_url")
