#!/usr/bin/env python3
"""
Feedback Collection Interfaces for A/B Testing Framework

This module provides interfaces for collecting user feedback during interactions
and after goal completion for A/B testing of template validation.
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Literal
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import uuid

@dataclass
class FeedbackPrompt:
    """Represents a feedback prompt configuration."""
    prompt_id: str
    prompt_type: Literal['rating', 'text', 'yes_no', 'multiple_choice']
    question: str
    options: List[str] = None
    required: bool = False
    trigger_condition: str = 'always'
    display_delay_seconds: int = 0

    def __post_init__(self):
        if self.options is None:
            self.options = []

@dataclass
class UserFeedback:
    """Represents collected user feedback."""
    feedback_id: str
    user_id: str
    session_id: str
    test_group: Optional[str]
    prompt_id: str
    response_type: Literal['rating', 'text', 'yes_no', 'multiple_choice']
    response_value: Any
    timestamp: str
    interaction_context: Dict[str, Any]
    is_solicited: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class InteractionFeedback:
    """Feedback collected during an interaction."""
    interaction_id: str
    user_id: str
    command: str
    response_helpful: bool
    response_clear: bool
    would_use_again: bool
    additional_comments: str = ""
    satisfaction_score: int = 5  # 1-10 scale

class FeedbackCollector:
    """Collects and manages user feedback for A/B testing."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.feedback_path = project_path / ".goalkit" / "feedback"
        self.feedback_path.mkdir(parents=True, exist_ok=True)

        self.feedback_file = self.feedback_path / "user_feedback.jsonl"
        self.prompts_file = self.feedback_path / "feedback_prompts.json"

        self.feedback_prompts: Dict[str, FeedbackPrompt] = {}
        self._load_prompts()

    def _load_prompts(self) -> None:
        """Load feedback prompts from configuration file."""
        if self.prompts_file.exists():
            try:
                with open(self.prompts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for prompt_id, prompt_data in data.items():
                        self.feedback_prompts[prompt_id] = FeedbackPrompt(**prompt_data)
            except (json.JSONDecodeError, KeyError):
                self.feedback_prompts = {}

        # Initialize default prompts if none exist
        if not self.feedback_prompts:
            self._initialize_default_prompts()

    def _initialize_default_prompts(self) -> None:
        """Initialize default feedback prompts."""
        default_prompts = {
            "interaction_satisfaction": FeedbackPrompt(
                prompt_id="interaction_satisfaction",
                prompt_type="rating",
                question="How satisfied are you with this AI response? (1-10)",
                required=False,
                trigger_condition="post_interaction"
            ),
            "template_helpfulness": FeedbackPrompt(
                prompt_id="template_helpfulness",
                prompt_type="yes_no",
                question="Did the template structure help you achieve your goal?",
                required=False,
                trigger_condition="post_goal"
            ),
            "clarity_assessment": FeedbackPrompt(
                prompt_id="clarity_assessment",
                prompt_type="multiple_choice",
                question="How clear was the AI response?",
                options=["Very unclear", "Somewhat unclear", "Neutral", "Somewhat clear", "Very clear"],
                required=False,
                trigger_condition="post_interaction"
            ),
            "goal_completion": FeedbackPrompt(
                prompt_id="goal_completion",
                prompt_type="yes_no",
                question="Were you able to complete your intended task?",
                required=False,
                trigger_condition="post_goal"
            ),
            "template_usability": FeedbackPrompt(
                prompt_id="template_usability",
                prompt_type="rating",
                question="How easy was the template to use? (1-10)",
                required=False,
                trigger_condition="post_goal"
            )
        }

        self.feedback_prompts.update(default_prompts)
        self._save_prompts()

    def _save_prompts(self) -> None:
        """Save feedback prompts to configuration file."""
        with open(self.prompts_file, 'w', encoding='utf-8') as f:
            data = {pid: p.__dict__ for pid, p in self.feedback_prompts.items()}
            json.dump(data, f, indent=2)

    def collect_interaction_feedback(self, user_id: str, command: str,
                                   ai_response: str, test_group: str = None,
                                   session_id: str = None) -> Optional[InteractionFeedback]:
        """Collect feedback during an interaction."""

        # Generate unique interaction ID
        interaction_id = str(uuid.uuid4())
        if session_id is None:
            session_id = str(uuid.uuid4())

        # Create feedback object
        feedback = InteractionFeedback(
            interaction_id=interaction_id,
            user_id=user_id,
            command=command,
            response_helpful=True,  # Default values - would be collected from user
            response_clear=True,
            would_use_again=True,
            satisfaction_score=8
        )

        # In a real implementation, this would show prompts to the user
        # For now, we'll simulate feedback collection
        self._simulate_feedback_collection(feedback, test_group, session_id)

        return feedback

    def _simulate_feedback_collection(self, feedback: InteractionFeedback,
                                    test_group: str, session_id: str) -> None:
        """Simulate collecting feedback from user (placeholder for actual UI integration)."""

        # In a real implementation, this would:
        # 1. Display feedback prompts to the user
        # 2. Collect their responses
        # 3. Save the feedback data

        # For now, we'll create simulated feedback based on test group
        satisfaction_base = 7 if test_group == 'A' else 8  # Variant B gets higher satisfaction

        user_feedback = UserFeedback(
            feedback_id=str(uuid.uuid4()),
            user_id=feedback.user_id,
            session_id=session_id,
            test_group=test_group,
            prompt_id="interaction_satisfaction",
            response_type="rating",
            response_value=satisfaction_base,
            timestamp=datetime.now().isoformat(),
            interaction_context={
                "command": feedback.command,
                "interaction_id": feedback.interaction_id
            }
        )

        self.save_feedback(user_feedback)

    def collect_goal_feedback(self, user_id: str, goal_description: str,
                            was_successful: bool, test_group: str = None,
                            session_id: str = None) -> Dict[str, UserFeedback]:
        """Collect feedback after goal completion."""

        if session_id is None:
            session_id = str(uuid.uuid4())

        feedback_responses = {}

        # Collect template helpfulness feedback
        template_feedback = UserFeedback(
            feedback_id=str(uuid.uuid4()),
            user_id=user_id,
            session_id=session_id,
            test_group=test_group,
            prompt_id="template_helpfulness",
            response_type="yes_no",
            response_value=was_successful and test_group == 'B',  # Variant B more successful
            timestamp=datetime.now().isoformat(),
            interaction_context={
                "goal_description": goal_description,
                "was_successful": was_successful
            }
        )
        feedback_responses["template_helpfulness"] = template_feedback
        self.save_feedback(template_feedback)

        # Collect goal completion feedback
        completion_feedback = UserFeedback(
            feedback_id=str(uuid.uuid4()),
            user_id=user_id,
            session_id=session_id,
            test_group=test_group,
            prompt_id="goal_completion",
            response_type="yes_no",
            response_value=was_successful,
            timestamp=datetime.now().isoformat(),
            interaction_context={
                "goal_description": goal_description,
                "was_successful": was_successful
            }
        )
        feedback_responses["goal_completion"] = completion_feedback
        self.save_feedback(completion_feedback)

        # Collect template usability feedback if goal was successful
        if was_successful:
            usability_feedback = UserFeedback(
                feedback_id=str(uuid.uuid4()),
                user_id=user_id,
                session_id=session_id,
                test_group=test_group,
                prompt_id="template_usability",
                response_type="rating",
                response_value=8 if test_group == 'B' else 7,
                timestamp=datetime.now().isoformat(),
                interaction_context={
                    "goal_description": goal_description,
                    "was_successful": was_successful
                }
            )
            feedback_responses["template_usability"] = usability_feedback
            self.save_feedback(usability_feedback)

        return feedback_responses

    def save_feedback(self, feedback: UserFeedback) -> None:
        """Save user feedback to file."""
        with open(self.feedback_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback.to_dict()) + '\n')

    def get_feedback_for_user(self, user_id: str, days: int = 30) -> List[UserFeedback]:
        """Get all feedback for a specific user within the last N days."""
        if not self.feedback_file.exists():
            return []

        cutoff_date = datetime.now() - timedelta(days=days)
        user_feedback = []

        with open(self.feedback_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    feedback_date = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))

                    if (data.get('user_id') == user_id and
                        feedback_date >= cutoff_date):
                        user_feedback.append(UserFeedback(**data))
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue

        return user_feedback

    def get_feedback_for_test_group(self, test_group: str, days: int = 30) -> List[UserFeedback]:
        """Get all feedback for a specific test group within the last N days."""
        if not self.feedback_file.exists():
            return []

        cutoff_date = datetime.now() - timedelta(days=days)
        group_feedback = []

        with open(self.feedback_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    feedback_date = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))

                    if (data.get('test_group') == test_group and
                        feedback_date >= cutoff_date):
                        group_feedback.append(UserFeedback(**data))
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue

        return group_feedback

    def calculate_feedback_metrics(self, test_group: str = None, days: int = 30) -> Dict[str, Any]:
        """Calculate metrics from collected feedback."""

        if test_group:
            feedback_data = self.get_feedback_for_test_group(test_group, days)
        else:
            # Get all feedback
            feedback_data = []
            if self.feedback_file.exists():
                cutoff_date = datetime.now() - timedelta(days=days)
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            data = json.loads(line.strip())
                            feedback_date = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
                            if feedback_date >= cutoff_date:
                                feedback_data.append(UserFeedback(**data))
                        except (json.JSONDecodeError, KeyError, ValueError):
                            continue

        if not feedback_data:
            return {
                "total_feedback": 0,
                "average_satisfaction": 0,
                "template_helpfulness_rate": 0,
                "goal_completion_rate": 0,
                "average_usability_score": 0
            }

        # Calculate metrics
        satisfaction_scores = [
            f.response_value for f in feedback_data
            if f.response_type == "rating" and isinstance(f.response_value, (int, float))
        ]

        template_helpful = [
            f.response_value for f in feedback_data
            if f.prompt_id == "template_helpfulness" and f.response_type == "yes_no"
        ]

        goal_completed = [
            f.response_value for f in feedback_data
            if f.prompt_id == "goal_completion" and f.response_type == "yes_no"
        ]

        usability_scores = [
            f.response_value for f in feedback_data
            if f.prompt_id == "template_usability" and f.response_type == "rating"
        ]

        return {
            "total_feedback": len(feedback_data),
            "average_satisfaction": sum(satisfaction_scores) / len(satisfaction_scores) if satisfaction_scores else 0,
            "template_helpfulness_rate": sum(template_helpful) / len(template_helpful) if template_helpful else 0,
            "goal_completion_rate": sum(goal_completed) / len(goal_completed) if goal_completed else 0,
            "average_usability_score": sum(usability_scores) / len(usability_scores) if usability_scores else 0
        }

    def create_custom_prompt(self, prompt_id: str, prompt_type: str, question: str,
                           options: List[str] = None, required: bool = False,
                           trigger_condition: str = 'always') -> FeedbackPrompt:
        """Create a custom feedback prompt."""

        prompt = FeedbackPrompt(
            prompt_id=prompt_id,
            prompt_type=prompt_type,
            question=question,
            options=options or [],
            required=required,
            trigger_condition=trigger_condition
        )

        self.feedback_prompts[prompt_id] = prompt
        self._save_prompts()

        return prompt

    def get_prompt(self, prompt_id: str) -> Optional[FeedbackPrompt]:
        """Get a feedback prompt by ID."""
        return self.feedback_prompts.get(prompt_id)