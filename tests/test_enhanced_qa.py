"""
Test file for enhanced quality assurance modules
"""

import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any

# Import our modules
from src.goal_cli.enhanced_quality_assurance import QualityMetrics, ValidationFinding
from src.goal_cli.real_time_monitoring import MonitoringEvent, ThresholdRule
from src.goal_cli.testing_integration import TestingFrameworkIntegration


class TestEnhancedQualityAssuranceDataclasses(unittest.TestCase):
    """Test cases for EnhancedQualityAssurance dataclasses"""
    
    def test_quality_metrics_dataclass(self):
        """Test QualityMetrics dataclass"""
        metrics = QualityMetrics(
            clarity_score=0.85,
            completeness_score=0.92,
            consistency_score=0.78,
            testability_score=0.88,
            maintainability_score=0.81,
            security_score=0.95,
            overall_score=0.87
        )
        
        self.assertEqual(metrics.clarity_score, 0.85)
        self.assertEqual(metrics.overall_score, 0.87)
    
    def test_validation_finding_dataclass(self):
        """Test ValidationFinding dataclass"""
        finding = ValidationFinding(
            id="test_001",
            type="error",
            category="clarity",
            message="Test message",
            severity=3,
            location="test.location",
            suggestion="Test suggestion"
        )
        
        self.assertEqual(finding.id, "test_001")
        self.assertEqual(finding.type, "error")
        self.assertEqual(finding.severity, 3)


class TestTestingFrameworkIntegration(unittest.TestCase):
    """Test cases for TestingFrameworkIntegration class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = Path(tempfile.mkdtemp())
        # Create the required .goal directory structure
        (self.test_dir / ".goal").mkdir()
        self.testing = TestingFrameworkIntegration(self.test_dir)
    
    def tearDown(self):
        """Tear down test fixtures"""
        shutil.rmtree(self.test_dir)
    
    def test_initialization(self):
        """Test that TestingFrameworkIntegration initializes correctly"""
        self.assertIsInstance(self.testing, TestingFrameworkIntegration)
        self.assertTrue((self.test_dir / ".goal" / "testing").exists())
    
    def test_supported_frameworks(self):
        """Test that supported frameworks are defined"""
        expected_frameworks = ["pytest", "unittest", "jest", "mocha"]
        for framework in expected_frameworks:
            self.assertIn(framework, self.testing.supported_frameworks)
    
    def test_detect_testing_framework(self):
        """Test detection of testing frameworks"""
        # Initially no framework should be detected
        detected = self.testing.detect_testing_framework()
        self.assertIsNone(detected)
        
        # Create a pytest config file and test detection
        pytest_config = self.test_dir / "pytest.ini"
        pytest_config.write_text("[pytest]\n")
        
        detected = self.testing.detect_testing_framework()
        self.assertEqual(detected, "pytest")


class TestRealTimeQualityMonitorDataclasses(unittest.TestCase):
    """Test cases for RealTimeQualityMonitor dataclasses"""
    
    def test_monitoring_event_dataclass(self):
        """Test MonitoringEvent dataclass"""
        event = MonitoringEvent(
            id="event_001",
            timestamp="2023-01-01T00:00:00Z",
            event_type="quality_change",
            severity=3,
            description="Test event",
            details={"test": "data"},
            related_artifacts=["artifact_001"]
        )
        
        self.assertEqual(event.id, "event_001")
        self.assertEqual(event.event_type, "quality_change")
        self.assertEqual(event.severity, 3)
    
    def test_threshold_rule_dataclass(self):
        """Test ThresholdRule dataclass"""
        rule = ThresholdRule(
            metric="overall_score",
            operator="lt",
            threshold=0.6,
            severity=4,
            action="alert"
        )
        
        self.assertEqual(rule.metric, "overall_score")
        self.assertEqual(rule.operator, "lt")
        self.assertEqual(rule.threshold, 0.6)
        self.assertEqual(rule.severity, 4)
        self.assertEqual(rule.action, "alert")


if __name__ == "__main__":
    unittest.main()