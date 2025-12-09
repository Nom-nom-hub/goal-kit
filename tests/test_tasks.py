"""Unit tests for TaskTracker class."""

import pytest
from pathlib import Path
from datetime import datetime, timedelta
from uuid import uuid4

from src.goalkeeper_cli.tasks import TaskTracker, TaskStats
from src.goalkeeper_cli.models import Task, TaskStatus


@pytest.fixture
def tmp_project(tmp_path):
    """Create a temporary project structure."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    (project_dir / ".goalkit").mkdir()
    return project_dir


@pytest.fixture
def tracker(tmp_project):
    """Create a TaskTracker instance."""
    return TaskTracker(tmp_project)


class TestTaskTrackerInit:
    """Test TaskTracker initialization."""

    def test_init_creates_goalkit_dir(self, tmp_path):
        """Test that init creates .goalkit directory."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        tracker = TaskTracker(project_dir)
        # Create a task to force directory creation
        tracker.create_task(str(uuid4()), "Test", "Desc")
        assert (project_dir / ".goalkit").exists()

    def test_init_loads_existing_tasks(self, tmp_project):
        """Test that init loads existing tasks from file."""
        tracker1 = TaskTracker(tmp_project)
        goal_id = str(uuid4())
        tracker1.create_task(goal_id, "Test Task", "Description")

        tracker2 = TaskTracker(tmp_project)
        assert len(tracker2.tasks) == 1

    def test_init_handles_missing_file(self, tmp_project):
        """Test that init handles missing tasks file gracefully."""
        tracker = TaskTracker(tmp_project)
        assert len(tracker.tasks) == 0


class TestCreateTask:
    """Test task creation."""

    def test_create_task_basic(self, tracker):
        """Test creating a basic task."""
        goal_id = str(uuid4())
        task_id = tracker.create_task(goal_id, "Test Task", "Test Description")

        assert task_id in tracker.tasks
        task = tracker.tasks[task_id]
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.goal_id == goal_id
        assert task.status == TaskStatus.TODO

    def test_create_task_with_hours(self, tracker):
        """Test creating a task with estimated hours."""
        goal_id = str(uuid4())
        task_id = tracker.create_task(
            goal_id, "Task", "Description", estimated_hours=5.5
        )

        task = tracker.tasks[task_id]
        assert task.estimated_hours == 5.5

    def test_create_task_generates_unique_ids(self, tracker):
        """Test that created tasks have unique IDs."""
        goal_id = str(uuid4())
        id1 = tracker.create_task(goal_id, "Task 1", "Desc")
        id2 = tracker.create_task(goal_id, "Task 2", "Desc")

        assert id1 != id2

    def test_create_task_persists(self, tmp_project):
        """Test that created task persists to disk."""
        tracker1 = TaskTracker(tmp_project)
        goal_id = str(uuid4())
        task_id = tracker1.create_task(goal_id, "Task", "Desc", estimated_hours=3.0)

        tracker2 = TaskTracker(tmp_project)
        assert task_id in tracker2.tasks
        assert tracker2.tasks[task_id].title == "Task"

    def test_create_task_sets_timestamps(self, tracker):
        """Test that created task has correct timestamps."""
        goal_id = str(uuid4())
        before = datetime.now()
        task_id = tracker.create_task(goal_id, "Task", "Desc")
        after = datetime.now()

        task = tracker.tasks[task_id]
        assert before <= task.created_at <= after
        assert before <= task.updated_at <= after
        assert task.completed_at is None


class TestUpdateTaskStatus:
    """Test task status updates."""

    def test_update_status_todo_to_in_progress(self, tracker):
        """Test updating task from todo to in_progress."""
        goal_id = str(uuid4())
        task_id = tracker.create_task(goal_id, "Task", "Desc")

        result = tracker.update_task_status(task_id, TaskStatus.IN_PROGRESS)
        assert result is True
        assert tracker.tasks[task_id].status == TaskStatus.IN_PROGRESS

    def test_update_status_to_completed(self, tracker):
        """Test updating task to completed sets completion time."""
        goal_id = str(uuid4())
        task_id = tracker.create_task(goal_id, "Task", "Desc")

        before = datetime.now()
        tracker.update_task_status(task_id, TaskStatus.COMPLETED)
        after = datetime.now()

        task = tracker.tasks[task_id]
        assert task.status == TaskStatus.COMPLETED
        assert task.completed_at is not None
        assert before <= task.completed_at <= after

    def test_update_status_clears_completion_time(self, tracker):
        """Test that moving away from completed clears completion time."""
        goal_id = str(uuid4())
        task_id = tracker.create_task(goal_id, "Task", "Desc")

        tracker.update_task_status(task_id, TaskStatus.COMPLETED)
        tracker.update_task_status(task_id, TaskStatus.TODO)

        task = tracker.tasks[task_id]
        assert task.status == TaskStatus.TODO
        assert task.completed_at is None

    def test_update_status_nonexistent_task(self, tracker):
        """Test updating nonexistent task returns False."""
        result = tracker.update_task_status("nonexistent", TaskStatus.COMPLETED)
        assert result is False

    def test_update_status_persists(self, tmp_project):
        """Test that status update persists to disk."""
        tracker1 = TaskTracker(tmp_project)
        goal_id = str(uuid4())
        task_id = tracker1.create_task(goal_id, "Task", "Desc")

        tracker1.update_task_status(task_id, TaskStatus.IN_PROGRESS)

        tracker2 = TaskTracker(tmp_project)
        assert tracker2.tasks[task_id].status == TaskStatus.IN_PROGRESS


class TestUpdateTask:
    """Test task detail updates."""

    def test_update_title(self, tracker):
        """Test updating task title."""
        goal_id = str(uuid4())
        task_id = tracker.create_task(goal_id, "Old Title", "Desc")

        result = tracker.update_task(task_id, title="New Title")
        assert result is True
        assert tracker.tasks[task_id].title == "New Title"

    def test_update_description(self, tracker):
        """Test updating task description."""
        goal_id = str(uuid4())
        task_id = tracker.create_task(goal_id, "Task", "Old Desc")

        tracker.update_task(task_id, description="New Desc")
        assert tracker.tasks[task_id].description == "New Desc"

    def test_update_estimated_hours(self, tracker):
        """Test updating estimated hours."""
        goal_id = str(uuid4())
        task_id = tracker.create_task(goal_id, "Task", "Desc", estimated_hours=2.0)

        tracker.update_task(task_id, estimated_hours=5.0)
        assert tracker.tasks[task_id].estimated_hours == 5.0

    def test_update_multiple_fields(self, tracker):
        """Test updating multiple fields at once."""
        goal_id = str(uuid4())
        task_id = tracker.create_task(goal_id, "Task", "Desc")

        tracker.update_task(
            task_id, title="New Title", description="New Desc", estimated_hours=3.0
        )

        task = tracker.tasks[task_id]
        assert task.title == "New Title"
        assert task.description == "New Desc"
        assert task.estimated_hours == 3.0

    def test_update_nonexistent_task(self, tracker):
        """Test updating nonexistent task returns False."""
        result = tracker.update_task("nonexistent", title="New")
        assert result is False

    def test_update_sets_updated_at(self, tracker):
        """Test that update sets updated_at timestamp."""
        goal_id = str(uuid4())
        task_id = tracker.create_task(goal_id, "Task", "Desc")
        original_time = tracker.tasks[task_id].updated_at

        import time

        time.sleep(0.01)  # Ensure time difference
        tracker.update_task(task_id, title="New")

        assert tracker.tasks[task_id].updated_at > original_time


class TestGetTask:
    """Test task retrieval."""

    def test_get_task(self, tracker):
        """Test getting a task by ID."""
        goal_id = str(uuid4())
        task_id = tracker.create_task(goal_id, "Task", "Desc")

        task = tracker.get_task(task_id)
        assert task is not None
        assert task.title == "Task"

    def test_get_nonexistent_task(self, tracker):
        """Test getting nonexistent task returns None."""
        task = tracker.get_task("nonexistent")
        assert task is None


class TestGetTasksByGoal:
    """Test filtering tasks by goal."""

    def test_get_tasks_by_goal(self, tracker):
        """Test getting all tasks for a goal."""
        goal1 = str(uuid4())
        goal2 = str(uuid4())

        tracker.create_task(goal1, "Task 1", "Desc")
        tracker.create_task(goal1, "Task 2", "Desc")
        tracker.create_task(goal2, "Task 3", "Desc")

        tasks = tracker.get_tasks_by_goal(goal1)
        assert len(tasks) == 2
        assert all(t.goal_id == goal1 for t in tasks)

    def test_get_tasks_by_goal_empty(self, tracker):
        """Test getting tasks for goal with no tasks."""
        tasks = tracker.get_tasks_by_goal(str(uuid4()))
        assert len(tasks) == 0


class TestGetTasksByStatus:
    """Test filtering tasks by status."""

    def test_get_tasks_by_status(self, tracker):
        """Test filtering tasks by status."""
        goal_id = str(uuid4())

        id1 = tracker.create_task(goal_id, "Task 1", "Desc")
        id2 = tracker.create_task(goal_id, "Task 2", "Desc")
        id3 = tracker.create_task(goal_id, "Task 3", "Desc")

        tracker.update_task_status(id1, TaskStatus.IN_PROGRESS)
        tracker.update_task_status(id2, TaskStatus.COMPLETED)

        todo_tasks = tracker.get_tasks_by_status(TaskStatus.TODO)
        assert len(todo_tasks) == 1
        assert todo_tasks[0].id == id3

        in_progress = tracker.get_tasks_by_status(TaskStatus.IN_PROGRESS)
        assert len(in_progress) == 1
        assert in_progress[0].id == id1

        completed = tracker.get_tasks_by_status(TaskStatus.COMPLETED)
        assert len(completed) == 1
        assert completed[0].id == id2


class TestGetAllTasks:
    """Test getting all tasks."""

    def test_get_all_tasks(self, tracker):
        """Test getting all tasks."""
        goal_id = str(uuid4())
        tracker.create_task(goal_id, "Task 1", "Desc")
        tracker.create_task(goal_id, "Task 2", "Desc")

        tasks = tracker.get_all_tasks()
        assert len(tasks) == 2

    def test_get_all_tasks_empty(self, tracker):
        """Test getting all tasks when none exist."""
        tasks = tracker.get_all_tasks()
        assert len(tasks) == 0


class TestDeleteTask:
    """Test task deletion."""

    def test_delete_task(self, tracker):
        """Test deleting a task."""
        goal_id = str(uuid4())
        task_id = tracker.create_task(goal_id, "Task", "Desc")

        result = tracker.delete_task(task_id)
        assert result is True
        assert task_id not in tracker.tasks

    def test_delete_nonexistent_task(self, tracker):
        """Test deleting nonexistent task returns False."""
        result = tracker.delete_task("nonexistent")
        assert result is False

    def test_delete_task_persists(self, tmp_project):
        """Test that deletion persists to disk."""
        tracker1 = TaskTracker(tmp_project)
        goal_id = str(uuid4())
        task_id = tracker1.create_task(goal_id, "Task", "Desc")

        tracker1.delete_task(task_id)

        tracker2 = TaskTracker(tmp_project)
        assert task_id not in tracker2.tasks


class TestTaskStats:
    """Test task statistics calculation."""

    def test_stats_empty_project(self, tracker):
        """Test stats for empty project."""
        stats = tracker.get_task_stats()

        assert stats.total_tasks == 0
        assert stats.completed_tasks == 0
        assert stats.in_progress_tasks == 0
        assert stats.todo_tasks == 0
        assert stats.completion_percent == 0.0
        assert stats.total_estimated_hours == 0.0

    def test_stats_with_tasks(self, tracker):
        """Test stats calculation with mixed task states."""
        goal1 = str(uuid4())
        goal2 = str(uuid4())

        id1 = tracker.create_task(goal1, "Task 1", "Desc", estimated_hours=2.0)
        id2 = tracker.create_task(goal1, "Task 2", "Desc", estimated_hours=3.0)
        id3 = tracker.create_task(goal2, "Task 3", "Desc", estimated_hours=5.0)

        tracker.update_task_status(id1, TaskStatus.COMPLETED)
        tracker.update_task_status(id2, TaskStatus.IN_PROGRESS)

        stats = tracker.get_task_stats()

        assert stats.total_tasks == 3
        assert stats.completed_tasks == 1
        assert stats.in_progress_tasks == 1
        assert stats.todo_tasks == 1
        assert stats.completion_percent == pytest.approx(33.33, 0.1)
        assert stats.total_estimated_hours == 10.0
        assert stats.completed_hours == 2.0
        assert stats.in_progress_hours == 3.0

    def test_stats_by_goal(self, tracker):
        """Test stats breakdown by goal."""
        goal1 = str(uuid4())
        goal2 = str(uuid4())

        tracker.create_task(goal1, "Task 1", "Desc")
        tracker.create_task(goal1, "Task 2", "Desc")
        tracker.create_task(goal2, "Task 3", "Desc")

        stats = tracker.get_task_stats()

        assert stats.tasks_by_goal[goal1] == 2
        assert stats.tasks_by_goal[goal2] == 1

    def test_stats_by_status(self, tracker):
        """Test stats breakdown by status."""
        goal_id = str(uuid4())

        id1 = tracker.create_task(goal_id, "Task 1", "Desc")
        id2 = tracker.create_task(goal_id, "Task 2", "Desc")
        id3 = tracker.create_task(goal_id, "Task 3", "Desc")

        tracker.update_task_status(id1, TaskStatus.IN_PROGRESS)
        tracker.update_task_status(id2, TaskStatus.COMPLETED)

        stats = tracker.get_task_stats()

        assert stats.tasks_by_status["todo"] == 1
        assert stats.tasks_by_status["in_progress"] == 1
        assert stats.tasks_by_status["completed"] == 1

    def test_stats_by_goal_single_goal(self, tracker):
        """Test stats for single goal."""
        goal_id = str(uuid4())

        id1 = tracker.create_task(goal_id, "Task 1", "Desc", estimated_hours=2.0)
        id2 = tracker.create_task(goal_id, "Task 2", "Desc", estimated_hours=3.0)

        tracker.update_task_status(id1, TaskStatus.COMPLETED)

        stats = tracker.get_task_stats_by_goal(goal_id)

        assert stats.total_tasks == 2
        assert stats.completed_tasks == 1
        assert stats.total_estimated_hours == 5.0
        assert stats.completed_hours == 2.0
        assert stats.completion_percent == 50.0


class TestTaskPersistence:
    """Test JSON persistence."""

    def test_persistence_round_trip(self, tmp_project):
        """Test that tasks survive a load/save cycle."""
        tracker1 = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        id1 = tracker1.create_task(goal_id, "Task 1", "Desc 1", estimated_hours=2.5)
        id2 = tracker1.create_task(goal_id, "Task 2", "Desc 2", estimated_hours=3.5)

        tracker1.update_task_status(id1, TaskStatus.IN_PROGRESS)
        tracker1.update_task_status(id2, TaskStatus.COMPLETED)

        tracker2 = TaskTracker(tmp_project)

        assert len(tracker2.tasks) == 2
        assert tracker2.tasks[id1].status == TaskStatus.IN_PROGRESS
        assert tracker2.tasks[id2].status == TaskStatus.COMPLETED
        assert tracker2.tasks[id1].estimated_hours == 2.5
        assert tracker2.tasks[id2].completed_at is not None

    def test_persistence_corrupted_file(self, tmp_project):
        """Test handling of corrupted JSON file."""
        tasks_file = tmp_project / ".goalkit" / "tasks.json"
        tasks_file.write_text("invalid json {")

        tracker = TaskTracker(tmp_project)
        assert len(tracker.tasks) == 0

    def test_persistence_missing_fields(self, tmp_project):
        """Test handling of missing fields in saved task."""
        tasks_file = tmp_project / ".goalkit" / "tasks.json"
        import json

        invalid_data = {"task1": {"id": "task1", "goal_id": "goal1"}}
        tasks_file.write_text(json.dumps(invalid_data))

        tracker = TaskTracker(tmp_project)
        assert len(tracker.tasks) == 0
