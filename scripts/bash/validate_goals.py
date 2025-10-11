#!/usr/bin/env python3
"""
Goal Validator - Validates goal files to ensure they meet quality standards

This script checks that goal files include all required elements for effective
Goal-Driven Development, focusing on measurable outcomes and success criteria.
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


class GoalValidator:
    """Validates goal files to ensure they meet quality standards."""
    
    def __init__(self):
        self.required_sections = [
            r'## 🎯 Goal Overview',
            r'## 📊 Success Metrics',
            r'## 👥 Target Users & Stakeholders',
            r'## 🎯 Goal Hypotheses'
        ]
        
        self.required_elements = {
            'goal_statement': r'\*\*Goal Statement\*\*:\s*\[(?!Clear,\s*concise)',
            'success_metrics': r'\*\*Metric [0-9]\*\*:\s*\[(?!Measurable outcome)',
            'primary_users': r'\*\*\[(?!User Type [0-9])',
            'hypotheses': r'\*\*Hypothesis [0-9]\*\*:\s*\[(?!Testable assumption)',
            'milestones': r'### Milestone [0-9]:.*\n.*Description:\s*\[(?!What this milestone achieves)'
        }
    
    def validate_file(self, file_path: Path) -> Tuple[bool, List[str]]:
        """
        Validates a single goal file.
        
        Args:
            file_path: Path to the goal file to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return False, [f"Could not read file: {e}"]
        
        # Check for required sections
        for section in self.required_sections:
            if not re.search(section, content):
                errors.append(f"Missing required section: {section}")
        
        # Check for properly filled out elements (not just placeholders)
        for element_name, pattern in self.required_elements.items():
            if re.search(pattern, content):
                errors.append(f"Found placeholder text in {element_name} - needs to be filled out properly")
        
        # Additional checks
        errors.extend(self._additional_checks(content))
        
        return len(errors) == 0, errors
    
    def _additional_checks(self, content: str) -> List[str]:
        """Perform additional validation checks."""
        errors = []
        
        # Check for measurable metrics (should contain specific, quantifiable targets)
        primary_metrics_section = re.search(r'### Primary Metrics \(Must achieve for success\)(.*?)###', 
                                           content, re.DOTALL)
        if primary_metrics_section:
            metrics_text = primary_metrics_section.group(1)
            # Look for actual targets vs placeholders - if it still has [specific, quantifiable target] then it's not filled out
            if re.search(r'Target:\s*\[specific,\s*quantifiable\s*target\]', metrics_text):
                errors.append("Primary metrics need specific, quantifiable targets")
        
        # Check for user/stakeholder identification
        stakeholders_section = re.search(r'### Primary Users(.*?)###', content, re.DOTALL)
        if stakeholders_section:
            stakeholders_text = stakeholders_section.group(1)
            if re.search(r'\[User Type [0-9]\]', stakeholders_text):
                errors.append("Primary users section has unfilled placeholders")
        
        # Check for testable hypotheses
        hypotheses_section = re.search(r'### Key Assumptions(.*?)###|### Key Assumptions(.*?)$', 
                                      content, re.DOTALL)
        if hypotheses_section:
            hypotheses_text = hypotheses_section.group(1) or hypotheses_section.group(2)
            if re.search(r'\[Testable assumption', hypotheses_text):
                errors.append("Goal hypotheses section has unfilled placeholders")
        
        return errors


def main():
    parser = argparse.ArgumentParser(description='Validate goal files for Goal Kit')
    parser.add_argument('files', nargs='+', type=Path, 
                        help='Goal file(s) to validate')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed validation information')
    
    args = parser.parse_args()
    
    validator = GoalValidator()
    all_valid = True
    
    for file_path in args.files:
        if not file_path.exists():
            print(f"[ERROR] File does not exist: {file_path}")
            all_valid = False
            continue
            
        is_valid, errors = validator.validate_file(file_path)
        
        if is_valid:
            print(f"[SUCCESS] {file_path.name} - Valid")
        else:
            print(f"[ERROR] {file_path.name} - Invalid")
            for error in errors:
                print(f"   - {error}")
            all_valid = False
    
    if not all_valid:
        sys.exit(1) 
    else:
        print("\n[SUCCESS] All goal files passed validation!")


if __name__ == "__main__":
    main()