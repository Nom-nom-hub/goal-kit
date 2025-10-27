#!/usr/bin/env python3
"""
Collaboration Hub for Goal Kit Methodology
Cross-goal knowledge sharing and insights for collective intelligence
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
class KnowledgeShare:
    """Structured knowledge sharing between goals"""
    share_id: str
    source_goal: str
    target_goals: List[str]
    knowledge_type: str  # 'pattern', 'insight', 'strategy', 'warning', 'recommendation'
    title: str
    description: str
    relevance_score: float  # 0-10 relevance to target goals
    applicability: str  # 'direct', 'adaptable', 'inspirational'
    tags: List[str]
    shared_date: str
    status: str  # 'active', 'applied', 'rejected', 'pending'


@dataclass
class GoalSimilarity:
    """Similarity analysis between goals"""
    goal_a: str
    goal_b: str
    similarity_score: float  # 0-10 similarity score
    shared_elements: List[str]
    complementary_aspects: List[str]
    learning_opportunities: List[str]
    collaboration_potential: str  # 'high', 'medium', 'low'


@dataclass
class CollaborationInsight:
    """Insights derived from cross-goal collaboration"""
    insight_id: str
    insight_type: str  # 'pattern_transfer', 'resource_sharing', 'joint_strategy', 'warning_transfer'
    description: str
    affected_goals: List[str]
    potential_benefits: List[str]
    implementation_effort: str  # 'low', 'medium', 'high'
    success_probability: float  # 0-10
    created_date: str


class CollaborationHub:
    """Cross-goal knowledge sharing and collaboration system"""

    def __init__(self, project_root: Optional[str] = None):
        self.project_root = project_root or get_git_root()
        if not self.project_root:
            raise ValueError("Must be run from a git repository")

        self.goals_dir = os.path.join(self.project_root, ".goalkit", "goals")
        self.collaboration_dir = os.path.join(self.project_root, ".goalkit", "collaboration")
        self.knowledge_shares_file = os.path.join(self.collaboration_dir, "knowledge_shares.json")
        self.similarities_file = os.path.join(self.collaboration_dir, "goal_similarities.json")
        self.collaboration_insights_file = os.path.join(self.collaboration_dir, "collaboration_insights.json")

        # Create collaboration directory if it doesn't exist
        os.makedirs(self.collaboration_dir, exist_ok=True)

    def analyze_goal_similarities(self) -> List[GoalSimilarity]:
        """Analyze similarities between all goals for collaboration opportunities"""
        goals = self._get_all_goals()
        if len(goals) < 2:
            return []

        similarities = []

        # Compare each pair of goals
        for i, goal_a in enumerate(goals):
            for goal_b in goals[i+1:]:
                similarity = self._compare_goals(goal_a, goal_b)
                if similarity.similarity_score >= 5.0:  # Only include meaningful similarities
                    similarities.append(similarity)

        # Save similarities for future reference
        self._save_goal_similarities(similarities)

        return similarities

    def _get_all_goals(self) -> List[str]:
        """Get all goal directories"""
        if not os.path.exists(self.goals_dir):
            return []

        goals = []
        for item in os.listdir(self.goals_dir):
            goal_path = os.path.join(self.goals_dir, item)
            if os.path.isdir(goal_path):
                goals.append(item)

        return goals

    def _compare_goals(self, goal_a: str, goal_b: str) -> GoalSimilarity:
        """Compare two goals for similarities and collaboration opportunities"""
        # Load goal files
        goal_a_path = os.path.join(self.goals_dir, goal_a, "goal.md")
        goal_b_path = os.path.join(self.goals_dir, goal_b, "goal.md")

        if not os.path.exists(goal_a_path) or not os.path.exists(goal_b_path):
            return GoalSimilarity(
                goal_a=goal_a, goal_b=goal_b, similarity_score=0.0,
                shared_elements=[], complementary_aspects=[], learning_opportunities=[],
                collaboration_potential='low'
            )

        # Read goal content
        with open(goal_a_path, 'r', encoding='utf-8') as f:
            content_a = f.read()
        with open(goal_b_path, 'r', encoding='utf-8') as f:
            content_b = f.read()

        # Find shared elements
        shared_elements = self._find_shared_elements(content_a, content_b)

        # Find complementary aspects
        complementary_aspects = self._find_complementary_aspects(content_a, content_b)

        # Identify learning opportunities
        learning_opportunities = self._identify_learning_opportunities(content_a, content_b, shared_elements)

        # Calculate similarity score
        similarity_score = self._calculate_similarity_score(shared_elements, complementary_aspects)

        # Determine collaboration potential
        collaboration_potential = self._assess_collaboration_potential(
            similarity_score, shared_elements, complementary_aspects
        )

        return GoalSimilarity(
            goal_a=goal_a,
            goal_b=goal_b,
            similarity_score=round(similarity_score, 2),
            shared_elements=shared_elements,
            complementary_aspects=complementary_aspects,
            learning_opportunities=learning_opportunities,
            collaboration_potential=collaboration_potential
        )

    def _find_shared_elements(self, content_a: str, content_b: str) -> List[str]:
        """Find shared elements between two goals"""
        shared = []

        # Shared user types
        user_patterns = [
            r'users?\s+(?:with|who|that)\s+([^.!?]+)',
            r'target\s+(?:users?|audience|customers?)\s*[:\-]?\s*([^.!?]+)',
            r'(?:developers?|teams?|organizations?)\s+([^.!?]+)'
        ]

        for pattern in user_patterns:
            matches_a = re.findall(pattern, content_a, re.IGNORECASE)
            matches_b = re.findall(pattern, content_b, re.IGNORECASE)
            for match_a in matches_a:
                for match_b in matches_b:
                    if self._text_similarity(match_a, match_b) > 0.7:
                        shared.append(f"Similar user focus: {match_a.strip()}")

        # Shared success metrics
        metrics_a = set(re.findall(r'\b\d+%|\b\d+\s*(?:user|customer|day|week|month|year|dollar|\$)', content_a, re.IGNORECASE))
        metrics_b = set(re.findall(r'\b\d+%|\b\d+\s*(?:user|customer|day|week|month|year|dollar|\$)', content_b, re.IGNORECASE))

        shared_metrics = metrics_a.intersection(metrics_b)
        if shared_metrics:
            shared.append(f"Shared success metrics: {', '.join(shared_metrics)}")

        # Shared technologies or approaches
        tech_keywords = ['api', 'database', 'ui', 'ux', 'testing', 'automation', 'integration']
        for keyword in tech_keywords:
            if keyword in content_a.lower() and keyword in content_b.lower():
                shared.append(f"Shared technology focus: {keyword}")

        return shared

    def _find_complementary_aspects(self, content_a: str, content_b: str) -> List[str]:
        """Find complementary aspects between goals"""
        complementary = []

        # Different user focuses that could benefit each other
        user_a_match = re.search(r'users?\s+(?:with|who|that)\s+([^.!?]+)', content_a, re.IGNORECASE)
        user_b_match = re.search(r'users?\s+(?:with|who|that)\s+([^.!?]+)', content_b, re.IGNORECASE)

        if user_a_match and user_b_match:
            user_a = user_a_match.group(1).strip()
            user_b = user_b_match.group(1).strip()
            if user_a.lower() != user_b.lower():
                complementary.append(f"Different user focuses: {user_a} vs {user_b}")

        # Different phases or approaches
        if 'planning' in content_a.lower() and 'execution' in content_b.lower():
            complementary.append("Complementary phases: planning focus vs execution focus")
        elif 'strategy' in content_a.lower() and 'implementation' in content_b.lower():
            complementary.append("Complementary approaches: strategy focus vs implementation focus")

        # Different technologies that could integrate
        tech_a = [t for t in ['frontend', 'backend', 'api', 'database', 'mobile', 'web'] if t in content_a.lower()]
        tech_b = [t for t in ['frontend', 'backend', 'api', 'database', 'mobile', 'web'] if t in content_b.lower()]

        if tech_a and tech_b and set(tech_a) != set(tech_b):
            complementary.append(f"Different technology focuses: {', '.join(tech_a)} vs {', '.join(tech_b)}")

        return complementary

    def _identify_learning_opportunities(self, content_a: str, content_b: str, shared_elements: List[str]) -> List[str]:
        """Identify learning opportunities between goals"""
        opportunities = []

        if shared_elements:
            opportunities.append("Share successful patterns and approaches")
            opportunities.append("Coordinate on common challenges and solutions")

        # Look for different approaches to similar problems
        if any('user' in element.lower() for element in shared_elements):
            opportunities.append("Compare user engagement strategies")
            opportunities.append("Share user feedback and insights")

        if any('metric' in element.lower() for element in shared_elements):
            opportunities.append("Align measurement approaches and success criteria")
            opportunities.append("Share validation strategies and results")

        # Risk sharing opportunities
        risks_a = re.findall(r'risk[:\s]+([^.!?]+)', content_a, re.IGNORECASE)
        risks_b = re.findall(r'risk[:\s]+([^.!?]+)', content_b, re.IGNORECASE)

        if risks_a or risks_b:
            opportunities.append("Share risk mitigation strategies")
            opportunities.append("Coordinate risk monitoring and response")

        return opportunities

    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity (simple word overlap)"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)

    def _calculate_similarity_score(self, shared_elements: List[str], complementary_aspects: List[str]) -> float:
        """Calculate overall similarity score between goals"""
        # Base score from shared elements
        shared_score = min(len(shared_elements) * 2, 6)  # Max 6 points for shared elements

        # Bonus for complementary aspects
        complementary_bonus = min(len(complementary_aspects) * 1.5, 3)  # Max 3 points for complementary

        # Overall similarity
        total_score = shared_score + complementary_bonus

        return min(total_score, 10.0)

    def _assess_collaboration_potential(self, similarity_score: float, shared_elements: List[str],
                                       complementary_aspects: List[str]) -> str:
        """Assess collaboration potential between goals"""
        if similarity_score >= 8.0 and len(shared_elements) >= 3:
            return 'high'
        elif similarity_score >= 6.0 and (shared_elements or complementary_aspects):
            return 'medium'
        else:
            return 'low'

    def _save_goal_similarities(self, similarities: List[GoalSimilarity]):
        """Save goal similarities for future reference"""
        similarities_data = [asdict(s) for s in similarities]

        with open(self.similarities_file, 'w', encoding='utf-8') as f:
            json.dump(similarities_data, f, indent=2)

    def share_knowledge_between_goals(self, source_goal: str, target_goals: List[str],
                                     knowledge_type: str, title: str, description: str) -> str:
        """Share knowledge from one goal to others"""
        share_id = f"share_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Calculate relevance to each target goal
        relevance_scores = []
        for target_goal in target_goals:
            relevance = self._calculate_knowledge_relevance(source_goal, target_goal, knowledge_type, description)
            relevance_scores.append(relevance)

        avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0

        # Determine applicability
        applicability = self._determine_applicability(knowledge_type, avg_relevance)

        # Create knowledge share
        knowledge_share = KnowledgeShare(
            share_id=share_id,
            source_goal=source_goal,
            target_goals=target_goals,
            knowledge_type=knowledge_type,
            title=title,
            description=description,
            relevance_score=round(avg_relevance, 2),
            applicability=applicability,
            tags=self._extract_knowledge_tags(description),
            shared_date=datetime.now().isoformat(),
            status='active'
        )

        # Save knowledge share
        self._save_knowledge_share(knowledge_share)

        write_success(f"Knowledge shared: {title} (relevance: {avg_relevance:.1f}/10)")
        return share_id

    def _calculate_knowledge_relevance(self, source_goal: str, target_goal: str,
                                      knowledge_type: str, description: str) -> float:
        """Calculate relevance of knowledge to target goal"""
        relevance = 5.0  # Base relevance

        # Load target goal content
        target_path = os.path.join(self.goals_dir, target_goal, "goal.md")
        if not os.path.exists(target_path):
            return 0.0

        with open(target_path, 'r', encoding='utf-8') as f:
            target_content = f.read()

        # Keyword matching
        keywords = description.lower().split()
        target_words = target_content.lower().split()

        matching_words = sum(1 for keyword in keywords if keyword in target_words)
        relevance += min(matching_words * 0.5, 3)  # Up to +3 for keyword matches

        # Knowledge type relevance
        type_relevance = {
            'pattern': 2.0 if 'pattern' in target_content.lower() else 0.5,
            'strategy': 2.0 if 'strategy' in target_content.lower() else 0.5,
            'warning': 1.5 if 'risk' in target_content.lower() else 0.3,
            'insight': 1.5 if 'learning' in target_content.lower() else 0.5,
            'recommendation': 1.8 if 'approach' in target_content.lower() else 0.5
        }

        relevance += type_relevance.get(knowledge_type, 1.0)

        return min(relevance, 10.0)

    def _determine_applicability(self, knowledge_type: str, relevance_score: float) -> str:
        """Determine how applicable the knowledge is"""
        if relevance_score >= 8.0:
            return 'direct'
        elif relevance_score >= 6.0:
            return 'adaptable'
        else:
            return 'inspirational'

    def _extract_knowledge_tags(self, description: str) -> List[str]:
        """Extract tags from knowledge description"""
        tags = []

        # Technology tags
        technologies = ['react', 'python', 'javascript', 'api', 'database', 'ui', 'ux', 'testing', 'automation']
        for tech in technologies:
            if tech.lower() in description.lower():
                tags.append(tech.lower())

        # Process tags
        processes = ['planning', 'design', 'development', 'deployment', 'monitoring', 'optimization']
        for process in processes:
            if process.lower() in description.lower():
                tags.append(process.lower())

        # Outcome tags
        outcomes = ['performance', 'usability', 'scalability', 'security', 'reliability', 'efficiency']
        for outcome in outcomes:
            if outcome.lower() in description.lower():
                tags.append(outcome.lower())

        return list(set(tags))

    def _save_knowledge_share(self, knowledge_share: KnowledgeShare):
        """Save knowledge share to persistent storage"""
        shares = self._load_knowledge_shares()
        shares.append(asdict(knowledge_share))

        with open(self.knowledge_shares_file, 'w', encoding='utf-8') as f:
            json.dump(shares, f, indent=2)

    def _load_knowledge_shares(self) -> List[Dict]:
        """Load existing knowledge shares"""
        if not os.path.exists(self.knowledge_shares_file):
            return []

        try:
            with open(self.knowledge_shares_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def generate_collaboration_insights(self) -> List[CollaborationInsight]:
        """Generate insights for cross-goal collaboration"""
        insights = []

        # Analyze goal similarities for collaboration opportunities
        similarities = self.analyze_goal_similarities()

        for similarity in similarities:
            if similarity.collaboration_potential in ['high', 'medium']:
                # Pattern transfer opportunity
                if similarity.shared_elements:
                    insight = CollaborationInsight(
                        insight_id=f"collab_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        insight_type='pattern_transfer',
                        description=f"Goals '{similarity.goal_a}' and '{similarity.goal_b}' share similar elements: {', '.join(similarity.shared_elements[:2])}. Consider sharing successful patterns and approaches.",
                        affected_goals=[similarity.goal_a, similarity.goal_b],
                        potential_benefits=['Accelerated learning', 'Reduced duplication', 'Improved consistency'],
                        implementation_effort='low',
                        success_probability=similarity.similarity_score,
                        created_date=datetime.now().isoformat()
                    )
                    insights.append(insight)

                # Resource sharing opportunity
                if similarity.complementary_aspects:
                    insight = CollaborationInsight(
                        insight_id=f"collab_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        insight_type='resource_sharing',
                        description=f"Goals '{similarity.goal_a}' and '{similarity.goal_b}' have complementary aspects: {', '.join(similarity.complementary_aspects[:2])}. Consider sharing resources and expertise.",
                        affected_goals=[similarity.goal_a, similarity.goal_b],
                        potential_benefits=['Resource optimization', 'Knowledge sharing', 'Efficiency gains'],
                        implementation_effort='medium',
                        success_probability=similarity.similarity_score * 0.8,
                        created_date=datetime.now().isoformat()
                    )
                    insights.append(insight)

        # Save collaboration insights
        if insights:
            self._save_collaboration_insights(insights)

        return insights

    def _save_collaboration_insights(self, insights: List[CollaborationInsight]):
        """Save collaboration insights"""
        insights_data = [asdict(i) for i in insights]

        with open(self.collaboration_insights_file, 'w', encoding='utf-8') as f:
            json.dump(insights_data, f, indent=2)

    def get_collaboration_recommendations(self, current_goal: Optional[str] = None) -> List[str]:
        """Get collaboration recommendations for goals"""
        recommendations = []

        # Load existing knowledge shares
        shares = self._load_knowledge_shares()

        if current_goal:
            # Find knowledge shares relevant to current goal
            relevant_shares = [s for s in shares if current_goal in s['target_goals']]
            recommendations.extend(self._generate_goal_specific_recommendations(current_goal, relevant_shares))
        else:
            # General collaboration recommendations
            similarities = self.analyze_goal_similarities()
            high_potential = [s for s in similarities if s.collaboration_potential == 'high']

            if high_potential:
                recommendations.append(f"High collaboration potential: {len(high_potential)} goal pairs identified")
                for similarity in high_potential[:3]:
                    recommendations.append(f"Consider collaboration between '{similarity.goal_a}' and '{similarity.goal_b}'")

        # Generate insights if we have enough data
        if len(self._get_all_goals()) >= 2:
            collaboration_insights = self.generate_collaboration_insights()
            for insight in collaboration_insights[:3]:
                recommendations.append(f"Collaboration opportunity: {insight.description}")

        return recommendations if recommendations else ["No specific collaboration opportunities identified yet."]

    def _generate_goal_specific_recommendations(self, goal: str, relevant_shares: List[Dict]) -> List[str]:
        """Generate recommendations specific to a goal"""
        recommendations = []

        for share in relevant_shares:
            if share['status'] == 'active':
                applicability_icon = {
                    'direct': '🔗',
                    'adaptable': '🔄',
                    'inspirational': '💡'
                }.get(share['applicability'], '❓')

                recommendations.append(f"{applicability_icon} {share['knowledge_type'].title()}: {share['title']} (relevance: {share['relevance_score']}/10)")

        return recommendations

    def generate_collaboration_report(self, output_format: str = 'text') -> str:
        """Generate comprehensive collaboration report"""
        goals = self._get_all_goals()
        similarities = self.analyze_goal_similarities()
        knowledge_shares = self._load_knowledge_shares()
        collaboration_insights = self.generate_collaboration_insights()

        if output_format == 'json':
            report_data = {
                'total_goals': len(goals),
                'goal_similarities': [asdict(s) for s in similarities],
                'knowledge_shares': knowledge_shares,
                'collaboration_insights': [asdict(i) for i in collaboration_insights],
                'collaboration_potential': self._assess_overall_collaboration_potential(similarities),
                'generated_at': datetime.now().isoformat()
            }
            return json.dumps(report_data, indent=2)

        # Generate text report
        report = self._generate_text_collaboration_report(goals, similarities, knowledge_shares, collaboration_insights)
        return report

    def _assess_overall_collaboration_potential(self, similarities: List[GoalSimilarity]) -> Dict[str, Any]:
        """Assess overall collaboration potential across project"""
        if not similarities:
            return {'level': 'low', 'score': 0, 'opportunities': 0}

        high_potential = len([s for s in similarities if s.collaboration_potential == 'high'])
        medium_potential = len([s for s in similarities if s.collaboration_potential == 'medium'])

        total_potential = high_potential * 3 + medium_potential * 2
        max_potential = len(similarities) * 3

        if max_potential == 0:
            return {'level': 'none', 'score': 0, 'opportunities': 0}

        score = (total_potential / max_potential) * 10

        if score >= 7:
            level = 'high'
        elif score >= 4:
            level = 'medium'
        else:
            level = 'low'

        return {
            'level': level,
            'score': round(score, 2),
            'opportunities': len(similarities)
        }

    def _generate_text_collaboration_report(self, goals: List[str], similarities: List[GoalSimilarity],
                                          knowledge_shares: List[Dict], collaboration_insights: List[CollaborationInsight]) -> str:
        """Generate formatted text collaboration report"""
        lines = []
        lines.append("=" * 80)
        lines.append("GOAL KIT COLLABORATION HUB REPORT")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)

        # Project overview
        lines.append(f"\n🏗️ PROJECT COLLABORATION OVERVIEW")
        lines.append("-" * 50)
        lines.append(f"Total Goals: {len(goals)}")
        lines.append(f"Goal Similarities Found: {len(similarities)}")
        lines.append(f"Knowledge Shares: {len(knowledge_shares)}")
        lines.append(f"Collaboration Insights: {len(collaboration_insights)}")

        # Collaboration potential assessment
        potential = self._assess_overall_collaboration_potential(similarities)
        lines.append(f"Collaboration Potential: {potential['level'].upper()} ({potential['score']}/10)")

        # Goal similarities
        if similarities:
            lines.append("\n🔗 GOAL SIMILARITIES")
            lines.append("-" * 50)

            for similarity in sorted(similarities, key=lambda x: x.similarity_score, reverse=True)[:5]:
                potential_icon = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }.get(similarity.collaboration_potential, '⚪')

                lines.append(f"{potential_icon} {similarity.goal_a} ↔ {similarity.goal_b}")
                lines.append(f"   Similarity: {similarity.similarity_score}/10")

                if similarity.shared_elements:
                    lines.append(f"   Shared: {', '.join(similarity.shared_elements[:2])}")

                if similarity.complementary_aspects:
                    lines.append(f"   Complementary: {', '.join(similarity.complementary_aspects[:2])}")

        # Knowledge shares
        if knowledge_shares:
            lines.append("\n📚 KNOWLEDGE SHARES")
            lines.append("-" * 50)

            for share in knowledge_shares[:5]:
                status_icon = {'active': '🟢', 'applied': '✅', 'pending': '⏳'}.get(share['status'], '❓')
                lines.append(f"{status_icon} {share['title']}")
                lines.append(f"   From: {share['source_goal']} → To: {', '.join(share['target_goals'])}")
                lines.append(f"   Type: {share['knowledge_type']} | Relevance: {share['relevance_score']}/10")

        # Collaboration insights
        if collaboration_insights:
            lines.append("\n💡 COLLABORATION INSIGHTS")
            lines.append("-" * 50)

            for insight in collaboration_insights[:5]:
                effort_icon = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}.get(insight.implementation_effort, '❓')
                lines.append(f"{effort_icon} {insight.insight_type.replace('_', ' ').title()}")
                lines.append(f"   {insight.description}")
                lines.append(f"   Success Probability: {insight.success_probability}/10")

        # Recommendations
        lines.append("\n🚀 COLLABORATION RECOMMENDATIONS")
        lines.append("-" * 50)

        if potential['level'] == 'high':
            lines.append("🔴 High collaboration potential - prioritize cross-goal coordination")
        elif potential['level'] == 'medium':
            lines.append("🟡 Medium collaboration potential - consider selective knowledge sharing")
        else:
            lines.append("🟢 Low collaboration potential - focus on individual goal execution")

        if not similarities:
            lines.append("Consider capturing more learnings to identify collaboration opportunities")
            lines.append("Use the learning system to build knowledge base for pattern sharing")

        lines.append("=" * 80)
        return "\n".join(lines)


def main():
    """Main collaboration hub function"""
    if not test_git_repo():
        write_error("Not in a git repository")
        write_info("Please run this from the root of a Goal Kit project")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(description='Goal Kit Collaboration Hub')
    parser.add_argument('--analyze-similarities', action='store_true', help='Analyze goal similarities for collaboration')
    parser.add_argument('--share-knowledge', nargs=4, metavar=('SOURCE', 'TARGETS', 'TYPE', 'TITLE'),
                       help='Share knowledge: source_goal "target1,target2" type "title"')
    parser.add_argument('--recommendations', nargs='?', const='all', metavar='GOAL',
                       help='Get collaboration recommendations for goal(s)')
    parser.add_argument('--report', action='store_true', help='Generate comprehensive collaboration report')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')

    args = parser.parse_args()

    try:
        hub = CollaborationHub()

        if args.analyze_similarities:
            similarities = hub.analyze_goal_similarities()
            if args.json:
                print(json.dumps([asdict(s) for s in similarities], indent=2))
            else:
                print(f"\n🔗 GOAL SIMILARITY ANALYSIS")
                print(f"Found {len(similarities)} goal similarities")

                for similarity in similarities[:5]:
                    print(f"  {similarity.goal_a} ↔ {similarity.goal_b}: {similarity.similarity_score}/10")

        elif args.share_knowledge:
            source_goal, targets_str, knowledge_type, title = args.share_knowledge
            target_goals = [t.strip() for t in targets_str.split(',')]

            # Get description from remaining arguments
            description = " ".join(args.share_knowledge[4:]) if len(args.share_knowledge) > 4 else title

            share_id = hub.share_knowledge_between_goals(source_goal, target_goals, knowledge_type, title, description)
            print(f"✅ Knowledge shared with ID: {share_id}")

        elif args.recommendations:
            recommendations = hub.get_collaboration_recommendations(args.recommendations if args.recommendations != 'all' else None)
            if args.json:
                print(json.dumps({'recommendations': recommendations}, indent=2))
            else:
                print("\n🤝 COLLABORATION RECOMMENDATIONS")
                for rec in recommendations:
                    print(f"  • {rec}")

        elif args.report:
            report = hub.generate_collaboration_report(args.json)
            print(report)

        else:
            # Default: show collaboration summary
            goals = hub._get_all_goals()
            similarities = hub.analyze_goal_similarities()
            potential = hub._assess_overall_collaboration_potential(similarities)

            print(f"\n🤝 COLLABORATION HUB STATUS")
            print(f"Total Goals: {len(goals)}")
            print(f"Collaboration Potential: {potential['level'].upper()} ({potential['score']}/10)")
            print(f"Opportunities: {potential['opportunities']}")

            if potential['level'] in ['high', 'medium']:
                print("💡 Consider exploring collaboration opportunities between similar goals")
            else:
                print("📈 Focus on individual goal execution and knowledge capture for future collaboration")

    except Exception as e:
        write_error(f"Error in collaboration hub: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()