#!/usr/bin/env python3
"""
Goal Kit Memory System - Dynamic learning and context management

This module implements a comprehensive memory system that learns from project
experiences, preserves AI context, and provides insights across projects.
"""

import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import re

class ProjectMemory:
    """Manages learning and insights from individual projects."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.memory_path = project_path / ".goalkit" / "memory"
        self.projects_path = self.memory_path / "projects"
        self.sessions_path = self.memory_path / "sessions"
        self.insights_path = self.memory_path / "insights"

        # Ensure memory directories exist
        for path in [self.memory_path, self.projects_path, self.sessions_path, self.insights_path]:
            path.mkdir(parents=True, exist_ok=True)

    def record_goal_completion(self, goal_name: str, goal_data: dict) -> None:
        """Record learnings when a goal is completed."""
        project_id = self._get_or_create_project_id()

        learning_data = {
            "project_id": project_id,
            "goal_name": goal_name,
            "completion_date": datetime.now().isoformat(),
            "duration_days": goal_data.get("duration_days", 0),
            "success_score": goal_data.get("success_score", 0),
            "milestone_count": goal_data.get("milestone_count", 0),
            "completion_rate": goal_data.get("completion_rate", 0),
            "key_learnings": goal_data.get("learnings", []),
            "challenges": goal_data.get("challenges", []),
            "success_factors": goal_data.get("success_factors", [])
        }

        # Save to project learnings
        learnings_file = self.projects_path / project_id / "goal_learnings.jsonl"
        learnings_file.parent.mkdir(exist_ok=True)

        with open(learnings_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(learning_data) + '\n')

        # Update project summary
        self._update_project_summary(project_id, learning_data)

    def get_project_patterns(self, project_id: str = None) -> dict:
        """Analyze patterns from project learnings."""
        if project_id:
            project_ids = [project_id]
        else:
            project_ids = [d.name for d in self.projects_path.iterdir() if d.is_dir()]

        all_learnings = []

        for pid in project_ids:
            learnings_file = self.projects_path / pid / "goal_learnings.jsonl"
            if learnings_file.exists():
                with open(learnings_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            all_learnings.append(json.loads(line.strip()))
                        except json.JSONDecodeError:
                            continue

        if not all_learnings:
            return {"patterns": [], "insights": [], "recommendations": []}

        # Analyze patterns
        patterns = self._analyze_learning_patterns(all_learnings)
        return patterns

    def _get_or_create_project_id(self) -> str:
        """Get existing project ID or create new one."""
        metadata_file = self.memory_path / "project_metadata.json"

        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                return metadata.get("project_id", self._generate_project_id())

        # Create new project metadata
        project_id = self._generate_project_id()
        metadata = {
            "project_id": project_id,
            "created_date": datetime.now().isoformat(),
            "project_name": self.project_path.name,
            "memory_version": "1.0"
        }

        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

        return project_id

    def _generate_project_id(self) -> str:
        """Generate unique project identifier."""
        return f"project-{self.project_path.name}-{str(uuid.uuid4())[:8]}"

    def _update_project_summary(self, project_id: str, learning_data: dict) -> None:
        """Update project summary with latest learning."""
        summary_file = self.projects_path / project_id / "summary.json"

        # Load existing summary or create new
        if summary_file.exists():
            with open(summary_file, 'r', encoding='utf-8') as f:
                summary = json.load(f)
        else:
            summary = {
                "project_id": project_id,
                "total_goals": 0,
                "completed_goals": 0,
                "average_success_score": 0,
                "common_success_factors": [],
                "common_challenges": [],
                "key_learnings": []
            }

        # Update summary statistics
        summary["total_goals"] += 1
        if learning_data.get("success_score", 0) > 7:
            summary["completed_goals"] += 1

        # Update success factors and challenges
        for factor in learning_data.get("success_factors", []):
            if factor not in summary["common_success_factors"]:
                summary["common_success_factors"].append(factor)

        for challenge in learning_data.get("challenges", []):
            if challenge not in summary["common_challenges"]:
                summary["common_challenges"].append(challenge)

        # Add new learnings
        for learning in learning_data.get("key_learnings", []):
            if learning not in summary["key_learnings"]:
                summary["key_learnings"].append(learning)

        # Save updated summary
        summary_file.parent.mkdir(exist_ok=True)
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)

    def _analyze_learning_patterns(self, learnings: List[dict]) -> dict:
        """Analyze learning data for patterns and insights."""
        if not learnings:
            return {"patterns": [], "insights": [], "recommendations": []}

        # Calculate statistics
        total_goals = len(learnings)
        successful_goals = len([l for l in learnings if l.get("success_score", 0) > 7])
        avg_success_score = sum(l.get("success_score", 0) for l in learnings) / total_goals

        # Find common success factors
        success_factors = {}
        for learning in learnings:
            for factor in learning.get("success_factors", []):
                success_factors[factor] = success_factors.get(factor, 0) + 1

        # Find common challenges
        challenges = {}
        for learning in learnings:
            for challenge in learning.get("challenges", []):
                challenges[challenge] = challenges.get(challenge, 0) + 1

        # Generate insights
        insights = []
        if avg_success_score > 8:
            insights.append("High success rate - current approaches are working well")
        elif avg_success_score < 5:
            insights.append("Low success rate - consider strategy review and process improvements")

        # Top success factors
        top_factors = sorted(success_factors.items(), key=lambda x: x[1], reverse=True)[:3]
        if top_factors:
            insights.append(f"Most effective success factors: {[f[0] for f in top_factors]}")

        # Generate recommendations
        recommendations = []
        if challenges:
            top_challenges = sorted(challenges.items(), key=lambda x: x[1], reverse=True)[:2]
            recommendations.append(f"Focus on mitigating: {[c[0] for c in top_challenges]}")

        if avg_success_score < 6:
            recommendations.append("Consider /goalkit.validate to review goal quality")
            recommendations.append("Use /goalkit.analyze to identify improvement opportunities")

        return {
            "patterns": {
                "total_goals": total_goals,
                "success_rate": successful_goals / total_goals,
                "average_success_score": avg_success_score,
                "common_success_factors": top_factors,
                "common_challenges": sorted(challenges.items(), key=lambda x: x[1], reverse=True)[:3]
            },
            "insights": insights,
            "recommendations": recommendations
        }


class AISessionMemory:
    """Manages AI conversation context and learning."""

    def __init__(self, project_path: Path):
        self.memory = ProjectMemory(project_path)
        self.current_session_id = None

    def start_session(self, agent_name: str) -> str:
        """Start new AI session with context."""
        self.current_session_id = f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{str(uuid.uuid4())[:8]}"

        session_data = {
            "session_id": self.current_session_id,
            "agent_name": agent_name,
            "start_time": datetime.now().isoformat(),
            "project_context": self._get_current_project_context(),
            "conversation_history": [],
            "decisions_made": [],
            "insights_gained": []
        }

        # Save session data
        session_file = self.memory.sessions_path / self.current_session_id / "session.json"
        session_file.parent.mkdir(exist_ok=True)

        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2)

        return self.current_session_id

    def add_interaction(self, command: str, user_input: str, ai_response: str, success_score: float = None) -> None:
        """Record AI interaction for context and learning."""
        if not self.current_session_id:
            return

        interaction = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "user_input": user_input,
            "ai_response_summary": self._summarize_response(ai_response),
            "success_score": success_score,
            "context_relevant": self._assess_context_relevance(command, user_input)
        }

        # Add to conversation history
        session_file = self.memory.sessions_path / self.current_session_id / "interactions.jsonl"
        with open(session_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(interaction) + '\n')

        # Update session summary
        self._update_session_summary(interaction)

    def get_relevant_context(self, current_command: str) -> dict:
        """Get relevant context from past interactions."""
        if not self.current_session_id:
            return {"recent_interactions": [], "preferences": {}, "insights": []}

        # Get recent interactions from current session
        interactions_file = self.memory.sessions_path / self.current_session_id / "interactions.jsonl"
        recent_interactions = []

        if interactions_file.exists():
            with open(interactions_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        interaction = json.loads(line.strip())
                        recent_interactions.append(interaction)
                    except json.JSONDecodeError:
                        continue

        # Get last 5 interactions
        recent_interactions = recent_interactions[-5:]

        # Extract preferences and patterns
        preferences = self._extract_preferences(recent_interactions)
        insights = self._extract_insights(recent_interactions)

        return {
            "recent_interactions": recent_interactions,
            "preferences": preferences,
            "insights": insights,
            "session_context": self._get_current_project_context()
        }

    def _get_current_project_context(self) -> dict:
        """Get current project state for context."""
        context = {
            "project_name": self.memory.project_path.name,
            "active_goals": [],
            "recent_activity": [],
            "current_phase": "unknown"
        }

        # Try to determine current phase from recent files
        goalkit_dir = self.memory.project_path / ".goalkit"
        if goalkit_dir.exists():
            goals_dir = goalkit_dir / "goals"
            if goals_dir.exists():
                context["active_goals"] = [d.name for d in goals_dir.iterdir() if d.is_dir()]

        return context

    def _summarize_response(self, response: str, max_length: int = 100) -> str:
        """Create summary of AI response for memory."""
        # Remove markdown formatting for summary
        summary = re.sub(r'\*\*(.*?)\*\*', r'\1', response)  # Remove bold
        summary = re.sub(r'^(#{1,6}\s)', '', summary, flags=re.MULTILINE)  # Remove headers
        summary = summary.replace('\n', ' ').strip()

        if len(summary) > max_length:
            summary = summary[:max_length] + "..."

        return summary

    def _assess_context_relevance(self, command: str, user_input: str) -> bool:
        """Assess if interaction is relevant to current project context."""
        # Simple relevance check - can be enhanced
        context_keywords = ["goal", "project", "milestone", "strategy", "plan"]
        combined_text = f"{command} {user_input}".lower()

        return any(keyword in combined_text for keyword in context_keywords)

    def _update_session_summary(self, interaction: dict) -> None:
        """Update session summary with latest interaction."""
        if not self.current_session_id:
            return

        session_file = self.memory.sessions_path / self.current_session_id / "session.json"

        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)

            # Update conversation history
            if "conversation_history" not in session_data:
                session_data["conversation_history"] = []

            session_data["conversation_history"].append({
                "command": interaction["command"],
                "timestamp": interaction["timestamp"],
                "success_score": interaction["success_score"]
            })

            # Keep only last 10 interactions in summary
            session_data["conversation_history"] = session_data["conversation_history"][-10:]

            # Update session metadata
            session_data["last_activity"] = interaction["timestamp"]
            session_data["interaction_count"] = len(session_data["conversation_history"])

            # Save updated session
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2)

    def _extract_preferences(self, interactions: List[dict]) -> dict:
        """Extract user and agent preferences from interactions."""
        preferences = {
            "preferred_commands": [],
            "communication_style": "balanced",
            "detail_level": "standard",
            "focus_areas": []
        }

        if not interactions:
            return preferences

        # Analyze command usage patterns
        commands = [i.get("command", "") for i in interactions]
        command_counts = {}
        for cmd in commands:
            command_counts[cmd] = command_counts.get(cmd, 0) + 1

        if command_counts:
            preferences["preferred_commands"] = sorted(command_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        return preferences

    def _extract_insights(self, interactions: List[dict]) -> List[str]:
        """Extract key insights from recent interactions."""
        insights = []

        for interaction in interactions:
            if interaction.get("success_score", 0) > 8:
                insights.append(f"High-quality interaction: {interaction.get('command', 'unknown')}")
            elif interaction.get("success_score", 0) < 5:
                insights.append(f"Struggled with: {interaction.get('command', 'unknown')}")

        return insights[:5]  # Return top 5 insights


class CrossProjectInsights:
    """Provides insights across multiple projects and experiences."""

    def __init__(self, memory: ProjectMemory):
        self.memory = memory

    def find_similar_projects(self, current_goal: str, min_similarity: float = 0.3) -> List[dict]:
        """Find projects with similar goals or characteristics."""
        similar_projects = []

        # Get all project summaries
        for project_dir in self.memory.projects_path.iterdir():
            if project_dir.is_dir():
                summary_file = project_dir / "summary.json"
                if summary_file.exists():
                    with open(summary_file, 'r', encoding='utf-8') as f:
                        try:
                            project_data = json.load(f)
                            similarity = self._calculate_similarity(current_goal, project_data)

                            if similarity >= min_similarity:
                                similar_projects.append({
                                    "project_id": project_data.get("project_id"),
                                    "similarity_score": similarity,
                                    "success_rate": project_data.get("completed_goals", 0) / max(project_data.get("total_goals", 1), 1),
                                    "key_learnings": project_data.get("key_learnings", [])[:3]
                                })
                        except json.JSONDecodeError:
                            continue

        # Sort by similarity score
        similar_projects.sort(key=lambda x: x["similarity_score"], reverse=True)
        return similar_projects[:5]  # Return top 5 similar projects

    def get_best_practices(self) -> dict:
        """Extract best practices from successful projects."""
        best_practices = {
            "success_factors": [],
            "process_improvements": [],
            "common_patterns": [],
            "recommended_approaches": []
        }

        # Aggregate learnings from all projects
        all_success_factors = {}
        all_learnings = {}

        for project_dir in self.memory.projects_path.iterdir():
            if project_dir.is_dir():
                # Get project summary
                summary_file = project_dir / "summary.json"
                if summary_file.exists():
                    with open(summary_file, 'r', encoding='utf-8') as f:
                        try:
                            project_data = json.load(f)

                            # Collect success factors
                            for factor in project_data.get("common_success_factors", []):
                                all_success_factors[factor] = all_success_factors.get(factor, 0) + 1

                            # Collect learnings
                            for learning in project_data.get("key_learnings", []):
                                all_learnings[learning] = all_learnings.get(learning, 0) + 1

                        except json.JSONDecodeError:
                            continue

        # Extract top patterns
        best_practices["success_factors"] = sorted(
            all_success_factors.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        best_practices["common_patterns"] = sorted(
            all_learnings.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return best_practices

    def detect_risk_patterns(self) -> List[str]:
        """Detect common risk patterns from project failures."""
        risk_patterns = []

        for project_dir in self.memory.projects_path.iterdir():
            if project_dir.is_dir():
                learnings_file = project_dir / "goal_learnings.jsonl"
                if learnings_file.exists():
                    with open(learnings_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            try:
                                learning = json.loads(line.strip())
                                if learning.get("success_score", 10) < 6:  # Low success
                                    for challenge in learning.get("challenges", []):
                                        if challenge not in risk_patterns:
                                            risk_patterns.append(challenge)
                            except json.JSONDecodeError:
                                continue

        return risk_patterns[:10]  # Return top 10 risk patterns

    def _calculate_similarity(self, current_goal: str, project_data: dict) -> float:
        """Calculate similarity between current goal and historical project."""
        similarity = 0.0

        # Simple keyword-based similarity
        goal_keywords = set(current_goal.lower().split())
        project_learnings = " ".join(project_data.get("key_learnings", [])).lower()

        matching_keywords = goal_keywords.intersection(set(project_learnings.split()))
        similarity = len(matching_keywords) / len(goal_keywords) if goal_keywords else 0.0

        return min(similarity, 1.0)


def extract_goal_learnings(goal_path: Path) -> dict:
    """Extract learnings from a completed goal for memory system."""
    learnings = {
        "success_factors": [],
        "challenges": [],
        "key_learnings": [],
        "duration_days": 0,
        "success_score": 5,  # Default moderate score
        "milestone_count": 0,
        "completion_rate": 0
    }

    goal_file = goal_path / "goal.md"
    if not goal_file.exists():
        return learnings

    try:
        content = goal_file.read_text(encoding='utf-8')

        # Extract basic metrics (simplified extraction)
        learnings["milestone_count"] = len(re.findall(r'### Milestone \d+', content))

        # Look for completion indicators
        if "[x]" in content or "completed" in content.lower():
            learnings["success_score"] = 8
            learnings["completion_rate"] = 0.9
        elif "cancelled" in content.lower() or "failed" in content.lower():
            learnings["success_score"] = 2
            learnings["completion_rate"] = 0.1

        # Extract key sections for learning
        sections = re.split(r'\n## ', content)
        for section in sections:
            if "success" in section.lower() and "factor" in section.lower():
                learnings["success_factors"].append(section.strip()[:100])
            elif "challenge" in section.lower() or "risk" in section.lower():
                learnings["challenges"].append(section.strip()[:100])
            elif "learning" in section.lower() or "lesson" in section.lower():
                learnings["key_learnings"].append(section.strip()[:100])

    except Exception as e:
        # If extraction fails, return default structure
        pass

    return learnings


# Convenience functions for CLI integration
def get_project_memory(project_path: Path) -> ProjectMemory:
    """Get or create project memory for given path."""
    return ProjectMemory(project_path)

def get_ai_session_memory(project_path: Path) -> AISessionMemory:
    """Get or create AI session memory for given path."""
    return AISessionMemory(project_path)

def get_cross_project_insights(project_path: Path) -> CrossProjectInsights:
    """Get cross-project insights for given path."""
    memory = ProjectMemory(project_path)
    return CrossProjectInsights(memory)