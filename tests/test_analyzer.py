"""Tests for analyzer module."""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

from goalkit.analyzer import ProjectAnalyzer, AnalysisResult
from goalkit.models import Goal


class TestProjectAnalyzer:
    """Tests for ProjectAnalyzer class."""

    @pytest.fixture
    def temp_project(self):
        """Create a temporary goal-kit project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir).resolve()  # resolve() to handle macOS /tmp -> /private/tmp symlink
            goalkit_dir = project_path / ".goalkit"
            goals_dir = goalkit_dir / "goals"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            goals_dir.mkdir(parents=True, exist_ok=True)

            yield project_path

    def test_analyzer_init_valid_project(self, temp_project):
        """Test initializing analyzer with valid project."""
        analyzer = ProjectAnalyzer(temp_project)
        assert analyzer.project_path == temp_project
        assert analyzer.goalkit_dir == temp_project / ".goalkit"
        assert analyzer.goals_dir == temp_project / ".goalkit" / "goals"

    def test_analyzer_init_missing_project_path(self):
        """Test initializing analyzer with non-existent path."""
        with pytest.raises(FileNotFoundError):
            ProjectAnalyzer(Path("/nonexistent/project"))

    def test_analyzer_init_missing_goalkit(self, temp_project):
        """Test initializing analyzer without .goalkit directory."""
        import shutil
        
        goalkit_dir = temp_project / ".goalkit"
        if goalkit_dir.exists():
            shutil.rmtree(goalkit_dir)

        with pytest.raises(FileNotFoundError):
            ProjectAnalyzer(temp_project)

    def test_analyze_empty_project(self, temp_project):
        """Test analyzing empty project."""
        analyzer = ProjectAnalyzer(temp_project)
        result = analyzer.analyze()

        assert isinstance(result, AnalysisResult)
        assert result.project.name == temp_project.name
        assert result.completion_percent == 0.0
        assert result.health_score == 0.0
        assert result.phase == "setup"
        assert len(result.goals) == 0

    def test_load_project_no_metadata(self, temp_project):
        """Test loading project without project.json."""
        analyzer = ProjectAnalyzer(temp_project)
        project = analyzer._load_project()

        assert project.name == temp_project.name
        assert project.path == temp_project
        assert project.agent == "unknown"

    def test_load_project_with_metadata(self, temp_project):
        """Test loading project with project.json."""
        metadata = {
            "name": "Test Project",
            "agent": "claude",
            "created_at": datetime.now().isoformat(),
        }
        project_file = temp_project / ".goalkit" / "project.json"
        with open(project_file, "w") as f:
            json.dump(metadata, f)

        analyzer = ProjectAnalyzer(temp_project)
        project = analyzer._load_project()

        assert project.name == "Test Project"
        assert project.agent == "claude"

    def test_load_project_invalid_json(self, temp_project):
        """Test loading project with invalid JSON."""
        project_file = temp_project / ".goalkit" / "project.json"
        with open(project_file, "w") as f:
            f.write("{invalid json}")

        analyzer = ProjectAnalyzer(temp_project)
        with pytest.raises(json.JSONDecodeError):
            analyzer._load_project()

    def test_parse_goal_file(self, temp_project):
        """Test parsing a goal markdown file."""
        goal_content = """# Test Task

## Phase
execute

## Completion
Completion: 50%

## Success Criteria
- [x] First criterion
- [ ] Second criterion

## Metrics
KPI 1: 80%
"""
        goal_file = temp_project / ".goalkit" / "goals" / "test-goal.md"
        with open(goal_file, "w") as f:
            f.write(goal_content)

        analyzer = ProjectAnalyzer(temp_project)
        goal = analyzer._parse_goal_file(goal_file)

        assert goal is not None
        assert goal.id == "test-goal"
        assert goal.phase == "execute"
        assert goal.completion_percent == 50
        assert goal.success_criteria_count == 2
        assert goal.metrics_defined is True

    def test_parse_goal_file_missing(self, temp_project):
        """Test parsing non-existent goal file."""
        analyzer = ProjectAnalyzer(temp_project)
        goal_file = temp_project / ".goalkit" / "goals" / "missing.md"

        result = analyzer._parse_goal_file(goal_file)
        assert result is None

    def test_extract_phase(self, temp_project):
        """Test extracting phase from content."""
        analyzer = ProjectAnalyzer(temp_project)

        assert analyzer._extract_phase("## Strategies") == "strategies"
        assert analyzer._extract_phase("## Milestones") == "milestones"
        assert analyzer._extract_phase("## Execute") == "execute"
        assert analyzer._extract_phase("No phase here") == "execute"

    def test_extract_completion(self, temp_project):
        """Test extracting completion percentage."""
        analyzer = ProjectAnalyzer(temp_project)

        assert analyzer._extract_completion("Progress: 50%") == 50
        assert analyzer._extract_completion("Completion: 75%") == 75
        assert analyzer._extract_completion("Completion: 100%") == 100
        assert analyzer._extract_completion("No percent values here") == 0
        assert analyzer._extract_completion("150% complete") == 100  # Capped at 100

    def test_count_success_criteria(self, temp_project):
        """Test counting success criteria."""
        analyzer = ProjectAnalyzer(temp_project)

        content = """
- [x] Completed item
- [ ] Pending item
- [x] Another completed
"""
        count = analyzer._count_success_criteria(content)
        assert count == 3

    def test_has_metrics(self, temp_project):
        """Test detecting metrics in content."""
        analyzer = ProjectAnalyzer(temp_project)

        assert analyzer._has_metrics("## Metrics\n- KPI: 80%") is True
        assert analyzer._has_metrics("KPI targets") is True
        assert analyzer._has_metrics("No metrics here") is False

    def test_calculate_completion_empty(self, temp_project):
        """Test calculating completion with no goals."""
        analyzer = ProjectAnalyzer(temp_project)
        completion = analyzer._calculate_completion([])
        assert completion == 0.0

    def test_calculate_completion_with_goals(self, temp_project):
        """Test calculating completion with goals."""
        analyzer = ProjectAnalyzer(temp_project)
        goals = [
            Goal("g1", "Goal 1", "execute", 50, 3, True),
            Goal("g2", "Goal 2", "execute", 75, 2, False),
            Goal("g3", "Goal 3", "execute", 25, 1, True),
        ]
        completion = analyzer._calculate_completion(goals)
        assert completion == 50.0  # (50 + 75 + 25) / 3

    def test_calculate_health_score_empty(self, temp_project):
        """Test calculating health score with no goals."""
        analyzer = ProjectAnalyzer(temp_project)
        score = analyzer._calculate_health_score([], 0.0)
        assert score == 0.0

    def test_calculate_health_score_with_goals(self, temp_project):
        """Test calculating health score with goals."""
        analyzer = ProjectAnalyzer(temp_project)
        goals = [
            Goal("g1", "Goal 1", "execute", 100, 3, True),
            Goal("g2", "Goal 2", "execute", 100, 2, True),
        ]
        score = analyzer._calculate_health_score(goals, 100.0)
        assert score > 0  # Should be > 0 for completed goals
        assert score <= 100  # Should not exceed 100

    def test_detect_phase_empty(self, temp_project):
        """Test detecting phase with no goals."""
        analyzer = ProjectAnalyzer(temp_project)
        phase = analyzer._detect_phase([], 0.0)
        assert phase == "setup"

    def test_detect_phase_with_goals(self, temp_project):
        """Test detecting phase with various goal states."""
        analyzer = ProjectAnalyzer(temp_project)

        goals_setup = [Goal("g1", "Goal", "vision", 0, 1, False)]
        assert analyzer._detect_phase(goals_setup, 0.0) == "setup"

        goals_active = [Goal("g1", "Goal", "strategies", 30, 2, False)]
        assert analyzer._detect_phase(goals_active, 30.0) == "active"

        goals_exec = [Goal("g1", "Goal", "execute", 60, 3, True)]
        assert analyzer._detect_phase(goals_exec, 60.0) == "execution"

        goals_done = [Goal("g1", "Goal", "done", 100, 3, True)]
        assert analyzer._detect_phase(goals_done, 100.0) == "complete"

    def test_count_milestones(self, temp_project):
        """Test counting milestones."""
        analyzer = ProjectAnalyzer(temp_project)

        goals = [
            Goal("g1", "Goal 1", "execute", 50, 3, True),
            Goal("g2", "Goal 2", "execute", 75, 2, False),
        ]
        count = analyzer._count_milestones(goals)
        assert count == len(goals) * 2

    def test_count_completed_milestones(self, temp_project):
        """Test counting completed milestones."""
        analyzer = ProjectAnalyzer(temp_project)

        goals = [
            Goal("g1", "Goal 1", "execute", 100, 3, True),
        ]
        completed = analyzer._count_completed_milestones(goals)
        assert completed > 0


class TestAnalysisIntegration:
    """Integration tests for full project analysis."""

    @pytest.fixture
    def sample_project(self):
        """Create a sample goal-kit project with content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            goalkit_dir = project_path / ".goalkit"
            goals_dir = goalkit_dir / "goals"
            goalkit_dir.mkdir(parents=True, exist_ok=True)
            goals_dir.mkdir(parents=True, exist_ok=True)

            # Create project metadata
            metadata = {
                "name": "Sample Project",
                "agent": "claude",
                "created_at": datetime.now().isoformat(),
            }
            with open(goalkit_dir / "project.json", "w") as f:
                json.dump(metadata, f)

            # Create sample goals
            goal1 = """# Authentication System

## Phase
execute

## Completion
50%

## Success Criteria
- [x] User login implemented
- [x] User registration implemented
- [ ] Password reset implemented

## Metrics
- Response time: < 100ms
- Success rate: > 99%
"""
            with open(goals_dir / "auth.md", "w") as f:
                f.write(goal1)

            goal2 = """# Database Design

## Phase
milestones

## Completion
75%

## Success Criteria
- [x] Schema designed
- [x] Indexes added
- [ ] Backups configured

## Metrics
- Query time: < 50ms
"""
            with open(goals_dir / "database.md", "w") as f:
                f.write(goal2)

            yield project_path

    def test_full_analysis(self, sample_project):
        """Test full project analysis with sample data."""
        analyzer = ProjectAnalyzer(sample_project)
        result = analyzer.analyze()

        assert result.project.name == "Sample Project"
        assert result.project.agent == "claude"
        assert len(result.goals) == 2
        assert result.completion_percent > 0
        assert result.health_score > 0
        assert result.phase in ["setup", "active", "execution", "complete"]
        assert result.milestone_count > 0

    def test_analysis_result_completeness(self, sample_project):
        """Test that analysis result contains all required fields."""
        analyzer = ProjectAnalyzer(sample_project)
        result = analyzer.analyze()

        # Check all fields are present
        assert hasattr(result, "project")
        assert hasattr(result, "goals")
        assert hasattr(result, "completion_percent")
        assert hasattr(result, "health_score")
        assert hasattr(result, "phase")
        assert hasattr(result, "milestone_count")
        assert hasattr(result, "completed_milestones")
        assert hasattr(result, "recent_milestones")

        # Check types
        assert isinstance(result.goals, list)
        assert isinstance(result.completion_percent, float)
        assert isinstance(result.health_score, float)
        assert isinstance(result.phase, str)
        assert isinstance(result.milestone_count, int)
        assert isinstance(result.recent_milestones, list)


class TestGoalDirectoryLayout:
    """Regression tests for goals stored as directories (goals/<id>/goal.md)."""

    @pytest.fixture
    def nested_project(self):
        """Create a project whose goal uses the canonical goal-directory layout."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir).resolve()
            goal_dir = (
                project_path
                / ".goalkit"
                / "goals"
                / "001-smarter-insights"
            )
            goal_dir.mkdir(parents=True)

            (goal_dir / "goal.md").write_text(
                """# Goal Statement: Make insights smarter

**Vision Alignment**: Success Scenario 1
**Status**: Draft

## User Stories

### Beneficiary Story 1 - Intelligent Insights

**Acceptance Scenarios**:

1. **Given** a user views status, **When** trends are poor, **Then** advice appears

### Key Metrics

- **SC-001**: 80% of users report insights are actionable

## Success Criteria

- [ ] Insights appear automatically
""",
                encoding="utf-8",
            )
            (goal_dir / "execution.md").write_text(
                "# Implementation Plan\n", encoding="utf-8"
            )
            (goal_dir / "milestones.md").write_text(
                """# Milestone Plan

**Milestone 1: Analysis Engine** (Weeks 1-2)
- **Deliverable**: Structured insights

**Milestone 2: Recommendations** (Weeks 3-4)
- **Deliverable**: Contextual advice

**Milestone 3: Validation** (Weeks 5-6)
- **Deliverable**: Measured outcomes

## Verification Plan

**Milestone 1 Verification**:
- [x] Tests pass
""",
                encoding="utf-8",
            )

            yield project_path

    def test_iter_goal_files_supports_both_layouts(self, nested_project):
        from goalkit.analyzer import iter_goal_files

        goals_dir = nested_project / ".goalkit" / "goals"
        (goals_dir / "002-legacy.md").write_text("# Legacy\n", encoding="utf-8")

        pairs = iter_goal_files(goals_dir)

        assert [goal_id for goal_id, _ in pairs] == [
            "001-smarter-insights",
            "002-legacy",
        ]
        assert pairs[0][1] == goals_dir / "001-smarter-insights" / "goal.md"
        assert pairs[1][1] == goals_dir / "002-legacy.md"

    def test_iter_goal_files_missing_directory(self, tmp_path):
        from goalkit.analyzer import iter_goal_files

        assert iter_goal_files(tmp_path / "missing") == []

    def test_analyze_discovers_goal_directories(self, nested_project):
        result = ProjectAnalyzer(nested_project).analyze()

        assert len(result.goals) == 1
        goal = result.goals[0]
        assert goal.id == "001-smarter-insights"
        assert goal.phase == "execute"
        assert goal.metrics_defined is True
        assert result.phase == "execution"
        assert result.milestone_count == 3
        assert result.completed_milestones == 0

    def test_analyze_mixed_layouts(self, nested_project):
        goals_dir = nested_project / ".goalkit" / "goals"
        (goals_dir / "002-legacy.md").write_text(
            "# Legacy Goal\n\n## Completion\n40%\n", encoding="utf-8"
        )

        result = ProjectAnalyzer(nested_project).analyze()

        assert [goal.id for goal in result.goals] == [
            "001-smarter-insights",
            "002-legacy",
        ]
        assert result.goals[1].completion_percent == 40

    def test_extract_phase_ignores_prose_mentions(self, tmp_path):
        analyzer = ProjectAnalyzer(self._empty_project(tmp_path))

        content = (
            "**Vision Alignment**: Success Scenario 1\n"
            "# Goal Statement: Smarter insights\n"
        )

        # "Vision Alignment" is prose, not a phase marker; the goal heading is.
        assert analyzer._extract_phase(content) == "goal"
        assert analyzer._extract_phase(
            "Goals and strategies and milestones are described below."
        ) == "execute"

    def test_extract_completion_ignores_success_metrics(self, tmp_path):
        analyzer = ProjectAnalyzer(self._empty_project(tmp_path))

        content = "### Key Metrics\n\n- 80% of users report insights are actionable\n"

        assert analyzer._extract_completion(content) == 0

    def test_extract_completion_reads_completion_section(self, tmp_path):
        analyzer = ProjectAnalyzer(self._empty_project(tmp_path))

        assert analyzer._extract_completion("## Completion\n50%\n") == 50

    def test_has_metrics_detects_nested_heading(self, tmp_path):
        analyzer = ProjectAnalyzer(self._empty_project(tmp_path))

        assert analyzer._has_metrics("### Key Metrics\n- SC-001: 80%") is True

    def test_no_metric_strength_without_goals(self, tmp_path):
        analyzer = ProjectAnalyzer(self._empty_project(tmp_path))

        insights = ProjectAnalyzer.get_insights_from_result(analyzer.analyze())

        assert "Most goals have defined metrics for tracking" not in insights["strengths"]

    @staticmethod
    def _empty_project(tmp_path: Path) -> Path:
        (tmp_path / ".goalkit" / "goals").mkdir(parents=True)
        return tmp_path
