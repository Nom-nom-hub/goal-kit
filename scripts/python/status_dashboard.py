#!/usr/bin/env python3
"""
Status Dashboard for Goal Kit Projects
Provides quick overview of project state and next recommended actions
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, cast
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

# Add the common Python utilities
sys.path.append(os.path.dirname(__file__))
from common import (
    write_info,
    write_success,
    write_error,
    write_warning,
    test_git_repo,
    get_git_root
)


@dataclass
class ProjectStatus:
    """Current project status summary"""
    vision_status: str  # 'none', 'present', 'outdated'
    goal_count: int
    active_goals: int
    completed_goals: int
    total_milestones: int
    completed_milestones: int
    recent_activity: List[str]
    next_recommended_actions: List[str]
    health_score: float  # 0-100


class StatusDashboard:
    """Dashboard for monitoring Goal Kit project status"""

    def __init__(self, project_root: Optional[str] = None):
        self.project_root = cast(str, project_root or get_git_root())
        if not self.project_root:
            raise ValueError("Must be run from a git repository")

        self.goalkit_dir = os.path.join(self.project_root, '.goalkit')
        self.goals_dir = os.path.join(self.goalkit_dir, 'goals')
        self.collaborations_dir = os.path.join(self.goalkit_dir, 'collaborations')

    def get_status(self) -> ProjectStatus:
        """Get comprehensive project status"""
        vision_status = self._check_vision_status()
        goals_status = self._check_goals_status()
        milestones_status = self._check_milestones_status()
        activity = self._get_recent_activity()
        actions = self._get_recommended_actions(vision_status, goals_status, milestones_status)
        health = self._calculate_health_score(vision_status, goals_status, milestones_status)

        return ProjectStatus(
            vision_status=vision_status,
            goal_count=goals_status['total'],
            active_goals=goals_status['active'],
            completed_goals=goals_status['completed'],
            total_milestones=milestones_status['total'],
            completed_milestones=milestones_status['completed'],
            recent_activity=activity,
            next_recommended_actions=actions,
            health_score=health
        )

    def _check_vision_status(self) -> str:
        """Check vision file status"""
        vision_file = os.path.join(self.goalkit_dir, 'vision.md')
        if not os.path.exists(vision_file):
            return 'none'

        # Check if vision is recent (within 90 days)
        stat = os.stat(vision_file)
        age_days = (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).days
        return 'present' if age_days <= 90 else 'outdated'

    def _check_goals_status(self) -> Dict[str, int]:
        """Check goals directory status"""
        if not os.path.exists(self.goals_dir):
            return {'total': 0, 'active': 0, 'completed': 0}

        goals = [d for d in os.listdir(self.goals_dir) if os.path.isdir(os.path.join(self.goals_dir, d))]
        active = 0
        completed = 0

        for goal in goals:
            goal_dir = os.path.join(self.goals_dir, goal)
            execution_file = os.path.join(goal_dir, 'execution.md')
            if os.path.exists(execution_file):
                # Simple heuristic: if execution file exists and is recent, consider active
                stat = os.stat(execution_file)
                age_days = (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).days
                if age_days <= 30:  # Active within last month
                    active += 1
                else:
                    completed += 1
            else:
                active += 1  # Goals without execution are considered active

        return {'total': len(goals), 'active': active, 'completed': completed}

    def _check_milestones_status(self) -> Dict[str, int]:
        """Check milestones across all goals"""
        if not os.path.exists(self.goals_dir):
            return {'total': 0, 'completed': 0}

        total_milestones = 0
        completed_milestones = 0

        for goal in os.listdir(self.goals_dir):
            goal_dir = os.path.join(self.goals_dir, goal)
            if not os.path.isdir(goal_dir):
                continue

            milestone_file = os.path.join(goal_dir, 'milestones.md')
            if os.path.exists(milestone_file):
                # Very simple heuristic - count lines that might be milestones
                with open(milestone_file, 'r') as f:
                    content = f.read()
                    # Count bullet points or numbered items as milestones
                    milestone_lines = len([line for line in content.split('\n')
                                         if line.strip().startswith(('- ', '1. ', '2. ', '3. ', '4. ', '5. '))])
                    total_milestones += milestone_lines

                    # Count completed milestones (very rough heuristic)
                    completed_lines = len([line for line in content.split('\n')
                                         if '[x]' in line.lower() or 'completed' in line.lower()])
                    completed_milestones += min(completed_lines, milestone_lines)

        return {'total': total_milestones, 'completed': completed_milestones}

    def _get_recent_activity(self) -> List[str]:
        """Get recent project activity"""
        activity = []

        # Check recent file modifications
        recent_files = []
        for root, dirs, files in os.walk(self.goalkit_dir):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    stat = os.stat(filepath)
                    age_hours = (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).total_seconds() / 3600
                    if age_hours <= 24:  # Within last 24 hours
                        recent_files.append((filepath, age_hours))

        recent_files.sort(key=lambda x: x[1])  # Sort by age

        for filepath, age_hours in recent_files[:5]:  # Top 5 most recent
            rel_path = os.path.relpath(filepath, self.project_root)
            if age_hours < 1:
                activity.append(f"Modified {rel_path} ({age_hours:.1f} hours ago)")
            else:
                activity.append(f"Modified {rel_path} ({int(age_hours)} hours ago)")

        if not activity:
            activity.append("No recent activity in the last 24 hours")

        return activity

    def _get_recommended_actions(self, vision_status: str, goals_status: Dict, milestones_status: Dict) -> List[str]:
        """Get recommended next actions based on current state"""
        actions = []

        if vision_status == 'none':
            actions.append("Create project vision with /goalkit.vision")
        elif vision_status == 'outdated':
            actions.append("Review and update project vision")

        if goals_status['total'] == 0:
            actions.append("Define your first goal with /goalkit.goal")
        elif goals_status['active'] == 0 and goals_status['total'] > 0:
            actions.append("Start working on existing goals or create new ones")

        if milestones_status['total'] > 0 and milestones_status['completed'] < milestones_status['total']:
            actions.append("Continue working toward milestone completion")

        if not actions:
            actions.append("Project is well-structured - consider defining new goals or reviewing progress")

        return actions

    def _calculate_health_score(self, vision_status: str, goals_status: Dict, milestones_status: Dict) -> float:
        """Calculate project health score (0-100)"""
        score = 0

        # Vision contributes 20 points
        if vision_status == 'present':
            score += 20
        elif vision_status == 'outdated':
            score += 10

        # Goals structure contributes 30 points
        if goals_status['total'] > 0:
            score += 15  # Having goals
            if goals_status['active'] > 0:
                score += 15  # Having active work

        # Milestone progress contributes 30 points
        if milestones_status['total'] > 0:
            completion_rate = milestones_status['completed'] / milestones_status['total']
            score += 30 * completion_rate

        # Methodology adherence contributes 20 points (simplified)
        has_structure = (vision_status != 'none' and goals_status['total'] > 0)
        if has_structure:
            score += 20

        return min(100, score)


def main():
    """CLI interface for status dashboard"""
    import argparse

    parser = argparse.ArgumentParser(description='Goal Kit project status dashboard')
    parser.add_argument('--json', action='store_true', help='Output JSON format')
    parser.add_argument('--detailed', action='store_true', help='Show detailed status')

    args = parser.parse_args()

    try:
        dashboard = StatusDashboard()
        status = dashboard.get_status()

        if args.json:
            result = {
                'status': asdict(status),
                'timestamp': datetime.now().isoformat()
            }
            print(json.dumps(result, indent=2))
        else:
            print("🎯 Goal Kit Project Status")
            print("=" * 40)

            # Health score
            health_color = "🟢" if status.health_score >= 80 else "🟡" if status.health_score >= 60 else "🔴"
            print(f"Health Score: {health_color} {status.health_score:.1f}/100")

            print(f"\n📋 Project Structure:")
            vision_icon = "✅" if status.vision_status == 'present' else "⚠️" if status.vision_status == 'outdated' else "❌"
            print(f"  Vision: {vision_icon} {status.vision_status}")
            print(f"  Goals: {status.goal_count} total ({status.active_goals} active, {status.completed_goals} completed)")
            print(f"  Milestones: {status.total_milestones} total ({status.completed_milestones} completed)")

            print(f"\n📈 Recent Activity:")
            for activity in status.recent_activity:
                print(f"  • {activity}")

            print(f"\n🎯 Next Recommended Actions:")
            for action in status.next_recommended_actions:
                print(f"  • {action}")

            if args.detailed:
                print(f"\n📊 Detailed Metrics:")
                if status.total_milestones > 0:
                    completion_rate = status.completed_milestones / status.total_milestones * 100
                    print(f"  Milestone Completion: {completion_rate:.1f}%")
                print(f"  Active Goals Ratio: {status.active_goals}/{status.goal_count}")

    except Exception as e:
        write_error(f"Status check failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
