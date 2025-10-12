#!/usr/bin/env python3
"""
Test suite for /goalkit.execute command template validation.
"""

import unittest
import os
from pathlib import Path
import re


class TestExecuteCommandTemplate(unittest.TestCase):
    """Test cases for /goalkit.execute command template."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.template_path = Path("templates/commands/execute.md")
        self.content = self.template_path.read_text()
        
    def test_execute_template_exists(self):
        """Test that the execute command template exists."""
        self.assertTrue(self.template_path.exists(), 
                       "Execute command template file should exist")
    
    def test_execute_template_content(self):
        """Test that the execute template has expected content."""
        # Check for required sections
        required_sections = [
            "# /goalkit.execute Command",
            "## Overview",
            "## Purpose", 
            "## When to Use",
            "## Input Format",
            "## Output",
            "## Execution Components"
        ]
        
        for section in required_sections:
            with self.subTest(section=section):
                self.assertIn(section, self.content, 
                             f"Template should contain section: {section}")
    
    def test_execute_template_format(self):
        """Test that the execute template follows proper format."""
        # Check for required format elements
        self.assertIn("/goalkit.execute", self.content, 
                     "Template should contain the command reference")
        self.assertIn("```", self.content, 
                     "Template should contain code examples")
        self.assertIn("Example", self.content, 
                     "Template should contain examples")
    
    def test_execute_input_format_example(self):
        """Test that the input format example is present."""
        # Look for the example input format
        self.assertIn("Implement the first milestone", self.content,
                     "Template should contain example execution approach")
        self.assertIn("daily measurement", self.content,
                     "Template should mention measurement approach")
        self.assertIn("learning from user feedback", self.content,
                     "Template should mention learning focus")
    
    def test_execute_components(self):
        """Test that all execution components are present."""
        components = [
            "Execution Strategy",
            "Measurement Framework", 
            "Learning Loop Process",
            "Adaptation Framework"
        ]
        
        for component in components:
            with self.subTest(component=component):
                self.assertIn(component, self.content,
                             f"Template should contain component: {component}")

    def test_execute_command_follows_standard_pattern(self):
        """Test that the execute command follows the standard pattern of other commands."""
        # Look for the pattern similar to other commands
        # Check for a proper structure with the expected format
        pattern = r'/goalkit\.execute\s+(.*)'
        match = re.search(pattern, self.content)
        self.assertIsNotNone(match, "Template should contain proper command format")
        
    def test_execute_has_proper_yaml_like_structure(self):
        """Test that the execute command information is properly documented in README."""
        # The specific format with these elements is documented in README.md
        readme_path = Path("README.md")
        self.assertTrue(readme_path.exists(), "README.md should exist")
        
        # Read with utf-8 encoding to handle special characters
        readme_content = readme_path.read_text(encoding='utf-8')
        
        # Check that the README contains the detailed execute command format
        required_elements = [
            "Goal:",
            "Current Milestone:",
            "Selected Strategy:",
            "Daily Focus:",
            "Success Indicator:",
            "Learning Objective:",
            "Adaptation Plan:"
        ]
        
        for element in required_elements:
            with self.subTest(element=element):
                self.assertIn(element, readme_content,
                             f"README.md should contain element: {element}")


if __name__ == '__main__':
    unittest.main()