#!/usr/bin/env python3
"""
Test suite for /goalkit.plan command template validation.
"""

import unittest
from pathlib import Path


class TestPlanCommandTemplate(unittest.TestCase):
    """Test cases for /goalkit.plan command template."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.template_path = Path("templates/commands/plan.md")
        self.readme_path = Path("README.md")
        self.examples_path = Path("examples.md")
        
    def test_plan_template_exists(self):
        """Test that the plan command template exists."""
        self.assertTrue(self.template_path.exists(), 
                       "Plan command template file should exist")
    
    def test_plan_template_content(self):
        """Test that the plan template has expected content."""
        content = self.template_path.read_text(encoding='utf-8')
        
        # Check for required sections
        required_sections = [
            "# /goalkit.plan Command",
            "## Overview",
            "## Purpose", 
            "## When to Use",
            "## Input Format",
            "## Output",
            "## Planning Components"
        ]
        
        for section in required_sections:
            with self.subTest(section=section):
                self.assertIn(section, content, 
                             f"Template should contain section: {section}")
    
    def test_plan_template_format(self):
        """Test that the plan template follows proper format."""
        content = self.template_path.read_text(encoding='utf-8')
        
        # Check for required format elements
        self.assertIn("/goalkit.plan", content, 
                     "Template should contain the command reference")
        self.assertIn("```", content, 
                     "Template should contain code examples")
        self.assertIn("Example", content, 
                     "Template should contain examples")
    
    def test_plan_input_format_example(self):
        """Test that the input format example is present."""
        content = self.template_path.read_text(encoding='utf-8')
        
        # Look for the example input format
        self.assertIn("Create detailed execution plan", content,
                     "Template should contain example execution plan approach")
        self.assertIn("resource allocation", content,
                     "Template should mention resource allocation")
        self.assertIn("timeline", content,
                     "Template should mention timeline")
    
    def test_plan_components(self):
        """Test that all planning components are present."""
        content = self.template_path.read_text(encoding='utf-8')
        
        components = [
            "Execution Phases",
            "Resource Planning", 
            "Timeline Management",
            "Progress Tracking"
        ]
        
        for component in components:
            with self.subTest(component=component):
                self.assertIn(component, content,
                             f"Template should contain component: {component}")
    
    def test_plan_has_proper_yaml_like_structure_in_readme(self):
        """Test that the plan command information is properly documented in README."""
        readme_content = self.readme_path.read_text(encoding='utf-8')
        
        # Check that the README contains the detailed plan command format
        required_elements = [
            "Goal:",
            "Selected Strategy:",
            "Execution Phases:",
            "Resource Allocation:",
            "Timeline:",
            "Success Metrics:",
            "Risk Management:"
        ]
        
        for element in required_elements:
            with self.subTest(element=element):
                self.assertIn(element, readme_content,
                             f"README.md should contain element: {element}")

    def test_plan_examples_in_examples_file(self):
        """Test that plan command examples exist in examples.md."""
        examples_content = self.examples_path.read_text(encoding='utf-8')
        
        self.assertIn("/goalkit.plan", examples_content,
                     "Examples.md should contain /goalkit.plan command")
        self.assertIn("Execution Phases:", examples_content,
                     "Examples.md should contain Execution Phases element")
        self.assertIn("Resource Allocation:", examples_content,
                     "Examples.md should contain Resource Allocation element")


if __name__ == '__main__':
    unittest.main()