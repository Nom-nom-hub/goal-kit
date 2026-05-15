"""Metrics tracking and health scoring for Goalkeeper projects.

This module provides metrics tracking capabilities including custom metric
recording, trend analysis, and health score calculation.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
from datetime import datetime, timedelta

from .models import Goal


@dataclass
class MetricRecord:
    """Record of a metric measurement."""

    metric_name: str
    goal_id: str
    value: float
    measured_at: datetime
    notes: Optional[str] = None


@dataclass
class MetricStats:
    """Statistics for a metric."""

    metric_name: str
    total_records: int
    current_value: Optional[float]
    average_value: float
    min_value: float
    max_value: float
    trend: float  # -1 to 1, negative = declining, positive = improving
    last_measured: Optional[datetime] = None


@dataclass
class HealthScore:
    """Project health score breakdown."""

    overall_score: float  # 0-100
    completion_score: float  # 0-100
    metrics_score: float  # 0-100
    momentum_score: float  # 0-100
    quality_score: float  # 0-100
    breakdown: Dict[str, float] = field(default_factory=dict)


class MetricsTracker:
    """Track project metrics and calculate health scores.
    
    Provides methods to:
    - Record custom metrics per goal
    - Track metric trends over time
    - Calculate project health scores
    - Retrieve metric history and statistics
    """

    def __init__(self, project_path: Path):
        """Initialize metrics tracker for a goal-kit project.
        
        Args:
            project_path: Path to the goal-kit project root
            
        Raises:
            FileNotFoundError: If project path doesn't exist or isn't a goal-kit project
        """
        self.project_path = Path(project_path).resolve()
        self.goalkit_dir = self.project_path / ".goalkit"
        self.metrics_dir = self.goalkit_dir / "metrics"
        self.history_file = self.goalkit_dir / "metrics_history.json"

        if not self.project_path.exists():
            raise FileNotFoundError(f"Project path does not exist: {self.project_path}")

        if not self.goalkit_dir.exists():
            raise FileNotFoundError(f"Not a goal-kit project (missing .goalkit): {self.project_path}")

        # Create metrics directory if it doesn't exist
        self.metrics_dir.mkdir(parents=True, exist_ok=True)

    def track_metric(
        self, goal_id: str, metric_name: str, value: float, notes: Optional[str] = None
    ) -> None:
        """Record a metric value for a goal.
        
        Args:
            goal_id: ID of the goal
            metric_name: Name of the metric
            value: Numeric value of the metric
            notes: Optional notes about the measurement
        """
        record = MetricRecord(
            metric_name=metric_name,
            goal_id=goal_id,
            value=value,
            measured_at=datetime.now(),
            notes=notes,
        )

        self._save_metric_record(record)

    def get_metrics_for_goal(
        self, goal_id: str, limit: int = 100
    ) -> Dict[str, List[MetricRecord]]:
        """Get all metrics for a goal, grouped by metric name.
        
        Args:
            goal_id: ID of the goal
            limit: Maximum number of records per metric
            
        Returns:
            Dictionary mapping metric names to lists of records
        """
        if not self.history_file.exists():
            return {}

        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            records = [
                MetricRecord(
                    metric_name=r["metric_name"],
                    goal_id=r["goal_id"],
                    value=r["value"],
                    measured_at=datetime.fromisoformat(r["measured_at"]),
                    notes=r.get("notes"),
                )
                for r in data
                if r["goal_id"] == goal_id
            ]

            # Group by metric name and sort by date (newest first)
            grouped: Dict[str, List[MetricRecord]] = {}
            for record in records:
                if record.metric_name not in grouped:
                    grouped[record.metric_name] = []
                grouped[record.metric_name].append(record)

            # Sort each metric's records by date (newest first) and limit
            for metric_name in grouped:
                grouped[metric_name].sort(key=lambda r: r.measured_at, reverse=True)
                grouped[metric_name] = grouped[metric_name][:limit]

            return grouped
        except (json.JSONDecodeError, KeyError, ValueError):
            return {}

    def get_metric_stats(self, goal_id: str, metric_name: str) -> Optional[MetricStats]:
        """Get statistics for a specific metric.
        
        Args:
            goal_id: ID of the goal
            metric_name: Name of the metric
            
        Returns:
            MetricStats object or None if no data
        """
        metrics = self.get_metrics_for_goal(goal_id)
        
        if metric_name not in metrics:
            return None

        records = metrics[metric_name]
        if not records:
            return None

        values = [r.value for r in records]
        trend = self._calculate_trend(records)

        return MetricStats(
            metric_name=metric_name,
            total_records=len(records),
            current_value=records[0].value if records else None,
            average_value=sum(values) / len(values),
            min_value=min(values),
            max_value=max(values),
            trend=trend,
            last_measured=records[0].measured_at if records else None,
        )

    def calculate_health_score(self, goals: List[Goal], completion_percent: float) -> HealthScore:
        """Calculate project health score from metrics and progress.
        
        Args:
            goals: List of goals in the project
            completion_percent: Overall project completion percentage
            
        Returns:
            HealthScore with breakdown by component
        """
        # Component weights
        completion_weight = 0.40
        metrics_weight = 0.30
        momentum_weight = 0.20
        quality_weight = 0.10

        # Completion score (0-100)
        completion_score = completion_percent

        # Metrics score based on goal metrics count
        goals_with_metrics = sum(1 for g in goals if g.metrics_defined)
        metrics_score = (
            (goals_with_metrics / len(goals) * 100) if goals else 0
        )

        # Momentum score based on recent activity
        momentum_score = self._calculate_momentum_score()

        # Quality score based on metric consistency
        quality_score = self._calculate_quality_score(goals)

        # Calculate weighted overall score
        overall_score = (
            (completion_score * completion_weight)
            + (metrics_score * metrics_weight)
            + (momentum_score * momentum_weight)
            + (quality_score * quality_weight)
        )

        breakdown = {
            "completion": round(completion_score, 1),
            "metrics": round(metrics_score, 1),
            "momentum": round(momentum_score, 1),
            "quality": round(quality_score, 1),
        }

        return HealthScore(
            overall_score=round(min(100, overall_score), 1),
            completion_score=round(completion_score, 1),
            metrics_score=round(metrics_score, 1),
            momentum_score=round(momentum_score, 1),
            quality_score=round(quality_score, 1),
            breakdown=breakdown,
        )

    def get_metric_trends(self, goal_id: str, metric_name: str, days: int = 30) -> Dict[str, float]:
        """Get metric trend values over the past N days.
        
        Args:
            goal_id: ID of the goal
            metric_name: Name of the metric
            days: Number of days to include
            
        Returns:
            Dictionary mapping date (YYYY-MM-DD) to metric value
        """
        if not self.history_file.exists():
            return {}

        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            now = datetime.now()
            cutoff_date = now - timedelta(days=days)

            trends = {}
            for record_data in data:
                if (record_data["goal_id"] == goal_id and 
                    record_data["metric_name"] == metric_name):
                    measured = datetime.fromisoformat(record_data["measured_at"])
                    if measured >= cutoff_date:
                        date_key = measured.strftime("%Y-%m-%d")
                        # Keep the most recent value for each day
                        if date_key not in trends or measured > datetime.fromisoformat(
                            data[[i for i, r in enumerate(data) if 
                                 r.get("metric_name") == metric_name and 
                                 r.get("goal_id") == goal_id and
                                 r.get("measured_at", "").startswith(date_key)][0]]["measured_at"]
                        ) if data else True:
                            trends[date_key] = record_data["value"]

            return trends
        except (json.JSONDecodeError, KeyError, ValueError, IndexError):
            return {}

    def _save_metric_record(self, record: MetricRecord) -> None:
        """Save a metric record to the history file.
        
        Args:
            record: The metric record to save
        """
        records = []
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    records = json.load(f)
            except (json.JSONDecodeError, IOError):
                records = []

        # Add new record
        records.append({
            "metric_name": record.metric_name,
            "goal_id": record.goal_id,
            "value": record.value,
            "measured_at": record.measured_at.isoformat(),
            "notes": record.notes,
        })

        # Save updated records
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

    def _calculate_trend(self, records: List[MetricRecord]) -> float:
        """Calculate trend for a metric (positive = improving).
        
        Args:
            records: List of metric records in descending time order
            
        Returns:
            Trend score from -1 to 1
        """
        if len(records) < 2:
            return 0.0

        # Compare recent average to older average
        recent = records[: len(records) // 2]
        older = records[len(records) // 2 :]

        recent_avg = sum(r.value for r in recent) / len(recent)
        older_avg = sum(r.value for r in older) / len(older)

        if older_avg == 0:
            return 0.0

        # Normalize trend to -1 to 1 range
        change = (recent_avg - older_avg) / older_avg
        return max(-1.0, min(1.0, change))

    def _calculate_momentum_score(self) -> float:
        """Calculate momentum score based on recent metric activity.
        
        Returns:
            Score from 0-100
        """
        if not self.history_file.exists():
            return 0.0

        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            now = datetime.now()
            week_ago = now - timedelta(days=7)

            recent_count = sum(
                1 for r in data
                if datetime.fromisoformat(r["measured_at"]) >= week_ago
            )

            # Momentum: expect 1 metric per day
            expected = 7
            momentum = min(100.0, (recent_count / expected * 100) if expected > 0 else 0)
            return round(momentum, 1)
        except (json.JSONDecodeError, KeyError, ValueError):
            return 0.0

    def _calculate_quality_score(self, goals: List[Goal]) -> float:
        """Calculate quality score based on metric consistency.
        
        Args:
            goals: List of goals
            
        Returns:
            Score from 0-100
        """
        if not goals or not self.history_file.exists():
            return 0.0

        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not data:
                return 0.0

            # Quality = consistency of metrics across goals
            goal_ids = {g.id for g in goals}
            covered_goals = len({r["goal_id"] for r in data if r["goal_id"] in goal_ids})

            quality = (covered_goals / len(goals) * 100) if goals else 0
            return round(min(100.0, quality), 1)
        except (json.JSONDecodeError, KeyError, ValueError):
            return 0.0
