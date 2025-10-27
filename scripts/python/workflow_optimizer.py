#!/usr/bin/env python3
"""
Workflow Optimizer for Goal Kit
Analyzes and optimizes the methodology workflow based on project patterns and user feedback
"""

import os
import sys
import json
import statistics
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
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

try:
    from task_assessor import TaskAssessor
    from status_dashboard import StatusDashboard
    from workflow_guide import WorkflowGuide
    FULL_OPTIMIZATION = True
except ImportError:
    FULL_OPTIMIZATION = False


@dataclass
class OptimizationInsight:
    """Insight from workflow optimization analysis"""
    category: str  # 'efficiency', 'quality', 'adoption', 'complexity'
    title: str
    description: str
    impact_score: float  # 1-10
    confidence: float  # 0-1
    recommendation: str
    implementation_effort: str


@dataclass
class WorkflowOptimizationReport:
    """Comprehensive workflow optimization analysis"""
    project_name: str
    analysis_timestamp: str
    current_efficiency_score: float
    optimization_opportunities: List[OptimizationInsight]
    workflow_patterns: Dict[str, Any]
    success_metrics: Dict[str, Any]
    recommendations: List[str]


class WorkflowOptimizer:
    """Workflow optimization and analysis system"""

    def __init__(self, project_root: str = None):
        self.project_root = project_root or get_git_root()
        if not self.project_root:
            raise ValueError("Must be run from a git repository")

        self.optimization_dir = os.path.join(self.project_root, '.goalkit', 'optimization')
        os.makedirs(self.optimization_dir, exist_ok=True)

        # Initialize components if available
        self.assessor = TaskAssessor(self.project_root) if FULL_OPTIMIZATION else None
        self.dashboard = StatusDashboard(self.project_root) if FULL_OPTIMIZATION else None
        self.guide = WorkflowGuide(self.project_root) if FULL_OPTIMIZATION else None

    def analyze_workflow(self) -> WorkflowOptimizationReport:
        """Analyze current workflow and identify optimization opportunities"""
        insights = []
        patterns = {}
        metrics = {}

        # Basic project metrics
        status = self.dashboard.get_status() if self.dashboard else None

        if status:
            patterns['project_health'] = status.health_score
            patterns['goal_completion_rate'] = (
                status.completed_goals / status.goal_count if status.goal_count > 0 else 0
            )
            patterns['milestone_completion_rate'] = (
                status.completed_milestones / status.total_milestones if status.total_milestones > 0 else 0
            )

        # Analyze methodology adherence
        methodology_insights = self._analyze_methodology_adherence()
        insights.extend(methodology_insights)

        # Analyze efficiency patterns
        efficiency_insights = self._analyze_efficiency_patterns()
        insights.extend(efficiency_insights)

        # Analyze complexity distribution
        complexity_insights = self._analyze_complexity_distribution()
        insights.extend(complexity_insights)

        # Calculate current efficiency score
        efficiency_score = self._calculate_efficiency_score(insights)

        # Generate recommendations
        recommendations = self._generate_recommendations(insights)

        return WorkflowOptimizationReport(
            project_name=os.path.basename(self.project_root),
            analysis_timestamp=datetime.now().isoformat(),
            current_efficiency_score=efficiency_score,
            optimization_opportunities=insights,
            workflow_patterns=patterns,
            success_metrics=metrics,
            recommendations=recommendations
        )

    def _analyze_methodology_adherence(self) -> List[OptimizationInsight]:
        """Analyze how well the methodology is being followed"""
        insights = []

        # Check for common methodology violations
        if self.dashboard:
            status = self.dashboard.get_status()

            # Check if simple tasks are using full methodology
            if status.goal_count > 0 and status.total_milestones == 0:
                insights.append(OptimizationInsight(
                    category='efficiency',
                    title='Potential Methodology Overuse',
                    description='Goals exist without milestones, suggesting simple tasks may be over-engineered',
                    impact_score=6.0,
                    confidence=0.7,
                    recommendation='Consider direct execution for simple goals without full milestone planning',
                    implementation_effort='low'
                ))

            # Check for methodology gaps
            if status.vision_status == 'none' and status.goal_count > 3:
                insights.append(OptimizationInsight(
                    category='quality',
                    title='Missing Vision Foundation',
                    description='Multiple goals exist without project vision for alignment',
                    impact_score=8.0,
                    confidence=0.9,
                    recommendation='Establish project vision to ensure goal alignment',
                    implementation_effort='medium'
                ))

        return insights

    def _analyze_efficiency_patterns(self) -> List[OptimizationInsight]:
        """Analyze workflow efficiency patterns"""
        insights = []

        # Check for rapid goal completion (potential for shortcuts)
        if self.dashboard:
            status = self.dashboard.get_status()
            if status.completed_goals > 0 and status.total_milestones < status.completed_goals * 2:
                insights.append(OptimizationInsight(
                    category='efficiency',
                    title='Efficient Simple Task Handling',
                    description='Goals completed with minimal milestones suggest effective simple task processing',
                    impact_score=7.0,
                    confidence=0.8,
                    recommendation='Continue using direct execution for similar simple tasks',
                    implementation_effort='low'
                ))

        # Template usage efficiency
        insights.append(OptimizationInsight(
            category='efficiency',
            title='Streamlined Template Usage',
            description='Templates can be optimized for common usage patterns',
            impact_score=5.0,
            confidence=0.6,
            recommendation='Use smart assessment to route users to appropriate template complexity',
            implementation_effort='medium'
        ))

        return insights

    def _analyze_complexity_distribution(self) -> List[OptimizationInsight]:
        """Analyze the distribution of task complexities"""
        insights = []

        # Placeholder for complexity analysis
        insights.append(OptimizationInsight(
            category='complexity',
            title='Task Complexity Awareness',
            description='Implement smart task assessment to match methodology complexity to task needs',
            impact_score=9.0,
            confidence=0.8,
            recommendation='Use automated task assessment to recommend appropriate workflow depth',
            implementation_effort='medium'
        ))

        return insights

    def _calculate_efficiency_score(self, insights: List[OptimizationInsight]) -> float:
        """Calculate overall workflow efficiency score"""
        if not insights:
            return 75.0  # Default good score

        # Weight insights by impact and confidence
        weighted_score = 0
        total_weight = 0

        for insight in insights:
            weight = insight.impact_score * insight.confidence
            # Efficiency insights positively affect score, others may negatively affect
            if insight.category == 'efficiency':
                weighted_score += weight * 1.2  # Bonus for efficiency
            elif insight.category == 'quality':
                weighted_score += weight * 0.9  # Slight penalty for quality issues
            else:
                weighted_score += weight

            total_weight += weight

        if total_weight == 0:
            return 75.0

        # Normalize to 0-100 scale (higher is better)
        efficiency_score = min(100, max(0, 80 + (weighted_score / total_weight - 5) * 10))
        return round(efficiency_score, 1)

    def _generate_recommendations(self, insights: List[OptimizationInsight]) -> List[str]:
        """Generate actionable recommendations from insights"""
        recommendations = []

        # Sort insights by impact score
        sorted_insights = sorted(insights, key=lambda x: x.impact_score, reverse=True)

        for insight in sorted_insights[:5]:  # Top 5 insights
            recommendations.append(f"{insight.title}: {insight.recommendation}")

        # Add general recommendations
        recommendations.extend([
            "Implement smart task assessment for automatic complexity routing",
            "Use status dashboard for better project awareness",
            "Streamline templates based on usage patterns",
            "Gather user feedback on workflow friction points"
        ])

        return recommendations

    def get_workflow_guidance(self, task_description: str = None) -> Dict[str, Any]:
        """Get intelligent workflow guidance"""
        guidance = {
            'assessment': {},
            'status': {},
            'recommendations': {},
            'next_steps': []
        }

        if self.assessor and task_description:
            assessment = self.assessor.assess_task(task_description)
            guidance['assessment'] = asdict(assessment)

        if self.dashboard:
            status = self.dashboard.get_status()
            guidance['status'] = asdict(status)

        if self.guide:
            recommendation = self.guide.get_guidance(task_description=task_description)
            guidance['recommendations'] = asdict(recommendation)

        # Generate next steps based on guidance
        if guidance['assessment'].get('complexity') == 'simple':
            guidance['next_steps'].append('/goalkit.execute - Direct implementation for simple task')
        elif guidance['status'].get('vision_status') == 'none':
            guidance['next_steps'].append('/goalkit.vision - Establish project foundation')
        else:
            guidance['next_steps'].append('/goalkit.goal - Define clear objectives')

        return guidance


def main():
    """CLI interface for workflow optimization"""
    import argparse

    parser = argparse.ArgumentParser(description='Goal Kit workflow optimization and analysis')
    parser.add_argument('--analyze', action='store_true', help='Run full workflow analysis')
    parser.add_argument('--guide', action='store_true', help='Get workflow guidance')
    parser.add_argument('--task', help='Task description for guidance')
    parser.add_argument('--json', action='store_true', help='Output JSON format')

    args = parser.parse_args()

    try:
        optimizer = WorkflowOptimizer()

        if args.analyze:
            report = optimizer.analyze_workflow()

            if args.json:
                result = {
                    'optimization_report': asdict(report),
                    'timestamp': datetime.now().isoformat()
                }
                print(json.dumps(result, indent=2))
            else:
                print("🔧 Workflow Optimization Report")
                print("=" * 40)
                print(f"Project: {report.project_name}")
                print(f"Efficiency Score: {report.current_efficiency_score:.1f}/100")

                print(f"\n📊 Key Insights:")
                for insight in report.optimization_opportunities[:3]:
                    print(f"  • {insight.title} (Impact: {insight.impact_score:.1f})")
                    print(f"    {insight.description}")

                print(f"\n🎯 Recommendations:")
                for rec in report.recommendations[:3]:
                    print(f"  • {rec}")

        elif args.guide:
            guidance = optimizer.get_workflow_guidance(args.task)

            if args.json:
                result = {
                    'workflow_guidance': guidance,
                    'timestamp': datetime.now().isoformat()
                }
                print(json.dumps(result, indent=2))
            else:
                print("🎯 Workflow Guidance")
                print("=" * 30)

                if guidance.get('assessment'):
                    assessment = guidance['assessment']
                    print(f"Task Complexity: {assessment.get('complexity', 'unknown')}")
                    print(f"Recommended Workflow: {assessment.get('recommended_workflow', 'unknown')}")

                if guidance.get('status'):
                    status = guidance['status']
                    print(f"Project Health: {status.get('health_score', 0):.1f}/100")
                    print(f"Active Goals: {status.get('active_goals', 0)}")

                print(f"\nNext Steps:")
                for step in guidance.get('next_steps', []):
                    print(f"  • {step}")

        else:
            # Default: show status
            if FULL_OPTIMIZATION:
                guidance = optimizer.get_workflow_guidance()
                print("🎯 Goal Kit Workflow Status")
                print("=" * 35)
                print(f"Optimization Available: ✅ Full feature set")
                print(f"Project Health: {guidance['status'].get('health_score', 0):.1f}/100")
                print(f"Active Goals: {guidance['status'].get('active_goals', 0)}")
                print("\nQuick Commands:")
                print("  /goalkit.smart [task]  - Assess task complexity")
                print("  python scripts/python/status_dashboard.py - Project overview")
                print("  python scripts/python/workflow_guide.py --task 'description' - Get guidance")
            else:
                print("⚠️  Limited optimization features available")
                print("Install full dependencies for complete workflow optimization")

    except Exception as e:
        write_error(f"Optimization failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
