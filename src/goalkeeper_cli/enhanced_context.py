#!/usr/bin/env python3
"""
Enhanced Context Retention Engine for AISessionMemory system

This module implements an advanced context retention system with multi-layer storage,
intelligent prioritization, and compression for efficient memory management.
"""

import json
import uuid
import zlib
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
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


class ContextLayer(Enum):
    """Storage layers for context data."""
    HOT = "hot"        # Active, frequently accessed context
    WARM = "warm"      # Recently accessed but not active
    COLD = "cold"      # Older context, accessed occasionally
    ARCHIVE = "archive" # Historical context, rarely accessed


class ContextPriority(Enum):
    """Priority levels for context objects."""
    CRITICAL = 5      # Must-keep context (user preferences, key decisions)
    HIGH = 4          # Important context (recent interactions, active goals)
    MEDIUM = 3        # Useful context (project patterns, insights)
    LOW = 2           # Nice-to-have context (historical data)
    TRIVIAL = 1       # Disposable context (temporary information)


@dataclass
class ContextMetadata:
    """Enhanced metadata for context objects."""

    # Core identification
    context_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ""
    agent_name: str = ""
    project_path: str = ""

    # Temporal information
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    accessed_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None

    # Content characteristics
    content_type: str = "text"  # text, code, structured, binary
    content_size: int = 0  # Size in bytes
    compressed_size: int = 0  # Compressed size in bytes

    # Context relationships
    parent_context_id: Optional[str] = None
    child_context_ids: List[str] = field(default_factory=list)
    related_context_ids: List[str] = field(default_factory=list)

    # Priority and retention
    priority: ContextPriority = ContextPriority.MEDIUM
    layer: ContextLayer = ContextLayer.HOT
    access_count: int = 0
    importance_score: float = 0.5  # 0.0 to 1.0

    # Content classification
    tags: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    entities: List[str] = field(default_factory=list)  # Named entities

    # Processing flags
    is_compressed: bool = False
    is_processed: bool = False
    is_indexed: bool = False

    # Quality metrics
    relevance_score: float = 0.5  # 0.0 to 1.0
    completeness_score: float = 0.5  # 0.0 to 1.0
    accuracy_score: float = 0.5  # 0.0 to 1.0

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        # Convert datetime objects to ISO strings
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        # Convert enums to strings
        data['priority'] = self.priority.name
        data['layer'] = self.layer.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'ContextMetadata':
        """Create from dictionary."""
        # Convert ISO strings back to datetime objects
        for key in ['created_at', 'updated_at', 'accessed_at', 'expires_at']:
            if key in data and data[key]:
                try:
                    data[key] = datetime.fromisoformat(data[key])
                except (ValueError, TypeError):
                    pass  # Keep original value if conversion fails

        # Convert string enums back to enum objects
        if 'priority' in data and isinstance(data['priority'], str):
            try:
                data['priority'] = ContextPriority[data['priority']]
            except KeyError:
                data['priority'] = ContextPriority.MEDIUM

        if 'layer' in data and isinstance(data['layer'], str):
            try:
                data['layer'] = ContextLayer(data['layer'])
            except ValueError:
                data['layer'] = ContextLayer.HOT

        return cls(**data)

    def update_access_time(self) -> None:
        """Update the last accessed time."""
        self.accessed_at = datetime.now()
        self.access_count += 1

    def calculate_importance_score(self) -> float:
        """Calculate overall importance score based on various factors."""
        # Base score from priority
        priority_score = self.priority.value / 5.0

        # Access frequency factor (logarithmic scaling)
        access_factor = min(self.access_count / 10.0, 1.0)

        # Recency factor (newer content is more important)
        hours_old = (datetime.now() - self.created_at).total_seconds() / 3600
        recency_factor = max(0, 1.0 - (hours_old / 168))  # Decay over a week

        # Relevance and completeness factors
        quality_factor = (self.relevance_score + self.completeness_score) / 2.0

        # Combine factors with weights
        importance = (
            priority_score * 0.3 +
            access_factor * 0.2 +
            recency_factor * 0.2 +
            quality_factor * 0.3
        )

        self.importance_score = max(0.0, min(1.0, importance))
        return self.importance_score


@dataclass
class ContextObject:
    """Enhanced context object with rich metadata and content."""

    # Core content
    content: Any = None  # The actual context data
    content_hash: str = ""

    # Metadata
    metadata: ContextMetadata = field(default_factory=ContextMetadata)

    # Additional context data
    raw_content: Optional[Any] = None  # Original content before processing
    processed_content: Optional[Any] = None  # Processed/enhanced content
    embeddings: Optional[List[float]] = None  # Vector embeddings for similarity

    # Compression data
    compressed_content: Optional[bytes] = None
    compression_algorithm: str = "none"

    # Storage information
    storage_path: Optional[Path] = None
    is_loaded: bool = True  # Whether content is loaded in memory

    def __post_init__(self):
        """Post-initialization processing."""
        if self.content is not None and not self.content_hash:
            self.content_hash = self._calculate_content_hash()

        if self.metadata.context_id:
            self.metadata.context_id = self.metadata.context_id
        else:
            self.metadata.context_id = str(uuid.uuid4())

    def _calculate_content_hash(self) -> str:
        """Calculate hash of the content for deduplication."""
        try:
            if isinstance(self.content, str):
                content_bytes = self.content.encode('utf-8')
            else:
                content_bytes = pickle.dumps(self.content, protocol=pickle.HIGHEST_PROTOCOL)

            return hashlib.sha256(content_bytes).hexdigest()
        except Exception as e:
            logger.warning(f"Failed to calculate content hash: {e}")
            return str(uuid.uuid4())

    def compress(self, algorithm: str = "zlib") -> bool:
        """Compress the content using specified algorithm."""
        try:
            if algorithm == "zlib":
                if isinstance(self.content, str):
                    content_bytes = self.content.encode('utf-8')
                else:
                    content_bytes = pickle.dumps(self.content, protocol=pickle.HIGHEST_PROTOCOL)

                self.compressed_content = zlib.compress(content_bytes)
                self.compression_algorithm = algorithm
                self.metadata.is_compressed = True
                self.metadata.compressed_size = len(self.compressed_content)
                self.metadata.content_size = len(content_bytes)

                return True
            else:
                logger.warning(f"Unsupported compression algorithm: {algorithm}")
                return False

        except Exception as e:
            logger.error(f"Compression failed: {e}")
            return False

    def decompress(self) -> bool:
        """Decompress the content."""
        try:
            if not self.metadata.is_compressed or not self.compressed_content:
                return False

            if self.compression_algorithm == "zlib":
                decompressed_data = zlib.decompress(self.compressed_content)

                # Try to decode as string first, then as pickle
                try:
                    self.content = decompressed_data.decode('utf-8')
                except UnicodeDecodeError:
                    self.content = pickle.loads(decompressed_data)

                self.metadata.is_compressed = False
                return True
            else:
                logger.warning(f"Unsupported compression algorithm: {self.compression_algorithm}")
                return False

        except Exception as e:
            logger.error(f"Decompression failed: {e}")
            return False

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        data = {
            'content_hash': self.content_hash,
            'metadata': self.metadata.to_dict(),
            'raw_content': self._serialize_content(self.raw_content),
            'processed_content': self._serialize_content(self.processed_content),
            'embeddings': self.embeddings,
            'compressed_content': self.compressed_content.hex() if self.compressed_content else None,
            'compression_algorithm': self.compression_algorithm,
            'is_loaded': self.is_loaded
        }

        # Only include content if it's loaded and not compressed
        if self.is_loaded and not self.metadata.is_compressed:
            data['content'] = self._serialize_content(self.content)

        return data

    def _serialize_content(self, content: Any) -> Any:
        """Serialize content for storage."""
        if content is None:
            return None
        elif isinstance(content, (str, int, float, bool)):
            return content
        else:
            # For complex objects, try to convert to string representation
            try:
                return str(content)
            except Exception:
                return f"<Complex object of type {type(content).__name__}>"

    @classmethod
    def from_dict(cls, data: dict) -> 'ContextObject':
        """Create from dictionary."""
        # Extract metadata
        metadata_data = data.get('metadata', {})
        metadata = ContextMetadata.from_dict(metadata_data)

        # Extract compressed content
        compressed_hex = data.get('compressed_content')
        compressed_content = bytes.fromhex(compressed_hex) if compressed_hex else None

        # Create object
        obj = cls(
            content=data.get('content'),
            content_hash=data.get('content_hash', ''),
            metadata=metadata,
            raw_content=data.get('raw_content'),
            processed_content=data.get('processed_content'),
            embeddings=data.get('embeddings'),
            compressed_content=compressed_content,
            compression_algorithm=data.get('compression_algorithm', 'none'),
            is_loaded=data.get('is_loaded', True)
        )

        return obj

    def update_metadata(self, **kwargs) -> None:
        """Update metadata fields."""
        self.metadata.updated_at = datetime.now()

        for key, value in kwargs.items():
            if hasattr(self.metadata, key):
                setattr(self.metadata, key, value)

    def mark_accessed(self) -> None:
        """Mark the context as accessed."""
        self.metadata.update_access_time()
        self.metadata.calculate_importance_score()

    def get_size(self) -> int:
        """Get the size of the context object in bytes."""
        if self.metadata.is_compressed and self.compressed_content:
            return len(self.compressed_content)
        else:
            return self._estimate_content_size()

    def _estimate_content_size(self) -> int:
        """Estimate the size of content in bytes."""
        try:
            if isinstance(self.content, str):
                return len(self.content.encode('utf-8'))
            elif isinstance(self.content, (int, float, bool)):
                return 8  # Approximate size for numeric types
            else:
                return len(pickle.dumps(self.content, protocol=pickle.HIGHEST_PROTOCOL))
        except Exception:
            return 0


class ContextRetentionEngine:
    """Main engine for enhanced context retention and management."""

    def __init__(self, project_path: Path, config: Optional[dict] = None):
        self.project_path = Path(project_path)
        self.config = self._get_default_config()
        if config:
            self.config.update(config)

        # Initialize storage layers
        self.storage_layers = {
            ContextLayer.HOT: self._init_hot_storage(),
            ContextLayer.WARM: self._init_warm_storage(),
            ContextLayer.COLD: self._init_cold_storage(),
            ContextLayer.ARCHIVE: self._init_archive_storage()
        }

        # Context registry for tracking all objects
        self.context_registry: Dict[str, ContextObject] = {}
        self.registry_lock = threading.Lock()

        # Processing components
        self.prioritizer = ContextPrioritizer(self.config)
        self.compressor = ContextCompressor(self.config)

        # Performance tracking
        self.stats = {
            'contexts_stored': 0,
            'contexts_retrieved': 0,
            'storage_size_mb': 0,
            'compression_ratio': 0.0,
            'cache_hits': 0,
            'cache_misses': 0
        }

        # Background maintenance
        self.maintenance_thread = None
        self.maintenance_running = False

        logger.info(f"ContextRetentionEngine initialized for project: {self.project_path}")

    def _get_default_config(self) -> dict:
        """Get default configuration for the engine."""
        return {
            'max_hot_storage_mb': 100,
            'max_warm_storage_mb': 500,
            'max_cold_storage_mb': 2000,
            'max_archive_storage_mb': 10000,
            'compression_threshold_kb': 50,
            'auto_maintenance_interval_hours': 24,
            'context_ttl_hours': {
                ContextPriority.CRITICAL: 8760 * 24,  # ~1 year
                ContextPriority.HIGH: 720 * 24,      # ~1 month
                ContextPriority.MEDIUM: 168 * 24,    # ~1 week
                ContextPriority.LOW: 24 * 24,        # ~1 day
                ContextPriority.TRIVIAL: 2 * 24      # ~2 hours
            },
            'similarity_threshold': 0.7,
            'max_contexts_per_session': 1000,
            'enable_auto_compression': True,
            'enable_auto_archival': True,
            'maintenance_batch_size': 100
        }

    def _init_hot_storage(self) -> dict:
        """Initialize hot storage layer (in-memory cache)."""
        return {
            'contexts': {},  # context_id -> ContextObject
            'max_size_mb': self.config['max_hot_storage_mb'],
            'current_size_mb': 0,
            'access_order': deque(maxlen=1000)  # LRU tracking
        }

    def _init_warm_storage(self) -> dict:
        """Initialize warm storage layer (recent files)."""
        warm_path = self.project_path / ".goalkit" / "memory" / "warm"
        warm_path.mkdir(parents=True, exist_ok=True)

        return {
            'path': warm_path,
            'contexts': {},  # context_id -> metadata only
            'max_size_mb': self.config['max_warm_storage_mb'],
            'current_size_mb': self._calculate_directory_size(warm_path)
        }

    def _init_cold_storage(self) -> dict:
        """Initialize cold storage layer (compressed files)."""
        cold_path = self.project_path / ".goalkit" / "memory" / "cold"
        cold_path.mkdir(parents=True, exist_ok=True)

        return {
            'path': cold_path,
            'contexts': {},  # context_id -> metadata only
            'max_size_mb': self.config['max_cold_storage_mb'],
            'current_size_mb': self._calculate_directory_size(cold_path)
        }

    def _init_archive_storage(self) -> dict:
        """Initialize archive storage layer (long-term storage)."""
        archive_path = self.project_path / ".goalkit" / "memory" / "archive"
        archive_path.mkdir(parents=True, exist_ok=True)

        return {
            'path': archive_path,
            'contexts': {},  # context_id -> metadata only
            'max_size_mb': self.config['max_archive_storage_mb'],
            'current_size_mb': self._calculate_directory_size(archive_path)
        }

    def _calculate_directory_size(self, path: Path) -> int:
        """Calculate directory size in MB."""
        try:
            total_size = 0
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
            return total_size // (1024 * 1024)  # Convert to MB
        except Exception:
            return 0

    def store_context(self, context_obj: ContextObject) -> bool:
        """Store a context object in the appropriate layer."""
        try:
            with self.registry_lock:
                context_id = context_obj.metadata.context_id

                # Check for duplicates
                if context_id in self.context_registry:
                    logger.warning(f"Context {context_id} already exists, updating...")
                    return self.update_context(context_obj)

                # Determine appropriate layer
                target_layer = self.prioritizer.determine_storage_layer(context_obj)

                # Apply compression if needed
                if self._should_compress(context_obj):
                    self.compressor.compress_context(context_obj)

                # Store in target layer
                success = self._store_in_layer(context_obj, target_layer)

                if success:
                    # Register the context
                    self.context_registry[context_id] = context_obj
                    self.stats['contexts_stored'] += 1

                    # Update storage stats
                    self._update_storage_stats()

                    logger.debug(f"Stored context {context_id} in {target_layer.value} layer")
                    return True
                else:
                    logger.error(f"Failed to store context {context_id}")
                    return False

        except Exception as e:
            logger.error(f"Error storing context: {e}")
            return False

    def _should_compress(self, context_obj: ContextObject) -> bool:
        """Determine if context should be compressed."""
        if not self.config['enable_auto_compression']:
            return False

        size_kb = context_obj.get_size() / 1024
        return size_kb > self.config['compression_threshold_kb']

    def _store_in_layer(self, context_obj: ContextObject, layer: ContextLayer) -> bool:
        """Store context object in specified layer."""
        try:
            if layer == ContextLayer.HOT:
                return self._store_hot(context_obj)
            elif layer == ContextLayer.WARM:
                return self._store_warm(context_obj)
            elif layer == ContextLayer.COLD:
                return self._store_cold(context_obj)
            elif layer == ContextLayer.ARCHIVE:
                return self._store_archive(context_obj)
            else:
                logger.error(f"Unknown storage layer: {layer}")
                return False

        except Exception as e:
            logger.error(f"Error storing in layer {layer}: {e}")
            return False

    def _store_hot(self, context_obj: ContextObject) -> bool:
        """Store in hot layer (memory cache)."""
        hot_storage = self.storage_layers[ContextLayer.HOT]

        # Check size limits
        context_size_mb = context_obj.get_size() / (1024 * 1024)
        if hot_storage['current_size_mb'] + context_size_mb > hot_storage['max_size_mb']:
            # Evict least recently used items
            self._evict_hot_storage(int(context_size_mb))

        # Store the context
        context_id = context_obj.metadata.context_id
        hot_storage['contexts'][context_id] = context_obj
        hot_storage['access_order'].append(context_id)
        hot_storage['current_size_mb'] += context_size_mb

        return True

    def _evict_hot_storage(self, needed_mb: int):
        """Evict contexts from hot storage to make room."""
        hot_storage = self.storage_layers[ContextLayer.HOT]

        while (hot_storage['current_size_mb'] + needed_mb > hot_storage['max_size_mb']
               and hot_storage['contexts']):

            # Remove oldest context (simple LRU)
            if hot_storage['access_order']:
                oldest_id = hot_storage['access_order'].popleft()
                if oldest_id in hot_storage['contexts']:
                    evicted_context = hot_storage['contexts'].pop(oldest_id)
                    hot_storage['current_size_mb'] -= evicted_context.get_size() / (1024 * 1024)

                    # Move to warm storage
                    evicted_context.metadata.layer = ContextLayer.WARM
                    self._store_warm(evicted_context)

    def _store_warm(self, context_obj: ContextObject) -> bool:
        """Store in warm layer (recent files)."""
        return self._store_to_disk(context_obj, ContextLayer.WARM)

    def _store_cold(self, context_obj: ContextObject) -> bool:
        """Store in cold layer (compressed files)."""
        return self._store_to_disk(context_obj, ContextLayer.COLD)

    def _store_archive(self, context_obj: ContextObject) -> bool:
        """Store in archive layer (long-term storage)."""
        return self._store_to_disk(context_obj, ContextLayer.ARCHIVE)

    def _store_to_disk(self, context_obj: ContextObject, layer: ContextLayer) -> bool:
        """Store context object to disk in specified layer."""
        try:
            layer_storage = self.storage_layers[layer]
            layer_path = layer_storage['path']

            # Create layer-specific subdirectory if needed
            context_dir = layer_path / context_obj.metadata.context_id[:2]
            context_dir.mkdir(exist_ok=True)

            # Save context data
            context_file = context_dir / f"{context_obj.metadata.context_id}.json"

            # Convert to dictionary for storage
            context_data = context_obj.to_dict()

            with open(context_file, 'w', encoding='utf-8') as f:
                json.dump(context_data, f, indent=2, ensure_ascii=False)

            # Update layer storage info
            context_size_mb = context_obj.get_size() / (1024 * 1024)
            layer_storage['contexts'][context_obj.metadata.context_id] = context_obj.metadata
            layer_storage['current_size_mb'] += context_size_mb

            return True

        except Exception as e:
            logger.error(f"Error storing to disk in layer {layer}: {e}")
            return False

    def retrieve_context(self, context_id: str) -> Optional[ContextObject]:
        """Retrieve a context object by ID."""
        try:
            with self.registry_lock:
                # Check if already in registry
                if context_id in self.context_registry:
                    context_obj = self.context_registry[context_id]
                    context_obj.mark_accessed()
                    self.stats['cache_hits'] += 1
                    return context_obj

                # Search through storage layers
                for layer in [ContextLayer.HOT, ContextLayer.WARM, ContextLayer.COLD, ContextLayer.ARCHIVE]:
                    context_obj = self._retrieve_from_layer(context_id, layer)
                    if context_obj:
                        # Load into hot storage if retrieved from disk
                        if layer != ContextLayer.HOT:
                            context_obj.metadata.layer = ContextLayer.HOT
                            self._store_hot(context_obj)

                        # Register the context
                        self.context_registry[context_id] = context_obj
                        context_obj.mark_accessed()

                        self.stats['contexts_retrieved'] += 1
                        self.stats['cache_misses'] += 1

                        return context_obj

                logger.warning(f"Context {context_id} not found in any layer")
                return None

        except Exception as e:
            logger.error(f"Error retrieving context {context_id}: {e}")
            return None

    def _retrieve_from_layer(self, context_id: str, layer: ContextLayer) -> Optional[ContextObject]:
        """Retrieve context from specific layer."""
        try:
            layer_storage = self.storage_layers[layer]

            if layer == ContextLayer.HOT:
                # Direct memory access
                return layer_storage['contexts'].get(context_id)

            else:
                # File-based access
                context_file = layer_storage['path'] / context_id[:2] / f"{context_id}.json"

                if not context_file.exists():
                    return None

                with open(context_file, 'r', encoding='utf-8') as f:
                    context_data = json.load(f)

                context_obj = ContextObject.from_dict(context_data)

                # Decompress if needed
                if context_obj.metadata.is_compressed:
                    context_obj.decompress()

                return context_obj

        except Exception as e:
            logger.error(f"Error retrieving from layer {layer}: {e}")
            return None

    def update_context(self, context_obj: ContextObject) -> bool:
        """Update an existing context object."""
        try:
            context_id = context_obj.metadata.context_id

            with self.registry_lock:
                if context_id not in self.context_registry:
                    logger.warning(f"Context {context_id} not in registry, storing as new")
                    return self.store_context(context_obj)

                # Update metadata
                old_context = self.context_registry[context_id]
                old_size = old_context.get_size()

                # Update in registry
                self.context_registry[context_id] = context_obj

                # Update in storage layers
                current_layer = context_obj.metadata.layer
                success = self._store_in_layer(context_obj, current_layer)

                if success:
                    # Update size tracking
                    new_size = context_obj.get_size()
                    size_diff_mb = (new_size - old_size) / (1024 * 1024)

                    if current_layer != ContextLayer.HOT:
                        layer_storage = self.storage_layers[current_layer]
                        layer_storage['current_size_mb'] += size_diff_mb

                    self._update_storage_stats()
                    return True

                return False

        except Exception as e:
            logger.error(f"Error updating context: {e}")
            return False

    def delete_context(self, context_id: str) -> bool:
        """Delete a context object from all layers."""
        try:
            with self.registry_lock:
                if context_id not in self.context_registry:
                    return False

                context_obj = self.context_registry[context_id]

                # Remove from storage layers
                for layer in [ContextLayer.HOT, ContextLayer.WARM, ContextLayer.COLD, ContextLayer.ARCHIVE]:
                    self._delete_from_layer(context_id, layer)

                # Remove from registry
                del self.context_registry[context_id]

                # Update stats
                self._update_storage_stats()
                return True

        except Exception as e:
            logger.error(f"Error deleting context {context_id}: {e}")
            return False

    def _delete_from_layer(self, context_id: str, layer: ContextLayer) -> None:
        """Delete context from specific layer."""
        try:
            layer_storage = self.storage_layers[layer]

            if layer == ContextLayer.HOT:
                # Remove from memory
                if context_id in layer_storage['contexts']:
                    removed_context = layer_storage['contexts'].pop(context_id)
                    size_mb = removed_context.get_size() / (1024 * 1024)
                    layer_storage['current_size_mb'] -= size_mb

                    # Remove from access order
                    if context_id in layer_storage['access_order']:
                        layer_storage['access_order'].remove(context_id)

            else:
                # Remove from disk
                context_file = layer_storage['path'] / context_id[:2] / f"{context_id}.json"
                if context_file.exists():
                    size_mb = context_file.stat().st_size / (1024 * 1024)
                    context_file.unlink()
                    layer_storage['current_size_mb'] -= size_mb

                # Remove from layer index
                if context_id in layer_storage['contexts']:
                    del layer_storage['contexts'][context_id]

        except Exception as e:
            logger.error(f"Error deleting from layer {layer}: {e}")

    def find_similar_contexts(self, query_context: ContextObject, limit: int = 10) -> List[ContextObject]:
        """Find contexts similar to the query context."""
        similar_contexts = []

        try:
            with self.registry_lock:
                for context_id, context_obj in self.context_registry.items():
                    # Calculate similarity (simplified implementation)
                    similarity = self._calculate_similarity(query_context, context_obj)

                    if similarity >= self.config['similarity_threshold']:
                        similar_contexts.append((context_obj, similarity))

                # Sort by similarity and return top results
                similar_contexts.sort(key=lambda x: x[1], reverse=True)
                return [ctx for ctx, _ in similar_contexts[:limit]]

        except Exception as e:
            logger.error(f"Error finding similar contexts: {e}")
            return []

    def _calculate_similarity(self, context1: ContextObject, context2: ContextObject) -> float:
        """Calculate similarity between two contexts (simplified implementation)."""
        # This is a placeholder - in a real implementation, you would use
        # embeddings and cosine similarity or other ML-based approaches

        similarity = 0.0

        # Compare tags
        if context1.metadata.tags and context2.metadata.tags:
            common_tags = set(context1.metadata.tags) & set(context2.metadata.tags)
            if common_tags:
                similarity += 0.3 * (len(common_tags) / max(len(context1.metadata.tags), len(context2.metadata.tags)))

        # Compare categories
        if context1.metadata.categories and context2.metadata.categories:
            common_categories = set(context1.metadata.categories) & set(context2.metadata.categories)
            if common_categories:
                similarity += 0.2 * (len(common_categories) / max(len(context1.metadata.categories), len(context2.metadata.categories)))

        # Compare content hash (exact match)
        if context1.content_hash == context2.content_hash:
            similarity += 0.5

        return min(similarity, 1.0)

    def get_contexts_by_layer(self, layer: ContextLayer) -> List[ContextObject]:
        """Get all contexts in a specific layer."""
        contexts = []

        try:
            layer_storage = self.storage_layers[layer]

            if layer == ContextLayer.HOT:
                # Return contexts from memory
                contexts = list(layer_storage['contexts'].values())
            else:
                # Load contexts from disk
                for context_id in layer_storage['contexts'].keys():
                    context_obj = self.retrieve_context(context_id)
                    if context_obj:
                        contexts.append(context_obj)

            return contexts

        except Exception as e:
            logger.error(f"Error getting contexts from layer {layer}: {e}")
            return []

    def _update_storage_stats(self) -> None:
        """Update storage statistics."""
        total_size = 0

        for layer_storage in self.storage_layers.values():
            if 'current_size_mb' in layer_storage:
                total_size += layer_storage['current_size_mb']

        self.stats['storage_size_mb'] = total_size

        # Calculate compression ratio
        original_size = sum(
            ctx.get_size() for ctx in self.context_registry.values()
            if not ctx.metadata.is_compressed
        )
        compressed_size = sum(
            ctx.metadata.compressed_size for ctx in self.context_registry.values()
            if ctx.metadata.is_compressed
        )

        if original_size > 0:
            self.stats['compression_ratio'] = compressed_size / original_size

    def get_stats(self) -> dict:
        """Get engine statistics."""
        return self.stats.copy()

    def start_maintenance(self) -> None:
        """Start background maintenance tasks."""
        if self.maintenance_running:
            return

        self.maintenance_running = True
        self.maintenance_thread = threading.Thread(target=self._maintenance_loop, daemon=True)
        self.maintenance_thread.start()
        logger.info("Context retention engine maintenance started")

    def stop_maintenance(self) -> None:
        """Stop background maintenance tasks."""
        self.maintenance_running = False
        if self.maintenance_thread:
            self.maintenance_thread.join(timeout=5)
        logger.info("Context retention engine maintenance stopped")

    def _maintenance_loop(self) -> None:
        """Background maintenance loop."""
        while self.maintenance_running:
            try:
                self._perform_maintenance()
                # Sleep for configured interval
                interval_seconds = self.config['auto_maintenance_interval_hours'] * 3600
                threading.Event().wait(interval_seconds)

            except Exception as e:
                logger.error(f"Error in maintenance loop: {e}")
                threading.Event().wait(3600)  # Wait 1 hour on error

    def _perform_maintenance(self) -> None:
        """Perform maintenance tasks."""
        try:
            logger.debug("Performing context retention maintenance")

            # Move expired contexts to lower layers
            self._cleanup_expired_contexts()

            # Rebalance storage layers
            self._rebalance_storage_layers()

            # Update importance scores
            self._update_importance_scores()

            logger.debug("Maintenance completed")

        except Exception as e:
            logger.error(f"Error during maintenance: {e}")

    def _cleanup_expired_contexts(self) -> None:
        """Remove or move expired contexts."""
        current_time = datetime.now()
        expired_contexts = []

        with self.registry_lock:
            for context_id, context_obj in self.context_registry.items():
                # Check expiration
                if (context_obj.metadata.expires_at and
                    current_time > context_obj.metadata.expires_at):

                    expired_contexts.append(context_id)

                # Check TTL based on priority
                elif self._is_beyond_ttl(context_obj, current_time):
                    # Move to lower priority layer instead of deleting
                    if context_obj.metadata.layer != ContextLayer.ARCHIVE:
                        context_obj.metadata.layer = self._get_lower_layer(context_obj.metadata.layer)
                        self._store_in_layer(context_obj, context_obj.metadata.layer)

        # Remove truly expired contexts
        for context_id in expired_contexts:
            self.delete_context(context_id)

    def _is_beyond_ttl(self, context_obj: ContextObject, current_time: datetime) -> bool:
        """Check if context is beyond its TTL."""
        created_hours_ago = (current_time - context_obj.metadata.created_at).total_seconds() / 3600

        priority = context_obj.metadata.priority
        ttl_hours = self.config['context_ttl_hours'].get(priority, 168 * 24)  # Default 1 week

        return created_hours_ago > ttl_hours

    def _get_lower_layer(self, current_layer: ContextLayer) -> ContextLayer:
        """Get the next lower layer."""
        layer_order = [ContextLayer.HOT, ContextLayer.WARM, ContextLayer.COLD, ContextLayer.ARCHIVE]
        current_index = layer_order.index(current_layer)

        if current_index < len(layer_order) - 1:
            return layer_order[current_index + 1]
        else:
            return ContextLayer.ARCHIVE

    def _rebalance_storage_layers(self) -> None:
        """Rebalance contexts across storage layers based on access patterns."""
        # Move frequently accessed contexts to higher layers
        for context_id, context_obj in list(self.context_registry.items()):
            if (context_obj.metadata.access_count > 10 and
                context_obj.metadata.layer != ContextLayer.HOT):

                # Try to move to hot storage
                if self._can_fit_in_hot(context_obj):
                    context_obj.metadata.layer = ContextLayer.HOT
                    self._store_hot(context_obj)

    def _can_fit_in_hot(self, context_obj: ContextObject) -> bool:
        """Check if context can fit in hot storage."""
        hot_storage = self.storage_layers[ContextLayer.HOT]
        context_size_mb = context_obj.get_size() / (1024 * 1024)

        return (hot_storage['current_size_mb'] + context_size_mb <= hot_storage['max_size_mb'])

    def _update_importance_scores(self) -> None:
        """Update importance scores for all contexts."""
        for context_obj in self.context_registry.values():
            context_obj.metadata.calculate_importance_score()

    def cleanup(self) -> None:
        """Clean up resources."""
        self.stop_maintenance()

        # Save any unsaved contexts
        for context_obj in self.context_registry.values():
            if context_obj.metadata.layer == ContextLayer.HOT:
                # Move to warm storage before shutdown
                context_obj.metadata.layer = ContextLayer.WARM
                self._store_warm(context_obj)

        logger.info("ContextRetentionEngine cleanup completed")


class ContextPrioritizer:
    """Intelligent context prioritization for optimal storage and retrieval."""

    def __init__(self, config: dict):
        self.config = config
        self.priority_weights = {
            'recency': 0.25,
            'frequency': 0.20,
            'relevance': 0.25,
            'importance': 0.15,
            'relationships': 0.15
        }

        # Priority thresholds for layer assignment
        self.layer_thresholds = {
            ContextLayer.HOT: 0.8,
            ContextLayer.WARM: 0.6,
            ContextLayer.COLD: 0.3,
            ContextLayer.ARCHIVE: 0.0
        }

    def calculate_priority_score(self, context_obj: ContextObject) -> float:
        """Calculate overall priority score for a context object."""
        try:
            scores = {
                'recency': self._calculate_recency_score(context_obj),
                'frequency': self._calculate_frequency_score(context_obj),
                'relevance': self._calculate_relevance_score(context_obj),
                'importance': context_obj.metadata.importance_score,
                'relationships': self._calculate_relationship_score(context_obj)
            }

            # Calculate weighted score
            total_score = sum(
                scores[factor] * weight
                for factor, weight in self.priority_weights.items()
            )

            return min(total_score, 1.0)

        except Exception as e:
            logger.error(f"Error calculating priority score: {e}")
            return 0.5  # Default medium priority

    def _calculate_recency_score(self, context_obj: ContextObject) -> float:
        """Calculate recency score based on access patterns."""
        now = datetime.now()

        # Base recency on last access time
        hours_since_access = (now - context_obj.metadata.accessed_at).total_seconds() / 3600

        # Exponential decay - more recent = higher score
        if hours_since_access < 1:
            return 1.0
        elif hours_since_access < 24:
            return 0.8
        elif hours_since_access < 168:  # 1 week
            return 0.6
        elif hours_since_access < 720:  # 1 month
            return 0.4
        else:
            return 0.2

    def _calculate_frequency_score(self, context_obj: ContextObject) -> float:
        """Calculate frequency score based on access count."""
        access_count = context_obj.metadata.access_count

        # Logarithmic scaling for access frequency
        if access_count == 0:
            return 0.0
        elif access_count < 5:
            return 0.3
        elif access_count < 20:
            return 0.6
        elif access_count < 100:
            return 0.8
        else:
            return 1.0

    def _calculate_relevance_score(self, context_obj: ContextObject) -> float:
        """Calculate relevance score based on content analysis."""
        # Use existing relevance score from metadata
        base_relevance = context_obj.metadata.relevance_score

        # Boost score for contexts with high completeness and accuracy
        quality_multiplier = (context_obj.metadata.completeness_score +
                            context_obj.metadata.accuracy_score) / 2.0

        return base_relevance * quality_multiplier

    def _calculate_relationship_score(self, context_obj: ContextObject) -> float:
        """Calculate score based on relationships with other contexts."""
        metadata = context_obj.metadata

        # Count relationships
        relationship_count = (len(metadata.child_context_ids) +
                           len(metadata.related_context_ids) +
                           (1 if metadata.parent_context_id else 0))

        # Normalize relationship count
        if relationship_count == 0:
            return 0.2  # Base score for isolated contexts
        elif relationship_count < 5:
            return 0.5
        elif relationship_count < 20:
            return 0.8
        else:
            return 1.0

    def determine_storage_layer(self, context_obj: ContextObject) -> ContextLayer:
        """Determine the appropriate storage layer for a context object."""
        priority_score = self.calculate_priority_score(context_obj)

        # Assign layer based on priority thresholds
        if priority_score >= self.layer_thresholds[ContextLayer.HOT]:
            return ContextLayer.HOT
        elif priority_score >= self.layer_thresholds[ContextLayer.WARM]:
            return ContextLayer.WARM
        elif priority_score >= self.layer_thresholds[ContextLayer.COLD]:
            return ContextLayer.COLD
        else:
            return ContextLayer.ARCHIVE

    def prioritize_contexts(self, contexts: List[ContextObject]) -> List[ContextObject]:
        """Sort contexts by priority (highest first)."""
        try:
            # Calculate priority scores for all contexts
            scored_contexts = []
            for context in contexts:
                score = self.calculate_priority_score(context)
                scored_contexts.append((context, score))

            # Sort by score (highest first)
            scored_contexts.sort(key=lambda x: x[1], reverse=True)

            return [context for context, _ in scored_contexts]

        except Exception as e:
            logger.error(f"Error prioritizing contexts: {e}")
            return contexts  # Return original order on error

    def get_retention_candidates(self, contexts: List[ContextObject],
                               max_contexts: int) -> List[ContextObject]:
        """Get the top contexts that should be retained based on priority."""
        prioritized = self.prioritize_contexts(contexts)
        return prioritized[:max_contexts]

    def should_evict_context(self, context_obj: ContextObject,
                           storage_pressure: float) -> bool:
        """Determine if a context should be evicted based on storage pressure."""
        priority_score = self.calculate_priority_score(context_obj)

        # Higher storage pressure = lower eviction threshold
        eviction_threshold = max(0.1, 0.5 - (storage_pressure * 0.3))

        return priority_score < eviction_threshold

    def analyze_context_value(self, context_obj: ContextObject) -> dict:
        """Analyze the value of a context object across multiple dimensions."""
        return {
            'priority_score': self.calculate_priority_score(context_obj),
            'recency_score': self._calculate_recency_score(context_obj),
            'frequency_score': self._calculate_frequency_score(context_obj),
            'relevance_score': self._calculate_relevance_score(context_obj),
            'relationship_score': self._calculate_relationship_score(context_obj),
            'importance_score': context_obj.metadata.importance_score,
            'recommended_layer': self.determine_storage_layer(context_obj).value,
            'eviction_risk': self._calculate_eviction_risk(context_obj)
        }

    def _calculate_eviction_risk(self, context_obj: ContextObject) -> float:
        """Calculate the risk of a context being evicted."""
        priority_score = self.calculate_priority_score(context_obj)

        # Lower priority = higher eviction risk
        return max(0.0, 1.0 - priority_score)

    def update_priority_weights(self, new_weights: dict) -> None:
        """Update priority calculation weights."""
        if not new_weights:
            return

        # Normalize weights to sum to 1.0
        total_weight = sum(new_weights.values())
        if total_weight > 0:
            for factor in self.priority_weights:
                if factor in new_weights:
                    self.priority_weights[factor] = new_weights[factor] / total_weight

    def get_priority_explanation(self, context_obj: ContextObject) -> str:
        """Get human-readable explanation of priority calculation."""
        analysis = self.analyze_context_value(context_obj)

        explanation = f"""
Priority Analysis for Context {context_obj.metadata.context_id}:
- Overall Priority Score: {analysis['priority_score']:.3f"}
- Recommended Layer: {analysis['recommended_layer']}
- Eviction Risk: {analysis['eviction_risk']:.3f"}

Breakdown:
- Recency Score: {analysis['recency_score']:.3f"} (accessed {self._get_time_ago_text(context_obj.metadata.accessed_at)})
- Frequency Score: {analysis['frequency_score']:.3f"} ({context_obj.metadata.access_count} accesses)
- Relevance Score: {analysis['relevance_score']:.3f"}
- Relationship Score: {analysis['relationship_score']:.3f"}
- Importance Score: {analysis['importance_score']:.3f"}
"""

        return explanation.strip()

    def _get_time_ago_text(self, dt: datetime) -> str:
        """Get human-readable time ago text."""
        now = datetime.now()
        diff = now - dt

        if diff.total_seconds() < 3600:
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes} minutes ago"
        elif diff.total_seconds() < 86400:
            hours = int(diff.total_seconds() / 3600)
            return f"{hours} hours ago"
        else:
            days = int(diff.total_seconds() / 86400)
            return f"{days} days ago"


class ContextCompressor:
    """Advanced compression system for context data."""

    def __init__(self, config: dict):
        self.config = config
        self.compression_stats = {
            'total_compressed': 0,
            'total_original_size': 0,
            'compression_attempts': 0,
            'compression_failures': 0
        }

        # Supported compression algorithms
        self.algorithms = {
            'zlib': self._compress_zlib,
            'gzip': self._compress_gzip,
            'lz4': self._compress_lz4,
            'zstd': self._compress_zstd,
            'brotli': self._compress_brotli
        }

        # Algorithm selection strategy
        self.compression_strategy = self._select_compression_strategy()

    def _select_compression_strategy(self) -> str:
        """Select the best compression strategy based on configuration."""
        # For now, use zlib as default
        # In a more advanced implementation, this could analyze content types
        # and select optimal algorithms
        return 'zlib'

    def compress_context(self, context_obj: ContextObject) -> bool:
        """Compress a context object using the best available algorithm."""
        try:
            if context_obj.metadata.is_compressed:
                logger.warning("Context is already compressed")
                return True

            self.compression_stats['compression_attempts'] += 1

            # Get content to compress
            content = self._get_compressible_content(context_obj)
            if not content:
                logger.warning("No compressible content found")
                return False

            # Try compression algorithms in order of preference
            algorithms_to_try = self._get_algorithm_priority()

            for algorithm in algorithms_to_try:
                if algorithm in self.algorithms:
                    success, compressed_data, original_size, compressed_size = self.algorithms[algorithm](content)

                    if success:
                        # Update context object
                        context_obj.compressed_content = compressed_data
                        context_obj.compression_algorithm = algorithm
                        context_obj.metadata.is_compressed = True
                        context_obj.metadata.content_size = original_size
                        context_obj.metadata.compressed_size = compressed_size

                        # Update stats
                        self.compression_stats['total_compressed'] += 1
                        self.compression_stats['total_original_size'] += original_size

                        logger.debug(f"Successfully compressed context {context_obj.metadata.context_id} "
                                   f"using {algorithm} ({original_size} -> {compressed_size} bytes)")
                        return True

            logger.warning(f"Failed to compress context {context_obj.metadata.context_id}")
            self.compression_stats['compression_failures'] += 1
            return False

        except Exception as e:
            logger.error(f"Error compressing context: {e}")
            self.compression_stats['compression_failures'] += 1
            return False

    def _get_compressible_content(self, context_obj: ContextObject) -> Any:
        """Extract content that can be compressed."""
        # Try different content sources in order of preference
        if context_obj.content is not None:
            return context_obj.content
        elif context_obj.raw_content is not None:
            return context_obj.raw_content
        elif context_obj.processed_content is not None:
            return context_obj.processed_content
        else:
            return None

    def _get_algorithm_priority(self) -> List[str]:
        """Get compression algorithms in order of preference."""
        # Default priority order
        return ['zlib', 'gzip', 'lz4', 'zstd', 'brotli']

    def _compress_zlib(self, content: Any) -> Tuple[bool, bytes, int, int]:
        """Compress using zlib."""
        try:
            import zlib

            # Convert content to bytes
            if isinstance(content, str):
                content_bytes = content.encode('utf-8')
            else:
                content_bytes = pickle.dumps(content, protocol=pickle.HIGHEST_PROTOCOL)

            original_size = len(content_bytes)
            compressed_data = zlib.compress(content_bytes, level=6)
            compressed_size = len(compressed_data)

            return True, compressed_data, original_size, compressed_size

        except Exception as e:
            logger.debug(f"Zlib compression failed: {e}")
            return False, b'', 0, 0

    def _compress_gzip(self, content: Any) -> Tuple[bool, bytes, int, int]:
        """Compress using gzip."""
        try:
            import gzip
            import io

            # Convert content to bytes
            if isinstance(content, str):
                content_bytes = content.encode('utf-8')
            else:
                content_bytes = pickle.dumps(content, protocol=pickle.HIGHEST_PROTOCOL)

            original_size = len(content_bytes)

            # Compress using gzip
            compressed_buffer = io.BytesIO()
            with gzip.GzipFile(fileobj=compressed_buffer, mode='wb', compresslevel=6) as f:
                f.write(content_bytes)

            compressed_data = compressed_buffer.getvalue()
            compressed_size = len(compressed_data)

            return True, compressed_data, original_size, compressed_size

        except Exception as e:
            logger.debug(f"Gzip compression failed: {e}")
            return False, b'', 0, 0

    def _compress_lz4(self, content: Any) -> Tuple[bool, bytes, int, int]:
        """Compress using LZ4 (if available)."""
        try:
            import lz4.frame

            # Convert content to bytes
            if isinstance(content, str):
                content_bytes = content.encode('utf-8')
            else:
                content_bytes = pickle.dumps(content, protocol=pickle.HIGHEST_PROTOCOL)

            original_size = len(content_bytes)
            compressed_data = lz4.frame.compress(content_bytes, compression_level=1)
            compressed_size = len(compressed_data)

            return True, compressed_data, original_size, compressed_size

        except ImportError:
            logger.debug("LZ4 not available")
            return False, b'', 0, 0
        except Exception as e:
            logger.debug(f"LZ4 compression failed: {e}")
            return False, b'', 0, 0

    def _compress_zstd(self, content: Any) -> Tuple[bool, bytes, int, int]:
        """Compress using Zstandard (if available)."""
        try:
            import zstandard as zstd

            # Convert content to bytes
            if isinstance(content, str):
                content_bytes = content.encode('utf-8')
            else:
                content_bytes = pickle.dumps(content, protocol=pickle.HIGHEST_PROTOCOL)

            original_size = len(content_bytes)

            # Compress using zstd
            ctx = zstd.ZstdCompressor(level=3)
            compressed_data = ctx.compress(content_bytes)
            compressed_size = len(compressed_data)

            return True, compressed_data, original_size, compressed_size

        except ImportError:
            logger.debug("Zstandard not available")
            return False, b'', 0, 0
        except Exception as e:
            logger.debug(f"Zstd compression failed: {e}")
            return False, b'', 0, 0

    def _compress_brotli(self, content: Any) -> Tuple[bool, bytes, int, int]:
        """Compress using Brotli (if available)."""
        try:
            import brotli

            # Convert content to bytes
            if isinstance(content, str):
                content_bytes = content.encode('utf-8')
            else:
                content_bytes = pickle.dumps(content, protocol=pickle.HIGHEST_PROTOCOL)

            original_size = len(content_bytes)
            compressed_data = brotli.compress(content_bytes, quality=6)
            compressed_size = len(compressed_data)

            return True, compressed_data, original_size, compressed_size

        except ImportError:
            logger.debug("Brotli not available")
            return False, b'', 0, 0
        except Exception as e:
            logger.debug(f"Brotli compression failed: {e}")
            return False, b'', 0, 0

    def decompress_context(self, context_obj: ContextObject) -> bool:
        """Decompress a context object."""
        try:
            if not context_obj.metadata.is_compressed or not context_obj.compressed_content:
                logger.warning("Context is not compressed")
                return True

            algorithm = context_obj.compression_algorithm
            if algorithm not in self.algorithms:
                logger.error(f"Unknown compression algorithm: {algorithm}")
                return False

            # Get decompression function
            if algorithm == 'zlib':
                success, decompressed_data = self._decompress_zlib(context_obj.compressed_content)
            elif algorithm == 'gzip':
                success, decompressed_data = self._decompress_gzip(context_obj.compressed_content)
            elif algorithm == 'lz4':
                success, decompressed_data = self._decompress_lz4(context_obj.compressed_content)
            elif algorithm == 'zstd':
                success, decompressed_data = self._decompress_zstd(context_obj.compressed_content)
            elif algorithm == 'brotli':
                success, decompressed_data = self._decompress_brotli(context_obj.compressed_content)
            else:
                logger.error(f"No decompression function for algorithm: {algorithm}")
                return False

            if success:
                # Try to decode as string first, then as pickle
                try:
                    context_obj.content = decompressed_data.decode('utf-8')
                except UnicodeDecodeError:
                    context_obj.content = pickle.loads(decompressed_data)

                context_obj.metadata.is_compressed = False
                context_obj.compressed_content = None
                context_obj.compression_algorithm = 'none'

                logger.debug(f"Successfully decompressed context {context_obj.metadata.context_id}")
                return True
            else:
                logger.error(f"Failed to decompress context {context_obj.metadata.context_id}")
                return False

        except Exception as e:
            logger.error(f"Error decompressing context: {e}")
            return False

    def _decompress_zlib(self, compressed_data: bytes) -> Tuple[bool, bytes]:
        """Decompress zlib data."""
        try:
            import zlib
            decompressed_data = zlib.decompress(compressed_data)
            return True, decompressed_data
        except Exception as e:
            logger.debug(f"Zlib decompression failed: {e}")
            return False, b''

    def _decompress_gzip(self, compressed_data: bytes) -> Tuple[bool, bytes]:
        """Decompress gzip data."""
        try:
            import gzip
            import io

            with gzip.GzipFile(fileobj=io.BytesIO(compressed_data), mode='rb') as f:
                decompressed_data = f.read()
            return True, decompressed_data

        except Exception as e:
            logger.debug(f"Gzip decompression failed: {e}")
            return False, b''

    def _decompress_lz4(self, compressed_data: bytes) -> Tuple[bool, bytes]:
        """Decompress LZ4 data."""
        try:
            import lz4.frame
            decompressed_data = lz4.frame.decompress(compressed_data)
            return True, decompressed_data
        except ImportError:
            logger.debug("LZ4 not available for decompression")
            return False, b''
        except Exception as e:
            logger.debug(f"LZ4 decompression failed: {e}")
            return False, b''

    def _decompress_zstd(self, compressed_data: bytes) -> Tuple[bool, bytes]:
        """Decompress Zstandard data."""
        try:
            import zstandard as zstd

            ctx = zstd.ZstdDecompressor()
            decompressed_data = ctx.decompress(compressed_data)
            return True, decompressed_data

        except ImportError:
            logger.debug("Zstandard not available for decompression")
            return False, b''
        except Exception as e:
            logger.debug(f"Zstd decompression failed: {e}")
            return False, b''

    def _decompress_brotli(self, compressed_data: bytes) -> Tuple[bool, bytes]:
        """Decompress Brotli data."""
        try:
            import brotli
            decompressed_data = brotli.decompress(compressed_data)
            return True, decompressed_data
        except ImportError:
            logger.debug("Brotli not available for decompression")
            return False, b''
        except Exception as e:
            logger.debug(f"Brotli decompression failed: {e}")
            return False, b''

    def get_compression_ratio(self, context_obj: ContextObject) -> float:
        """Get compression ratio for a context object."""
        if not context_obj.metadata.is_compressed:
            return 1.0

        original_size = context_obj.metadata.content_size
        compressed_size = context_obj.metadata.compressed_size

        if original_size > 0:
            return compressed_size / original_size
        else:
            return 1.0

    def should_compress(self, context_obj: ContextObject) -> bool:
        """Determine if a context should be compressed."""
        if context_obj.metadata.is_compressed:
            return False

        content_size = context_obj.get_size()

        # Check size threshold
        size_threshold = self.config.get('compression_threshold_kb', 50) * 1024
        if content_size < size_threshold:
            return False

        # Check content type suitability
        content_type = context_obj.metadata.content_type.lower()
        compressible_types = ['text', 'json', 'xml', 'code', 'structured']

        return any(ct in content_type for ct in compressible_types)

    def get_optimal_algorithm(self, content: Any) -> str:
        """Get the optimal compression algorithm for specific content."""
        # Simple heuristic-based selection
        # In a more advanced implementation, this could analyze content characteristics

        if isinstance(content, str):
            # Text content - try multiple algorithms
            return 'zlib'  # Default choice
        else:
            # Binary/complex content - prefer algorithms that handle it well
            return 'zlib'

    def get_compression_stats(self) -> dict:
        """Get compression statistics."""
        stats = self.compression_stats.copy()

        # Calculate derived metrics
        if stats['total_original_size'] > 0:
            stats['overall_compression_ratio'] = (stats['total_original_size'] -
                                               (stats['total_original_size'] * stats.get('overall_compression_ratio', 0))) / stats['total_original_size']
        else:
            stats['overall_compression_ratio'] = 0.0

        stats['success_rate'] = (stats['total_compressed'] /
                               max(stats['compression_attempts'], 1))

        return stats


class EnhancedContextConfig:
    """Configuration management for enhanced context retention system."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path
        self.config = self._get_default_config()
        self.config_listeners = []

        if config_path:
            self.load_config()

    def _get_default_config(self) -> dict:
        """Get default configuration values."""
        return {
            # Storage layer limits (in MB)
            'max_hot_storage_mb': 100,
            'max_warm_storage_mb': 500,
            'max_cold_storage_mb': 2000,
            'max_archive_storage_mb': 10000,

            # Compression settings
            'compression_threshold_kb': 50,
            'enable_auto_compression': True,
            'preferred_compression_algorithm': 'zlib',
            'compression_level': 6,

            # Context lifecycle settings (in hours)
            'context_ttl_hours': {
                ContextPriority.CRITICAL.value: 8760 * 24,  # ~1 year
                ContextPriority.HIGH.value: 720 * 24,       # ~1 month
                ContextPriority.MEDIUM.value: 168 * 24,     # ~1 week
                ContextPriority.LOW.value: 24 * 24,         # ~1 day
                ContextPriority.TRIVIAL.value: 2 * 24       # ~2 hours
            },

            # Maintenance settings
            'auto_maintenance_interval_hours': 24,
            'enable_auto_maintenance': True,
            'maintenance_batch_size': 100,
            'enable_auto_archival': True,

            # Priority calculation weights
            'priority_weights': {
                'recency': 0.25,
                'frequency': 0.20,
                'relevance': 0.25,
                'importance': 0.15,
                'relationships': 0.15
            },

            # Layer assignment thresholds
            'layer_thresholds': {
                ContextLayer.HOT.value: 0.8,
                ContextLayer.WARM.value: 0.6,
                ContextLayer.COLD.value: 0.3,
                ContextLayer.ARCHIVE.value: 0.0
            },

            # Similarity settings
            'similarity_threshold': 0.7,
            'max_similar_contexts': 10,

            # Performance settings
            'max_contexts_per_session': 1000,
            'enable_background_processing': True,
            'cache_size_limit_mb': 50,

            # Logging settings
            'log_level': 'INFO',
            'enable_detailed_logging': False,
            'log_rotation_days': 7,

            # Advanced features
            'enable_ml_embeddings': False,
            'enable_semantic_search': False,
            'enable_auto_tagging': True,
            'enable_context_deduplication': True
        }

    def load_config(self) -> bool:
        """Load configuration from file."""
        if not self.config_path or not self.config_path.exists():
            return False

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                file_config = json.load(f)

            # Merge with defaults (file config takes precedence)
            self._deep_merge(self.config, file_config)

            # Validate configuration
            if self.validate_config():
                logger.info(f"Configuration loaded from {self.config_path}")
                self._notify_listeners()
                return True
            else:
                logger.error("Invalid configuration, using defaults")
                return False

        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return False

    def save_config(self) -> bool:
        """Save current configuration to file."""
        if not self.config_path:
            logger.error("No config path specified")
            return False

        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)

            logger.info(f"Configuration saved to {self.config_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False

    def _deep_merge(self, base_dict: dict, update_dict: dict) -> None:
        """Deep merge update_dict into base_dict."""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_merge(base_dict[key], value)
            else:
                base_dict[key] = value

    def validate_config(self) -> bool:
        """Validate configuration values."""
        try:
            # Validate storage limits
            for layer in ['hot', 'warm', 'cold', 'archive']:
                max_key = f'max_{layer}_storage_mb'
                if max_key in self.config:
                    if not isinstance(self.config[max_key], int) or self.config[max_key] <= 0:
                        logger.error(f"Invalid {max_key}: must be positive integer")
                        return False

            # Validate compression threshold
            threshold = self.config.get('compression_threshold_kb', 0)
            if not isinstance(threshold, int) or threshold < 0:
                logger.error("Invalid compression_threshold_kb: must be non-negative integer")
                return False

            # Validate TTL values
            ttl_config = self.config.get('context_ttl_hours', {})
            for priority_value, ttl_hours in ttl_config.items():
                if not isinstance(ttl_hours, (int, float)) or ttl_hours <= 0:
                    logger.error(f"Invalid TTL for priority {priority_value}: must be positive number")
                    return False

            # Validate priority weights sum to approximately 1.0
            weights = self.config.get('priority_weights', {})
            total_weight = sum(weights.values())
            if abs(total_weight - 1.0) > 0.01:
                logger.error(f"Priority weights must sum to 1.0, got {total_weight}")
                return False

            # Validate layer thresholds are in descending order
            thresholds = self.config.get('layer_thresholds', {})
            prev_threshold = 2.0  # Start higher than max possible
            for layer in [ContextLayer.HOT.value, ContextLayer.WARM.value,
                         ContextLayer.COLD.value, ContextLayer.ARCHIVE.value]:
                threshold = thresholds.get(layer, 0)
                if threshold >= prev_threshold:
                    logger.error(f"Layer thresholds must be in descending order, {layer} threshold {threshold} >= {prev_threshold}")
                    return False
                prev_threshold = threshold

            return True

        except Exception as e:
            logger.error(f"Configuration validation error: {e}")
            return False

    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._get_nested_value(self.config, key, default)

    def set_config_value(self, key: str, value: Any) -> bool:
        """Set a configuration value."""
        try:
            keys = key.split('.')
            config = self.config

            # Navigate to parent of target key
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]

            # Set the value
            config[keys[-1]] = value

            # Validate and save if valid
            if self.validate_config():
                self.save_config()
                self._notify_listeners()
                return True
            else:
                # Revert on validation failure
                self.load_config()
                return False

        except Exception as e:
            logger.error(f"Error setting config value {key}={value}: {e}")
            return False

    def _get_nested_value(self, config: dict, key: str, default: Any) -> Any:
        """Get nested configuration value."""
        try:
            keys = key.split('.')
            value = config

            for k in keys:
                value = value[k]

            return value

        except (KeyError, TypeError):
            return default

    def add_config_listener(self, listener) -> None:
        """Add a configuration change listener."""
        self.config_listeners.append(listener)

    def remove_config_listener(self, listener) -> None:
        """Remove a configuration change listener."""
        if listener in self.config_listeners:
            self.config_listeners.remove(listener)

    def _notify_listeners(self) -> None:
        """Notify listeners of configuration changes."""
        for listener in self.config_listeners:
            try:
                listener.on_config_changed(self.config)
            except Exception as e:
                logger.error(f"Error notifying config listener: {e}")

    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults."""
        self.config = self._get_default_config()
        self.save_config()
        self._notify_listeners()
        logger.info("Configuration reset to defaults")

    def export_config(self) -> str:
        """Export configuration as JSON string."""
        return json.dumps(self.config, indent=2, ensure_ascii=False)

    def import_config(self, config_json: str) -> bool:
        """Import configuration from JSON string."""
        try:
            imported_config = json.loads(config_json)
            old_config = self.config.copy()

            # Apply imported config
            self._deep_merge(self.config, imported_config)

            # Validate
            if self.validate_config():
                self.save_config()
                self._notify_listeners()
                return True
            else:
                # Revert on validation failure
                self.config = old_config
                return False

        except Exception as e:
            logger.error(f"Error importing configuration: {e}")
            return False

    def get_config_summary(self) -> dict:
        """Get a summary of current configuration."""
        return {
            'storage_limits': {
                'hot_mb': self.config['max_hot_storage_mb'],
                'warm_mb': self.config['max_warm_storage_mb'],
                'cold_mb': self.config['max_cold_storage_mb'],
                'archive_mb': self.config['max_archive_storage_mb']
            },
            'compression': {
                'enabled': self.config['enable_auto_compression'],
                'threshold_kb': self.config['compression_threshold_kb'],
                'algorithm': self.config['preferred_compression_algorithm']
            },
            'maintenance': {
                'auto_maintenance': self.config['enable_auto_maintenance'],
                'interval_hours': self.config['auto_maintenance_interval_hours'],
                'auto_archival': self.config['enable_auto_archival']
            },
            'features': {
                'ml_embeddings': self.config['enable_ml_embeddings'],
                'semantic_search': self.config['enable_semantic_search'],
                'auto_tagging': self.config['enable_auto_tagging'],
                'context_deduplication': self.config['enable_context_deduplication']
            }
        }


class ConfigurationListener:
    """Base class for configuration change listeners."""

    def on_config_changed(self, new_config: dict) -> None:
        """Called when configuration changes."""
        pass

    def reset_stats(self) -> None:
        """Reset compression statistics."""
        for key in self.compression_stats:
            if isinstance(self.compression_stats[key], int):
                self.compression_stats[key] = 0
            elif isinstance(self.compression_stats[key], float):
                self.compression_stats[key] = 0.0