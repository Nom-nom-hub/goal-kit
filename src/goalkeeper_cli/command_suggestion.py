#!/usr/bin/env python3
"""
Context-Aware Command Suggestion System for Goalkeeper CLI

This module implements intelligent command suggestions based on user context,
interaction history, and project state.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple, TYPE_CHECKING
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import re
import logging

if TYPE_CHECKING:
    # Forward references for type hints
    from typing import List as ListType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SuggestionCategory(Enum):
    """Categories for command suggestions."""
    GOAL_MANAGEMENT = "goal_management"
    PROJECT_ANALYSIS = "project_analysis"
    PROGRESS_TRACKING = "progress_tracking"
    COLLABORATION = "collaboration"
    AUTOMATION = "automation"
    LEARNING = "learning"
    VALIDATION = "validation"
    PLANNING = "planning"


class ConfidenceLevel(Enum):
    """Confidence levels for suggestions."""
    VERY_HIGH = "very_high"  # 0.9-1.0
    HIGH = "high"           # 0.7-0.9
    MEDIUM = "medium"       # 0.5-0.7
    LOW = "low"            # 0.3-0.5
    VERY_LOW = "very_low"   # 0.0-0.3


@dataclass
class UserIntentSignal:
    """Represents a signal indicating user intent."""

    signal_type: str  # e.g., "recent_command", "project_phase", "time_of_day"
    signal_value: Any
    confidence: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self, max_age_hours: int = 24) -> bool:
        """Check if signal is too old to be relevant."""
        age_hours = (datetime.now() - self.timestamp).total_seconds() / 3600
        return age_hours > max_age_hours

    def get_relevance_score(self) -> float:
        """Get relevance score based on age and confidence."""
        age_hours = (datetime.now() - self.timestamp).total_seconds() / 3600
        age_factor = max(0.1, 1.0 - (age_hours / 24.0))  # Decay over 24 hours

        return self.confidence * age_factor


@dataclass
class CommandUsagePattern:
    """Pattern of command usage for learning."""

    command: str
    usage_count: int = 0
    success_rate: float = 0.0
    avg_confidence_before_use: float = 0.0
    contexts: List[str] = field(default_factory=list)  # Project phases, times, etc.
    co_occurring_commands: Dict[str, int] = field(default_factory=dict)
    last_used: Optional[datetime] = None
    first_used: Optional[datetime] = None

    def record_usage(self, success: bool, confidence_score: float, context: str = "") -> None:
        """Record a usage instance."""
        self.usage_count += 1
        now = datetime.now()

        if self.first_used is None:
            self.first_used = now

        self.last_used = now

        # Update success rate (exponential moving average)
        alpha = 0.1  # Learning rate
        if success:
            self.success_rate = (1 - alpha) * self.success_rate + alpha * 1.0
        else:
            self.success_rate = (1 - alpha) * self.success_rate + alpha * 0.0

        # Update average confidence
        self.avg_confidence_before_use = (
            (1 - alpha) * self.avg_confidence_before_use + alpha * confidence_score
        )

        # Track context
        if context:
            self.contexts.append(context)

        # Update co-occurring commands (simplified - in real implementation,
        # this would track commands used in the same session)
        # For now, just track frequency

    def get_usage_frequency_score(self) -> float:
        """Get frequency-based score for ranking."""
        if self.usage_count == 0:
            return 0.0

        # Logarithmic scaling for frequency
        return min(1.0, self.usage_count / 20.0)

    def get_success_score(self) -> float:
        """Get success-based score."""
        return self.success_rate

    def get_context_relevance_score(self, current_context: str) -> float:
        """Get relevance score for current context."""
        if not current_context or not self.contexts:
            return 0.5  # Neutral score

        context_count = self.contexts.count(current_context)
        return min(1.0, context_count / len(self.contexts))


@dataclass
class CommandSuggestion:
    """Structured suggestion format with confidence scores and reasoning."""

    # Core suggestion data
    command: str
    description: str
    category: SuggestionCategory
    confidence_score: float = 0.0
    confidence_level: ConfidenceLevel = ConfidenceLevel.MEDIUM

    # Reasoning and context
    reasoning: List[str] = field(default_factory=list)
    context_factors: Dict[str, float] = field(default_factory=dict)
    user_intent_signals: List[str] = field(default_factory=list)

    # Usage and feedback
    suggested_at: datetime = field(default_factory=datetime.now)
    used_count: int = 0
    last_used: Optional[datetime] = None
    user_feedback_score: Optional[float] = None  # -1.0 to 1.0

    # Command metadata
    parameters: Dict[str, Any] = field(default_factory=dict)
    examples: List[str] = field(default_factory=list)
    related_commands: List[str] = field(default_factory=list)

    # Project context
    project_phase: str = "unknown"
    goal_context: List[str] = field(default_factory=list)
    urgency_level: str = "normal"  # low, normal, high, critical

    def __post_init__(self):
        """Post-initialization processing."""
        self._update_confidence_level()
        self._validate_suggestion()

    def _update_confidence_level(self) -> None:
        """Update confidence level based on score."""
        if self.confidence_score >= 0.9:
            self.confidence_level = ConfidenceLevel.VERY_HIGH
        elif self.confidence_score >= 0.7:
            self.confidence_level = ConfidenceLevel.HIGH
        elif self.confidence_score >= 0.5:
            self.confidence_level = ConfidenceLevel.MEDIUM
        elif self.confidence_score >= 0.3:
            self.confidence_level = ConfidenceLevel.LOW
        else:
            self.confidence_level = ConfidenceLevel.VERY_LOW

    def _validate_suggestion(self) -> None:
        """Validate suggestion data."""
        if not self.command or not self.description:
            raise ValueError("Command and description are required")

        if not 0.0 <= self.confidence_score <= 1.0:
            raise ValueError("Confidence score must be between 0.0 and 1.0")

        if self.user_feedback_score is not None:
            if not -1.0 <= self.user_feedback_score <= 1.0:
                raise ValueError("User feedback score must be between -1.0 and 1.0")

    def add_reasoning(self, reason: str, weight: float = 1.0) -> None:
        """Add reasoning with optional weight for confidence calculation."""
        self.reasoning.append(reason)
        if weight != 1.0:
            self.context_factors[f"reasoning_{len(self.reasoning)}"] = weight

    def add_context_factor(self, factor: str, value: float) -> None:
        """Add context factor that influenced this suggestion."""
        self.context_factors[factor] = value

    def mark_used(self, success: bool = True) -> None:
        """Mark suggestion as used."""
        self.used_count += 1
        self.last_used = datetime.now()

        # Adjust confidence based on usage success
        if success:
            # Positive reinforcement
            self.confidence_score = min(1.0, self.confidence_score + 0.1)
        else:
            # Negative feedback
            self.confidence_score = max(0.0, self.confidence_score - 0.1)

        self._update_confidence_level()

    def set_user_feedback(self, score: float) -> None:
        """Set user feedback score and adjust confidence."""
        if not -1.0 <= score <= 1.0:
            raise ValueError("Feedback score must be between -1.0 and 1.0")

        self.user_feedback_score = score

        # Adjust confidence based on user feedback
        adjustment = score * 0.2  # Scale feedback impact
        self.confidence_score = max(0.0, min(1.0, self.confidence_score + adjustment))
        self._update_confidence_level()

    def get_usage_score(self) -> float:
        """Calculate usage-based score for ranking."""
        if self.used_count == 0:
            return 0.5  # Neutral score for unused suggestions

        # Recency factor (newer usage = higher score)
        if self.last_used:
            hours_ago = (datetime.now() - self.last_used).total_seconds() / 3600
            recency_factor = max(0.1, 1.0 - (hours_ago / 168))  # Decay over a week
        else:
            recency_factor = 0.5

        # Frequency factor (logarithmic scaling)
        frequency_factor = min(1.0, self.used_count / 10.0)

        # Success rate factor (based on user feedback)
        if self.user_feedback_score is not None:
            success_factor = (self.user_feedback_score + 1.0) / 2.0  # Convert -1..1 to 0..1
        else:
            success_factor = 0.7  # Assume moderate success if no feedback

        # Combine factors
        usage_score = (recency_factor * 0.4 + frequency_factor * 0.3 + success_factor * 0.3)
        return min(1.0, usage_score)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)

        # Convert datetime objects
        for key in ['suggested_at', 'last_used']:
            if data[key] is not None:
                data[key] = data[key].isoformat()

        # Convert enums to strings
        data['category'] = self.category.value
        data['confidence_level'] = self.confidence_level.value

        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'CommandSuggestion':
        """Create from dictionary."""
        # Convert ISO strings back to datetime
        for key in ['suggested_at', 'last_used']:
            if key in data and data[key]:
                try:
                    data[key] = datetime.fromisoformat(data[key])
                except (ValueError, TypeError):
                    data[key] = None

        # Convert string enums back to enum objects
        if 'category' in data and isinstance(data['category'], str):
            try:
                data['category'] = SuggestionCategory(data['category'])
            except ValueError:
                data['category'] = SuggestionCategory.GOAL_MANAGEMENT

        if 'confidence_level' in data and isinstance(data['confidence_level'], str):
            try:
                data['confidence_level'] = ConfidenceLevel(data['confidence_level'])
            except ValueError:
                data['confidence_level'] = ConfidenceLevel.MEDIUM

        return cls(**data)


@dataclass
class SuggestionContext:
    """Context information for generating suggestions."""

    # Project context
    project_path: Optional[Path] = None
    current_goal: Optional[str] = None
    project_phase: str = "unknown"
    active_goals: List[str] = field(default_factory=list)

    # User context
    recent_commands: List[str] = field(default_factory=list)
    session_commands: List[str] = field(default_factory=list)
    user_preferences: Dict[str, Any] = field(default_factory=dict)

    # Temporal context
    time_of_day: str = "unknown"
    day_of_week: str = "unknown"
    session_duration_minutes: int = 0

    # System context
    available_commands: Set[str] = field(default_factory=set)
    system_capabilities: Dict[str, bool] = field(default_factory=dict)

    # Learning context
    intent_signals: List[UserIntentSignal] = field(default_factory=list)
    usage_patterns: Dict[str, CommandUsagePattern] = field(default_factory=dict)

    def add_intent_signal(self, signal: UserIntentSignal) -> None:
        """Add user intent signal."""
        self.intent_signals.append(signal)

    def get_recent_intent_signals(self, max_age_hours: int = 24) -> List[UserIntentSignal]:
        """Get recent intent signals."""
        return [
            signal for signal in self.intent_signals
            if not signal.is_expired(max_age_hours)
        ]

    def get_command_pattern(self, command: str) -> Optional[CommandUsagePattern]:
        """Get usage pattern for a command."""
        return self.usage_patterns.get(command)

    def update_command_pattern(self, command: str, success: bool,
                              confidence_score: float, context: str = "") -> None:
        """Update usage pattern for a command."""
        if command not in self.usage_patterns:
            self.usage_patterns[command] = CommandUsagePattern(command=command)

        self.usage_patterns[command].record_usage(success, confidence_score, context)

    def get_context_relevance_score(self, category: SuggestionCategory) -> float:
        """Get relevance score for suggestion category based on current context."""
        score = 0.5  # Base score

        # Project phase relevance
        phase_relevance = self._get_phase_relevance(category)
        score = (score + phase_relevance) / 2.0

        # Recent activity relevance
        activity_relevance = self._get_activity_relevance(category)
        score = (score + activity_relevance) / 2.0

        # Time-based relevance
        time_relevance = self._get_time_relevance(category)
        score = (score + time_relevance) / 2.0

        return min(1.0, score)

    def _get_phase_relevance(self, category: SuggestionCategory) -> float:
        """Get relevance based on project phase."""
        phase = self.project_phase.lower()

        relevance_map = {
            SuggestionCategory.GOAL_MANAGEMENT: {
                "planning": 0.9, "setup": 0.8, "execution": 0.6, "review": 0.7
            },
            SuggestionCategory.PROJECT_ANALYSIS: {
                "planning": 0.7, "setup": 0.5, "execution": 0.8, "review": 0.9
            },
            SuggestionCategory.PROGRESS_TRACKING: {
                "planning": 0.4, "setup": 0.6, "execution": 0.9, "review": 0.8
            },
            SuggestionCategory.VALIDATION: {
                "planning": 0.6, "setup": 0.7, "execution": 0.8, "review": 0.9
            }
        }

        return relevance_map.get(category, {}).get(phase, 0.5)

    def _get_activity_relevance(self, category: SuggestionCategory) -> float:
        """Get relevance based on recent activity."""
        if not self.recent_commands:
            return 0.5

        # Analyze recent command patterns
        recent_categories = []
        for cmd in self.recent_commands[-5:]:  # Last 5 commands
            recent_categories.extend(self._command_to_categories(cmd))

        if category.value in recent_categories:
            return 0.8
        elif len(set(recent_categories)) < 3:  # Focused activity
            return 0.6
        else:
            return 0.4

    def _get_time_relevance(self, category: SuggestionCategory) -> float:
        """Get relevance based on time of day/week."""
        time_of_day = self.time_of_day.lower()

        # Morning hours - planning and setup
        if time_of_day in ["morning", "early"] and category in [
            SuggestionCategory.GOAL_MANAGEMENT, SuggestionCategory.PLANNING
        ]:
            return 0.8

        # Evening hours - review and analysis
        if time_of_day in ["evening", "night"] and category in [
            SuggestionCategory.PROJECT_ANALYSIS, SuggestionCategory.PROGRESS_TRACKING
        ]:
            return 0.8

        return 0.5

    def _command_to_categories(self, command: str) -> List[str]:
        """Map command to categories."""
        # This is a simplified mapping - in practice, this would be more sophisticated
        command_category_map = {
            "init": ["goal_management"],
            "goal": ["goal_management"],
            "vision": ["goal_management"],
            "strategies": ["planning"],
            "milestones": ["planning"],
            "tasks": ["planning"],
            "progress": ["progress_tracking"],
            "analytics": ["project_analysis"],
            "validate": ["validation"],
            "analyze": ["project_analysis"],
            "insights": ["project_analysis"],
            "track": ["progress_tracking"],
            "learn": ["learning"],
            "research": ["project_analysis"],
            "benchmark": ["project_analysis"],
            "memory": ["learning"],
            "baseline": ["project_analysis"]
        }

        return command_category_map.get(command, ["goal_management"])

    def _get_command_metadata(self, command: str) -> Dict[str, Any]:
        """Get metadata for a command."""
        # This is a simplified implementation for testing
        return {
            'complexity': 'medium',
            'category': 'goal_management',
            'frequency': 'medium'
        }

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)

        # Convert Path to string
        if self.project_path:
            data['project_path'] = str(self.project_path)

        # Convert datetime objects
        for key in ['intent_signals']:
            if key in data:
                data[key] = [
                    signal.__dict__ if hasattr(signal, '__dict__') else asdict(signal)
                    for signal in data[key]
                ]

        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'SuggestionContext':
        """Create from dictionary."""
        # Convert string to Path
        if 'project_path' in data and data['project_path']:
            data['project_path'] = Path(data['project_path'])

        # Convert intent signals
        if 'intent_signals' in data:
            data['intent_signals'] = [
                UserIntentSignal(**signal_data) if isinstance(signal_data, dict) else signal_data
                for signal_data in data['intent_signals']
            ]

        return cls(**data)


class UserIntentAnalyzer:
    """Analyze user patterns and intent from interaction history."""

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.intent_patterns: Dict[str, List[UserIntentSignal]] = {}
        self.command_sequences: List[List[str]] = []
        self.session_patterns: Dict[str, Dict[str, Any]] = {}
        self.learning_data: Dict[str, Any] = {}

        # Load existing data
        self._load_intent_data()

    def _load_intent_data(self) -> None:
        """Load existing intent analysis data."""
        intent_file = self.project_path / ".goalkit" / "intent_patterns.json"

        if intent_file.exists():
            try:
                with open(intent_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                self.intent_patterns = data.get('intent_patterns', {})
                self.command_sequences = data.get('command_sequences', [])
                self.session_patterns = data.get('session_patterns', {})
                self.learning_data = data.get('learning_data', {})

                logger.info(f"Loaded intent data from {intent_file}")

            except Exception as e:
                logger.warning(f"Failed to load intent data: {e}")

    def _save_intent_data(self) -> None:
        """Save intent analysis data."""
        intent_file = self.project_path / ".goalkit" / "intent_patterns.json"

        try:
            intent_file.parent.mkdir(parents=True, exist_ok=True)

            data = {
                'intent_patterns': self.intent_patterns,
                'command_sequences': self.command_sequences,
                'session_patterns': self.session_patterns,
                'learning_data': self.learning_data,
                'last_updated': datetime.now().isoformat()
            }

            with open(intent_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Failed to save intent data: {e}")

    def analyze_command_sequence(self, commands: List[str],
                               context: 'SuggestionContext') -> Dict[str, Any]:
        """Analyze a sequence of commands to identify patterns and intent."""
        if len(commands) < 2:
            return {}

        analysis = {
            'sequence_length': len(commands),
            'unique_commands': len(set(commands)),
            'command_categories': self._categorize_command_sequence(commands),
            'intent_signals': [],
            'patterns_detected': [],
            'confidence_factors': {}
        }

        # Detect common patterns
        patterns = self._detect_patterns(commands)
        analysis['patterns_detected'] = patterns

        # Generate intent signals
        intent_signals = self._generate_intent_signals(commands, context)
        analysis['intent_signals'] = intent_signals

        # Calculate confidence factors
        confidence_factors = self._calculate_confidence_factors(commands, context)
        analysis['confidence_factors'] = confidence_factors

        # Store for learning
        self._store_sequence_for_learning(commands, analysis)

        return analysis

    def _categorize_command_sequence(self, commands: List[str]) -> Dict[str, int]:
        """Categorize commands in sequence."""
        categories = {}

        for cmd in commands:
            cmd_categories = self._get_command_categories(cmd)
            for category in cmd_categories:
                categories[category] = categories.get(category, 0) + 1

        return categories

    def _get_command_categories(self, command: str) -> List[str]:
        """Get categories for a command."""
        # Map commands to categories based on goalkeeper CLI structure
        category_map = {
            # Goal Management
            'init': ['goal_management'],
            'goal': ['goal_management'],
            'vision': ['goal_management'],
            'strategies': ['planning'],
            'milestones': ['planning'],
            'tasks': ['planning'],

            # Progress Tracking
            'progress': ['progress_tracking'],
            'track': ['progress_tracking'],
            'analytics': ['project_analysis'],
            'ai_analytics': ['project_analysis'],

            # Analysis & Validation
            'analyze': ['project_analysis'],
            'validate': ['validation'],
            'validate_goals': ['validation'],
            'insights': ['project_analysis'],
            'insights_project': ['project_analysis'],
            'memory_insights': ['learning'],

            # Learning & Research
            'learn': ['learning'],
            'learn_from_project': ['learning'],
            'research': ['project_analysis'],
            'research_project': ['project_analysis'],
            'benchmark': ['project_analysis'],
            'benchmark_project': ['project_analysis'],

            # Memory & Patterns
            'memory': ['learning'],
            'memory_status': ['learning'],
            'memory_patterns': ['learning'],
            'learn_extract': ['learning'],

            # Automation
            'automate': ['automation'],
            'ai_generate': ['automation'],

            # Baseline & Metrics
            'baseline': ['project_analysis'],
            'check': ['validation']
        }

        return category_map.get(command, ['general'])

    def _detect_patterns(self, commands: List[str]) -> List[str]:
        """Detect patterns in command sequence."""
        patterns = []

        if len(commands) < 2:
            return patterns

        # Pattern: Goal workflow (vision -> goal -> strategies -> milestones)
        goal_workflow = ['vision', 'goal', 'strategies', 'milestones']
        if self._contains_sequence(commands, goal_workflow):
            patterns.append('goal_workflow')

        # Pattern: Analysis workflow (analyze -> insights -> validate)
        analysis_workflow = ['analyze', 'insights', 'validate']
        if self._contains_sequence(commands, analysis_workflow):
            patterns.append('analysis_workflow')

        # Pattern: Learning workflow (learn -> memory -> insights)
        learning_workflow = ['learn', 'memory', 'insights']
        if self._contains_sequence(commands, learning_workflow):
            patterns.append('learning_workflow')

        # Pattern: Progress tracking (progress -> track -> analytics)
        progress_workflow = ['progress', 'track', 'analytics']
        if self._contains_sequence(commands, progress_workflow):
            patterns.append('progress_tracking')

        # Pattern: Validation workflow (validate -> check -> baseline)
        validation_workflow = ['validate', 'check', 'baseline']
        if self._contains_sequence(commands, validation_workflow):
            patterns.append('validation_workflow')

        # Frequency patterns
        if len(set(commands)) == 1:
            patterns.append('repetitive_commands')

        if len(commands) >= 5:
            patterns.append('extended_session')

        # Category focus patterns
        categories = self._categorize_command_sequence(commands)
        if len(categories) == 1:
            dominant_category = list(categories.keys())[0]
            patterns.append(f'focused_on_{dominant_category}')

        return patterns

    def _contains_sequence(self, commands: List[str], pattern: List[str]) -> bool:
        """Check if command sequence contains a specific pattern."""
        for i in range(len(commands) - len(pattern) + 1):
            if commands[i:i+len(pattern)] == pattern:
                return True
        return False

    def _generate_intent_signals(self, commands: List[str],
                               context: 'SuggestionContext') -> List[UserIntentSignal]:
        """Generate intent signals from command sequence."""
        signals = []

        # Time-based signals
        time_signal = self._analyze_time_patterns(commands, context)
        if time_signal:
            signals.append(time_signal)

        # Workflow signals
        workflow_signal = self._analyze_workflow_intent(commands)
        if workflow_signal:
            signals.append(workflow_signal)

        # Context signals
        context_signal = self._analyze_context_intent(commands, context)
        if context_signal:
            signals.append(context_signal)

        # Frequency signals
        frequency_signal = self._analyze_frequency_intent(commands)
        if frequency_signal:
            signals.append(frequency_signal)

        return signals

    def _analyze_time_patterns(self, commands: List[str],
                             context: 'SuggestionContext') -> Optional[UserIntentSignal]:
        """Analyze time-based patterns."""
        if not hasattr(context, 'time_of_day') or not context.time_of_day:
            return None

        # Morning patterns - planning and setup
        morning_commands = {'vision', 'goal', 'strategies', 'plan'}
        if (context.time_of_day.lower() in ['morning', 'early'] and
            any(cmd in commands for cmd in morning_commands)):
            return UserIntentSignal(
                signal_type="time_based_planning",
                signal_value="morning_planning_session",
                confidence=0.8,
                context={'time_of_day': context.time_of_day, 'commands': commands}
            )

        # Evening patterns - review and analysis
        evening_commands = {'progress', 'analytics', 'insights', 'validate'}
        if (context.time_of_day.lower() in ['evening', 'night'] and
            any(cmd in commands for cmd in evening_commands)):
            return UserIntentSignal(
                signal_type="time_based_review",
                signal_value="evening_review_session",
                confidence=0.8,
                context={'time_of_day': context.time_of_day, 'commands': commands}
            )

        return None

    def _analyze_workflow_intent(self, commands: List[str]) -> Optional[UserIntentSignal]:
        """Analyze workflow-based intent."""
        # Goal creation workflow
        goal_indicators = {'vision', 'goal', 'strategies'}
        if (len(set(commands) & goal_indicators) >= 2 and
            'goal' in commands):
            return UserIntentSignal(
                signal_type="workflow_goal_creation",
                signal_value="creating_new_goal",
                confidence=0.7,
                context={'workflow': 'goal_creation', 'commands': commands}
            )

        # Analysis workflow
        analysis_indicators = {'analyze', 'insights', 'validate'}
        if (len(set(commands) & analysis_indicators) >= 2):
            return UserIntentSignal(
                signal_type="workflow_analysis",
                signal_value="project_analysis",
                confidence=0.7,
                context={'workflow': 'analysis', 'commands': commands}
            )

        # Learning workflow
        learning_indicators = {'learn', 'memory', 'research'}
        if (len(set(commands) & learning_indicators) >= 2):
            return UserIntentSignal(
                signal_type="workflow_learning",
                signal_value="knowledge_building",
                confidence=0.7,
                context={'workflow': 'learning', 'commands': commands}
            )

        return None

    def _analyze_context_intent(self, commands: List[str],
                               context: 'SuggestionContext') -> Optional[UserIntentSignal]:
        """Analyze context-based intent."""
        # Project phase context
        if context.project_phase != 'unknown':
            phase_commands = {
                'planning': {'vision', 'goal', 'strategies'},
                'execution': {'tasks', 'progress', 'track'},
                'review': {'analytics', 'insights', 'validate'}
            }

            phase = context.project_phase.lower()
            if phase in phase_commands:
                relevant_commands = phase_commands[phase]
                if any(cmd in commands for cmd in relevant_commands):
                    return UserIntentSignal(
                        signal_type="project_phase_context",
                        signal_value=phase,
                        confidence=0.6,
                        context={'project_phase': phase, 'commands': commands}
                    )

        # Goal context
        if context.current_goal:
            goal_commands = {'milestones', 'tasks', 'progress'}
            if any(cmd in commands for cmd in goal_commands):
                return UserIntentSignal(
                    signal_type="goal_context",
                    signal_value=context.current_goal,
                    confidence=0.8,
                    context={'current_goal': context.current_goal, 'commands': commands}
                )

        return None

    def _analyze_frequency_intent(self, commands: List[str]) -> Optional[UserIntentSignal]:
        """Analyze frequency-based intent."""
        if len(commands) <= 3:
            return None

        # Check for repetitive patterns
        command_counts = {}
        for cmd in commands:
            command_counts[cmd] = command_counts.get(cmd, 0) + 1

        repetitive_commands = [cmd for cmd, count in command_counts.items() if count >= 3]

        if repetitive_commands:
            return UserIntentSignal(
                signal_type="frequency_repetitive",
                signal_value=repetitive_commands,
                confidence=0.6,
                context={'repetitive_commands': repetitive_commands, 'counts': command_counts}
            )

        # Check for exploratory patterns (many different commands)
        unique_ratio = len(set(commands)) / len(commands)
        if unique_ratio > 0.7 and len(commands) >= 5:
            return UserIntentSignal(
                signal_type="frequency_exploratory",
                signal_value="exploring_capabilities",
                confidence=0.5,
                context={'unique_ratio': unique_ratio, 'total_commands': len(commands)}
            )

        return None

    def _calculate_confidence_factors(self, commands: List[str],
                                    context: SuggestionContext) -> Dict[str, float]:
        """Calculate confidence factors for suggestions."""
        factors = {
            'sequence_length': min(1.0, len(commands) / 10.0),
            'pattern_strength': 0.5,
            'context_relevance': 0.5,
            'historical_success': 0.5
        }

        # Pattern strength based on detected patterns
        patterns = self._detect_patterns(commands)
        if patterns:
            factors['pattern_strength'] = min(1.0, len(patterns) * 0.2)

        # Context relevance
        if context.project_phase != 'unknown':
            factors['context_relevance'] = 0.8
        elif context.current_goal:
            factors['context_relevance'] = 0.7

        # Historical success based on stored patterns
        if self.learning_data.get('success_patterns'):
            factors['historical_success'] = 0.7

        return factors

    def _store_sequence_for_learning(self, commands: List[str], analysis: Dict[str, Any]) -> None:
        """Store command sequence for future learning."""
        # Store sequence
        self.command_sequences.append(commands)

        # Keep only recent sequences (last 100)
        if len(self.command_sequences) > 100:
            self.command_sequences = self.command_sequences[-100:]

        # Update learning data
        for pattern in analysis.get('patterns_detected', []):
            if pattern not in self.learning_data:
                self.learning_data[pattern] = {'count': 0, 'success_rate': 0.5}
            self.learning_data[pattern]['count'] += 1

        # Save data
        self._save_intent_data()

    def get_intent_prediction(self, partial_commands: List[str],
                            context: SuggestionContext) -> Dict[str, Any]:
        """Predict user intent based on partial command sequence."""
        if len(partial_commands) < 1:
            return {}

        prediction = {
            'likely_intent': 'unknown',
            'confidence': 0.0,
            'next_commands': [],
            'intent_signals': [],
            'reasoning': []
        }

        # Find similar sequences
        similar_sequences = self._find_similar_sequences(partial_commands)

        if similar_sequences:
            # Analyze similar sequences to predict next steps
            next_commands = self._predict_next_commands(partial_commands, similar_sequences)
            prediction['next_commands'] = next_commands

            # Determine likely intent
            intent_analysis = self._analyze_predicted_intent(next_commands, context)
            prediction.update(intent_analysis)

        # Generate intent signals for current partial sequence
        current_signals = self._generate_intent_signals(partial_commands, context)
        prediction['intent_signals'] = current_signals

        return prediction

    def _find_similar_sequences(self, partial_commands: List[str]) -> List[List[str]]:
        """Find command sequences similar to the partial sequence."""
        similar = []

        for sequence in self.command_sequences:
            if len(sequence) >= len(partial_commands):
                # Check if sequence starts with partial commands
                if sequence[:len(partial_commands)] == partial_commands:
                    similar.append(sequence)

        return similar

    def _predict_next_commands(self, partial_commands: List[str],
                             similar_sequences: List[List[str]]) -> List[str]:
        """Predict next commands based on similar sequences."""
        next_commands = {}

        for sequence in similar_sequences:
            if len(sequence) > len(partial_commands):
                next_cmd = sequence[len(partial_commands)]
                next_commands[next_cmd] = next_commands.get(next_cmd, 0) + 1

        # Return commands sorted by frequency
        return sorted(next_commands.keys(), key=lambda x: next_commands[x], reverse=True)

    def _analyze_predicted_intent(self, next_commands: List[str],
                                context: SuggestionContext) -> Dict[str, Any]:
        """Analyze predicted intent based on next commands."""
        if not next_commands:
            return {'likely_intent': 'unknown', 'confidence': 0.0}

        # Analyze categories of predicted commands
        predicted_categories = {}
        for cmd in next_commands:
            categories = self._get_command_categories(cmd)
            for category in categories:
                predicted_categories[category] = predicted_categories.get(category, 0) + 1

        # Determine most likely intent
        if predicted_categories:
            likely_category = max(predicted_categories.keys(),
                               key=lambda x: predicted_categories[x])

            # Map category to intent
            intent_map = {
                'goal_management': 'goal_creation',
                'planning': 'project_planning',
                'project_analysis': 'data_analysis',
                'progress_tracking': 'monitoring',
                'validation': 'quality_assurance',
                'learning': 'knowledge_building',
                'automation': 'task_automation'
            }

            confidence = min(0.9, len(next_commands) * 0.2)

            return {
                'likely_intent': intent_map.get(likely_category, 'general'),
                'confidence': confidence,
                'reasoning': [f'Predicted next commands suggest {likely_category} focus']
            }

        return {'likely_intent': 'unknown', 'confidence': 0.0}

    def learn_from_feedback(self, commands: List[str], suggestion: CommandSuggestion,
                           was_helpful: bool, context: SuggestionContext) -> None:
        """Learn from user feedback on suggestions."""
        # Store feedback for learning
        feedback_key = f"{suggestion.command}_{'helpful' if was_helpful else 'not_helpful'}"

        if feedback_key not in self.learning_data:
            self.learning_data[feedback_key] = {
                'count': 0,
                'contexts': [],
                'avg_confidence': 0.0
            }

        feedback_data = self.learning_data[feedback_key]
        feedback_data['count'] += 1

        # Update average confidence
        alpha = 0.1
        feedback_data['avg_confidence'] = (
            (1 - alpha) * feedback_data['avg_confidence'] + alpha * suggestion.confidence_score
        )

        # Store context for pattern analysis
        context_key = f"{context.project_phase}_{context.time_of_day}"
        if context_key not in feedback_data['contexts']:
            feedback_data['contexts'].append(context_key)

        # Update suggestion success patterns
        pattern_key = f"success_pattern_{suggestion.category.value}"
        if pattern_key not in self.learning_data:
            self.learning_data[pattern_key] = {'helpful_count': 0, 'total_count': 0}

        pattern_data = self.learning_data[pattern_key]
        pattern_data['total_count'] += 1
        if was_helpful:
            pattern_data['helpful_count'] += 1

        # Save updated learning data
        self._save_intent_data()

    def get_user_preferences(self) -> Dict[str, Any]:
        """Get learned user preferences."""
        preferences = {
            'favorite_commands': [],
            'preferred_workflows': [],
            'time_patterns': {},
            'context_preferences': {}
        }

        # Analyze command frequency
        command_frequency = {}
        for sequence in self.command_sequences:
            for cmd in sequence:
                command_frequency[cmd] = command_frequency.get(cmd, 0) + 1

        # Get top commands
        if command_frequency:
            sorted_commands = sorted(command_frequency.items(), key=lambda x: x[1], reverse=True)
            preferences['favorite_commands'] = [cmd for cmd, _ in sorted_commands[:5]]

        # Analyze workflow preferences
        workflow_patterns = {}
        for sequence in self.command_sequences:
            patterns = self._detect_patterns(sequence)
            for pattern in patterns:
                workflow_patterns[pattern] = workflow_patterns.get(pattern, 0) + 1

        if workflow_patterns:
            sorted_workflows = sorted(workflow_patterns.items(), key=lambda x: x[1], reverse=True)
            preferences['preferred_workflows'] = [workflow for workflow, _ in sorted_workflows[:3]]

        return preferences

    def get_contextual_insights(self, context: SuggestionContext) -> Dict[str, Any]:
        """Get insights about user behavior in current context."""
        insights = {
            'current_session_patterns': [],
            'recommended_next_steps': [],
            'context_relevance': {},
            'learning_opportunities': []
        }

        # Analyze current session
        if context.session_commands:
            session_patterns = self._detect_patterns(context.session_commands)
            insights['current_session_patterns'] = session_patterns

            # Generate next step recommendations
            next_steps = self._generate_next_step_suggestions(context.session_commands, context)
            insights['recommended_next_steps'] = next_steps

        # Context relevance analysis
        for category in SuggestionCategory:
            relevance = context.get_context_relevance_score(category)
            insights['context_relevance'][category.value] = relevance

        return insights

    def _generate_next_step_suggestions(self, recent_commands: List[str],
                                      context: SuggestionContext) -> List[str]:
        """Generate next step suggestions based on recent commands."""
        suggestions = []

        if not recent_commands:
            return suggestions

        last_command = recent_commands[-1]

        # Command-based next step logic
        next_step_map = {
            'vision': ['goal', 'analyze'],
            'goal': ['strategies', 'milestones', 'validate'],
            'strategies': ['milestones', 'tasks', 'analyze'],
            'milestones': ['tasks', 'progress', 'track'],
            'tasks': ['progress', 'execute', 'validate'],
            'progress': ['analytics', 'insights', 'track'],
            'analytics': ['insights', 'validate', 'benchmark'],
            'validate': ['progress', 'learn', 'memory'],
            'analyze': ['insights', 'validate', 'research'],
            'insights': ['learn', 'memory', 'benchmark'],
            'learn': ['memory', 'research', 'benchmark'],
            'research': ['analyze', 'benchmark', 'validate']
        }

        if last_command in next_step_map:
            suggestions = next_step_map[last_command]

            # Filter based on context
            if context.project_phase != 'unknown':
                suggestions = self._filter_by_project_phase(suggestions, context.project_phase)

        return suggestions

    def _filter_by_project_phase(self, suggestions: List[str], phase: str) -> List[str]:
        """Filter suggestions based on project phase."""
        phase_filters = {
            'planning': ['vision', 'goal', 'strategies', 'plan'],
            'execution': ['tasks', 'progress', 'track', 'execute'],
            'review': ['analytics', 'insights', 'validate', 'benchmark'],
            'setup': ['init', 'vision', 'goal']
        }

        phase = phase.lower()
        if phase in phase_filters:
            allowed_commands = set(phase_filters[phase])
            return [s for s in suggestions if s in allowed_commands]

        return suggestions

    def export_learning_data(self) -> Dict[str, Any]:
        """Export learning data for analysis."""
        return {
            'intent_patterns': self.intent_patterns,
            'command_sequences_count': len(self.command_sequences),
            'session_patterns': self.session_patterns,
            'learning_data': self.learning_data,
            'exported_at': datetime.now().isoformat()
        }


class CommandPatternMatcher:
    """Match user intent to available commands using pattern recognition."""

    def __init__(self, available_commands: List[str]):
        self.available_commands = set(available_commands)
        self.intent_patterns: Dict[str, Dict[str, Any]] = {}
        self.command_metadata: Dict[str, Dict[str, Any]] = {}
        self.pattern_cache: Dict[str, List[str]] = {}

        # Initialize command metadata
        self._initialize_command_metadata()

    def _initialize_command_metadata(self) -> None:
        """Initialize metadata for all available commands."""
        # Command categories and characteristics
        command_info = {
            # Goal Management Commands
            'init': {
                'category': SuggestionCategory.GOAL_MANAGEMENT,
                'intent_keywords': ['start', 'create', 'initialize', 'setup', 'new project'],
                'context_phases': ['planning', 'setup'],
                'complexity': 'medium',
                'frequency': 'low',
                'prerequisites': [],
                'related_commands': ['goal', 'vision']
            },
            'goal': {
                'category': SuggestionCategory.GOAL_MANAGEMENT,
                'intent_keywords': ['goal', 'objective', 'target', 'define', 'create goal'],
                'context_phases': ['planning', 'execution'],
                'complexity': 'high',
                'frequency': 'medium',
                'prerequisites': ['init'],
                'related_commands': ['vision', 'strategies', 'milestones']
            },
            'vision': {
                'category': SuggestionCategory.GOAL_MANAGEMENT,
                'intent_keywords': ['vision', 'direction', 'purpose', 'mission', 'principles'],
                'context_phases': ['planning', 'setup'],
                'complexity': 'high',
                'frequency': 'low',
                'prerequisites': [],
                'related_commands': ['goal', 'strategies']
            },

            # Planning Commands
            'strategies': {
                'category': SuggestionCategory.PLANNING,
                'intent_keywords': ['strategy', 'approach', 'method', 'plan', 'how'],
                'context_phases': ['planning', 'execution'],
                'complexity': 'high',
                'frequency': 'medium',
                'prerequisites': ['goal'],
                'related_commands': ['milestones', 'tasks', 'analyze']
            },
            'milestones': {
                'category': SuggestionCategory.PLANNING,
                'intent_keywords': ['milestone', 'checkpoint', 'phase', 'stage', 'timeline'],
                'context_phases': ['planning', 'execution'],
                'complexity': 'medium',
                'frequency': 'medium',
                'prerequisites': ['strategies'],
                'related_commands': ['tasks', 'progress', 'track']
            },
            'tasks': {
                'category': SuggestionCategory.PLANNING,
                'intent_keywords': ['task', 'todo', 'action', 'work', 'execute'],
                'context_phases': ['execution', 'planning'],
                'complexity': 'medium',
                'frequency': 'high',
                'prerequisites': ['milestones'],
                'related_commands': ['progress', 'execute', 'validate']
            },

            # Progress Tracking Commands
            'progress': {
                'category': SuggestionCategory.PROGRESS_TRACKING,
                'intent_keywords': ['progress', 'status', 'advance', 'completion', 'update'],
                'context_phases': ['execution', 'review'],
                'complexity': 'low',
                'frequency': 'high',
                'prerequisites': ['milestones'],
                'related_commands': ['track', 'analytics', 'validate']
            },
            'track': {
                'category': SuggestionCategory.PROGRESS_TRACKING,
                'intent_keywords': ['track', 'monitor', 'follow', 'watch', 'observe'],
                'context_phases': ['execution', 'review'],
                'complexity': 'low',
                'frequency': 'medium',
                'prerequisites': ['progress'],
                'related_commands': ['progress', 'analytics']
            },

            # Analysis Commands
            'analytics': {
                'category': SuggestionCategory.PROJECT_ANALYSIS,
                'intent_keywords': ['analytics', 'data', 'metrics', 'statistics', 'performance'],
                'context_phases': ['review', 'execution'],
                'complexity': 'medium',
                'frequency': 'medium',
                'prerequisites': ['progress'],
                'related_commands': ['insights', 'benchmark', 'analyze']
            },
            'analyze': {
                'category': SuggestionCategory.PROJECT_ANALYSIS,
                'intent_keywords': ['analyze', 'examine', 'study', 'investigate', 'review'],
                'context_phases': ['review', 'planning'],
                'complexity': 'high',
                'frequency': 'medium',
                'prerequisites': [],
                'related_commands': ['insights', 'validate', 'research']
            },
            'insights': {
                'category': SuggestionCategory.PROJECT_ANALYSIS,
                'intent_keywords': ['insight', 'understanding', 'learning', 'discovery', 'wisdom'],
                'context_phases': ['review', 'planning'],
                'complexity': 'high',
                'frequency': 'medium',
                'prerequisites': ['analyze'],
                'related_commands': ['learn', 'memory', 'research']
            },

            # Validation Commands
            'validate': {
                'category': SuggestionCategory.VALIDATION,
                'intent_keywords': ['validate', 'verify', 'check', 'confirm', 'ensure'],
                'context_phases': ['review', 'execution'],
                'complexity': 'medium',
                'frequency': 'medium',
                'prerequisites': [],
                'related_commands': ['check', 'baseline', 'progress']
            },
            'validate_goals': {
                'category': SuggestionCategory.VALIDATION,
                'intent_keywords': ['validate goals', 'check goals', 'review objectives'],
                'context_phases': ['planning', 'review'],
                'complexity': 'medium',
                'frequency': 'low',
                'prerequisites': ['goal'],
                'related_commands': ['validate', 'analyze']
            },

            # Learning Commands
            'learn': {
                'category': SuggestionCategory.LEARNING,
                'intent_keywords': ['learn', 'knowledge', 'understand', 'discover', 'study'],
                'context_phases': ['review', 'planning'],
                'complexity': 'medium',
                'frequency': 'medium',
                'prerequisites': [],
                'related_commands': ['memory', 'insights', 'research']
            },
            'memory': {
                'category': SuggestionCategory.LEARNING,
                'intent_keywords': ['memory', 'recall', 'history', 'past', 'experience'],
                'context_phases': ['review', 'planning'],
                'complexity': 'low',
                'frequency': 'medium',
                'prerequisites': [],
                'related_commands': ['learn', 'insights', 'patterns']
            },
            'research': {
                'category': SuggestionCategory.LEARNING,
                'intent_keywords': ['research', 'investigate', 'explore', 'study', 'find'],
                'context_phases': ['planning', 'review'],
                'complexity': 'high',
                'frequency': 'low',
                'prerequisites': [],
                'related_commands': ['analyze', 'insights', 'benchmark']
            },

            # Automation Commands
            'automate': {
                'category': SuggestionCategory.AUTOMATION,
                'intent_keywords': ['automate', 'automatic', 'script', 'workflow'],
                'context_phases': ['execution', 'planning'],
                'complexity': 'high',
                'frequency': 'low',
                'prerequisites': [],
                'related_commands': ['tasks', 'execute']
            },

            # Baseline and Check Commands
            'baseline': {
                'category': SuggestionCategory.PROJECT_ANALYSIS,
                'intent_keywords': ['baseline', 'benchmark', 'standard', 'measure'],
                'context_phases': ['planning', 'review'],
                'complexity': 'medium',
                'frequency': 'low',
                'prerequisites': [],
                'related_commands': ['analytics', 'benchmark']
            },
            'check': {
                'category': SuggestionCategory.VALIDATION,
                'intent_keywords': ['check', 'verify', 'test', 'ensure'],
                'context_phases': ['setup', 'planning'],
                'complexity': 'low',
                'frequency': 'low',
                'prerequisites': [],
                'related_commands': ['validate', 'init']
            }
        }

        # Only include commands that are actually available
        for command in self.available_commands:
            if command in command_info:
                self.command_metadata[command] = command_info[command]
            else:
                # Default metadata for unknown commands
                self.command_metadata[command] = {
                    'category': SuggestionCategory.GOAL_MANAGEMENT,
                    'intent_keywords': [command],
                    'context_phases': ['planning', 'execution'],
                    'complexity': 'medium',
                    'frequency': 'medium',
                    'prerequisites': [],
                    'related_commands': []
                }

    def match_intent_to_commands(self, intent: str, context: SuggestionContext,
                               limit: int = 5) -> List[CommandSuggestion]:
        """Match user intent to available commands."""
        suggestions = []

        # Direct intent matching
        direct_matches = self._find_direct_matches(intent)
        for command in direct_matches:
            suggestion = self._create_suggestion(command, intent, context, 'direct_match')
            suggestions.append(suggestion)

        # Keyword-based matching
        keyword_matches = self._find_keyword_matches(intent)
        for command in keyword_matches:
            if command not in direct_matches:  # Avoid duplicates
                suggestion = self._create_suggestion(command, intent, context, 'keyword_match')
                suggestions.append(suggestion)

        # Context-based matching
        context_matches = self._find_context_matches(context)
        for command in context_matches:
            if command not in direct_matches and command not in keyword_matches:
                suggestion = self._create_suggestion(command, intent, context, 'context_match')
                suggestions.append(suggestion)

        # Pattern-based matching
        pattern_matches = self._find_pattern_matches(intent, context)
        for command in pattern_matches:
            if command not in [s.command for s in suggestions]:
                suggestion = self._create_suggestion(command, intent, context, 'pattern_match')
                suggestions.append(suggestion)

        # Sort by confidence and limit results
        suggestions.sort(key=lambda x: x.confidence_score, reverse=True)
        return suggestions[:limit]

    def _find_direct_matches(self, intent: str) -> List[str]:
        """Find direct command matches for intent."""
        matches = []

        # Check if intent directly mentions a command
        intent_words = set(re.findall(r'\w+', intent.lower()))

        for command in self.available_commands:
            if command in intent_words:
                matches.append(command)

        return matches

    def _find_keyword_matches(self, intent: str) -> List[str]:
        """Find commands matching intent keywords."""
        matches = []
        intent_lower = intent.lower()

        for command, metadata in self.command_metadata.items():
            # Check intent keywords
            for keyword in metadata['intent_keywords']:
                if keyword.lower() in intent_lower:
                    matches.append(command)
                    break

        return matches

    def _find_context_matches(self, context: SuggestionContext) -> List[str]:
        """Find commands relevant to current context."""
        matches = []

        # Project phase context
        if context.project_phase != 'unknown':
            phase = context.project_phase.lower()
            for command, metadata in self.command_metadata.items():
                if phase in metadata['context_phases']:
                    matches.append(command)

        # Recent commands context
        if context.recent_commands:
            recent_cmd = context.recent_commands[-1]
            if recent_cmd in self.command_metadata:
                related_commands = self.command_metadata[recent_cmd]['related_commands']
                for related_cmd in related_commands:
                    if related_cmd in self.available_commands:
                        matches.append(related_cmd)

        # Goal context
        if context.current_goal:
            goal_commands = ['milestones', 'tasks', 'progress', 'validate']
            for cmd in goal_commands:
                if cmd in self.available_commands:
                    matches.append(cmd)

        return matches

    def _find_pattern_matches(self, intent: str, context: SuggestionContext) -> List[str]:
        """Find commands based on detected patterns."""
        matches = []

        # Analyze intent for patterns
        intent_lower = intent.lower()

        # Goal-related patterns
        goal_patterns = ['goal', 'objective', 'target', 'achieve']
        if any(pattern in intent_lower for pattern in goal_patterns):
            goal_commands = ['goal', 'vision', 'strategies']
            for cmd in goal_commands:
                if cmd in self.available_commands:
                    matches.append(cmd)

        # Analysis patterns
        analysis_patterns = ['analyze', 'review', 'examine', 'study']
        if any(pattern in intent_lower for pattern in analysis_patterns):
            analysis_commands = ['analyze', 'insights', 'analytics']
            for cmd in analysis_commands:
                if cmd in self.available_commands:
                    matches.append(cmd)

        # Progress patterns
        progress_patterns = ['progress', 'status', 'advance', 'complete']
        if any(pattern in intent_lower for pattern in progress_patterns):
            progress_commands = ['progress', 'track', 'analytics']
            for cmd in progress_commands:
                if cmd in self.available_commands:
                    matches.append(cmd)

        # Learning patterns
        learning_patterns = ['learn', 'knowledge', 'understand', 'discover']
        if any(pattern in intent_lower for pattern in learning_patterns):
            learning_commands = ['learn', 'memory', 'insights', 'research']
            for cmd in learning_commands:
                if cmd in self.available_commands:
                    matches.append(cmd)

        return matches

    def _create_suggestion(self, command: str, original_intent: str,
                         context: SuggestionContext, match_type: str) -> CommandSuggestion:
        """Create a command suggestion."""
        metadata = self.command_metadata[command]

        # Calculate base confidence
        base_confidence = self._calculate_base_confidence(command, original_intent, match_type)

        # Adjust confidence based on context
        context_multiplier = self._calculate_context_multiplier(command, context)
        confidence_score = min(1.0, base_confidence * context_multiplier)

        # Generate reasoning
        reasoning = self._generate_reasoning(command, original_intent, match_type, context)

        # Create suggestion
        suggestion = CommandSuggestion(
            command=command,
            description=self._get_command_description(command),
            category=metadata['category'],
            confidence_score=confidence_score,
            reasoning=reasoning,
            project_phase=context.project_phase,
            urgency_level=self._get_urgency_level(command, context)
        )

        # Add context factors
        suggestion.add_context_factor('match_type', 1.0 if match_type == 'direct_match' else 0.7)
        suggestion.add_context_factor('context_relevance', context_multiplier)
        suggestion.add_context_factor('command_complexity', self._get_complexity_score(metadata['complexity']))

        return suggestion

    def _calculate_base_confidence(self, command: str, intent: str, match_type: str) -> float:
        """Calculate base confidence for a command match."""
        base_scores = {
            'direct_match': 0.9,
            'keyword_match': 0.7,
            'context_match': 0.6,
            'pattern_match': 0.5
        }

        base_score = base_scores.get(match_type, 0.5)

        # Boost confidence for exact matches
        if command in intent.lower():
            base_score += 0.1

        return min(1.0, base_score)

    def _calculate_context_multiplier(self, command: str, context: SuggestionContext) -> float:
        """Calculate context relevance multiplier."""
        metadata = self.command_metadata[command]
        multiplier = 1.0

        # Project phase relevance
        if context.project_phase != 'unknown':
            phase = context.project_phase.lower()
            if phase in metadata['context_phases']:
                multiplier *= 1.2
            else:
                multiplier *= 0.8

        # Recent commands relevance
        if context.recent_commands:
            recent_cmd = context.recent_commands[-1]
            if recent_cmd in metadata['related_commands']:
                multiplier *= 1.3
            elif recent_cmd == command:
                multiplier *= 0.7  # Avoid suggesting same command repeatedly

        # Time-based relevance
        time_relevance = self._get_time_relevance(command, context)
        multiplier *= time_relevance

        return min(1.5, max(0.5, multiplier))

    def _get_time_relevance(self, command: str, context: SuggestionContext) -> float:
        """Get time-based relevance for command."""
        if not hasattr(context, 'time_of_day') or not context.time_of_day:
            return 1.0

        time_of_day = context.time_of_day.lower()
        metadata = self.command_metadata[command]

        # Planning commands in morning
        if (time_of_day in ['morning', 'early'] and
            metadata['category'] in [SuggestionCategory.GOAL_MANAGEMENT, SuggestionCategory.PLANNING]):
            return 1.2

        # Review commands in evening
        if (time_of_day in ['evening', 'night'] and
            metadata['category'] in [SuggestionCategory.PROJECT_ANALYSIS, SuggestionCategory.PROGRESS_TRACKING]):
            return 1.2

        return 1.0

    def _generate_reasoning(self, command: str, intent: str, match_type: str,
                          context: SuggestionContext) -> List[str]:
        """Generate reasoning for suggestion."""
        reasoning = []
        metadata = self.command_metadata[command]

        # Match type reasoning
        match_reasons = {
            'direct_match': f"Command '{command}' was directly mentioned in your request",
            'keyword_match': f"Matches keywords in '{metadata['intent_keywords'][0]}'",
            'context_match': "Relevant to your current project context",
            'pattern_match': f"Follows common pattern for '{metadata['category'].value}' tasks"
        }
        reasoning.append(match_reasons.get(match_type, "Matches your intent"))

        # Context reasoning
        if context.project_phase != 'unknown':
            reasoning.append(f"Suitable for {context.project_phase} phase")

        if context.current_goal:
            reasoning.append("Relevant to your current goal focus")

        # Complexity reasoning
        complexity = metadata['complexity']
        if complexity == 'high':
            reasoning.append("Comprehensive command for detailed work")
        elif complexity == 'low':
            reasoning.append("Quick command for immediate needs")

        return reasoning

    def _get_command_description(self, command: str) -> str:
        """Get description for a command."""
        descriptions = {
            'init': 'Initialize a new Goalkeeper project',
            'goal': 'Define and manage project goals',
            'vision': 'Establish project vision and principles',
            'strategies': 'Explore implementation strategies',
            'milestones': 'Create measurable milestones',
            'tasks': 'Create actionable tasks for goals',
            'progress': 'Visualize progress of goals and milestones',
            'analytics': 'Generate analytics report on goal effectiveness',
            'validate': 'Validate goal files for quality standards',
            'analyze': 'Analyze project health and patterns',
            'insights': 'Generate AI-powered insights from project data',
            'learn': 'Extract and document lessons learned',
            'memory': 'Display memory system status and insights',
            'research': 'Research external information for project goals',
            'automate': 'Automate common goal management tasks',
            'baseline': 'Establish baseline metrics for AI performance',
            'check': 'Check that all required tools are installed'
        }

        return descriptions.get(command, f'Execute {command} command')

    def _get_urgency_level(self, command: str, context: SuggestionContext) -> str:
        """Get urgency level for command."""
        metadata = self.command_metadata[command]

        # High urgency for critical path commands
        if metadata['category'] == SuggestionCategory.GOAL_MANAGEMENT:
            if context.project_phase in ['setup', 'planning']:
                return 'high'

        # Medium urgency for progress tracking
        if metadata['category'] == SuggestionCategory.PROGRESS_TRACKING:
            return 'normal'

        # Low urgency for analysis and learning
        if metadata['category'] in [SuggestionCategory.PROJECT_ANALYSIS, SuggestionCategory.LEARNING]:
            return 'low'

        return 'normal'

    def _get_complexity_score(self, complexity: str) -> float:
        """Get numeric score for complexity."""
        scores = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.9
        }
        return scores.get(complexity, 0.5)

    def get_command_suggestions_for_category(self, category: SuggestionCategory,
                                           context: SuggestionContext, limit: int = 3) -> List[CommandSuggestion]:
        """Get command suggestions for a specific category."""
        suggestions = []

        for command, metadata in self.command_metadata.items():
            if metadata['category'] == category:
                suggestion = self._create_suggestion(command, f"work with {category.value}", context, 'category_match')
                suggestions.append(suggestion)

        # Sort by context relevance and limit
        suggestions.sort(key=lambda x: x.confidence_score, reverse=True)
        return suggestions[:limit]

    def update_command_metadata(self, command: str, updates: Dict[str, Any]) -> None:
        """Update metadata for a command."""
        if command in self.command_metadata:
            self.command_metadata[command].update(updates)
            # Clear pattern cache since metadata changed
            self.pattern_cache.clear()

    def get_available_commands_by_category(self) -> Dict[SuggestionCategory, List[str]]:
        """Get available commands organized by category."""
        commands_by_category = {}

        for command, metadata in self.command_metadata.items():
            category = metadata['category']
            if category not in commands_by_category:
                commands_by_category[category] = []
            commands_by_category[category].append(command)

        return commands_by_category

    def find_command_sequences(self, start_command: str, max_length: int = 3) -> List[List[str]]:
        """Find common command sequences starting with a command."""
        sequences = []

        # This is a simplified implementation
        # In practice, this would analyze historical command sequences

        common_sequences = {
            'vision': ['goal', 'strategies'],
            'goal': ['strategies', 'milestones'],
            'strategies': ['milestones', 'tasks'],
            'milestones': ['tasks', 'progress'],
            'progress': ['analytics', 'validate'],
            'analyze': ['insights', 'validate'],
            'validate': ['progress', 'learn']
        }

        if start_command in common_sequences:
            for next_cmd in common_sequences[start_command]:
                if next_cmd in self.available_commands:
                    sequences.append([start_command, next_cmd])

        return sequences


class SuggestionRankingEngine:
    """Rank and filter suggestions based on multiple factors."""

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.ranking_weights = self._get_default_weights()
        self.ranking_history: List[Dict[str, Any]] = []
        self.feedback_data: Dict[str, Dict[str, float]] = {}

        # Load existing ranking data
        self._load_ranking_data()

    def _get_default_weights(self) -> Dict[str, float]:
        """Get default ranking weights."""
        return {
            'confidence_score': 0.25,
            'context_relevance': 0.20,
            'usage_frequency': 0.15,
            'user_feedback': 0.15,
            'category_balance': 0.10,
            'urgency': 0.08,
            'complexity_fit': 0.07
        }

    def _load_ranking_data(self) -> None:
        """Load existing ranking data."""
        ranking_file = self.project_path / ".goalkit" / "ranking_data.json"

        if ranking_file.exists():
            try:
                with open(ranking_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                self.ranking_history = data.get('ranking_history', [])
                self.feedback_data = data.get('feedback_data', {})

            except Exception as e:
                logger.warning(f"Failed to load ranking data: {e}")

    def _save_ranking_data(self) -> None:
        """Save ranking data."""
        ranking_file = self.project_path / ".goalkit" / "ranking_data.json"

        try:
            ranking_file.parent.mkdir(parents=True, exist_ok=True)

            data = {
                'ranking_history': self.ranking_history,
                'feedback_data': self.feedback_data,
                'last_updated': datetime.now().isoformat()
            }

            with open(ranking_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Failed to save ranking data: {e}")

    def rank_suggestions(self, suggestions: List[CommandSuggestion],
                        context: SuggestionContext) -> List[CommandSuggestion]:
        """Rank suggestions using multiple factors."""
        if not suggestions:
            return suggestions

        # Calculate ranking scores for each suggestion
        ranked_suggestions = []
        for suggestion in suggestions:
            ranking_score = self._calculate_ranking_score(suggestion, context)
            suggestion.confidence_score = ranking_score  # Update confidence with ranking score
            suggestion._update_confidence_level()
            ranked_suggestions.append(suggestion)

        # Sort by ranking score
        ranked_suggestions.sort(key=lambda x: x.confidence_score, reverse=True)

        # Apply diversity and balance
        balanced_suggestions = self._apply_category_balance(ranked_suggestions, context)

        # Filter based on thresholds
        filtered_suggestions = self._apply_thresholds(balanced_suggestions)

        # Store ranking decision for learning
        self._store_ranking_decision(suggestions, filtered_suggestions, context)

        return filtered_suggestions

    def _calculate_ranking_score(self, suggestion: CommandSuggestion,
                               context: SuggestionContext) -> float:
        """Calculate comprehensive ranking score."""
        scores = {}

        # Base confidence score
        scores['confidence_score'] = suggestion.confidence_score

        # Context relevance score
        scores['context_relevance'] = context.get_context_relevance_score(suggestion.category)

        # Usage frequency score
        scores['usage_frequency'] = self._calculate_usage_frequency_score(suggestion, context)

        # User feedback score
        scores['user_feedback'] = self._calculate_user_feedback_score(suggestion)

        # Category balance score
        scores['category_balance'] = self._calculate_category_balance_score(suggestion, context)

        # Urgency score
        scores['urgency'] = self._calculate_urgency_score(suggestion)

        # Complexity fit score
        scores['complexity_fit'] = self._calculate_complexity_fit_score(suggestion, context)

        # Calculate weighted score
        weighted_score = sum(
            scores[factor] * weight
            for factor, weight in self.ranking_weights.items()
        )

        return min(1.0, max(0.0, weighted_score))

    def _calculate_usage_frequency_score(self, suggestion: CommandSuggestion,
                                       context: SuggestionContext) -> float:
        """Calculate score based on usage frequency."""
        # Check if there's a usage pattern for this command
        pattern = context.get_command_pattern(suggestion.command)

        if pattern:
            # Use pattern's frequency score
            frequency_score = pattern.get_usage_frequency_score()

            # Boost score for successful commands
            success_score = pattern.get_success_score()
            combined_score = (frequency_score + success_score) / 2.0

            return min(1.0, combined_score + 0.2)  # Slight boost for known commands
        else:
            # New command - moderate score
            return 0.5

    def _calculate_user_feedback_score(self, suggestion: CommandSuggestion) -> float:
        """Calculate score based on user feedback."""
        if suggestion.user_feedback_score is not None:
            # Convert -1..1 range to 0..1 range
            return (suggestion.user_feedback_score + 1.0) / 2.0

        # Check historical feedback for this command
        command_feedback = self.feedback_data.get(suggestion.command, {})
        if command_feedback:
            avg_feedback = sum(command_feedback.values()) / len(command_feedback)
            return (avg_feedback + 1.0) / 2.0

        # No feedback data - neutral score
        return 0.5

    def _calculate_category_balance_score(self, suggestion: CommandSuggestion,
                                        context: SuggestionContext) -> float:
        """Calculate score based on category balance."""
        # Analyze recent command categories
        if not context.recent_commands:
            return 0.5

        recent_categories = []
        for cmd in context.recent_commands[-10:]:  # Last 10 commands
            categories = context._command_to_categories(cmd)
            recent_categories.extend(categories)

        # Count category frequency
        category_counts = {}
        for category in recent_categories:
            category_counts[category] = category_counts.get(category, 0) + 1

        # Calculate diversity score
        total_commands = len(recent_categories)
        if total_commands == 0:
            return 0.5

        # Higher score for underrepresented categories
        suggestion_category = suggestion.category.value
        category_frequency = category_counts.get(suggestion_category, 0) / total_commands

        # Invert frequency for balance (less frequent = higher score)
        balance_score = 1.0 - category_frequency

        return min(1.0, balance_score + 0.2)  # Ensure minimum score

    def _calculate_urgency_score(self, suggestion: CommandSuggestion) -> float:
        """Calculate score based on urgency."""
        urgency_scores = {
            'low': 0.3,
            'normal': 0.6,
            'high': 0.8,
            'critical': 1.0
        }

        return urgency_scores.get(suggestion.urgency_level, 0.6)

    def _calculate_complexity_fit_score(self, suggestion: CommandSuggestion,
                                      context: SuggestionContext) -> float:
        """Calculate score based on complexity fit with user preferences."""
        # This is a simplified implementation
        # In practice, this would analyze user's historical preference for command complexity

        # For now, assume moderate complexity preference
        complexity_scores = {
            'low': 0.7,
            'medium': 0.8,
            'high': 0.6
        }

        # Get complexity from command metadata (simplified)
        metadata = context._get_command_metadata(suggestion.command)
        complexity = metadata.get('complexity', 'medium')

        return complexity_scores.get(complexity, 0.7)

    def _apply_category_balance(self, suggestions: List[CommandSuggestion],
                              context: SuggestionContext) -> List[CommandSuggestion]:
        """Apply category balance to avoid over-representing one category."""
        if len(suggestions) <= 3:
            return suggestions

        # Count categories in top suggestions
        category_count = {}
        for suggestion in suggestions[:5]:  # Consider top 5
            category = suggestion.category
            category_count[category] = category_count.get(category, 0) + 1

        # If one category dominates, boost diversity
        max_category = max(category_count.items(), key=lambda x: x[1])
        if max_category[1] >= 3:  # If one category has 3+ suggestions in top 5
            # Demote some suggestions from the dominant category
            balanced_suggestions = []
            dominant_category = max_category[0]

            for suggestion in suggestions:
                if suggestion.category == dominant_category and category_count[dominant_category] > 2:
                    # Reduce score for additional suggestions from dominant category
                    suggestion.confidence_score *= 0.8
                    suggestion._update_confidence_level()
                    category_count[dominant_category] -= 1

                balanced_suggestions.append(suggestion)

            return sorted(balanced_suggestions, key=lambda x: x.confidence_score, reverse=True)

        return suggestions

    def _apply_thresholds(self, suggestions: List[CommandSuggestion]) -> List[CommandSuggestion]:
        """Apply ranking thresholds to filter low-quality suggestions."""
        if not suggestions:
            return suggestions

        # Minimum confidence threshold
        min_confidence = 0.3

        # Filter suggestions above threshold
        filtered = [s for s in suggestions if s.confidence_score >= min_confidence]

        # If no suggestions pass threshold, include the top one
        if not filtered and suggestions:
            filtered = [suggestions[0]]

        return filtered

    def _store_ranking_decision(self, original_suggestions: List[CommandSuggestion],
                              ranked_suggestions: List[CommandSuggestion],
                              context: SuggestionContext) -> None:
        """Store ranking decision for learning."""
        decision = {
            'timestamp': datetime.now().isoformat(),
            'context_phase': context.project_phase,
            'original_count': len(original_suggestions),
            'ranked_count': len(ranked_suggestions),
            'top_suggestions': [
                {
                    'command': s.command,
                    'category': s.category.value,
                    'confidence': s.confidence_score,
                    'rank': i + 1
                }
                for i, s in enumerate(ranked_suggestions[:3])  # Store top 3
            ]
        }

        self.ranking_history.append(decision)

        # Keep only recent history (last 100 decisions)
        if len(self.ranking_history) > 100:
            self.ranking_history = self.ranking_history[-100:]

        self._save_ranking_data()

    def record_suggestion_feedback(self, suggestion: CommandSuggestion,
                                 was_helpful: bool, context: SuggestionContext) -> None:
        """Record feedback on suggestion helpfulness."""
        feedback_key = f"{suggestion.command}_{context.project_phase}"

        if feedback_key not in self.feedback_data:
            self.feedback_data[feedback_key] = {
                'helpful_count': 0,
                'total_count': 0,
                'avg_confidence': 0.0
            }

        feedback = self.feedback_data[feedback_key]
        feedback['total_count'] += 1

        if was_helpful:
            feedback['helpful_count'] += 1

        # Update average confidence for helpful suggestions
        if was_helpful:
            alpha = 0.1  # Learning rate
            feedback['avg_confidence'] = (
                (1 - alpha) * feedback['avg_confidence'] + alpha * suggestion.confidence_score
            )

        # Update suggestion's own feedback score
        current_feedback = suggestion.user_feedback_score or 0.0
        alpha = 0.2
        new_feedback = (1 - alpha) * current_feedback + alpha * (1.0 if was_helpful else -1.0)
        suggestion.set_user_feedback(new_feedback)

        self._save_ranking_data()

    def get_ranking_insights(self) -> Dict[str, Any]:
        """Get insights about ranking performance."""
        if not self.ranking_history:
            return {
                'message': 'No ranking history available',
                'total_decisions': 0,
                'avg_suggestions_per_decision': 0,
                'category_distribution': {},
                'feedback_effectiveness': {},
                'ranking_trends': []
            }

        insights = {
            'total_decisions': len(self.ranking_history),
            'avg_suggestions_per_decision': 0,
            'category_distribution': {},
            'feedback_effectiveness': {},
            'ranking_trends': []
        }

        # Calculate averages
        total_suggestions = sum(decision['ranked_count'] for decision in self.ranking_history)
        insights['avg_suggestions_per_decision'] = total_suggestions / len(self.ranking_history)

        # Category distribution
        for decision in self.ranking_history:
            for suggestion in decision['top_suggestions']:
                category = suggestion['category']
                insights['category_distribution'][category] = (
                    insights['category_distribution'].get(category, 0) + 1
                )

        # Feedback effectiveness (based on stored feedback)
        for command_phase, feedback in self.feedback_data.items():
            if feedback['total_count'] > 0:
                success_rate = feedback['helpful_count'] / feedback['total_count']
                insights['feedback_effectiveness'][command_phase] = {
                    'success_rate': success_rate,
                    'avg_confidence': feedback['avg_confidence']
                }

        # Recent trends (last 10 decisions)
        recent_decisions = self.ranking_history[-10:]
        for decision in recent_decisions:
            insights['ranking_trends'].append({
                'phase': decision['context_phase'],
                'suggestion_count': decision['ranked_count'],
                'top_category': decision['top_suggestions'][0]['category'] if decision['top_suggestions'] else 'none'
            })

        return insights

    def adjust_ranking_weights(self, new_weights: Dict[str, float]) -> None:
        """Adjust ranking weights based on performance."""
        if not new_weights:
            return

        # Normalize weights to sum to 1.0
        total_weight = sum(new_weights.values())
        if total_weight > 0:
            for factor in self.ranking_weights:
                if factor in new_weights:
                    self.ranking_weights[factor] = new_weights[factor] / total_weight

        logger.info(f"Updated ranking weights: {self.ranking_weights}")

    def get_personalized_weights(self, context: SuggestionContext) -> Dict[str, float]:
        """Get personalized ranking weights based on user behavior."""
        personalized_weights = self.ranking_weights.copy()

        # Adjust based on project phase
        if context.project_phase == 'planning':
            personalized_weights['context_relevance'] += 0.05
            personalized_weights['category_balance'] += 0.05
        elif context.project_phase == 'execution':
            personalized_weights['usage_frequency'] += 0.05
            personalized_weights['urgency'] += 0.05
        elif context.project_phase == 'review':
            personalized_weights['user_feedback'] += 0.05
            personalized_weights['confidence_score'] += 0.05

        # Adjust based on recent activity
        if context.recent_commands:
            # If user has been using many different commands, boost diversity
            unique_commands = len(set(context.recent_commands))
            if unique_commands > 5:
                personalized_weights['category_balance'] += 0.1

            # If user has been focused on one area, boost relevance
            if unique_commands < 3:
                personalized_weights['context_relevance'] += 0.1

        # Normalize weights
        total_weight = sum(personalized_weights.values())
        for factor in personalized_weights:
            personalized_weights[factor] /= total_weight

        return personalized_weights

    def filter_suggestions_by_context(self, suggestions: List[CommandSuggestion],
                                    context: SuggestionContext) -> List[CommandSuggestion]:
        """Filter suggestions based on current context."""
        filtered_suggestions = []

        for suggestion in suggestions:
            # Check project phase compatibility
            if not self._is_compatible_with_phase(suggestion, context.project_phase):
                continue

            # Check command availability
            if suggestion.command not in context.available_commands:
                continue

            # Check for command conflicts
            if self._has_command_conflicts(suggestion, context):
                continue

            filtered_suggestions.append(suggestion)

        return filtered_suggestions

    def _is_compatible_with_phase(self, suggestion: CommandSuggestion, phase: str) -> bool:
        """Check if suggestion is compatible with project phase."""
        if phase == 'unknown':
            return True

        # Define phase compatibility
        phase_compatibility = {
            'setup': [SuggestionCategory.GOAL_MANAGEMENT],
            'planning': [SuggestionCategory.GOAL_MANAGEMENT, SuggestionCategory.PLANNING],
            'execution': [SuggestionCategory.PLANNING, SuggestionCategory.PROGRESS_TRACKING, SuggestionCategory.AUTOMATION],
            'review': [SuggestionCategory.PROJECT_ANALYSIS, SuggestionCategory.VALIDATION, SuggestionCategory.LEARNING]
        }

        phase = phase.lower()
        compatible_categories = phase_compatibility.get(phase, [])

        return suggestion.category in compatible_categories

    def _has_command_conflicts(self, suggestion: CommandSuggestion,
                             context: SuggestionContext) -> bool:
        """Check if suggestion conflicts with recent commands."""
        # Avoid suggesting the same command repeatedly
        if (context.recent_commands and
            context.recent_commands[-1] == suggestion.command):
            return True

        # Avoid suggesting conflicting commands
        conflicting_commands = {
            'init': ['validate', 'analyze'],  # Don't analyze before init
            'validate': ['init'],  # Don't init after validation
        }

        recent_cmd = context.recent_commands[-1] if context.recent_commands else None
        if (recent_cmd in conflicting_commands and
            suggestion.command in conflicting_commands[recent_cmd]):
            return True

        return False

    def get_suggestion_explanations(self, suggestions: List[CommandSuggestion]) -> Dict[str, str]:
        """Get explanations for why suggestions were ranked as they were."""
        explanations = {}

        for suggestion in suggestions:
            explanation_parts = []

            # Confidence explanation
            if suggestion.confidence_score > 0.8:
                explanation_parts.append("High confidence match")
            elif suggestion.confidence_score > 0.6:
                explanation_parts.append("Good contextual fit")
            else:
                explanation_parts.append("Basic relevance match")

            # Context explanation
            if suggestion.context_factors.get('context_relevance', 0) > 0.7:
                explanation_parts.append("Highly relevant to current project phase")

            # Usage explanation
            if suggestion.context_factors.get('usage_frequency', 0) > 0.7:
                explanation_parts.append("Frequently used command")

            # Category explanation
            if suggestion.context_factors.get('category_balance', 0) > 0.7:
                explanation_parts.append("Provides category diversity")

            explanations[suggestion.command] = " • ".join(explanation_parts)

        return explanations


class ContextAwareCommandRecommender:
    """Main recommendation engine with intelligent scoring."""

    def __init__(self, project_path: Path, available_commands: List[str]):
        self.project_path = Path(project_path)
        self.available_commands = set(available_commands)

        # Initialize components
        self.intent_analyzer = UserIntentAnalyzer(project_path)
        self.pattern_matcher = CommandPatternMatcher(available_commands)
        self.ranking_engine = SuggestionRankingEngine(project_path)

        # Recommendation cache
        self.recommendation_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_ttl_minutes = 30

        # Performance tracking
        self.performance_stats = {
            'total_recommendations': 0,
            'cache_hits': 0,
            'avg_response_time_ms': 0,
            'user_satisfaction_score': 0.0
        }

        logger.info(f"ContextAwareCommandRecommender initialized for project: {project_path}")

    def get_command_suggestions(self, user_input: str, context: SuggestionContext,
                              max_suggestions: int = 5) -> List[CommandSuggestion]:
        """Get intelligent command suggestions based on user input and context."""
        import time

        start_time = time.time()

        try:
            # Check cache first
            cache_key = self._generate_cache_key(user_input, context)
            cached_result = self._get_cached_recommendation(cache_key)

            if cached_result:
                self.performance_stats['cache_hits'] += 1
                return cached_result['suggestions']

            # Analyze user intent
            intent_analysis = self.intent_analyzer.analyze_command_sequence(
                [user_input] if user_input else [], context
            )

            # Generate candidate suggestions
            candidate_suggestions = self._generate_candidate_suggestions(
                user_input, context, intent_analysis
            )

            if not candidate_suggestions:
                # Fallback to context-based suggestions
                candidate_suggestions = self._generate_fallback_suggestions(context)

            # Rank and filter suggestions
            ranked_suggestions = self.ranking_engine.rank_suggestions(candidate_suggestions, context)

            # Limit results
            final_suggestions = ranked_suggestions[:max_suggestions]

            # Cache the result
            self._cache_recommendation(cache_key, {
                'suggestions': final_suggestions,
                'intent_analysis': intent_analysis,
                'timestamp': datetime.now()
            })

            # Update performance stats
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            self._update_performance_stats(response_time)

            self.performance_stats['total_recommendations'] += 1

            return final_suggestions

        except Exception as e:
            logger.error(f"Error generating command suggestions: {e}")
            # Return fallback suggestions on error
            return self._generate_fallback_suggestions(context)

    def _generate_cache_key(self, user_input: str, context: SuggestionContext) -> str:
        """Generate cache key for recommendations."""
        import hashlib

        # Create a hash of the key components
        key_components = [
            user_input or "",
            context.project_phase,
            str(context.current_goal or ""),
            str(len(context.recent_commands)),
            context.time_of_day
        ]

        key_string = "|".join(key_components)
        return hashlib.sha256(key_string.encode()).hexdigest()

    def _get_cached_recommendation(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached recommendation if still valid."""
        if cache_key not in self.recommendation_cache:
            return None

        cached = self.recommendation_cache[cache_key]
        cache_age_minutes = (datetime.now() - cached['timestamp']).total_seconds() / 60

        if cache_age_minutes > self.cache_ttl_minutes:
            # Cache expired
            del self.recommendation_cache[cache_key]
            return None

        return cached

    def _cache_recommendation(self, cache_key: str, recommendation: Dict[str, Any]) -> None:
        """Cache recommendation result."""
        self.recommendation_cache[cache_key] = recommendation

        # Limit cache size
        if len(self.recommendation_cache) > 100:
            # Remove oldest entries (simple LRU)
            oldest_keys = sorted(
                self.recommendation_cache.keys(),
                key=lambda k: self.recommendation_cache[k]['timestamp']
            )[:50]
            for key in oldest_keys:
                del self.recommendation_cache[key]

    def _generate_candidate_suggestions(self, user_input: str, context: SuggestionContext,
                                      intent_analysis: Dict[str, Any]) -> List[CommandSuggestion]:
        """Generate candidate suggestions based on input and analysis."""
        candidates = []

        # Pattern-based suggestions
        if user_input:
            pattern_suggestions = self.pattern_matcher.match_intent_to_commands(
                user_input, context, limit=8
            )
            candidates.extend(pattern_suggestions)

        # Intent-based suggestions
        intent_signals = intent_analysis.get('intent_signals', [])
        for signal in intent_signals:
            if signal.signal_type in ['workflow_goal_creation', 'workflow_analysis']:
                # Generate workflow-specific suggestions
                workflow_suggestions = self._generate_workflow_suggestions(signal, context)
                candidates.extend(workflow_suggestions)

        # Context-based suggestions
        context_suggestions = self._generate_context_suggestions(context)
        candidates.extend(context_suggestions)

        # Remove duplicates while preserving order
        seen_commands = set()
        unique_candidates = []
        for candidate in candidates:
            if candidate.command not in seen_commands:
                seen_commands.add(candidate.command)
                unique_candidates.append(candidate)

        return unique_candidates

    def _generate_workflow_suggestions(self, intent_signal: UserIntentSignal,
                                     context: SuggestionContext) -> List[CommandSuggestion]:
        """Generate suggestions based on detected workflow."""
        suggestions = []

        signal_value = intent_signal.signal_value

        if signal_value == 'creating_new_goal':
            # Goal creation workflow
            workflow_commands = ['vision', 'goal', 'strategies', 'milestones']
            for cmd in workflow_commands:
                if cmd in self.available_commands:
                    suggestion = CommandSuggestion(
                        command=cmd,
                        description=f"Continue with {cmd} to build your goal",
                        category=SuggestionCategory.GOAL_MANAGEMENT,
                        confidence_score=0.8,
                        reasoning=[f"Part of goal creation workflow detected from {intent_signal.signal_type}"],
                        project_phase=context.project_phase
                    )
                    suggestions.append(suggestion)

        elif signal_value == 'project_analysis':
            # Analysis workflow
            analysis_commands = ['analyze', 'insights', 'validate', 'benchmark']
            for cmd in analysis_commands:
                if cmd in self.available_commands:
                    suggestion = CommandSuggestion(
                        command=cmd,
                        description=f"Use {cmd} for project analysis",
                        category=SuggestionCategory.PROJECT_ANALYSIS,
                        confidence_score=0.7,
                        reasoning=["Part of analysis workflow detected"],
                        project_phase=context.project_phase
                    )
                    suggestions.append(suggestion)

        return suggestions

    def _generate_context_suggestions(self, context: SuggestionContext) -> List[CommandSuggestion]:
        """Generate suggestions based on current context."""
        suggestions = []

        # Project phase-based suggestions
        if context.project_phase != 'unknown':
            phase_suggestions = self._get_phase_based_suggestions(context.project_phase)
            suggestions.extend(phase_suggestions)

        # Goal-based suggestions
        if context.current_goal:
            goal_suggestions = self._get_goal_based_suggestions(context.current_goal, context)
            suggestions.extend(goal_suggestions)

        # Time-based suggestions
        time_suggestions = self._get_time_based_suggestions(context)
        suggestions.extend(time_suggestions)

        # Usage pattern-based suggestions
        pattern_suggestions = self._get_pattern_based_suggestions(context)
        suggestions.extend(pattern_suggestions)

        return suggestions

    def _get_phase_based_suggestions(self, phase: str) -> List[CommandSuggestion]:
        """Get suggestions based on project phase."""
        suggestions = []

        phase_command_map = {
            'setup': [
                ('init', 'Initialize your Goalkeeper project', SuggestionCategory.GOAL_MANAGEMENT, 0.9),
                ('vision', 'Define your project vision', SuggestionCategory.GOAL_MANAGEMENT, 0.8)
            ],
            'planning': [
                ('goal', 'Define specific goals', SuggestionCategory.GOAL_MANAGEMENT, 0.9),
                ('strategies', 'Explore implementation strategies', SuggestionCategory.PLANNING, 0.8),
                ('milestones', 'Create measurable milestones', SuggestionCategory.PLANNING, 0.7)
            ],
            'execution': [
                ('tasks', 'Create actionable tasks', SuggestionCategory.PLANNING, 0.9),
                ('progress', 'Track your progress', SuggestionCategory.PROGRESS_TRACKING, 0.8),
                ('validate', 'Validate your work', SuggestionCategory.VALIDATION, 0.7)
            ],
            'review': [
                ('analytics', 'Analyze project performance', SuggestionCategory.PROJECT_ANALYSIS, 0.9),
                ('insights', 'Get AI-powered insights', SuggestionCategory.PROJECT_ANALYSIS, 0.8),
                ('learn', 'Extract lessons learned', SuggestionCategory.LEARNING, 0.7)
            ]
        }

        phase = phase.lower()
        if phase in phase_command_map:
            for command, description, category, confidence in phase_command_map[phase]:
                if command in self.available_commands:
                    suggestion = CommandSuggestion(
                        command=command,
                        description=description,
                        category=category,
                        confidence_score=confidence,
                        reasoning=[f"Recommended for {phase} phase"],
                        project_phase=phase
                    )
                    suggestions.append(suggestion)

        return suggestions

    def _get_goal_based_suggestions(self, current_goal: str,
                                  context: SuggestionContext) -> List[CommandSuggestion]:
        """Get suggestions based on current goal."""
        suggestions = []

        goal_commands = [
            ('milestones', 'Create milestones for your goal', SuggestionCategory.PLANNING, 0.8),
            ('tasks', 'Break down into actionable tasks', SuggestionCategory.PLANNING, 0.8),
            ('progress', 'Track goal progress', SuggestionCategory.PROGRESS_TRACKING, 0.7),
            ('validate', 'Validate goal achievement', SuggestionCategory.VALIDATION, 0.7)
        ]

        for command, description, category, confidence in goal_commands:
            if command in self.available_commands:
                suggestion = CommandSuggestion(
                    command=command,
                    description=description,
                    category=category,
                    confidence_score=confidence,
                    reasoning=[f"Relevant to current goal: {current_goal}"],
                    project_phase=context.project_phase,
                    goal_context=[current_goal]
                )
                suggestions.append(suggestion)

        return suggestions

    def _get_time_based_suggestions(self, context: SuggestionContext) -> List[CommandSuggestion]:
        """Get suggestions based on time of day."""
        suggestions = []

        if not hasattr(context, 'time_of_day') or not context.time_of_day:
            return suggestions

        time_of_day = context.time_of_day.lower()

        if time_of_day in ['morning', 'early']:
            # Morning - planning and setup
            morning_commands = [
                ('vision', 'Start with project vision', SuggestionCategory.GOAL_MANAGEMENT, 0.7),
                ('goal', 'Define morning objectives', SuggestionCategory.GOAL_MANAGEMENT, 0.7),
                ('plan', 'Plan your day', SuggestionCategory.PLANNING, 0.6)
            ]

            for command, description, category, confidence in morning_commands:
                if command in self.available_commands:
                    suggestion = CommandSuggestion(
                        command=command,
                        description=description,
                        category=category,
                        confidence_score=confidence,
                        reasoning=[f"Suitable for {time_of_day} timing"],
                        project_phase=context.project_phase
                    )
                    suggestions.append(suggestion)

        elif time_of_day in ['evening', 'night']:
            # Evening - review and reflection
            evening_commands = [
                ('progress', 'Review day\'s progress', SuggestionCategory.PROGRESS_TRACKING, 0.7),
                ('analytics', 'Analyze performance', SuggestionCategory.PROJECT_ANALYSIS, 0.7),
                ('learn', 'Reflect on learnings', SuggestionCategory.LEARNING, 0.6)
            ]

            for command, description, category, confidence in evening_commands:
                if command in self.available_commands:
                    suggestion = CommandSuggestion(
                        command=command,
                        description=description,
                        category=category,
                        confidence_score=confidence,
                        reasoning=[f"Suitable for {time_of_day} reflection"],
                        project_phase=context.project_phase
                    )
                    suggestions.append(suggestion)

        return suggestions

    def _get_pattern_based_suggestions(self, context: SuggestionContext) -> List[CommandSuggestion]:
        """Get suggestions based on usage patterns."""
        suggestions = []

        # Analyze recent command patterns
        if context.recent_commands:
            recent_cmd = context.recent_commands[-1]

            # Get command pattern
            pattern = context.get_command_pattern(recent_cmd)
            if pattern and pattern.co_occurring_commands:
                # Suggest frequently co-occurring commands
                for co_cmd, frequency in pattern.co_occurring_commands.items():
                    if co_cmd in self.available_commands and co_cmd != recent_cmd:
                        suggestion = CommandSuggestion(
                            command=co_cmd,
                            description=f"Often used with {recent_cmd}",
                            category=SuggestionCategory.GOAL_MANAGEMENT,  # Default category
                            confidence_score=min(0.8, frequency / 10.0),
                            reasoning=[f"Frequently co-occurs with {recent_cmd}"],
                            project_phase=context.project_phase
                        )
                        suggestions.append(suggestion)

        return suggestions

    def _generate_fallback_suggestions(self, context: SuggestionContext) -> List[CommandSuggestion]:
        """Generate fallback suggestions when no specific matches found."""
        suggestions = []

        # Default helpful commands based on project phase
        fallback_commands = []

        if context.project_phase == 'unknown':
            # General helpful commands for new projects
            fallback_commands = [
                ('init', 'Initialize your project', SuggestionCategory.GOAL_MANAGEMENT, 0.6),
                ('vision', 'Define project vision', SuggestionCategory.GOAL_MANAGEMENT, 0.5),
                ('analyze', 'Analyze current state', SuggestionCategory.PROJECT_ANALYSIS, 0.4)
            ]
        else:
            # Phase-specific fallbacks
            phase_fallbacks = {
                'setup': [('init', 'Initialize project', SuggestionCategory.GOAL_MANAGEMENT, 0.7)],
                'planning': [('goal', 'Define goals', SuggestionCategory.GOAL_MANAGEMENT, 0.7)],
                'execution': [('progress', 'Track progress', SuggestionCategory.PROGRESS_TRACKING, 0.7)],
                'review': [('analytics', 'Review performance', SuggestionCategory.PROJECT_ANALYSIS, 0.7)]
            }

            fallback_commands = phase_fallbacks.get(context.project_phase.lower(),
                                                   [('analyze', 'Analyze project', SuggestionCategory.PROJECT_ANALYSIS, 0.5)])

        for command, description, category, confidence in fallback_commands:
            if command in self.available_commands:
                suggestion = CommandSuggestion(
                    command=command,
                    description=description,
                    category=category,
                    confidence_score=confidence,
                    reasoning=['Fallback suggestion based on project context'],
                    project_phase=context.project_phase
                )
                suggestions.append(suggestion)

        return suggestions

    def _update_performance_stats(self, response_time_ms: float) -> None:
        """Update performance statistics."""
        # Update average response time (exponential moving average)
        alpha = 0.1
        current_avg = self.performance_stats['avg_response_time_ms']
        self.performance_stats['avg_response_time_ms'] = (
            (1 - alpha) * current_avg + alpha * response_time_ms
        )

    def learn_from_user_interaction(self, user_input: str, selected_suggestion: CommandSuggestion,
                                  was_helpful: bool, context: SuggestionContext) -> None:
        """Learn from user interaction with suggestions."""
        # Update intent analyzer
        self.intent_analyzer.learn_from_feedback(
            [user_input] if user_input else [], selected_suggestion, was_helpful, context
        )

        # Update ranking engine
        self.ranking_engine.record_suggestion_feedback(selected_suggestion, was_helpful, context)

        # Update context with new command
        context.update_command_pattern(
            selected_suggestion.command, was_helpful,
            selected_suggestion.confidence_score, context.project_phase
        )

        # Clear cache to ensure fresh recommendations
        self.recommendation_cache.clear()

        logger.info(f"Learned from interaction: {selected_suggestion.command} was {'helpful' if was_helpful else 'not helpful'}")

    def get_recommendation_insights(self) -> Dict[str, Any]:
        """Get insights about recommendation performance."""
        insights = {
            'performance_stats': self.performance_stats,
            'cache_info': {
                'cache_size': len(self.recommendation_cache),
                'ttl_minutes': self.cache_ttl_minutes
            },
            'ranking_insights': self.ranking_engine.get_ranking_insights(),
            'intent_insights': self.intent_analyzer.get_user_preferences(),
            'available_commands': len(self.available_commands)
        }

        return insights

    def clear_cache(self) -> None:
        """Clear recommendation cache."""
        self.recommendation_cache.clear()
        logger.info("Recommendation cache cleared")

    def export_recommendation_data(self) -> Dict[str, Any]:
        """Export recommendation data for analysis."""
        return {
            'performance_stats': self.performance_stats,
            'cache_info': {
                'size': len(self.recommendation_cache),
                'ttl': self.cache_ttl_minutes
            },
            'ranking_data': self.ranking_engine.get_ranking_insights(),
            'intent_data': self.intent_analyzer.export_learning_data(),
            'exported_at': datetime.now().isoformat()
        }

    def get_suggestions_for_category(self, category: SuggestionCategory,
                                   context: SuggestionContext, limit: int = 3) -> List[CommandSuggestion]:
        """Get suggestions for a specific category."""
        # Generate category-specific input
        category_intent = f"work with {category.value}"

        # Get suggestions using pattern matcher
        suggestions = self.pattern_matcher.get_command_suggestions_for_category(category, context, limit)

        # Rank the suggestions
        ranked_suggestions = self.ranking_engine.rank_suggestions(suggestions, context)

        return ranked_suggestions[:limit]

    def get_next_steps_suggestions(self, current_command: str,
                                 context: SuggestionContext) -> List[CommandSuggestion]:
        """Get next step suggestions after a command."""
        suggestions = []

        # Find command sequences
        sequences = self.pattern_matcher.find_command_sequences(current_command)

        for sequence in sequences:
            if len(sequence) > 1:
                next_cmd = sequence[1]
                if next_cmd in self.available_commands:
                    suggestion = CommandSuggestion(
                        command=next_cmd,
                        description=f"Next step after {current_command}",
                        category=SuggestionCategory.GOAL_MANAGEMENT,  # Default
                        confidence_score=0.7,
                        reasoning=[f"Commonly follows {current_command} in workflows"],
                        project_phase=context.project_phase
                    )
                    suggestions.append(suggestion)

        # Rank suggestions
        ranked_suggestions = self.ranking_engine.rank_suggestions(suggestions, context)

        return ranked_suggestions

    def get_display_text(self) -> str:
        """Get formatted display text for the suggestion."""
        confidence_indicator = self._get_confidence_indicator()
        category_indicator = f"[{self.category.value.upper()}]"

        text = f"{confidence_indicator} {self.command} - {self.description} {category_indicator}"

        if self.confidence_score < 0.5:
            text += f" (confidence: {self.confidence_score:.1%})"

        return text

    def _get_confidence_indicator(self) -> str:
        """Get visual confidence indicator."""
        indicators = {
            ConfidenceLevel.VERY_HIGH: "🔥",
            ConfidenceLevel.HIGH: "⭐",
            ConfidenceLevel.MEDIUM: "●",
            ConfidenceLevel.LOW: "○",
            ConfidenceLevel.VERY_LOW: "○"
        }
        return indicators.get(self.confidence_level, "○")

    def is_similar_to(self, other: 'CommandSuggestion') -> bool:
        """Check if this suggestion is similar to another."""
        # Same command
        if self.command == other.command:
            return True

        # Same category and similar description
        if (self.category == other.category and
            self._calculate_text_similarity(self.description, other.description) > 0.7):
            return True

        # Related commands
        if (self.command in other.related_commands or
            other.command in self.related_commands):
            return True

        return False

    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity (Jaccard similarity of words)."""
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)



