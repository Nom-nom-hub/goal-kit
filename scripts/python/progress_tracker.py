#!/usr/bin/env python3
"""
Progress Tracking System for Goal Kit Methodology
Real-time dashboards and basic analytics for project monitoring
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict

# Add the common Python utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common import (
    write_info,
    write_success,
    write_error,
    write_warning,
    test_git_repo,
    get_git_root
)


@dataclass
class ProgressMetrics:
    """Progress metrics for goals and milestones"""
    goal_name: str
    total_milestones: int
    completed_milestones: int
    in_progress_milestones: int
    not_started_milestones: int
    completion_percentage: float
    days_since_creation: int
    estimated_completion_date: str
    velocity_score: float  # milestones completed per week
    status: str  # 'on_track', 'at_risk', 'behind', 'completed'


@dataclass
class ProjectAnalytics:
    """Overall project analytics"""
    project_name: str
    total_goals: int
    completed_goals: int
    in_progress_goals: int
    not_started_goals: int
    overall_completion: float
    average_goal_completion: float
    project_velocity: float  # goals completed per month
    risk_score: float  # 1-10 risk assessment
    last_updated: str


class ProgressTracker:
    """Progress tracking and analytics system"""

    def __init__(self, project_root: Optional[str] = None):
        self.project_root = project_root or get_git_root()
        if not self.project_root:
            raise ValueError("Must be run from a git repository")

        self.goals_dir = os.path.join(self.project_root, ".goalkit", "goals")
        self.analytics_file = os.path.join(self.project_root, ".goalkit", "analytics", "progress.json")

    def analyze_project_progress(self) -> ProjectAnalytics:
        """Analyze overall project progress"""
        if not os.path.exists(self.goals_dir):
            return ProjectAnalytics(
                project_name=os.path.basename(self.project_root) if self.project_root else "unknown",
                total_goals=0,
                completed_goals=0,
                in_progress_goals=0,
                not_started_goals=0,
                overall_completion=0.0,
                average_goal_completion=0.0,
                project_velocity=0.0,
                risk_score=1.0,
                last_updated=datetime.now().isoformat()
            )

        goals = self._get_all_goals()
        if not goals:
            return ProjectAnalytics(
                project_name=os.path.basename(self.project_root) if self.project_root else "unknown",
                total_goals=0,
                completed_goals=0,
                in_progress_goals=0,
                not_started_goals=0,
                overall_completion=0.0,
                average_goal_completion=0.0,
                project_velocity=0.0,
                risk_score=5.0,
                last_updated=datetime.now().isoformat()
            )

        # Analyze each goal
        goal_metrics = []
        for goal in goals:
            metrics = self._analyze_goal_progress(goal)
            goal_metrics.append(metrics)

        # Calculate project-level metrics
        total_goals = len(goal_metrics)
        completed_goals = sum(1 for m in goal_metrics if m.status == 'completed')
        in_progress_goals = sum(1 for m in goal_metrics if m.status in ['on_track', 'at_risk'])
        not_started_goals = sum(1 for m in goal_metrics if m.status == 'behind')

        overall_completion = sum(m.completion_percentage for m in goal_metrics) / total_goals
        average_goal_completion = sum(m.completion_percentage for m in goal_metrics) / total_goals

        # Calculate project velocity (goals completed per month)
        project_velocity = self._calculate_project_velocity(goal_metrics)

        # Calculate risk score
        risk_score = self._calculate_project_risk(goal_metrics)

        return ProjectAnalytics(
            project_name=os.path.basename(self.project_root) if self.project_root else "unknown",
            total_goals=total_goals,
            completed_goals=completed_goals,
            in_progress_goals=in_progress_goals,
            not_started_goals=not_started_goals,
            overall_completion=round(overall_completion, 2),
            average_goal_completion=round(average_goal_completion, 2),
            project_velocity=round(project_velocity, 2),
            risk_score=round(risk_score, 2),
            last_updated=datetime.now().isoformat()
        )

    def _get_all_goals(self) -> List[str]:
        """Get all goal directories"""
        if not os.path.exists(self.goals_dir):
            return []

        goals = []
        for item in os.listdir(self.goals_dir):
            goal_path = os.path.join(self.goals_dir, item)
            if os.path.isdir(goal_path):
                goals.append(goal_path)

        return goals

    def _analyze_goal_progress(self, goal_path: str) -> ProgressMetrics:
        """Analyze progress for a specific goal"""
        goal_name = os.path.basename(goal_path)

        # Get creation date from goal.md
        goal_file = os.path.join(goal_path, "goal.md")
        creation_date = self._get_creation_date(goal_file)

        # Analyze milestones
        milestones_file = os.path.join(goal_path, "milestones.md")
        if os.path.exists(milestones_file):
            milestone_stats = self._analyze_milestones(milestones_file)
        else:
            milestone_stats = (0, 0, 0, 0)  # total, completed, in_progress, not_started

        total, completed, in_progress, not_started = milestone_stats

        # Calculate completion percentage
        completion_percentage = (completed / max(total, 1)) * 100

        # Calculate days since creation
        if creation_date:
            days_since_creation = (datetime.now() - creation_date).days
        else:
            days_since_creation = 0

        # Estimate completion date
        estimated_completion_date = self._estimate_completion_date(
            completion_percentage, days_since_creation, total, completed
        )

        # Calculate velocity score
        velocity_score = self._calculate_velocity_score(
            completed, days_since_creation
        )

        # Determine status
        status = self._determine_goal_status(
            completion_percentage, velocity_score, days_since_creation
        )

        return ProgressMetrics(
            goal_name=goal_name,
            total_milestones=total,
            completed_milestones=completed,
            in_progress_milestones=in_progress,
            not_started_milestones=not_started,
            completion_percentage=round(completion_percentage, 2),
            days_since_creation=days_since_creation,
            estimated_completion_date=estimated_completion_date,
            velocity_score=round(velocity_score, 2),
            status=status
        )

    def _get_creation_date(self, goal_file: str) -> Optional[datetime]:
        """Extract creation date from goal file"""
        if not os.path.exists(goal_file):
            return None

        try:
            with open(goal_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Look for creation date in various formats
            date_patterns = [
                r'Created:\s*(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)',
                r'created:\s*(\d{4}-\d{2}-\d{2})',
                r'Date:\s*(\d{4}-\d{2}-\d{2})'
            ]

            for pattern in date_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    date_str = match.group(1)
                    try:
                        if 'T' in date_str:
                            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        else:
                            return datetime.strptime(date_str, '%Y-%m-%d')
                    except ValueError:
                        continue

        except Exception:
            pass

        return None

    def _analyze_milestones(self, milestones_file: str) -> Tuple[int, int, int, int]:
        """Analyze milestone completion status"""
        try:
            with open(milestones_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return (0, 0, 0, 0)

        # Count milestones by looking for milestone headers
        milestone_headers = re.findall(r'^#{2,3}\s+.*milestone.*', content, re.IGNORECASE | re.MULTILINE)
        total_milestones = len(milestone_headers)

        if total_milestones == 0:
            return (0, 0, 0, 0)

        # Look for completion indicators
        completed_indicators = re.findall(r'✅|completed|done|finished', content, re.IGNORECASE)
        in_progress_indicators = re.findall(r'🔄|in.progress|working|ongoing', content, re.IGNORECASE)

        # Estimate completion based on indicators
        completed = min(len(completed_indicators), total_milestones)
        in_progress = min(len(in_progress_indicators), total_milestones - completed)
        not_started = total_milestones - completed - in_progress

        return (total_milestones, completed, in_progress, not_started)

    def _estimate_completion_date(self, completion_percentage: float, days_since_creation: int,
                                 total_milestones: int, completed_milestones: int) -> str:
        """Estimate when the goal will be completed"""
        if completion_percentage >= 100:
            return "Completed"

        if completion_percentage <= 0 or total_milestones == 0:
            return "Unknown"

        # Calculate average milestones per day so far
        if days_since_creation > 0 and completed_milestones > 0:
            milestones_per_day = completed_milestones / days_since_creation
        else:
            milestones_per_day = 0.1  # Assume slow progress if no data

        remaining_milestones = total_milestones - completed_milestones
        if milestones_per_day > 0:
            days_to_completion = int(remaining_milestones / milestones_per_day)
            completion_date = datetime.now() + timedelta(days=days_to_completion)
            return completion_date.strftime('%Y-%m-%d')
        else:
            return "Unknown"

    def _calculate_velocity_score(self, completed_milestones: int, days_since_creation: int) -> float:
        """Calculate velocity as milestones completed per week"""
        if days_since_creation <= 0:
            return 0.0

        weeks_elapsed = days_since_creation / 7.0
        if weeks_elapsed <= 0:
            return 0.0

        return (completed_milestones / weeks_elapsed) * 10  # Scale to 0-10

    def _determine_goal_status(self, completion_percentage: float, velocity_score: float,
                              days_since_creation: int) -> str:
        """Determine overall goal status"""
        if completion_percentage >= 100:
            return "completed"

        # High velocity goals that are making good progress
        if velocity_score >= 7.0 and completion_percentage >= 30:
            return "on_track"

        # Moderate progress but some concerns
        if velocity_score >= 4.0 and completion_percentage >= 15:
            return "at_risk"

        # Slow progress or stalled
        if velocity_score < 4.0 or (days_since_creation > 30 and completion_percentage < 20):
            return "behind"

        return "on_track"

    def _calculate_project_velocity(self, goal_metrics: List[ProgressMetrics]) -> float:
        """Calculate overall project velocity"""
        if not goal_metrics:
            return 0.0

        total_velocity = sum(m.velocity_score for m in goal_metrics)
        return total_velocity / len(goal_metrics)

    def _calculate_project_risk(self, goal_metrics: List[ProgressMetrics]) -> float:
        """Calculate overall project risk score (1-10)"""
        if not goal_metrics:
            return 5.0

        # Risk factors
        behind_goals = sum(1 for m in goal_metrics if m.status == 'behind')
        at_risk_goals = sum(1 for m in goal_metrics if m.status == 'at_risk')
        stalled_goals = sum(1 for m in goal_metrics if m.velocity_score < 2.0)

        # Calculate risk score
        total_risk_factors = behind_goals * 3 + at_risk_goals * 2 + stalled_goals * 1.5
        max_possible_risk = len(goal_metrics) * 3

        if max_possible_risk == 0:
            return 1.0

        risk_ratio = total_risk_factors / max_possible_risk
        return 1.0 + (risk_ratio * 9.0)  # Scale to 1-10

    def generate_progress_report(self, output_format: str = 'text') -> str:
        """Generate comprehensive progress report"""
        project_analytics = self.analyze_project_progress()
        goal_metrics = []

        # Get detailed goal metrics
        for goal_path in self._get_all_goals():
            metrics = self._analyze_goal_progress(goal_path)
            goal_metrics.append(metrics)

        if output_format == 'json':
            report_data = {
                'project_analytics': asdict(project_analytics),
                'goal_details': [asdict(m) for m in goal_metrics],
                'generated_at': datetime.now().isoformat()
            }
            return json.dumps(report_data, indent=2)

        # Generate text report
        report = self._generate_text_report(project_analytics, goal_metrics)
        return report

    def _generate_text_report(self, project: ProjectAnalytics, goals: List[ProgressMetrics]) -> str:
        """Generate formatted text report"""
        lines = []
        lines.append("=" * 80)
        lines.append("GOAL KIT PROGRESS TRACKING REPORT")
        lines.append(f"Project: {project.project_name}")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)

        # Project summary
        lines.append("\n📊 PROJECT SUMMARY")
        lines.append("-" * 40)
        lines.append(f"Total Goals: {project.total_goals}")
        lines.append(f"Completed: {project.completed_goals} ({project.completed_goals/project.total_goals*100:.1f}%)" if project.total_goals > 0 else "Completed: 0")
        lines.append(f"In Progress: {project.in_progress_goals}")
        lines.append(f"Not Started: {project.not_started_goals}")
        lines.append(f"Overall Completion: {project.overall_completion:.1f}%")
        lines.append(f"Project Velocity: {project.project_velocity:.1f}/10")
        lines.append(f"Risk Score: {project.risk_score:.1f}/10 {'🟢' if project.risk_score < 4 else '🟡' if project.risk_score < 7 else '🔴'}")

        # Individual goal progress
        if goals:
            lines.append("\n🎯 GOAL PROGRESS DETAILS")
            lines.append("-" * 40)

            for goal in sorted(goals, key=lambda x: x.completion_percentage, reverse=True):
                status_icon = {
                    'completed': '✅',
                    'on_track': '🚀',
                    'at_risk': '⚠️',
                    'behind': '🐌'
                }.get(goal.status, '❓')

                lines.append(f"\n{status_icon} {goal.goal_name}")
                lines.append(f"   Progress: {goal.completion_percentage:.1f}% ({goal.completed_milestones}/{goal.total_milestones} milestones)")
                lines.append(f"   Velocity: {goal.velocity_score:.1f}/10")
                lines.append(f"   Age: {goal.days_since_creation} days")

                if goal.estimated_completion_date != "Unknown":
                    lines.append(f"   Est. Completion: {goal.estimated_completion_date}")

        # Recommendations
        lines.append("\n💡 RECOMMENDATIONS")
        lines.append("-" * 40)

        if project.risk_score > 7:
            lines.append("🔴 HIGH RISK: Consider reviewing goals that are behind schedule")
        elif project.risk_score > 4:
            lines.append("🟡 MEDIUM RISK: Monitor goals with low velocity scores")
        else:
            lines.append("🟢 LOW RISK: Project is progressing well")

        if project.project_velocity < 3:
            lines.append("🐌 SLOW VELOCITY: Consider accelerating milestone completion")

        if project.overall_completion < 25:
            lines.append("🚀 EARLY STAGE: Focus on completing initial milestones to build momentum")

        lines.append("=" * 80)
        return "\n".join(lines)

    def save_analytics_data(self):
        """Save current analytics data for historical tracking"""
        os.makedirs(os.path.dirname(self.analytics_file), exist_ok=True)

        analytics_data = {
            'timestamp': datetime.now().isoformat(),
            'project_analytics': asdict(self.analyze_project_progress()),
            'goal_snapshots': []
        }

        # Save current state of each goal
        for goal_path in self._get_all_goals():
            goal_metrics = self._analyze_goal_progress(goal_path)
            analytics_data['goal_snapshots'].append({
                'goal_name': goal_metrics.goal_name,
                'metrics': asdict(goal_metrics)
            })

        with open(self.analytics_file, 'w', encoding='utf-8') as f:
            json.dump(analytics_data, f, indent=2)

        write_success(f"Analytics data saved to {self.analytics_file}")


def main():
    """Main progress tracking function"""
    if not test_git_repo():
        write_error("Not in a git repository")
        write_info("Please run this from the root of a Goal Kit project")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(description='Goal Kit Progress Tracking System')
    parser.add_argument('--json', action='store_true', help='Output report in JSON format')
    parser.add_argument('--save', action='store_true', help='Save analytics data for historical tracking')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')

    args = parser.parse_args()

    try:
        tracker = ProgressTracker()
        report = tracker.generate_progress_report(args.format)

        if args.format == 'json':
            print(report)
        else:
            print(report)

        if args.save:
            tracker.save_analytics_data()

    except Exception as e:
        write_error(f"Error generating progress report: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()