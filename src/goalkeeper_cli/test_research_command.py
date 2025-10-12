#!/usr/bin/env python3
"""
Test suite for /goalkit.research command template validation.
"""

import unittest
from pathlib import Path


class TestResearchCommandTemplate(unittest.TestCase):
    """Test cases for /goalkit.research command template."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.template_path = Path("templates/commands/research.md")
        self.examples_path = Path("examples.md")
        
    def test_research_template_exists(self):
        """Test that the research command template exists."""
        self.assertTrue(self.template_path.exists(), 
                       "Research command template file should exist")
    
    def test_research_template_content(self):
        """Test that the research template has expected content."""
        content = self.template_path.read_text(encoding='utf-8')
        
        # Check for required sections
        required_sections = [
            "# /goalkit.research Command",
            "## Overview",
            "## Purpose", 
            "## When to Use",
            "## Input Format",
            "## Output",
            "## Research Components"
        ]
        
        for section in required_sections:
            with self.subTest(section=section):
                self.assertIn(section, content, 
                             f"Template should contain section: {section}")
    
    def test_research_template_format(self):
        """Test that the research template follows proper format."""
        content = self.template_path.read_text(encoding='utf-8')
        
        # Check for required format elements
        self.assertIn("/goalkit.research", content, 
                     "Template should contain the command reference")
        self.assertIn("```", content, 
                     "Template should contain code examples")
        self.assertIn("Example", content, 
                     "Template should contain examples")
    
    def test_research_input_format_example(self):
        """Test that the input format example is present."""
        content = self.template_path.read_text(encoding='utf-8')
        
        # Look for the example input format
        self.assertIn("Research user authentication best practices", content,
                     "Template should contain example research approach")
        self.assertIn("security standards", content,
                     "Template should mention security standards")
        self.assertIn("user experience patterns", content,
                     "Template should mention user experience")
    
    def test_research_components(self):
        """Test that all research components are present."""
        content = self.template_path.read_text(encoding='utf-8')
        
        components = [
            "Research Planning",
            "Methodology Design", 
            "External Context Integration",
            "Knowledge Application"
        ]
        
        for component in components:
            with self.subTest(component=component):
                self.assertIn(component, content,
                             f"Template should contain component: {component}")
    
    def test_research_examples_in_examples_file(self):
        """Test that research command examples exist in examples.md."""
        examples_content = self.examples_path.read_text(encoding='utf-8')
        
        self.assertIn("/goalkit.research", examples_content,
                     "Examples.md should contain /goalkit.research command")
        self.assertIn("Research Topic:", examples_content,
                     "Examples.md should contain Research Topic element")
        self.assertIn("Research Goal:", examples_content,
                     "Examples.md should contain Research Goal element")
        self.assertIn("Methodology:", examples_content,
                     "Examples.md should contain Methodology element")


if __name__ == '__main__':
    unittest.main()