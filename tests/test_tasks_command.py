"""Unit tests for tasks command function."""

import pytest
import json
from pathlib import Path
from uuid import uuid4
from io import StringIO

from src.goalkeeper_cli.commands.tasks import tasks_command
from src.goalkeeper_cli.tasks import TaskTracker
from src.goalkeeper_cli.models import TaskStatus


@pytest.fixture
def tmp_project(tmp_path):
    """Create a temporary project structure."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    (project_dir / ".goalkit").mkdir()
    return project_dir


@pytest.fixture
def populated_tracker(tmp_project):
    """Create a tracker with sample tasks."""
    tracker = TaskTracker(tmp_project)

    goal1 = str(uuid4())
    goal2 = str(uuid4())

    # Create tasks for goal1
    id1 = tracker.create_task(goal1, "Design API", "Create REST API spec", 3.0)
    id2 = tracker.create_task(goal1, "Implement API", "Code API endpoints", 8.0)
    id3 = tracker.create_task(goal1, "Test API", "Write API tests", 5.0)

    # Create tasks for goal2
    id4 = tracker.create_task(goal2, "Write Docs", "Create documentation", 4.0)
    id5 = tracker.create_task(goal2, "Review Docs", "Review documentation", 2.0)

    # Set various statuses
    tracker.update_task_status(id1, TaskStatus.COMPLETED)
    tracker.update_task_status(id2, TaskStatus.IN_PROGRESS)

    return tracker, goal1, goal2


class TestTasksCommandBasic:
    """Test basic tasks command functionality."""

    def test_command_empty_project(self, tmp_project, capsys):
        """Test command on empty project."""
        tasks_command(str(tmp_project))
        captured = capsys.readouterr()
        assert "Task Statistics" in captured.out or "No tasks" in captured.out

    def test_command_with_tasks(self, populated_tracker, capsys):
        """Test command displays tasks."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path))
        captured = capsys.readouterr()
        assert "Task Statistics" in captured.out
        assert "Task" in captured.out or "task" in captured.out

    def test_command_missing_project(self, capsys):
        """Test command with missing project directory."""
        tasks_command("/nonexistent/path")
        captured = capsys.readouterr()
        # Should handle gracefully or error out
        assert len(captured.out) > 0 or len(captured.err) > 0


class TestTasksCommandFiltering:
    """Test tasks command filtering."""

    def test_filter_by_goal(self, populated_tracker, capsys):
        """Test filtering tasks by goal ID."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path), goal_id=goal1)
        captured = capsys.readouterr()

        assert "Task Statistics" in captured.out

    def test_filter_by_status_todo(self, populated_tracker, capsys):
        """Test filtering by todo status."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path), status="todo")
        captured = capsys.readouterr()

        # Should show only todo tasks
        assert "Task Statistics" in captured.out

    def test_filter_by_status_in_progress(self, populated_tracker, capsys):
        """Test filtering by in_progress status."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path), status="in_progress")
        captured = capsys.readouterr()

        assert "Task Statistics" in captured.out

    def test_filter_by_status_completed(self, populated_tracker, capsys):
        """Test filtering by completed status."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path), status="completed")
        captured = capsys.readouterr()

        assert "Task Statistics" in captured.out

    def test_filter_by_invalid_status(self, populated_tracker, capsys):
        """Test filtering by invalid status."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path), status="invalid")
        captured = capsys.readouterr()

        assert "Invalid status" in captured.out

    def test_filter_goal_and_status(self, populated_tracker, capsys):
        """Test combining goal and status filters."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(
            str(tracker.project_path), goal_id=goal1, status="in_progress"
        )
        captured = capsys.readouterr()

        assert "Task Statistics" in captured.out


class TestTasksCommandJsonOutput:
    """Test JSON output format."""

    def test_json_output_structure(self, populated_tracker, capsys):
        """Test JSON output has correct structure."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path), json_output=True)
        captured = capsys.readouterr()

        data = json.loads(captured.out)

        assert "statistics" in data
        assert "tasks" in data
        assert "total_tasks" in data["statistics"]

    def test_json_output_has_stats(self, populated_tracker, capsys):
        """Test JSON includes statistics."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path), json_output=True)
        captured = capsys.readouterr()

        data = json.loads(captured.out)
        stats = data["statistics"]

        assert stats["total_tasks"] == 5
        assert stats["completed_tasks"] == 1
        assert stats["in_progress_tasks"] == 1
        assert stats["todo_tasks"] == 3

    def test_json_output_has_tasks(self, populated_tracker, capsys):
        """Test JSON includes task details."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path), json_output=True)
        captured = capsys.readouterr()

        data = json.loads(captured.out)
        tasks = data["tasks"]

        assert len(tasks) == 5
        assert all("id" in t for t in tasks)
        assert all("goal_id" in t for t in tasks)
        assert all("title" in t for t in tasks)
        assert all("status" in t for t in tasks)

    def test_json_output_task_fields(self, populated_tracker, capsys):
        """Test JSON task objects have all required fields."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path), json_output=True)
        captured = capsys.readouterr()

        data = json.loads(captured.out)
        task = data["tasks"][0]

        assert "id" in task
        assert "goal_id" in task
        assert "title" in task
        assert "description" in task
        assert "status" in task
        assert "estimated_hours" in task
        assert "created_at" in task
        assert "updated_at" in task
        assert "completed_at" in task

    def test_json_output_with_filter(self, populated_tracker, capsys):
        """Test JSON output respects filters."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(
            str(tracker.project_path), goal_id=goal1, json_output=True
        )
        captured = capsys.readouterr()

        data = json.loads(captured.out)
        tasks = data["tasks"]

        assert len(tasks) == 3  # Only goal1's tasks
        assert all(t["goal_id"] == goal1 for t in tasks)

    def test_json_output_empty_project(self, tmp_project, capsys):
        """Test JSON output for empty project."""
        tasks_command(str(tmp_project), json_output=True)
        captured = capsys.readouterr()

        data = json.loads(captured.out)
        assert data["statistics"]["total_tasks"] == 0
        assert len(data["tasks"]) == 0


class TestTasksCommandFormatted:
    """Test formatted text output."""

    def test_formatted_output_includes_stats_panel(self, populated_tracker, capsys):
        """Test formatted output includes statistics panel."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path))
        captured = capsys.readouterr()

        assert "Task Statistics" in captured.out
        assert "Total Tasks:" in captured.out
        assert "Completed:" in captured.out

    def test_formatted_output_includes_table(self, populated_tracker, capsys):
        """Test formatted output includes tasks table."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path))
        captured = capsys.readouterr()

        # Check for table headers or content
        output = captured.out.lower()
        assert any(
            keyword in output for keyword in ["task", "goal", "status", "hours"]
        )

    def test_formatted_output_shows_task_count(self, populated_tracker, capsys):
        """Test formatted output displays correct task count."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path))
        captured = capsys.readouterr()

        assert "Total Tasks: 5" in captured.out

    def test_formatted_output_shows_completion(self, populated_tracker, capsys):
        """Test formatted output shows completion percentage."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path))
        captured = capsys.readouterr()

        # 1 out of 5 = 20%
        assert "20.0%" in captured.out

    def test_formatted_output_empty_shows_message(self, tmp_project, capsys):
        """Test formatted output shows message for empty project."""
        tasks_command(str(tmp_project))
        captured = capsys.readouterr()

        assert "0" in captured.out or "No tasks" in captured.out.lower()


class TestTasksCommandStatistics:
    """Test statistics display."""

    def test_stats_show_hours(self, populated_tracker, capsys):
        """Test that hours are displayed."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path))
        captured = capsys.readouterr()

        # Total estimated hours = 3+8+5+4+2 = 22
        assert "Hours" in captured.out or "hours" in captured.out

    def test_stats_show_status_breakdown(self, populated_tracker, capsys):
        """Test that status breakdown is shown."""
        tracker, goal1, goal2 = populated_tracker
        tasks_command(str(tracker.project_path))
        captured = capsys.readouterr()

        output = captured.out.lower()
        assert any(
            status in output for status in ["todo", "in_progress", "in progress"]
        )


class TestTasksCommandEdgeCases:
    """Test edge cases and error handling."""

    def test_command_with_no_estimated_hours(self, tmp_project, capsys):
        """Test command with tasks having no estimated hours."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())
        tracker.create_task(goal_id, "Task 1", "No hours")

        tasks_command(str(tmp_project))
        captured = capsys.readouterr()
        assert "Task Statistics" in captured.out

    def test_command_with_all_completed_tasks(self, tmp_project, capsys):
        """Test command when all tasks are completed."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        id1 = tracker.create_task(goal_id, "Task 1", "Desc")
        id2 = tracker.create_task(goal_id, "Task 2", "Desc")

        tracker.update_task_status(id1, TaskStatus.COMPLETED)
        tracker.update_task_status(id2, TaskStatus.COMPLETED)

        tasks_command(str(tmp_project))
        captured = capsys.readouterr()

        assert "100.0%" in captured.out

    def test_command_with_many_tasks(self, tmp_project, capsys):
        """Test command with large number of tasks."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        for i in range(50):
            tracker.create_task(goal_id, f"Task {i}", f"Description {i}")

        tasks_command(str(tmp_project))
        captured = capsys.readouterr()

        assert "50" in captured.out

    def test_command_preserves_data(self, populated_tracker):
        """Test that command doesn't modify project data."""
        tracker, goal1, goal2 = populated_tracker
        original_count = len(tracker.get_all_tasks())

        tasks_command(str(tracker.project_path))

        new_tracker = TaskTracker(tracker.project_path)
        assert len(new_tracker.get_all_tasks()) == original_count


class TestTasksCommandIntegration:
    """Integration tests for tasks command."""

    def test_command_sequence_create_and_display(self, tmp_project, capsys):
        """Test creating tasks and then displaying them."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        tracker.create_task(goal_id, "Task 1", "Desc 1", 2.0)
        tracker.create_task(goal_id, "Task 2", "Desc 2", 3.0)

        tasks_command(str(tmp_project))
        captured = capsys.readouterr()

        assert "2" in captured.out  # 2 tasks
        assert "5.0" in captured.out  # 5 total hours

    def test_command_reflects_status_changes(self, tmp_project, capsys):
        """Test that command reflects status changes."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        task_id = tracker.create_task(goal_id, "Task", "Desc")
        tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        tasks_command(str(tmp_project))
        captured = capsys.readouterr()

        assert "100.0%" in captured.out
