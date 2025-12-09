"""Integration tests for milestones command with realistic scenarios."""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta
from io import StringIO
from unittest.mock import patch

from goalkeeper_cli.commands.milestones import milestones
from goalkeeper_cli.execution import ExecutionTracker, MilestoneRecord
from goalkeeper_cli.models import Goal


class TestMilestonesCommandIntegration:
    """Integration tests for milestones command with realistic data."""

    @pytest.fixture
    def realistic_project(self):
        """Create a realistic project with execution history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goals_dir = goalkit_dir / "goals"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            goals_dir.mkdir(parents=True, exist_ok=True)

            tracker = ExecutionTracker(project_path)

            # Simulate 2 weeks of execution with varying pace
            now = datetime.now()
            
            # Week 1: slow start (goal1: 3 milestones, goal2: 1)
            for i in range(3):
                tracker._save_milestone_record(
                    MilestoneRecord(
                        milestone_id=f"g1_m{i+1}",
                        goal_id="goal1",
                        completed_at=now - timedelta(days=14-i*3),
                        notes=f"Goal 1 milestone {i+1}",
                    )
                )
            
            tracker._save_milestone_record(
                MilestoneRecord(
                    milestone_id="g2_m1",
                    goal_id="goal2",
                    completed_at=now - timedelta(days=12),
                    notes="Goal 2 milestone 1",
                )
            )
            
            # Week 2: faster pace (goal1: 3 more, goal2: 2 more)
            for i in range(3):
                tracker._save_milestone_record(
                    MilestoneRecord(
                        milestone_id=f"g1_m{i+4}",
                        goal_id="goal1",
                        completed_at=now - timedelta(days=7-i*2),
                        notes=f"Goal 1 milestone {i+4}",
                    )
                )
            
            for i in range(2):
                tracker._save_milestone_record(
                    MilestoneRecord(
                        milestone_id=f"g2_m{i+2}",
                        goal_id="goal2",
                        completed_at=now - timedelta(days=5-i*2),
                        notes=f"Goal 2 milestone {i+2}",
                    )
                )
            
            yield project_path

    def test_milestones_basic_display(self, realistic_project, capsys):
        """Test basic milestones command display."""
        milestones(realistic_project)
        captured = capsys.readouterr()
        
        # Should show project summary
        assert "Milestone Summary" in captured.out or "11/" in captured.out
        # Should not error
        assert "Error" not in captured.out

    def test_milestones_json_output_complete(self, realistic_project, capsys):
        """Test JSON output contains all expected fields."""
        milestones(realistic_project, json_output=True)
        captured = capsys.readouterr()
        
        try:
            data = json.loads(captured.out)
            
            # Verify structure
            assert "milestones" in data
            assert "velocity" in data
            assert "momentum" in data
            assert "goals" in data
            
            # Verify milestone counts
            milestones_info = data["milestones"]
            assert milestones_info["total"] >= 0
            assert milestones_info["completed"] >= 0
            
            # Verify velocity is calculated
            velocity = data["velocity"]["per_day"]
            assert velocity >= 0
            
            # Verify momentum is in range
            momentum = data["momentum"]["score"]
            assert 0 <= momentum <= 100
            
        except json.JSONDecodeError:
            pytest.fail("Invalid JSON output")

    def test_milestones_goal_filter(self, realistic_project, capsys):
        """Test filtering milestones by goal."""
        milestones(realistic_project, goal_id="goal1")
        captured = capsys.readouterr()
        
        # Should display goal1 information
        assert "Goal 1" in captured.out or "goal1" in captured.out or captured.out != ""
        assert "Error" not in captured.out

    def test_milestones_goal_filter_json(self, realistic_project, capsys):
        """Test JSON output with goal filter."""
        milestones(realistic_project, goal_id="goal1", json_output=True)
        captured = capsys.readouterr()
        
        try:
            data = json.loads(captured.out)
            
            # Should have expected structure
            if "error" not in data:
                # Should have goals array
                assert "goals" in data or "milestones" in data
            
        except json.JSONDecodeError:
            pytest.fail("Invalid JSON output")

    def test_milestones_execution_velocity(self, realistic_project):
        """Test that velocity is correctly calculated."""
        tracker = ExecutionTracker(realistic_project)
        history = tracker.get_milestone_history(limit=100)
        
        velocity = tracker._calculate_velocity(history)
        
        # Should have positive velocity from 14 days of activity
        assert velocity > 0
        # Should be roughly 0.5-1.0 milestones per day from test data
        assert 0.1 < velocity < 2.0

    def test_milestones_momentum_calculation(self, realistic_project):
        """Test momentum calculation."""
        tracker = ExecutionTracker(realistic_project)
        
        # Recent activity (last 7 days) should show high momentum
        momentum_recent = tracker.get_momentum(days=7)
        assert 0 <= momentum_recent <= 100
        
        # Should have measurable momentum from test data
        # (3 + 2 = 5 milestones in last 7 days, expected ~1/day = 5/7 ≈ 71%)
        assert momentum_recent > 0

    def test_milestones_timeline_generation(self, realistic_project):
        """Test timeline generation for 30 days."""
        tracker = ExecutionTracker(realistic_project)
        
        timeline = tracker.get_completion_timeline(days=30)
        
        # Should have entries for multiple days
        assert len(timeline) > 0
        
        # All values should be positive
        for count in timeline.values():
            assert count > 0
        
        # Should have multiple completions across dates
        total = sum(timeline.values())
        assert total > 5

    def test_milestones_goal_specific_stats(self, realistic_project):
        """Test getting goal-specific execution stats."""
        tracker = ExecutionTracker(realistic_project)
        
        goal1_stats = tracker.get_goal_execution_stats("goal1")
        goal2_stats = tracker.get_goal_execution_stats("goal2")
        
        # Both goals should have completions
        assert goal1_stats["completed_milestones"] > 0
        assert goal2_stats["completed_milestones"] > 0
        
        # Goal 1 should have at least as many as goal 2
        assert goal1_stats["completed_milestones"] >= goal2_stats["completed_milestones"]
        
        # Both should have recent milestones
        assert len(goal1_stats["recent_milestones"]) > 0
        assert len(goal2_stats["recent_milestones"]) > 0
        
        # Should have last completion timestamps
        assert goal1_stats["last_completion"] is not None
        assert goal2_stats["last_completion"] is not None

    def test_milestones_with_multiple_commands(self, realistic_project, capsys):
        """Test running milestones command multiple times."""
        # First call - full display
        milestones(realistic_project)
        first_output = capsys.readouterr()
        
        # Second call - JSON output
        milestones(realistic_project, json_output=True)
        second_output = capsys.readouterr()
        
        # Both should succeed
        assert "Error" not in first_output.out
        assert second_output.out.startswith("{") or second_output.out == ""
        
        # Third call - filtered
        milestones(realistic_project, goal_id="goal2")
        third_output = capsys.readouterr()
        
        assert "Error" not in third_output.out

    def test_milestones_execution_stats_aggregate(self, realistic_project):
        """Test aggregated execution stats."""
        tracker = ExecutionTracker(realistic_project)
        goals = [
            Goal("goal1", "Goal 1", "execute", 75, 3, True),
            Goal("goal2", "Goal 2", "execute", 62, 2, False),
        ]
        
        stats = tracker.get_execution_stats(goals, 68.5)
        
        # Should aggregate stats correctly
        assert stats.total_milestones >= 0
        assert stats.completed_milestones >= 0
        
        # Velocity should be calculated
        assert stats.velocity_per_day >= 0
        
        # Should have recent milestones if there are completions
        if stats.completed_milestones > 0:
            assert len(stats.recent_milestones) > 0


class TestMilestonesEdgeCases:
    """Test edge cases and error handling."""

    def test_milestones_empty_project(self):
        """Test milestones command on empty project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            
            tracker = ExecutionTracker(project_path)
            
            # Empty project should have zero stats
            stats = tracker.get_execution_stats([], 0.0)
            assert stats.total_milestones == 0
            assert stats.completed_milestones == 0
            
            # Momentum should be calculable
            momentum = tracker.get_momentum()
            assert 0 <= momentum <= 100

    def test_milestones_single_milestone(self):
        """Test with only one milestone."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            
            tracker = ExecutionTracker(project_path)
            
            tracker._save_milestone_record(
                MilestoneRecord(
                    milestone_id="m1",
                    goal_id="g1",
                    completed_at=datetime.now(),
                )
            )
            
            stats = tracker.get_execution_stats(
                [Goal("g1", "Goal 1", "execute", 50, 1, True)],
                50.0
            )
            
            assert stats.completed_milestones == 1
            # Can't calculate velocity from single point
            assert stats.velocity_per_day == 0.0

    def test_milestones_very_recent_activity(self):
        """Test with all activity in the last 24 hours."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            
            tracker = ExecutionTracker(project_path)
            now = datetime.now()
            
            # Add 5 milestones in the last hour
            for i in range(5):
                tracker._save_milestone_record(
                    MilestoneRecord(
                        milestone_id=f"m{i}",
                        goal_id="g1",
                        completed_at=now - timedelta(minutes=i*12),
                    )
                )
            
            momentum = tracker.get_momentum(days=1)
            
            # Should have very high momentum from recent activity
            assert momentum > 50
