"""Data models for Goalkeeper CLI."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from datetime import datetime
from enum import Enum


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


class TaskStatus(Enum):
    """Task status enumeration."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Task:
    """Implementation task within a goal."""

    id: str
    goal_id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.TODO
    estimated_hours: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    depends_on: Optional[str] = None  # Optional task ID this task depends on


@dataclass
class TemplateMetadata:
    """Metadata about a downloaded template."""

    filename: str
    size: int
    release: str
    asset_url: str
