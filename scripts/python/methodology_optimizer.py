#!/usr/bin/env python3
"""
Methodology Optimization Framework for Goal Kit
Continuous improvement system that optimizes the Goal Kit methodology itself
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
class MethodologyMetric:
    """Metrics for evaluating methodology effectiveness"""
    metric_id: str
    name: str
    description: str
    current_value: float
    target_value: float
    unit: str  # 'percentage', 'score', 'count', 'days', 'ratio'
    trend: str  # 'improving', 'declining', 'stable'
    last_updated: str
    source: str  # 'validation', 'progress', 'learning', 'collaboration'


@dataclass
class MethodologyInsight:
    """Insights about methodology effectiveness and improvement opportunities"""
    insight_id: str
    category: str  # 'process', 'quality', 'efficiency', 'effectiveness', 'usability'
    title: str
    description: str
    evidence: List[str]
    impact_assessment: str  # 'high', 'medium', 'low'
    implementation_complexity: str  # 'low', 'medium', 'high'
    affected_components: List[str]
    related_metrics: List[str]
    created_date: str


@dataclass
class OptimizationProposal:
    """Specific proposal for methodology optimization"""
    proposal_id: str
    title: str
    problem_statement: str
    proposed_solution: str
    expected_benefits: List[str]
    implementation_steps: List[str]
    success_criteria: List[str]
    risk_assessment: Dict[str, Any]
    priority_score: float  # 0-10
    estimated_effort: str  # 'low', 'medium', 'high'
    created_date: str


class MethodologyOptimizer:
    """Continuous improvement system for Goal Kit methodology"""

    def __init__(self, project_root: Optional[str] = None):
        self.project_root = project_root or get_git_root()
        if not self.project_root:
            raise ValueError("Must be run from a git repository")

        self.optimization_dir = os.path.join(self.project_root, ".goalkit", "optimization")
        self.metrics_file = os.path.join(self.optimization_dir, "methodology_metrics.json")
        self.insights_file = os.path.join(self.optimization_dir, "methodology_insights.json")
        self.proposals_file = os.path.join(self.optimization_dir, "optimization_proposals.json")

        # Create optimization directory if it doesn't exist
        os.makedirs(self.optimization_dir, exist_ok=True)

        # Load existing data from all Phase 1 & 2 systems
        self.methodology_data = self._collect_methodology_data()

    def _collect_methodology_data(self) -> Dict[str, Any]:
        """Collect data from all methodology systems for analysis"""
        data = {
            'validation': self._get_validation_data(),
            'progress': self._get_progress_data(),
            'learning': self._get_learning_data(),
            'collaboration': self._get_collaboration_data(),
            'timestamp': datetime.now().isoformat()
        }

        return data

    def _get_validation_data(self) -> Dict[str, Any]:
        """Get validation data for methodology analysis"""
        try:
            import subprocess
            result = subprocess.run([
                sys.executable, "scripts/python/enhanced_validator.py", "--json"
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return json.loads(result.stdout)
        except:
            pass

        return {}

    def _get_progress_data(self) -> Dict[str, Any]:
        """Get progress data for methodology analysis"""
        try:
            import subprocess
            result = subprocess.run([
                sys.executable, "scripts/python/progress_tracker.py", "--json"
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return json.loads(result.stdout)
        except:
            pass

        return {}

    def _get_learning_data(self) -> Dict[str, Any]:
        """Get learning data for methodology analysis"""
        try:
            import subprocess
            result = subprocess.run([
                sys.executable, "scripts/python/learning_system.py", "--report", "--json"
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return json.loads(result.stdout)
        except:
            pass

        return {}

    def _get_collaboration_data(self) -> Dict[str, Any]:
        """Get collaboration data for methodology analysis"""
        try:
            import subprocess
            result = subprocess.run([
                sys.executable, "scripts/python/collaboration_hub.py", "--report", "--json"
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return json.loads(result.stdout)
        except:
            pass

        return {}

    def analyze_methodology_effectiveness(self) -> Dict[str, Any]:
        """Analyze overall methodology effectiveness and identify improvement areas"""
        analysis = {
            'methodology_health': 'unknown',
            'effectiveness_score': 0.0,
            'efficiency_score': 0.0,
            'quality_score': 0.0,
            'learning_score': 0.0,
            'collaboration_score': 0.0,
            'key_insights': [],
            'improvement_areas': [],
            'optimization_opportunities': []
        }

        # Calculate effectiveness scores
        analysis['effectiveness_score'] = self._calculate_effectiveness_score()
        analysis['efficiency_score'] = self._calculate_efficiency_score()
        analysis['quality_score'] = self._calculate_quality_score()
        analysis['learning_score'] = self._calculate_learning_score()
        analysis['collaboration_score'] = self._calculate_collaboration_score()

        # Overall methodology health
        overall_score = sum([
            analysis['effectiveness_score'],
            analysis['efficiency_score'],
            analysis['quality_score'],
            analysis['learning_score'],
            analysis['collaboration_score']
        ]) / 5

        if overall_score >= 8.0:
            analysis['methodology_health'] = 'excellent'
        elif overall_score >= 6.0:
            analysis['methodology_health'] = 'good'
        elif overall_score >= 4.0:
            analysis['methodology_health'] = 'needs_improvement'
        else:
            analysis['methodology_health'] = 'critical'

        # Generate insights and opportunities
        analysis['key_insights'] = self._generate_methodology_insights()
        analysis['improvement_areas'] = self._identify_improvement_areas()
        analysis['optimization_opportunities'] = self._generate_optimization_opportunities()

        return analysis

    def _calculate_effectiveness_score(self) -> float:
        """Calculate methodology effectiveness score"""
        score = 5.0  # Base score

        # Use progress data for effectiveness
        if self.methodology_data['progress']:
            progress_data = self.methodology_data['progress']
            if 'project_analytics' in progress_data:
                analytics = progress_data['project_analytics']
                completion = analytics.get('overall_completion', 0)
                velocity = analytics.get('project_velocity', 5.0)

                # Higher completion and velocity = higher effectiveness
                score += (completion / 100) * 3  # Up to +3 points
                score += (velocity / 10) * 2     # Up to +2 points

        return min(score, 10.0)

    def _calculate_efficiency_score(self) -> float:
        """Calculate methodology efficiency score"""
        score = 5.0  # Base score

        # Use learning data for efficiency (more insights = more efficient learning)
        if self.methodology_data['learning']:
            learning_data = self.methodology_data['learning']
            insights_count = learning_data.get('total_insights', 0)
            patterns_count = learning_data.get('total_patterns', 0)

            # More insights and patterns = higher efficiency
            score += min(insights_count * 0.5, 3)  # Up to +3 points
            score += min(patterns_count * 0.4, 2)  # Up to +2 points

        return min(score, 10.0)

    def _calculate_quality_score(self) -> float:
        """Calculate methodology quality score"""
        score = 5.0  # Base score

        # Use validation data for quality
        if self.methodology_data['validation']:
            validation_data = self.methodology_data['validation']
            if 'validation_results' in validation_data:
                results = validation_data['validation_results']
                if results:
                    # Average quality score across all components
                    scores = [r.get('overall_score', 0) for r in results]
                    avg_score = sum(scores) / len(scores)
                    score = avg_score

        return min(score, 10.0)

    def _calculate_learning_score(self) -> float:
        """Calculate methodology learning score"""
        score = 5.0  # Base score

        # Use learning data for learning effectiveness
        if self.methodology_data['learning']:
            learning_data = self.methodology_data['learning']
            insights = learning_data.get('recent_insights', [])

            # More recent insights = higher learning score
            recent_insights = len([i for i in insights if self._is_recent_insight(i)])
            score += min(recent_insights * 1.0, 5)  # Up to +5 points

        return min(score, 10.0)

    def _calculate_collaboration_score(self) -> float:
        """Calculate methodology collaboration score"""
        score = 5.0  # Base score

        # Use collaboration data for collaboration effectiveness
        if self.methodology_data['collaboration']:
            collaboration_data = self.methodology_data['collaboration']
            similarities = collaboration_data.get('goal_similarities', [])

            # More similarities = higher collaboration potential
            high_potential = len([s for s in similarities if s.get('collaboration_potential') == 'high'])
            score += min(high_potential * 1.5, 5)  # Up to +5 points

        return min(score, 10.0)

    def _is_recent_insight(self, insight: Dict) -> bool:
        """Check if insight is recent (within last 7 days)"""
        try:
            insight_date = datetime.fromisoformat(insight.get('created_date', ''))
            days_since = (datetime.now() - insight_date).days
            return days_since <= 7
        except:
            return False

    def _generate_methodology_insights(self) -> List[str]:
        """Generate insights about methodology effectiveness"""
        insights = []

        # Quality insights
        if self.methodology_data['validation']:
            validation_results = self.methodology_data['validation'].get('validation_results', [])
            if validation_results:
                avg_score = sum(r.get('overall_score', 0) for r in validation_results) / len(validation_results)
                if avg_score >= 8.0:
                    insights.append(f"High-quality methodology execution with average score of {avg_score:.1f}/10")
                elif avg_score < 6.0:
                    insights.append(f"Quality issues detected with average score of {avg_score:.1f}/10 - review and improve")

        # Progress insights
        if self.methodology_data['progress']:
            progress_data = self.methodology_data['progress']
            if 'project_analytics' in progress_data:
                analytics = progress_data['project_analytics']
                completion = analytics.get('overall_completion', 0)
                if completion > 0:
                    insights.append(f"Project is {completion:.1f}% complete with current trajectory")

        # Learning insights
        if self.methodology_data['learning']:
            learning_data = self.methodology_data['learning']
            insights_count = learning_data.get('total_insights', 0)
            if insights_count > 0:
                insights.append(f"Captured {insights_count} learning insights for continuous improvement")

        # Collaboration insights
        if self.methodology_data['collaboration']:
            collaboration_data = self.methodology_data['collaboration']
            similarities = collaboration_data.get('goal_similarities', [])
            if similarities:
                insights.append(f"Identified {len(similarities)} collaboration opportunities between goals")

        return insights if insights else ["Limited data available for methodology analysis - continue using Goal Kit to build insights"]

    def _identify_improvement_areas(self) -> List[str]:
        """Identify specific areas for methodology improvement"""
        areas = []

        # Quality improvement areas
        if self.methodology_data['validation']:
            low_quality = [r for r in self.methodology_data['validation'].get('validation_results', [])
                          if r.get('overall_score', 10) < 7.0]
            if low_quality:
                areas.append(f"Quality improvement needed for {len(low_quality)} components")

        # Progress improvement areas
        if self.methodology_data['progress']:
            progress_data = self.methodology_data['progress']
            if 'project_analytics' in progress_data:
                analytics = progress_data['project_analytics']
                risk_score = analytics.get('risk_score', 5.0)
                if risk_score > 7.0:
                    areas.append("High-risk goals need attention and risk mitigation")

        # Learning improvement areas
        if self.methodology_data['learning']:
            learning_data = self.methodology_data['learning']
            insights_count = learning_data.get('total_insights', 0)
            if insights_count < 5:
                areas.append("Increase learning capture for better methodology intelligence")

        # Collaboration improvement areas
        if self.methodology_data['collaboration']:
            collaboration_data = self.methodology_data['collaboration']
            similarities = collaboration_data.get('goal_similarities', [])
            if not similarities:
                areas.append("Explore collaboration opportunities between goals")

        return areas if areas else ["Methodology performing well - maintain current practices"]

    def _generate_optimization_opportunities(self) -> List[str]:
        """Generate optimization opportunities for methodology"""
        opportunities = []

        # Quality optimization
        if self.methodology_data['validation']:
            validation_results = self.methodology_data['validation'].get('validation_results', [])
            if validation_results:
                # Look for patterns in validation issues
                common_issues = self._identify_common_validation_issues(validation_results)
                if common_issues:
                    opportunities.append(f"Address common quality issues: {', '.join(common_issues[:3])}")

        # Efficiency optimization
        if self.methodology_data['progress']:
            progress_data = self.methodology_data['progress']
            if 'project_analytics' in progress_data:
                analytics = progress_data['project_analytics']
                velocity = analytics.get('project_velocity', 5.0)
                if velocity < 5.0:
                    opportunities.append("Optimize milestone completion velocity and resource allocation")

        # Learning optimization
        if self.methodology_data['learning']:
            learning_data = self.methodology_data['learning']
            patterns = learning_data.get('total_patterns', 0)
            if patterns > 0:
                opportunities.append("Leverage identified patterns for process standardization")

        return opportunities if opportunities else ["Continue current methodology practices - no specific optimizations identified"]

    def _identify_common_validation_issues(self, validation_results: List[Dict]) -> List[str]:
        """Identify common issues across validation results"""
        all_issues = []

        for result in validation_results:
            issues = result.get('issues', [])
            all_issues.extend(issues)

        # Count issue frequency
        issue_counts = defaultdict(int)
        for issue in all_issues:
            issue_counts[issue] += 1

        # Return most common issues
        common_issues = [issue for issue, count in issue_counts.items() if count > 1]
        return common_issues

    def generate_optimization_proposals(self) -> List[OptimizationProposal]:
        """Generate specific optimization proposals for methodology improvement"""
        proposals = []

        # Quality optimization proposal
        quality_proposal = self._generate_quality_optimization_proposal()
        if quality_proposal:
            proposals.append(quality_proposal)

        # Efficiency optimization proposal
        efficiency_proposal = self._generate_efficiency_optimization_proposal()
        if efficiency_proposal:
            proposals.append(efficiency_proposal)

        # Learning optimization proposal
        learning_proposal = self._generate_learning_optimization_proposal()
        if learning_proposal:
            proposals.append(learning_proposal)

        # Collaboration optimization proposal
        collaboration_proposal = self._generate_collaboration_optimization_proposal()
        if collaboration_proposal:
            proposals.append(collaboration_proposal)

        # Sort by priority score
        proposals.sort(key=lambda x: x.priority_score, reverse=True)

        # Save proposals
        self._save_optimization_proposals(proposals)

        return proposals

    def _generate_quality_optimization_proposal(self) -> Optional[OptimizationProposal]:
        """Generate quality optimization proposal"""
        if not self.methodology_data['validation']:
            return None

        validation_results = self.methodology_data['validation'].get('validation_results', [])
        if not validation_results:
            return None

        avg_score = sum(r.get('overall_score', 0) for r in validation_results) / len(validation_results)

        if avg_score >= 8.0:
            return None  # No quality optimization needed

        proposal = OptimizationProposal(
            proposal_id=f"quality_opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=f"Improve methodology quality from {avg_score:.1f}/10 to 8.0+",
            problem_statement=f"Current average quality score of {avg_score:.1f}/10 indicates room for improvement in methodology execution.",
            proposed_solution="Implement enhanced quality assurance processes with automated validation and continuous improvement loops.",
            expected_benefits=[
                "Higher goal success rates",
                "Better stakeholder alignment",
                "Reduced execution risks",
                "Improved team confidence"
            ],
            implementation_steps=[
                "Deploy enhanced validation system",
                "Establish quality gates in workflow",
                "Train team on quality standards",
                "Implement continuous quality monitoring",
                "Create quality improvement feedback loops"
            ],
            success_criteria=[
                "Average quality score of 8.0+ across all components",
                "Zero components with quality scores below 6.0",
                "Consistent quality improvement over time",
                "Team adoption of quality standards"
            ],
            risk_assessment={
                'time_risk': 'medium',
                'resource_risk': 'low',
                'change_risk': 'low',
                'benefit_risk': 'high'
            },
            priority_score=8.5 if avg_score < 6.0 else 6.5,
            estimated_effort='medium',
            created_date=datetime.now().isoformat()
        )

        return proposal

    def _generate_efficiency_optimization_proposal(self) -> Optional[OptimizationProposal]:
        """Generate efficiency optimization proposal"""
        if not self.methodology_data['progress']:
            return None

        progress_data = self.methodology_data['progress']
        if 'project_analytics' not in progress_data:
            return None

        analytics = progress_data['project_analytics']
        velocity = analytics.get('project_velocity', 5.0)

        if velocity >= 7.0:
            return None  # No efficiency optimization needed

        proposal = OptimizationProposal(
            proposal_id=f"efficiency_opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=f"Improve methodology efficiency and velocity from {velocity}/10 to 7.0+",
            problem_statement=f"Current project velocity of {velocity}/10 indicates potential efficiency improvements in methodology execution.",
            proposed_solution="Optimize milestone definitions, improve resource allocation, and implement progress acceleration techniques.",
            expected_benefits=[
                "Faster time to market",
                "Improved resource utilization",
                "Better team productivity",
                "Enhanced stakeholder satisfaction"
            ],
            implementation_steps=[
                "Analyze current milestone completion patterns",
                "Optimize milestone granularity and dependencies",
                "Implement progress tracking and bottleneck identification",
                "Create efficiency improvement feedback loops",
                "Establish velocity optimization processes"
            ],
            success_criteria=[
                "Project velocity of 7.0+",
                "Reduced milestone completion time by 20%",
                "Improved resource utilization metrics",
                "Enhanced team satisfaction scores"
            ],
            risk_assessment={
                'time_risk': 'low',
                'resource_risk': 'medium',
                'change_risk': 'medium',
                'benefit_risk': 'high'
            },
            priority_score=7.0 if velocity < 4.0 else 5.0,
            estimated_effort='medium',
            created_date=datetime.now().isoformat()
        )

        return proposal

    def _generate_learning_optimization_proposal(self) -> Optional[OptimizationProposal]:
        """Generate learning optimization proposal"""
        if not self.methodology_data['learning']:
            return None

        learning_data = self.methodology_data['learning']
        insights_count = learning_data.get('total_insights', 0)

        if insights_count >= 10:
            return None  # Sufficient learning capture

        proposal = OptimizationProposal(
            proposal_id=f"learning_opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title="Establish systematic learning capture and knowledge management",
            problem_statement=f"Only {insights_count} learning insights captured. Systematic learning capture is essential for methodology optimization.",
            proposed_solution="Implement structured learning capture processes with automated retrospective generation and pattern recognition.",
            expected_benefits=[
                "Accelerated project learning",
                "Reduced repeated mistakes",
                "Improved decision-making quality",
                "Enhanced team knowledge base"
            ],
            implementation_steps=[
                "Deploy automated learning capture system",
                "Establish regular retrospective processes",
                "Implement pattern recognition and analysis",
                "Create knowledge sharing mechanisms",
                "Build learning feedback loops"
            ],
            success_criteria=[
                "10+ learning insights captured per month",
                "Pattern recognition system operational",
                "Reduced issue recurrence by 30%",
                "Improved team learning satisfaction"
            ],
            risk_assessment={
                'time_risk': 'medium',
                'resource_risk': 'low',
                'change_risk': 'low',
                'benefit_risk': 'high'
            },
            priority_score=8.0 if insights_count < 3 else 6.0,
            estimated_effort='low',
            created_date=datetime.now().isoformat()
        )

        return proposal

    def _generate_collaboration_optimization_proposal(self) -> Optional[OptimizationProposal]:
        """Generate collaboration optimization proposal"""
        if not self.methodology_data['collaboration']:
            return None

        collaboration_data = self.methodology_data['collaboration']
        similarities = collaboration_data.get('goal_similarities', [])
        high_potential = len([s for s in similarities if s.get('collaboration_potential') == 'high'])

        if high_potential == 0:
            return None  # No collaboration opportunities

        proposal = OptimizationProposal(
            proposal_id=f"collaboration_opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=f"Enable knowledge sharing for {high_potential} high-potential goal pairs",
            problem_statement=f"Identified {high_potential} high-potential collaboration opportunities that are not being leveraged.",
            proposed_solution="Implement structured knowledge sharing processes with automated similarity detection and collaboration facilitation.",
            expected_benefits=[
                "Reduced duplication of effort",
                "Accelerated learning across goals",
                "Improved overall project efficiency",
                "Enhanced team collaboration culture"
            ],
            implementation_steps=[
                "Deploy collaboration hub system",
                "Implement automated similarity detection",
                "Establish knowledge sharing workflows",
                "Create collaboration tracking and metrics",
                "Build cross-goal communication channels"
            ],
            success_criteria=[
                "Successful knowledge transfers between similar goals",
                "Reduced goal completion time through collaboration",
                "Improved cross-team knowledge sharing",
                "Increased collaboration satisfaction scores"
            ],
            risk_assessment={
                'time_risk': 'low',
                'resource_risk': 'medium',
                'change_risk': 'medium',
                'benefit_risk': 'medium'
            },
            priority_score=7.0,
            estimated_effort='medium',
            created_date=datetime.now().isoformat()
        )

        return proposal

    def _save_optimization_proposals(self, proposals: List[OptimizationProposal]):
        """Save optimization proposals for review and implementation"""
        proposals_data = [asdict(p) for p in proposals]

        with open(self.proposals_file, 'w', encoding='utf-8') as f:
            json.dump(proposals_data, f, indent=2)

    def generate_optimization_report(self, output_format: str = 'text') -> str:
        """Generate comprehensive methodology optimization report"""
        methodology_analysis = self.analyze_methodology_effectiveness()
        optimization_proposals = self.generate_optimization_proposals()

        if output_format == 'json':
            report_data = {
                'methodology_analysis': methodology_analysis,
                'optimization_proposals': [asdict(p) for p in optimization_proposals],
                'generated_at': datetime.now().isoformat()
            }
            return json.dumps(report_data, indent=2)

        # Generate text report
        report = self._generate_text_optimization_report(methodology_analysis, optimization_proposals)
        return report

    def _generate_text_optimization_report(self, analysis: Dict[str, Any], proposals: List[OptimizationProposal]) -> str:
        """Generate formatted text optimization report"""
        lines = []
        lines.append("=" * 80)
        lines.append("GOAL KIT METHODOLOGY OPTIMIZATION REPORT")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)

        # Methodology health overview
        lines.append(f"\n🏥 METHODOLOGY HEALTH ASSESSMENT")
        lines.append("-" * 50)
        lines.append(f"Overall Health: {analysis['methodology_health'].upper()}")
        lines.append(f"Effectiveness Score: {analysis['effectiveness_score']:.1f}/10")
        lines.append(f"Efficiency Score: {analysis['efficiency_score']:.1f}/10")
        lines.append(f"Quality Score: {analysis['quality_score']:.1f}/10")
        lines.append(f"Learning Score: {analysis['learning_score']:.1f}/10")
        lines.append(f"Collaboration Score: {analysis['collaboration_score']:.1f}/10")

        # Key insights
        if analysis['key_insights']:
            lines.append("\n🔍 KEY METHODOLOGY INSIGHTS")
            lines.append("-" * 50)

            for insight in analysis['key_insights']:
                lines.append(f"• {insight}")

        # Improvement areas
        if analysis['improvement_areas']:
            lines.append("\n🔧 IMPROVEMENT AREAS")
            lines.append("-" * 50)

            for area in analysis['improvement_areas']:
                lines.append(f"• {area}")

        # Optimization opportunities
        if analysis['optimization_opportunities']:
            lines.append("\n💡 OPTIMIZATION OPPORTUNITIES")
            lines.append("-" * 50)

            for opportunity in analysis['optimization_opportunities']:
                lines.append(f"• {opportunity}")

        # Optimization proposals
        if proposals:
            lines.append("\n🚀 OPTIMIZATION PROPOSALS")
            lines.append("-" * 50)

            for proposal in proposals[:3]:  # Top 3 proposals
                effort_icon = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}.get(proposal.estimated_effort, '⚪')
                lines.append(f"{effort_icon} {proposal.title}")
                lines.append(f"   Priority: {proposal.priority_score}/10 | Effort: {proposal.estimated_effort}")
                lines.append(f"   {proposal.problem_statement}")

                if proposal.expected_benefits:
                    lines.append("   Expected Benefits:")
                    for benefit in proposal.expected_benefits[:2]:
                        lines.append(f"     • {benefit}")

        # Recommendations
        lines.append("\n📋 OPTIMIZATION RECOMMENDATIONS")
        lines.append("-" * 50)

        if analysis['methodology_health'] == 'excellent':
            lines.append("🟢 Methodology performing excellently - maintain current practices")
            lines.append("   Consider sharing successful patterns with other projects")
        elif analysis['methodology_health'] == 'good':
            lines.append("🟡 Methodology performing well - consider minor optimizations")
            lines.append("   Focus on the highest priority optimization proposals")
        elif analysis['methodology_health'] == 'needs_improvement':
            lines.append("🟠 Methodology needs improvement - implement optimization proposals")
            lines.append("   Prioritize quality and efficiency improvements")
        else:
            lines.append("🔴 Methodology in critical state - immediate optimization required")
            lines.append("   Implement all high-priority optimization proposals")

        lines.append("=" * 80)
        return "\n".join(lines)


def main():
    """Main methodology optimization function"""
    if not test_git_repo():
        write_error("Not in a git repository")
        write_info("Please run this from the root of a Goal Kit project")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(description='Goal Kit Methodology Optimization Framework')
    parser.add_argument('--analyze', action='store_true', help='Analyze methodology effectiveness')
    parser.add_argument('--proposals', action='store_true', help='Generate optimization proposals')
    parser.add_argument('--report', action='store_true', help='Generate comprehensive optimization report')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')

    args = parser.parse_args()

    try:
        optimizer = MethodologyOptimizer()

        if args.analyze or args.report:
            report = optimizer.generate_optimization_report(args.json)
            print(report)

        elif args.proposals:
            proposals = optimizer.generate_optimization_proposals()
            if args.json:
                print(json.dumps([asdict(p) for p in proposals], indent=2))
            else:
                print("\n🚀 OPTIMIZATION PROPOSALS")
                for proposal in proposals:
                    effort_icon = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}.get(proposal.estimated_effort, '⚪')
                    print(f"{effort_icon} {proposal.title}")
                    print(f"   Priority: {proposal.priority_score}/10")
                    print(f"   {proposal.problem_statement}")

        else:
            # Default: show optimization summary
            analysis = optimizer.analyze_methodology_effectiveness()

            print(f"\n🔧 METHODOLOGY OPTIMIZATION SUMMARY")
            print(f"Methodology Health: {analysis['methodology_health'].upper()}")
            print(f"Overall Score: {(analysis['effectiveness_score'] + analysis['efficiency_score'] + analysis['quality_score'] + analysis['learning_score'] + analysis['collaboration_score']) / 5:.1f}/10")
            print(f"Key Insights: {len(analysis['key_insights'])}")
            print(f"Improvement Areas: {len(analysis['improvement_areas'])}")

            if analysis['methodology_health'] in ['needs_improvement', 'critical']:
                print(f"\n⚠️ Attention needed - run --proposals for specific optimization recommendations")
            else:
                print(f"\n✅ Methodology performing well - run --report for detailed analysis")

    except Exception as e:
        write_error(f"Error in methodology optimization: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()