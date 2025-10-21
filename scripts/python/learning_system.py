#!/usr/bin/env python3
"""
Learning Loop System for Goal Kit Methodology
Automated retrospectives, pattern recognition, and knowledge capture
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
class LearningInsight:
    """Structured learning insight with metadata"""
    insight_id: str
    goal_name: str
    category: str  # 'strategy', 'milestone', 'execution', 'validation', 'risk'
    insight_type: str  # 'success_pattern', 'failure_pattern', 'optimization', 'risk_mitigation'
    title: str
    description: str
    impact: str  # 'high', 'medium', 'low'
    confidence: float  # 0-10 confidence score
    related_goals: List[str]
    tags: List[str]
    created_date: str
    last_updated: str


@dataclass
class RetrospectiveData:
    """Data for automated retrospective analysis"""
    goal_name: str
    time_period: str  # 'sprint', 'milestone', 'project'
    start_date: str
    end_date: str
    achievements: List[str]
    challenges: List[str]
    learnings: List[str]
    improvements: List[str]
    next_steps: List[str]
    metrics: Dict[str, Any]


@dataclass
class PatternAnalysis:
    """Analysis of patterns across goals and projects"""
    pattern_id: str
    pattern_type: str  # 'strategy_success', 'milestone_velocity', 'risk_factor', 'quality_issue'
    description: str
    frequency: int  # How often this pattern occurs
    success_rate: float  # Success rate when this pattern is present
    related_patterns: List[str]
    recommendations: List[str]
    examples: List[str]


class LearningSystem:
    """Automated learning loops and retrospective system"""

    def __init__(self, project_root: str = None):
        self.project_root = project_root or get_git_root()
        if not self.project_root:
            raise ValueError("Must be run from a git repository")

        self.goals_dir = os.path.join(self.project_root, ".goalkit", "goals")
        self.learning_dir = os.path.join(self.project_root, ".goalkit", "learning")
        self.insights_file = os.path.join(self.learning_dir, "insights.json")
        self.patterns_file = os.path.join(self.learning_dir, "patterns.json")
        self.retrospectives_file = os.path.join(self.learning_dir, "retrospectives.json")

        # Create learning directory if it doesn't exist
        os.makedirs(self.learning_dir, exist_ok=True)

    def capture_learning_insight(self, goal_name: str, insight_text: str,
                                category: str = 'general', impact: str = 'medium') -> str:
        """Capture a new learning insight from goal execution"""
        # Generate unique insight ID
        insight_id = f"insight_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Analyze insight for categorization and metadata
        analyzed_insight = self._analyze_insight_text(insight_text, category)

        # Create learning insight
        insight = LearningInsight(
            insight_id=insight_id,
            goal_name=goal_name,
            category=analyzed_insight['category'],
            insight_type=analyzed_insight['insight_type'],
            title=analyzed_insight['title'],
            description=insight_text,
            impact=impact,
            confidence=analyzed_insight['confidence'],
            related_goals=analyzed_insight['related_goals'],
            tags=analyzed_insight['tags'],
            created_date=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat()
        )

        # Save insight
        self._save_insight(insight)

        # Update patterns analysis
        self._update_patterns_analysis(insight)

        write_success(f"Learning insight captured: {insight.title}")
        return insight_id

    def _analyze_insight_text(self, text: str, suggested_category: str) -> Dict[str, Any]:
        """Analyze insight text for categorization and metadata extraction"""
        # Default analysis
        analysis = {
            'category': suggested_category,
            'insight_type': 'general_observation',
            'title': self._generate_insight_title(text),
            'confidence': 7.0,
            'related_goals': [],
            'tags': []
        }

        # Strategy-related insights
        strategy_keywords = [
            'approach', 'strategy', 'method', 'technique', 'framework',
            'architecture', 'design pattern', 'implementation approach'
        ]

        if any(keyword in text.lower() for keyword in strategy_keywords):
            analysis['category'] = 'strategy'
            analysis['insight_type'] = 'strategy_effectiveness'

            # Check for success/failure patterns
            if any(word in text.lower() for word in ['successful', 'worked well', 'effective', 'better than']):
                analysis['insight_type'] = 'success_pattern'
            elif any(word in text.lower() for word in ['failed', 'did not work', 'ineffective', 'worse than']):
                analysis['insight_type'] = 'failure_pattern'

        # Milestone-related insights
        milestone_keywords = [
            'milestone', 'checkpoint', 'progress', 'timeline', 'schedule',
            'velocity', 'pace', 'momentum', 'completion'
        ]

        if any(keyword in text.lower() for keyword in milestone_keywords):
            analysis['category'] = 'milestone'
            analysis['insight_type'] = 'progress_insight'

        # Execution-related insights
        execution_keywords = [
            'implementation', 'execution', 'development', 'coding', 'testing',
            'deployment', 'user feedback', 'iteration', 'pivot'
        ]

        if any(keyword in text.lower() for keyword in execution_keywords):
            analysis['category'] = 'execution'
            analysis['insight_type'] = 'execution_learning'

        # Risk-related insights
        risk_keywords = [
            'risk', 'issue', 'problem', 'challenge', 'obstacle', 'blocker',
            'mitigation', 'prevention', 'warning', 'concern'
        ]

        if any(keyword in text.lower() for keyword in risk_keywords):
            analysis['category'] = 'risk'
            analysis['insight_type'] = 'risk_insight'

        # Extract tags
        analysis['tags'] = self._extract_tags(text)

        # Adjust confidence based on insight quality
        if len(text) > 100:
            analysis['confidence'] = min(analysis['confidence'] + 1, 10)
        if len(analysis['tags']) > 2:
            analysis['confidence'] = min(analysis['confidence'] + 0.5, 10)

        return analysis

    def _generate_insight_title(self, text: str) -> str:
        """Generate a concise title for the insight"""
        # Take first sentence or key phrase
        sentences = re.split(r'[.!?]', text.strip())
        first_sentence = sentences[0].strip()

        # Limit to 60 characters
        if len(first_sentence) > 60:
            return first_sentence[:57] + "..."
        else:
            return first_sentence

    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from insight text"""
        tags = []

        # Technology tags
        technologies = ['react', 'python', 'javascript', 'api', 'database', 'ui', 'ux', 'testing']
        for tech in technologies:
            if tech.lower() in text.lower():
                tags.append(tech.lower())

        # Process tags
        processes = ['planning', 'design', 'development', 'testing', 'deployment', 'monitoring']
        for process in processes:
            if process.lower() in text.lower():
                tags.append(process.lower())

        # Outcome tags
        outcomes = ['performance', 'usability', 'scalability', 'security', 'reliability']
        for outcome in outcomes:
            if outcome.lower() in text.lower():
                tags.append(outcome.lower())

        return list(set(tags))  # Remove duplicates

    def _save_insight(self, insight: LearningInsight):
        """Save learning insight to persistent storage"""
        # Load existing insights
        insights = self._load_insights()

        # Add new insight
        insights.append(asdict(insight))

        # Save back to file
        with open(self.insights_file, 'w', encoding='utf-8') as f:
            json.dump(insights, f, indent=2)

    def _load_insights(self) -> List[Dict]:
        """Load existing insights from storage"""
        if not os.path.exists(self.insights_file):
            return []

        try:
            with open(self.insights_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def generate_retrospective(self, goal_name: str = None, time_period: str = 'recent') -> RetrospectiveData:
        """Generate automated retrospective for goals"""
        if goal_name:
            goals_to_analyze = [goal_name]
        else:
            goals_to_analyze = self._get_active_goals()

        all_achievements = []
        all_challenges = []
        all_learnings = []
        all_improvements = []

        for goal in goals_to_analyze:
            # Analyze goal files for insights
            goal_insights = self._analyze_goal_for_retrospective(goal)

            all_achievements.extend(goal_insights['achievements'])
            all_challenges.extend(goal_insights['challenges'])
            all_learnings.extend(goal_insights['learnings'])
            all_improvements.extend(goal_insights['improvements'])

        # Generate next steps based on learnings
        next_steps = self._generate_next_steps(all_learnings, all_improvements)

        # Calculate time period
        if time_period == 'recent':
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
        else:
            start_date = datetime.now() - timedelta(days=90)
            end_date = datetime.now()

        return RetrospectiveData(
            goal_name=goal_name or 'all_goals',
            time_period=time_period,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            achievements=list(set(all_achievements)),  # Remove duplicates
            challenges=list(set(all_challenges)),
            learnings=list(set(all_learnings)),
            improvements=list(set(all_improvements)),
            next_steps=next_steps,
            metrics=self._calculate_retrospective_metrics(goals_to_analyze)
        )

    def _analyze_goal_for_retrospective(self, goal_name: str) -> Dict[str, List[str]]:
        """Analyze a specific goal for retrospective insights"""
        insights = {
            'achievements': [],
            'challenges': [],
            'learnings': [],
            'improvements': []
        }

        goal_path = os.path.join(self.goals_dir, goal_name)

        # Analyze execution file for insights
        execution_file = os.path.join(goal_path, "execution.md")
        if os.path.exists(execution_file):
            insights.update(self._extract_insights_from_execution(execution_file))

        # Analyze milestone progress
        milestones_file = os.path.join(goal_path, "milestones.md")
        if os.path.exists(milestones_file):
            milestone_insights = self._extract_insights_from_milestones(milestones_file)
            insights['achievements'].extend(milestone_insights.get('achievements', []))
            insights['challenges'].extend(milestone_insights.get('challenges', []))

        # Analyze git history for patterns
        git_insights = self._extract_insights_from_git(goal_name)
        insights['learnings'].extend(git_insights.get('learnings', []))
        insights['improvements'].extend(git_insights.get('improvements', []))

        return insights

    def _extract_insights_from_execution(self, execution_file: str) -> Dict[str, List[str]]:
        """Extract insights from execution file"""
        insights = {
            'achievements': [],
            'challenges': [],
            'learnings': [],
            'improvements': []
        }

        try:
            with open(execution_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Look for learning indicators
            learning_patterns = [
                (r'✅.*learning|insight|discovery', 'learnings'),
                (r'🎯.*achievement|success|accomplished', 'achievements'),
                (r'⚠️.*challenge|issue|problem', 'challenges'),
                (r'💡.*improvement|suggestion|optimization', 'improvements')
            ]

            for pattern, category in learning_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                insights[category].extend(matches)

        except Exception as e:
            write_warning(f"Could not analyze execution file: {e}")

        return insights

    def _extract_insights_from_milestones(self, milestones_file: str) -> Dict[str, List[str]]:
        """Extract insights from milestones file"""
        insights = {
            'achievements': [],
            'challenges': []
        }

        try:
            with open(milestones_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Look for completion indicators
            completed_milestones = re.findall(r'✅.*', content)
            insights['achievements'].extend(completed_milestones)

            # Look for incomplete or problematic milestones
            incomplete_indicators = re.findall(r'[❌⏳].*', content)
            insights['challenges'].extend(incomplete_indicators)

        except Exception as e:
            write_warning(f"Could not analyze milestones file: {e}")

        return insights

    def _extract_insights_from_git(self, goal_name: str) -> Dict[str, List[str]]:
        """Extract insights from git commit history"""
        insights = {
            'learnings': [],
            'improvements': []
        }

        try:
            # Get recent commits for this goal
            result = os.popen(f"cd {self.project_root} && git log --oneline --grep='{goal_name}' --since='30 days ago'").read()

            if result.strip():
                # Analyze commit messages for learning patterns
                commits = result.strip().split('\n')

                for commit in commits:
                    if any(word in commit.lower() for word in ['fix', 'improve', 'optimize', 'refactor']):
                        insights['improvements'].append(commit)
                    elif any(word in commit.lower() for word in ['learn', 'discover', 'realize', 'insight']):
                        insights['learnings'].append(commit)

        except Exception as e:
            write_warning(f"Could not analyze git history: {e}")

        return insights

    def _generate_next_steps(self, learnings: List[str], improvements: List[str]) -> List[str]:
        """Generate actionable next steps based on learnings"""
        next_steps = []

        # Analyze learnings for patterns
        if any('user feedback' in learning.lower() for learning in learnings):
            next_steps.append("Incorporate user feedback into next iteration")

        if any('performance' in learning.lower() for learning in learnings):
            next_steps.append("Focus on performance optimization in next milestone")

        if any('testing' in learning.lower() for learning in learnings):
            next_steps.append("Enhance testing strategy for better quality assurance")

        if any('communication' in learning.lower() for learning in learnings):
            next_steps.append("Improve stakeholder communication and alignment")

        # Add improvement-based steps
        if any('automation' in improvement.lower() for improvement in improvements):
            next_steps.append("Identify additional automation opportunities")

        if any('process' in improvement.lower() for improvement in improvements):
            next_steps.append("Document and standardize improved processes")

        # Default next steps if no specific patterns found
        if not next_steps:
            next_steps.extend([
                "Review and apply successful patterns to other goals",
                "Document key learnings for future reference",
                "Plan next iteration based on insights gained"
            ])

        return list(set(next_steps))  # Remove duplicates

    def _calculate_retrospective_metrics(self, goals_analyzed: List[str]) -> Dict[str, Any]:
        """Calculate metrics for retrospective period"""
        metrics = {
            'goals_analyzed': len(goals_analyzed),
            'total_insights_captured': 0,
            'learning_velocity': 0.0,
            'improvement_rate': 0.0
        }

        # Count total insights
        insights = self._load_insights()
        metrics['total_insights_captured'] = len(insights)

        # Calculate learning velocity (insights per week)
        if insights:
            oldest_insight = min(datetime.fromisoformat(i['created_date']) for i in insights)
            weeks_elapsed = max((datetime.now() - oldest_insight).days / 7, 1)
            metrics['learning_velocity'] = len(insights) / weeks_elapsed

        return metrics

    def _update_patterns_analysis(self, insight: LearningInsight):
        """Update patterns analysis with new insight"""
        # Load existing patterns
        patterns = self._load_patterns()

        # Find or create pattern for this insight type
        pattern_key = f"{insight.category}_{insight.insight_type}"

        if pattern_key in patterns:
            patterns[pattern_key]['frequency'] += 1
            patterns[pattern_key]['examples'].append(insight.title)
        else:
            patterns[pattern_key] = {
                'pattern_id': pattern_key,
                'pattern_type': insight.insight_type,
                'description': f"Pattern in {insight.category} related to {insight.insight_type}",
                'frequency': 1,
                'success_rate': insight.confidence / 10.0,
                'related_patterns': [],
                'recommendations': [insight.title],
                'examples': [insight.title]
            }

        # Save updated patterns
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump(patterns, f, indent=2)

    def _load_patterns(self) -> Dict[str, Any]:
        """Load existing patterns from storage"""
        if not os.path.exists(self.patterns_file):
            return {}

        try:
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def get_learning_recommendations(self, current_goal: str = None) -> List[str]:
        """Get learning-based recommendations for current work"""
        recommendations = []

        # Load insights and patterns
        insights = self._load_insights()
        patterns = self._load_patterns()

        if not insights:
            return ["No learning data available yet. Start capturing insights from goal execution."]

        # Filter insights by relevance
        relevant_insights = []
        if current_goal:
            relevant_insights = [i for i in insights if i['goal_name'] == current_goal or current_goal in i['related_goals']]
        else:
            relevant_insights = insights

        if not relevant_insights:
            return ["No specific learnings for current goal yet. Consider capturing insights from execution."]

        # Generate recommendations based on insights
        success_patterns = [i for i in relevant_insights if i['insight_type'] == 'success_pattern']
        failure_patterns = [i for i in relevant_insights if i['insight_type'] == 'failure_pattern']

        # Success pattern recommendations
        for pattern in success_patterns[:3]:  # Top 3 success patterns
            recommendations.append(f"Apply success pattern: {pattern['title']}")

        # Failure pattern avoidance
        for pattern in failure_patterns[:2]:  # Top 2 failure patterns to avoid
            recommendations.append(f"Avoid failure pattern: {pattern['title']}")

        # Pattern-based recommendations
        high_frequency_patterns = [p for p in patterns.values() if p['frequency'] >= 3]
        for pattern in high_frequency_patterns[:2]:
            recommendations.append(f"Consider {pattern['pattern_type']} pattern: {pattern['description']}")

        return recommendations if recommendations else ["Continue current approach and capture learnings for future optimization."]

    def generate_learning_report(self, output_format: str = 'text') -> str:
        """Generate comprehensive learning report"""
        insights = self._load_insights()
        patterns = self._load_patterns()

        if output_format == 'json':
            report_data = {
                'total_insights': len(insights),
                'total_patterns': len(patterns),
                'insights_by_category': self._categorize_insights(insights),
                'top_patterns': list(patterns.values())[:10],
                'recent_insights': insights[-10:] if insights else [],
                'generated_at': datetime.now().isoformat()
            }
            return json.dumps(report_data, indent=2)

        # Generate text report
        report = self._generate_text_learning_report(insights, patterns)
        return report

    def _categorize_insights(self, insights: List[Dict]) -> Dict[str, int]:
        """Categorize insights by type and category"""
        categories = defaultdict(int)

        for insight in insights:
            key = f"{insight['category']}_{insight['insight_type']}"
            categories[key] += 1

        return dict(categories)

    def _generate_text_learning_report(self, insights: List[Dict], patterns: Dict) -> str:
        """Generate formatted text learning report"""
        lines = []
        lines.append("=" * 80)
        lines.append("GOAL KIT LEARNING SYSTEM REPORT")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)

        # Summary statistics
        lines.append(f"\n📊 LEARNING SUMMARY")
        lines.append("-" * 40)
        lines.append(f"Total Insights Captured: {len(insights)}")
        lines.append(f"Pattern Types Identified: {len(patterns)}")

        if insights:
            # Recent insights
            lines.append("\n🔍 RECENT INSIGHTS")
            lines.append("-" * 40)

            for insight in insights[-5:]:  # Last 5 insights
                impact_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(insight['impact'], '⚪')
                lines.append(f"{impact_icon} [{insight['category'].upper()}] {insight['title']}")
                lines.append(f"   Goal: {insight['goal_name']} | Confidence: {insight['confidence']}")

        if patterns:
            # Top patterns
            lines.append("\n🎯 TOP PATTERNS")
            lines.append("-" * 40)

            sorted_patterns = sorted(patterns.values(), key=lambda x: x['frequency'], reverse=True)
            for pattern in sorted_patterns[:5]:  # Top 5 patterns
                lines.append(f"📈 {pattern['pattern_type']}: {pattern['description']}")
                lines.append(f"   Frequency: {pattern['frequency']} | Success Rate: {pattern['success_rate']:.1%}")

        # Recommendations
        lines.append("\n💡 LEARNING RECOMMENDATIONS")
        lines.append("-" * 40)

        if insights:
            # Generate recommendations based on insights
            high_impact_insights = [i for i in insights if i['impact'] == 'high']
            if high_impact_insights:
                lines.append("High-priority learnings to apply:")
                for insight in high_impact_insights[:3]:
                    lines.append(f"  • {insight['title']}")

            # Pattern-based recommendations
            success_patterns = [i for i in insights if i['insight_type'] == 'success_pattern']
            if success_patterns:
                lines.append("\nSuccess patterns to replicate:")
                for pattern in success_patterns[:3]:
                    lines.append(f"  • {pattern['title']}")
        else:
            lines.append("No learning data available yet.")
            lines.append("Start capturing insights from goal execution to build knowledge base.")

        lines.append("=" * 80)
        return "\n".join(lines)


def main():
    """Main learning system function"""
    if not test_git_repo():
        write_error("Not in a git repository")
        write_info("Please run this from the root of a Goal Kit project")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(description='Goal Kit Learning System')
    parser.add_argument('--capture', nargs=2, metavar=('GOAL', 'INSIGHT'),
                       help='Capture learning insight: goal_name "insight description"')
    parser.add_argument('--retrospective', nargs='?', const='recent', metavar='PERIOD',
                       help='Generate retrospective report (recent, project)')
    parser.add_argument('--recommendations', nargs='?', const='current', metavar='GOAL',
                       help='Get learning recommendations for goal')
    parser.add_argument('--report', action='store_true', help='Generate comprehensive learning report')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')

    args = parser.parse_args()

    try:
        system = LearningSystem()

        if args.capture:
            goal_name, insight_text = args.capture
            insight_id = system.capture_learning_insight(goal_name, insight_text)
            print(f"✅ Learning insight captured with ID: {insight_id}")

        elif args.retrospective:
            retro = system.generate_retrospective(time_period=args.retrospective)
            if args.json:
                print(json.dumps(asdict(retro), indent=2))
            else:
                print("\n📋 RETROSPECTIVE REPORT")
                print(f"Goal(s): {retro.goal_name}")
                print(f"Period: {retro.start_date} to {retro.end_date}")

                if retro.achievements:
                    print("\n✅ Achievements:")
                    for achievement in retro.achievements:
                        print(f"  • {achievement}")

                if retro.challenges:
                    print("\n⚠️ Challenges:")
                    for challenge in retro.challenges:
                        print(f"  • {challenge}")

                if retro.learnings:
                    print("\n💡 Learnings:")
                    for learning in retro.learnings:
                        print(f"  • {learning}")

                if retro.next_steps:
                    print("\n🚀 Next Steps:")
                    for step in retro.next_steps:
                        print(f"  • {step}")

        elif args.recommendations:
            recommendations = system.get_learning_recommendations(args.recommendations if args.recommendations != 'current' else None)
            if args.json:
                print(json.dumps({'recommendations': recommendations}, indent=2))
            else:
                print("\n💡 LEARNING RECOMMENDATIONS")
                for rec in recommendations:
                    print(f"  • {rec}")

        elif args.report:
            report = system.generate_learning_report(args.json)
            print(report)

        else:
            # Default: show learning summary
            insights = system._load_insights()
            patterns = system._load_patterns()

            print(f"\n🧠 LEARNING SYSTEM STATUS")
            print(f"Total Insights: {len(insights)}")
            print(f"Pattern Types: {len(patterns)}")

            if not insights:
                print("No learning data yet. Use --capture to start building knowledge base.")

    except Exception as e:
        write_error(f"Error in learning system: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()