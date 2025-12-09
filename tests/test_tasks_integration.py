"""Integration tests for task management system."""

import pytest
import json
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timedelta

from src.goalkeeper_cli.tasks import TaskTracker, TaskStats
from src.goalkeeper_cli.models import Task, TaskStatus
from src.goalkeeper_cli.commands.tasks import tasks_command


@pytest.fixture
def tmp_project(tmp_path):
    """Create a temporary project structure."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    (project_dir / ".goalkit").mkdir()
    return project_dir


class TestTaskManagementWorkflow:
    """Test complete task management workflows."""

    def test_create_update_complete_workflow(self, tmp_project):
        """Test complete task lifecycle: create -> update -> complete."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        # Create task
        task_id = tracker.create_task(
            goal_id, "Implement Feature", "Add new feature to product", 8.0
        )
        assert task_id is not None

        task = tracker.get_task(task_id)
        assert task.status == TaskStatus.TODO
        assert task.estimated_hours == 8.0

        # Update task to in progress
        tracker.update_task_status(task_id, TaskStatus.IN_PROGRESS)
        task = tracker.get_task(task_id)
        assert task.status == TaskStatus.IN_PROGRESS

        # Update estimated hours
        tracker.update_task(task_id, estimated_hours=6.0)
        task = tracker.get_task(task_id)
        assert task.estimated_hours == 6.0

        # Mark complete
        tracker.update_task_status(task_id, TaskStatus.COMPLETED)
        task = tracker.get_task(task_id)
        assert task.status == TaskStatus.COMPLETED
        assert task.completed_at is not None

    def test_multi_goal_task_management(self, tmp_project):
        """Test managing tasks across multiple goals."""
        tracker = TaskTracker(tmp_project)
        goal1 = str(uuid4())
        goal2 = str(uuid4())
        goal3 = str(uuid4())

        # Create tasks for each goal
        for goal, count in [(goal1, 3), (goal2, 2), (goal3, 4)]:
            for i in range(count):
                tracker.create_task(goal, f"Task {i+1}", f"Description {i+1}", 2.0)

        # Verify tasks per goal
        assert len(tracker.get_tasks_by_goal(goal1)) == 3
        assert len(tracker.get_tasks_by_goal(goal2)) == 2
        assert len(tracker.get_tasks_by_goal(goal3)) == 4
        assert len(tracker.get_all_tasks()) == 9

        # Get stats
        stats = tracker.get_task_stats()
        assert stats.total_tasks == 9
        assert stats.total_estimated_hours == 18.0
        assert stats.tasks_by_goal[goal1] == 3

    def test_task_filtering_and_aggregation(self, tmp_project):
        """Test filtering and aggregating tasks."""
        tracker = TaskTracker(tmp_project)
        goal1 = str(uuid4())
        goal2 = str(uuid4())

        # Create tasks with mixed statuses
        id1 = tracker.create_task(goal1, "Design", "Design phase", 3.0)
        id2 = tracker.create_task(goal1, "Development", "Dev phase", 8.0)
        id3 = tracker.create_task(goal1, "Testing", "Test phase", 5.0)
        id4 = tracker.create_task(goal2, "Documentation", "Docs", 4.0)
        id5 = tracker.create_task(goal2, "Review", "Review docs", 2.0)

        # Set statuses
        tracker.update_task_status(id1, TaskStatus.COMPLETED)
        tracker.update_task_status(id2, TaskStatus.IN_PROGRESS)
        tracker.update_task_status(id3, TaskStatus.TODO)
        tracker.update_task_status(id4, TaskStatus.COMPLETED)

        # Filter by status
        todo_tasks = tracker.get_tasks_by_status(TaskStatus.TODO)
        assert len(todo_tasks) == 2  # id3 and id5 are still TODO
        assert any(t.id == id3 for t in todo_tasks)
        assert any(t.id == id5 for t in todo_tasks)

        in_progress = tracker.get_tasks_by_status(TaskStatus.IN_PROGRESS)
        assert len(in_progress) == 1

        completed = tracker.get_tasks_by_status(TaskStatus.COMPLETED)
        assert len(completed) == 2

        # Verify stats
        stats = tracker.get_task_stats()
        assert stats.completed_hours == 7.0  # 3.0 + 4.0
        assert stats.in_progress_hours == 8.0
        assert stats.completion_percent == pytest.approx(40.0, 0.1)

    def test_task_persistence_across_sessions(self, tmp_project):
        """Test that tasks persist across multiple tracker instances."""
        # First session
        tracker1 = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        task_id1 = tracker1.create_task(goal_id, "Task 1", "Desc 1", 2.0)
        task_id2 = tracker1.create_task(goal_id, "Task 2", "Desc 2", 3.0)
        task_id3 = tracker1.create_task(goal_id, "Task 3", "Desc 3", 5.0)

        tracker1.update_task_status(task_id1, TaskStatus.COMPLETED)
        tracker1.update_task_status(task_id2, TaskStatus.IN_PROGRESS)

        # Second session
        tracker2 = TaskTracker(tmp_project)

        assert len(tracker2.get_all_tasks()) == 3
        assert tracker2.get_task(task_id1).status == TaskStatus.COMPLETED
        assert tracker2.get_task(task_id2).status == TaskStatus.IN_PROGRESS
        assert tracker2.get_task(task_id3).status == TaskStatus.TODO

        # Third session - modify and verify
        tracker2.update_task_status(task_id3, TaskStatus.IN_PROGRESS)

        tracker3 = TaskTracker(tmp_project)
        assert tracker3.get_task(task_id3).status == TaskStatus.IN_PROGRESS

    def test_bulk_task_operations(self, tmp_project):
        """Test operations on many tasks."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        # Create many tasks
        task_ids = []
        for i in range(20):
            task_id = tracker.create_task(
                goal_id, f"Task {i+1}", f"Description {i+1}", float(i + 1)
            )
            task_ids.append(task_id)

        # Verify creation
        assert len(tracker.get_all_tasks()) == 20
        stats = tracker.get_task_stats()
        assert stats.total_tasks == 20

        # Update half to completed
        for task_id in task_ids[:10]:
            tracker.update_task_status(task_id, TaskStatus.COMPLETED)

        stats = tracker.get_task_stats()
        assert stats.completed_tasks == 10
        assert stats.completion_percent == 50.0

        # Delete completed tasks
        for task_id in task_ids[:10]:
            tracker.delete_task(task_id)

        assert len(tracker.get_all_tasks()) == 10
        assert all(t.status != TaskStatus.COMPLETED for t in tracker.get_all_tasks())


class TestTaskStatisticsAccuracy:
    """Test accuracy of statistical calculations."""

    def test_completion_percentage_calculation(self, tmp_project):
        """Test completion percentage is calculated correctly."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        # Create 3 tasks
        id1 = tracker.create_task(goal_id, "Task 1", "Desc", 1.0)
        id2 = tracker.create_task(goal_id, "Task 2", "Desc", 1.0)
        id3 = tracker.create_task(goal_id, "Task 3", "Desc", 1.0)

        # Complete 1
        tracker.update_task_status(id1, TaskStatus.COMPLETED)
        stats = tracker.get_task_stats()
        assert stats.completion_percent == pytest.approx(33.33, 0.1)

        # Complete 2
        tracker.update_task_status(id2, TaskStatus.COMPLETED)
        stats = tracker.get_task_stats()
        assert stats.completion_percent == pytest.approx(66.67, 0.1)

        # Complete 3
        tracker.update_task_status(id3, TaskStatus.COMPLETED)
        stats = tracker.get_task_stats()
        assert stats.completion_percent == 100.0

    def test_hours_calculation(self, tmp_project):
        """Test hour calculations."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        id1 = tracker.create_task(goal_id, "Task 1", "Desc", 2.5)
        id2 = tracker.create_task(goal_id, "Task 2", "Desc", 3.5)
        id3 = tracker.create_task(goal_id, "Task 3", "Desc", 4.0)

        stats = tracker.get_task_stats()
        assert stats.total_estimated_hours == 10.0

        tracker.update_task_status(id1, TaskStatus.IN_PROGRESS)
        tracker.update_task_status(id2, TaskStatus.COMPLETED)

        stats = tracker.get_task_stats()
        assert stats.completed_hours == 3.5
        assert stats.in_progress_hours == 2.5

    def test_status_distribution(self, tmp_project):
        """Test status distribution is accurate."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        ids = [
            tracker.create_task(goal_id, f"Task {i}", "Desc", 1.0)
            for i in range(10)
        ]

        # Set different statuses
        for i, task_id in enumerate(ids):
            if i < 3:
                tracker.update_task_status(task_id, TaskStatus.COMPLETED)
            elif i < 6:
                tracker.update_task_status(task_id, TaskStatus.IN_PROGRESS)

        stats = tracker.get_task_stats()
        assert stats.completed_tasks == 3
        assert stats.in_progress_tasks == 3
        assert stats.todo_tasks == 4


class TestTaskDataIntegrity:
    """Test data integrity and edge cases."""

    def test_timestamp_accuracy(self, tmp_project):
        """Test that timestamps are accurate."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        before = datetime.now()
        task_id = tracker.create_task(goal_id, "Task", "Desc")
        after = datetime.now()

        task = tracker.get_task(task_id)
        assert before <= task.created_at <= after
        assert before <= task.updated_at <= after
        assert task.completed_at is None

        # Update status
        before = datetime.now()
        tracker.update_task_status(task_id, TaskStatus.COMPLETED)
        after = datetime.now()

        task = tracker.get_task(task_id)
        assert before <= task.completed_at <= after

    def test_task_isolation_by_goal(self, tmp_project):
        """Test that tasks in different goals don't interfere."""
        tracker = TaskTracker(tmp_project)
        goal1 = str(uuid4())
        goal2 = str(uuid4())

        id1 = tracker.create_task(goal1, "Task 1", "Desc")
        id2 = tracker.create_task(goal2, "Task 2", "Desc")

        tracker.update_task_status(id1, TaskStatus.COMPLETED)

        # Verify only goal1's task is completed
        assert tracker.get_task(id1).status == TaskStatus.COMPLETED
        assert tracker.get_task(id2).status == TaskStatus.TODO

        # Verify stats per goal
        stats1 = tracker.get_task_stats_by_goal(goal1)
        stats2 = tracker.get_task_stats_by_goal(goal2)

        assert stats1.completion_percent == 100.0
        assert stats2.completion_percent == 0.0

    def test_delete_and_recreate(self, tmp_project):
        """Test deleting and recreating tasks."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        id1 = tracker.create_task(goal_id, "Task", "Desc")
        assert len(tracker.get_all_tasks()) == 1

        tracker.delete_task(id1)
        assert len(tracker.get_all_tasks()) == 0

        id2 = tracker.create_task(goal_id, "Task", "Desc")
        assert len(tracker.get_all_tasks()) == 1
        assert id1 != id2

    def test_concurrent_goal_operations(self, tmp_project):
        """Test operations on multiple goals simultaneously."""
        tracker = TaskTracker(tmp_project)
        goals = [str(uuid4()) for _ in range(5)]

        # Create multiple tasks across goals
        all_ids = []
        for goal in goals:
            for i in range(3):
                task_id = tracker.create_task(goal, f"Task {i+1}", "Desc", 1.0)
                all_ids.append((goal, task_id))

        # Randomly update statuses
        for i, (goal, task_id) in enumerate(all_ids):
            if i % 3 == 0:
                tracker.update_task_status(task_id, TaskStatus.COMPLETED)
            elif i % 3 == 1:
                tracker.update_task_status(task_id, TaskStatus.IN_PROGRESS)

        # Verify stats are correct
        stats = tracker.get_task_stats()
        assert stats.total_tasks == 15

        # Verify individual goal stats
        for goal in goals:
            goal_stats = tracker.get_task_stats_by_goal(goal)
            assert goal_stats.total_tasks == 3


class TestTaskCommandIntegration:
    """Test integration between TaskTracker and command."""

    def test_command_with_complex_scenario(self, tmp_project, capsys):
        """Test command with complex multi-goal scenario."""
        tracker = TaskTracker(tmp_project)

        # Create realistic project
        goals = {
            "backend": str(uuid4()),
            "frontend": str(uuid4()),
            "devops": str(uuid4()),
        }

        # Backend tasks
        for task in ["API Design", "Database Setup", "Authentication"]:
            tracker.create_task(goals["backend"], task, f"{task} implementation", 5.0)

        # Frontend tasks
        for task in ["UI Design", "Component Library", "Integration"]:
            tracker.create_task(goals["frontend"], task, f"{task} implementation", 4.0)

        # DevOps tasks
        for task in ["CI/CD", "Monitoring", "Deployment"]:
            tracker.create_task(goals["devops"], task, f"{task} setup", 3.0)

        # Update some statuses
        all_tasks = tracker.get_all_tasks()
        for task in all_tasks[:4]:
            tracker.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        for task in all_tasks[:2]:
            tracker.update_task_status(task.id, TaskStatus.COMPLETED)

        # Run command and verify output
        tasks_command(str(tmp_project))
        captured = capsys.readouterr()

        assert "9" in captured.out  # 9 total tasks
        assert "Task Statistics" in captured.out

    def test_command_json_with_all_features(self, tmp_project, capsys):
        """Test JSON command with all features."""
        tracker = TaskTracker(tmp_project)
        goal_id = str(uuid4())

        # Create diverse tasks
        for i in range(5):
            tracker.create_task(goal_id, f"Task {i+1}", f"Desc {i+1}", float(i + 1))

        # Mix statuses
        tasks = tracker.get_all_tasks()
        tracker.update_task_status(tasks[0].id, TaskStatus.COMPLETED)
        tracker.update_task_status(tasks[1].id, TaskStatus.IN_PROGRESS)

        # Get JSON output
        tasks_command(str(tmp_project), json_output=True)
        captured = capsys.readouterr()

        data = json.loads(captured.out)

        # Verify complete JSON structure
        assert len(data["tasks"]) == 5
        assert data["statistics"]["completed_tasks"] == 1
        assert data["statistics"]["in_progress_tasks"] == 1
        assert data["statistics"]["todo_tasks"] == 3
        assert data["statistics"]["total_estimated_hours"] == 15.0
