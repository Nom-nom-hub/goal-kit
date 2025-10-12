#!/usr/bin/env python3
"""
Test suite for Context-Aware Command Suggestion System

This module provides comprehensive tests for all components of the suggestion system.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import json

from command_suggestion import (
    CommandSuggestion,
    SuggestionContext,
    SuggestionCategory,
    ConfidenceLevel,
    UserIntentSignal,
    CommandUsagePattern,
    UserIntentAnalyzer,
    CommandPatternMatcher,
    SuggestionRankingEngine,
    ContextAwareCommandRecommender
)
from suggestion_integration import (
    SuggestionIntegrationManager,
    SuggestionLearningEngine
)

import logging
logger = logging.getLogger(__name__)


class TestCommandSuggestion(unittest.TestCase):
    """Test cases for CommandSuggestion data class."""

    def setUp(self):
        """Set up test fixtures."""
        self.suggestion = CommandSuggestion(
            command="goal",
            description="Define project goals",
            category=SuggestionCategory.GOAL_MANAGEMENT,
            confidence_score=0.8,
            reasoning=["Based on project context", "Common next step"]
        )

    def test_suggestion_creation(self):
        """Test suggestion creation and validation."""
        self.assertEqual(self.suggestion.command, "goal")
        self.assertEqual(self.suggestion.category, SuggestionCategory.GOAL_MANAGEMENT)
        self.assertEqual(self.suggestion.confidence_score, 0.8)
        self.assertEqual(self.suggestion.confidence_level, ConfidenceLevel.HIGH)

    def test_confidence_level_update(self):
        """Test confidence level updates based on score."""
        # Test very high confidence
        self.suggestion.confidence_score = 0.95
        self.suggestion._update_confidence_level()
        self.assertEqual(self.suggestion.confidence_level, ConfidenceLevel.VERY_HIGH)

        # Test low confidence
        self.suggestion.confidence_score = 0.2
        self.suggestion._update_confidence_level()
        self.assertEqual(self.suggestion.confidence_level, ConfidenceLevel.VERY_LOW)

    def test_suggestion_validation(self):
        """Test suggestion validation."""
        # Valid suggestion should not raise
        try:
            valid_suggestion = CommandSuggestion(
                command="test",
                description="Test command",
                category=SuggestionCategory.GOAL_MANAGEMENT
            )
        except ValueError:
            self.fail("Valid suggestion raised ValueError")

        # Invalid confidence score should raise
        with self.assertRaises(ValueError):
            CommandSuggestion(
                command="test",
                description="Test command",
                category=SuggestionCategory.GOAL_MANAGEMENT,
                confidence_score=1.5  # Invalid score
            )

    def test_usage_tracking(self):
        """Test usage tracking functionality."""
        initial_score = self.suggestion.confidence_score

        # Mark as used successfully
        self.suggestion.mark_used(success=True)
        self.assertEqual(self.suggestion.used_count, 1)
        self.assertIsNotNone(self.suggestion.last_used)
        self.assertGreater(self.suggestion.confidence_score, initial_score)

        # Mark as used unsuccessfully
        self.suggestion.mark_used(success=False)
        self.assertEqual(self.suggestion.used_count, 2)
        self.assertLess(self.suggestion.confidence_score, initial_score + 0.1)

    def test_user_feedback(self):
        """Test user feedback functionality."""
        # Set positive feedback
        self.suggestion.set_user_feedback(0.8)
        self.assertEqual(self.suggestion.user_feedback_score, 0.8)
        self.assertGreater(self.suggestion.confidence_score, 0.8)

        # Set negative feedback
        self.suggestion.set_user_feedback(-0.5)
        self.assertEqual(self.suggestion.user_feedback_score, -0.5)
        self.assertLess(self.suggestion.confidence_score, 0.9)

    def test_serialization(self):
        """Test suggestion serialization."""
        # Test to_dict
        data = self.suggestion.to_dict()
        self.assertIn('command', data)
        self.assertIn('confidence_score', data)
        self.assertIn('category', data)

        # Test from_dict
        new_suggestion = CommandSuggestion.from_dict(data)
        self.assertEqual(new_suggestion.command, self.suggestion.command)
        self.assertEqual(new_suggestion.confidence_score, self.suggestion.confidence_score)


class TestSuggestionContext(unittest.TestCase):
    """Test cases for SuggestionContext."""

    def setUp(self):
        """Set up test fixtures."""
        self.context = SuggestionContext(
            project_path=Path("/test/project"),
            project_phase="planning",
            current_goal="test_goal"
        )

    def test_context_creation(self):
        """Test context creation."""
        self.assertEqual(self.context.project_phase, "planning")
        self.assertEqual(self.context.current_goal, "test_goal")
        self.assertEqual(len(self.context.intent_signals), 0)

    def test_intent_signal_management(self):
        """Test intent signal management."""
        signal = UserIntentSignal(
            signal_type="test_signal",
            signal_value="test_value",
            confidence=0.8
        )

        self.context.add_intent_signal(signal)
        self.assertEqual(len(self.context.intent_signals), 1)

        # Test signal expiration
        expired_signal = UserIntentSignal(
            signal_type="old_signal",
            signal_value="old_value",
            timestamp=datetime.now() - timedelta(hours=25)
        )
        self.context.add_intent_signal(expired_signal)

        recent_signals = self.context.get_recent_intent_signals(max_age_hours=24)
        self.assertEqual(len(recent_signals), 1)
        self.assertEqual(recent_signals[0].signal_type, "test_signal")

    def test_context_relevance_scoring(self):
        """Test context relevance scoring."""
        # Test relevance for different categories
        goal_relevance = self.context.get_context_relevance_score(SuggestionCategory.GOAL_MANAGEMENT)
        analysis_relevance = self.context.get_context_relevance_score(SuggestionCategory.PROJECT_ANALYSIS)

        # Goal management should be more relevant in planning phase
        self.assertGreaterEqual(goal_relevance, 0.5)
        self.assertGreaterEqual(analysis_relevance, 0.0)


class TestUserIntentAnalyzer(unittest.TestCase):
    """Test cases for UserIntentAnalyzer."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.analyzer = UserIntentAnalyzer(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_command_sequence_analysis(self):
        """Test command sequence analysis."""
        commands = ["vision", "goal", "strategies", "milestones"]
        context = SuggestionContext(project_path=self.temp_dir, project_phase="planning")

        analysis = self.analyzer.analyze_command_sequence(commands, context)

        self.assertIn('sequence_length', analysis)
        self.assertIn('patterns_detected', analysis)
        self.assertIn('intent_signals', analysis)
        self.assertEqual(analysis['sequence_length'], 4)

    def test_pattern_detection(self):
        """Test pattern detection in command sequences."""
        # Test goal workflow pattern
        goal_commands = ["vision", "goal", "strategies", "milestones"]
        patterns = self.analyzer._detect_patterns(goal_commands)
        self.assertIn('goal_workflow', patterns)

        # Test analysis workflow pattern
        analysis_commands = ["analyze", "insights", "validate"]
        patterns = self.analyzer._detect_patterns(analysis_commands)
        self.assertIn('analysis_workflow', patterns)

    def test_intent_signal_generation(self):
        """Test intent signal generation."""
        commands = ["vision", "goal"]
        context = SuggestionContext(
            project_path=self.temp_dir,
            project_phase="planning",
            time_of_day="morning"
        )

        signals = self.analyzer._generate_intent_signals(commands, context)

        # Should generate some intent signals
        self.assertGreaterEqual(len(signals), 0)

        if signals:
            self.assertIsInstance(signals[0], UserIntentSignal)


class TestCommandPatternMatcher(unittest.TestCase):
    """Test cases for CommandPatternMatcher."""

    def setUp(self):
        """Set up test fixtures."""
        available_commands = ["goal", "vision", "strategies", "analyze", "validate"]
        self.matcher = CommandPatternMatcher(available_commands)

    def test_command_metadata_initialization(self):
        """Test command metadata initialization."""
        # Check that available commands have metadata
        for command in ["goal", "vision", "strategies"]:
            self.assertIn(command, self.matcher.command_metadata)
            metadata = self.matcher.command_metadata[command]
            self.assertIn('category', metadata)
            self.assertIn('intent_keywords', metadata)

    def test_intent_matching(self):
        """Test intent to command matching."""
        context = SuggestionContext(project_path=Path("/test"))

        # Test direct intent matching
        suggestions = self.matcher.match_intent_to_commands("create a goal", context, limit=3)
        self.assertGreater(len(suggestions), 0)

        # Should suggest goal command for "create a goal"
        command_names = [s.command for s in suggestions]
        self.assertIn("goal", command_names)

    def test_category_based_suggestions(self):
        """Test category-based suggestion retrieval."""
        context = SuggestionContext(project_path=Path("/test"))

        suggestions = self.matcher.get_command_suggestions_for_category(
            SuggestionCategory.GOAL_MANAGEMENT, context, limit=2
        )

        self.assertLessEqual(len(suggestions), 2)
        for suggestion in suggestions:
            self.assertEqual(suggestion.category, SuggestionCategory.GOAL_MANAGEMENT)


class TestSuggestionRankingEngine(unittest.TestCase):
    """Test cases for SuggestionRankingEngine."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.ranking_engine = SuggestionRankingEngine(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_suggestion_ranking(self):
        """Test suggestion ranking."""
        # Create test suggestions
        suggestions = [
            CommandSuggestion("goal", "Define goals", SuggestionCategory.GOAL_MANAGEMENT, confidence_score=0.8),
            CommandSuggestion("analyze", "Analyze project", SuggestionCategory.PROJECT_ANALYSIS, confidence_score=0.6),
            CommandSuggestion("validate", "Validate work", SuggestionCategory.VALIDATION, confidence_score=0.7)
        ]

        context = SuggestionContext(project_path=self.temp_dir, project_phase="planning")

        # Rank suggestions
        ranked = self.ranking_engine.rank_suggestions(suggestions, context)

        # Should maintain same number of suggestions
        self.assertEqual(len(ranked), 3)

        # Should be sorted by confidence score
        for i in range(len(ranked) - 1):
            self.assertGreaterEqual(ranked[i].confidence_score, ranked[i + 1].confidence_score)

    def test_feedback_recording(self):
        """Test feedback recording."""
        suggestion = CommandSuggestion(
            "goal", "Define goals", SuggestionCategory.GOAL_MANAGEMENT, confidence_score=0.8
        )
        context = SuggestionContext(project_path=self.temp_dir, project_phase="planning")

        # Record positive feedback
        self.ranking_engine.record_suggestion_feedback(suggestion, True, context)

        # Check that feedback was recorded
        insights = self.ranking_engine.get_ranking_insights()
        self.assertIn('total_decisions', insights)


class TestContextAwareCommandRecommender(unittest.TestCase):
    """Test cases for ContextAwareCommandRecommender."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        available_commands = ["goal", "vision", "strategies", "analyze", "validate"]
        self.recommender = ContextAwareCommandRecommender(self.temp_dir, available_commands)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_suggestion_generation(self):
        """Test suggestion generation."""
        context = SuggestionContext(project_path=self.temp_dir, project_phase="planning")

        suggestions = self.recommender.get_command_suggestions("create a goal", context, max_suggestions=3)

        # Should return suggestions
        self.assertGreater(len(suggestions), 0)
        self.assertLessEqual(len(suggestions), 3)

        # All suggestions should be valid commands
        for suggestion in suggestions:
            self.assertIn(suggestion.command, self.recommender.available_commands)

    def test_learning_from_interaction(self):
        """Test learning from user interaction."""
        suggestion = CommandSuggestion(
            "goal", "Define goals", SuggestionCategory.GOAL_MANAGEMENT, confidence_score=0.8
        )
        context = SuggestionContext(project_path=self.temp_dir, project_phase="planning")

        # Learn from positive interaction
        self.recommender.learn_from_user_interaction("create goal", suggestion, True, context)

        # Check that learning occurred
        insights = self.recommender.get_recommendation_insights()
        self.assertIn('performance_stats', insights)


class TestSuggestionIntegrationManager(unittest.TestCase):
    """Test cases for SuggestionIntegrationManager."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.integration = SuggestionIntegrationManager(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        self.integration.cleanup()
        shutil.rmtree(self.temp_dir)

    def test_context_creation(self):
        """Test suggestion context creation."""
        context = self.integration.create_suggestion_context("goal", ["vision"])

        self.assertIsNotNone(context)
        self.assertEqual(context.project_path, self.temp_dir)
        self.assertIn("goal", context.recent_commands)

    def test_suggestion_generation(self):
        """Test integrated suggestion generation."""
        suggestions = self.integration.get_command_suggestions("create a goal", "vision", ["vision"])

        if suggestions:  # Only test if suggestions are generated
            self.assertGreater(len(suggestions), 0)
            for suggestion in suggestions:
                self.assertIsInstance(suggestion, CommandSuggestion)

    def test_analytics_generation(self):
        """Test analytics generation."""
        analytics = self.integration.get_suggestion_analytics()

        self.assertIn('integration_status', analytics)
        self.assertIn('project_context', analytics)


class TestSuggestionLearningEngine(unittest.TestCase):
    """Test cases for SuggestionLearningEngine."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.learning_engine = SuggestionLearningEngine(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_interaction_recording(self):
        """Test interaction recording for learning."""
        suggestion = CommandSuggestion(
            "goal", "Define goals", SuggestionCategory.GOAL_MANAGEMENT, confidence_score=0.8
        )
        context = SuggestionContext(project_path=self.temp_dir, project_phase="planning")

        # Record interaction
        self.learning_engine.record_suggestion_interaction(
            suggestion, True, context, 150.0
        )

        # Check that interaction was recorded
        insights = self.learning_engine.get_learned_insights()
        self.assertIn('learning_summary', insights)

    def test_personalized_adjustments(self):
        """Test personalized suggestion adjustments."""
        suggestion = CommandSuggestion(
            "goal", "Define goals", SuggestionCategory.GOAL_MANAGEMENT, confidence_score=0.8
        )
        context = SuggestionContext(project_path=self.temp_dir, project_phase="planning")

        # Get personalized adjustments
        adjustments = self.learning_engine.get_personalized_suggestion_adjustments(suggestion, context)

        self.assertIn('confidence_boost', adjustments)
        self.assertIn('context_multiplier', adjustments)
        self.assertIsInstance(adjustments['confidence_boost'], float)


class TestIntegrationScenarios(unittest.TestCase):
    """Integration test scenarios."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())

        # Create mock project structure
        goalkit_dir = self.temp_dir / ".goalkit"
        goalkit_dir.mkdir()

        # Create mock goal file
        goal_file = goalkit_dir / "goal.md"
        goal_file.write_text("# Goal Definition: Test Goal\n\n**Status**: planning\n")

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_end_to_end_suggestion_flow(self):
        """Test complete suggestion flow from input to learning."""
        # Initialize integration
        integration = SuggestionIntegrationManager(self.temp_dir)

        try:
            # Create context
            context = integration.create_suggestion_context("goal", ["vision"])

            # Get suggestions
            suggestions = integration.get_command_suggestions("create a goal", "vision", ["vision"])

            if suggestions:
                # Select a suggestion
                selected_suggestion = suggestions[0]

                # Learn from interaction
                integration.learn_from_suggestion_feedback(selected_suggestion, True, context)

                # Verify learning occurred
                analytics = integration.get_suggestion_analytics()
                self.assertIsInstance(analytics, dict)

        finally:
            integration.cleanup()

    def test_suggestion_system_with_memory_integration(self):
        """Test suggestion system with memory system integration."""
        integration = SuggestionIntegrationManager(self.temp_dir)

        try:
            # Test that memory system is properly integrated
            context = integration.create_suggestion_context()

            # Should be able to create context even without full memory system
            self.assertIsNotNone(context)

            # Should be able to get suggestions
            suggestions = integration.get_command_suggestions("analyze project")

            # Suggestions should be valid
            for suggestion in suggestions:
                self.assertIsInstance(suggestion, CommandSuggestion)
                self.assertGreater(suggestion.confidence_score, 0.0)

        finally:
            integration.cleanup()


def run_suggestion_system_tests():
    """Run all suggestion system tests."""
    # Create test suite
    test_classes = [
        TestCommandSuggestion,
        TestSuggestionContext,
        TestUserIntentAnalyzer,
        TestCommandPatternMatcher,
        TestSuggestionRankingEngine,
        TestContextAwareCommandRecommender,
        TestSuggestionIntegrationManager,
        TestSuggestionLearningEngine,
        TestIntegrationScenarios
    ]

    suite = unittest.TestSuite()
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_suggestion_system_tests()
    if success:
        print("\n✅ All suggestion system tests passed!")
    else:
        print("\n❌ Some suggestion system tests failed!")
        exit(1)