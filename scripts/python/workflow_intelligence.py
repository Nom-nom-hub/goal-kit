#!/usr/bin/env python3
"""
Workflow Intelligence System for Goal Kit Methodology
Smart recommendations and optimization suggestions based on project patterns
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
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
class WorkflowRecommendation:
    """Structured workflow recommendation with reasoning"""
    recommendation_id: str
    category: str  # 'quality', 'velocity', 'risk', 'learning', 'collaboration'
    priority: str  # 'high', 'medium', 'low'
    title: str
    description: str
    reasoning: str
    expected_impact: str  # 'high', 'medium', 'low'
    implementation_effort: str  # 'low', 'medium', 'high'
    affected_components: List[str]
    related_insights: List[str]
    created_date: str


@dataclass
class OptimizationOpportunity:
    """Specific optimization opportunity with metrics"""
    opportunity_id: str
    optimization_type: str  # 'process', 'quality', 'velocity', 'collaboration', 'learning'
    title: str
    current_state: str
    proposed_state: str
    expected_benefits: List[str]
    implementation_steps: List[str]
    success_metrics: List[str]
    risk_factors: List[str]
    confidence_score: float  # 0-10


@dataclass
class IntelligenceReport:
    """Comprehensive workflow intelligence report"""
    project_name: str
    analysis_timestamp: str
    current_phase: str
    project_health: str
    recommendations: List[WorkflowRecommendation]
    optimizations: List[OptimizationOpportunity]
    risk_assessment: Dict[str, Any]
    success_predictions: Dict[str, Any]
    learning_insights: List[str]


class WorkflowIntelligence:
    """Smart workflow analysis and optimization system"""

    def __init__(self, project_root: str = None):
        self.project_root = project_root or get_git_root()
        if not self.project_root:
            raise ValueError("Must be run from a git repository")

        self.goals_dir = os.path.join(self.project_root, ".goalkit", "goals")
        self.intelligence_dir = os.path.join(self.project_root, ".goalkit", "intelligence")
        self.recommendations_file = os.path.join(self.intelligence_dir, "recommendations.json")
        self.optimizations_file = os.path.join(self.intelligence_dir, "optimizations.json")

        # Create intelligence directory if it doesn't exist
        os.makedirs(self.intelligence_dir, exist_ok=True)

        # Load existing data
        self.validation_data = self._load_validation_data()
        self.progress_data = self._load_progress_data()
        self.learning_data = self._load_learning_data()
        self.collaboration_data = self._load_collaboration_data()

    def _load_validation_data(self) -> Dict[str, Any]:
        """Load latest validation results"""
        try:
            # Try to run validation to get current data
            import subprocess
            result = subprocess.run([
                sys.executable, "scripts/python/enhanced_validator.py", "--json"
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return json.loads(result.stdout)
        except:
            pass

        return {}

    def _load_progress_data(self) -> Dict[str, Any]:
        """Load latest progress data"""
        try:
            # Try to run progress tracking to get current data
            import subprocess
            result = subprocess.run([
                sys.executable, "scripts/python/progress_tracker.py", "--json"
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return json.loads(result.stdout)
        except:
            pass

        return {}

    def _load_learning_data(self) -> Dict[str, Any]:
        """Load learning insights and patterns"""
        try:
            # Try to run learning system to get current data
            import subprocess
            result = subprocess.run([
                sys.executable, "scripts/python/learning_system.py", "--report", "--json"
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return json.loads(result.stdout)
        except:
            pass

        return {}

    def _load_collaboration_data(self) -> Dict[str, Any]:
        """Load collaboration insights"""
        try:
            # Try to run collaboration hub to get current data
            import subprocess
            result = subprocess.run([
                sys.executable, "scripts/python/collaboration_hub.py", "--report", "--json"
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return json.loads(result.stdout)
        except:
            pass

        return {}

    def analyze_workflow_intelligence(self) -> IntelligenceReport:
        """Analyze entire project for workflow intelligence and recommendations"""
        project_name = os.path.basename(self.project_root)

        # Determine current phase and health
        current_phase = self._determine_current_phase()
        project_health = self._assess_project_health()

        # Generate comprehensive recommendations
        recommendations = self._generate_workflow_recommendations()

        # Identify optimization opportunities
        optimizations = self._identify_optimization_opportunities()

        # Assess risks
        risk_assessment = self._assess_workflow_risks()

        # Generate success predictions
        success_predictions = self._generate_success_predictions()

        # Extract learning insights
        learning_insights = self._extract_workflow_insights()

        return IntelligenceReport(
            project_name=project_name,
            analysis_timestamp=datetime.now().isoformat(),
            current_phase=current_phase,
            project_health=project_health,
            recommendations=recommendations,
            optimizations=optimizations,
            risk_assessment=risk_assessment,
            success_predictions=success_predictions,
            learning_insights=learning_insights
        )

    def _determine_current_phase(self) -> str:
        """Determine current project phase based on available components"""
        if not os.path.exists(self.goals_dir):
            return 'vision'

        goals = [d for d in os.listdir(self.goals_dir) if os.path.isdir(os.path.join(self.goals_dir, d))]

        if not goals:
            return 'goal_creation'

        # Check for strategies
        strategies_found = 0
        for goal in goals:
            strategies_file = os.path.join(self.goals_dir, goal, "strategies.md")
            if os.path.exists(strategies_file):
                strategies_found += 1

        if strategies_found == 0:
            return 'strategy'
        elif strategies_found < len(goals):
            return 'strategy'

        # Check for milestones
        milestones_found = 0
        for goal in goals:
            milestones_file = os.path.join(self.goals_dir, goal, "milestones.md")
            if os.path.exists(milestones_file):
                milestones_found += 1

        if milestones_found < len(goals):
            return 'milestone'

        return 'execution'

    def _assess_project_health(self) -> str:
        """Assess overall project health"""
        # Use validation data if available
        if self.validation_data and 'validation_results' in self.validation_data:
            scores = [r.get('overall_score', 0) for r in self.validation_data['validation_results']]
            if scores:
                avg_score = sum(scores) / len(scores)
                if avg_score >= 8:
                    return 'excellent'
                elif avg_score >= 6:
                    return 'good'
                elif avg_score >= 4:
                    return 'concerning'
                else:
                    return 'critical'

        # Use progress data if available
        if self.progress_data and 'project_analytics' in self.progress_data:
            analytics = self.progress_data['project_analytics']
            if analytics.get('overall_completion', 0) >= 80:
                return 'excellent'
            elif analytics.get('overall_completion', 0) >= 50:
                return 'good'
            elif analytics.get('overall_completion', 0) >= 20:
                return 'concerning'
            else:
                return 'critical'

        return 'unknown'

    def _generate_workflow_recommendations(self) -> List[WorkflowRecommendation]:
        """Generate intelligent workflow recommendations"""
        recommendations = []

        # Quality-based recommendations
        if self.validation_data:
            quality_recs = self._generate_quality_recommendations()
            recommendations.extend(quality_recs)

        # Progress-based recommendations
        if self.progress_data:
            progress_recs = self._generate_progress_recommendations()
            recommendations.extend(progress_recs)

        # Learning-based recommendations
        if self.learning_data:
            learning_recs = self._generate_learning_recommendations()
            recommendations.extend(learning_recs)

        # Collaboration-based recommendations
        if self.collaboration_data:
            collab_recs = self._generate_collaboration_recommendations()
            recommendations.extend(collab_recs)

        # Sort by priority
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        recommendations.sort(key=lambda x: priority_order.get(x.priority, 0), reverse=True)

        # Save recommendations
        self._save_recommendations(recommendations)

        return recommendations

    def _generate_quality_recommendations(self) -> List[WorkflowRecommendation]:
        """Generate quality-based recommendations"""
        recommendations = []

        if not self.validation_data or 'validation_results' not in self.validation_data:
            return recommendations

        validation_results = self.validation_data['validation_results']

        # Find low-quality components
        low_quality = [r for r in validation_results if r.get('overall_score', 10) < 6.0]

        if low_quality:
            for result in low_quality[:3]:  # Top 3 issues
                rec = WorkflowRecommendation(
                    recommendation_id=f"quality_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    category='quality',
                    priority='high' if result['overall_score'] < 4.0 else 'medium',
                    title=f"Improve {result['file_type']} quality",
                    description=f"Current score: {result['overall_score']}/10. Address quality issues to ensure project success.",
                    reasoning=f"Low quality {result['file_type']} components can impact overall project success and should be addressed promptly.",
                    expected_impact='high',
                    implementation_effort='medium',
                    affected_components=[result['file_path']],
                    related_insights=result.get('recommendations', []),
                    created_date=datetime.now().isoformat()
                )
                recommendations.append(rec)

        # Find high-quality patterns to replicate
        high_quality = [r for r in validation_results if r.get('overall_score', 0) >= 8.0]

        if high_quality:
            rec = WorkflowRecommendation(
                recommendation_id=f"quality_pattern_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                category='quality',
                priority='medium',
                title="Replicate high-quality patterns",
                description=f"Found {len(high_quality)} high-quality components. Apply successful patterns to other goals.",
                reasoning="High-quality components represent proven approaches that should be replicated across the project.",
                expected_impact='medium',
                implementation_effort='low',
                affected_components=['all_goals'],
                related_insights=[r.get('file_path', '') for r in high_quality],
                created_date=datetime.now().isoformat()
            )
            recommendations.append(rec)

        return recommendations

    def _generate_progress_recommendations(self) -> List[WorkflowRecommendation]:
        """Generate progress-based recommendations"""
        recommendations = []

        if not self.progress_data or 'project_analytics' not in self.progress_data:
            return recommendations

        analytics = self.progress_data['project_analytics']

        # Risk-based recommendations
        risk_score = analytics.get('risk_score', 5.0)
        if risk_score > 7:
            rec = WorkflowRecommendation(
                recommendation_id=f"risk_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                category='risk',
                priority='high',
                title="Address high project risk",
                description=f"Project risk score is {risk_score}/10. Immediate attention required for at-risk goals.",
                reasoning="High risk scores indicate goals that may not achieve their objectives without intervention.",
                expected_impact='high',
                implementation_effort='medium',
                affected_components=['at_risk_goals'],
                related_insights=["Monitor progress velocity", "Review milestone completion rates"],
                created_date=datetime.now().isoformat()
            )
            recommendations.append(rec)

        # Velocity-based recommendations
        velocity = analytics.get('project_velocity', 5.0)
        if velocity < 3:
            rec = WorkflowRecommendation(
                recommendation_id=f"velocity_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                category='velocity',
                priority='medium',
                title="Improve project velocity",
                description=f"Current velocity is {velocity}/10. Consider accelerating milestone completion.",
                reasoning="Low velocity may indicate bottlenecks or resource constraints that should be addressed.",
                expected_impact='medium',
                implementation_effort='medium',
                affected_components=['all_goals'],
                related_insights=["Review milestone definitions", "Check resource allocation"],
                created_date=datetime.now().isoformat()
            )
            recommendations.append(rec)

        return recommendations

    def _generate_learning_recommendations(self) -> List[WorkflowRecommendation]:
        """Generate learning-based recommendations"""
        recommendations = []

        if not self.learning_data:
            return recommendations

        insights = self.learning_data.get('recent_insights', [])
        patterns = self.learning_data.get('top_patterns', [])

        # High-impact insights
        high_impact_insights = [i for i in insights if i.get('impact') == 'high']

        if high_impact_insights:
            for insight in high_impact_insights[:2]:
                rec = WorkflowRecommendation(
                    recommendation_id=f"learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    category='learning',
                    priority='medium',
                    title=f"Apply learning: {insight.get('title', 'Unknown')}",
                    description=insight.get('description', ''),
                    reasoning="High-impact learnings should be applied to improve project outcomes.",
                    expected_impact='high',
                    implementation_effort='low',
                    affected_components=['current_goals'],
                    related_insights=[insight.get('insight_id', '')],
                    created_date=datetime.now().isoformat()
                )
                recommendations.append(rec)

        # Pattern-based recommendations
        if patterns:
            top_pattern = patterns[0]  # Highest frequency pattern
            rec = WorkflowRecommendation(
                recommendation_id=f"pattern_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                category='learning',
                priority='medium',
                title=f"Leverage top pattern: {top_pattern.get('pattern_type', 'Unknown')}",
                description=top_pattern.get('description', ''),
                reasoning=f"This pattern occurs frequently ({top_pattern.get('frequency', 0)} times) and has proven effectiveness.",
                expected_impact='medium',
                implementation_effort='low',
                affected_components=['similar_goals'],
                related_insights=top_pattern.get('examples', []),
                created_date=datetime.now().isoformat()
            )
            recommendations.append(rec)

        return recommendations

    def _generate_collaboration_recommendations(self) -> List[WorkflowRecommendation]:
        """Generate collaboration-based recommendations"""
        recommendations = []

        if not self.collaboration_data:
            return recommendations

        similarities = self.collaboration_data.get('goal_similarities', [])
        high_potential = [s for s in similarities if s.get('collaboration_potential') == 'high']

        if high_potential:
            rec = WorkflowRecommendation(
                recommendation_id=f"collaboration_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                category='collaboration',
                priority='medium',
                title=f"Enable collaboration for {len(high_potential)} goal pairs",
                description=f"Found {len(high_potential)} high-potential collaboration opportunities between goals.",
                reasoning="High similarity scores indicate goals that could benefit from knowledge sharing and coordination.",
                expected_impact='medium',
                implementation_effort='low',
                affected_components=[s.get('goal_a', '') for s in high_potential] + [s.get('goal_b', '') for s in high_potential],
                related_insights=[f"Similarity: {s.get('similarity_score', 0)}/10" for s in high_potential],
                created_date=datetime.now().isoformat()
            )
            recommendations.append(rec)

        return recommendations

    def _identify_optimization_opportunities(self) -> List[OptimizationOpportunity]:
        """Identify specific optimization opportunities"""
        opportunities = []

        # Quality optimization opportunities
        quality_opportunities = self._identify_quality_optimizations()
        opportunities.extend(quality_opportunities)

        # Velocity optimization opportunities
        velocity_opportunities = self._identify_velocity_optimizations()
        opportunities.extend(velocity_opportunities)

        # Learning optimization opportunities
        learning_opportunities = self._identify_learning_optimizations()
        opportunities.extend(learning_opportunities)

        # Collaboration optimization opportunities
        collaboration_opportunities = self._identify_collaboration_optimizations()
        opportunities.extend(collaboration_opportunities)

        # Save opportunities
        self._save_optimization_opportunities(opportunities)

        return opportunities

    def _identify_quality_optimizations(self) -> List[OptimizationOpportunity]:
        """Identify quality optimization opportunities"""
        opportunities = []

        if not self.validation_data:
            return opportunities

        validation_results = self.validation_data.get('validation_results', [])

        # Find components that could be optimized
        medium_quality = [r for r in validation_results if 6.0 <= r.get('overall_score', 0) < 8.0]

        for result in medium_quality[:3]:
            opp = OptimizationOpportunity(
                opportunity_id=f"quality_opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                optimization_type='quality',
                title=f"Optimize {result['file_type']} quality from {result['overall_score']}/10 to 8.0+",
                current_state=f"Current score: {result['overall_score']}/10",
                proposed_state="Target score: 8.0+/10 with enhanced specificity and measurability",
                expected_benefits=[
                    "Improved goal success probability",
                    "Better stakeholder alignment",
                    "Reduced execution risks"
                ],
                implementation_steps=[
                    "Review validation feedback",
                    "Address specific recommendations",
                    "Enhance success metrics",
                    "Re-validate for improvement confirmation"
                ],
                success_metrics=[
                    "Quality score improvement of 1.5+ points",
                    "Zero high-priority validation issues",
                    "Stakeholder approval of enhanced quality"
                ],
                risk_factors=[
                    "Time investment for quality improvements",
                    "Potential scope adjustments needed"
                ],
                confidence_score=8.0
            )
            opportunities.append(opp)

        return opportunities

    def _identify_velocity_optimizations(self) -> List[OptimizationOpportunity]:
        """Identify velocity optimization opportunities"""
        opportunities = []

        if not self.progress_data:
            return opportunities

        analytics = self.progress_data.get('project_analytics', {})
        velocity = analytics.get('project_velocity', 5.0)

        if velocity < 5.0:
            opp = OptimizationOpportunity(
                opportunity_id=f"velocity_opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                optimization_type='velocity',
                title=f"Improve project velocity from {velocity}/10 to 7.0+",
                current_state=f"Current velocity: {velocity}/10",
                proposed_state="Target velocity: 7.0+/10 with optimized milestone completion",
                expected_benefits=[
                    "Faster time to market",
                    "Improved team productivity",
                    "Better resource utilization"
                ],
                implementation_steps=[
                    "Analyze milestone bottlenecks",
                    "Optimize milestone definitions",
                    "Improve resource allocation",
                    "Implement velocity tracking"
                ],
                success_metrics=[
                    "Velocity improvement of 2+ points",
                    "Reduced milestone completion time",
                    "Increased team satisfaction scores"
                ],
                risk_factors=[
                    "Potential quality trade-offs",
                    "Team burnout if pushed too hard"
                ],
                confidence_score=7.5
            )
            opportunities.append(opp)

        return opportunities

    def _identify_learning_optimizations(self) -> List[OptimizationOpportunity]:
        """Identify learning optimization opportunities"""
        opportunities = []

        if not self.learning_data:
            return opportunities

        insights = self.learning_data.get('total_insights', 0)

        if insights < 5:
            opp = OptimizationOpportunity(
                opportunity_id=f"learning_opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                optimization_type='learning',
                title="Establish systematic learning capture process",
                current_state=f"Only {insights} insights captured",
                proposed_state="Regular learning capture with 10+ insights per month",
                expected_benefits=[
                    "Accelerated project learning",
                    "Reduced repeated mistakes",
                    "Improved decision-making quality"
                ],
                implementation_steps=[
                    "Implement regular retrospective meetings",
                    "Train team on insight capture",
                    "Set up learning tracking systems",
                    "Create learning review processes"
                ],
                success_metrics=[
                    "10+ insights captured per month",
                    "Learning velocity of 2.0+",
                    "Reduced issue recurrence rate"
                ],
                risk_factors=[
                    "Time investment for learning activities",
                    "Potential information overload"
                ],
                confidence_score=8.5
            )
            opportunities.append(opp)

        return opportunities

    def _identify_collaboration_optimizations(self) -> List[OptimizationOpportunity]:
        """Identify collaboration optimization opportunities"""
        opportunities = []

        if not self.collaboration_data:
            return opportunities

        similarities = self.collaboration_data.get('goal_similarities', [])
        high_potential = len([s for s in similarities if s.get('collaboration_potential') == 'high'])

        if high_potential > 0:
            opp = OptimizationOpportunity(
                opportunity_id=f"collaboration_opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                optimization_type='collaboration',
                title=f"Enable knowledge sharing for {high_potential} high-potential goal pairs",
                current_state=f"{high_potential} high-potential collaboration opportunities identified",
                proposed_state="Active knowledge sharing and coordination between similar goals",
                expected_benefits=[
                    "Reduced duplication of effort",
                    "Accelerated learning across goals",
                    "Improved overall project efficiency"
                ],
                implementation_steps=[
                    "Set up cross-goal communication channels",
                    "Implement knowledge sharing sessions",
                    "Create shared pattern libraries",
                    "Establish collaboration tracking"
                ],
                success_metrics=[
                    "Successful knowledge transfers",
                    "Reduced goal completion time",
                    "Improved cross-team satisfaction"
                ],
                risk_factors=[
                    "Coordination overhead",
                    "Potential for conflicting priorities"
                ],
                confidence_score=7.0
            )
            opportunities.append(opp)

        return opportunities

    def _assess_workflow_risks(self) -> Dict[str, Any]:
        """Assess workflow-related risks"""
        risks = {
            'quality_risks': [],
            'velocity_risks': [],
            'learning_risks': [],
            'collaboration_risks': []
        }

        # Quality risks
        if self.validation_data:
            low_quality_count = len([r for r in self.validation_data.get('validation_results', [])
                                   if r.get('overall_score', 10) < 6.0])
            if low_quality_count > 0:
                risks['quality_risks'].append(f"{low_quality_count} components with quality scores < 6.0")

        # Velocity risks
        if self.progress_data:
            analytics = self.progress_data.get('project_analytics', {})
            if analytics.get('risk_score', 5.0) > 7.0:
                risks['velocity_risks'].append(f"High project risk score: {analytics['risk_score']}/10")

        # Learning risks
        if self.learning_data:
            insights = self.learning_data.get('total_insights', 0)
            if insights < 3:
                risks['learning_risks'].append("Insufficient learning capture for project intelligence")

        # Collaboration risks
        if self.collaboration_data:
            similarities = self.collaboration_data.get('goal_similarities', [])
            if not similarities:
                risks['collaboration_risks'].append("No collaboration opportunities identified")

        return risks

    def _generate_success_predictions(self) -> Dict[str, Any]:
        """Generate success predictions based on current data"""
        predictions = {
            'goal_success_probability': 0.0,
            'timeline_confidence': 0.0,
            'quality_outcome': 'unknown',
            'risk_level': 'unknown',
            'recommendations': []
        }

        # Base predictions on available data
        quality_score = 5.0
        velocity_score = 5.0
        learning_score = 5.0

        if self.validation_data and 'validation_results' in self.validation_data:
            scores = [r.get('overall_score', 0) for r in self.validation_data['validation_results']]
            if scores:
                quality_score = sum(scores) / len(scores)

        if self.progress_data and 'project_analytics' in self.progress_data:
            analytics = self.progress_data['project_analytics']
            velocity_score = analytics.get('project_velocity', 5.0)

        if self.learning_data:
            insights = self.learning_data.get('total_insights', 0)
            learning_score = min(insights * 2, 10.0)  # Scale insights to 0-10

        # Calculate overall success probability
        predictions['goal_success_probability'] = (quality_score + velocity_score + learning_score) / 30.0 * 100

        # Timeline confidence
        predictions['timeline_confidence'] = velocity_score

        # Quality outcome prediction
        if quality_score >= 8.0:
            predictions['quality_outcome'] = 'excellent'
        elif quality_score >= 6.0:
            predictions['quality_outcome'] = 'good'
        elif quality_score >= 4.0:
            predictions['quality_outcome'] = 'concerning'
        else:
            predictions['quality_outcome'] = 'critical'

        # Risk level prediction
        if predictions['goal_success_probability'] >= 80:
            predictions['risk_level'] = 'low'
        elif predictions['goal_success_probability'] >= 60:
            predictions['risk_level'] = 'medium'
        else:
            predictions['risk_level'] = 'high'

        return predictions

    def _extract_workflow_insights(self) -> List[str]:
        """Extract key workflow insights"""
        insights = []

        # Quality insights
        if self.validation_data:
            high_quality_count = len([r for r in self.validation_data.get('validation_results', [])
                                    if r.get('overall_score', 0) >= 8.0])
            if high_quality_count > 0:
                insights.append(f"Found {high_quality_count} high-quality components demonstrating best practices")

        # Progress insights
        if self.progress_data:
            analytics = self.progress_data.get('project_analytics', {})
            completion = analytics.get('overall_completion', 0)
            if completion > 0:
                insights.append(f"Project is {completion}% complete with current velocity trajectory")

        # Learning insights
        if self.learning_data:
            patterns = self.learning_data.get('total_patterns', 0)
            if patterns > 0:
                insights.append(f"Identified {patterns} recurring patterns for optimization")

        # Collaboration insights
        if self.collaboration_data:
            similarities = self.collaboration_data.get('goal_similarities', [])
            if similarities:
                insights.append(f"Found {len(similarities)} collaboration opportunities between goals")

        return insights if insights else ["Continue building project components to generate workflow insights"]

    def _save_recommendations(self, recommendations: List[WorkflowRecommendation]):
        """Save recommendations for future reference"""
        recommendations_data = [asdict(r) for r in recommendations]

        with open(self.recommendations_file, 'w', encoding='utf-8') as f:
            json.dump(recommendations_data, f, indent=2)

    def _save_optimization_opportunities(self, opportunities: List[OptimizationOpportunity]):
        """Save optimization opportunities"""
        opportunities_data = [asdict(o) for o in opportunities]

        with open(self.optimizations_file, 'w', encoding='utf-8') as f:
            json.dump(opportunities_data, f, indent=2)

    def generate_workflow_report(self, output_format: str = 'text') -> str:
        """Generate comprehensive workflow intelligence report"""
        intelligence = self.analyze_workflow_intelligence()

        if output_format == 'json':
            report_data = {
                'intelligence_report': asdict(intelligence),
                'generated_at': datetime.now().isoformat()
            }
            return json.dumps(report_data, indent=2)

        # Generate text report
        report = self._generate_text_intelligence_report(intelligence)
        return report

    def _generate_text_intelligence_report(self, intelligence: IntelligenceReport) -> str:
        """Generate formatted text intelligence report"""
        lines = []
        lines.append("=" * 80)
        lines.append("GOAL KIT WORKFLOW INTELLIGENCE REPORT")
        lines.append(f"Project: {intelligence.project_name}")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)

        # Current state
        lines.append(f"\n📊 CURRENT PROJECT STATE")
        lines.append("-" * 40)
        lines.append(f"Current Phase: {intelligence.current_phase.title()}")
        lines.append(f"Project Health: {intelligence.project_health.upper()}")
        lines.append(f"Success Probability: {intelligence.success_predictions['goal_success_probability']:.1f}%")
        lines.append(f"Risk Level: {intelligence.success_predictions['risk_level'].upper()}")

        # Key recommendations
        if intelligence.recommendations:
            lines.append("\n🚀 PRIORITY RECOMMENDATIONS")
            lines.append("-" * 40)

            for rec in intelligence.recommendations[:5]:  # Top 5 recommendations
                priority_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(rec.priority, '⚪')
                lines.append(f"{priority_icon} [{rec.category.upper()}] {rec.title}")
                lines.append(f"   {rec.description}")
                lines.append(f"   Impact: {rec.expected_impact} | Effort: {rec.implementation_effort}")

        # Optimization opportunities
        if intelligence.optimizations:
            lines.append("\n💡 OPTIMIZATION OPPORTUNITIES")
            lines.append("-" * 40)

            for opt in intelligence.optimizations[:3]:  # Top 3 opportunities
                effort_icon = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}.get(opt.implementation_effort, '⚪')
                lines.append(f"{effort_icon} {opt.title}")
                lines.append(f"   {opt.current_state} → {opt.proposed_state}")
                lines.append(f"   Confidence: {opt.confidence_score}/10")

        # Risk assessment
        risk_count = sum(len(risks) for risks in intelligence.risk_assessment.values())
        if risk_count > 0:
            lines.append("\n⚠️ RISK ASSESSMENT")
            lines.append("-" * 40)

            for category, risks in intelligence.risk_assessment.items():
                if risks:
                    lines.append(f"{category.replace('_', ' ').title()}:")
                    for risk in risks:
                        lines.append(f"  • {risk}")

        # Learning insights
        if intelligence.learning_insights:
            lines.append("\n🔍 WORKFLOW INSIGHTS")
            lines.append("-" * 40)

            for insight in intelligence.learning_insights:
                lines.append(f"• {insight}")

        lines.append("=" * 80)
        return "\n".join(lines)


def main():
    """Main workflow intelligence function"""
    if not test_git_repo():
        write_error("Not in a git repository")
        write_info("Please run this from the root of a Goal Kit project")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(description='Goal Kit Workflow Intelligence System')
    parser.add_argument('--analyze', action='store_true', help='Analyze workflow for intelligence and recommendations')
    parser.add_argument('--recommendations', action='store_true', help='Show current recommendations only')
    parser.add_argument('--optimizations', action='store_true', help='Show optimization opportunities only')
    parser.add_argument('--report', action='store_true', help='Generate comprehensive intelligence report')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')

    args = parser.parse_args()

    try:
        system = WorkflowIntelligence()

        if args.analyze or args.report:
            report = system.generate_workflow_report(args.json)
            print(report)

        elif args.recommendations:
            intelligence = system.analyze_workflow_intelligence()
            if args.json:
                print(json.dumps([asdict(r) for r in intelligence.recommendations], indent=2))
            else:
                print("\n🚀 CURRENT RECOMMENDATIONS")
                for rec in intelligence.recommendations:
                    priority_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(rec.priority, '⚪')
                    print(f"{priority_icon} {rec.title}")
                    print(f"   {rec.description}")

        elif args.optimizations:
            intelligence = system.analyze_workflow_intelligence()
            if args.json:
                print(json.dumps([asdict(o) for o in intelligence.optimizations], indent=2))
            else:
                print("\n💡 OPTIMIZATION OPPORTUNITIES")
                for opt in intelligence.optimizations:
                    effort_icon = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}.get(opt.implementation_effort, '⚪')
                    print(f"{effort_icon} {opt.title}")
                    print(f"   {opt.current_state}")
                    print(f"   → {opt.proposed_state}")

        else:
            # Default: show intelligence summary
            intelligence = system.analyze_workflow_intelligence()

            print(f"\n🧠 WORKFLOW INTELLIGENCE SUMMARY")
            print(f"Project: {intelligence.project_name}")
            print(f"Current Phase: {intelligence.current_phase}")
            print(f"Project Health: {intelligence.project_health}")
            print(f"Success Probability: {intelligence.success_predictions['goal_success_probability']:.1f}%")
            print(f"Active Recommendations: {len(intelligence.recommendations)}")
            print(f"Optimization Opportunities: {len(intelligence.optimizations)}")

            if intelligence.recommendations:
                high_priority = [r for r in intelligence.recommendations if r.priority == 'high']
                if high_priority:
                    print(f"\n🔴 High Priority Recommendations:")
                    for rec in high_priority:
                        print(f"  • {rec.title}")

    except Exception as e:
        write_error(f"Error in workflow intelligence: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()