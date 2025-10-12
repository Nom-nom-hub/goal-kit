#!/usr/bin/env python3
"""
Integration module for Context-Aware Command Suggestion System

This module integrates the suggestion system with the existing Goalkeeper CLI
and memory system for seamless operation.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta

try:
    from .command_suggestion import (
        ContextAwareCommandRecommender,
        SuggestionContext,
        CommandSuggestion,
        SuggestionCategory,
        UserIntentSignal
    )
    from .memory import ProjectMemory, AISessionMemory
    from .enhanced_context import ContextRetentionEngine
except ImportError:
    # Fallback for when running tests or modules are not available
    ContextAwareCommandRecommender = None
    SuggestionContext = None
    CommandSuggestion = None
    SuggestionCategory = None
    UserIntentSignal = None
    ProjectMemory = None
    AISessionMemory = None
    ContextRetentionEngine = None

import logging
logger = logging.getLogger(__name__)


class SuggestionIntegrationManager:
    """Manages integration between suggestion system and existing Goalkeeper components."""

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.goalkit_dir = self.project_path / ".goalkit"

        # Initialize components
        self.memory_system = None
        self.session_memory = None
        self.context_engine = None
        self.recommender = None

        # Available commands from the main CLI
        self.available_commands = self._get_available_commands()

        # Integration state
        self.integration_enabled = True
        self.last_context_update = None

        # Initialize integration
        self._initialize_integration()

    def _get_available_commands(self) -> List[str]:
        """Get list of available Goalkeeper commands."""
        return [
            'init', 'goal', 'vision', 'strategies', 'milestones', 'tasks',
            'progress', 'analytics', 'validate', 'analyze', 'insights',
            'learn', 'memory', 'research', 'automate', 'baseline', 'check',
            'validate_goals', 'plan_project', 'insights_project', 'prioritize_goals',
            'track_progress', 'research_project', 'learn_from_project',
            'benchmark_project', 'memory_status', 'learn_extract',
            'memory_insights', 'memory_patterns', 'ai_analytics',
            'ai_generate', 'suggest'  # Add suggest command for the suggestion system
        ]

    def _initialize_integration(self) -> None:
        """Initialize integration with existing systems."""
        try:
            # Initialize memory system
            if ProjectMemory:
                self.memory_system = ProjectMemory(self.project_path)
            else:
                logger.warning("ProjectMemory not available - running without memory system")

            # Initialize session memory
            if AISessionMemory:
                self.session_memory = AISessionMemory(self.project_path)
            else:
                logger.warning("AISessionMemory not available - running without session memory")

            # Initialize context engine
            if ContextRetentionEngine:
                self.context_engine = ContextRetentionEngine(self.project_path)
            else:
                logger.warning("ContextRetentionEngine not available - running without context engine")

            # Initialize recommender
            if ContextAwareCommandRecommender:
                self.recommender = ContextAwareCommandRecommender(
                    self.project_path, self.available_commands
                )
            else:
                logger.warning("ContextAwareCommandRecommender not available - running without recommender")

            logger.info("Suggestion system integration initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize suggestion integration: {e}")
            self.integration_enabled = False

    def create_suggestion_context(self, current_command: str = None,
                                 session_commands: List[str] = None) -> SuggestionContext:
        """Create suggestion context from current session and project state."""
        if SuggestionContext is None:
            # Return a mock context for testing
            class MockContext:
                def __init__(self, project_path):
                    self.project_path = project_path
                    self.project_phase = "unknown"
                    self.current_goal = None
                    self.active_goals = []
                    self.time_of_day = "unknown"
                    self.recent_commands = []
                    self.session_commands = []
                    self.available_commands = set()
                    self.intent_signals = []
                    self.user_preferences = {}
                    self.session_duration_minutes = 0
                    self.system_capabilities = {}
                    self.usage_patterns = {}

            # Create mock context instance
            mock_context = MockContext(self.project_path)
            
            # Set recent commands if provided
            if current_command:
                mock_context.recent_commands = [current_command]
            
            if session_commands:
                mock_context.session_commands = session_commands

            return mock_context

        context = SuggestionContext(project_path=self.project_path)

        try:
            # Get project phase from memory system
            context.project_phase = self._detect_project_phase()

            # Get current goal from recent context
            context.current_goal = self._get_current_goal()

            # Get active goals
            context.active_goals = self._get_active_goals()

            # Set temporal context
            context.time_of_day = self._get_time_of_day()
            context.day_of_week = datetime.now().strftime('%A')

            # Set command history
            if session_commands:
                context.session_commands = session_commands.copy()
            if current_command:
                context.recent_commands = [current_command]

            # Set recent and session commands if provided
            if current_command:
                context.recent_commands = [current_command]
            if session_commands:
                context.session_commands = session_commands

            # Set available commands
            context.available_commands = set(self.available_commands)

            # Set system capabilities
            context.system_capabilities = self._get_system_capabilities()

            # Load user preferences from memory
            context.user_preferences = self._load_user_preferences()

            # Add intent signals from recent activity
            self._add_recent_intent_signals(context)

            # Update last context refresh time
            self.last_context_update = datetime.now()

        except Exception as e:
            logger.warning(f"Error creating suggestion context: {e}")
            # Use default context on error

        return context

    def _detect_project_phase(self) -> str:
        """Detect current project phase from project structure and memory."""
        try:
            # Check for goal files to determine phase
            goals_dir = self.goalkit_dir / "goals"
            if not goals_dir.exists():
                return "setup"

            goal_dirs = [d for d in goals_dir.iterdir() if d.is_dir()]
            if not goal_dirs:
                return "planning"

            # Check for milestones and tasks to determine execution phase
            has_milestones = False
            has_tasks = False

            for goal_dir in goal_dirs:
                milestones_file = goal_dir / "milestones.md"
                tasks_file = goal_dir / "tasks.md"

                if milestones_file.exists():
                    has_milestones = True
                if tasks_file.exists():
                    has_tasks = True

            if has_tasks:
                return "execution"
            elif has_milestones:
                return "planning"
            else:
                return "planning"

        except Exception as e:
            logger.warning(f"Error detecting project phase: {e}")
            return "unknown"

    def _get_current_goal(self) -> Optional[str]:
        """Get currently active goal."""
        try:
            if not self.memory_system:
                return None

            # Get recent goal context from memory
            recent_contexts = self.memory_system.get_recent_contexts(limit=5)
            for context_obj in recent_contexts:
                if hasattr(context_obj, 'metadata') and context_obj.metadata.categories:
                    if 'goal' in context_obj.metadata.categories:
                        return context_obj.metadata.categories[0]  # Return first goal category

        except Exception as e:
            logger.warning(f"Error getting current goal: {e}")

        return None

    def _get_active_goals(self) -> List[str]:
        """Get list of active goals."""
        active_goals = []

        try:
            goals_dir = self.goalkit_dir / "goals"
            if goals_dir.exists():
                for goal_dir in goals_dir.iterdir():
                    if goal_dir.is_dir():
                        goal_file = goal_dir / "goal.md"
                        if goal_file.exists():
                            # Check if goal is active (not completed)
                            content = goal_file.read_text(encoding='utf-8')
                            if 'completed' not in content.lower():
                                active_goals.append(goal_dir.name)

        except Exception as e:
            logger.warning(f"Error getting active goals: {e}")

        return active_goals

    def _get_time_of_day(self) -> str:
        """Get current time of day."""
        hour = datetime.now().hour

        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        else:
            return "night"

    def _get_system_capabilities(self) -> Dict[str, bool]:
        """Get system capabilities."""
        capabilities = {}

        # Check for AI assistants
        ai_assistants = ['claude', 'gemini', 'cursor', 'qwen', 'windsurf', 'kilocode']
        for assistant in ai_assistants:
            capabilities[f'ai_{assistant}'] = self._check_command_availability(assistant)

        # Check for development tools
        dev_tools = ['git', 'node', 'python', 'docker']
        for tool in dev_tools:
            capabilities[f'tool_{tool}'] = self._check_command_availability(tool)

        return capabilities

    def _check_command_availability(self, command: str) -> bool:
        """Check if a command is available in the system."""
        import shutil
        return shutil.which(command) is not None

    def _load_user_preferences(self) -> Dict[str, Any]:
        """Load user preferences from memory system."""
        preferences = {}

        try:
            if self.memory_system:
                # Get user preferences from memory
                patterns = self.memory_system.get_project_patterns()
                if patterns.get('preferences'):
                    preferences = patterns['preferences']

        except Exception as e:
            logger.warning(f"Error loading user preferences: {e}")

        return preferences

    def _add_recent_intent_signals(self, context: SuggestionContext) -> None:
        """Add recent intent signals from memory and session."""
        try:
            # Get recent commands from session memory
            if self.session_memory:
                recent_interactions = self.session_memory.get_recent_interactions(limit=10)

                for interaction in recent_interactions:
                    signal = UserIntentSignal(
                        signal_type="recent_interaction",
                        signal_value=interaction.get('command', ''),
                        confidence=0.6,
                        timestamp=datetime.now() - timedelta(minutes=30),  # Approximate timestamp
                        context={'interaction': interaction}
                    )
                    context.add_intent_signal(signal)

        except Exception as e:
            logger.warning(f"Error adding recent intent signals: {e}")

    def get_command_suggestions(self, user_input: str, current_command: str = None,
                              session_commands: List[str] = None) -> List[CommandSuggestion]:
        """Get command suggestions with full context integration."""
        if not self.integration_enabled or not self.recommender:
            return []

        try:
            # Create comprehensive context
            context = self.create_suggestion_context(current_command, session_commands)

            # Get suggestions from recommender
            suggestions = self.recommender.get_command_suggestions(user_input, context)

            # Enhance suggestions with memory system insights
            enhanced_suggestions = self._enhance_suggestions_with_memory(suggestions, context)

            return enhanced_suggestions

        except Exception as e:
            logger.error(f"Error getting command suggestions: {e}")
            return []

    def _enhance_suggestions_with_memory(self, suggestions: List[CommandSuggestion],
                                       context: SuggestionContext) -> List[CommandSuggestion]:
        """Enhance suggestions using memory system insights."""
        if not self.memory_system or not suggestions:
            return suggestions

        try:
            # Get relevant memories for each suggestion
            for suggestion in suggestions:
                # Find similar contexts in memory
                similar_contexts = self.memory_system.find_similar_contexts(
                    suggestion.command, limit=3
                )

                if similar_contexts:
                    # Add memory-based reasoning
                    memory_insights = []
                    for similar_ctx in similar_contexts:
                        if hasattr(similar_ctx, 'metadata'):
                            metadata = similar_ctx.metadata
                            if metadata.relevance_score > 0.7:
                                memory_insights.append(
                                    f"Similar to previous {metadata.categories} work"
                                )

                    if memory_insights:
                        suggestion.add_reasoning(memory_insights[0])
                        suggestion.add_context_factor('memory_relevance', 0.8)

        except Exception as e:
            logger.warning(f"Error enhancing suggestions with memory: {e}")

        return suggestions

    def record_command_usage(self, command: str, success: bool, context: SuggestionContext) -> None:
        """Record command usage for learning."""
        if not self.recommender:
            return

        try:
            # Update context with usage pattern
            context.update_command_pattern(command, success, 0.7, context.project_phase)

            # Store in memory system
            if self.memory_system:
                # Create context object for the command usage
                from .enhanced_context import ContextObject, ContextMetadata, ContextPriority

                metadata = ContextMetadata(
                    session_id=getattr(context, 'session_id', 'unknown'),
                    agent_name='suggestion_system',
                    project_path=str(self.project_path),
                    content_type='command_usage',
                    priority=ContextPriority.MEDIUM,
                    categories=['command_usage', command]
                )

                usage_context = ContextObject(
                    content={
                        'command': command,
                        'success': success,
                        'project_phase': context.project_phase,
                        'timestamp': datetime.now().isoformat()
                    },
                    metadata=metadata
                )

                self.memory_system.store_context(usage_context)

        except Exception as e:
            logger.warning(f"Error recording command usage: {e}")

    def learn_from_suggestion_feedback(self, suggestion: CommandSuggestion,
                                     was_helpful: bool, context: SuggestionContext) -> None:
        """Learn from user feedback on suggestions."""
        if not self.recommender:
            return

        try:
            # Learn from the interaction
            self.recommender.learn_from_user_interaction(
                suggestion.command, suggestion, was_helpful, context
            )

            # Record in memory system for long-term learning
            if self.memory_system:
                from .enhanced_context import ContextObject, ContextMetadata, ContextPriority

                metadata = ContextMetadata(
                    session_id=getattr(context, 'session_id', 'unknown'),
                    agent_name='suggestion_system',
                    project_path=str(self.project_path),
                    content_type='suggestion_feedback',
                    priority=ContextPriority.HIGH,
                    categories=['suggestion_feedback', suggestion.category.value]
                )

                feedback_context = ContextObject(
                    content={
                        'suggestion_command': suggestion.command,
                        'was_helpful': was_helpful,
                        'confidence_score': suggestion.confidence_score,
                        'project_phase': context.project_phase,
                        'timestamp': datetime.now().isoformat()
                    },
                    metadata=metadata
                )

                self.memory_system.store_context(feedback_context)

        except Exception as e:
            logger.warning(f"Error learning from suggestion feedback: {e}")

    def get_suggestion_analytics(self) -> Dict[str, Any]:
        """Get analytics about suggestion system performance."""
        if not self.recommender:
            return {
                'integration_status': {
                    'enabled': self.integration_enabled,
                    'memory_system': self.memory_system is not None,
                    'session_memory': self.session_memory is not None,
                    'context_engine': self.context_engine is not None,
                    'recommender': False,
                    'last_context_update': self.last_context_update.isoformat() if self.last_context_update else None
                },
                'project_context': {
                    'phase': self._detect_project_phase(),
                    'active_goals': len(self._get_active_goals()),
                    'available_commands': len(self.available_commands)
                },
                'error': 'Recommender not initialized'
            }

        try:
            analytics = {
                'recommender_insights': self.recommender.get_recommendation_insights(),
                'integration_status': {
                    'enabled': self.integration_enabled,
                    'memory_system': self.memory_system is not None,
                    'session_memory': self.session_memory is not None,
                    'context_engine': self.context_engine is not None,
                    'last_context_update': self.last_context_update.isoformat() if self.last_context_update else None
                },
                'project_context': {
                    'phase': self._detect_project_phase(),
                    'active_goals': len(self._get_active_goals()),
                    'available_commands': len(self.available_commands)
                }
            }

            return analytics

        except Exception as e:
            logger.error(f"Error getting suggestion analytics: {e}")
            return {'error': str(e)}

    def refresh_context(self) -> None:
        """Refresh integration context from current project state."""
        try:
            # Update available commands
            self.available_commands = self._get_available_commands()

            # Update project phase detection
            current_phase = self._detect_project_phase()

            # Refresh memory system connection
            if self.memory_system:
                # Update memory system with current project state
                pass

            self.last_context_update = datetime.now()
            logger.info("Integration context refreshed")

        except Exception as e:
            logger.error(f"Error refreshing context: {e}")

    def export_integration_data(self) -> Dict[str, Any]:
        """Export integration data for debugging and analysis."""
        return {
            'integration_config': {
                'project_path': str(self.project_path),
                'goalkit_dir': str(self.goalkit_dir),
                'integration_enabled': self.integration_enabled,
                'available_commands_count': len(self.available_commands)
            },
            'component_status': {
                'memory_system': self.memory_system is not None,
                'session_memory': self.session_memory is not None,
                'context_engine': self.context_engine is not None,
                'recommender': self.recommender is not None
            },
            'recommender_data': self.recommender.export_recommendation_data() if self.recommender else {},
            'exported_at': datetime.now().isoformat()
        }

    def cleanup(self) -> None:
        """Clean up integration resources."""
        try:
            # Clean up context engine
            if self.context_engine:
                self.context_engine.cleanup()

            logger.info("Suggestion integration cleanup completed")

        except Exception as e:
            logger.error(f"Error during integration cleanup: {e}")


# Global integration manager instance
_integration_manager: Optional[SuggestionIntegrationManager] = None


def get_integration_manager(project_path: Path) -> SuggestionIntegrationManager:
    """Get or create global integration manager."""
    global _integration_manager

    if _integration_manager is None:
        _integration_manager = SuggestionIntegrationManager(project_path)

    return _integration_manager


def reset_integration_manager() -> None:
    """Reset global integration manager."""
    global _integration_manager

    if _integration_manager:
        _integration_manager.cleanup()
        _integration_manager = None


class SuggestionLearningEngine:
    """Advanced learning engine for continuous improvement of suggestions."""

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.learning_data_file = self.project_path / ".goalkit" / "suggestion_learning.json"

        # Learning data structures
        self.feedback_patterns: Dict[str, Dict[str, Any]] = {}
        self.success_patterns: Dict[str, Dict[str, Any]] = {}
        self.context_effectiveness: Dict[str, Dict[str, float]] = {}
        self.temporal_patterns: Dict[str, Dict[str, Any]] = {}

        # Learning configuration
        self.learning_rate = 0.1
        self.min_samples_for_learning = 5
        self.pattern_decay_factor = 0.95

        # Load existing learning data
        self._load_learning_data()

    def _load_learning_data(self) -> None:
        """Load existing learning data."""
        if self.learning_data_file.exists():
            try:
                with open(self.learning_data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                self.feedback_patterns = data.get('feedback_patterns', {})
                self.success_patterns = data.get('success_patterns', {})
                self.context_effectiveness = data.get('context_effectiveness', {})
                self.temporal_patterns = data.get('temporal_patterns', {})

                logger.info(f"Loaded suggestion learning data from {self.learning_data_file}")

            except Exception as e:
                logger.warning(f"Failed to load learning data: {e}")

    def _save_learning_data(self) -> None:
        """Save learning data."""
        try:
            self.learning_data_file.parent.mkdir(parents=True, exist_ok=True)

            data = {
                'feedback_patterns': self.feedback_patterns,
                'success_patterns': self.success_patterns,
                'context_effectiveness': self.context_effectiveness,
                'temporal_patterns': self.temporal_patterns,
                'last_updated': datetime.now().isoformat()
            }

            with open(self.learning_data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Failed to save learning data: {e}")

    def record_suggestion_interaction(self, suggestion: CommandSuggestion,
                                    was_helpful: bool, context: SuggestionContext,
                                    response_time_ms: float) -> None:
        """Record interaction with suggestion for learning."""
        try:
            # Record feedback pattern
            self._record_feedback_pattern(suggestion, was_helpful, context)

            # Record success pattern
            self._record_success_pattern(suggestion, was_helpful, context)

            # Record context effectiveness
            self._record_context_effectiveness(suggestion, was_helpful, context)

            # Record temporal pattern
            self._record_temporal_pattern(suggestion, was_helpful, context)

            # Apply learning decay to old patterns
            self._apply_learning_decay()

            # Save learning data
            self._save_learning_data()

        except Exception as e:
            logger.error(f"Error recording suggestion interaction: {e}")

    def _record_feedback_pattern(self, suggestion: CommandSuggestion,
                               was_helpful: bool, context: SuggestionContext) -> None:
        """Record feedback pattern for learning."""
        pattern_key = f"{suggestion.command}_{suggestion.category.value}"

        if pattern_key not in self.feedback_patterns:
            self.feedback_patterns[pattern_key] = {
                'total_interactions': 0,
                'helpful_interactions': 0,
                'confidence_sum': 0.0,
                'contexts': {},
                'recent_feedback': []
            }

        pattern = self.feedback_patterns[pattern_key]
        pattern['total_interactions'] += 1

        if was_helpful:
            pattern['helpful_interactions'] += 1

        pattern['confidence_sum'] += suggestion.confidence_score

        # Record context-specific feedback
        context_key = f"{context.project_phase}_{context.time_of_day}"
        if context_key not in pattern['contexts']:
            pattern['contexts'][context_key] = {'helpful': 0, 'total': 0}

        pattern['contexts'][context_key]['total'] += 1
        if was_helpful:
            pattern['contexts'][context_key]['helpful'] += 1

        # Keep recent feedback for trend analysis
        feedback_entry = {
            'helpful': was_helpful,
            'confidence': suggestion.confidence_score,
            'timestamp': datetime.now().isoformat(),
            'context': context_key
        }
        pattern['recent_feedback'].append(feedback_entry)

        # Keep only recent feedback (last 50)
        if len(pattern['recent_feedback']) > 50:
            pattern['recent_feedback'] = pattern['recent_feedback'][-50:]

    def _record_success_pattern(self, suggestion: CommandSuggestion,
                              was_helpful: bool, context: SuggestionContext) -> None:
        """Record success pattern for learning."""
        pattern_key = f"{suggestion.category.value}_{context.project_phase}"

        if pattern_key not in self.success_patterns:
            self.success_patterns[pattern_key] = {
                'commands': {},
                'total_suggestions': 0,
                'successful_suggestions': 0
            }

        pattern = self.success_patterns[pattern_key]

        if suggestion.command not in pattern['commands']:
            pattern['commands'][suggestion.command] = {
                'suggestions': 0,
                'successes': 0,
                'avg_confidence': 0.0
            }

        command_pattern = pattern['commands'][suggestion.command]
        command_pattern['suggestions'] += 1

        if was_helpful:
            command_pattern['successes'] += 1

        # Update average confidence
        alpha = self.learning_rate
        command_pattern['avg_confidence'] = (
            (1 - alpha) * command_pattern['avg_confidence'] + alpha * suggestion.confidence_score
        )

        pattern['total_suggestions'] += 1
        if was_helpful:
            pattern['successful_suggestions'] += 1

    def _record_context_effectiveness(self, suggestion: CommandSuggestion,
                                    was_helpful: bool, context: SuggestionContext) -> None:
        """Record context effectiveness for learning."""
        context_key = f"{context.project_phase}_{context.time_of_day}"

        if context_key not in self.context_effectiveness:
            self.context_effectiveness[context_key] = {
                'categories': {},
                'total_suggestions': 0,
                'successful_suggestions': 0
            }

        context_data = self.context_effectiveness[context_key]
        category = suggestion.category.value

        if category not in context_data['categories']:
            context_data['categories'][category] = {
                'suggestions': 0,
                'successes': 0,
                'avg_confidence': 0.0
            }

        category_data = context_data['categories'][category]
        category_data['suggestions'] += 1

        if was_helpful:
            category_data['successes'] += 1

        # Update average confidence
        alpha = self.learning_rate
        category_data['avg_confidence'] = (
            (1 - alpha) * category_data['avg_confidence'] + alpha * suggestion.confidence_score
        )

        context_data['total_suggestions'] += 1
        if was_helpful:
            context_data['successful_suggestions'] += 1

    def _record_temporal_pattern(self, suggestion: CommandSuggestion,
                               was_helpful: bool, context: SuggestionContext) -> None:
        """Record temporal pattern for learning."""
        time_key = context.time_of_day

        if time_key not in self.temporal_patterns:
            self.temporal_patterns[time_key] = {
                'categories': {},
                'total_suggestions': 0,
                'successful_suggestions': 0
            }

        time_data = self.temporal_patterns[time_key]
        category = suggestion.category.value

        if category not in time_data['categories']:
            time_data['categories'][category] = {
                'suggestions': 0,
                'successes': 0,
                'avg_confidence': 0.0
            }

        category_data = time_data['categories'][category]
        category_data['suggestions'] += 1

        if was_helpful:
            category_data['successes'] += 1

        # Update average confidence
        alpha = self.learning_rate
        category_data['avg_confidence'] = (
            (1 - alpha) * category_data['avg_confidence'] + alpha * suggestion.confidence_score
        )

        time_data['total_suggestions'] += 1
        if was_helpful:
            time_data['successful_suggestions'] += 1

    def _apply_learning_decay(self) -> None:
        """Apply decay to old learning patterns."""
        # Decay feedback patterns
        for pattern_key, pattern in self.feedback_patterns.items():
            # Decay interaction counts slightly
            pattern['total_interactions'] = int(pattern['total_interactions'] * self.pattern_decay_factor)
            pattern['helpful_interactions'] = int(pattern['helpful_interactions'] * self.pattern_decay_factor)

            # Remove very old patterns
            if pattern['total_interactions'] < self.min_samples_for_learning:
                del self.feedback_patterns[pattern_key]

        # Apply similar decay to other pattern types
        for pattern_dict in [self.success_patterns, self.context_effectiveness, self.temporal_patterns]:
            keys_to_remove = []
            for key, pattern in pattern_dict.items():
                pattern['total_suggestions'] = int(pattern['total_suggestions'] * self.pattern_decay_factor)
                pattern['successful_suggestions'] = int(pattern['successful_suggestions'] * self.pattern_decay_factor)

                if pattern['total_suggestions'] < self.min_samples_for_learning:
                    keys_to_remove.append(key)

            for key in keys_to_remove:
                del pattern_dict[key]

    def get_learned_insights(self) -> Dict[str, Any]:
        """Get insights from learning data."""
        insights = {
            'feedback_insights': self._get_feedback_insights(),
            'success_insights': self._get_success_insights(),
            'context_insights': self._get_context_insights(),
            'temporal_insights': self._get_temporal_insights(),
            'learning_summary': self._get_learning_summary()
        }

        return insights

    def _get_feedback_insights(self) -> Dict[str, Any]:
        """Get insights from feedback patterns."""
        insights = {
            'most_helpful_commands': [],
            'least_helpful_commands': [],
            'category_feedback_rates': {},
            'context_specific_feedback': {}
        }

        # Analyze command helpfulness
        command_feedback = {}
        for pattern_key, pattern in self.feedback_patterns.items():
            if pattern['total_interactions'] >= self.min_samples_for_learning:
                command = pattern_key.split('_')[0]
                success_rate = pattern['helpful_interactions'] / pattern['total_interactions']
                avg_confidence = pattern['confidence_sum'] / pattern['total_interactions']

                command_feedback[command] = {
                    'success_rate': success_rate,
                    'avg_confidence': avg_confidence,
                    'sample_size': pattern['total_interactions']
                }

        # Sort by success rate
        sorted_commands = sorted(command_feedback.items(), key=lambda x: x[1]['success_rate'], reverse=True)

        insights['most_helpful_commands'] = [
            {'command': cmd, 'success_rate': data['success_rate'], 'sample_size': data['sample_size']}
            for cmd, data in sorted_commands[:5]
        ]

        insights['least_helpful_commands'] = [
            {'command': cmd, 'success_rate': data['success_rate'], 'sample_size': data['sample_size']}
            for cmd, data in sorted_commands[-5:]
        ]

        return insights

    def _get_success_insights(self) -> Dict[str, Any]:
        """Get insights from success patterns."""
        insights = {
            'best_categories_by_phase': {},
            'command_success_by_phase': {},
            'overall_category_success': {}
        }

        # Analyze success by category and phase
        for pattern_key, pattern in self.success_patterns.items():
            if pattern['total_suggestions'] >= self.min_samples_for_learning:
                category, phase = pattern_key.split('_', 1)
                success_rate = pattern['successful_suggestions'] / pattern['total_suggestions']

                if phase not in insights['best_categories_by_phase']:
                    insights['best_categories_by_phase'][phase] = []

                insights['best_categories_by_phase'][phase].append({
                    'category': category,
                    'success_rate': success_rate,
                    'sample_size': pattern['total_suggestions']
                })

        # Sort categories by success rate for each phase
        for phase in insights['best_categories_by_phase']:
            insights['best_categories_by_phase'][phase].sort(key=lambda x: x['success_rate'], reverse=True)

        return insights

    def _get_context_insights(self) -> Dict[str, Any]:
        """Get insights from context effectiveness."""
        insights = {
            'most_effective_contexts': [],
            'category_effectiveness_by_context': {}
        }

        # Find most effective contexts
        context_effectiveness = []
        for context_key, context_data in self.context_effectiveness.items():
            if context_data['total_suggestions'] >= self.min_samples_for_learning:
                success_rate = context_data['successful_suggestions'] / context_data['total_suggestions']
                context_effectiveness.append({
                    'context': context_key,
                    'success_rate': success_rate,
                    'sample_size': context_data['total_suggestions']
                })

        # Sort by effectiveness
        context_effectiveness.sort(key=lambda x: x['success_rate'], reverse=True)
        insights['most_effective_contexts'] = context_effectiveness[:10]

        return insights

    def _get_temporal_insights(self) -> Dict[str, Any]:
        """Get insights from temporal patterns."""
        insights = {
            'best_times_for_categories': {},
            'time_based_success_rates': {}
        }

        # Analyze success by time of day
        for time_key, time_data in self.temporal_patterns.items():
            if time_data['total_suggestions'] >= self.min_samples_for_learning:
                success_rate = time_data['successful_suggestions'] / time_data['total_suggestions']

                insights['time_based_success_rates'][time_key] = {
                    'success_rate': success_rate,
                    'sample_size': time_data['total_suggestions']
                }

                # Find best categories for this time
                best_categories = []
                for category, cat_data in time_data['categories'].items():
                    if cat_data['suggestions'] >= 3:  # Minimum samples
                        cat_success_rate = cat_data['successes'] / cat_data['suggestions']
                        best_categories.append({
                            'category': category,
                            'success_rate': cat_success_rate,
                            'sample_size': cat_data['suggestions']
                        })

                if best_categories:
                    best_categories.sort(key=lambda x: x['success_rate'], reverse=True)
                    insights['best_times_for_categories'][time_key] = best_categories[:3]

        return insights

    def _get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of learning progress."""
        total_patterns = (
            len(self.feedback_patterns) +
            len(self.success_patterns) +
            len(self.context_effectiveness) +
            len(self.temporal_patterns)
        )

        total_samples = sum(
            pattern.get('total_interactions', 0) +
            pattern.get('total_suggestions', 0)
            for pattern in [
                *self.feedback_patterns.values(),
                *self.success_patterns.values(),
                *self.context_effectiveness.values(),
                *self.temporal_patterns.values()
            ]
        )

        return {
            'total_patterns_learned': total_patterns,
            'total_interaction_samples': total_samples,
            'learning_rate': self.learning_rate,
            'min_samples_threshold': self.min_samples_for_learning,
            'patterns_by_type': {
                'feedback_patterns': len(self.feedback_patterns),
                'success_patterns': len(self.success_patterns),
                'context_effectiveness': len(self.context_effectiveness),
                'temporal_patterns': len(self.temporal_patterns)
            }
        }

    def get_personalized_suggestion_adjustments(self, suggestion: CommandSuggestion,
                                              context: SuggestionContext) -> Dict[str, float]:
        """Get personalized adjustments for suggestion based on learning."""
        adjustments = {
            'confidence_boost': 0.0,
            'context_multiplier': 1.0,
            'temporal_multiplier': 1.0,
            'category_multiplier': 1.0
        }

        try:
            # Apply feedback-based adjustments
            feedback_boost = self._get_feedback_based_boost(suggestion, context)
            adjustments['confidence_boost'] += feedback_boost

            # Apply context-based adjustments
            context_multiplier = self._get_context_based_multiplier(suggestion, context)
            adjustments['context_multiplier'] *= context_multiplier

            # Apply temporal adjustments
            temporal_multiplier = self._get_temporal_multiplier(suggestion, context)
            adjustments['temporal_multiplier'] *= temporal_multiplier

            # Apply category adjustments
            category_multiplier = self._get_category_multiplier(suggestion, context)
            adjustments['category_multiplier'] *= category_multiplier

        except Exception as e:
            logger.warning(f"Error calculating personalized adjustments: {e}")

        return adjustments

    def _get_feedback_based_boost(self, suggestion: CommandSuggestion,
                                context: SuggestionContext) -> float:
        """Get confidence boost based on feedback patterns."""
        pattern_key = f"{suggestion.command}_{suggestion.category.value}"

        if pattern_key in self.feedback_patterns:
            pattern = self.feedback_patterns[pattern_key]

            if pattern['total_interactions'] >= self.min_samples_for_learning:
                success_rate = pattern['helpful_interactions'] / pattern['total_interactions']

                # Boost confidence for well-received suggestions
                if success_rate > 0.7:
                    return 0.1
                elif success_rate < 0.3:
                    return -0.1

        return 0.0

    def _get_context_based_multiplier(self, suggestion: CommandSuggestion,
                                    context: SuggestionContext) -> float:
        """Get context-based multiplier."""
        context_key = f"{context.project_phase}_{context.time_of_day}"

        if context_key in self.context_effectiveness:
            context_data = self.context_effectiveness[context_key]
            category = suggestion.category.value

            if category in context_data['categories']:
                cat_data = context_data['categories'][category]

                if cat_data['suggestions'] >= 3:
                    success_rate = cat_data['successes'] / cat_data['suggestions']

                    # Scale multiplier based on success rate
                    if success_rate > 0.7:
                        return 1.2
                    elif success_rate < 0.3:
                        return 0.8

        return 1.0

    def _get_temporal_multiplier(self, suggestion: CommandSuggestion,
                               context: SuggestionContext) -> float:
        """Get temporal multiplier."""
        time_key = context.time_of_day

        if time_key in self.temporal_patterns:
            time_data = self.temporal_patterns[time_key]
            category = suggestion.category.value

            if category in time_data['categories']:
                cat_data = time_data['categories'][category]

                if cat_data['suggestions'] >= 3:
                    success_rate = cat_data['successes'] / cat_data['suggestions']

                    # Scale multiplier based on time-based success
                    if success_rate > 0.7:
                        return 1.15
                    elif success_rate < 0.3:
                        return 0.85

        return 1.0

    def _get_category_multiplier(self, suggestion: CommandSuggestion,
                               context: SuggestionContext) -> float:
        """Get category-based multiplier."""
        pattern_key = f"{suggestion.category.value}_{context.project_phase}"

        if pattern_key in self.success_patterns:
            pattern = self.success_patterns[pattern_key]

            if pattern['total_suggestions'] >= self.min_samples_for_learning:
                success_rate = pattern['successful_suggestions'] / pattern['total_suggestions']

                if success_rate > 0.7:
                    return 1.1
                elif success_rate < 0.3:
                    return 0.9

        return 1.0

    def export_learning_model(self) -> Dict[str, Any]:
        """Export learning model for backup or transfer."""
        return {
            'feedback_patterns': self.feedback_patterns,
            'success_patterns': self.success_patterns,
            'context_effectiveness': self.context_effectiveness,
            'temporal_patterns': self.temporal_patterns,
            'learning_config': {
                'learning_rate': self.learning_rate,
                'min_samples_for_learning': self.min_samples_for_learning,
                'pattern_decay_factor': self.pattern_decay_factor
            },
            'exported_at': datetime.now().isoformat()
        }

    def import_learning_model(self, model_data: Dict[str, Any]) -> bool:
        """Import learning model from backup."""
        try:
            if 'feedback_patterns' in model_data:
                self.feedback_patterns = model_data['feedback_patterns']
            if 'success_patterns' in model_data:
                self.success_patterns = model_data['success_patterns']
            if 'context_effectiveness' in model_data:
                self.context_effectiveness = model_data['context_effectiveness']
            if 'temporal_patterns' in model_data:
                self.temporal_patterns = model_data['temporal_patterns']

            # Update config if provided
            if 'learning_config' in model_data:
                config = model_data['learning_config']
                self.learning_rate = config.get('learning_rate', self.learning_rate)
                self.min_samples_for_learning = config.get('min_samples_for_learning', self.min_samples_for_learning)
                self.pattern_decay_factor = config.get('pattern_decay_factor', self.pattern_decay_factor)

            self._save_learning_data()
            logger.info("Learning model imported successfully")
            return True

        except Exception as e:
            logger.error(f"Error importing learning model: {e}")
            return False