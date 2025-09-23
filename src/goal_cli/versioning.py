"""
Versioning and breaking change management module for the goal-dev-spec system.
Manages semantic versioning, breaking change detection, and migration paths.
"""

import os
import yaml
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from packaging import version

class VersionManager:
    """Manages project versioning, breaking changes, and migration paths."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.version_path = project_path / ".goal" / "versioning"
        self.version_path.mkdir(exist_ok=True)
        
        # Load current version
        self.current_version = self._load_current_version()
        
        # Load version history
        self.version_history = self._load_version_history()
    
    def _load_current_version(self) -> str:
        """Load the current project version."""
        version_file = self.project_path / ".goal" / "VERSION"
        if version_file.exists():
            with open(version_file, 'r') as f:
                return f.read().strip()
        else:
            # Default to 0.1.0 for new projects
            return "0.1.0"
    
    def _load_version_history(self) -> List[Dict]:
        """Load version history."""
        history_file = self.version_path / "history.json"
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_current_version(self, version_str: str):
        """Save the current project version."""
        version_file = self.project_path / ".goal" / "VERSION"
        with open(version_file, 'w') as f:
            f.write(version_str)
        
        self.current_version = version_str
    
    def _save_version_history(self):
        """Save version history."""
        history_file = self.version_path / "history.json"
        with open(history_file, 'w') as f:
            json.dump(self.version_history, f, indent=2)
    
    def bump_version(self, bump_type: str, breaking_changes: List[str] = None, 
                     new_features: List[str] = None, bug_fixes: List[str] = None) -> str:
        """
        Bump the project version based on semantic versioning.
        
        Args:
            bump_type: One of 'major', 'minor', 'patch'
            breaking_changes: List of breaking changes (for major bumps)
            new_features: List of new features (for minor bumps)
            bug_fixes: List of bug fixes (for patch bumps)
        
        Returns:
            New version string
        """
        current = version.parse(self.current_version)
        
        if bump_type == "major":
            new_version = version.Version(f"{current.major + 1}.0.0")
        elif bump_type == "minor":
            new_version = version.Version(f"{current.major}.{current.minor + 1}.0")
        elif bump_type == "patch":
            new_version = version.Version(f"{current.major}.{current.minor}.{current.micro + 1}")
        else:
            raise ValueError("bump_type must be one of 'major', 'minor', 'patch'")
        
        new_version_str = str(new_version)
        
        # Create version record
        version_record = {
            "version": new_version_str,
            "previous_version": self.current_version,
            "bump_type": bump_type,
            "timestamp": datetime.now().isoformat(),
            "breaking_changes": breaking_changes or [],
            "new_features": new_features or [],
            "bug_fixes": bug_fixes or [],
            "changelog": self._generate_changelog_entry(breaking_changes, new_features, bug_fixes)
        }
        
        # Update current version
        self._save_current_version(new_version_str)
        
        # Add to version history
        self.version_history.append(version_record)
        self._save_version_history()
        
        return new_version_str
    
    def _generate_changelog_entry(self, breaking_changes: List[str], 
                                  new_features: List[str], bug_fixes: List[str]) -> str:
        """Generate a changelog entry."""
        changelog = ""
        
        if breaking_changes:
            changelog += "### Breaking Changes\\n"
            for change in breaking_changes:
                changelog += f"- {change}\\n"
            changelog += "\\n"
        
        if new_features:
            changelog += "### New Features\\n"
            for feature in new_features:
                changelog += f"- {feature}\\n"
            changelog += "\\n"
        
        if bug_fixes:
            changelog += "### Bug Fixes\\n"
            for fix in bug_fixes:
                changelog += f"- {fix}\\n"
            changelog += "\\n"
        
        return changelog.strip()
    
    def detect_breaking_changes(self, old_spec: Dict, new_spec: Dict) -> List[str]:
        """
        Detect potential breaking changes between two specifications.
        
        Args:
            old_spec: The old specification
            new_spec: The new specification
        
        Returns:
            List of detected breaking changes
        """
        breaking_changes = []
        
        # Check for removed required fields
        old_required = set(self._get_required_fields(old_spec))
        new_required = set(self._get_required_fields(new_spec))
        removed_required = old_required - new_required
        
        if removed_required:
            breaking_changes.append(f"Removed required fields: {', '.join(removed_required)}")
        
        # Check for changed field types
        type_changes = self._compare_field_types(old_spec, new_spec)
        if type_changes:
            breaking_changes.extend(type_changes)
        
        # Check for removed API endpoints (if applicable)
        api_changes = self._compare_api_endpoints(old_spec, new_spec)
        if api_changes:
            breaking_changes.extend(api_changes)
        
        # Check for changed data formats
        format_changes = self._compare_data_formats(old_spec, new_spec)
        if format_changes:
            breaking_changes.extend(format_changes)
        
        return breaking_changes
    
    def _get_required_fields(self, spec: Dict) -> List[str]:
        """Extract required fields from a specification."""
        required = []
        
        # This is a simplified implementation
        # In a real system, this would parse the actual schema
        if "required" in spec:
            required.extend(spec["required"])
        
        # Check nested objects
        for key, value in spec.items():
            if isinstance(value, dict):
                nested_required = self._get_required_fields(value)
                required.extend([f"{key}.{nr}" for nr in nested_required])
        
        return required
    
    def _compare_field_types(self, old_spec: Dict, new_spec: Dict) -> List[str]:
        """Compare field types between specifications."""
        changes = []
        
        # This is a simplified implementation
        # In a real system, this would do a detailed schema comparison
        old_types = self._extract_field_types(old_spec)
        new_types = self._extract_field_types(new_spec)
        
        for field, old_type in old_types.items():
            if field in new_types and new_types[field] != old_type:
                changes.append(f"Changed type of field '{field}' from '{old_type}' to '{new_types[field]}'")
        
        return changes
    
    def _extract_field_types(self, spec: Dict, prefix: str = "") -> Dict[str, str]:
        """Extract field types from a specification."""
        types = {}
        
        for key, value in spec.items():
            field_name = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict) and "type" in value:
                types[field_name] = value["type"]
                # Recursively check nested objects
                nested_types = self._extract_field_types(value, field_name)
                types.update(nested_types)
            elif isinstance(value, dict):
                # Recursively check nested objects
                nested_types = self._extract_field_types(value, field_name)
                types.update(nested_types)
            elif isinstance(value, list):
                types[field_name] = "array"
            elif isinstance(value, str):
                types[field_name] = "string"
            elif isinstance(value, int):
                types[field_name] = "integer"
            elif isinstance(value, float):
                types[field_name] = "number"
            elif isinstance(value, bool):
                types[field_name] = "boolean"
        
        return types
    
    def _compare_api_endpoints(self, old_spec: Dict, new_spec: Dict) -> List[str]:
        """Compare API endpoints between specifications."""
        # This is a placeholder implementation
        # In a real system, this would compare actual API endpoint definitions
        return []
    
    def _compare_data_formats(self, old_spec: Dict, new_spec: Dict) -> List[str]:
        """Compare data formats between specifications."""
        # This is a placeholder implementation
        # In a real system, this would compare actual data format definitions
        return []
    
    def generate_migration_guide(self, from_version: str, to_version: str, 
                                 breaking_changes: List[str]) -> str:
        """
        Generate a migration guide for breaking changes.
        
        Args:
            from_version: The version to migrate from
            to_version: The version to migrate to
            breaking_changes: List of breaking changes
        
        Returns:
            Migration guide in markdown format
        """
        guide = f"# Migration Guide: {from_version} \\u2192 {to_version}\\n\\n"
        guide += f"Generated: {datetime.now().isoformat()}\\n\\n"
        
        if not breaking_changes:
            guide += "## No Breaking Changes\\n\\n"
            guide += "This version does not contain any breaking changes. You can upgrade without modifications.\\n\\n"
            return guide
        
        guide += "## Breaking Changes\\n\\n"
        for i, change in enumerate(breaking_changes, 1):
            guide += f"{i}. {change}\\n"
        guide += "\\n"
        
        guide += "## Migration Steps\\n\\n"
        for i, change in enumerate(breaking_changes, 1):
            guide += f"### {i}. {change}\\n\\n"
            guide += "#### Impact\\n\\n"
            guide += "Describe the impact of this change on existing implementations.\\n\\n"
            guide += "#### Migration Instructions\\n\\n"
            guide += "Provide step-by-step instructions for migrating affected code.\\n\\n"
            guide += "#### Example\\n\\n"
            guide += "```code\\n"
            guide += "// Show before and after code examples\\n"
            guide += "```\\n\\n"
        
        guide += "## Testing\\n\\n"
        guide += "After migration, ensure you test the following:\\n\\n"
        guide += "- All existing functionality works as expected\\n"
        guide += "- New features work correctly\\n"
        guide += "- No regressions were introduced\\n\\n"
        
        return guide
    
    def get_version_history(self) -> List[Dict]:
        """Get the version history."""
        return self.version_history
    
    def generate_changelog(self) -> str:
        """Generate a changelog in markdown format."""
        changelog = "# Changelog\n\n"
        changelog += f"All notable changes to this project will be documented in this file.\n\n"
        
        # Add unreleased section if there are pending changes
        # (In a real implementation, this would check for pending changes)
        changelog += "## [Unreleased]\n\n"
        changelog += "### Added\n- \n\n"
        changelog += "### Changed\n- \n\n"
        changelog += "### Deprecated\n- \n\n"
        changelog += "### Removed\n- \n\n"
        changelog += "### Fixed\n- \n\n"
        changelog += "### Security\n- \n\n"
        
        # Add version history
        for record in reversed(self.version_history):
            changelog += f"## [{record['version']}] - {record['timestamp'][:10]}\n\n"
            
            if record['changelog']:
                changelog += record['changelog'] + "\n\n"
            else:
                changelog += "### Changes\n\n"
                changelog += "- No detailed changelog available\n\n"
        
        return changelog

# Example usage
if __name__ == "__main__":
    # This is just for testing purposes
    manager = VersionManager(Path("."))
    print("VersionManager initialized")