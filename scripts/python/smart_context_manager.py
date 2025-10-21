#!/usr/bin/env python3
"""
Smart Context Management System for Goal Kit
Dynamic, intelligent context updates based on project state and progress
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

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
class ContextIntelligence:
    """Intelligent context data for agents"""
    project_name: str
    current_phase: str  # 'vision', 'goal_creation', 'strategy', 'milestone', 'execution'
    project_health: str  # 'excellent', 'good', 'concerning', 'critical'
    active_goals: List[str]
    recent_achievements: List[str]
    current_focus: str
    recommended_actions: List[str]
    risk_factors: List[str]
    success_patterns: List[str]
    last_updated: str


@dataclass
class AdaptiveContext:
    """Adaptive context that changes based on project state"""
    core_methodology: str
    current_priorities: List[str]
    progress_insights: str
    quality_standards: str
    collaboration_notes: str
    learning_highlights: str
    next_milestone_focus: str


class SmartContextManager:
    """Intelligent context management system"""

    def __init__(self, project_root: str = None):
        self.project_root = project_root or get_git_root()
        if not self.project_root:
            raise ValueError("Must be run from a git repository")

        self.vision_file = os.path.join(self.project_root, ".goalkit", "vision.md")
        self.goals_dir = os.path.join(self.project_root, ".goalkit", "goals")
        self.analytics_dir = os.path.join(self.project_root, ".goalkit", "analytics")

        # Context priorities based on project phase
        self.phase_priorities = {
            'vision': ['methodology_compliance', 'quality_standards', 'foundation_building'],
            'goal_creation': ['outcome_focus', 'measurability', 'specificity'],
            'strategy': ['multiple_approaches', 'risk_assessment', 'validation_planning'],
            'milestone': ['progress_tracking', 'success_measurement', 'adaptation_readiness'],
            'execution': ['learning_integration', 'metric_tracking', 'continuous_improvement']
        }

    def analyze_project_state(self) -> ContextIntelligence:
        """Analyze current project state for intelligent context"""
        project_name = os.path.basename(self.project_root)

        # Determine current phase
        current_phase = self._determine_current_phase()

        # Assess project health
        project_health = self._assess_project_health()

        # Get active goals
        active_goals = self._get_active_goals()

        # Identify recent achievements
        recent_achievements = self._get_recent_achievements()

        # Determine current focus
        current_focus = self._determine_current_focus(current_phase, active_goals)

        # Generate recommended actions
        recommended_actions = self._generate_recommendations(current_phase, project_health, active_goals)

        # Identify risk factors
        risk_factors = self._identify_risk_factors(project_health, active_goals)

        # Extract success patterns
        success_patterns = self._extract_success_patterns()

        return ContextIntelligence(
            project_name=project_name,
            current_phase=current_phase,
            project_health=project_health,
            active_goals=active_goals,
            recent_achievements=recent_achievements,
            current_focus=current_focus,
            recommended_actions=recommended_actions,
            risk_factors=risk_factors,
            success_patterns=success_patterns,
            last_updated=datetime.now().isoformat()
        )

    def _determine_current_phase(self) -> str:
        """Determine the current project phase"""
        # Check for vision
        if not os.path.exists(self.vision_file):
            return 'vision'

        # Check for active goals
        if not os.path.exists(self.goals_dir):
            return 'goal_creation'

        active_goals = self._get_active_goals()
        if not active_goals:
            return 'goal_creation'

        # Check for strategies in goals
        strategies_found = 0
        for goal in active_goals:
            goal_path = os.path.join(self.goals_dir, goal)
            strategies_file = os.path.join(goal_path, "strategies.md")
            if os.path.exists(strategies_file):
                strategies_found += 1

        if strategies_found == 0:
            return 'strategy'
        elif strategies_found < len(active_goals):
            return 'strategy'  # Some goals need strategies

        # Check for milestones
        milestones_found = 0
        for goal in active_goals:
            goal_path = os.path.join(self.goals_dir, goal)
            milestones_file = os.path.join(goal_path, "milestones.md")
            if os.path.exists(milestones_file):
                milestones_found += 1

        if milestones_found < len(active_goals):
            return 'milestone'

        return 'execution'

    def _assess_project_health(self) -> str:
        """Assess overall project health"""
        # Check for recent activity (git commits in last 7 days)
        try:
            result = os.popen(f"cd {self.project_root} && git log --since='7 days ago' --oneline | wc -l").read()
            recent_commits = int(result.strip())
            if recent_commits >= 3:
                activity_score = 10
            elif recent_commits >= 1:
                activity_score = 7
            else:
                activity_score = 3
        except:
            activity_score = 5

        # Check for validation issues
        validation_score = self._check_validation_health()

        # Check for progress indicators
        progress_score = self._check_progress_health()

        # Calculate overall health
        overall_score = (activity_score + validation_score + progress_score) / 3

        if overall_score >= 8:
            return 'excellent'
        elif overall_score >= 6:
            return 'good'
        elif overall_score >= 4:
            return 'concerning'
        else:
            return 'critical'

    def _check_validation_health(self) -> int:
        """Check validation health score"""
        try:
            # Try to run enhanced validator if available
            import subprocess
            result = subprocess.run([
                sys.executable, "scripts/python/enhanced_validator.py", "--json"
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                data = json.loads(result.stdout)
                if 'validation_results' in data:
                    scores = [r.get('overall_score', 0) for r in data['validation_results']]
                    if scores:
                        return sum(scores) / len(scores)
        except:
            pass

        return 5  # Default moderate score

    def _check_progress_health(self) -> int:
        """Check progress health indicators"""
        # Look for progress indicators in recent files
        progress_indicators = [
            '✅', 'completed', 'done', 'finished',
            'progress', 'milestone', 'achievement'
        ]

        score = 5  # Base score

        try:
            # Check recent git commits for progress keywords
            result = os.popen(f"cd {self.project_root} && git log --since='14 days ago' --oneline").read()
            found_indicators = sum(1 for indicator in progress_indicators if indicator.lower() in result.lower())
            score += min(found_indicators * 2, 5)  # Up to +5 points
        except:
            pass

        return min(score, 10)

    def _get_active_goals(self) -> List[str]:
        """Get list of active goal directories"""
        if not os.path.exists(self.goals_dir):
            return []

        active_goals = []
        for item in os.listdir(self.goals_dir):
            goal_path = os.path.join(self.goals_dir, item)
            if os.path.isdir(goal_path):
                # Check if goal has recent activity
                goal_file = os.path.join(goal_path, "goal.md")
                if os.path.exists(goal_file):
                    active_goals.append(item)

        return active_goals

    def _get_recent_achievements(self) -> List[str]:
        """Get recent project achievements"""
        achievements = []

        try:
            # Check git log for achievement indicators
            result = os.popen(f"cd {self.project_root} && git log --since='14 days ago' --oneline").read()
            achievement_patterns = [
                'complete', 'finish', 'achieve', 'milestone', 'goal',
                'success', 'validate', 'approve'
            ]

            for pattern in achievement_patterns:
                if pattern.lower() in result.lower():
                    achievements.append(f"Recent {pattern} activity detected")
                    break

        except:
            pass

        # Check for validation successes
        if len(achievements) == 0:
            achievements.append("Project initialization complete")

        return achievements[:3]  # Return top 3 achievements

    def _determine_current_focus(self, phase: str, active_goals: List[str]) -> str:
        """Determine what the current focus should be"""
        focus_templates = {
            'vision': 'Establishing project vision and guiding principles',
            'goal_creation': 'Creating goals with measurable success criteria',
            'strategy': 'Exploring multiple implementation strategies',
            'milestone': 'Defining measurable milestones and progress indicators',
            'execution': 'Implementing with learning and adaptation'
        }

        base_focus = focus_templates.get(phase, 'General project development')

        if active_goals:
            goal_count = len(active_goals)
            if goal_count == 1:
                base_focus += f" (focusing on {active_goals[0]})"
            else:
                base_focus += f" (managing {goal_count} active goals)"

        return base_focus

    def _generate_recommendations(self, phase: str, health: str, active_goals: List[str]) -> List[str]:
        """Generate intelligent recommendations"""
        recommendations = []

        # Phase-based recommendations
        if phase == 'vision':
            recommendations.append("Use /goalkit.vision to establish project foundation")
            recommendations.append("Focus on measurable outcomes and success criteria")
        elif phase == 'goal_creation':
            recommendations.append("Use /goalkit.goal to create first goal with specific metrics")
            recommendations.append("Ensure goals focus on outcomes, not implementation")
        elif phase == 'strategy':
            recommendations.append("Use /goalkit.strategies to explore multiple approaches")
            recommendations.append("Consider 3+ different strategies for each goal")
        elif phase == 'milestone':
            recommendations.append("Use /goalkit.milestones to create measurable checkpoints")
            recommendations.append("Define clear success indicators for each milestone")
        elif phase == 'execution':
            recommendations.append("Use /goalkit.execute to implement with learning loops")
            recommendations.append("Track metrics and adapt based on results")

        # Health-based recommendations
        if health in ['concerning', 'critical']:
            recommendations.append("Run enhanced validation to identify quality issues")
            recommendations.append("Review progress tracking for bottleneck identification")

        if health == 'critical':
            recommendations.append("Consider project realignment or scope adjustment")

        # Goal-based recommendations
        if len(active_goals) > 3:
            recommendations.append("Consider focusing on fewer goals for better progress")

        return recommendations[:4]  # Return top 4 recommendations

    def _identify_risk_factors(self, health: str, active_goals: List[str]) -> List[str]:
        """Identify current risk factors"""
        risks = []

        if health in ['concerning', 'critical']:
            risks.append(f"Project health is {health} - review validation results")

        if len(active_goals) > 5:
            risks.append("High number of active goals may impact focus")

        # Check for stalled goals (no recent activity)
        stalled_goals = 0
        for goal in active_goals:
            goal_path = os.path.join(self.goals_dir, goal)
            # Simple check: look for recent modifications
            try:
                mtime = os.path.getmtime(os.path.join(goal_path, "goal.md"))
                days_since_modification = (datetime.now().timestamp() - mtime) / (24 * 3600)
                if days_since_modification > 14:
                    stalled_goals += 1
            except:
                pass

        if stalled_goals > 0:
            risks.append(f"{stalled_goals} goals appear stalled (>14 days since last update)")

        if not risks:
            risks.append("No significant risk factors identified")

        return risks[:3]

    def _extract_success_patterns(self) -> List[str]:
        """Extract patterns from successful project elements"""
        patterns = []

        # Look for validation successes
        try:
            import subprocess
            result = subprocess.run([
                sys.executable, "scripts/python/enhanced_validator.py", "--json"
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                data = json.loads(result.stdout)
                high_scores = [r for r in data.get('validation_results', []) if r.get('overall_score', 0) >= 8.0]

                if high_scores:
                    patterns.append(f"{len(high_scores)} high-quality methodology components identified")
        except:
            pass

        # Look for progress indicators
        if not patterns:
            patterns.append("Standard Goal-Driven Development patterns in use")

        return patterns[:2]

    def generate_adaptive_context(self, intelligence: ContextIntelligence) -> AdaptiveContext:
        """Generate adaptive context based on current state"""
        # Core methodology (always consistent)
        core_methodology = """Focus on outcomes over specifications. Every goal must have:
- Measurable success criteria (percentages, timeframes, user counts)
- Multiple strategy exploration before implementation
- Learning and adaptation during execution"""

        # Current priorities based on phase
        current_priorities = self.phase_priorities.get(intelligence.current_phase, [])

        # Progress insights
        progress_insights = self._generate_progress_insights(intelligence)

        # Quality standards based on project health
        quality_standards = self._generate_quality_standards(intelligence.project_health)

        # Collaboration notes
        collaboration_notes = self._generate_collaboration_notes(intelligence)

        # Learning highlights
        learning_highlights = self._generate_learning_highlights(intelligence)

        # Next milestone focus
        next_milestone_focus = self._generate_milestone_focus(intelligence)

        return AdaptiveContext(
            core_methodology=core_methodology,
            current_priorities=current_priorities,
            progress_insights=progress_insights,
            quality_standards=quality_standards,
            collaboration_notes=collaboration_notes,
            learning_highlights=learning_highlights,
            next_milestone_focus=next_milestone_focus
        )

    def _generate_progress_insights(self, intelligence: ContextIntelligence) -> str:
        """Generate progress insights"""
        if intelligence.project_health == 'excellent':
            return "Project is progressing exceptionally well. Maintain current momentum and focus on continuous improvement."
        elif intelligence.project_health == 'good':
            return "Project is on track. Continue following methodology and address any validation recommendations."
        elif intelligence.project_health == 'concerning':
            return "Project needs attention. Review validation results and consider adjusting approach or scope."
        else:
            return "Project is at critical risk. Immediate review and potential realignment required."

    def _generate_quality_standards(self, health: str) -> str:
        """Generate quality standards based on project health"""
        base_standards = """Quality Standards:
- Goals must have specific, measurable targets (%, $, timeframes, user counts)
- All methodology components must score 7.0+ on validation
- Success metrics must be tracked and validated
- Learning must be captured and applied"""

        if health in ['concerning', 'critical']:
            base_standards += "\n- Enhanced validation required before proceeding"
            base_standards += "\n- Progress review mandatory for stalled components"

        return base_standards

    def _generate_collaboration_notes(self, intelligence: ContextIntelligence) -> str:
        """Generate collaboration guidance"""
        notes = f"""Collaboration Focus:
- Current Phase: {intelligence.current_phase}
- Active Goals: {len(intelligence.active_goals)}
- Project Health: {intelligence.project_health}"""

        if len(intelligence.active_goals) > 1:
            notes += "\n- Coordinate across multiple goals for consistency"
            notes += "\n- Share learning and patterns between goals"

        return notes

    def _generate_learning_highlights(self, intelligence: ContextIntelligence) -> str:
        """Generate learning highlights"""
        highlights = "Learning Focus:"

        if intelligence.recent_achievements:
            highlights += f"\n- Recent achievements: {', '.join(intelligence.recent_achievements)}"

        if intelligence.success_patterns:
            highlights += f"\n- Success patterns: {', '.join(intelligence.success_patterns)}"

        highlights += f"\n- Current focus: {intelligence.current_focus}"

        return highlights

    def _generate_milestone_focus(self, intelligence: ContextIntelligence) -> str:
        """Generate next milestone focus"""
        if intelligence.current_phase == 'vision':
            return "Complete project vision with measurable success criteria"
        elif intelligence.current_phase == 'goal_creation':
            return "Create first goal with specific, measurable targets"
        elif intelligence.current_phase == 'strategy':
            return "Explore 3+ implementation strategies for active goals"
        elif intelligence.current_phase == 'milestone':
            return "Define measurable milestones with clear success indicators"
        else:
            return "Execute implementation with continuous learning and adaptation"

    def update_agent_context_files(self):
        """Update all agent context files with intelligent context"""
        intelligence = self.analyze_project_state()
        adaptive_context = self.generate_adaptive_context(intelligence)

        # Generate comprehensive context content
        context_content = self._generate_context_content(intelligence, adaptive_context)

        # Update context files for different agents
        agent_context_files = [
            "CLAUDE.md",
            ".claude/context.md",
            "GEMINI.md",
            ".gemini/context.md",
            "CURSOR.md",
            ".cursor/context.md",
            "QWEN.md",
            ".qwen/context.md",
            "WINDSURF.md",
            ".windsurf/context.md",
            "KILOCODE.md",
            ".kilocode/context.md",
            "ROO.md",
            ".roo/context.md",
            "OPENCODE.md"
        ]

        updated_count = 0
        for context_file in agent_context_files:
            full_path = os.path.join(self.project_root, context_file)
            if self._update_context_file(full_path, context_content):
                updated_count += 1

        write_success(f"Updated {updated_count} agent context files with intelligent context")

    def _generate_context_content(self, intelligence: ContextIntelligence, adaptive_context: AdaptiveContext) -> str:
        """Generate comprehensive context content"""
        return f"""# Goal Kit Project Context (Smart Update)

**Project**: {intelligence.project_name}
**Current Phase**: {intelligence.current_phase}
**Project Health**: {intelligence.project_health}
**Last Updated**: {intelligence.last_updated}

## 🎯 CURRENT PROJECT STATE

**Phase**: {intelligence.current_phase.title()}
**Active Goals**: {len(intelligence.active_goals)}
**Recent Achievements**: {', '.join(intelligence.recent_achievements)}
**Current Focus**: {intelligence.current_focus}

## 📊 PROJECT HEALTH ASSESSMENT

**Overall Health**: {intelligence.project_health.upper()}
**Risk Factors**: {', '.join(intelligence.risk_factors)}
**Success Patterns**: {', '.join(intelligence.success_patterns)}

## 🚀 IMMEDIATE RECOMMENDED ACTIONS

{chr(10).join(f"• {action}" for action in intelligence.recommended_actions)}

## 📈 PROGRESS INSIGHTS

{adaptive_context.progress_insights}

## 🎯 CURRENT PRIORITIES

**Core Methodology**:
{adaptive_context.core_methodology}

**Priority Areas**:
{chr(10).join(f"• {priority}" for priority in adaptive_context.current_priorities)}

## 📋 QUALITY STANDARDS

{adaptive_context.quality_standards}

## 🤝 COLLABORATION NOTES

{adaptive_context.collaboration_notes}

## 💡 LEARNING HIGHLIGHTS

{adaptive_context.learning_highlights}

## 🎯 NEXT MILESTONE FOCUS

{adaptive_context.next_milestone_focus}

## 🔧 METHODOLOGY REMINDERS

### Strict Workflow Enforcement
**🛑 STOP AFTER EACH COMMAND - ONE AT A TIME**

1. **`/goalkit.vision`** → Create vision file → **🛑 STOP**
2. **User runs** `/goalkit.goal`** → Create goal → **🛑 STOP**
3. **User runs** `/goalkit.strategies`** → Explore strategies → **🛑 STOP**
4. **User runs** `/goalkit.milestones`** → Create milestones → **🛑 STOP**
5. **User runs** `/goalkit.execute`** → Implement → Continue

### Quality Thresholds
- **Vision**: Score 6.0+ on validation
- **Goals**: Score 7.0+ on validation (higher standard)
- **All Components**: Must include specific, measurable targets
- **Success Metrics**: Must be tracked and validated

### Critical Success Factors
- **Outcome-First**: Focus on user/business outcomes, not implementation
- **Measurable**: Every goal must have quantifiable success criteria
- **Multiple Strategies**: Explore 3+ approaches before implementing
- **Learning Integration**: Capture and apply lessons learned
- **Adaptive Execution**: Be ready to pivot based on evidence

---
*This context is automatically updated by the Smart Context Management system based on project state, progress, and validation results.*
"""

    def _update_context_file(self, file_path: str, content: str) -> bool:
        """Update a single context file"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            write_warning(f"Could not update context file {file_path}: {e}")
            return False


def main():
    """Main smart context management function"""
    if not test_git_repo():
        write_error("Not in a git repository")
        write_info("Please run this from the root of a Goal Kit project")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(description='Smart Context Management for Goal Kit')
    parser.add_argument('--analyze-only', action='store_true', help='Only analyze, do not update context files')
    parser.add_argument('--json', action='store_true', help='Output analysis in JSON format')

    args = parser.parse_args()

    try:
        manager = SmartContextManager()
        intelligence = manager.analyze_project_state()

        if args.json:
            print(json.dumps({
                'context_intelligence': asdict(intelligence),
                'generated_at': datetime.now().isoformat()
            }, indent=2))
        else:
            # Display analysis
            print(f"\n🧠 SMART CONTEXT ANALYSIS")
            print(f"Project: {intelligence.project_name}")
            print(f"Current Phase: {intelligence.current_phase}")
            print(f"Project Health: {intelligence.project_health}")
            print(f"Active Goals: {len(intelligence.active_goals)}")
            print(f"Current Focus: {intelligence.current_focus}")

            if intelligence.recommended_actions:
                print(f"\n💡 Recommended Actions:")
                for action in intelligence.recommended_actions:
                    print(f"  • {action}")

            if intelligence.risk_factors:
                print(f"\n⚠️ Risk Factors:")
                for risk in intelligence.risk_factors:
                    print(f"  • {risk}")

        if not args.analyze_only:
            print(f"\n🔄 Updating agent context files...")
            manager.update_agent_context_files()

    except Exception as e:
        write_error(f"Error in smart context management: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()