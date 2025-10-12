# Performance Optimization for Context Retrieval

This document outlines strategies to optimize the performance of AI context retrieval in the markdown-based Goal Kit system.

## Performance Challenges

When dealing with a markdown-based context system, potential performance challenges include:

1. **File I/O overhead**: Reading multiple markdown files for context retrieval
2. **Parsing complexity**: Processing markdown content to extract structured data
3. **Large file sizes**: Goal files with extensive content taking longer to process
4. **Directory traversal**: Scanning through many goal files to find relevant ones
5. **Regex inefficiency**: Suboptimal patterns for extracting information from markdown

## Optimization Strategies

### 1. Selective Context Loading

Rather than loading all goal files, only load context for active or relevant goals:

```python
def load_context(self, goal_filter: Optional[Callable] = None) -> Dict:
    """Load context with optional filtering for active goals only"""
    # Load context summary first
    context = {"summary": self._load_context_summary()}
    
    # Apply filter to determine which goals to load
    goal_paths = self._get_goal_paths()
    active_goal_paths = [
        path for path in goal_paths 
        if not goal_filter or goal_filter(path)
    ]
    
    # Load only active goals
    context["goals"] = [
        self._parse_goal_file(path) for path in active_goal_paths
    ]
    
    return context

def _get_active_goal_paths(self) -> List[str]:
    """Get paths for only active goals, as defined in context summary"""
    summary = self._load_context_summary()
    if not summary or 'active_goals' not in summary:
        return self._get_all_goal_paths()
    
    active_paths = []
    for goal_ref in summary['active_goals']:
        if len(goal_ref) >= 2:  # Second element is the path
            full_path = os.path.join(self.project_root, goal_ref[1])
            if os.path.exists(full_path):
                active_paths.append(full_path)
    
    return active_paths
```

### 2. Caching Mechanism

Implement a caching layer to store parsed context and avoid re-parsing:

```python
import hashlib
from functools import wraps

class ContextCache:
    def __init__(self, ttl_seconds=30):
        self.cache = {}
        self.ttl = ttl_seconds
    
    def _get_cache_key(self, project_root, file_paths):
        """Generate a cache key based on file modification times"""
        mtime_hash = hashlib.md5()
        for path in sorted(file_paths):
            if os.path.exists(path):
                mtime = os.path.getmtime(path)
                mtime_hash.update(f"{path}:{mtime}".encode())
        return mtime_hash.hexdigest()
    
    def get(self, project_root, file_paths):
        """Get cached data if still valid"""
        cache_key = self._get_cache_key(project_root, file_paths)
        cached = self.cache.get(cache_key)
        
        if cached:
            data, timestamp = cached
            if time.time() - timestamp < self.ttl:
                return data
        
        return None
    
    def set(self, project_root, file_paths, data):
        """Set data in cache"""
        cache_key = self._get_cache_key(project_root, file_paths)
        self.cache[cache_key] = (data, time.time())

# Use the cache in ContextLoader
class OptimizedContextLoader(ContextLoader):
    def __init__(self, project_root: str):
        super().__init__(project_root)
        self.cache = ContextCache()
    
    def load_context(self) -> Dict:
        """Load context with caching"""
        # Get all relevant file paths
        file_paths = self._get_relevant_file_paths()
        
        # Check cache first
        cached_context = self.cache.get(self.project_root, file_paths)
        if cached_context:
            return cached_context
        
        # Load fresh context
        context = super().load_context()
        
        # Store in cache
        self.cache.set(self.project_root, file_paths, context)
        
        return context
```

### 3. Incremental Context Updates

Instead of reloading everything, update only changed components:

```python
class IncrementalContextLoader(OptimizedContextLoader):
    def __init__(self, project_root: str):
        super().__init__(project_root)
        self.file_timestamps = {}
    
    def load_context(self, force_full_reload=False) -> Dict:
        """Load context with incremental updates"""
        if force_full_reload or not hasattr(self, '_cached_context'):
            self._cached_context = super().load_context()
            self._update_file_timestamps()
            return self._cached_context
        
        # Check for changed files
        changed_files = self._get_changed_files()
        if not changed_files:
            return self._cached_context
        
        # Update only changed components
        for file_path in changed_files:
            if 'ai-context.md' in file_path:
                self._cached_context['summary'] = self._load_context_summary()
            elif '/goals/' in file_path:
                self._update_goal_in_context(file_path)
        
        self._update_file_timestamps()
        return self._cached_context
    
    def _get_changed_files(self) -> List[str]:
        """Get list of files that have changed since last check"""
        changed = []
        current_timestamps = {}
        
        # Check all relevant files
        for file_path in self._get_relevant_file_paths():
            if os.path.exists(file_path):
                current_mtime = os.path.getmtime(file_path)
                current_timestamps[file_path] = current_mtime
                
                if (file_path not in self.file_timestamps or 
                    current_mtime > self.file_timestamps[file_path]):
                    changed.append(file_path)
        
        self.file_timestamps = current_timestamps
        return changed
    
    def _update_goal_in_context(self, goal_file_path: str):
        """Update a single goal in the cached context"""
        goal_data = self._parse_goal_file(goal_file_path)
        
        # Find and replace the goal in cached context
        for i, goal in enumerate(self._cached_context['goals']):
            if goal['path'] == goal_file_path:
                self._cached_context['goals'][i] = goal_data
                break
        else:
            # Goal not found, add it (shouldn't happen in normal operation)
            self._cached_context['goals'].append(goal_data)
```

### 4. Optimized Parsing

Optimize the markdown parsing by focusing on relevant sections:

```python
class OptimizedParsingLoader(ContextLoader):
    def _parse_goal_file(self, goal_path: str) -> Dict:
        """Optimized goal file parsing focusing on key sections"""
        with open(goal_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Use compiled regex patterns for better performance
        if not hasattr(self, '_compiled_patterns'):
            self._compiled_patterns = {
                'title': re.compile(r'^# Goal: (.+)', re.MULTILINE),
                'statement': re.compile(r'\*\*Goal Statement\*\*:\s*(.*?)(?=\n\n|\n\*\*)', re.DOTALL),
                'created': re.compile(r'\*\*Created\*\*:\s*(\d{4}-\d{2}-\d{2})'),
                'branch': re.compile(r'\*\*Goal Branch\*\*:\s*([^\n]+)'),
                'status': re.compile(r'\*\*Status\*\*:\s*([^\n]+)'),
                'active_strategy': re.compile(r'\*\*Active Strategy\*\*:\s*([^\n]+)'),
                'current_milestone': re.compile(r'\*\*Current Milestone\*\*:\s*([^\n]+)'),
            }
        
        # Extract only the needed information
        goal_data = {
            'path': goal_path,
            'goal_title': self._safe_extract(content, 'title'),
            'goal_statement': self._safe_extract(content, 'statement'),
            'created': self._safe_extract(content, 'created'),
            'goal_branch': self._safe_extract(content, 'branch'),
            'status': self._safe_extract(content, 'status'),
            'active_strategy': self._safe_extract(content, 'active_strategy'),
            'current_milestone': self._safe_extract(content, 'current_milestone'),
        }
        
        return goal_data

    def _safe_extract(self, content: str, pattern_name: str) -> Optional[str]:
        """Safely extract using compiled pattern"""
        try:
            pattern = self._compiled_patterns.get(pattern_name)
            if pattern:
                match = pattern.search(content)
                return match.group(1).strip() if match else None
        except Exception:
            # Return None if extraction fails
            return None
        
        return None
```

### 5. Parallel Processing

Use parallel processing for independent file operations:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class ParallelContextLoader(OptimizedParsingLoader):
    def __init__(self, project_root: str, max_workers: int = 4):
        super().__init__(project_root)
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def _load_active_goals(self) -> List[Dict]:
        """Load active goals using parallel processing"""
        goal_paths = self._get_active_goal_paths()
        
        # Process goals in parallel
        goals = []
        with self.executor as executor:
            # Submit all tasks
            future_to_path = {
                executor.submit(self._parse_goal_file, path): path 
                for path in goal_paths
            }
            
            # Collect results
            for future in as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    goal_data = future.result()
                    goals.append(goal_data)
                except Exception as e:
                    print(f"Error processing goal {path}: {e}")
        
        return goals
```

### 6. Indexing for Fast Lookup

Create an index for fast lookup of goals and context:

```python
import json

class IndexedContextLoader(ParallelContextLoader):
    def __init__(self, project_root: str):
        super().__init__(project_root)
        self.index_path = os.path.join(project_root, '.goalkit', 'context-index.json')
        self.index = self._load_index()
    
    def _load_index(self) -> Dict:
        """Load the context index file"""
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass  # If index is corrupted, start fresh
        
        return {"last_updated": 0, "goals": {}, "metadata": {}}
    
    def _save_index(self):
        """Save the context index file"""
        try:
            os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
            with open(self.index_path, 'w') as f:
                json.dump(self.index, f)
        except Exception as e:
            print(f"Error saving index: {e}")
    
    def _update_index(self):
        """Update the context index if needed"""
        project_mtime = os.path.getmtime(self.project_root)
        
        if project_mtime > self.index["last_updated"]:
            # Rebuild index
            goals_dir = os.path.join(self.project_root, ".goalkit", "goals")
            if os.path.exists(goals_dir):
                for goal_dir in os.listdir(goals_dir):
                    goal_path = os.path.join(goals_dir, goal_dir, "goal.md")
                    if os.path.exists(goal_path):
                        mtime = os.path.getmtime(goal_path)
                        self.index["goals"][goal_dir] = {
                            "path": goal_path,
                            "mtime": mtime
                        }
            
            self.index["last_updated"] = project_mtime
            self._save_index()
    
    def load_context(self) -> Dict:
        """Load context using the index for optimization"""
        self._update_index()
        
        # Only process goals that have changed since last index update
        context = {"summary": self._load_context_summary(), "goals": []}
        
        for goal_id, goal_info in self.index["goals"].items():
            goal_path = goal_info["path"]
            if os.path.exists(goal_path):
                # Only reload if file is newer than index timestamp
                if os.path.getmtime(goal_path) > self.index["last_updated"]:
                    goal_data = self._parse_goal_file(goal_path)
                else:
                    # Use simplified data from index
                    goal_data = {
                        "path": goal_path,
                        "goal_branch": goal_id,
                        "title_from_index": goal_info.get("title", "Unknown")
                    }
                
                context["goals"].append(goal_data)
        
        return context
```

## Performance Testing

To measure the effectiveness of optimizations:

```python
import time

def performance_test():
    """Test the performance of context loading"""
    project_path = "/path/to/test/project"
    
    # Test basic loader
    start_time = time.time()
    basic_loader = ContextLoader(project_path)
    basic_context = basic_loader.load_context()
    basic_time = time.time() - start_time
    
    # Test optimized loader
    start_time = time.time()
    opt_loader = IndexedContextLoader(project_path)
    opt_context = opt_loader.load_context()
    opt_time = time.time() - start_time
    
    print(f"Basic loader time: {basic_time:.2f}s")
    print(f"Optimized loader time: {opt_time:.2f}s")
    print(f"Improvement: {((basic_time - opt_time) / basic_time * 100):.1f}%")
    
    return basic_time, opt_time
```

## Configuration Options

Provide configuration options to tune performance based on project size:

```python
class ConfigurableContextLoader(IndexedContextLoader):
    def __init__(self, project_root: str, config: Dict = None):
        super().__init__(project_root)
        
        # Apply configuration
        self.config = config or {}
        self.max_workers = self.config.get('max_workers', 4)
        self.cache_ttl = self.config.get('cache_ttl', 30)
        self.use_index = self.config.get('use_index', True)
        
        # Reinitialize with config
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.cache = ContextCache(ttl_seconds=self.cache_ttl)
```