#!/usr/bin/env python3
"""
Workflow Guidance System for Goal Kit
Provides intelligent recommendations for next steps based on project state and task complexity
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

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

try:
    from task_assessor import TaskAssessor
    from status_dashboard import StatusDashboard
    TASK_ASSESSOR_AVAILABLE = True
except ImportError:
    TASK_ASSESSOR_AVAILABLE = False


@dataclass
class WorkflowRecommendation:
    """Recommendation for next workflow steps"""
    primary_action: str
    reasoning: str
    alternatives: List[str]
    effort_estimate: str
    confidence: float


class WorkflowGuide:
    """Intelligent workflow guidance system"""

    def __init__(self, project_root: str = None):
        self.project_root = project_root or get_git_root()
        if not self.project_root:
            raise ValueError("Must be run from a git repository")

        self.assessor = TaskAssessor(self.project_root) if TASK_ASSESSOR_AVAILABLE else None
        self.dashboard = StatusDashboard(self.project_root)

    def get_guidance(self, current_command: str = None, task_description: str = None) -> WorkflowRecommendation:
        """
        Get intelligent workflow guidance based on current state and context

        Args:
            current_command: The command being executed (e.g., 'goal', 'strategies')
            task_description: Description of the task being worked on

        Returns:
            WorkflowRecommendation with guidance
        """
        status = self.dashboard.get_status()

        # Get task assessment if available
        task_assessment = None
        if self.assessor and task_description:
            context = {
                'has_vision': status.vision_status != 'none',
                'recent_goals': status.goal_count,
                'current_milestones': status.active_goals
            }
            task_assessment = self.assessor.assess_task(task_description, context)

        # Base guidance on current state and command
        if current_command == 'vision':
            return self._guidance_after_vision(status)
        elif current_command == 'goal':
            return self._guidance_after_goal(status, task_assessment)
        elif current_command == 'strategies':
            return self._guidance_after_strategies(status)
        elif current_command == 'milestones':
            return self._guidance_after_milestones(status)
        elif current_command == 'execute':
            return self._guidance_after_execute(status)
        else:
            return self._general_guidance(status, task_assessment)

    def _guidance_after_vision(self, status) -> WorkflowRecommendation:
        """Guidance after vision creation"""
        reasoning = "Vision established - ready to define specific goals"

        if status.goal_count == 0:
            primary = "/goalkit.goal - Define your first goal based on the vision"
            alternatives = [
                "/goalkit.goal - Start with the most important goal from your vision",
                "Review vision and identify 2-3 key goals to tackle first"
            ]
        else:
            primary = "/goalkit.goal - Define next priority goal"
            alternatives = [
                "Review existing goals and see if they align with updated vision",
                "/goalkit.goal - Define goals for any gaps identified in vision"
            ]

        return WorkflowRecommendation(
            primary_action=primary,
            reasoning=reasoning,
            alternatives=alternatives,
            effort_estimate="medium",
            confidence=0.9
        )

    def _guidance_after_goal(self, status, task_assessment) -> WorkflowRecommendation:
        """Guidance after goal creation"""
        if task_assessment and task_assessment.complexity == 'simple':
            primary = "/goalkit.execute - Implement directly for this simple goal"
            reasoning = "Simple task detected - can proceed directly to implementation"
            alternatives = [
                "/goalkit.strategies - Explore approaches if you want structure",
                "/goalkit.execute - Quick implementation with basic tracking"
            ]
            effort = "low"
            confidence = task_assessment.confidence
        else:
            primary = "/goalkit.strategies - Explore multiple approaches for this goal"
            reasoning = "Goal defined - explore implementation strategies"
            alternatives = [
                "/goalkit.execute - If you're confident in the approach",
                "/goalkit.strategies - Recommended for complex goals"
            ]
            effort = "medium"
            confidence = 0.8

        return WorkflowRecommendation(
            primary_action=primary,
            reasoning=reasoning,
            alternatives=alternatives,
            effort_estimate=effort,
            confidence=confidence
        )

    def _guidance_after_strategies(self, status) -> WorkflowRecommendation:
        """Guidance after strategy exploration"""
        primary = "/goalkit.milestones - Break goal into measurable progress steps"
        reasoning = "Strategies explored - create milestones for execution"
        alternatives = [
            "/goalkit.execute - If you have clear milestones in mind",
            "/goalkit.milestones - Recommended for structured progress tracking"
        ]

        return WorkflowRecommendation(
            primary_action=primary,
            reasoning=reasoning,
            alternatives=alternatives,
            effort_estimate="medium",
            confidence=0.8
        )

    def _guidance_after_milestones(self, status) -> WorkflowRecommendation:
        """Guidance after milestone creation"""
        primary = "/goalkit.execute - Implement with learning and milestone tracking"
        reasoning = "Milestones defined - ready for adaptive execution"
        alternatives = [
            "Begin implementation following milestone plan",
            "/goalkit.execute - Start with first milestone"
        ]

        return WorkflowRecommendation(
            primary_action=primary,
            reasoning=reasoning,
            alternatives=alternatives,
            effort_estimate="high",
            confidence=0.9
        )

    def _guidance_after_execute(self, status) -> WorkflowRecommendation:
        """Guidance after execution begins"""
        if status.health_score < 70:
            primary = "Continue execution and monitor progress against milestones"
            reasoning = "Execution in progress - focus on learning and adaptation"
            alternatives = [
                "Review milestones and adjust approach based on learnings",
                "Complete current milestone before planning next steps"
            ]
        else:
            primary = "Complete current milestone and plan next steps"
            reasoning = "Good progress - evaluate completion and plan continuation"
            alternatives = [
                "/goalkit.goal - Define new goal if current one is complete",
                "Continue with next milestone in current goal"
            ]

        return WorkflowRecommendation(
            primary_action=primary,
            reasoning=reasoning,
            alternatives=alternatives,
            effort_estimate="variable",
            confidence=0.7
        )

    def _general_guidance(self, status, task_assessment) -> WorkflowRecommendation:
        """General guidance when no specific command context"""
        # Project health-based guidance
        if status.vision_status == 'none':
            primary = "/goalkit.vision - Establish project vision and principles"
            reasoning = "No project vision found - start here for goal-driven development"
            alternatives = [
                "/goalkit.goal - If you have a clear goal in mind",
                "/goalkit.vision - Recommended foundation for structured development"
            ]
            effort = "medium"

        elif status.goal_count == 0:
            primary = "/goalkit.goal - Define your first goal"
            reasoning = "Vision exists but no goals defined yet"
            alternatives = [
                "/goalkit.goal - Start with the most important user outcome",
                "Review vision to identify key goals"
            ]
            effort = "medium"

        elif status.active_goals == 0 and status.completed_goals > 0:
            primary = "/goalkit.goal - Define new goal or revive existing work"
            reasoning = "Previous work completed - ready for new goals"
            alternatives = [
                "/goalkit.goal - Build on successful previous work",
                "Review completed goals for lessons learned"
            ]
            effort = "medium"

        else:
            primary = "/goalkit.execute - Continue with active goals"
            reasoning = "Active work in progress - focus on execution"
            alternatives = [
                "Review current milestone progress",
                "/goalkit.goal - If you have a new goal to add"
            ]
            effort = "variable"

        # Adjust based on task assessment
        if task_assessment and task_assessment.complexity == 'simple':
            primary = f"/goalkit.execute - Handle simple task: {task_assessment.recommended_workflow}"
            reasoning = f"Simple task detected - {task_assessment.reasoning[0] if task_assessment.reasoning else 'can proceed directly'}"
            effort = "low"

        return WorkflowRecommendation(
            primary_action=primary,
            reasoning=reasoning,
            alternatives=alternatives,
            effort_estimate=effort,
            confidence=0.8
        )


def main():
    """CLI interface for workflow guidance"""
    import argparse

    parser = argparse.ArgumentParser(description='Get intelligent workflow guidance for Goal Kit')
    parser.add_argument('--command', help='Current command being executed')
    parser.add_argument('--task', help='Task description for assessment')
    parser.add_argument('--json', action='store_true', help='Output JSON format')

    args = parser.parse_args()

    try:
        guide = WorkflowGuide()
        recommendation = guide.get_guidance(args.command, args.task)

        if args.json:
            result = {
                'guidance': asdict(recommendation),
                'timestamp': datetime.now().isoformat()
            }
            print(json.dumps(result, indent=2))
        else:
            print("🎯 Workflow Guidance")
            print("=" * 30)
            print(f"Recommended: {recommendation.primary_action}")
            print(f"Reasoning: {recommendation.reasoning}")
            print(f"Effort: {recommendation.effort_estimate}")
            print(f"Confidence: {recommendation.confidence:.1%}")
            print()
            print("Alternatives:")
            for alt in recommendation.alternatives:
                print(f"  • {alt}")

    except Exception as e:
        write_error(f"Guidance failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
