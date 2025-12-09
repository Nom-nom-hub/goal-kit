"""Project analysis and health scoring for Goalkeeper projects.

This module provides analysis capabilities for Goal Kit projects,
including goal parsing, completion tracking, and health scoring.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
from datetime import datetime

from .models import Project, Goal, Milestone, Task


@dataclass
class AnalysisResult:
    """Result of analyzing a goal-kit project."""

    project: Project
    goals: List[Goal]
    completion_percent: float
    health_score: float
    phase: str  # 'setup', 'active', 'execution', 'complete'
    milestone_count: int
    completed_milestones: int
    recent_milestones: List[Milestone]


class ProjectAnalyzer:
    """Analyze Goal Kit projects and extract state information.
    
    Provides methods to:
    - Load project metadata from .goalkit directory
    - Parse goal markdown files
    - Calculate completion percentage
    - Compute health score
    - Detect current project phase
    - Extract milestone information
    """

    def __init__(self, project_path: Path):
        """Initialize analyzer for a goal-kit project.
        
        Args:
            project_path: Path to the goal-kit project root
            
        Raises:
            FileNotFoundError: If project path doesn't exist or isn't a goal-kit project
        """
        self.project_path = Path(project_path).resolve()
        self.goalkit_dir = self.project_path / ".goalkit"
        self.goals_dir = self.goalkit_dir / "goals"

        if not self.project_path.exists():
            raise FileNotFoundError(f"Project path does not exist: {self.project_path}")

        if not self.goalkit_dir.exists():
            raise FileNotFoundError(f"Not a goal-kit project (missing .goalkit): {self.project_path}")

    def analyze(self) -> AnalysisResult:
        """Perform complete analysis of the project.
        
        Returns:
            AnalysisResult containing all project analysis data
        """
        project = self._load_project()
        goals = self._analyze_goals()
        completion_percent = self._calculate_completion(goals)
        health_score = self._calculate_health_score(goals, completion_percent)
        phase = self._detect_phase(goals, completion_percent)
        milestone_count = self._count_milestones(goals)
        completed_milestones = self._count_completed_milestones(goals)
        recent_milestones = self._get_recent_milestones(goals, limit=3)

        return AnalysisResult(
            project=project,
            goals=goals,
            completion_percent=completion_percent,
            health_score=health_score,
            phase=phase,
            milestone_count=milestone_count,
            completed_milestones=completed_milestones,
            recent_milestones=recent_milestones,
        )

    def _load_project(self) -> Project:
        """Load project metadata from .goalkit directory.
        
        Returns:
            Project instance with loaded metadata
            
        Raises:
            FileNotFoundError: If project.json is missing
            json.JSONDecodeError: If project.json is invalid
        """
        project_file = self.goalkit_dir / "project.json"

        if not project_file.exists():
            # Return a basic project if metadata doesn't exist
            return Project(
                name=self.project_path.name,
                path=self.project_path,
                agent="unknown",
                created_at=datetime.now(),
                health_score=None,
            )

        try:
            with open(project_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            return Project(
                name=data.get("name", self.project_path.name),
                path=self.project_path,
                agent=data.get("agent", "unknown"),
                created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
                health_score=data.get("health_score"),
            )
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid project.json: {e.msg}", e.doc, e.pos) from e

    def _analyze_goals(self) -> List[Goal]:
        """Parse and analyze all goal markdown files.
        
        Returns:
            List of Goal instances parsed from markdown files
        """
        if not self.goals_dir.exists():
            return []

        goals = []
        for goal_file in self.goals_dir.glob("*.md"):
            try:
                goal = self._parse_goal_file(goal_file)
                if goal:
                    goals.append(goal)
            except Exception:
                # Skip files that can't be parsed
                continue

        return goals

    def _parse_goal_file(self, goal_file: Path) -> Optional[Goal]:
        """Parse a single goal markdown file.
        
        Args:
            goal_file: Path to goal markdown file
            
        Returns:
            Goal instance or None if parsing fails
        """
        try:
            with open(goal_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract basic info from filename and content
            goal_id = goal_file.stem  # Use filename without .md
            name = goal_id.replace("-", " ").title()

            # Try to extract phase from content
            phase = self._extract_phase(content)

            # Try to extract completion percentage
            completion_percent = self._extract_completion(content)

            # Count success criteria and metrics
            success_criteria_count = self._count_success_criteria(content)
            metrics_defined = self._has_metrics(content)

            return Goal(
                id=goal_id,
                name=name,
                phase=phase,
                completion_percent=completion_percent,
                success_criteria_count=success_criteria_count,
                metrics_defined=metrics_defined,
            )
        except Exception:
            return None

    def _extract_phase(self, content: str) -> str:
        """Extract phase from goal content.
        
        Args:
            content: Goal markdown content
            
        Returns:
            Phase string (default 'execute')
        """
        phases = ["vision", "goal", "strategies", "milestones", "execute", "done"]
        content_lower = content.lower()

        for phase in phases:
            if phase in content_lower:
                return phase

        return "execute"

    def _extract_completion(self, content: str) -> int:
        """Extract completion percentage from goal content.
        
        Args:
            content: Goal markdown content
            
        Returns:
            Completion percentage (0-100)
        """
        import re

        # Look for patterns like "50%" or "completion: 50"
        # Only match patterns that look like legitimate percentages
        patterns = [
            r"(?:completion|progress|completed)\s*:?\s*(\d+)%",
            r"(\d+)%\s*(?:complete|done|finished)",
            r"^.*?(\d+)%",
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                percent = int(match.group(1))
                return min(100, max(0, percent))

        return 0

    def _count_success_criteria(self, content: str) -> int:
        """Count success criteria in goal content.
        
        Args:
            content: Goal markdown content
            
        Returns:
            Number of success criteria found
        """
        import re

        # Count lines starting with "- [x]" or "- [ ]"
        pattern = r"^-\s*\[[x ]?\]"
        matches = re.findall(pattern, content, re.MULTILINE)
        return len(matches)

    def _has_metrics(self, content: str) -> bool:
        """Check if metrics are defined in goal content.
        
        Args:
            content: Goal markdown content
            
        Returns:
            True if metrics section found
        """
        import re
        
        # Look for ## Metrics heading or actual KPI definitions
        patterns = [r"^##\s+Metrics", r"^##\s+KPI", r"KPI\s*\d+:\s*", r"\bKPI\b"]
        return any(re.search(pattern, content, re.IGNORECASE | re.MULTILINE) for pattern in patterns)

    def _calculate_completion(self, goals: List[Goal]) -> float:
        """Calculate overall project completion percentage.
        
        Args:
            goals: List of goals to analyze
            
        Returns:
            Completion percentage (0-100)
        """
        if not goals:
            return 0.0

        total_completion = sum(goal.completion_percent for goal in goals)
        avg_completion = total_completion / len(goals)
        return round(avg_completion, 1)

    def _calculate_health_score(self, goals: List[Goal], completion: float) -> float:
        """Calculate project health score.
        
        Factors:
        - Completion percentage (40%)
        - Goals with metrics (30%)
        - Goals with success criteria (20%)
        - Phase progression (10%)
        
        Args:
            goals: List of goals
            completion: Completion percentage
            
        Returns:
            Health score (0-100)
        """
        if not goals:
            return 0.0

        # Completion factor (40%)
        completion_score = completion * 0.4

        # Metrics factor (30%)
        goals_with_metrics = sum(1 for g in goals if g.metrics_defined)
        metrics_score = (goals_with_metrics / len(goals)) * 100 * 0.3

        # Success criteria factor (20%)
        goals_with_criteria = sum(1 for g in goals if g.success_criteria_count > 0)
        criteria_score = (goals_with_criteria / len(goals)) * 100 * 0.2

        # Phase factor (10%)
        phase_scores = {
            "vision": 10,
            "goal": 20,
            "strategies": 40,
            "milestones": 60,
            "execute": 80,
            "done": 100,
        }
        avg_phase = sum(phase_scores.get(g.phase, 50) for g in goals) / len(goals)
        phase_score = (avg_phase / 100) * 100 * 0.1

        total_score = completion_score + metrics_score + criteria_score + phase_score
        return round(min(100.0, max(0.0, total_score)), 1)

    def _detect_phase(self, goals: List[Goal], completion: float) -> str:
        """Detect current project phase based on goals and completion.
        
        Args:
            goals: List of goals
            completion: Overall completion percentage
            
        Returns:
            Phase string ('setup', 'active', 'execution', 'complete')
        """
        if not goals:
            return "setup"

        # Determine phase based on goal states
        phases = [g.phase for g in goals]
        phase_counts = {phase: phases.count(phase) for phase in set(phases)}

        if completion >= 90:
            return "complete"
        elif "execute" in phases or "milestones" in phases:
            return "execution"
        elif "strategies" in phases or "goal" in phases:
            return "active"
        else:
            return "setup"

    def _count_milestones(self, goals: List[Goal]) -> int:
        """Count total milestones across all goals.
        
        Args:
            goals: List of goals
            
        Returns:
            Total milestone count
        """
        # For now, return a simple count based on goals
        # In future, will parse actual milestone files
        return max(0, len(goals) * 2)

    def _count_completed_milestones(self, goals: List[Goal]) -> int:
        """Count completed milestones across all goals.
        
        Args:
            goals: List of goals
            
        Returns:
            Completed milestone count
        """
        total = self._count_milestones(goals)
        completion = self._calculate_completion(goals)
        return int(total * (completion / 100))

    def _get_recent_milestones(self, goals: List[Goal], limit: int = 3) -> List[Milestone]:
        """Get recent completed milestones.
        
        Args:
            goals: List of goals
            limit: Maximum number of milestones to return
            
        Returns:
            List of recent Milestone instances
        """
        # For now, return empty list
        # In future, will parse actual milestone files
        return []
