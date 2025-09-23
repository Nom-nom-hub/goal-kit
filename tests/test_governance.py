"""
Test cases for the governance system modules.
"""

import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from src.goal_cli.compliance import ComplianceChecker
from src.goal_cli.governance import GovernanceManager
from src.goal_cli.governance_system import GovernanceSystem
from src.goal_cli.performance import PerformanceMonitor
from src.goal_cli.quality_gates import QualityGateManager
from src.goal_cli.reviews import ReviewManager
from src.goal_cli.security import SecurityManager
from src.goal_cli.versioning import VersionManager

class TestGovernanceSystem(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = Path(tempfile.mkdtemp())
        self.test_dir.mkdir(exist_ok=True)
        
        # Create .goal directory structure
        (self.test_dir / ".goal").mkdir(exist_ok=True)
        (self.test_dir / ".goal" / "goals").mkdir(exist_ok=True)
        (self.test_dir / ".goal" / "templates").mkdir(exist_ok=True)
        
        # Create a simple goal template
        goal_template = {
            "id": "",
            "title": "",
            "description": "",
            "objectives": [],
            "success_criteria": [],
            "dependencies": [],
            "related_goals": [],
            "priority": "medium",
            "status": "draft",
            "created_at": "",
            "updated_at": "",
            "owner": "",
            "tags": [],
            "metadata": {}
        }
        
        with open(self.test_dir / ".goal" / "templates" / "goal-template.yaml", 'w') as f:
            yaml.dump(goal_template, f)
    
    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_governance_manager_initialization(self):
        """Test that GovernanceManager initializes correctly."""
        manager = GovernanceManager(self.test_dir)
        self.assertIsNotNone(manager)
        self.assertEqual(manager.project_path, self.test_dir)
    
    def test_governance_manager_validate_goal(self):
        """Test that GovernanceManager can validate goals."""
        manager = GovernanceManager(self.test_dir)
        
        # Test a valid goal
        valid_goal = {
            "title": "Test Goal",
            "description": "This is a test goal with sufficient detail to pass validation",
            "objectives": ["Objective 1", "Objective 2"],
            "success_criteria": ["Criterion 1", "Criterion 2"],
            "priority": "medium",
            "status": "draft"
        }
        
        result = manager.validate_goal(valid_goal)
        self.assertTrue(isinstance(result, dict))
        self.assertIn("valid", result)
        self.assertIn("violations", result)
        self.assertIn("warnings", result)
    
    def test_compliance_checker_initialization(self):
        """Test that ComplianceChecker initializes correctly."""
        checker = ComplianceChecker(self.test_dir)
        self.assertIsNotNone(checker)
        self.assertEqual(checker.project_path, self.test_dir)
    
    def test_quality_gate_manager_initialization(self):
        """Test that QualityGateManager initializes correctly."""
        manager = QualityGateManager(self.test_dir)
        self.assertIsNotNone(manager)
        self.assertEqual(manager.project_path, self.test_dir)
    
    def test_security_manager_initialization(self):
        """Test that SecurityManager initializes correctly."""
        manager = SecurityManager(self.test_dir)
        self.assertIsNotNone(manager)
        self.assertEqual(manager.project_path, self.test_dir)
    
    def test_performance_monitor_initialization(self):
        """Test that PerformanceMonitor initializes correctly."""
        monitor = PerformanceMonitor(self.test_dir)
        self.assertIsNotNone(monitor)
        self.assertEqual(monitor.project_path, self.test_dir)
    
    def test_review_manager_initialization(self):
        """Test that ReviewManager initializes correctly."""
        manager = ReviewManager(self.test_dir)
        self.assertIsNotNone(manager)
        self.assertEqual(manager.project_path, self.test_dir)
    
    def test_version_manager_initialization(self):
        """Test that VersionManager initializes correctly."""
        manager = VersionManager(self.test_dir)
        self.assertIsNotNone(manager)
        self.assertEqual(manager.project_path, self.test_dir)
    
    def test_governance_system_initialization(self):
        """Test that GovernanceSystem initializes correctly."""
        system = GovernanceSystem(self.test_dir)
        self.assertIsNotNone(system)
        self.assertEqual(system.project_path, self.test_dir)

if __name__ == '__main__':
    unittest.main()