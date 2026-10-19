"""Project analysis and health scoring for Goalkeeper projects.

This module provides analysis capabilities for Goal Kit projects,
including goal parsing, completion tracking, and health scoring.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
import json
import re
from datetime import datetime

from .models import Project, Goal, Milestone


def iter_goal_files(goals_dir: Path) -> List[Tuple[str, Path]]:
    """List every goal file in a ``.goalkit/goals`` directory.

    Goalkit supports two layouts and both must be discovered:

    - ``goals/<goal-id>.md`` - single-file goals.
    - ``goals/<goal-id>/goal.md`` - goal directories created by the
      workflow scripts (``create-new-goal.sh`` and friends).

    Args:
        goals_dir: Path to the ``.goalkit/goals`` directory.

    Returns:
        Sorted ``(goal_id, goal_file)`` pairs. Empty when the directory
        is missing.
    """
    goals_dir = Path(goals_dir)
    if not goals_dir.is_dir():
        return []

    found: Dict[str, Path] = {}
    for entry in sorted(goals_dir.iterdir()):
        if entry.is_file() and entry.suffix == ".md":
            found.setdefault(entry.stem, entry)
        elif entry.is_dir():
            goal_md = entry / "goal.md"
            if goal_md.is_file():
                found[entry.name] = goal_md

    return sorted(found.items())


def count_goal_milestones(goals_dir: Path, goal_id: str) -> Optional[int]:
    """Count distinct milestones in a goal directory's milestone plan.

    Args:
        goals_dir: Path to the ``.goalkit/goals`` directory.
        goal_id: Goal directory name.

    Returns:
        Number of milestones, or None when the goal has no
        ``milestones.md`` to read.
    """
    milestone_file = Path(goals_dir) / goal_id / "milestones.md"
    if not milestone_file.is_file():
        return None

    try:
        content = milestone_file.read_text(encoding="utf-8")
    except OSError:
        return None

    numbers = set(
        re.findall(
            r"^\s*(?:#{1,6}\s*|\*\*|[-*]\s+\*\*)?Milestone\s+(\d+)\b",
            content,
            re.IGNORECASE | re.MULTILINE,
        )
    )
    return len(numbers)


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
        for goal_id, goal_file in iter_goal_files(self.goals_dir):
            try:
                goal = self._parse_goal_file(goal_file, goal_id=goal_id)
                if goal:
                    goals.append(goal)
            except Exception:
                # Skip files that can't be parsed
                continue

        # Sort by goal ID for deterministic, reproducible output
        goals.sort(key=lambda g: g.id)

        return goals

    def _parse_goal_file(
        self, goal_file: Path, goal_id: Optional[str] = None
    ) -> Optional[Goal]:
        """Parse a single goal markdown file.
        
        Args:
            goal_file: Path to goal markdown file
            goal_id: Optional goal ID (directory name for goal directories).
                Defaults to the file stem.
            
        Returns:
            Goal instance or None if parsing fails
        """
        try:
            with open(goal_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract basic info from filename and content
            goal_id = goal_id or goal_file.stem  # Use filename without .md
            name = goal_id.replace("-", " ").title()

            # Prefer workflow artifacts next to goal.md over free-text hints
            phase = self._phase_from_layout(goal_file) or self._extract_phase(content)

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

    def _phase_from_layout(self, goal_file: Path) -> Optional[str]:
        """Infer a goal's phase from the workflow files in its directory.

        Goal directories gain one artifact per GDD phase. The most advanced
        artifact present wins. Returns None for single-file goals, which carry
        no phase artifacts.
        """
        goal_dir = goal_file.parent
        if goal_dir == self.goals_dir:
            return None

        artifacts = (
            ("execution.md", "execute"),
            ("milestones.md", "milestones"),
            ("strategies.md", "strategies"),
        )
        for filename, phase in artifacts:
            if (goal_dir / filename).is_file():
                return phase

        return "goal"

    def _extract_phase(self, content: str) -> str:
        """Extract phase from goal content.
        
        Only explicit phase markers (headings or ``Phase:`` labels) count, so
        prose such as "Vision Alignment" is not mistaken for a phase. The most
        advanced marker wins because later phases imply earlier ones.
        
        Args:
            content: Goal markdown content
            
        Returns:
            Phase string (default 'execute')
        """
        for phase in ("done", "execute", "milestones", "strategies", "goal", "vision"):
            marker = rf"^\s*(?:#+\s*|\*\*)?(?:phase\s*[:\-]\s*)?{phase}\b"
            if re.search(marker, content, re.IGNORECASE | re.MULTILINE):
                return phase

        return "execute"

    def _extract_completion(self, content: str) -> int:
        """Extract completion percentage from goal content.
        
        Args:
            content: Goal markdown content
            
        Returns:
            Completion percentage (0-100)
        """
        def _clamp(value: str) -> int:
            return min(100, max(0, int(value)))

        # Explicit progress statements, e.g. "Completion: 75%"
        for pattern in (
            r"(?:completion|progress|completed)\s*[:=]\s*(\d+)\s*%",
            r"(\d+)\s*%\s*(?:complete|completed|done|finished)",
        ):
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return _clamp(match.group(1))

        # A bare percentage is only progress when it sits in a completion or
        # progress section; otherwise success metrics like "80% of users"
        # would be read as progress.
        section = re.search(
            r"(?ims)^#{1,6}\s*(?:completion|progress)\s*$(.*?)(?=^#{1,6}\s|\Z)",
            content,
        )
        if section:
            match = re.search(r"(\d+)\s*%", section.group(1))
            if match:
                return _clamp(match.group(1))

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
        # A metrics/KPI heading (at any depth, e.g. "### Key Metrics") or an
        # explicit KPI definition counts as metrics being defined.
        patterns = [
            r"^#{1,6}\s+.*\bmetrics?\b",
            r"^#{1,6}\s+.*\bkpis?\b",
            r"KPI\s*\d+\s*:\s*",
            r"\bKPI\b",
        ]
        return any(
            re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            for pattern in patterns
        )

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
        total = 0
        for goal in goals:
            parsed = self._count_goal_milestones(goal.id)
            # Legacy single-file goals have no milestone plan to parse; keep
            # the historic two-per-goal estimate for them.
            total += 2 if parsed is None else parsed

        return max(0, total)

    def _count_goal_milestones(self, goal_id: str) -> Optional[int]:
        """Count distinct milestones in a goal directory's milestone plan."""
        return count_goal_milestones(self.goals_dir, goal_id)

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

    def get_insights(self) -> Dict[str, Any]:
        """Generate actionable insights for the project.
        
        Returns:
            Dictionary containing insights and recommendations
        """
        result = self.analyze()
        return self.get_insights_from_result(result)
    
    @staticmethod
    def get_insights_from_result(result: AnalysisResult) -> Dict[str, Any]:
        """Generate insights from existing analysis result.
        
        Args:
            result: Existing AnalysisResult to generate insights from
            
        Returns:
            Dictionary containing insights and recommendations
        """
        analyzer = ProjectAnalyzer.__new__(ProjectAnalyzer)
        insights = {
            "summary": analyzer._generate_summary(result),
            "recommendations": analyzer._generate_recommendations(result),
            "concerns": analyzer._identify_concerns(result),
            "strengths": analyzer._identify_strengths(result),
        }
        return insights

    def _generate_summary(self, result: AnalysisResult) -> str:
        """Generate project summary."""
        if result.health_score >= 80:
            status = "healthy"
        elif result.health_score >= 50:
            status = "needs attention"
        else:
            status = "requires action"
        
        return f"Project is {status} (health: {result.health_score}%, completion: {result.completion_percent}%)"

    def _generate_recommendations(self, result: AnalysisResult) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if result.completion_percent < 30:
            recommendations.append("Focus on making progress - break down goals into smaller milestones")
        
        if result.health_score < 50:
            recommendations.append("Define success metrics for goals to improve tracking")
        
        if result.milestone_count > 0 and result.completed_milestones == 0:
            recommendations.append("Complete at least one milestone to build momentum")
        
        goals_without_metrics = [g for g in result.goals if not g.metrics_defined]
        if goals_without_metrics:
            recommendations.append(f"Add metrics to {len(goals_without_metrics)} goal(s) for better progress visibility")
        
        if not recommendations:
            recommendations.append("Keep up the good work - project is on track")
        
        return recommendations

    def _identify_concerns(self, result: AnalysisResult) -> List[str]:
        """Identify areas of concern."""
        concerns = []
        
        if result.phase == "execute" and result.completion_percent < 20:
            concerns.append("Low progress in execution phase")
        
        if result.health_score < 40:
            concerns.append("Health score is below critical threshold")
        
        stalled_goals = [g for g in result.goals if g.phase == "execute" and g.completion_percent == 0]
        if stalled_goals:
            concerns.append(f"{len(stalled_goals)} goal(s) stalled in execution")
        
        return concerns

    def _identify_strengths(self, result: AnalysisResult) -> List[str]:
        """Identify project strengths."""
        strengths = []
        
        if result.health_score >= 70:
            strengths.append("Strong health score indicates good project management")
        
        if result.completion_percent >= 50:
            strengths.append("Over 50% completion shows solid progress")
        
        goals_with_metrics = [g for g in result.goals if g.metrics_defined]
        if result.goals and len(goals_with_metrics) >= len(result.goals) * 0.7:
            strengths.append("Most goals have defined metrics for tracking")
        
        return strengths
