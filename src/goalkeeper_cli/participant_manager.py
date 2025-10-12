#!/usr/bin/env python3
"""
Participant Management System for A/B Testing Framework

This module handles user assignment, tracking, and management for A/B testing
of template validation and AI performance enhancements.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Literal, Set, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import random

@dataclass
class Participant:
    """Represents a participant in A/B testing."""
    user_id: str
    test_group: Literal['A', 'B']
    assigned_at: str
    test_ids: List[str]
    is_active: bool = True
    completed_tests: List[str] = None
    demographic_data: Dict[str, Any] = None

    def __post_init__(self):
        if self.test_ids is None:
            self.test_ids = []
        if self.completed_tests is None:
            self.completed_tests = []
        if self.demographic_data is None:
            self.demographic_data = {}

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class TestGroup:
    """Represents an A/B test group configuration."""
    group_id: str
    name: str
    description: str
    variant_config: Dict[str, Any]
    target_percentage: float
    is_control: bool = False

class ParticipantManager:
    """Manages participant assignment and tracking for A/B tests."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.participants_path = project_path / ".goalkit" / "participants"
        self.participants_path.mkdir(parents=True, exist_ok=True)

        self.participants_file = self.participants_path / "participants.json"
        self.test_groups_file = self.participants_path / "test_groups.json"

        self.participants: Dict[str, Participant] = {}
        self.test_groups: Dict[str, TestGroup] = {}

        self._load_data()

    def _load_data(self) -> None:
        """Load participant and test group data from files."""
        # Load participants
        if self.participants_file.exists():
            try:
                with open(self.participants_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for user_id, participant_data in data.items():
                        self.participants[user_id] = Participant(**participant_data)
            except (json.JSONDecodeError, KeyError):
                self.participants = {}

        # Load test groups
        if self.test_groups_file.exists():
            try:
                with open(self.test_groups_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for group_id, group_data in data.items():
                        self.test_groups[group_id] = TestGroup(**group_data)
            except (json.JSONDecodeError, KeyError):
                self.test_groups = {}

    def _save_data(self) -> None:
        """Save participant and test group data to files."""
        # Save participants
        with open(self.participants_file, 'w', encoding='utf-8') as f:
            data = {user_id: p.to_dict() for user_id, p in self.participants.items()}
            json.dump(data, f, indent=2)

        # Save test groups
        with open(self.test_groups_file, 'w', encoding='utf-8') as f:
            data = {group_id: tg.__dict__ for group_id, tg in self.test_groups.items()}
            json.dump(data, f, indent=2)

    def create_test_groups(self, test_id: str, control_config: Dict[str, Any],
                          variant_config: Dict[str, Any], control_percentage: float = 50.0) -> None:
        """Create A/B test groups for a new test."""

        # Create control group (A)
        control_group = TestGroup(
            group_id=f"{test_id}_A",
            name="Control Group",
            description="Original template system without enhancements",
            variant_config=control_config,
            target_percentage=control_percentage,
            is_control=True
        )

        # Create variant group (B)
        variant_group = TestGroup(
            group_id=f"{test_id}_B",
            name="Variant Group",
            description="Enhanced template system with validation",
            variant_config=variant_config,
            target_percentage=100.0 - control_percentage,
            is_control=False
        )

        self.test_groups[f"{test_id}_A"] = control_group
        self.test_groups[f"{test_id}_B"] = variant_group
        self._save_data()

    def assign_user_to_test(self, user_id: str, test_id: str) -> str:
        """Assign a user to a test group using consistent hashing."""

        # Generate consistent hash for user-test combination
        hash_input = f"{user_id}:{test_id}".encode('utf-8')
        hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)
        normalized_hash = hash_value / (16**32)  # Normalize to 0-1

        # Find appropriate group based on percentages
        cumulative_percentage = 0.0
        for group_id, group in self.test_groups.items():
            if group_id.startswith(f"{test_id}_"):
                cumulative_percentage += group.target_percentage / 100.0
                if normalized_hash <= cumulative_percentage:
                    return group.group_id.split('_')[-1]  # Return 'A' or 'B'

        # Fallback to group A if something goes wrong
        return 'A'

    def register_participant(self, user_id: str, test_id: str,
                           demographic_data: Dict[str, Any] = None) -> Participant:
        """Register a new participant for a test."""

        if user_id in self.participants:
            participant = self.participants[user_id]
            if test_id not in participant.test_ids:
                participant.test_ids.append(test_id)
        else:
            # Assign user to test group
            test_group = self.assign_user_to_test(user_id, test_id)

            participant = Participant(
                user_id=user_id,
                test_group=test_group,
                assigned_at=datetime.now().isoformat(),
                test_ids=[test_id],
                demographic_data=demographic_data or {}
            )
            self.participants[user_id] = participant

        self._save_data()
        return participant

    def get_participant_group(self, user_id: str, test_id: str) -> Optional[str]:
        """Get the test group assignment for a participant."""
        if user_id in self.participants:
            participant = self.participants[user_id]
            if test_id in participant.test_ids:
                return participant.test_group
        return None

    def get_participants_for_test(self, test_id: str) -> List[Participant]:
        """Get all participants for a specific test."""
        return [
            p for p in self.participants.values()
            if test_id in p.test_ids and p.is_active
        ]

    def get_group_participants(self, test_id: str, group: str) -> List[Participant]:
        """Get participants in a specific test group."""
        return [
            p for p in self.get_participants_for_test(test_id)
            if p.test_group == group
        ]

    def mark_test_completed(self, user_id: str, test_id: str) -> None:
        """Mark a test as completed for a participant."""
        if user_id in self.participants:
            participant = self.participants[user_id]
            if test_id not in participant.completed_tests:
                participant.completed_tests.append(test_id)
                self._save_data()

    def get_test_statistics(self, test_id: str) -> Dict[str, Any]:
        """Get statistics for a test."""
        all_participants = self.get_participants_for_test(test_id)
        group_a = self.get_group_participants(test_id, 'A')
        group_b = self.get_group_participants(test_id, 'B')

        completed_a = [p for p in group_a if test_id in p.completed_tests]
        completed_b = [p for p in group_b if test_id in p.completed_tests]

        return {
            "test_id": test_id,
            "total_participants": len(all_participants),
            "group_A_count": len(group_a),
            "group_B_count": len(group_b),
            "group_A_completed": len(completed_a),
            "group_B_completed": len(completed_b),
            "group_A_completion_rate": len(completed_a) / len(group_a) if group_a else 0,
            "group_B_completion_rate": len(completed_b) / len(group_b) if group_b else 0
        }

    def cleanup_inactive_participants(self, days_inactive: int = 30) -> int:
        """Remove participants who haven't been active for specified days."""
        cutoff_date = datetime.now() - timedelta(days=days_inactive)
        inactive_count = 0

        for user_id, participant in list(self.participants.items()):
            try:
                assigned_date = datetime.fromisoformat(participant.assigned_at.replace('Z', '+00:00'))
                if assigned_date < cutoff_date and not participant.completed_tests:
                    del self.participants[user_id]
                    inactive_count += 1
            except ValueError:
                # If date parsing fails, consider it inactive
                del self.participants[user_id]
                inactive_count += 1

        if inactive_count > 0:
            self._save_data()

        return inactive_count