"""
Specification processing module for the goal-dev-spec system.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from jsonschema import validate, ValidationError

class SpecManager:
    """Manages feature specifications and their validation."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.specs_path = project_path / ".goal" / "specs"
        self.specs_path.mkdir(exist_ok=True)
        
        # Load schema for validation
        schema_path = project_path / ".goal" / "templates" / "spec-schema.json"
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                self.spec_schema = json.load(f)
        else:
            self.spec_schema = None
    
    def create_spec(self, goal_id: str, title: str, description: str) -> str:
        """Create a new feature specification and return its ID."""
        # Validate inputs
        if not goal_id or not goal_id.strip():
            raise ValueError("Goal ID cannot be empty")
            
        if not title or not title.strip():
            raise ValueError("Specification title cannot be empty")
            
        if not description or not description.strip():
            raise ValueError("Specification description cannot be empty")
        
        # Generate spec ID (simple approach for now)
        import uuid
        spec_id = str(uuid.uuid4())[:8]
        
        # Create spec directory
        spec_dir = self.specs_path / spec_id
        try:
            spec_dir.mkdir(exist_ok=True)
        except Exception as e:
            raise ValueError(f"Failed to create specification directory: {e}")
        
        # Create feature specification
        spec = {
            "id": spec_id,
            "goal_id": goal_id.strip(),
            "title": title.strip(),
            "description": description.strip(),
            "user_stories": [],
            "acceptance_criteria": [],
            "functional_requirements": [],
            "non_functional_requirements": [],
            "constraints": [],
            "assumptions": [],
            "out_of_scope": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "draft",
            "metadata": {}
        }
        
        # Validate against schema if available
        if self.spec_schema:
            try:
                validate(instance=spec, schema=self.spec_schema)
            except ValidationError as e:
                raise ValueError(f"Invalid specification: {e.message}")
        
        # Save specification
        spec_file = spec_dir / "spec.yaml"
        try:
            with open(spec_file, 'w') as f:
                yaml.dump(spec, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise ValueError(f"Failed to save specification: {e}")
        
        return spec_id
    
    def get_spec(self, spec_id: str) -> Optional[Dict]:
        """Retrieve a specification by ID."""
        if not spec_id:
            return None
            
        spec_file = self.specs_path / spec_id / "spec.yaml"
        if not spec_file.exists():
            return None
        
        try:
            with open(spec_file, 'r') as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            raise ValueError(f"Failed to read specification: {e}")
    
    def update_spec_status(self, spec_id: str, status: str) -> bool:
        """Update the status of a specification."""
        spec = self.get_spec(spec_id)
        if not spec:
            return False
        
        valid_statuses = ["draft", "reviewed", "approved", "implemented"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}. Valid statuses: {valid_statuses}")
        
        spec["status"] = status
        spec["updated_at"] = datetime.now().isoformat()
        
        # Validate against schema if available
        if self.spec_schema:
            try:
                validate(instance=spec, schema=self.spec_schema)
            except ValidationError as e:
                raise ValueError(f"Invalid specification: {e.message}")
        
        # Save updated specification
        spec_file = self.specs_path / spec_id / "spec.yaml"
        try:
            with open(spec_file, 'w') as f:
                yaml.dump(spec, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise ValueError(f"Failed to update specification: {e}")
        
        return True

# Example usage
if __name__ == "__main__":
    # This is just for testing purposes
    manager = SpecManager(Path("."))
    print("SpecManager initialized")