#!/usr/bin/env python3
"""
Enhanced Metrics System for A/B Testing Framework

This module extends the baseline metrics system with A/B testing capabilities
for template validation and hypothesis testing.
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Literal
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import re
import random
import math

@dataclass
class EnhancedInteractionMetrics:
    """Enhanced metrics for individual AI interactions with A/B testing support."""

    # Original fields from InteractionMetrics
    timestamp: str
    command: str
    user_input_length: int
    response_length: int
    clarification_needed: bool
    response_quality_score: float
    context_retained: bool
    template_used: bool

    # A/B testing fields
    test_group: Optional[Literal['A', 'B']] = None
    test_id: Optional[str] = None
    variant_name: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None

    # Enhanced feedback fields
    user_satisfaction_score: Optional[float] = None
    feedback_text: Optional[str] = None
    task_completion_time: Optional[float] = None
    error_encountered: bool = False
    error_type: Optional[str] = None

    # Template validation fields
    template_validation_score: Optional[float] = None
    template_compliance_issues: List[str] = None
    success_criteria_met: bool = False

    def __post_init__(self):
        if self.template_compliance_issues is None:
            self.template_compliance_issues = []

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        # Handle non-serializable fields
        if isinstance(data['template_compliance_issues'], list):
            data['template_compliance_issues'] = list(data['template_compliance_issues'])
        return data

    def is_successful_interaction(self) -> bool:
        """Determine if this interaction was successful."""
        return (
            not self.clarification_needed and
            not self.error_encountered and
            self.response_quality_score >= 7.0 and
            (self.user_satisfaction_score is None or self.user_satisfaction_score >= 7.0)
        )