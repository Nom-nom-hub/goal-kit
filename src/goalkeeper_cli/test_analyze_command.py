#!/usr/bin/env python3
"""
Test suite for /goalkit.analyze command template validation.
"""

import unittest
from pathlib import Path


class TestAnalyzeCommandTemplate(unittest.TestCase):
    """Test cases for /goalkit.analyze command template."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.template_path = Path("templates/commands/analyze.md")
        self.examples_path = Path("examples.md")
        
    def test_analyze_template_exists(self):
        """Test that the analyze command template exists."""
        self.assertTrue(self.template_path.exists(), 
                       "Analyze command template file should exist")
    
    def test_analyze_template_content(self):
        """Test that the analyze template has expected content."""
        content = self.template_path.read_text(encoding='utf-8')
        
        # Check for required sections
        required_sections = [
            "# /goalkit.analyze Command",
            "## Overview",
            "## Purpose", 
            "## When to Use",
            "## Input Format",
            "## Output",
            "## Analysis Components"
        ]
        
        for section in required_sections:
            with self.subTest(section=section):
                self.assertIn(section, content, 
                             f"Template should contain section: {section}")
    
    def test_analyze_template_format(self):
        """Test that the analyze template follows proper format."""
        content = self.template_path.read_text(encoding='utf-8')
        
        # Check for required format elements
        self.assertIn("/goalkit.analyze", content, 
                     "Template should contain the command reference")
        self.assertIn("```", content, 
                     "Template should contain code examples")
        self.assertIn("Example", content, 
                     "Template should contain examples")
    
    def test_analyze_input_format_example(self):
        """Test that the input format example is present."""
        content = self.template_path.read_text(encoding='utf-8')
        
        # Look for the example input format
        self.assertIn("Focus on goal completion patterns", content,
                     "Template should contain example analysis approach")
        self.assertIn("milestone velocity", content,
                     "Template should mention milestone velocity")
        self.assertIn("prioritization adjustments", content,
                     "Template should mention prioritization")
    
    def test_analyze_components(self):
        """Test that all analysis components are present."""
        content = self.template_path.read_text(encoding='utf-8')
        
        components = [
            "Project Health Assessment",
            "Pattern Recognition", 
            "Risk Analysis",
            "Recommendations Engine"
        ]
        
        for component in components:
            with self.subTest(component=component):
                self.assertIn(component, content,
                             f"Template should contain component: {component}")
    
    def test_analyze_examples_in_examples_file(self):
        """Test that analyze command examples exist in examples.md."""
        examples_content = self.examples_path.read_text(encoding='utf-8')
        
        self.assertIn("/goalkit.analyze", examples_content,
                     "Examples.md should contain /goalkit.analyze command")
        self.assertIn("Project Focus:", examples_content,
                     "Examples.md should contain Project Focus element")
        self.assertIn("Health Indicators:", examples_content,
                     "Examples.md should contain Health Indicators element")
        self.assertIn("Pattern Recognition:", examples_content,
                     "Examples.md should contain Pattern Recognition element")


if __name__ == '__main__':
    unittest.main()