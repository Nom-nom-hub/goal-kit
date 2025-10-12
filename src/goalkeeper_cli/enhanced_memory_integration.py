#!/usr/bin/env python3
"""
Integration layer for enhanced context retention system with existing AISessionMemory.

This module provides backward compatibility while enabling enhanced context retention
capabilities for the Goal Kit memory system.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from .enhanced_context import (
    ContextObject, ContextMetadata, ContextLayer, ContextPriority,
    ContextRetentionEngine, ContextPrioritizer, ContextCompressor
)
from .memory import AISessionMemory, ProjectMemory

logger = logging.getLogger(__name__)


class EnhancedAISessionMemory(AISessionMemory):
    """Enhanced AI session memory with advanced context retention."""

    def __init__(self, project_path: Path, enable_enhanced: bool = True):
        # Store the project path for later use
        self._init_project_path = project_path

        super().__init__(project_path)

        self.enable_enhanced = enable_enhanced
        self.enhanced_engine = None
        self.migration_mode = False

        if enable_enhanced:
            self._initialize_enhanced_engine()

    def _initialize_enhanced_engine(self) -> None:
        """Initialize the enhanced context retention engine."""
        try:
            # Get configuration from project or use defaults
            config = self._load_enhanced_config()

            # Use the project path - try multiple ways to get it
            project_path = None

            # Method 1: Try to get from parent class memory attribute
            if hasattr(self, 'memory') and hasattr(self.memory, 'project_path'):
                project_path = self.memory.project_path
            # Method 2: Use the stored path from constructor
            elif hasattr(self, '_init_project_path'):
                project_path = self._init_project_path
            # Method 3: Try to infer from current working directory
            else:
                project_path = Path.cwd()

            # Ensure we have a valid path
            if project_path is None:
                raise ValueError("Could not determine project path")

            self.enhanced_engine = ContextRetentionEngine(project_path, config)

            # Start background maintenance
            self.enhanced_engine.start_maintenance()

            logger.info("Enhanced context retention engine initialized")

        except Exception as e:
            logger.error(f"Failed to initialize enhanced engine: {e}")
            # Keep enable_enhanced as True - the engine failure shouldn't disable the feature
            # The system should still work in legacy mode
            self.enhanced_engine = None

    def _initialize_enhanced_engine(self) -> None:
        """Initialize the enhanced context retention engine."""
        try:
            # Get configuration from project or use defaults
            config = self._load_enhanced_config()

            self.enhanced_engine = ContextRetentionEngine(self.project_path, config)

            # Start background maintenance
            self.enhanced_engine.start_maintenance()

            logger.info("Enhanced context retention engine initialized")

        except Exception as e:
            logger.error(f"Failed to initialize enhanced engine: {e}")
            self.enable_enhanced = False

    def _load_enhanced_config(self) -> dict:
        """Load enhanced configuration from project settings."""
        config_file = self.project_path / ".goalkit" / "memory" / "enhanced_config.json"

        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load enhanced config: {e}")

        # Return default configuration
        return {
            'max_hot_storage_mb': 50,
            'max_warm_storage_mb': 200,
            'max_cold_storage_mb': 1000,
            'max_archive_storage_mb': 5000,
            'compression_threshold_kb': 25,
            'auto_maintenance_interval_hours': 12,
            'context_ttl_hours': {
                'CRITICAL': 8760 * 24,  # 1 year
                'HIGH': 720 * 24,       # 1 month
                'MEDIUM': 168 * 24,     # 1 week
                'LOW': 24 * 24,         # 1 day
                'TRIVIAL': 2 * 24       # 2 hours
            },
            'enable_auto_compression': True,
            'enable_auto_archival': True
        }

    def start_session(self, agent_name: str) -> str:
        """Start new AI session with enhanced context support."""
        session_id = super().start_session(agent_name)

        if self.enable_enhanced and self.enhanced_engine:
            # Create enhanced context for session start
            self._create_session_context(session_id, agent_name)

        return session_id

    def _create_session_context(self, session_id: str, agent_name: str) -> None:
        """Create enhanced context object for session."""
        try:
            # Create context metadata
            metadata = ContextMetadata(
                session_id=session_id,
                agent_name=agent_name,
                project_path=str(self.project_path),
                priority=ContextPriority.HIGH,
                layer=ContextLayer.HOT,
                tags=['session', 'start', agent_name],
                categories=['session_management']
            )

            # Create context object
            session_context = ContextObject(
                content={
                    'event': 'session_started',
                    'timestamp': datetime.now().isoformat(),
                    'agent_name': agent_name,
                    'project': self.project_path.name
                },
                metadata=metadata
            )

            # Store in enhanced engine
            self.enhanced_engine.store_context(session_context)

        except Exception as e:
            logger.error(f"Failed to create session context: {e}")

    def add_interaction(self, command: str, user_input: str, ai_response: str, success_score: float = None) -> None:
        """Record AI interaction with enhanced context retention."""
        # Call parent method for backward compatibility
        super().add_interaction(command, user_input, ai_response, success_score)

        if self.enable_enhanced and self.enhanced_engine:
            self._store_enhanced_interaction(command, user_input, ai_response, success_score)

    def _store_enhanced_interaction(self, command: str, user_input: str, ai_response: str, success_score: float) -> None:
        """Store interaction in enhanced context system."""
        try:
            # Determine priority based on success score and command type
            priority = self._determine_interaction_priority(command, success_score)

            # Create metadata
            metadata = ContextMetadata(
                session_id=self.current_session_id,
                agent_name="goal-kit-ai",  # Default agent name
                project_path=str(self.project_path),
                priority=priority,
                layer=ContextLayer.HOT,
                tags=self._extract_tags(command, user_input),
                categories=self._extract_categories(command),
                relevance_score=self._calculate_relevance_score(command, user_input),
                importance_score=self._calculate_importance_score(command, success_score)
            )

            # Create context content
            content = {
                'interaction_type': 'ai_conversation',
                'command': command,
                'user_input': user_input,
                'ai_response_summary': self._summarize_response_enhanced(ai_response),
                'success_score': success_score,
                'timestamp': datetime.now().isoformat()
            }

            # Create context object
            context_obj = ContextObject(
                content=content,
                metadata=metadata
            )

            # Store in enhanced engine
            self.enhanced_engine.store_context(context_obj)

        except Exception as e:
            logger.error(f"Failed to store enhanced interaction: {e}")

    def _determine_interaction_priority(self, command: str, success_score: float) -> ContextPriority:
        """Determine priority level for interaction."""
        # High priority commands
        high_priority_commands = ['goal', 'vision', 'plan', 'analyze', 'validate']

        if any(cmd in command.lower() for cmd in high_priority_commands):
            return ContextPriority.HIGH

        # Consider success score
        if success_score is not None:
            if success_score > 8:
                return ContextPriority.HIGH
            elif success_score > 6:
                return ContextPriority.MEDIUM
            elif success_score > 4:
                return ContextPriority.LOW
            else:
                return ContextPriority.TRIVIAL

        return ContextPriority.MEDIUM

    def _extract_tags(self, command: str, user_input: str) -> List[str]:
        """Extract relevant tags from interaction."""
        tags = []

        # Command-based tags
        command_lower = command.lower()
        if 'goal' in command_lower:
            tags.append('goal_management')
        if 'vision' in command_lower:
            tags.append('vision_planning')
        if 'plan' in command_lower:
            tags.append('planning')
        if 'analyze' in command_lower:
            tags.append('analysis')
        if 'validate' in command_lower:
            tags.append('validation')

        # Content-based tags
        content_lower = user_input.lower()
        if 'urgent' in content_lower or 'important' in content_lower:
            tags.append('urgent')
        if 'bug' in content_lower or 'error' in content_lower:
            tags.append('issue')
        if 'feature' in content_lower or 'enhancement' in content_lower:
            tags.append('feature_request')

        return tags

    def _extract_categories(self, command: str) -> List[str]:
        """Extract categories from command."""
        categories = []

        command_lower = command.lower()
        if command_lower in ['goal', 'vision', 'plan', 'analyze', 'validate']:
            categories.append('core_commands')
        elif command_lower.startswith('template'):
            categories.append('template_management')
        elif command_lower.startswith('memory'):
            categories.append('memory_operations')
        else:
            categories.append('general_commands')

        return categories

    def _calculate_relevance_score(self, command: str, user_input: str) -> float:
        """Calculate relevance score for interaction."""
        # Base score
        relevance = 0.5

        # Boost for project-related content
        project_keywords = ['goal', 'project', 'milestone', 'strategy', 'plan']
        content_text = f"{command} {user_input}".lower()

        matching_keywords = sum(1 for keyword in project_keywords if keyword in content_text)
        relevance += min(matching_keywords * 0.1, 0.3)

        return min(relevance, 1.0)

    def _calculate_importance_score(self, command: str, success_score: float) -> float:
        """Calculate importance score for interaction."""
        importance = 0.5

        # Command importance
        important_commands = ['goal', 'vision', 'plan']
        if any(cmd in command.lower() for cmd in important_commands):
            importance += 0.2

        # Success score influence
        if success_score is not None:
            importance += (success_score - 5) * 0.1

        return min(importance, 1.0)

    def _summarize_response_enhanced(self, response: str, max_length: int = 200) -> str:
        """Create enhanced summary of AI response."""
        # Use the existing summarization method
        summary = self._summarize_response(response, max_length)

        # Add enhanced analysis if response is long enough
        if len(response) > 500:
            # Extract key insights or decisions
            insights = self._extract_key_insights(response)
            if insights:
                summary += f" [Key insights: {', '.join(insights[:2])}]"

        return summary

    def _extract_key_insights(self, response: str) -> List[str]:
        """Extract key insights from AI response."""
        insights = []

        # Look for decision indicators
        if any(word in response.lower() for word in ['recommend', 'suggest', 'decide', 'conclude']):
            insights.append('decision_made')

        # Look for learning indicators
        if any(word in response.lower() for word in ['learn', 'discover', 'realize', 'understand']):
            insights.append('learning')

        # Look for action indicators
        if any(word in response.lower() for word in ['create', 'implement', 'execute', 'build']):
            insights.append('action_planned')

        return insights

    def get_relevant_context(self, current_command: str) -> dict:
        """Get enhanced relevant context from both systems."""
        # Get context from parent class (backward compatibility)
        base_context = super().get_relevant_context(current_command)

        if not self.enable_enhanced or not self.enhanced_engine:
            return base_context

        try:
            # Create query context for enhanced search
            query_context = ContextObject(
                content={'command': current_command, 'query_type': 'context_search'},
                metadata=ContextMetadata(
                    tags=self._extract_tags(current_command, ''),
                    categories=self._extract_categories(current_command)
                )
            )

            # Find similar contexts in enhanced system
            similar_contexts = self.enhanced_engine.find_similar_contexts(query_context, limit=5)

            # Convert to enhanced context format
            enhanced_contexts = []
            for context in similar_contexts:
                enhanced_contexts.append({
                    'content': context.content,
                    'priority': context.metadata.priority.name,
                    'layer': context.metadata.layer.value,
                    'relevance_score': context.metadata.relevance_score,
                    'created_at': context.metadata.created_at.isoformat()
                })

            # Merge contexts
            merged_context = base_context.copy()
            merged_context['enhanced_contexts'] = enhanced_contexts
            merged_context['enhanced_available'] = True

            return merged_context

        except Exception as e:
            logger.error(f"Error getting enhanced context: {e}")
            return base_context

    def migrate_from_legacy(self) -> bool:
        """Migrate existing session data to enhanced system."""
        if not self.enable_enhanced or not self.enhanced_engine:
            return False

        try:
            self.migration_mode = True

            # Get existing sessions
            sessions_path = self.memory.sessions_path

            if not sessions_path.exists():
                return True

            # Migrate each session
            for session_dir in sessions_path.iterdir():
                if session_dir.is_dir():
                    self._migrate_session(session_dir)

            logger.info("Legacy migration completed")
            return True

        except Exception as e:
            logger.error(f"Migration failed: {e}")
            return False
        finally:
            self.migration_mode = False

    def _migrate_session(self, session_dir: Path) -> None:
        """Migrate a single session to enhanced system."""
        try:
            session_file = session_dir / "session.json"
            interactions_file = session_dir / "interactions.jsonl"

            if not session_file.exists():
                return

            # Load session data
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)

            # Create enhanced context for session
            metadata = ContextMetadata(
                session_id=session_data.get('session_id', ''),
                agent_name=session_data.get('agent_name', ''),
                project_path=str(self.project_path),
                priority=ContextPriority.HIGH,
                layer=ContextLayer.WARM,  # Legacy sessions go to warm storage
                tags=['legacy_session', 'migration'],
                categories=['session_management']
            )

            context_obj = ContextObject(
                content=session_data,
                metadata=metadata
            )

            self.enhanced_engine.store_context(context_obj)

            # Migrate interactions if they exist
            if interactions_file.exists():
                self._migrate_interactions(interactions_file, session_data.get('session_id', ''))

        except Exception as e:
            logger.error(f"Failed to migrate session {session_dir.name}: {e}")

    def _migrate_interactions(self, interactions_file: Path, session_id: str) -> None:
        """Migrate interaction data to enhanced system."""
        try:
            with open(interactions_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        interaction = json.loads(line.strip())

                        # Create context for interaction
                        metadata = ContextMetadata(
                            session_id=session_id,
                            project_path=str(self.project_path),
                            priority=ContextPriority.MEDIUM,
                            layer=ContextLayer.WARM,
                            tags=['legacy_interaction', 'migration'],
                            categories=['conversation_history']
                        )

                        context_obj = ContextObject(
                            content=interaction,
                            metadata=metadata
                        )

                        self.enhanced_engine.store_context(context_obj)

                    except json.JSONDecodeError as e:
                        logger.warning(f"Skipping invalid interaction at line {line_num}: {e}")
                    except Exception as e:
                        logger.error(f"Error migrating interaction at line {line_num}: {e}")

        except Exception as e:
            logger.error(f"Failed to migrate interactions from {interactions_file}: {e}")

    def get_enhanced_stats(self) -> dict:
        """Get statistics from enhanced system."""
        if not self.enable_enhanced or not self.enhanced_engine:
            return {'enhanced_enabled': False}

        stats = self.enhanced_engine.get_stats()

        # Add compression stats if available
        if hasattr(self.enhanced_engine, 'compressor'):
            stats['compression'] = self.enhanced_engine.compressor.get_compression_stats()

        return {
            'enhanced_enabled': True,
            'engine_stats': stats,
            'migration_mode': self.migration_mode
        }

    def cleanup(self) -> None:
        """Clean up resources including enhanced engine."""
        if self.enhanced_engine:
            self.enhanced_engine.cleanup()

        logger.info("Enhanced AI session memory cleanup completed")


class EnhancedProjectMemory(ProjectMemory):
    """Enhanced project memory with advanced context retention."""

    def __init__(self, project_path: Path, enable_enhanced: bool = True):
        super().__init__(project_path)

        self.enable_enhanced = enable_enhanced
        self.enhanced_engine = None

        if enable_enhanced:
            self._initialize_enhanced_engine()

    def _initialize_enhanced_engine(self) -> None:
        """Initialize enhanced engine for project memory."""
        try:
            config = self._load_enhanced_config()
            self.enhanced_engine = ContextRetentionEngine(self.project_path, config)

            logger.info("Enhanced project memory engine initialized")

        except Exception as e:
            logger.error(f"Failed to initialize enhanced project engine: {e}")
            self.enable_enhanced = False

    def _load_enhanced_config(self) -> dict:
        """Load enhanced configuration."""
        config_file = self.project_path / ".goalkit" / "memory" / "enhanced_config.json"

        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass

        return {
            'max_hot_storage_mb': 100,
            'max_warm_storage_mb': 500,
            'max_cold_storage_mb': 2000,
            'max_archive_storage_mb': 10000,
            'compression_threshold_kb': 50,
            'auto_maintenance_interval_hours': 24,
            'context_ttl_hours': {
                'CRITICAL': 8760 * 24,
                'HIGH': 720 * 24,
                'MEDIUM': 168 * 24,
                'LOW': 24 * 24,
                'TRIVIAL': 2 * 24
            },
            'enable_auto_compression': True,
            'enable_auto_archival': True
        }

    def record_goal_completion(self, goal_name: str, goal_data: dict) -> None:
        """Record goal completion with enhanced context."""
        # Call parent method for backward compatibility
        super().record_goal_completion(goal_name, goal_data)

        if self.enable_enhanced and self.enhanced_engine:
            self._store_enhanced_goal_completion(goal_name, goal_data)

    def _store_enhanced_goal_completion(self, goal_name: str, goal_data: dict) -> None:
        """Store goal completion in enhanced system."""
        try:
            # Determine priority based on success
            success_score = goal_data.get('success_score', 5)
            if success_score > 8:
                priority = ContextPriority.HIGH
            elif success_score > 6:
                priority = ContextPriority.MEDIUM
            else:
                priority = ContextPriority.LOW

            # Create metadata
            metadata = ContextMetadata(
                project_path=str(self.project_path),
                priority=priority,
                layer=ContextLayer.WARM,
                tags=['goal_completion', goal_name.lower()],
                categories=['project_learning', 'goal_management'],
                relevance_score=min(success_score / 10.0, 1.0),
                importance_score=min(success_score / 10.0, 1.0)
            )

            # Create context content
            content = {
                'event_type': 'goal_completion',
                'goal_name': goal_name,
                'completion_data': goal_data,
                'timestamp': datetime.now().isoformat()
            }

            # Create context object
            context_obj = ContextObject(
                content=content,
                metadata=metadata
            )

            # Store in enhanced engine
            self.enhanced_engine.store_context(context_obj)

        except Exception as e:
            logger.error(f"Failed to store enhanced goal completion: {e}")

    def get_project_patterns(self, project_id: str = None) -> dict:
        """Get enhanced project patterns."""
        # Get base patterns
        patterns = super().get_project_patterns(project_id)

        if self.enable_enhanced and self.enhanced_engine:
            # Enhance with similar contexts from enhanced system
            try:
                query_context = ContextObject(
                    content={'query_type': 'project_patterns', 'project_id': project_id},
                    metadata=ContextMetadata(
                        tags=['project_analysis'],
                        categories=['pattern_analysis']
                    )
                )

                similar_contexts = self.enhanced_engine.find_similar_contexts(query_context, limit=10)

                # Extract additional insights
                enhanced_insights = []
                for context in similar_contexts:
                    if context.content and isinstance(context.content, dict):
                        if context.content.get('event_type') == 'goal_completion':
                            completion_data = context.content.get('completion_data', {})
                            if completion_data.get('success_score', 0) > 7:
                                enhanced_insights.append({
                                    'type': 'success_pattern',
                                    'goal': context.content.get('goal_name'),
                                    'success_factors': completion_data.get('success_factors', [])
                                })

                patterns['enhanced_insights'] = enhanced_insights

            except Exception as e:
                logger.error(f"Error getting enhanced patterns: {e}")

        return patterns


# Convenience functions for easy integration
def get_enhanced_ai_session_memory(project_path: Path, enable_enhanced: bool = True) -> EnhancedAISessionMemory:
    """Get enhanced AI session memory with backward compatibility."""
    return EnhancedAISessionMemory(project_path, enable_enhanced)

def get_enhanced_project_memory(project_path: Path, enable_enhanced: bool = True) -> EnhancedProjectMemory:
    """Get enhanced project memory with backward compatibility."""
    return EnhancedProjectMemory(project_path, enable_enhanced)

def migrate_to_enhanced_system(project_path: Path) -> bool:
    """Migrate existing memory system to enhanced version."""
    try:
        # Create enhanced session memory to trigger migration
        enhanced_memory = EnhancedAISessionMemory(project_path, enable_enhanced=True)

        # Perform migration
        success = enhanced_memory.migrate_from_legacy()

        # Cleanup
        enhanced_memory.cleanup()

        return success

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return False