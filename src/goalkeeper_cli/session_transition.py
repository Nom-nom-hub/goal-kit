#!/usr/bin/env python3
"""
Session Transition Logging and Monitoring System

This module implements comprehensive logging and monitoring for session transitions
with context retention tracking, performance metrics, and quality validation.
"""

import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging
import hashlib
import threading
from collections import defaultdict, deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransitionType(Enum):
    """Types of session transitions."""
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    CONTEXT_LOAD = "context_load"
    CONTEXT_SAVE = "context_save"
    CONTEXT_MERGE = "context_merge"
    CONTEXT_EVICTION = "context_eviction"
    GOAL_TRANSITION = "goal_transition"
    PROJECT_SWITCH = "project_switch"
    USER_CHANGE = "user_change"
    SYSTEM_RESTART = "system_restart"


class TransitionStatus(Enum):
    """Status of transition operations."""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class RetentionQuality(Enum):
    """Quality levels for context retention."""
    EXCELLENT = "excellent"  # 95%+ retention
    GOOD = "good"           # 85-94% retention
    FAIR = "fair"           # 70-84% retention
    POOR = "poor"           # <70% retention


@dataclass
class SessionTransition:
    """Structured format for session transition events and metadata."""

    # Core identification
    transition_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ""
    previous_session_id: Optional[str] = None
    user_id: str = ""
    project_path: str = ""

    # Transition details
    transition_type: TransitionType = TransitionType.SESSION_START
    status: TransitionStatus = TransitionStatus.SUCCESS
    timestamp: datetime = field(default_factory=datetime.now)

    # Context information
    context_objects_loaded: int = 0
    context_objects_saved: int = 0
    context_objects_evicted: int = 0
    context_objects_merged: int = 0

    # Retention metrics
    context_retention_rate: float = 0.0  # Percentage of context retained
    decision_history_preserved: bool = True
    re_explanation_events: int = 0  # How many times user had to re-explain

    # Performance metrics
    transition_duration_ms: float = 0.0
    memory_usage_before_mb: float = 0.0
    memory_usage_after_mb: float = 0.0
    cpu_usage_percent: float = 0.0

    # Quality metrics
    retention_quality: RetentionQuality = RetentionQuality.EXCELLENT
    user_satisfaction_score: Optional[float] = None
    error_count: int = 0
    warning_count: int = 0

    # Content analysis
    topics_discussed: List[str] = field(default_factory=list)
    goals_mentioned: List[str] = field(default_factory=list)
    decisions_made: List[str] = field(default_factory=list)
    files_accessed: List[str] = field(default_factory=list)

    # Technical details
    system_version: str = ""
    python_version: str = ""
    memory_available_mb: float = 0.0
    disk_space_available_gb: float = 0.0

    # Additional metadata
    notes: str = ""
    tags: List[str] = field(default_factory=list)
    custom_metrics: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization processing."""
        if not self.transition_id:
            self.transition_id = str(uuid.uuid4())

        # Calculate retention quality based on rate
        self._update_retention_quality()

    def _update_retention_quality(self):
        """Update retention quality based on retention rate."""
        if self.context_retention_rate >= 0.95:
            self.retention_quality = RetentionQuality.EXCELLENT
        elif self.context_retention_rate >= 0.85:
            self.retention_quality = RetentionQuality.GOOD
        elif self.context_retention_rate >= 0.70:
            self.retention_quality = RetentionQuality.FAIR
        else:
            self.retention_quality = RetentionQuality.POOR

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)

        # Convert datetime to ISO string
        data['timestamp'] = self.timestamp.isoformat()

        # Convert enums to strings
        data['transition_type'] = self.transition_type.value
        data['status'] = self.status.value
        data['retention_quality'] = self.retention_quality.value

        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'SessionTransition':
        """Create from dictionary."""
        # Convert ISO string back to datetime
        if 'timestamp' in data and isinstance(data['timestamp'], str):
            try:
                data['timestamp'] = datetime.fromisoformat(data['timestamp'])
            except (ValueError, TypeError):
                data['timestamp'] = datetime.now()

        # Convert string enums back to enum objects
        if 'transition_type' in data and isinstance(data['transition_type'], str):
            try:
                data['transition_type'] = TransitionType(data['transition_type'])
            except ValueError:
                data['transition_type'] = TransitionType.SESSION_START

        if 'status' in data and isinstance(data['status'], str):
            try:
                data['status'] = TransitionStatus(data['status'])
            except ValueError:
                data['status'] = TransitionStatus.SUCCESS

        if 'retention_quality' in data and isinstance(data['retention_quality'], str):
            try:
                data['retention_quality'] = RetentionQuality(data['retention_quality'])
            except ValueError:
                data['retention_quality'] = RetentionQuality.EXCELLENT

        return cls(**data)

    def calculate_transition_efficiency(self) -> float:
        """Calculate overall transition efficiency score."""
        # Base efficiency from retention rate
        efficiency = self.context_retention_rate * 0.4

        # Performance factor (lower duration = higher efficiency)
        if self.transition_duration_ms > 0:
            performance_factor = min(1.0, 5000 / self.transition_duration_ms)
            efficiency += performance_factor * 0.3

        # Quality factor
        quality_multiplier = {
            RetentionQuality.EXCELLENT: 1.0,
            RetentionQuality.GOOD: 0.8,
            RetentionQuality.FAIR: 0.6,
            RetentionQuality.POOR: 0.4
        }
        efficiency += quality_multiplier[self.retention_quality] * 0.3

        return min(1.0, efficiency)

    def is_successful_transition(self) -> bool:
        """Determine if this was a successful transition."""
        return (
            self.status == TransitionStatus.SUCCESS and
            self.context_retention_rate >= 0.8 and
            self.error_count == 0
        )

    def get_summary(self) -> str:
        """Get a human-readable summary of the transition."""
        return (
            f"Transition {self.transition_id}: {self.transition_type.value} "
            f"({self.status.value}) - Retention: {self.context_retention_rate".1%"} "
            f"({self.retention_quality.value}) - Duration: {self.transition_duration_ms".0f"}ms"
        )
class SessionTransitionLogger:
    """Comprehensive logging system for session transitions with detailed metrics."""

    def __init__(self, project_path: Path, config: Optional[dict] = None):
        self.project_path = Path(project_path)
        self.config = self._get_default_config()
        if config:
            self.config.update(config)

        # Initialize storage
        self.log_path = self.project_path / ".goalkit" / "logs" / "transitions"
        self.log_path.mkdir(parents=True, exist_ok=True)

        # Transition storage
        self.transitions: List[SessionTransition] = []
        self.transition_index: Dict[str, SessionTransition] = {}
        self.session_index: Dict[str, List[SessionTransition]] = defaultdict(list)
        self.storage_lock = threading.Lock()

        # Performance tracking
        self.stats = {
            'total_transitions': 0,
            'successful_transitions': 0,
            'failed_transitions': 0,
            'average_retention_rate': 0.0,
            'average_transition_time': 0.0,
            'total_re_explanations': 0,
            'context_objects_processed': 0
        }

        # Background processing
        self.flush_thread = None
        self.flush_running = False
        self.pending_transitions: deque = deque(maxlen=1000)

        logger.info(f"SessionTransitionLogger initialized for project: {self.project_path}")

    def _get_default_config(self) -> dict:
        """Get default configuration for the logger."""
        return {
            'max_log_files': 100,
            'max_log_age_days': 30,
            'flush_interval_seconds': 30,
            'enable_background_flush': True,
            'log_level': 'INFO',
            'include_system_metrics': True,
            'include_performance_metrics': True,
            'enable_compression': True,
            'buffer_size': 100
        }

    def log_transition(self, transition: SessionTransition) -> bool:
        """Log a session transition event."""
        try:
            with self.storage_lock:
                # Add to pending transitions for background processing
                self.pending_transitions.append(transition)

                # Update indexes
                self.transition_index[transition.transition_id] = transition
                self.session_index[transition.session_id].append(transition)

                # Update statistics
                self._update_statistics(transition)

                logger.debug(f"Logged transition: {transition.get_summary()}")

                # Immediate flush if buffer is full
                if len(self.pending_transitions) >= self.config['buffer_size']:
                    self._flush_pending_transitions()

                return True

        except Exception as e:
            logger.error(f"Error logging transition: {e}")
            return False

    def log_session_start(self, session_id: str, user_id: str, project_path: str,
                         context_objects_loaded: int = 0) -> SessionTransition:
        """Log the start of a new session."""
        transition = SessionTransition(
            session_id=session_id,
            user_id=user_id,
            project_path=project_path,
            transition_type=TransitionType.SESSION_START,
            context_objects_loaded=context_objects_loaded,
            system_version=self._get_system_version(),
            python_version=self._get_python_version(),
            memory_available_mb=self._get_memory_available(),
            disk_space_available_gb=self._get_disk_space_available()
        )

        # Add performance metrics
        if self.config['include_performance_metrics']:
            transition.memory_usage_before_mb = self._get_memory_usage()
            transition.cpu_usage_percent = self._get_cpu_usage()

        self.log_transition(transition)
        return transition

    def log_session_end(self, session_id: str, context_objects_saved: int = 0,
                       context_retention_rate: float = 1.0) -> SessionTransition:
        """Log the end of a session."""
        # Get the corresponding start transition
        start_transition = None
        if session_id in self.session_index:
            session_transitions = self.session_index[session_id]
            for t in reversed(session_transitions):
                if t.transition_type == TransitionType.SESSION_START:
                    start_transition = t
                    break

        transition = SessionTransition(
            session_id=session_id,
            previous_session_id=start_transition.session_id if start_transition else None,
            user_id=start_transition.user_id if start_transition else "",
            project_path=start_transition.project_path if start_transition else "",
            transition_type=TransitionType.SESSION_END,
            context_objects_saved=context_objects_saved,
            context_retention_rate=context_retention_rate,
            system_version=self._get_system_version(),
            python_version=self._get_python_version(),
            memory_available_mb=self._get_memory_available(),
            disk_space_available_gb=self._get_disk_space_available()
        )

        # Calculate duration from start transition
        if start_transition:
            duration = (datetime.now() - start_transition.timestamp).total_seconds() * 1000
            transition.transition_duration_ms = duration

        # Add performance metrics
        if self.config['include_performance_metrics']:
            transition.memory_usage_after_mb = self._get_memory_usage()
            transition.cpu_usage_percent = self._get_cpu_usage()

        self.log_transition(transition)
        return transition

    def log_context_operation(self, session_id: str, operation: TransitionType,
                            context_objects_affected: int, success: bool = True,
                            notes: str = "") -> SessionTransition:
        """Log a context-related operation."""
        transition = SessionTransition(
            session_id=session_id,
            transition_type=operation,
            status=TransitionStatus.SUCCESS if success else TransitionStatus.FAILURE,
            notes=notes
        )

        # Set appropriate counters based on operation type
        if operation == TransitionType.CONTEXT_LOAD:
            transition.context_objects_loaded = context_objects_affected
        elif operation == TransitionType.CONTEXT_SAVE:
            transition.context_objects_saved = context_objects_affected
        elif operation == TransitionType.CONTEXT_EVICTION:
            transition.context_objects_evicted = context_objects_affected
        elif operation == TransitionType.CONTEXT_MERGE:
            transition.context_objects_merged = context_objects_affected

        # Add performance metrics
        if self.config['include_performance_metrics']:
            transition.memory_usage_before_mb = self._get_memory_usage()
            transition.memory_usage_after_mb = self._get_memory_usage()
            transition.cpu_usage_percent = self._get_cpu_usage()

        self.log_transition(transition)
        return transition

    def _update_statistics(self, transition: SessionTransition) -> None:
        """Update internal statistics based on transition."""
        self.stats['total_transitions'] += 1

        if transition.is_successful_transition():
            self.stats['successful_transitions'] += 1
        else:
            self.stats['failed_transitions'] += 1

        # Update running averages
        total_transitions = self.stats['total_transitions']
        self.stats['average_retention_rate'] = (
            (self.stats['average_retention_rate'] * (total_transitions - 1) +
             transition.context_retention_rate) / total_transitions
        )

        if transition.transition_duration_ms > 0:
            self.stats['average_transition_time'] = (
                (self.stats['average_transition_time'] * (total_transitions - 1) +
                 transition.transition_duration_ms) / total_transitions
            )

        self.stats['total_re_explanations'] += transition.re_explanation_events
        self.stats['context_objects_processed'] += (
            transition.context_objects_loaded +
            transition.context_objects_saved +
            transition.context_objects_evicted +
            transition.context_objects_merged
        )

    def _flush_pending_transitions(self) -> None:
        """Flush pending transitions to disk."""
        try:
            while self.pending_transitions:
                transition = self.pending_transitions.popleft()

                # Save to daily log file
                log_file = self._get_log_file_for_date(transition.timestamp)
                self._append_transition_to_file(transition, log_file)

                # Also save individual transition file for quick access
                individual_file = self.log_path / f"{transition.transition_id}.json"
                self._save_transition_file(transition, individual_file)

        except Exception as e:
            logger.error(f"Error flushing transitions: {e}")

    def _get_log_file_for_date(self, timestamp: datetime) -> Path:
        """Get the log file path for a specific date."""
        date_str = timestamp.strftime("%Y-%m-%d")
        return self.log_path / f"transitions_{date_str}.jsonl"

    def _append_transition_to_file(self, transition: SessionTransition, file_path: Path) -> None:
        """Append a transition to a log file."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'a', encoding='utf-8') as f:
                json.dump(transition.to_dict(), f, ensure_ascii=False)
                f.write('\n')

        except Exception as e:
            logger.error(f"Error appending transition to file {file_path}: {e}")

    def _save_transition_file(self, transition: SessionTransition, file_path: Path) -> None:
        """Save a transition to an individual file."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(transition.to_dict(), f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error saving transition file {file_path}: {e}")

    def get_transition(self, transition_id: str) -> Optional[SessionTransition]:
        """Retrieve a specific transition by ID."""
        try:
            with self.storage_lock:
                # Check memory first
                if transition_id in self.transition_index:
                    return self.transition_index[transition_id]

                # Check disk
                transition_file = self.log_path / f"{transition_id}.json"
                if transition_file.exists():
                    with open(transition_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    return SessionTransition.from_dict(data)

                return None

        except Exception as e:
            logger.error(f"Error retrieving transition {transition_id}: {e}")
            return None

    def get_session_transitions(self, session_id: str) -> List[SessionTransition]:
        """Get all transitions for a specific session."""
        try:
            with self.storage_lock:
                # Return from memory if available
                if session_id in self.session_index:
                    return self.session_index[session_id].copy()

                # Otherwise return empty list - disk loading would be expensive
                return []

        except Exception as e:
            logger.error(f"Error retrieving session transitions for {session_id}: {e}")
            return []

    def get_transitions_by_type(self, transition_type: TransitionType,
                              limit: int = 100) -> List[SessionTransition]:
        """Get transitions of a specific type."""
        try:
            with self.storage_lock:
                transitions = [
                    t for t in self.transition_index.values()
                    if t.transition_type == transition_type
                ]

                # Sort by timestamp (newest first)
                transitions.sort(key=lambda x: x.timestamp, reverse=True)
                return transitions[:limit]

        except Exception as e:
            logger.error(f"Error retrieving transitions by type {transition_type}: {e}")
            return []

    def get_transitions_in_range(self, start_time: datetime,
                               end_time: datetime) -> List[SessionTransition]:
        """Get transitions within a time range."""
        try:
            with self.storage_lock:
                transitions = [
                    t for t in self.transition_index.values()
                    if start_time <= t.timestamp <= end_time
                ]

                # Sort by timestamp
                transitions.sort(key=lambda x: x.timestamp)
                return transitions

        except Exception as e:
            logger.error(f"Error retrieving transitions in range: {e}")
            return []

    def get_statistics(self) -> dict:
        """Get comprehensive transition statistics."""
        try:
            with self.storage_lock:
                stats = self.stats.copy()

                # Calculate additional metrics
                if stats['total_transitions'] > 0:
                    stats['success_rate'] = stats['successful_transitions'] / stats['total_transitions']
                    stats['failure_rate'] = stats['failed_transitions'] / stats['total_transitions']

                    # Calculate retention quality distribution
                    quality_counts = defaultdict(int)
                    for transition in self.transition_index.values():
                        quality_counts[transition.retention_quality.value] += 1

                    stats['retention_quality_distribution'] = dict(quality_counts)

                    # Calculate average efficiency
                    total_efficiency = sum(
                        t.calculate_transition_efficiency()
                        for t in self.transition_index.values()
                    )
                    stats['average_efficiency'] = total_efficiency / stats['total_transitions']

                return stats

        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {}

    def start_background_flush(self) -> None:
        """Start background flush thread."""
        if self.flush_running:
            return

        self.flush_running = True
        self.flush_thread = threading.Thread(target=self._background_flush_loop, daemon=True)
        self.flush_thread.start()
        logger.info("Background flush thread started")

    def stop_background_flush(self) -> None:
        """Stop background flush thread."""
        self.flush_running = False
        if self.flush_thread:
            self.flush_thread.join(timeout=5)

        # Final flush
        self._flush_pending_transitions()
        logger.info("Background flush thread stopped")

    def _background_flush_loop(self) -> None:
        """Background loop for flushing transitions."""
        while self.flush_running:
            try:
                # Sleep for flush interval
                threading.Event().wait(self.config['flush_interval_seconds'])

                if self.flush_running:
                    self._flush_pending_transitions()

            except Exception as e:
                logger.error(f"Error in background flush loop: {e}")
                threading.Event().wait(60)  # Wait 1 minute on error

    def cleanup_old_logs(self) -> int:
        """Clean up old log files based on retention policy."""
        try:
            cleaned_count = 0
            cutoff_date = datetime.now() - timedelta(days=self.config['max_log_age_days'])

            # Clean individual transition files
            for transition_file in self.log_path.glob("*.json"):
                if transition_file.name.endswith('.json') and not transition_file.name.startswith('transitions_'):
                    try:
                        # Check if file is old enough to delete
                        file_modified = datetime.fromtimestamp(transition_file.stat().st_mtime)
                        if file_modified < cutoff_date:
                            transition_file.unlink()
                            cleaned_count += 1
                    except Exception as e:
                        logger.warning(f"Error cleaning up file {transition_file}: {e}")

            # Clean old daily log files
            for log_file in self.log_path.glob("transitions_*.jsonl"):
                try:
                    file_modified = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if file_modified < cutoff_date:
                        log_file.unlink()
                        cleaned_count += 1
                except Exception as e:
                    logger.warning(f"Error cleaning up log file {log_file}: {e}")

            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} old log files")

            return cleaned_count

        except Exception as e:
            logger.error(f"Error during log cleanup: {e}")
            return 0

    def _get_system_version(self) -> str:
        """Get system version information."""
        try:
            import platform
            return platform.platform()
        except Exception:
            return "Unknown"

    def _get_python_version(self) -> str:
        """Get Python version information."""
        try:
            import sys
            return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        except Exception:
            return "Unknown"

    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / (1024 * 1024)
        except ImportError:
            return 0.0
        except Exception:
            return 0.0

    def _get_memory_available(self) -> float:
        """Get available memory in MB."""
        try:
            import psutil
            return psutil.virtual_memory().available / (1024 * 1024)
        except ImportError:
            return 0.0
        except Exception:
            return 0.0

    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage."""
        try:
            import psutil
            return psutil.cpu_percent(interval=0.1)
        except ImportError:
            return 0.0
        except Exception:
            return 0.0

    def _get_disk_space_available(self) -> float:
        """Get available disk space in GB."""
        try:
            import shutil
            total, used, free = shutil.disk_usage(str(self.project_path))
            return free / (1024**3)
        except Exception:
            return 0.0

    def export_transitions(self, start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None,
                          transition_types: Optional[List[TransitionType]] = None) -> str:
        """Export transitions to JSON format."""
        try:
            transitions = []

            if start_date and end_date:
                transitions = self.get_transitions_in_range(start_date, end_date)
            else:
                # Get all transitions from memory
                transitions = list(self.transition_index.values())

            # Filter by transition types if specified
            if transition_types:
                transitions = [t for t in transitions if t.transition_type in transition_types]

            # Sort by timestamp
            transitions.sort(key=lambda x: x.timestamp)

            # Convert to dictionaries
            export_data = {
                'export_info': {
                    'exported_at': datetime.now().isoformat(),
                    'total_transitions': len(transitions),
                    'date_range': {
                        'start': start_date.isoformat() if start_date else None,
                        'end': end_date.isoformat() if end_date else None
                    },
                    'transition_types': [t.value for t in transition_types] if transition_types else None
                },
                'transitions': [t.to_dict() for t in transitions]
            }

            return json.dumps(export_data, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error exporting transitions: {e}")
            return json.dumps({'error': str(e)})

    def cleanup(self) -> None:
        """Clean up resources."""
        self.stop_background_flush()
        self._flush_pending_transitions()
        logger.info("SessionTransitionLogger cleanup completed")
class ContextRetentionValidator:
    """Validate and measure context retention goals with 95% target tracking."""

    def __init__(self, target_retention_rate: float = 0.95, config: Optional[dict] = None):
        self.target_retention_rate = target_retention_rate
        self.config = self._get_default_config()
        if config:
            self.config.update(config)

        # Validation state
        self.validation_history: List[dict] = []
        self.current_session_data: Dict[str, Any] = {}
        self.retention_targets = {
            'overall': target_retention_rate,
            'critical_context': 0.99,  # Critical context should almost never be lost
            'recent_context': 0.90,    # Recently accessed context
            'goal_context': 0.95,      # Goal-related context
            'decision_context': 0.98   # Decision history context
        }

        # Alert thresholds
        self.alert_thresholds = {
            'warning': 0.05,  # 5% below target
            'critical': 0.10,  # 10% below target
            'severe': 0.15     # 15% below target
        }

        logger.info(f"ContextRetentionValidator initialized with {target_retention_rate".1%"} target")

    def _get_default_config(self) -> dict:
        """Get default configuration for the validator."""
        return {
            'validation_interval_minutes': 5,
            'history_retention_days': 7,
            'enable_alerts': True,
            'alert_webhook_url': None,
            'min_sample_size': 10,
            'confidence_level': 0.95,
            'enable_detailed_analysis': True,
            'track_context_categories': True
        }

    def start_session_validation(self, session_id: str, initial_context_count: int) -> None:
        """Start validation tracking for a new session."""
        self.current_session_data[session_id] = {
            'start_time': datetime.now(),
            'initial_context_count': initial_context_count,
            'context_snapshots': [],
            'transitions_recorded': [],
            'retention_measurements': [],
            'alerts_triggered': []
        }

        logger.debug(f"Started validation for session {session_id}")

    def record_context_snapshot(self, session_id: str, context_count: int,
                              context_types: Optional[Dict[str, int]] = None) -> None:
        """Record a snapshot of current context state."""
        if session_id not in self.current_session_data:
            logger.warning(f"No session data found for {session_id}")
            return

        snapshot = {
            'timestamp': datetime.now(),
            'context_count': context_count,
            'context_types': context_types or {},
            'session_duration': (datetime.now() - self.current_session_data[session_id]['start_time']).total_seconds()
        }

        self.current_session_data[session_id]['context_snapshots'].append(snapshot)

        # Keep only recent snapshots to avoid memory bloat
        max_snapshots = 100
        if len(self.current_session_data[session_id]['context_snapshots']) > max_snapshots:
            self.current_session_data[session_id]['context_snapshots'] = \
                self.current_session_data[session_id]['context_snapshots'][-max_snapshots:]

    def record_transition_measurement(self, session_id: str, transition: SessionTransition) -> None:
        """Record a transition for retention analysis."""
        if session_id not in self.current_session_data:
            logger.warning(f"No session data found for {session_id}")
            return

        self.current_session_data[session_id]['transitions_recorded'].append(transition)

        # Calculate retention metrics for this transition
        measurement = self._calculate_retention_metrics(session_id, transition)
        if measurement:
            self.current_session_data[session_id]['retention_measurements'].append(measurement)

    def _calculate_retention_metrics(self, session_id: str,
                                   transition: SessionTransition) -> Optional[dict]:
        """Calculate detailed retention metrics for a transition."""
        try:
            session_data = self.current_session_data[session_id]
            initial_count = session_data['initial_context_count']

            if initial_count == 0:
                return None

            # Calculate current retention rate
            current_retention_rate = transition.context_retention_rate

            # Calculate retention by context type if available
            retention_by_type = {}
            if hasattr(transition, 'context_types') and transition.context_types:
                for context_type, count in transition.context_types.items():
                    if count > 0:
                        # Estimate retention for this type (simplified)
                        retention_by_type[context_type] = current_retention_rate

            # Calculate trend (comparing to previous measurements)
            measurements = session_data['retention_measurements']
            trend = 'stable'
            if len(measurements) > 1:
                prev_rate = measurements[-2].get('retention_rate', current_retention_rate)
                if current_retention_rate < prev_rate - 0.05:
                    trend = 'declining'
                elif current_retention_rate > prev_rate + 0.05:
                    trend = 'improving'

            return {
                'timestamp': datetime.now(),
                'transition_id': transition.transition_id,
                'retention_rate': current_retention_rate,
                'retention_by_type': retention_by_type,
                'trend': trend,
                'target_rate': self.target_retention_rate,
                'deviation_from_target': current_retention_rate - self.target_retention_rate,
                'is_acceptable': current_retention_rate >= self.target_retention_rate,
                'quality_level': transition.retention_quality.value,
                're_explanation_events': transition.re_explanation_events
            }

        except Exception as e:
            logger.error(f"Error calculating retention metrics: {e}")
            return None

    def validate_session_retention(self, session_id: str) -> dict:
        """Validate retention for a completed session."""
        if session_id not in self.current_session_data:
            return {'error': f'No session data found for {session_id}'}

        try:
            session_data = self.current_session_data[session_id]
            measurements = session_data['retention_measurements']

            if not measurements:
                return {
                    'session_id': session_id,
                    'validation_result': 'insufficient_data',
                    'message': 'No retention measurements recorded'
                }

            # Calculate overall metrics
            retention_rates = [m['retention_rate'] for m in measurements]
            avg_retention_rate = sum(retention_rates) / len(retention_rates)

            # Calculate statistical measures
            import math
            variance = sum((r - avg_retention_rate) ** 2 for r in retention_rates) / len(retention_rates)
            std_deviation = math.sqrt(variance)

            # Determine validation result
            validation_result = self._determine_validation_result(avg_retention_rate, std_deviation)

            # Generate alerts if needed
            alerts = self._check_alert_thresholds(session_id, avg_retention_rate)

            # Create validation report
            validation_report = {
                'session_id': session_id,
                'validation_timestamp': datetime.now().isoformat(),
                'validation_result': validation_result,
                'metrics': {
                    'average_retention_rate': avg_retention_rate,
                    'min_retention_rate': min(retention_rates),
                    'max_retention_rate': max(retention_rates),
                    'std_deviation': std_deviation,
                    'measurement_count': len(measurements),
                    'target_rate': self.target_retention_rate,
                    'deviation_from_target': avg_retention_rate - self.target_retention_rate,
                    'success_rate': sum(1 for m in measurements if m['is_acceptable']) / len(measurements)
                },
                'alerts': alerts,
                'recommendations': self._generate_recommendations(validation_result, avg_retention_rate),
                'detailed_measurements': measurements[-10:]  # Last 10 measurements
            }

            # Store in history
            self.validation_history.append(validation_report)

            # Clean up session data
            del self.current_session_data[session_id]

            # Keep only recent history
            max_history = 1000
            if len(self.validation_history) > max_history:
                self.validation_history = self.validation_history[-max_history:]

            logger.info(f"Session {session_id} validation completed: {validation_result}")
            return validation_report

        except Exception as e:
            logger.error(f"Error validating session retention: {e}")
            return {
                'session_id': session_id,
                'validation_result': 'error',
                'error_message': str(e)
            }

    def _determine_validation_result(self, avg_retention_rate: float, std_deviation: float) -> str:
        """Determine the validation result based on metrics."""
        if avg_retention_rate >= self.target_retention_rate:
            if std_deviation < 0.02:  # Low variance
                return 'excellent'
            else:
                return 'good'
        elif avg_retention_rate >= self.target_retention_rate - self.alert_thresholds['warning']:
            return 'acceptable'
        elif avg_retention_rate >= self.target_retention_rate - self.alert_thresholds['critical']:
            return 'needs_attention'
        else:
            return 'critical'

    def _check_alert_thresholds(self, session_id: str, retention_rate: float) -> List[dict]:
        """Check if retention rate triggers any alerts."""
        alerts = []

        try:
            deviation = self.target_retention_rate - retention_rate

            if deviation >= self.alert_thresholds['severe']:
                alerts.append({
                    'level': 'severe',
                    'message': f'Retention rate {retention_rate".1%"} is severely below target {self.target_retention_rate".1%"}',
                    'deviation': deviation,
                    'timestamp': datetime.now().isoformat()
                })
            elif deviation >= self.alert_thresholds['critical']:
                alerts.append({
                    'level': 'critical',
                    'message': f'Retention rate {retention_rate".1%"} is critically below target {self.target_retention_rate".1%"}',
                    'deviation': deviation,
                    'timestamp': datetime.now().isoformat()
                })
            elif deviation >= self.alert_thresholds['warning']:
                alerts.append({
                    'level': 'warning',
                    'message': f'Retention rate {retention_rate".1%"} is below target {self.target_retention_rate".1%"}',
                    'deviation': deviation,
                    'timestamp': datetime.now().isoformat()
                })

            # Store alerts in session data
            if session_id in self.current_session_data:
                self.current_session_data[session_id]['alerts_triggered'].extend(alerts)

        except Exception as e:
            logger.error(f"Error checking alert thresholds: {e}")

        return alerts

    def _generate_recommendations(self, validation_result: str, retention_rate: float) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []

        if validation_result == 'excellent':
            recommendations.append("Continue current practices - retention performance is excellent")
        elif validation_result == 'good':
            recommendations.append("Retention performance is good, consider minor optimizations")
        elif validation_result == 'acceptable':
            recommendations.append("Review context prioritization settings")
            recommendations.append("Consider increasing cache sizes for better retention")
        elif validation_result == 'needs_attention':
            recommendations.append("Immediate attention needed - review context management strategy")
            recommendations.append("Check for memory pressure or storage issues")
            recommendations.append("Review context eviction policies")
        elif validation_result == 'critical':
            recommendations.append("Critical retention issues - immediate action required")
            recommendations.append("Review and optimize context storage configuration")
            recommendations.append("Check system resources and memory availability")
            recommendations.append("Consider reducing context retention requirements if appropriate")

        # Specific recommendations based on retention rate
        if retention_rate < 0.8:
            recommendations.append("Consider implementing context compression to improve retention")
        if retention_rate < 0.7:
            recommendations.append("Review context importance scoring algorithm")

        return recommendations

    def get_retention_summary(self, days: int = 7) -> dict:
        """Get retention summary for the specified number of days."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)

            # Filter recent validations
            recent_validations = [
                v for v in self.validation_history
                if datetime.fromisoformat(v['validation_timestamp']) >= cutoff_date
            ]

            if not recent_validations:
                return {
                    'period_days': days,
                    'total_sessions': 0,
                    'message': 'No validation data available for the specified period'
                }

            # Calculate summary statistics
            retention_rates = [v['metrics']['average_retention_rate'] for v in recent_validations]
            validation_results = [v['validation_result'] for v in recent_validations]

            # Count results by category
            result_counts = defaultdict(int)
            for result in validation_results:
                result_counts[result] += 1

            # Calculate trends
            if len(retention_rates) >= 2:
                older_rates = retention_rates[:len(retention_rates)//2]
                newer_rates = retention_rates[len(retention_rates)//2:]

                older_avg = sum(older_rates) / len(older_rates)
                newer_avg = sum(newer_rates) / len(newer_rates)

                if newer_avg > older_avg + 0.02:
                    trend = 'improving'
                elif newer_avg < older_avg - 0.02:
                    trend = 'declining'
                else:
                    trend = 'stable'
            else:
                trend = 'insufficient_data'

            return {
                'period_days': days,
                'total_sessions': len(recent_validations),
                'summary': {
                    'average_retention_rate': sum(retention_rates) / len(retention_rates),
                    'min_retention_rate': min(retention_rates),
                    'max_retention_rate': max(retention_rates),
                    'target_achievement_rate': sum(1 for v in recent_validations if v['validation_result'] in ['excellent', 'good']) / len(recent_validations),
                    'trend': trend
                },
                'validation_distribution': dict(result_counts),
                'alert_summary': self._get_alert_summary(recent_validations),
                'recommendations': self._generate_period_recommendations(result_counts, trend)
            }

        except Exception as e:
            logger.error(f"Error generating retention summary: {e}")
            return {
                'period_days': days,
                'error': str(e)
            }

    def _get_alert_summary(self, validations: List[dict]) -> dict:
        """Get summary of alerts from validation data."""
        all_alerts = []
        for validation in validations:
            all_alerts.extend(validation.get('alerts', []))

        if not all_alerts:
            return {'total_alerts': 0}

        # Count alerts by level
        alert_counts = defaultdict(int)
        for alert in all_alerts:
            alert_counts[alert['level']] += 1

        return {
            'total_alerts': len(all_alerts),
            'alerts_by_level': dict(alert_counts),
            'most_common_level': max(alert_counts, key=alert_counts.get) if alert_counts else None
        }

    def _generate_period_recommendations(self, result_counts: dict, trend: str) -> List[str]:
        """Generate recommendations for the period."""
        recommendations = []

        excellent_count = result_counts.get('excellent', 0)
        good_count = result_counts.get('good', 0)
        poor_count = result_counts.get('critical', 0) + result_counts.get('needs_attention', 0)

        total_sessions = sum(result_counts.values())

        if total_sessions == 0:
            return ["No data available for recommendations"]

        success_rate = (excellent_count + good_count) / total_sessions

        if success_rate >= 0.9:
            recommendations.append("Retention performance is excellent across the period")
        elif success_rate >= 0.7:
            recommendations.append("Retention performance is generally good with some areas for improvement")
        else:
            recommendations.append("Significant retention issues identified - comprehensive review recommended")

        if trend == 'declining':
            recommendations.append("Retention trend is declining - investigate recent changes")
        elif trend == 'improving':
            recommendations.append("Retention trend is improving - continue current optimization efforts")

        if poor_count > 0:
            recommendations.append(f"Focus on the {poor_count} sessions with critical retention issues")

        return recommendations

    def validate_against_targets(self, transitions: List[SessionTransition]) -> dict:
        """Validate a set of transitions against retention targets."""
        if not transitions:
            return {'error': 'No transitions provided for validation'}

        try:
            # Group transitions by type for targeted analysis
            transitions_by_type = defaultdict(list)
            for transition in transitions:
                transitions_by_type[transition.transition_type].append(transition)

            validation_results = {}

            # Overall validation
            overall_retention = sum(t.context_retention_rate for t in transitions) / len(transitions)
            validation_results['overall'] = {
                'retention_rate': overall_retention,
                'meets_target': overall_retention >= self.target_retention_rate,
                'deviation': overall_retention - self.target_retention_rate
            }

            # Critical context validation
            critical_transitions = [t for t in transitions if t.transition_type == TransitionType.CONTEXT_SAVE]
            if critical_transitions:
                critical_retention = sum(t.context_retention_rate for t in critical_transitions) / len(critical_transitions)
                validation_results['critical_context'] = {
                    'retention_rate': critical_retention,
                    'meets_target': critical_retention >= self.retention_targets['critical_context'],
                    'deviation': critical_retention - self.retention_targets['critical_context']
                }

            # Goal context validation (if we can identify goal-related transitions)
            goal_transitions = [t for t in transitions if 'goal' in str(t.notes).lower() or TransitionType.GOAL_TRANSITION in [t.transition_type]]
            if goal_transitions:
                goal_retention = sum(t.context_retention_rate for t in goal_transitions) / len(goal_transitions)
                validation_results['goal_context'] = {
                    'retention_rate': goal_retention,
                    'meets_target': goal_retention >= self.retention_targets['goal_context'],
                    'deviation': goal_retention - self.retention_targets['goal_context']
                }

            return {
                'validation_timestamp': datetime.now().isoformat(),
                'total_transitions': len(transitions),
                'target_retention_rate': self.target_retention_rate,
                'results': validation_results,
                'overall_assessment': self._assess_overall_validation(validation_results)
            }

        except Exception as e:
            logger.error(f"Error validating against targets: {e}")
            return {'error': str(e)}

    def _assess_overall_validation(self, validation_results: dict) -> str:
        """Assess overall validation results."""
        if 'error' in validation_results:
            return 'error'

        results = validation_results.get('results', {})

        # Check if all targets are met
        all_targets_met = all(
            details.get('meets_target', False)
            for details in results.values()
        )

        if all_targets_met:
            return 'all_targets_met'

        # Check if critical targets are met
        critical_met = results.get('overall', {}).get('meets_target', False)
        if not critical_met:
            return 'critical_targets_not_met'

        return 'some_targets_not_met'

    def export_validation_history(self, format: str = 'json') -> str:
        """Export validation history in specified format."""
        try:
            if format.lower() == 'json':
                return json.dumps(self.validation_history, indent=2, ensure_ascii=False, default=str)
            else:
                # Simple text format
                lines = ["Context Retention Validation History", "=" * 50, ""]

                for validation in self.validation_history[-20:]:  # Last 20 entries
                    lines.append(f"Session: {validation['session_id']}")
                    lines.append(f"Result: {validation['validation_result']}")
                    lines.append(f"Average Retention: {validation['metrics']['average_retention_rate']".1%"}")
                    lines.append(f"Timestamp: {validation['validation_timestamp']}")
                    lines.append("")

                return "\n".join(lines)

        except Exception as e:
            logger.error(f"Error exporting validation history: {e}")
            return f"Error: {str(e)}"
class TransitionMetricsCollector:
    """Collect performance and quality metrics during session transitions."""

    def __init__(self, config: Optional[dict] = None):
        self.config = self._get_default_config()
        if config:
            self.config.update(config)

        # Metrics storage
        self.performance_metrics: List[dict] = []
        self.quality_metrics: List[dict] = []
        self.system_metrics: List[dict] = []
        self.context_metrics: List[dict] = []

        # Real-time tracking
        self.current_session_metrics: Dict[str, dict] = {}
        self.metrics_lock = threading.Lock()

        # Aggregation windows
        self.aggregation_windows = {
            'minute': 60,
            'hour': 3600,
            'day': 86400,
            'week': 604800
        }

        # Performance baselines
        self.baselines = self._initialize_baselines()

        logger.info("TransitionMetricsCollector initialized")

    def _get_default_config(self) -> dict:
        """Get default configuration for the metrics collector."""
        return {
            'collection_interval_seconds': 10,
            'max_metrics_age_hours': 24,
            'enable_system_metrics': True,
            'enable_performance_monitoring': True,
            'enable_quality_tracking': True,
            'enable_context_analysis': True,
            'metrics_buffer_size': 1000,
            'aggregation_enabled': True,
            'baseline_update_interval_hours': 1
        }

    def _initialize_baselines(self) -> dict:
        """Initialize performance baselines."""
        return {
            'transition_duration_ms': {'p50': 100, 'p95': 500, 'p99': 1000},
            'memory_usage_mb': {'current': 0, 'baseline': 0},
            'cpu_usage_percent': {'current': 0, 'baseline': 0},
            'context_retention_rate': {'baseline': 0.95},
            're_explanation_rate': {'baseline': 0.05}
        }

    def start_session_collection(self, session_id: str) -> None:
        """Start collecting metrics for a new session."""
        with self.metrics_lock:
            self.current_session_metrics[session_id] = {
                'start_time': datetime.now(),
                'performance_samples': [],
                'quality_samples': [],
                'system_samples': [],
                'context_samples': [],
                'transition_events': [],
                'baseline_violations': []
            }

        logger.debug(f"Started metrics collection for session {session_id}")

    def record_performance_metrics(self, session_id: str, transition_duration_ms: float,
                                 memory_before_mb: float, memory_after_mb: float,
                                 cpu_usage_percent: float) -> None:
        """Record performance metrics for a transition."""
        if session_id not in self.current_session_metrics:
            logger.warning(f"No session found for metrics recording: {session_id}")
            return

        try:
            metrics = {
                'timestamp': datetime.now(),
                'session_id': session_id,
                'transition_duration_ms': transition_duration_ms,
                'memory_usage_before_mb': memory_before_mb,
                'memory_usage_after_mb': memory_after_mb,
                'memory_delta_mb': memory_after_mb - memory_before_mb,
                'cpu_usage_percent': cpu_usage_percent,
                'is_performance_regression': self._check_performance_regression(transition_duration_ms)
            }

            # Store in session data
            self.current_session_metrics[session_id]['performance_samples'].append(metrics)

            # Store globally
            with self.metrics_lock:
                self.performance_metrics.append(metrics)

                # Maintain buffer size
                if len(self.performance_metrics) > self.config['metrics_buffer_size']:
                    self.performance_metrics = self.performance_metrics[-self.config['metrics_buffer_size']:]

            # Check for baseline violations
            if metrics['is_performance_regression']:
                self.current_session_metrics[session_id]['baseline_violations'].append({
                    'type': 'performance',
                    'metric': 'transition_duration_ms',
                    'value': transition_duration_ms,
                    'baseline': self.baselines['transition_duration_ms']['p95'],
                    'timestamp': metrics['timestamp']
                })

        except Exception as e:
            logger.error(f"Error recording performance metrics: {e}")

    def record_quality_metrics(self, session_id: str, retention_rate: float,
                             re_explanation_events: int, user_satisfaction: Optional[float] = None,
                             error_count: int = 0) -> None:
        """Record quality metrics for a transition."""
        if session_id not in self.current_session_metrics:
            logger.warning(f"No session found for quality metrics recording: {session_id}")
            return

        try:
            metrics = {
                'timestamp': datetime.now(),
                'session_id': session_id,
                'context_retention_rate': retention_rate,
                're_explanation_events': re_explanation_events,
                're_explanation_rate': re_explanation_events / max(1, re_explanation_events),  # Simplified
                'user_satisfaction_score': user_satisfaction,
                'error_count': error_count,
                'quality_score': self._calculate_quality_score(retention_rate, re_explanation_events, user_satisfaction, error_count),
                'is_quality_regression': self._check_quality_regression(retention_rate)
            }

            # Store in session data
            self.current_session_metrics[session_id]['quality_samples'].append(metrics)

            # Store globally
            with self.metrics_lock:
                self.quality_metrics.append(metrics)

                # Maintain buffer size
                if len(self.quality_metrics) > self.config['metrics_buffer_size']:
                    self.quality_metrics = self.quality_metrics[-self.config['metrics_buffer_size']:]

            # Check for baseline violations
            if metrics['is_quality_regression']:
                self.current_session_metrics[session_id]['baseline_violations'].append({
                    'type': 'quality',
                    'metric': 'context_retention_rate',
                    'value': retention_rate,
                    'baseline': self.baselines['context_retention_rate']['baseline'],
                    'timestamp': metrics['timestamp']
                })

        except Exception as e:
            logger.error(f"Error recording quality metrics: {e}")

    def record_system_metrics(self, session_id: str) -> None:
        """Record system-level metrics."""
        if not self.config['enable_system_metrics']:
            return

        if session_id not in self.current_session_metrics:
            logger.warning(f"No session found for system metrics recording: {session_id}")
            return

        try:
            metrics = {
                'timestamp': datetime.now(),
                'session_id': session_id,
                'memory_available_mb': self._get_memory_available(),
                'disk_space_available_gb': self._get_disk_space_available(),
                'cpu_count': self._get_cpu_count(),
                'system_load_average': self._get_system_load_average()
            }

            # Store in session data
            self.current_session_metrics[session_id]['system_samples'].append(metrics)

            # Store globally
            with self.metrics_lock:
                self.system_metrics.append(metrics)

                # Maintain buffer size
                if len(self.system_metrics) > self.config['metrics_buffer_size']:
                    self.system_metrics = self.system_metrics[-self.config['metrics_buffer_size']:]

        except Exception as e:
            logger.error(f"Error recording system metrics: {e}")

    def record_context_metrics(self, session_id: str, context_count: int,
                             context_types: Optional[Dict[str, int]] = None,
                             context_sizes: Optional[Dict[str, float]] = None) -> None:
        """Record context-specific metrics."""
        if not self.config['enable_context_analysis']:
            return

        if session_id not in self.current_session_metrics:
            logger.warning(f"No session found for context metrics recording: {session_id}")
            return

        try:
            metrics = {
                'timestamp': datetime.now(),
                'session_id': session_id,
                'total_context_objects': context_count,
                'context_types': context_types or {},
                'context_sizes': context_sizes or {},
                'context_diversity_score': self._calculate_context_diversity(context_types or {}),
                'average_context_size_mb': self._calculate_average_context_size(context_sizes or {})
            }

            # Store in session data
            self.current_session_metrics[session_id]['context_samples'].append(metrics)

            # Store globally
            with self.metrics_lock:
                self.context_metrics.append(metrics)

                # Maintain buffer size
                if len(self.context_metrics) > self.config['metrics_buffer_size']:
                    self.context_metrics = self.context_metrics[-self.config['metrics_buffer_size']:]

        except Exception as e:
            logger.error(f"Error recording context metrics: {e}")

    def record_transition_event(self, session_id: str, transition: SessionTransition) -> None:
        """Record a complete transition event with all metrics."""
        if session_id not in self.current_session_metrics:
            logger.warning(f"No session found for transition event recording: {session_id}")
            return

        try:
            # Record all types of metrics for this transition
            self.record_performance_metrics(
                session_id,
                transition.transition_duration_ms,
                transition.memory_usage_before_mb,
                transition.memory_usage_after_mb,
                transition.cpu_usage_percent
            )

            self.record_quality_metrics(
                session_id,
                transition.context_retention_rate,
                transition.re_explanation_events,
                transition.user_satisfaction_score,
                transition.error_count
            )

            if self.config['enable_system_metrics']:
                self.record_system_metrics(session_id)

            if self.config['enable_context_analysis']:
                # Extract context information from transition if available
                context_types = getattr(transition, 'context_types', None)
                context_sizes = getattr(transition, 'context_sizes', None)
                self.record_context_metrics(
                    session_id,
                    transition.context_objects_loaded + transition.context_objects_saved,
                    context_types,
                    context_sizes
                )

            # Store transition event
            self.current_session_metrics[session_id]['transition_events'].append({
                'timestamp': datetime.now(),
                'transition_id': transition.transition_id,
                'transition_type': transition.transition_type.value,
                'status': transition.status.value,
                'efficiency_score': transition.calculate_transition_efficiency()
            })

        except Exception as e:
            logger.error(f"Error recording transition event: {e}")

    def _check_performance_regression(self, duration_ms: float) -> bool:
        """Check if performance metric indicates a regression."""
        baseline = self.baselines['transition_duration_ms']['p95']
        return duration_ms > baseline * 1.5  # 50% over baseline

    def _check_quality_regression(self, retention_rate: float) -> bool:
        """Check if quality metric indicates a regression."""
        baseline = self.baselines['context_retention_rate']['baseline']
        return retention_rate < baseline * 0.9  # 10% under baseline

    def _calculate_quality_score(self, retention_rate: float, re_explanation_events: int,
                               user_satisfaction: Optional[float], error_count: int) -> float:
        """Calculate overall quality score from multiple factors."""
        score = retention_rate * 0.4

        # Re-explanation penalty
        re_explanation_penalty = min(re_explanation_events * 0.1, 0.3)
        score -= re_explanation_penalty

        # User satisfaction factor
        if user_satisfaction is not None:
            satisfaction_factor = user_satisfaction / 10.0  # Normalize to 0-1
            score = score * 0.7 + satisfaction_factor * 0.3

        # Error penalty
        error_penalty = min(error_count * 0.05, 0.2)
        score -= error_penalty

        return max(0.0, min(1.0, score))

    def _calculate_context_diversity(self, context_types: Dict[str, int]) -> float:
        """Calculate diversity score for context types."""
        if not context_types:
            return 0.0

        total_contexts = sum(context_types.values())
        if total_contexts == 0:
            return 0.0

        # Shannon diversity index
        import math
        diversity = 0.0
        for count in context_types.values():
            if count > 0:
                proportion = count / total_contexts
                diversity -= proportion * math.log2(proportion)

        # Normalize to 0-1 range
        max_diversity = math.log2(len(context_types)) if context_types else 1
        return diversity / max_diversity if max_diversity > 0 else 0.0

    def _calculate_average_context_size(self, context_sizes: Dict[str, float]) -> float:
        """Calculate average context size in MB."""
        if not context_sizes:
            return 0.0

        total_size = sum(context_sizes.values())
        return total_size / len(context_sizes)

    def get_session_metrics_summary(self, session_id: str) -> dict:
        """Get comprehensive metrics summary for a session."""
        if session_id not in self.current_session_metrics:
            return {'error': f'No metrics found for session {session_id}'}

        try:
            session_data = self.current_session_metrics[session_id]

            # Aggregate performance metrics
            performance_samples = session_data['performance_samples']
            performance_summary = self._aggregate_performance_metrics(performance_samples)

            # Aggregate quality metrics
            quality_samples = session_data['quality_samples']
            quality_summary = self._aggregate_quality_metrics(quality_samples)

            # Aggregate system metrics
            system_samples = session_data['system_samples']
            system_summary = self._aggregate_system_metrics(system_samples)

            # Aggregate context metrics
            context_samples = session_data['context_samples']
            context_summary = self._aggregate_context_metrics(context_samples)

            # Calculate session duration
            session_duration = (datetime.now() - session_data['start_time']).total_seconds()

            return {
                'session_id': session_id,
                'session_duration_seconds': session_duration,
                'sample_counts': {
                    'performance': len(performance_samples),
                    'quality': len(quality_samples),
                    'system': len(system_samples),
                    'context': len(context_samples)
                },
                'performance': performance_summary,
                'quality': quality_summary,
                'system': system_summary,
                'context': context_summary,
                'baseline_violations': session_data['baseline_violations'],
                'transition_count': len(session_data['transition_events']),
                'overall_health_score': self._calculate_session_health_score(
                    performance_summary, quality_summary, session_data['baseline_violations']
                )
            }

        except Exception as e:
            logger.error(f"Error generating session metrics summary: {e}")
            return {'error': str(e)}

    def _aggregate_performance_metrics(self, samples: List[dict]) -> dict:
        """Aggregate performance metrics."""
        if not samples:
            return {}

        durations = [s['transition_duration_ms'] for s in samples]
        memory_deltas = [s['memory_delta_mb'] for s in samples]
        cpu_usages = [s['cpu_usage_percent'] for s in samples]

        return {
            'avg_transition_duration_ms': sum(durations) / len(durations),
            'min_transition_duration_ms': min(durations),
            'max_transition_duration_ms': max(durations),
            'avg_memory_delta_mb': sum(memory_deltas) / len(memory_deltas),
            'avg_cpu_usage_percent': sum(cpu_usages) / len(cpu_usages),
            'performance_regression_count': sum(1 for s in samples if s['is_performance_regression'])
        }

    def _aggregate_quality_metrics(self, samples: List[dict]) -> dict:
        """Aggregate quality metrics."""
        if not samples:
            return {}

        retention_rates = [s['context_retention_rate'] for s in samples]
        quality_scores = [s['quality_score'] for s in samples]
        re_explanation_events = [s['re_explanation_events'] for s in samples]
        error_counts = [s['error_count'] for s in samples]

        return {
            'avg_retention_rate': sum(retention_rates) / len(retention_rates),
            'min_retention_rate': min(retention_rates),
            'max_retention_rate': max(retention_rates),
            'avg_quality_score': sum(quality_scores) / len(quality_scores),
            'total_re_explanation_events': sum(re_explanation_events),
            'total_errors': sum(error_counts),
            'quality_regression_count': sum(1 for s in samples if s['is_quality_regression'])
        }

    def _aggregate_system_metrics(self, samples: List[dict]) -> dict:
        """Aggregate system metrics."""
        if not samples:
            return {}

        memory_available = [s['memory_available_mb'] for s in samples]
        disk_space = [s['disk_space_available_gb'] for s in samples]

        return {
            'avg_memory_available_mb': sum(memory_available) / len(memory_available),
            'min_memory_available_mb': min(memory_available),
            'avg_disk_space_available_gb': sum(disk_space) / len(disk_space),
            'min_disk_space_available_gb': min(disk_space)
        }

    def _aggregate_context_metrics(self, samples: List[dict]) -> dict:
        """Aggregate context metrics."""
        if not samples:
            return {}

        total_contexts = [s['total_context_objects'] for s in samples]
        diversity_scores = [s['context_diversity_score'] for s in samples]

        return {
            'avg_context_objects': sum(total_contexts) / len(total_contexts),
            'max_context_objects': max(total_contexts),
            'avg_context_diversity': sum(diversity_scores) / len(diversity_scores),
            'context_type_distribution': self._get_context_type_distribution(samples)
        }

    def _get_context_type_distribution(self, samples: List[dict]) -> dict:
        """Get distribution of context types across samples."""
        type_counts = defaultdict(int)

        for sample in samples:
            for context_type, count in sample.get('context_types', {}).items():
                type_counts[context_type] += count

        return dict(type_counts)

    def _calculate_session_health_score(self, performance_summary: dict,
                                      quality_summary: dict, violations: List[dict]) -> float:
        """Calculate overall health score for a session."""
        score = 0.5  # Base score

        # Performance factor (lower duration = higher score)
        if 'avg_transition_duration_ms' in performance_summary:
            duration = performance_summary['avg_transition_duration_ms']
            if duration < 100:
                score += 0.2
            elif duration < 500:
                score += 0.1
            elif duration > 2000:
                score -= 0.2

        # Quality factor
        if 'avg_retention_rate' in quality_summary:
            retention = quality_summary['avg_retention_rate']
            score += retention * 0.3

        # Violation penalty
        if violations:
            score -= len(violations) * 0.05

        return max(0.0, min(1.0, score))

    def get_aggregated_metrics(self, time_window_seconds: int = 3600) -> dict:
        """Get aggregated metrics for the specified time window."""
        try:
            cutoff_time = datetime.now() - timedelta(seconds=time_window_seconds)

            # Filter recent metrics
            recent_performance = [
                m for m in self.performance_metrics
                if m['timestamp'] >= cutoff_time
            ]

            recent_quality = [
                m for m in self.quality_metrics
                if m['timestamp'] >= cutoff_time
            ]

            # Aggregate metrics
            aggregated = {
                'time_window_seconds': time_window_seconds,
                'collection_timestamp': datetime.now().isoformat(),
                'sample_counts': {
                    'performance': len(recent_performance),
                    'quality': len(recent_quality)
                }
            }

            if recent_performance:
                aggregated['performance'] = self._aggregate_performance_metrics(recent_performance)

            if recent_quality:
                aggregated['quality'] = self._aggregate_quality_metrics(recent_quality)

            return aggregated

        except Exception as e:
            logger.error(f"Error getting aggregated metrics: {e}")
            return {'error': str(e)}

    def update_baselines(self) -> None:
        """Update performance baselines based on recent data."""
        try:
            # Update performance baselines
            if len(self.performance_metrics) >= 50:  # Need sufficient data
                recent_durations = [
                    m['transition_duration_ms']
                    for m in self.performance_metrics[-1000:]  # Last 1000 samples
                ]

                recent_durations.sort()
                n = len(recent_durations)

                self.baselines['transition_duration_ms'] = {
                    'p50': recent_durations[int(n * 0.5)],
                    'p95': recent_durations[int(n * 0.95)],
                    'p99': recent_durations[int(n * 0.99)]
                }

            # Update quality baselines
            if len(self.quality_metrics) >= 50:
                recent_retention = [
                    m['context_retention_rate']
                    for m in self.quality_metrics[-1000:]
                ]

                self.baselines['context_retention_rate']['baseline'] = sum(recent_retention) / len(recent_retention)

            logger.debug("Performance baselines updated")

        except Exception as e:
            logger.error(f"Error updating baselines: {e}")

    def export_metrics(self, format: str = 'json', session_id: Optional[str] = None) -> str:
        """Export metrics in specified format."""
        try:
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'baselines': self.baselines,
                'config': self.config
            }

            if session_id:
                # Export specific session metrics
                if session_id in self.current_session_metrics:
                    export_data['session_metrics'] = self.current_session_metrics[session_id]
                else:
                    export_data['error'] = f'No metrics found for session {session_id}'
            else:
                # Export global metrics
                export_data.update({
                    'performance_metrics_count': len(self.performance_metrics),
                    'quality_metrics_count': len(self.quality_metrics),
                    'system_metrics_count': len(self.system_metrics),
                    'context_metrics_count': len(self.context_metrics),
                    'active_sessions': list(self.current_session_metrics.keys())
                })

            if format.lower() == 'json':
                return json.dumps(export_data, indent=2, ensure_ascii=False, default=str)
            else:
                # Simple text format
                lines = ["Transition Metrics Export", "=" * 30, ""]
                lines.append(f"Export Time: {export_data['export_timestamp']}")
                lines.append(f"Active Sessions: {len(export_data.get('active_sessions', []))}")
                lines.append(f"Total Metrics Collected: {sum(len(metrics) for metrics in [
                    self.performance_metrics, self.quality_metrics,
                    self.system_metrics, self.context_metrics
                ])}")
                lines.append("")
                return "\n".join(lines)

        except Exception as e:
            logger.error(f"Error exporting metrics: {e}")
            return f"Error: {str(e)}"

    def cleanup_old_metrics(self) -> int:
        """Clean up old metrics based on retention policy."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=self.config['max_metrics_age_hours'])

            # Clean up global metrics
            cleaned_count = 0

            for metrics_list in [self.performance_metrics, self.quality_metrics,
                               self.system_metrics, self.context_metrics]:
                original_count = len(metrics_list)
                metrics_list[:] = [m for m in metrics_list if m['timestamp'] >= cutoff_time]
                cleaned_count += original_count - len(metrics_list)

            # Clean up old session data
            sessions_to_remove = []
            for session_id, session_data in self.current_session_metrics.items():
                session_age = datetime.now() - session_data['start_time']
                if session_age.total_seconds() > self.config['max_metrics_age_hours'] * 3600:
                    sessions_to_remove.append(session_id)

            for session_id in sessions_to_remove:
                del self.current_session_metrics[session_id]
                cleaned_count += 1

            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} old metrics")

            return cleaned_count

        except Exception as e:
            logger.error(f"Error during metrics cleanup: {e}")
            return 0

    def _get_memory_available(self) -> float:
        """Get available memory in MB."""
        try:
            import psutil
            return psutil.virtual_memory().available / (1024 * 1024)
        except ImportError:
            return 0.0
        except Exception:
            return 0.0

    def _get_disk_space_available(self) -> float:
        """Get available disk space in GB."""
        try:
            import shutil
            total, used, free = shutil.disk_usage(str(Path.home()))
            return free / (1024**3)
        except Exception:
            return 0.0

    def _get_cpu_count(self) -> int:
        """Get CPU count."""
        try:
            import multiprocessing
            return multiprocessing.cpu_count()
        except Exception:
            return 1

    def _get_system_load_average(self) -> float:
        """Get system load average."""
        try:
            import os
            if hasattr(os, 'getloadavg'):
                return os.getloadavg()[0]
            return 0.0
        except Exception:
            return 0.0

    def cleanup(self) -> None:
        """Clean up resources."""
        self.cleanup_old_metrics()
        logger.info("TransitionMetricsCollector cleanup completed")
class RetentionReportGenerator:
    """Generate detailed reports on retention performance and trends."""

    def __init__(self, logger: 'SessionTransitionLogger',
                 validator: 'ContextRetentionValidator',
                 metrics_collector: 'TransitionMetricsCollector',
                 config: Optional[dict] = None):
        self.logger = logger
        self.validator = validator
        self.metrics_collector = metrics_collector

        self.config = self._get_default_config()
        if config:
            self.config.update(config)

        # Report storage
        self.report_history: List[dict] = []
        self.report_templates = self._initialize_report_templates()

        logger.info("RetentionReportGenerator initialized")

    def _get_default_config(self) -> dict:
        """Get default configuration for the report generator."""
        return {
            'report_retention_days': 90,
            'auto_report_interval_hours': 24,
            'include_charts': True,
            'include_recommendations': True,
            'include_trend_analysis': True,
            'report_output_path': None,
            'enable_auto_reporting': False,
            'min_data_points_for_trends': 10
        }

    def _initialize_report_templates(self) -> dict:
        """Initialize report templates for different report types."""
        return {
            'daily_summary': {
                'title': 'Daily Context Retention Summary',
                'sections': ['overview', 'performance', 'quality', 'trends', 'recommendations']
            },
            'weekly_analysis': {
                'title': 'Weekly Context Retention Analysis',
                'sections': ['overview', 'detailed_metrics', 'trend_analysis', 'comparative_analysis', 'strategic_recommendations']
            },
            'session_report': {
                'title': 'Session Context Retention Report',
                'sections': ['session_overview', 'transition_details', 'retention_analysis', 'performance_metrics', 'improvement_suggestions']
            },
            'comprehensive_review': {
                'title': 'Comprehensive Context Retention Review',
                'sections': ['executive_summary', 'detailed_analysis', 'historical_trends', 'benchmarking', 'strategic_planning']
            }
        }

    def generate_daily_summary_report(self, date: Optional[datetime] = None) -> dict:
        """Generate a daily summary report."""
        if date is None:
            date = datetime.now()

        try:
            # Get data for the specified date
            start_of_day = datetime(date.year, date.month, date.day)
            end_of_day = start_of_day + timedelta(days=1)

            # Collect data from all sources
            day_transitions = self.logger.get_transitions_in_range(start_of_day, end_of_day)
            day_validation = self.validator.get_retention_summary(days=1)
            day_metrics = self.metrics_collector.get_aggregated_metrics(time_window_seconds=86400)

            # Generate report sections
            report = {
                'report_type': 'daily_summary',
                'report_date': date.date().isoformat(),
                'generated_at': datetime.now().isoformat(),
                'data_period': {
                    'start': start_of_day.isoformat(),
                    'end': end_of_day.isoformat()
                }
            }

            # Overview section
            report['overview'] = self._generate_overview_section(day_transitions, day_validation)

            # Performance section
            report['performance'] = self._generate_performance_section(day_transitions, day_metrics)

            # Quality section
            report['quality'] = self._generate_quality_section(day_transitions, day_validation)

            # Trends section (if enough data)
            if len(day_transitions) >= self.config['min_data_points_for_trends']:
                report['trends'] = self._generate_trends_section(day_transitions)

            # Recommendations section
            if self.config['include_recommendations']:
                report['recommendations'] = self._generate_recommendations_section(day_validation, day_transitions)

            # Store in history
            self.report_history.append(report)

            # Keep only recent reports
            max_reports = 100
            if len(self.report_history) > max_reports:
                self.report_history = self.report_history[-max_reports:]

            logger.info(f"Generated daily summary report for {date.date()}")
            return report

        except Exception as e:
            logger.error(f"Error generating daily summary report: {e}")
            return {'error': str(e)}

    def generate_session_report(self, session_id: str) -> dict:
        """Generate a detailed report for a specific session."""
        try:
            # Get session data from all sources
            session_transitions = self.logger.get_session_transitions(session_id)
            session_metrics = self.metrics_collector.get_session_metrics_summary(session_id)

            if not session_transitions:
                return {'error': f'No transitions found for session {session_id}'}

            # Generate report sections
            report = {
                'report_type': 'session_report',
                'session_id': session_id,
                'generated_at': datetime.now().isoformat(),
                'transition_count': len(session_transitions)
            }

            # Session overview
            report['session_overview'] = self._generate_session_overview(session_transitions)

            # Transition details
            report['transition_details'] = self._generate_transition_details(session_transitions)

            # Retention analysis
            report['retention_analysis'] = self._generate_retention_analysis(session_transitions)

            # Performance metrics
            if 'error' not in session_metrics:
                report['performance_metrics'] = session_metrics

            # Improvement suggestions
            if self.config['include_recommendations']:
                report['improvement_suggestions'] = self._generate_session_improvements(session_transitions, session_metrics)

            logger.info(f"Generated session report for {session_id}")
            return report

        except Exception as e:
            logger.error(f"Error generating session report: {e}")
            return {'error': str(e)}

    def generate_weekly_analysis_report(self, end_date: Optional[datetime] = None) -> dict:
        """Generate a comprehensive weekly analysis report."""
        if end_date is None:
            end_date = datetime.now()

        try:
            start_of_week = end_date - timedelta(days=7)

            # Get data for the week
            week_transitions = self.logger.get_transitions_in_range(start_of_week, end_date)
            week_validation = self.validator.get_retention_summary(days=7)
            week_metrics = self.metrics_collector.get_aggregated_metrics(time_window_seconds=604800)

            report = {
                'report_type': 'weekly_analysis',
                'report_period': {
                    'start': start_of_week.date().isoformat(),
                    'end': end_date.date().isoformat()
                },
                'generated_at': datetime.now().isoformat(),
                'total_transitions': len(week_transitions)
            }

            # Overview section
            report['overview'] = self._generate_overview_section(week_transitions, week_validation)

            # Detailed metrics section
            report['detailed_metrics'] = self._generate_detailed_metrics_section(week_transitions, week_metrics)

            # Trend analysis section
            if self.config['include_trend_analysis'] and len(week_transitions) >= self.config['min_data_points_for_trends']:
                report['trend_analysis'] = self._generate_comprehensive_trends(week_transitions)

            # Comparative analysis
            report['comparative_analysis'] = self._generate_comparative_analysis(week_transitions)

            # Strategic recommendations
            if self.config['include_recommendations']:
                report['strategic_recommendations'] = self._generate_strategic_recommendations(week_validation, week_transitions)

            logger.info(f"Generated weekly analysis report for period ending {end_date.date()}")
            return report

        except Exception as e:
            logger.error(f"Error generating weekly analysis report: {e}")
            return {'error': str(e)}

    def _generate_overview_section(self, transitions: List[SessionTransition], validation: dict) -> dict:
        """Generate overview section for reports."""
        if not transitions:
            return {'message': 'No transition data available'}

        # Calculate basic statistics
        total_transitions = len(transitions)
        successful_transitions = sum(1 for t in transitions if t.is_successful_transition())
        avg_retention_rate = sum(t.context_retention_rate for t in transitions) / total_transitions

        # Calculate quality distribution
        quality_counts = defaultdict(int)
        for transition in transitions:
            quality_counts[transition.retention_quality.value] += 1

        return {
            'total_transitions': total_transitions,
            'successful_transitions': successful_transitions,
            'success_rate': successful_transitions / total_transitions,
            'average_retention_rate': avg_retention_rate,
            'quality_distribution': dict(quality_counts),
            'date_range': {
                'earliest': min(t.timestamp for t in transitions).isoformat(),
                'latest': max(t.timestamp for t in transitions).isoformat()
            },
            'validation_summary': validation.get('summary', {})
        }

    def _generate_performance_section(self, transitions: List[SessionTransition], metrics: dict) -> dict:
        """Generate performance section for reports."""
        if not transitions:
            return {'message': 'No performance data available'}

        # Performance metrics from transitions
        durations = [t.transition_duration_ms for t in transitions if t.transition_duration_ms > 0]
        memory_usages = [t.memory_usage_after_mb for t in transitions if t.memory_usage_after_mb > 0]

        performance_data = {
            'transition_performance': {
                'average_duration_ms': sum(durations) / len(durations) if durations else 0,
                'min_duration_ms': min(durations) if durations else 0,
                'max_duration_ms': max(durations) if durations else 0,
                'duration_trend': self._calculate_trend(durations)
            },
            'memory_usage': {
                'average_mb': sum(memory_usages) / len(memory_usages) if memory_usages else 0,
                'min_mb': min(memory_usages) if memory_usages else 0,
                'max_mb': max(memory_usages) if memory_usages else 0
            }
        }

        # Add metrics collector data if available
        if 'error' not in metrics and 'performance' in metrics:
            performance_data['aggregated_metrics'] = metrics['performance']

        return performance_data

    def _generate_quality_section(self, transitions: List[SessionTransition], validation: dict) -> dict:
        """Generate quality section for reports."""
        if not transitions:
            return {'message': 'No quality data available'}

        # Quality metrics from transitions
        retention_rates = [t.context_retention_rate for t in transitions]
        re_explanation_events = sum(t.re_explanation_events for t in transitions)
        error_counts = sum(t.error_count for t in transitions)

        # Calculate quality trends
        retention_trend = self._calculate_trend(retention_rates)

        quality_data = {
            'retention_metrics': {
                'average_rate': sum(retention_rates) / len(retention_rates),
                'min_rate': min(retention_rates),
                'max_rate': max(retention_rates),
                'retention_trend': retention_trend,
                'target_achievement_rate': sum(1 for r in retention_rates if r >= 0.95) / len(retention_rates)
            },
            'user_experience': {
                'total_re_explanations': re_explanation_events,
                're_explanation_rate': re_explanation_events / len(transitions),
                'total_errors': error_counts,
                'error_rate': error_counts / len(transitions)
            },
            'validation_results': validation
        }

        return quality_data

    def _generate_trends_section(self, transitions: List[SessionTransition]) -> dict:
        """Generate trends section for reports."""
        if len(transitions) < 5:
            return {'message': 'Insufficient data for trend analysis'}

        # Sort transitions by timestamp
        sorted_transitions = sorted(transitions, key=lambda x: x.timestamp)

        # Calculate retention trend over time
        retention_rates = [t.context_retention_rate for t in sorted_transitions]
        timestamps = [t.timestamp for t in sorted_transitions]

        # Simple linear trend calculation
        retention_trend = self._calculate_linear_trend(timestamps, retention_rates)

        # Calculate performance trend
        durations = [t.transition_duration_ms for t in sorted_transitions if t.transition_duration_ms > 0]
        performance_trend = self._calculate_linear_trend(timestamps[:len(durations)], durations)

        return {
            'retention_trend': {
                'direction': retention_trend['direction'],
                'slope': retention_trend['slope'],
                'strength': retention_trend['strength'],
                'data_points': len(retention_rates)
            },
            'performance_trend': {
                'direction': performance_trend['direction'],
                'slope': performance_trend['slope'],
                'strength': performance_trend['strength'],
                'data_points': len(durations)
            },
            'trend_period': {
                'start': timestamps[0].isoformat(),
                'end': timestamps[-1].isoformat()
            }
        }

    def _generate_recommendations_section(self, validation: dict, transitions: List[SessionTransition]) -> List[str]:
        """Generate recommendations section for reports."""
        recommendations = []

        if not transitions:
            return ["No data available for recommendations"]

        # Analyze current performance
        avg_retention = sum(t.context_retention_rate for t in transitions) / len(transitions)
        success_rate = sum(1 for t in transitions if t.is_successful_transition()) / len(transitions)

        # Generate recommendations based on analysis
        if avg_retention < 0.85:
            recommendations.append("Critical: Context retention is below acceptable levels. Immediate investigation required.")
            recommendations.append("Consider reviewing context storage configuration and memory allocation.")
            recommendations.append("Check for context eviction policies that may be too aggressive.")

        if success_rate < 0.9:
            recommendations.append("Warning: Transition success rate is below target. Review error patterns.")
            recommendations.append("Investigate common failure modes in transition logs.")

        # Performance recommendations
        slow_transitions = [t for t in transitions if t.transition_duration_ms > 1000]
        if slow_transitions:
            recommendations.append(f"Performance: {len(slow_transitions)} transitions exceeded 1 second. Consider optimization.")

        # Quality recommendations
        high_re_explanation = [t for t in transitions if t.re_explanation_events > 2]
        if high_re_explanation:
            recommendations.append("User Experience: High re-explanation rate detected. Review context relevance algorithms.")

        if not recommendations:
            recommendations.append("All metrics within acceptable ranges. Continue current practices.")

        return recommendations

    def _generate_session_overview(self, transitions: List[SessionTransition]) -> dict:
        """Generate session overview for session reports."""
        if not transitions:
            return {}

        first_transition = min(transitions, key=lambda x: x.timestamp)
        last_transition = max(transitions, key=lambda x: x.timestamp)

        return {
            'session_id': transitions[0].session_id,
            'user_id': transitions[0].user_id,
            'project_path': transitions[0].project_path,
            'session_duration': (last_transition.timestamp - first_transition.timestamp).total_seconds(),
            'transition_count': len(transitions),
            'session_period': {
                'start': first_transition.timestamp.isoformat(),
                'end': last_transition.timestamp.isoformat()
            }
        }

    def _generate_transition_details(self, transitions: List[SessionTransition]) -> List[dict]:
        """Generate detailed transition information for session reports."""
        return [
            {
                'transition_id': t.transition_id,
                'type': t.transition_type.value,
                'status': t.status.value,
                'timestamp': t.timestamp.isoformat(),
                'retention_rate': t.context_retention_rate,
                'duration_ms': t.transition_duration_ms,
                'quality': t.retention_quality.value,
                'efficiency_score': t.calculate_transition_efficiency()
            }
            for t in sorted(transitions, key=lambda x: x.timestamp)
        ]

    def _generate_retention_analysis(self, transitions: List[SessionTransition]) -> dict:
        """Generate retention analysis for session reports."""
        if not transitions:
            return {}

        retention_rates = [t.context_retention_rate for t in transitions]

        # Analyze retention patterns
        excellent_count = sum(1 for t in transitions if t.retention_quality.value == 'excellent')
        poor_count = sum(1 for t in transitions if t.retention_quality.value == 'poor')

        return {
            'overall_retention_rate': sum(retention_rates) / len(retention_rates),
            'retention_consistency': 1 - (max(retention_rates) - min(retention_rates)),  # Higher is better
            'quality_distribution': {
                'excellent': excellent_count,
                'good': sum(1 for t in transitions if t.retention_quality.value == 'good'),
                'fair': sum(1 for t in transitions if t.retention_quality.value == 'fair'),
                'poor': poor_count
            },
            'target_achievement': sum(1 for r in retention_rates if r >= 0.95) / len(retention_rates),
            'improvement_potential': poor_count / len(transitions)  # Lower is better
        }

    def _generate_session_improvements(self, transitions: List[SessionTransition], metrics: dict) -> List[str]:
        """Generate improvement suggestions for session reports."""
        suggestions = []

        if not transitions:
            return suggestions

        # Analyze areas for improvement
        avg_retention = sum(t.context_retention_rate for t in transitions) / len(transitions)

        if avg_retention < 0.9:
            suggestions.append("Focus on improving context retention through better prioritization")
            suggestions.append("Consider increasing memory allocation for context storage")

        # Check for performance issues
        slow_transitions = [t for t in transitions if t.transition_duration_ms > 2000]
        if slow_transitions:
            suggestions.append(f"Optimize {len(slow_transitions)} slow transitions detected")

        # Check for quality issues
        error_transitions = [t for t in transitions if t.error_count > 0]
        if error_transitions:
            suggestions.append(f"Address errors in {len(error_transitions)} transitions")

        if not suggestions:
            suggestions.append("Session performance is within acceptable parameters")

        return suggestions

    def _generate_detailed_metrics_section(self, transitions: List[SessionTransition], metrics: dict) -> dict:
        """Generate detailed metrics section for weekly reports."""
        detailed_metrics = {
            'transition_analysis': self._analyze_transition_patterns(transitions),
            'context_analysis': self._analyze_context_patterns(transitions),
            'performance_analysis': self._analyze_performance_patterns(transitions)
        }

        if 'error' not in metrics:
            detailed_metrics['aggregated_metrics'] = metrics

        return detailed_metrics

    def _generate_comprehensive_trends(self, transitions: List[SessionTransition]) -> dict:
        """Generate comprehensive trend analysis."""
        if len(transitions) < 10:
            return {'message': 'Insufficient data for comprehensive trend analysis'}

        # Sort by timestamp for trend analysis
        sorted_transitions = sorted(transitions, key=lambda x: x.timestamp)

        # Multiple trend calculations
        retention_rates = [t.context_retention_rate for t in sorted_transitions]
        timestamps = [t.timestamp for t in sorted_transitions]

        # Calculate various trend metrics
        retention_trend = self._calculate_linear_trend(timestamps, retention_rates)

        # Calculate moving averages
        window_size = min(7, len(retention_rates) // 3)
        moving_averages = self._calculate_moving_averages(retention_rates, window_size)

        return {
            'retention_trends': retention_trend,
            'moving_averages': moving_averages,
            'volatility_analysis': self._analyze_volatility(retention_rates),
            'pattern_recognition': self._recognize_patterns(retention_rates)
        }

    def _generate_comparative_analysis(self, transitions: List[SessionTransition]) -> dict:
        """Generate comparative analysis for weekly reports."""
        if len(transitions) < 5:
            return {'message': 'Insufficient data for comparative analysis'}

        # Group by transition type
        by_type = defaultdict(list)
        for transition in transitions:
            by_type[transition.transition_type].append(transition)

        # Compare performance across types
        type_comparison = {}
        for transition_type, type_transitions in by_type.items():
            if len(type_transitions) >= 3:  # Need minimum samples
                retention_rates = [t.context_retention_rate for t in type_transitions]
                durations = [t.transition_duration_ms for t in type_transitions if t.transition_duration_ms > 0]

                type_comparison[transition_type.value] = {
                    'count': len(type_transitions),
                    'avg_retention': sum(retention_rates) / len(retention_rates),
                    'retention_consistency': 1 - (max(retention_rates) - min(retention_rates)),
                    'avg_duration': sum(durations) / len(durations) if durations else 0
                }

        return {
            'by_transition_type': type_comparison,
            'best_performing_type': max(type_comparison.items(), key=lambda x: x[1]['avg_retention'])[0] if type_comparison else None,
            'most_consistent_type': max(type_comparison.items(), key=lambda x: x[1]['retention_consistency'])[0] if type_comparison else None
        }

    def _generate_strategic_recommendations(self, validation: dict, transitions: List[SessionTransition]) -> List[str]:
        """Generate strategic recommendations for weekly reports."""
        recommendations = []

        if not transitions:
            return recommendations

        # Long-term strategic analysis
        avg_retention = sum(t.context_retention_rate for t in transitions) / len(transitions)

        if avg_retention < 0.8:
            recommendations.append("STRATEGIC: Major retention overhaul needed. Consider architectural changes.")
            recommendations.append("Evaluate context storage mechanisms and consider distributed storage options.")
        elif avg_retention < 0.9:
            recommendations.append("TACTICAL: Focused improvements in context management and prioritization.")
            recommendations.append("Consider implementing advanced caching strategies and compression techniques.")
        else:
            recommendations.append("STRATEGIC: Current retention levels are good. Focus on optimization and scaling.")

        # Trend-based recommendations
        if len(transitions) >= 10:
            recent_transitions = transitions[-10:]
            older_transitions = transitions[:10]

            recent_avg = sum(t.context_retention_rate for t in recent_transitions) / len(recent_transitions)
            older_avg = sum(t.context_retention_rate for t in older_transitions) / len(older_transitions)

            if recent_avg < older_avg - 0.05:
                recommendations.append("DECLINING TREND: Recent performance decline detected. Immediate investigation required.")
            elif recent_avg > older_avg + 0.05:
                recommendations.append("IMPROVING TREND: Recent improvements detected. Continue current strategies.")

        return recommendations

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate simple trend direction."""
        if len(values) < 3:
            return 'insufficient_data'

        # Simple linear trend
        first_half = sum(values[:len(values)//2]) / (len(values)//2)
        second_half = sum(values[len(values)//2:]) / (len(values) - len(values)//2)

        if second_half > first_half + 0.02:
            return 'improving'
        elif second_half < first_half - 0.02:
            return 'declining'
        else:
            return 'stable'

    def _calculate_linear_trend(self, timestamps: List[datetime], values: List[float]) -> dict:
        """Calculate linear trend with statistical measures."""
        if len(values) < 3:
            return {'direction': 'insufficient_data', 'slope': 0, 'strength': 0}

        # Convert timestamps to numeric values (seconds since first)
        start_time = timestamps[0]
        time_numeric = [(t - start_time).total_seconds() for t in timestamps]

        # Simple linear regression
        n = len(values)
        sum_x = sum(time_numeric)
        sum_y = sum(values)
        sum_xy = sum(x * y for x, y in zip(time_numeric, values))
        sum_x2 = sum(x * x for x in time_numeric)

        # Calculate slope
        denominator = n * sum_x2 - sum_x * sum_x
        if denominator == 0:
            slope = 0
        else:
            slope = (n * sum_xy - sum_x * sum_y) / denominator

        # Calculate correlation coefficient (trend strength)
        mean_x = sum_x / n
        mean_y = sum_y / n

        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(time_numeric, values))
        denominator_x = sum((x - mean_x) ** 2 for x in time_numeric)
        denominator_y = sum((y - mean_y) ** 2 for y in values)

        if denominator_x == 0 or denominator_y == 0:
            correlation = 0
        else:
            correlation = numerator / (denominator_x ** 0.5 * denominator_y ** 0.5)

        # Determine direction
        if slope > 0.001:
            direction = 'improving'
        elif slope < -0.001:
            direction = 'declining'
        else:
            direction = 'stable'

        return {
            'direction': direction,
            'slope': slope,
            'strength': abs(correlation),
            'correlation': correlation
        }

    def _calculate_moving_averages(self, values: List[float], window_size: int) -> List[float]:
        """Calculate moving averages for trend smoothing."""
        if len(values) < window_size:
            return []

        moving_averages = []
        for i in range(window_size - 1, len(values)):
            window = values[i - window_size + 1:i + 1]
            moving_averages.append(sum(window) / len(window))

        return moving_averages

    def _analyze_volatility(self, values: List[float]) -> dict:
        """Analyze volatility in retention rates."""
        if len(values) < 5:
            return {'volatility_level': 'insufficient_data'}

        # Calculate standard deviation
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5

        # Determine volatility level
        if std_dev < 0.05:
            volatility_level = 'low'
        elif std_dev < 0.1:
            volatility_level = 'moderate'
        else:
            volatility_level = 'high'

        return {
            'volatility_level': volatility_level,
            'standard_deviation': std_dev,
            'coefficient_of_variation': std_dev / mean if mean > 0 else 0
        }

    def _recognize_patterns(self, values: List[float]) -> List[str]:
        """Recognize patterns in retention data."""
        patterns = []

        if len(values) < 5:
            return patterns

        # Simple pattern recognition
        increasing_count = sum(1 for i in range(1, len(values)) if values[i] > values[i-1])
        decreasing_count = sum(1 for i in range(1, len(values)) if values[i] < values[i-1])

        if increasing_count >= len(values) * 0.7:
            patterns.append('consistently_increasing')
        elif decreasing_count >= len(values) * 0.7:
            patterns.append('consistently_decreasing')
        elif increasing_count > decreasing_count:
            patterns.append('generally_increasing')
        elif decreasing_count > increasing_count:
            patterns.append('generally_decreasing')
        else:
            patterns.append('mixed_pattern')

        return patterns

    def _analyze_transition_patterns(self, transitions: List[SessionTransition]) -> dict:
        """Analyze patterns in transition data."""
        if not transitions:
            return {}

        # Group by transition type
        by_type = defaultdict(list)
        for transition in transitions:
            by_type[transition.transition_type].append(transition)

        # Analyze each type
        type_analysis = {}
        for transition_type, type_transitions in by_type.items():
            if len(type_transitions) >= 3:
                retention_rates = [t.context_retention_rate for t in type_transitions]
                durations = [t.transition_duration_ms for t in type_transitions if t.transition_duration_ms > 0]

                type_analysis[transition_type.value] = {
                    'frequency': len(type_transitions),
                    'avg_retention': sum(retention_rates) / len(retention_rates),
                    'retention_stability': 1 - (max(retention_rates) - min(retention_rates)),
                    'avg_duration': sum(durations) / len(durations) if durations else 0
                }

        return type_analysis

    def _analyze_context_patterns(self, transitions: List[SessionTransition]) -> dict:
        """Analyze context-related patterns."""
        context_analysis = {
            'total_context_objects': sum(t.context_objects_loaded + t.context_objects_saved for t in transitions),
            'context_operations': {
                'loaded': sum(t.context_objects_loaded for t in transitions),
                'saved': sum(t.context_objects_saved for t in transitions),
                'evicted': sum(t.context_objects_evicted for t in transitions),
                'merged': sum(t.context_objects_merged for t in transitions)
            }
        }

        # Analyze context efficiency
        if context_analysis['total_context_objects'] > 0:
            successful_operations = sum(
                t.context_objects_loaded + t.context_objects_saved
                for t in transitions
                if t.is_successful_transition()
            )
            context_analysis['context_efficiency'] = successful_operations / context_analysis['total_context_objects']

        return context_analysis

    def _analyze_performance_patterns(self, transitions: List[SessionTransition]) -> dict:
        """Analyze performance patterns."""
        durations = [t.transition_duration_ms for t in transitions if t.transition_duration_ms > 0]

        if not durations:
            return {}

        return {
            'duration_statistics': {
                'mean': sum(durations) / len(durations),
                'median': sorted(durations)[len(durations) // 2],
                'min': min(durations),
                'max': max(durations),
                'p95': sorted(durations)[int(len(durations) * 0.95)]
            },
            'performance_classification': self._classify_performance(durations)
        }

    def _classify_performance(self, durations: List[float]) -> dict:
        """Classify performance levels."""
        if not durations:
            return {}

        mean_duration = sum(durations) / len(durations)

        # Classify based on duration thresholds
        fast_count = sum(1 for d in durations if d < 100)
        moderate_count = sum(1 for d in durations if 100 <= d < 1000)
        slow_count = sum(1 for d in durations if d >= 1000)

        return {
            'fast_transitions': fast_count,
            'moderate_transitions': moderate_count,
            'slow_transitions': slow_count,
            'overall_performance': 'good' if mean_duration < 500 else ('moderate' if mean_duration < 2000 else 'poor')
        }

    def export_report(self, report: dict, format: str = 'json') -> str:
        """Export a report in the specified format."""
        try:
            if format.lower() == 'json':
                return json.dumps(report, indent=2, ensure_ascii=False, default=str)
            elif format.lower() == 'text':
                return self._format_report_as_text(report)
            elif format.lower() == 'markdown':
                return self._format_report_as_markdown(report)
            else:
                return f"Unsupported format: {format}"

        except Exception as e:
            logger.error(f"Error exporting report: {e}")
            return f"Error: {str(e)}"

    def _format_report_as_text(self, report: dict) -> str:
        """Format report as plain text."""
        lines = []
        lines.append(f"Context Retention Report")
        lines.append(f"Type: {report.get('report_type', 'Unknown')}")
        lines.append(f"Generated: {report.get('generated_at', 'Unknown')}")
        lines.append("")

        # Add sections based on report type
        if 'overview' in report:
            lines.append("OVERVIEW")
            lines.append("-" * 20)
            overview = report['overview']
            lines.append(f"Total Transitions: {overview.get('total_transitions', 0)}")
            lines.append(f"Success Rate: {overview.get('success_rate', 0)".1%"}")
            lines.append(f"Average Retention: {overview.get('average_retention_rate', 0)".1%"}")
            lines.append("")

        if 'recommendations' in report:
            lines.append("RECOMMENDATIONS")
            lines.append("-" * 20)
            for rec in report['recommendations']:
                lines.append(f"• {rec}")
            lines.append("")

        return "\n".join(lines)

    def _format_report_as_markdown(self, report: dict) -> str:
        """Format report as Markdown."""
        lines = []
        lines.append(f"# Context Retention Report")
        lines.append("")
        lines.append(f"**Type:** {report.get('report_type', 'Unknown')}  ")
        lines.append(f"**Generated:** {report.get('generated_at', 'Unknown')}  ")
        lines.append("")

        # Add sections based on report type
        if 'overview' in report:
            lines.append("## Overview")
            lines.append("")
            overview = report['overview']
            lines.append(f"- **Total Transitions:** {overview.get('total_transitions', 0)}")
            lines.append(f"- **Success Rate:** {overview.get('success_rate', 0)".1%"}")
            lines.append(f"- **Average Retention:** {overview.get('average_retention_rate', 0)".1%"}")
            lines.append("")

        if 'recommendations' in report:
            lines.append("## Recommendations")
            lines.append("")
            for rec in report['recommendations']:
                lines.append(f"- {rec}")
            lines.append("")

        return "\n".join(lines)

    def cleanup_old_reports(self) -> int:
        """Clean up old reports based on retention policy."""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.config['report_retention_days'])

            original_count = len(self.report_history)
            self.report_history = [
                report for report in self.report_history
                if datetime.fromisoformat(report['generated_at']) >= cutoff_date
            ]

            cleaned_count = original_count - len(self.report_history)

            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} old reports")

            return cleaned_count

        except Exception as e:
            logger.error(f"Error during report cleanup: {e}")
            return 0

    def get_report_history(self, limit: int = 10) -> List[dict]:
        """Get recent reports from history."""
        return self.report_history[-limit:] if self.report_history else []

    def cleanup(self) -> None:
        """Clean up resources."""
        self.cleanup_old_reports()
        logger.info("RetentionReportGenerator cleanup completed")
class SessionTransitionMonitor:
    """Main integration class for session transition logging and monitoring system."""

    def __init__(self, project_path: Path, config: Optional[dict] = None):
        self.project_path = Path(project_path)
        self.config = self._get_default_config()
        if config:
            self.config.update(config)

        # Initialize all components
        self.logger = SessionTransitionLogger(project_path, self.config.get('logger_config'))
        self.validator = ContextRetentionValidator(
            target_retention_rate=self.config['target_retention_rate'],
            config=self.config.get('validator_config')
        )
        self.metrics_collector = TransitionMetricsCollector(self.config.get('metrics_config'))
        self.report_generator = RetentionReportGenerator(
            self.logger, self.validator, self.metrics_collector,
            self.config.get('report_config')
        )

        # Monitoring state
        self.active_sessions: Dict[str, dict] = {}
        self.monitoring_enabled = False
        self.background_thread = None
        self.maintenance_thread = None

        # Integration with existing context system
        self.context_engine = None

        logger.info(f"SessionTransitionMonitor initialized for project: {self.project_path}")

    def _get_default_config(self) -> dict:
        """Get default configuration for the monitor."""
        return {
            'target_retention_rate': 0.95,
            'enable_auto_monitoring': True,
            'monitoring_interval_seconds': 30,
            'maintenance_interval_hours': 6,
            'enable_alerts': True,
            'alert_webhook_url': None,
            'logger_config': {},
            'validator_config': {},
            'metrics_config': {},
            'report_config': {}
        }

    def start_monitoring(self) -> bool:
        """Start the session transition monitoring system."""
        try:
            if self.monitoring_enabled:
                logger.warning("Monitoring is already enabled")
                return True

            # Start all components
            self.logger.start_background_flush()
            self.metrics_collector.start_session_collection("system_monitor")

            # Start background monitoring
            self.monitoring_enabled = True
            self.background_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.background_thread.start()

            # Start maintenance thread
            self.maintenance_thread = threading.Thread(target=self._maintenance_loop, daemon=True)
            self.maintenance_thread.start()

            logger.info("Session transition monitoring started")
            return True

        except Exception as e:
            logger.error(f"Error starting monitoring: {e}")
            return False

    def stop_monitoring(self) -> bool:
        """Stop the session transition monitoring system."""
        try:
            if not self.monitoring_enabled:
                logger.warning("Monitoring is not enabled")
                return True

            # Stop monitoring
            self.monitoring_enabled = False

            # Stop background threads
            if self.background_thread and self.background_thread.is_alive():
                self.background_thread.join(timeout=5)

            if self.maintenance_thread and self.maintenance_thread.is_alive():
                self.maintenance_thread.join(timeout=5)

            # Stop all components
            self.logger.stop_background_flush()
            self.metrics_collector.cleanup()
            self.report_generator.cleanup()

            logger.info("Session transition monitoring stopped")
            return True

        except Exception as e:
            logger.error(f"Error stopping monitoring: {e}")
            return False

    def register_session_start(self, session_id: str, user_id: str,
                             initial_context_count: int = 0) -> bool:
        """Register the start of a new session."""
        try:
            # Log session start
            start_transition = self.logger.log_session_start(
                session_id, user_id, str(self.project_path), initial_context_count
            )

            # Start validation tracking
            self.validator.start_session_validation(session_id, initial_context_count)

            # Start metrics collection
            self.metrics_collector.start_session_collection(session_id)

            # Track active session
            self.active_sessions[session_id] = {
                'user_id': user_id,
                'start_time': datetime.now(),
                'start_transition': start_transition,
                'context_snapshots': [],
                'last_activity': datetime.now()
            }

            logger.info(f"Registered session start: {session_id}")
            return True

        except Exception as e:
            logger.error(f"Error registering session start: {e}")
            return False

    def register_session_end(self, session_id: str, final_context_count: int = 0) -> bool:
        """Register the end of a session."""
        try:
            if session_id not in self.active_sessions:
                logger.warning(f"No active session found: {session_id}")
                return False

            # Calculate retention rate
            session_data = self.active_sessions[session_id]
            initial_count = session_data.get('initial_context_count', 0)

            if initial_count > 0:
                retention_rate = final_context_count / initial_count
            else:
                retention_rate = 1.0

            # Log session end
            end_transition = self.logger.log_session_end(
                session_id, final_context_count, retention_rate
            )

            # Validate session retention
            validation_result = self.validator.validate_session_retention(session_id)

            # Record final metrics
            self.metrics_collector.record_transition_event(session_id, end_transition)

            # Clean up active session
            del self.active_sessions[session_id]

            logger.info(f"Registered session end: {session_id} (retention: {retention_rate".1%"})")
            return True

        except Exception as e:
            logger.error(f"Error registering session end: {e}")
            return False

    def record_context_operation(self, session_id: str, operation: TransitionType,
                               context_count: int, success: bool = True,
                               notes: str = "") -> bool:
        """Record a context-related operation."""
        try:
            # Log the operation
            transition = self.logger.log_context_operation(
                session_id, operation, context_count, success, notes
            )

            # Record metrics
            self.metrics_collector.record_transition_event(session_id, transition)

            # Update validation
            self.validator.record_transition_measurement(session_id, transition)

            # Update session activity
            if session_id in self.active_sessions:
                self.active_sessions[session_id]['last_activity'] = datetime.now()

            return True

        except Exception as e:
            logger.error(f"Error recording context operation: {e}")
            return False

    def record_context_snapshot(self, session_id: str, context_count: int,
                              context_types: Optional[Dict[str, int]] = None) -> None:
        """Record a snapshot of current context state."""
        try:
            # Update validator
            self.validator.record_context_snapshot(session_id, context_count, context_types)

            # Update metrics collector
            self.metrics_collector.record_context_metrics(
                session_id, context_count, context_types
            )

            # Update session data
            if session_id in self.active_sessions:
                self.active_sessions[session_id]['context_snapshots'].append({
                    'timestamp': datetime.now(),
                    'context_count': context_count,
                    'context_types': context_types or {}
                })

        except Exception as e:
            logger.error(f"Error recording context snapshot: {e}")

    def get_session_status(self, session_id: str) -> dict:
        """Get current status of a session."""
        try:
            if session_id not in self.active_sessions:
                return {'error': f'Session {session_id} not found or not active'}

            session_data = self.active_sessions[session_id]

            # Get recent transitions
            recent_transitions = self.logger.get_session_transitions(session_id)[-5:]  # Last 5

            # Get metrics summary
            metrics_summary = self.metrics_collector.get_session_metrics_summary(session_id)

            # Calculate session duration
            duration = datetime.now() - session_data['start_time']

            return {
                'session_id': session_id,
                'user_id': session_data['user_id'],
                'status': 'active',
                'duration_seconds': duration.total_seconds(),
                'start_time': session_data['start_time'].isoformat(),
                'last_activity': session_data['last_activity'].isoformat(),
                'recent_transitions': [
                    {
                        'type': t.transition_type.value,
                        'status': t.status.value,
                        'retention_rate': t.context_retention_rate,
                        'timestamp': t.timestamp.isoformat()
                    }
                    for t in recent_transitions
                ],
                'metrics_summary': metrics_summary if 'error' not in metrics_summary else {},
                'context_snapshots_count': len(session_data['context_snapshots'])
            }

        except Exception as e:
            logger.error(f"Error getting session status: {e}")
            return {'error': str(e)}

    def get_system_status(self) -> dict:
        """Get overall system status."""
        try:
            return {
                'monitoring_enabled': self.monitoring_enabled,
                'active_sessions_count': len(self.active_sessions),
                'active_sessions': list(self.active_sessions.keys()),
                'components_status': {
                    'logger': 'active' if self.logger else 'inactive',
                    'validator': 'active' if self.validator else 'inactive',
                    'metrics_collector': 'active' if self.metrics_collector else 'inactive',
                    'report_generator': 'active' if self.report_generator else 'inactive'
                },
                'statistics': self.logger.get_statistics(),
                'target_retention_rate': self.config['target_retention_rate'],
                'last_maintenance': getattr(self, '_last_maintenance', None)
            }

        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {'error': str(e)}

    def generate_comprehensive_report(self, report_type: str = 'daily_summary',
                                   **kwargs) -> dict:
        """Generate a comprehensive report."""
        try:
            if report_type == 'daily_summary':
                return self.report_generator.generate_daily_summary_report(**kwargs)
            elif report_type == 'session_report':
                return self.report_generator.generate_session_report(**kwargs)
            elif report_type == 'weekly_analysis':
                return self.report_generator.generate_weekly_analysis_report(**kwargs)
            else:
                return {'error': f'Unknown report type: {report_type}'}

        except Exception as e:
            logger.error(f"Error generating comprehensive report: {e}")
            return {'error': str(e)}

    def export_all_data(self, format: str = 'json') -> str:
        """Export all monitoring data."""
        try:
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'system_status': self.get_system_status(),
                'logger_statistics': self.logger.get_statistics(),
                'validator_summary': self.validator.get_retention_summary(),
                'metrics_summary': self.metrics_collector.get_aggregated_metrics(),
                'recent_reports': self.report_generator.get_report_history(5)
            }

            if format.lower() == 'json':
                return json.dumps(export_data, indent=2, ensure_ascii=False, default=str)
            else:
                # Simple text format
                lines = ["Session Transition Monitor - Full Export", "=" * 50, ""]
                lines.append(f"Export Time: {export_data['export_timestamp']}")
                lines.append(f"Active Sessions: {export_data['system_status'].get('active_sessions_count', 0)}")
                lines.append(f"Total Transitions: {export_data['logger_statistics'].get('total_transitions', 0)}")
                lines.append(f"Average Retention: {export_data['logger_statistics'].get('average_retention_rate', 0)".1%"}")
                lines.append("")
                return "\n".join(lines)

        except Exception as e:
            logger.error(f"Error exporting all data: {e}")
            return f"Error: {str(e)}"

    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring_enabled:
            try:
                # Check for inactive sessions
                self._check_inactive_sessions()

                # Update system metrics
                self._update_system_metrics()

                # Sleep for monitoring interval
                threading.Event().wait(self.config['monitoring_interval_seconds'])

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                threading.Event().wait(60)  # Wait 1 minute on error

    def _maintenance_loop(self) -> None:
        """Maintenance loop for cleanup and optimization."""
        while self.monitoring_enabled:
            try:
                # Perform maintenance tasks
                self._perform_maintenance()

                # Sleep for maintenance interval
                interval_seconds = self.config['maintenance_interval_hours'] * 3600
                threading.Event().wait(interval_seconds)

            except Exception as e:
                logger.error(f"Error in maintenance loop: {e}")
                threading.Event().wait(3600)  # Wait 1 hour on error

    def _check_inactive_sessions(self) -> None:
        """Check for inactive sessions and clean them up."""
        try:
            current_time = datetime.now()
            inactive_threshold = timedelta(minutes=30)  # Configurable

            inactive_sessions = []
            for session_id, session_data in self.active_sessions.items():
                if current_time - session_data['last_activity'] > inactive_threshold:
                    inactive_sessions.append(session_id)

            # End inactive sessions
            for session_id in inactive_sessions:
                logger.info(f"Ending inactive session: {session_id}")
                self.register_session_end(session_id, 0)  # Unknown final count

        except Exception as e:
            logger.error(f"Error checking inactive sessions: {e}")

    def _update_system_metrics(self) -> None:
        """Update system-wide metrics."""
        try:
            # Update baselines in metrics collector
            self.metrics_collector.update_baselines()

            # Record system health metrics
            system_session_id = "system_monitor"
            if system_session_id in self.active_sessions:
                self.metrics_collector.record_system_metrics(system_session_id)

        except Exception as e:
            logger.error(f"Error updating system metrics: {e}")

    def _perform_maintenance(self) -> None:
        """Perform maintenance tasks."""
        try:
            # Clean up old data
            self.logger.cleanup_old_logs()
            self.metrics_collector.cleanup_old_metrics()
            self.report_generator.cleanup_old_reports()

            # Update baselines
            self.metrics_collector.update_baselines()

            # Log maintenance completion
            self._last_maintenance = datetime.now()
            logger.debug("Maintenance tasks completed")

        except Exception as e:
            logger.error(f"Error during maintenance: {e}")

    def integrate_with_context_engine(self, context_engine) -> bool:
        """Integrate with the existing context retention engine."""
        try:
            self.context_engine = context_engine

            # Set up hooks for context operations
            original_store = context_engine.store_context
            original_retrieve = context_engine.retrieve_context
            original_update = context_engine.update_context
            original_delete = context_engine.delete_context

            def monitored_store(context_obj):
                result = original_store(context_obj)
                if result and context_obj.metadata.session_id:
                    self.record_context_operation(
                        context_obj.metadata.session_id,
                        TransitionType.CONTEXT_SAVE,
                        1,
                        result,
                        f"Stored context {context_obj.metadata.context_id}"
                    )
                return result

            def monitored_retrieve(context_id):
                result = original_retrieve(context_id)
                if result and result.metadata.session_id:
                    self.record_context_operation(
                        result.metadata.session_id,
                        TransitionType.CONTEXT_LOAD,
                        1,
                        result is not None,
                        f"Retrieved context {context_id}"
                    )
                return result

            def monitored_update(context_obj):
                result = original_update(context_obj)
                if result and context_obj.metadata.session_id:
                    self.record_context_operation(
                        context_obj.metadata.session_id,
                        TransitionType.CONTEXT_SAVE,
                        1,
                        result,
                        f"Updated context {context_obj.metadata.context_id}"
                    )
                return result

            def monitored_delete(context_id):
                # Find the context object first
                context_obj = context_engine.retrieve_context(context_id)
                result = original_delete(context_id)

                if result and context_obj and context_obj.metadata.session_id:
                    self.record_context_operation(
                        context_obj.metadata.session_id,
                        TransitionType.CONTEXT_EVICTION,
                        1,
                        result,
                        f"Deleted context {context_id}"
                    )
                return result

            # Replace methods with monitored versions
            context_engine.store_context = monitored_store
            context_engine.retrieve_context = monitored_retrieve
            context_engine.update_context = monitored_update
            context_engine.delete_context = monitored_delete

            logger.info("Successfully integrated with context engine")
            return True

        except Exception as e:
            logger.error(f"Error integrating with context engine: {e}")
            return False

    def get_monitoring_summary(self) -> dict:
        """Get a comprehensive summary of the monitoring system."""
        try:
            return {
                'system_overview': {
                    'monitoring_enabled': self.monitoring_enabled,
                    'active_sessions': len(self.active_sessions),
                    'target_retention_rate': self.config['target_retention_rate'],
                    'uptime_seconds': (datetime.now() - getattr(self, '_start_time', datetime.now())).total_seconds()
                },
                'component_health': {
                    'logger': self._check_component_health(self.logger),
                    'validator': self._check_component_health(self.validator),
                    'metrics_collector': self._check_component_health(self.metrics_collector),
                    'report_generator': self._check_component_health(self.report_generator)
                },
                'recent_activity': {
                    'transitions_last_hour': len(self.logger.get_transitions_in_range(
                        datetime.now() - timedelta(hours=1), datetime.now()
                    )),
                    'active_sessions_list': list(self.active_sessions.keys()),
                    'validation_results': self.validator.get_retention_summary(days=1)
                },
                'performance_indicators': {
                    'average_retention_rate': self.logger.get_statistics().get('average_retention_rate', 0),
                    'average_transition_time': self.logger.get_statistics().get('average_transition_time', 0),
                    'success_rate': self.logger.get_statistics().get('success_rate', 0)
                }
            }

        except Exception as e:
            logger.error(f"Error getting monitoring summary: {e}")
            return {'error': str(e)}

    def _check_component_health(self, component) -> str:
        """Check the health status of a component."""
        try:
            if component is None:
                return 'not_initialized'

            # Check if component has basic methods
            if hasattr(component, 'get_statistics'):
                stats = component.get_statistics()
                if isinstance(stats, dict) and len(stats) > 0:
                    return 'healthy'

            if hasattr(component, 'get_retention_summary'):
                summary = component.get_retention_summary()
                if isinstance(summary, dict):
                    return 'healthy'

            return 'unknown'

        except Exception:
            return 'error'

    def cleanup(self) -> None:
        """Clean up all resources."""
        try:
            # End all active sessions
            for session_id in list(self.active_sessions.keys()):
                self.register_session_end(session_id, 0)

            # Stop monitoring
            self.stop_monitoring()

            logger.info("SessionTransitionMonitor cleanup completed")

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


# Convenience function for easy setup
def create_session_monitor(project_path: Union[str, Path],
                         target_retention_rate: float = 0.95,
                         config: Optional[dict] = None) -> SessionTransitionMonitor:
    """Create and initialize a session transition monitor."""
    project_path = Path(project_path)

    if config is None:
        config = {}

    config['target_retention_rate'] = target_retention_rate

    monitor = SessionTransitionMonitor(project_path, config)

    # Auto-start monitoring if configured
    if config.get('enable_auto_monitoring', True):
        monitor.start_monitoring()

    return monitor