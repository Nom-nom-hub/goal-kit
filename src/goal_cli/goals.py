"""
Goal management module for the goal-dev-spec system.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from jsonschema import validate, ValidationError

class GoalManager:
    """Manages goals, their dependencies, and tracking."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.goals_path = project_path / ".goal" / "goals"
        self.goals_path.mkdir(exist_ok=True)
        
        # Load schema for validation
        schema_path = project_path / ".goal" / "templates" / "goal-schema.json"
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                self.goal_schema = json.load(f)
        else:
            self.goal_schema = None
    
    def create_goal_from_data(self, goal_data: Dict) -> str:
        """Create a new goal from provided data."""
        # Validate inputs
        if not goal_data.get('title') or not goal_data['title'].strip():
            raise ValueError("Goal title cannot be empty")
        
        if not goal_data.get('description') or not goal_data['description'].strip():
            raise ValueError("Goal description cannot be empty")
        
        # Generate goal ID (simple approach for now)
        import uuid
        goal_id = str(uuid.uuid4())[:8]
        
        # Create goal directory
        goal_dir = self.goals_path / goal_id
        try:
            goal_dir.mkdir(exist_ok=True)
        except Exception as e:
            raise ValueError(f"Failed to create goal directory: {e}")
        
        # Add required fields if missing
        goal_spec = goal_data.copy()
        goal_spec["id"] = goal_id
        goal_spec.setdefault("created_at", datetime.now().isoformat())
        goal_spec.setdefault("updated_at", datetime.now().isoformat())
        
        # Validate against schema if available
        if self.goal_schema:
            try:
                from jsonschema import validate, ValidationError
                validate(instance=goal_spec, schema=self.goal_schema)
            except ValidationError as e:
                raise ValueError(f"Invalid goal specification: {e.message}")
        
        # Save goal specification
        goal_file = goal_dir / "goal.yaml"
        try:
            with open(goal_file, 'w') as f:
                yaml.dump(goal_spec, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise ValueError(f"Failed to save goal specification: {e}")
        
        # Create goals index if it doesn't exist
        goals_index = self.goals_path / "goals.yaml"
        if not goals_index.exists():
            try:
                with open(goals_index, 'w') as f:
                    yaml.dump({"goals": []}, f)
            except Exception as e:
                raise ValueError(f"Failed to create goals index: {e}")
        
        # Add to goals index
        try:
            with open(goals_index, 'r') as f:
                index = yaml.load(f, Loader=yaml.FullLoader)
            
            if index is None:
                index = {"goals": []}
            elif "goals" not in index:
                index["goals"] = []
            
            index["goals"].append({
                "id": goal_id,
                "title": goal_spec["title"],
                "created_at": goal_spec["created_at"]
            })
            
            with open(goals_index, 'w') as f:
                yaml.dump(index, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise ValueError(f"Failed to update goals index: {e}")
        
        return goal_id
    
    def get_goal(self, goal_id: str) -> Optional[Dict]:
        """Retrieve a goal by ID."""
        if not goal_id:
            return None
            
        goal_file = self.goals_path / goal_id / "goal.yaml"
        if not goal_file.exists():
            return None
        
        try:
            with open(goal_file, 'r') as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            raise ValueError(f"Failed to read goal specification: {e}")
    
    def list_goals(self) -> List[Dict]:
        """List all goals in the project."""
        goals_index = self.goals_path / "goals.yaml"
        if not goals_index.exists():
            return []
        
        try:
            with open(goals_index, 'r') as f:
                index = yaml.load(f, Loader=yaml.FullLoader)
            
            if index is None:
                return []
                
            return index.get("goals", [])
        except Exception as e:
            raise ValueError(f"Failed to read goals index: {e}")
    
    def update_goal_status(self, goal_id: str, status: str) -> bool:
        """Update the status of a goal."""
        goal = self.get_goal(goal_id)
        if not goal:
            return False
        
        valid_statuses = ["draft", "planned", "in_progress", "completed", "blocked"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}. Valid statuses: {valid_statuses}")
        
        goal["status"] = status
        goal["updated_at"] = datetime.now().isoformat()
        
        # Validate against schema if available
        if self.goal_schema:
            try:
                validate(instance=goal, schema=self.goal_schema)
            except ValidationError as e:
                raise ValueError(f"Invalid goal specification: {e.message}")
        
        # Save updated goal
        goal_file = self.goals_path / goal_id / "goal.yaml"
        try:
            with open(goal_file, 'w') as f:
                yaml.dump(goal, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise ValueError(f"Failed to update goal specification: {e}")
        
        return True
    
    def add_dependency(self, goal_id: str, dependency_id: str) -> bool:
        """Add a dependency to a goal."""
        goal = self.get_goal(goal_id)
        if not goal:
            return False
        
        if dependency_id not in goal["dependencies"]:
            goal["dependencies"].append(dependency_id)
            goal["updated_at"] = datetime.now().isoformat()
            
            # Save updated goal
            goal_file = self.goals_path / goal_id / "goal.yaml"
            try:
                with open(goal_file, 'w') as f:
                    yaml.dump(goal, f, default_flow_style=False, sort_keys=False)
            except Exception as e:
                raise ValueError(f"Failed to update goal dependencies: {e}")
        
        return True

# Example usage
if __name__ == "__main__":
    # This is just for testing purposes
    manager = GoalManager(Path("."))
    print("GoalManager initialized")