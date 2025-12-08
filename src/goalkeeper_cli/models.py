"""Data models for Goalkeeper CLI."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from datetime import datetime


@dataclass
class Project:
    """Goal Kit project."""

    name: str
    path: Path
    agent: str
    created_at: datetime
    health_score: Optional[float] = None


@dataclass
class Goal:
    """Individual goal within a project."""

    id: str
    name: str
    phase: str  # 'vision', 'goal', 'strategies', 'milestones', 'execute', 'done'
    completion_percent: int
    success_criteria_count: int
    metrics_defined: bool


@dataclass
class Milestone:
    """Milestone within a goal."""

    id: str
    name: str
    description: str
    completed: bool
    due_date: Optional[datetime] = None


@dataclass
class Task:
    """Implementation task within a milestone."""

    id: str
    title: str
    description: str
    milestone_id: str
    completed: bool
    priority: str = "medium"  # 'low', 'medium', 'high'
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None


@dataclass
class TemplateMetadata:
    """Metadata about a downloaded template."""

    filename: str
    size: int
    release: str
    asset_url: str
