"""Tests for execution tracker module."""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta

from goalkeeper_cli.execution import ExecutionTracker, MilestoneRecord, ExecutionStats
from goalkeeper_cli.models import Goal


@pytest.fixture
def temp_project():
    """Create a temporary goal-kit project."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        goalkit_dir = project_path / ".goalkit"
        milestones_dir = goalkit_dir / "milestones"
        goalkit_dir.mkdir(parents=True, exist_ok=True)
        milestones_dir.mkdir(parents=True, exist_ok=True)

        yield project_path


class TestExecutionTracker:
    """Tests for ExecutionTracker class."""

    def test_tracker_init_valid_project(self, temp_project):
        """Test initializing tracker with valid project."""
        tracker = ExecutionTracker(temp_project)
        assert tracker.project_path == temp_project
        assert tracker.goalkit_dir == temp_project / ".goalkit"
        assert tracker.milestones_dir == temp_project / ".goalkit" / "milestones"

    def test_tracker_init_missing_project_path(self):
        """Test initializing tracker with non-existent path."""
        with pytest.raises(FileNotFoundError):
            ExecutionTracker(Path("/nonexistent/project"))

    def test_tracker_init_missing_goalkit(self, temp_project):
        """Test initializing tracker without .goalkit directory."""
        import shutil

        goalkit_dir = temp_project / ".goalkit"
        if goalkit_dir.exists():
            shutil.rmtree(goalkit_dir)

        with pytest.raises(FileNotFoundError):
            ExecutionTracker(temp_project)

    def test_track_milestone(self, temp_project):
        """Test tracking a milestone."""
        tracker = ExecutionTracker(temp_project)
        tracker.track_milestone("goal1", "milestone1", "Completed successfully")

        # Verify history file was created
        assert tracker.history_file.exists()

        # Verify record was saved
        history = tracker.get_milestone_history()
        assert len(history) == 1
        assert history[0].goal_id == "goal1"
        assert history[0].milestone_id == "milestone1"
        assert history[0].notes == "Completed successfully"

    def test_track_multiple_milestones(self, temp_project):
        """Test tracking multiple milestones."""
        tracker = ExecutionTracker(temp_project)

        tracker.track_milestone("goal1", "milestone1")
        tracker.track_milestone("goal1", "milestone2")
        tracker.track_milestone("goal2", "milestone1")

        history = tracker.get_milestone_history()
        assert len(history) == 3

    def test_get_milestone_history_filter_by_goal(self, temp_project):
        """Test filtering milestone history by goal."""
        tracker = ExecutionTracker(temp_project)

        tracker.track_milestone("goal1", "milestone1")
        tracker.track_milestone("goal1", "milestone2")
        tracker.track_milestone("goal2", "milestone1")

        goal1_history = tracker.get_milestone_history(goal_id="goal1")
        assert len(goal1_history) == 2
        assert all(r.goal_id == "goal1" for r in goal1_history)

        goal2_history = tracker.get_milestone_history(goal_id="goal2")
        assert len(goal2_history) == 1
        assert goal2_history[0].goal_id == "goal2"

    def test_get_milestone_history_limit(self, temp_project):
        """Test limiting milestone history results."""
        tracker = ExecutionTracker(temp_project)

        for i in range(20):
            tracker.track_milestone("goal1", f"milestone{i}")

        history = tracker.get_milestone_history(limit=5)
        assert len(history) == 5

    def test_get_milestone_history_empty(self, temp_project):
        """Test getting history from empty project."""
        tracker = ExecutionTracker(temp_project)
        history = tracker.get_milestone_history()
        assert len(history) == 0

    def test_milestone_history_ordering(self, temp_project):
        """Test that history is ordered by completion time (newest first)."""
        tracker = ExecutionTracker(temp_project)

        # Add milestones
        tracker.track_milestone("goal1", "milestone1")
        tracker.track_milestone("goal1", "milestone2")
        tracker.track_milestone("goal1", "milestone3")

        history = tracker.get_milestone_history()

        # Should be in reverse chronological order (newest first)
        for i in range(len(history) - 1):
            assert history[i].completed_at >= history[i + 1].completed_at

    def test_update_goal_progress(self, temp_project):
        """Test updating goal progress percentage."""
        tracker = ExecutionTracker(temp_project)

        # Should not raise error
        tracker.update_goal_progress("goal1", 50)
        tracker.update_goal_progress("goal1", 100)

    def test_update_goal_progress_clamped(self, temp_project):
        """Test that progress percentage is clamped to 0-100."""
        tracker = ExecutionTracker(temp_project)

        # These should not raise errors
        tracker.update_goal_progress("goal1", -10)  # Should clamp to 0
        tracker.update_goal_progress("goal1", 150)  # Should clamp to 100

    def test_get_execution_stats_empty_project(self, temp_project):
        """Test getting execution stats for empty project."""
        tracker = ExecutionTracker(temp_project)
        goals = []

        stats = tracker.get_execution_stats(goals, 0.0)

        assert stats.total_milestones == 0
        assert stats.completed_milestones == 0
        assert stats.completion_percent == 0.0
        assert stats.velocity_per_day == 0.0

    def test_get_execution_stats_with_milestones(self, temp_project):
        """Test getting execution stats with completed milestones."""
        tracker = ExecutionTracker(temp_project)
        goals = [
            Goal("g1", "Goal 1", "execute", 50, 3, True),
            Goal("g2", "Goal 2", "execute", 50, 2, False),
        ]

        tracker.track_milestone("g1", "m1")
        tracker.track_milestone("g1", "m2")

        stats = tracker.get_execution_stats(goals, 50.0)

        assert stats.total_milestones == 4  # 2 goals * 2 milestones
        assert stats.completed_milestones == 2
        assert stats.completion_percent == 50.0
        assert len(stats.recent_milestones) <= 3

    def test_milestone_record_creation(self):
        """Test creating a milestone record."""
        now = datetime.now()
        record = MilestoneRecord(
            milestone_id="m1",
            goal_id="g1",
            completed_at=now,
            notes="Test note",
        )

        assert record.milestone_id == "m1"
        assert record.goal_id == "g1"
        assert record.completed_at == now
        assert record.notes == "Test note"

    def test_calculate_velocity(self, temp_project):
        """Test calculating completion velocity."""
        tracker = ExecutionTracker(temp_project)

        # Create records with known time gaps
        now = datetime.now()
        for i in range(5):
            record = MilestoneRecord(
                milestone_id=f"m{i}",
                goal_id="g1",
                completed_at=now - timedelta(days=5 - i),
            )
            tracker._save_milestone_record(record)

        history = tracker.get_milestone_history()
        velocity = tracker._calculate_velocity(history)

        # Should have positive velocity
        assert velocity > 0

    def test_estimate_completion_with_velocity(self, temp_project):
        """Test estimating completion date."""
        tracker = ExecutionTracker(temp_project)

        total = 10
        completed = 5
        velocity = 1.0  # 1 milestone per day

        estimated = tracker._estimate_completion(total, completed, velocity)

        assert estimated is not None
        # Should estimate 5 days from now (5 remaining / 1 per day)
        days_diff = (estimated - datetime.now()).days
        assert 4 <= days_diff <= 6

    def test_estimate_completion_no_velocity(self, temp_project):
        """Test estimation with zero velocity."""
        tracker = ExecutionTracker(temp_project)

        estimated = tracker._estimate_completion(10, 5, 0.0)

        assert estimated is None

    def test_estimate_completion_already_done(self, temp_project):
        """Test estimation when project is already done."""
        tracker = ExecutionTracker(temp_project)

        estimated = tracker._estimate_completion(10, 10, 1.0)

        assert estimated is None

    def test_count_total_milestones(self, temp_project):
        """Test counting total milestones."""
        tracker = ExecutionTracker(temp_project)
        goals = [
            Goal("g1", "Goal 1", "execute", 50, 3, True),
            Goal("g2", "Goal 2", "execute", 50, 2, False),
            Goal("g3", "Goal 3", "execute", 50, 1, True),
        ]

        total = tracker._count_total_milestones(goals)
        assert total == 6  # 3 goals * 2 milestones each


class TestMilestoneRecord:
    """Tests for MilestoneRecord dataclass."""

    def test_record_creation(self):
        """Test creating a milestone record."""
        now = datetime.now()
        record = MilestoneRecord(
            milestone_id="m1",
            goal_id="g1",
            completed_at=now,
        )

        assert record.milestone_id == "m1"
        assert record.goal_id == "g1"
        assert record.completed_at == now
        assert record.notes is None

    def test_record_with_notes(self):
        """Test creating record with notes."""
        record = MilestoneRecord(
            milestone_id="m1",
            goal_id="g1",
            completed_at=datetime.now(),
            notes="Important milestone",
        )

        assert record.notes == "Important milestone"


class TestExecutionStats:
    """Tests for ExecutionStats dataclass."""

    def test_stats_creation(self):
        """Test creating execution stats."""
        stats = ExecutionStats(
            total_milestones=10,
            completed_milestones=5,
            completion_percent=50.0,
            velocity_per_day=1.5,
            estimated_completion=datetime.now() + timedelta(days=3),
        )

        assert stats.total_milestones == 10
        assert stats.completed_milestones == 5
        assert stats.completion_percent == 50.0
        assert stats.velocity_per_day == 1.5

    def test_stats_defaults(self):
        """Test stats default values."""
        stats = ExecutionStats(
            total_milestones=10,
            completed_milestones=5,
            completion_percent=50.0,
            velocity_per_day=1.0,
            estimated_completion=None,
        )

        assert stats.recent_milestones == []
        assert stats.milestone_by_goal == {}


class TestExecutionTrackerEnhanced:
    """Tests for enhanced ExecutionTracker methods."""

    @pytest.fixture
    def temp_project_with_history(self):
        """Create a project with execution history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            milestones_dir = goalkit_dir / "milestones"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            milestones_dir.mkdir(parents=True, exist_ok=True)

            tracker = ExecutionTracker(project_path)

            # Create history over 14 days
            now = datetime.now()
            for i in range(10):
                record = MilestoneRecord(
                    milestone_id=f"m{i}",
                    goal_id="goal1" if i < 6 else "goal2",
                    completed_at=now - timedelta(days=10 - i),
                    notes=f"Milestone {i}",
                )
                tracker._save_milestone_record(record)

            yield project_path, tracker

    def test_get_goal_execution_stats(self, temp_project_with_history):
        """Test getting execution stats for a specific goal."""
        _, tracker = temp_project_with_history

        stats = tracker.get_goal_execution_stats("goal1")

        assert stats["goal_id"] == "goal1"
        assert stats["completed_milestones"] == 6
        assert "recent_milestones" in stats
        assert "last_completion" in stats

    def test_get_goal_execution_stats_no_history(self, temp_project):
        """Test getting stats for goal with no history."""
        tracker = ExecutionTracker(temp_project)

        stats = tracker.get_goal_execution_stats("nonexistent")

        assert stats["completed_milestones"] == 0
        assert stats["recent_milestones"] == []
        assert stats["last_completion"] is None

    def test_get_completion_timeline(self, temp_project_with_history):
        """Test getting completion timeline."""
        _, tracker = temp_project_with_history

        timeline = tracker.get_completion_timeline(days=30)

        assert isinstance(timeline, dict)
        assert len(timeline) > 0
        # Each day should have at least one completion
        for count in timeline.values():
            assert count > 0

    def test_get_completion_timeline_empty(self, temp_project):
        """Test timeline for project with no completions."""
        tracker = ExecutionTracker(temp_project)

        timeline = tracker.get_completion_timeline()

        assert len(timeline) == 0

    def test_get_momentum_active(self, temp_project_with_history):
        """Test momentum calculation for active project."""
        _, tracker = temp_project_with_history

        momentum = tracker.get_momentum(days=14)

        assert 0 <= momentum <= 100
        assert isinstance(momentum, float)

    def test_get_momentum_inactive(self, temp_project):
        """Test momentum for project with no recent activity."""
        tracker = ExecutionTracker(temp_project)

        momentum = tracker.get_momentum(days=7)

        assert momentum == 0.0

    def test_get_momentum_high_velocity(self, temp_project):
        """Test momentum with high completion velocity."""
        tracker = ExecutionTracker(temp_project)

        # Create multiple completions in recent days
        now = datetime.now()
        for i in range(5):
            record = MilestoneRecord(
                milestone_id=f"m{i}",
                goal_id="goal1",
                completed_at=now - timedelta(days=1 - i / 10),
            )
            tracker._save_milestone_record(record)

        momentum = tracker.get_momentum(days=7)

        # Should have high momentum due to recent activity
        assert momentum > 50

    def test_multiple_goal_stats(self, temp_project_with_history):
        """Test that stats correctly separate goals."""
        _, tracker = temp_project_with_history

        goal1_stats = tracker.get_goal_execution_stats("goal1")
        goal2_stats = tracker.get_goal_execution_stats("goal2")

        assert goal1_stats["completed_milestones"] == 6
        assert goal2_stats["completed_milestones"] == 4
        assert goal1_stats["completed_milestones"] + goal2_stats["completed_milestones"] == 10

    def test_timeline_date_formatting(self, temp_project_with_history):
        """Test that timeline dates are properly formatted."""
        _, tracker = temp_project_with_history

        timeline = tracker.get_completion_timeline(days=30)

        # All keys should be YYYY-MM-DD format
        for date_key in timeline.keys():
            parts = date_key.split("-")
            assert len(parts) == 3
            assert len(parts[0]) == 4  # Year
            assert len(parts[1]) == 2  # Month
            assert len(parts[2]) == 2  # Day

    def test_recent_milestones_order(self, temp_project_with_history):
        """Test that recent milestones are in correct order."""
        _, tracker = temp_project_with_history

        stats = tracker.get_goal_execution_stats("goal1")
        recent = stats["recent_milestones"]

        # Should be in reverse chronological order (most recent first)
        for i in range(len(recent) - 1):
            time_i = datetime.fromisoformat(recent[i]["completed_at"])
            time_i1 = datetime.fromisoformat(recent[i + 1]["completed_at"])
            assert time_i >= time_i1
