"""Execution tracking and milestone management for Goalkeeper projects.

This module provides execution tracking capabilities including milestone
completion, progress updates, and execution velocity metrics.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
from datetime import datetime, timedelta

from .models import Project, Goal, Milestone, Task


@dataclass
class MilestoneRecord:
    """Record of a completed milestone."""

    milestone_id: str
    goal_id: str
    completed_at: datetime
    notes: Optional[str] = None


@dataclass
class ExecutionStats:
    """Execution statistics for a project."""

    total_milestones: int
    completed_milestones: int
    completion_percent: float
    velocity_per_day: float
    estimated_completion: Optional[datetime]
    recent_milestones: List[MilestoneRecord] = field(default_factory=list)
    milestone_by_goal: Dict[str, int] = field(default_factory=dict)


class ExecutionTracker:
    """Track goal execution progress and milestone completion.
    
    Provides methods to:
    - Track milestone completion
    - Update goal progress
    - Calculate execution velocity
    - Estimate project completion date
    - Retrieve execution history
    """

    def __init__(self, project_path: Path):
        """Initialize execution tracker for a goal-kit project.
        
        Args:
            project_path: Path to the goal-kit project root
            
        Raises:
            FileNotFoundError: If project path doesn't exist or isn't a goal-kit project
        """
        self.project_path = Path(project_path).resolve()
        self.goalkit_dir = self.project_path / ".goalkit"
        self.milestones_dir = self.goalkit_dir / "milestones"
        self.history_file = self.goalkit_dir / "execution_history.json"

        if not self.project_path.exists():
            raise FileNotFoundError(f"Project path does not exist: {self.project_path}")

        if not self.goalkit_dir.exists():
            raise FileNotFoundError(f"Not a goal-kit project (missing .goalkit): {self.project_path}")

        # Create milestones directory if it doesn't exist
        self.milestones_dir.mkdir(parents=True, exist_ok=True)

    def track_milestone(self, goal_id: str, milestone_id: str, notes: Optional[str] = None) -> None:
        """Mark a milestone as completed.
        
        Args:
            goal_id: ID of the goal containing the milestone
            milestone_id: ID of the milestone to mark complete
            notes: Optional notes about the milestone completion
        """
        record = MilestoneRecord(
            milestone_id=milestone_id,
            goal_id=goal_id,
            completed_at=datetime.now(),
            notes=notes,
        )

        self._save_milestone_record(record)

    def get_milestone_history(self, goal_id: Optional[str] = None, limit: int = 10) -> List[MilestoneRecord]:
        """Get execution history, optionally filtered by goal.
        
        Args:
            goal_id: Optional goal ID to filter by
            limit: Maximum number of records to return
            
        Returns:
            List of milestone records in reverse chronological order
        """
        if not self.history_file.exists():
            return []

        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            records = [
                MilestoneRecord(
                    milestone_id=r["milestone_id"],
                    goal_id=r["goal_id"],
                    completed_at=datetime.fromisoformat(r["completed_at"]),
                    notes=r.get("notes"),
                )
                for r in data
            ]

            # Filter by goal if specified
            if goal_id:
                records = [r for r in records if r.goal_id == goal_id]

            # Sort by completed_at descending (most recent first)
            records.sort(key=lambda r: r.completed_at, reverse=True)

            return records[:limit]
        except (json.JSONDecodeError, KeyError, ValueError):
            return []

    def update_goal_progress(self, goal_id: str, percent: int) -> None:
        """Update goal completion percentage.
        
        Args:
            goal_id: ID of the goal to update
            percent: Completion percentage (0-100)
        """
        # Validate percentage
        percent = max(0, min(100, percent))

        # In a full implementation, this would update the goal markdown file
        # For now, just ensure the value is valid
        assert 0 <= percent <= 100

    def get_execution_stats(self, goals: List[Goal], completion_percent: float) -> ExecutionStats:
        """Get execution statistics for the project.
        
        Args:
            goals: List of goals in the project
            completion_percent: Overall project completion percentage
            
        Returns:
            ExecutionStats with velocity and completion estimates
        """
        history = self.get_milestone_history(limit=100)

        # Calculate total and completed milestones
        total_milestones = self._count_total_milestones(goals)
        completed_milestones = len(history)

        # Calculate completion percentage
        milestone_completion = (
            (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0
        )

        # Calculate velocity
        velocity = self._calculate_velocity(history)

        # Estimate completion date
        estimated_completion = self._estimate_completion(
            total_milestones, completed_milestones, velocity
        )

        # Count milestones by goal
        milestone_by_goal = self._count_milestones_by_goal(goals)

        # Get recent milestones
        recent_milestones = self.get_milestone_history(limit=3)

        return ExecutionStats(
            total_milestones=total_milestones,
            completed_milestones=completed_milestones,
            completion_percent=milestone_completion,
            velocity_per_day=velocity,
            estimated_completion=estimated_completion,
            recent_milestones=recent_milestones,
            milestone_by_goal=milestone_by_goal,
        )

    def _save_milestone_record(self, record: MilestoneRecord) -> None:
        """Save a milestone record to the execution history file.
        
        Args:
            record: The milestone record to save
        """
        # Load existing records
        records = []
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    records = json.load(f)
            except (json.JSONDecodeError, IOError):
                records = []

        # Add new record
        records.append({
            "milestone_id": record.milestone_id,
            "goal_id": record.goal_id,
            "completed_at": record.completed_at.isoformat(),
            "notes": record.notes,
        })

        # Save updated records
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

    def _calculate_velocity(self, history: List[MilestoneRecord]) -> float:
        """Calculate completion velocity in milestones per day.
        
        Args:
            history: List of milestone records
            
        Returns:
            Velocity in milestones per day
        """
        if len(history) < 2:
            return 0.0

        # Use first and last records to calculate velocity
        oldest = history[-1]  # Last item (oldest, since sorted descending)
        newest = history[0]   # First item (newest)

        days_elapsed = (newest.completed_at - oldest.completed_at).days
        if days_elapsed == 0:
            return 0.0

        milestones_completed = len(history) - 1
        return milestones_completed / days_elapsed

    def _estimate_completion(
        self, total: int, completed: int, velocity: float
    ) -> Optional[datetime]:
        """Estimate project completion date.
        
        Args:
            total: Total number of milestones
            completed: Number of completed milestones
            velocity: Milestones per day
            
        Returns:
            Estimated completion datetime or None if cannot estimate
        """
        if velocity <= 0 or total <= completed:
            return None

        remaining = total - completed
        days_remaining = remaining / velocity
        return datetime.now() + timedelta(days=days_remaining)

    def _count_total_milestones(self, goals: List[Goal]) -> int:
        """Count total milestones across all goals.
        
        Args:
            goals: List of goals
            
        Returns:
            Total milestone count
        """
        # Each goal has 2 milestones (placeholder)
        # In full implementation, would parse actual milestone files
        return max(0, len(goals) * 2)

    def _count_milestones_by_goal(self, goals: List[Goal]) -> Dict[str, int]:
        """Count milestones for each goal.
        
        Args:
            goals: List of goals
            
        Returns:
            Dictionary mapping goal ID to milestone count
        """
        return {goal.id: 2 for goal in goals}  # Placeholder: 2 per goal
