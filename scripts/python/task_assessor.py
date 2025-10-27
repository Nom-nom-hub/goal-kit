#!/usr/bin/env python3
"""
Smart Task Assessment for Goal Kit Methodology
Automatically determines appropriate workflow complexity based on task analysis
"""

import os
import sys
import json
import re
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


@dataclass
class TaskAssessment:
    """Assessment result for a task or request"""
    complexity: str  # 'simple', 'moderate', 'complex'
    confidence: float  # 0-1
    reasoning: List[str]
    recommended_workflow: str  # 'direct', 'basic_methodology', 'full_methodology'
    estimated_effort: str  # 'low', 'medium', 'high'
    risk_factors: List[str]
    shortcuts_available: List[str]


class TaskAssessor:
    """Smart assessment system for determining appropriate workflow complexity"""

    def __init__(self, project_root: str = None):
        self.project_root = project_root or get_git_root()
        if not self.project_root:
            raise ValueError("Must be run from a git repository")

    def assess_task(self, task_description: str, context: Dict[str, Any] = None) -> TaskAssessment:
        """
        Assess a task and determine appropriate workflow complexity

        Args:
            task_description: Description of the task to assess
            context: Additional context about current project state

        Returns:
            TaskAssessment with complexity analysis and recommendations
        """
        reasoning = []
        risk_factors = []
        shortcuts = []

        # Analyze task characteristics
        task_lower = task_description.lower()

        # Simple task indicators
        simple_indicators = [
            'fix', 'update', 'change', 'modify', 'add', 'remove', 'correct',
            'styling', 'color', 'font', 'margin', 'padding', 'alignment',
            'text', 'label', 'button', 'link', 'icon', 'image',
            'typo', 'grammar', 'spelling', 'format', 'indent',
            'comment', 'log', 'debug', 'print'
        ]

        # Complex task indicators
        complex_indicators = [
            'feature', 'system', 'architecture', 'design', 'framework',
            'integration', 'api', 'database', 'security', 'authentication',
            'performance', 'scalability', 'optimization', 'migration',
            'refactor', 'rewrite', 'redesign', 'restructure',
            'multi-step', 'coordination', 'collaboration', 'team'
        ]

        # Count indicators
        simple_matches = sum(1 for indicator in simple_indicators if indicator in task_lower)
        complex_matches = sum(1 for indicator in complex_indicators if indicator in task_lower)

        # Length and structure analysis
        word_count = len(task_description.split())
        has_measurements = bool(re.search(r'\d+', task_description))
        has_multiple_steps = task_description.count(',') + task_description.count(';') + task_description.count('and') > 2

        # Determine complexity
        if simple_matches >= 2 and word_count < 20 and not has_multiple_steps:
            complexity = 'simple'
            confidence = 0.8
            workflow = 'direct'
            effort = 'low'
            reasoning.append("Task appears to be a simple, focused change")
            shortcuts.extend(['skip_vision', 'skip_strategies', 'skip_milestones', 'direct_execution'])

        elif complex_matches >= 1 or has_multiple_steps or word_count > 50:
            complexity = 'complex'
            confidence = 0.7
            workflow = 'full_methodology'
            effort = 'high'
            reasoning.append("Task involves complex changes requiring full methodology")
            risk_factors.extend(['high_scope', 'multiple_dependencies', 'coordination_needed'])

        else:
            complexity = 'moderate'
            confidence = 0.6
            workflow = 'basic_methodology'
            effort = 'medium'
            reasoning.append("Task requires some structure but may not need full methodology")
            shortcuts.extend(['skip_vision', 'streamlined_strategies'])

        # Context-based adjustments
        if context:
            if context.get('has_vision', False):
                reasoning.append("Project already has vision established")
                shortcuts.append('use_existing_vision')

            if context.get('recent_goals', 0) > 0:
                reasoning.append("Recent goals exist that may be relevant")
                shortcuts.append('leverage_existing_goals')

            if context.get('current_milestones', 0) > 0:
                reasoning.append("Active milestones suggest ongoing methodology")
                if complexity == 'simple':
                    workflow = 'basic_methodology'  # Respect existing structure

        return TaskAssessment(
            complexity=complexity,
            confidence=confidence,
            reasoning=reasoning,
            recommended_workflow=workflow,
            estimated_effort=effort,
            risk_factors=risk_factors,
            shortcuts_available=shortcuts
        )

    def get_project_context(self) -> Dict[str, Any]:
        """Get current project context for assessment"""
        context = {
            'has_vision': False,
            'goal_count': 0,
            'active_milestones': 0,
            'recent_activity': 0
        }

        # Check for vision file
        vision_path = os.path.join(self.project_root, '.goalkit', 'vision.md')
        context['has_vision'] = os.path.exists(vision_path)

        # Check goals directory
        goals_dir = os.path.join(self.project_root, '.goalkit', 'goals')
        if os.path.exists(goals_dir):
            context['goal_count'] = len([d for d in os.listdir(goals_dir) if os.path.isdir(os.path.join(goals_dir, d))])

            # Check for active milestones
            for goal_dir in os.listdir(goals_dir):
                goal_path = os.path.join(goals_dir, goal_dir)
                if os.path.isdir(goal_path):
                    milestone_file = os.path.join(goal_path, 'milestones.md')
                    if os.path.exists(milestone_file):
                        context['active_milestones'] += 1

        return context


def main():
    """CLI interface for task assessment"""
    import argparse

    parser = argparse.ArgumentParser(description='Assess task complexity for Goal Kit methodology')
    parser.add_argument('task', help='Task description to assess')
    parser.add_argument('--json', action='store_true', help='Output JSON format')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    try:
        assessor = TaskAssessor()
        context = assessor.get_project_context()
        assessment = assessor.assess_task(args.task, context)

        if args.json:
            result = {
                'task': args.task,
                'assessment': asdict(assessment),
                'context': context,
                'timestamp': datetime.now().isoformat()
            }
            print(json.dumps(result, indent=2))
        else:
            print(f"Task: {args.task}")
            print(f"Complexity: {assessment.complexity} (confidence: {assessment.confidence:.1%})")
            print(f"Recommended Workflow: {assessment.recommended_workflow}")
            print(f"Estimated Effort: {assessment.estimated_effort}")
            print()
            print("Reasoning:")
            for reason in assessment.reasoning:
                print(f"  • {reason}")
            print()
            if assessment.shortcuts_available:
                print("Available Shortcuts:")
                for shortcut in assessment.shortcuts_available:
                    print(f"  • {shortcut}")
            if assessment.risk_factors:
                print("Risk Factors:")
                for risk in assessment.risk_factors:
                    print(f"  • {risk}")

    except Exception as e:
        write_error(f"Assessment failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
