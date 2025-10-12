# Implementation Guide: Context Retrieval in Goal Kit

This document outlines the practical implementation of the context retrieval system using markdown files, focusing on how an AI agent would actually load and use context when starting a new session.

## Core Components

### 1. Context Loader Module

The Context Loader is responsible for reading and parsing all context-related markdown files:

```python
# context_loader.py
import os
import re
import glob
from datetime import datetime
from typing import Dict, List, Optional

class ContextLoader:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.context_summary = None
        self.active_goals = []
        self.interaction_logs = []

    def load_context(self) -> Dict:
        """Load all project context and return as a structured dictionary"""
        
        # Load context summary
        self.context_summary = self._load_context_summary()
        
        # Load active goals
        self.active_goals = self._load_active_goals()
        
        # Load recent interaction logs
        self.interaction_logs = self._load_recent_interaction_logs()
        
        # Combine all into a unified context
        return self._build_unified_context()

    def _load_context_summary(self) -> Optional[Dict]:
        """Load the ai-context.md file if it exists"""
        context_file = os.path.join(self.project_root, "ai-context.md")
        
        if not os.path.exists(context_file):
            return None
            
        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract sections using regex
        context_data = {
            'date': self._extract_value(content, r'\*\*Date\*\*:\s*(\d{4}-\d{2}-\d{2})'),
            'active_goals': self._extract_list(content, r'## Active Goals', r'\- \[([^\]]+)\]\(([^)]+)\)(?: - ([^\n]+))?'),
            'active_strategies': self._extract_list(content, r'## Active Strategies', r'\- \*\*Goal ([^\*]+)\*\*: (.+)'),
            'current_milestones': self._extract_list(content, r'## Current Milestones', r'\- (\d+): ([^(]+) \(due (\d{4}-\d{2}-\d{2})\)'),
            'key_information': self._extract_section(content, r'## Key Information', r'## \w+'),
            'recent_decisions': self._extract_list(content, r'## Recent Decisions', r'\d+\. (.+)')
        }
        
        return context_data

    def _load_active_goals(self) -> List[Dict]:
        """Load active goal files based on context summary"""
        active_goals = []
        
        if self.context_summary and 'active_goals' in self.context_summary:
            for goal_ref in self.context_summary['active_goals']:
                if len(goal_ref) >= 2:
                    goal_path = os.path.join(self.project_root, goal_ref[1])  # Second element is the path
                    
                    if os.path.exists(goal_path):
                        goal_data = self._parse_goal_file(goal_path)
                        active_goals.append(goal_data)
        
        return active_goals

    def _parse_goal_file(self, goal_path: str) -> Dict:
        """Parse a goal markdown file to extract relevant information"""
        with open(goal_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract goal information
        goal_data = {
            'path': goal_path,
            'goal_title': self._extract_value(content, r'^# Goal: (.+)', multiline=True),
            'goal_statement': self._extract_value(content, r'\*\*Goal Statement\*\*:\s*(.*?)(?=\n\n|\n\*\*)', multiline=True),
            'created': self._extract_value(content, r'\*\*Created\*\*:\s*(\d{4}-\d{2}-\d{2})'),
            'goal_branch': self._extract_value(content, r'\*\*Goal Branch\*\*:\s*([^\n]+)'),
            'status': self._extract_value(content, r'\*\*Status\*\*:\s*([^\n]+)'),
            'active_strategy': self._extract_value(content, r'\*\*Active Strategy\*\*:\s*([^\n]+)'),
            'current_milestone': self._extract_value(content, r'\*\*Current Milestone\*\*:\s*([^\n]+)'),
        }
        
        # Extract success metrics
        metrics_section = self._extract_section(content, r'## 2\. Success Metrics', r'## \d+\.')
        goal_data['primary_metrics'] = self._extract_list(metrics_section, r'### Primary Metrics', r'\- (.+)')
        goal_data['secondary_metrics'] = self._extract_list(metrics_section, r'### Secondary Metrics', r'\- (.+)')
        
        # Extract milestones
        milestones_section = self._extract_section(content, r'## 5\. Goal Milestones', r'## \d+\.')
        goal_data['milestones'] = self._extract_list(milestones_section, r'### Milestone \d+:', r'### Milestone \d+: ([^\n]+)')
        
        return goal_data

    def _load_recent_interaction_logs(self) -> List[Dict]:
        """Load recent AI interaction log files"""
        log_pattern = os.path.join(self.project_root, ".goalkit", "logs", "ai-interaction-*.md")
        log_files = glob.glob(log_pattern)
        
        # Sort by modification time, most recent first
        log_files.sort(key=os.path.getmtime, reverse=True)
        
        interaction_logs = []
        for log_file in log_files[:5]:  # Load only 5 most recent logs
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                log_data = {
                    'file_path': log_file,
                    'date': self._extract_value(content, r'\*\*Date\*\*:\s*(\d{4}-\d{2}-\d{2})'),
                    'participants': self._extract_value(content, r'\*\*Participants\*\*:\s*(.+)'),
                    'summary': self._extract_value(content, r'## Summary\n(.+?)(?=\n## |\n$)', multiline=True),
                    'decisions': self._extract_list(content, r'## Decisions Made', r'\d+\. (.+)')
                }
                
                interaction_logs.append(log_data)
            except Exception as e:
                print(f"Error reading interaction log {log_file}: {e}")
        
        return interaction_logs

    def _build_unified_context(self) -> Dict:
        """Combine all loaded context into a unified structure"""
        return {
            'summary': self.context_summary,
            'goals': self.active_goals,
            'interactions': self.interaction_logs,
            'last_updated': datetime.now().isoformat()
        }

    def _extract_value(self, text: str, pattern: str, multiline: bool = False) -> Optional[str]:
        """Extract a single value using regex"""
        flags = re.MULTILINE | re.DOTALL if multiline else 0
        match = re.search(pattern, text, flags)
        return match.group(1).strip() if match else None

    def _extract_list(self, text: str, section_pattern: str, item_pattern: str) -> List:
        """Extract a list of items from a section"""
        # Find the section first
        section_match = re.search(section_pattern, text, re.MULTILINE)
        if not section_match:
            return []
        
        # Find the start of the section
        start_pos = section_match.end()
        
        # Find the end of the section (next heading or end of text)
        next_heading = re.search(r'\n##\s', text[start_pos:])
        end_pos = start_pos + next_heading.start() if next_heading else len(text)
        
        section_text = text[start_pos:end_pos]
        
        # Find all items in the section
        items = []
        for match in re.finditer(item_pattern, section_text, re.MULTILINE):
            if match.groups():
                # If the pattern has groups, take all groups
                item_groups = [g.strip() for g in match.groups() if g.strip()]
                items.append(item_groups[0] if len(item_groups) == 1 else item_groups)
            else:
                # If no groups, take the full match
                items.append(match.group().strip())
        
        return items

    def _extract_section(self, text: str, start_pattern: str, end_pattern: str) -> str:
        """Extract an entire section between two patterns"""
        start_match = re.search(start_pattern, text, re.MULTILINE)
        if not start_match:
            return ""
        
        start_pos = start_match.end()
        end_match = re.search(end_pattern, text[start_pos:], re.MULTILINE)
        
        if end_match:
            end_pos = start_pos + end_match.start()
            return text[start_pos:end_pos].strip()
        else:
            return text[start_pos:].strip()

# Usage example
if __name__ == "__main__":
    loader = ContextLoader("/path/to/project")
    context = loader.load_context()
    print(f"Loaded context with {len(context['goals'])} active goals")
```

### 2. Context Retrieval Service

A service that coordinates the loading and makes context available to AI agents:

```python
# context_retrieval_service.py
from context_loader import ContextLoader
from typing import Dict, Any
import json

class ContextRetrievalService:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.context_cache = {}
        self.loader = ContextLoader(project_root)

    def get_context(self, force_reload: bool = False) -> Dict[str, Any]:
        """Get the current project context, using cache if available"""
        
        cache_key = self._get_cache_key()
        
        if not force_reload and cache_key in self.context_cache:
            # Check if cache is still valid
            if not self._is_cache_expired(cache_key):
                return self.context_cache[cache_key]
        
        # Load fresh context
        context = self.loader.load_context()
        
        # Store in cache
        self.context_cache[cache_key] = context
        
        return context

    def _get_cache_key(self) -> str:
        """Generate a cache key based on project directory modification time"""
        import os
        mtime = os.path.getmtime(self.project_root)
        return f"{self.project_root}_{mtime}"

    def _is_cache_expired(self, cache_key: str) -> bool:
        """Check if cache entry is expired"""
        import time
        
        # For simplicity, expire cache after 30 seconds
        # In a real implementation, you'd check file modification times
        return time.time() - self.context_cache.get(cache_key + '_timestamp', 0) > 30

    def get_goal_context(self, goal_id: str) -> Dict[str, Any]:
        """Get context specifically for a given goal"""
        context = self.get_context()
        
        # Find the goal in loaded goals
        for goal in context.get('goals', []):
            if goal.get('goal_branch') == goal_id or goal.get('path', '').endswith(goal_id):
                return goal
        
        return {}

    def get_project_summary(self) -> Dict[str, Any]:
        """Get a high-level summary of the project context"""
        context = self.get_context()
        
        summary = context.get('summary', {})
        goals = context.get('goals', [])
        
        return {
            'project_name': self._extract_project_name(summary),
            'active_goals_count': len(goals),
            'active_goals': [g.get('goal_title', 'Unknown') for g in goals],
            'recent_interactions': len(context.get('interactions', [])),
            'last_updated': context.get('last_updated', 'Unknown')
        }

    def _extract_project_name(self, summary: Dict) -> str:
        """Extract project name from context summary"""
        if summary and 'key_information' in summary:
            key_info = summary['key_information']
            project_match = re.search(r'\*\*Project\*\*:\s*([^\n]+)', key_info)
            if project_match:
                return project_match.group(1).strip()
        
        return 'Unknown Project'
```

### 3. Integration with AI Agent

How the context retrieval system would integrate with an AI agent:

```python
# ai_agent_integration.py
from context_retrieval_service import ContextRetrievalService
import os

class AIAgent:
    def __init__(self, project_path: str):
        self.context_service = ContextRetrievalService(project_path)
        self.current_context = None

    def start_session(self):
        """Called when starting a new AI session"""
        print("Loading project context...")
        self.current_context = self.context_service.get_context()
        print("Context loaded successfully!")
        
        # Optionally display project summary to user
        summary = self.context_service.get_project_summary()
        print(f"Active project: {summary['project_name']}")
        print(f"Active goals: {summary['active_goals_count']}")
        print("Context is now available for this session.")

    def get_context_for_query(self, user_query: str) -> str:
        """Get relevant context for a specific user query"""
        if not self.current_context:
            self.start_session()
        
        # Simple approach: return overall project summary
        # In a more advanced implementation, this would use semantic search
        # to find the most relevant context for the query
        summary = self.context_service.get_project_summary()
        
        context_str = f"""
Project Context:
- Project: {summary['project_name']}
- Active Goals: {', '.join(summary['active_goals'])}
- Active Goals Count: {summary['active_goals_count']}
- Recent Interactions: {summary['recent_interactions']} conversations
- Last Updated: {summary['last_updated']}
        """.strip()
        
        return context_str

# Usage
if __name__ == "__main__":
    agent = AIAgent("/path/to/project")
    agent.start_session()
    
    user_query = "How is the onboarding improvement goal progressing?"
    context = agent.get_context_for_query(user_query)
    print("Context provided to AI for query:")
    print(context)
```

## Implementation Process

When an AI agent starts a new session:

1. **Initialize ContextRetrievalService** with the project path
2. **Load context** by calling `get_context()` which reads markdown files
3. **Cache context** for performance during the session
4. **Make context available** to the AI for generating relevant responses
5. **Update cache** when files change during the session

## Performance Considerations

- **Selective loading**: Only load active goals rather than all goals in the project
- **Efficient parsing**: Use regex-based parsing for speed rather than full markdown parsing
- **Caching**: Cache loaded context with expiration based on file modification times
- **Incremental updates**: Re-load only files that have changed since last cache