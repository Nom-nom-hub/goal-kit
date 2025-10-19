#!/usr/bin/env python3
"""
Simple goal validation script for Goal Kit
"""

import sys
import os
import re


def validate_goal_file(file_path):
    """Validate a single goal file based on required elements."""
    if not os.path.exists(file_path):
        print(f"[ERROR] Goal file not found: {file_path}")
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Basic validations for goal files
        issues = []

        # Check for required sections
        if "Goal Statement" not in content:
            issues.append("Missing 'Goal Statement' section")
        
        if "Success Metrics" not in content:
            issues.append("Missing 'Success Metrics' section")
        
        if "Target:" not in content:
            issues.append("Missing 'Target:' in success metrics")
        
        if "Milestone" not in content:
            issues.append("Missing 'Milestone' sections")

        if issues:
            print(f"[VALIDATION ISSUES] {file_path}:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print(f"[VALIDATION SUCCESS] {file_path} passed validation.")
            return True

    except Exception as e:
        print(f"[ERROR] Could not read {file_path}: {str(e)}")
        return False


def main():
    if len(sys.argv) < 2:
        print("[ERROR] No goal files provided to validate.")
        print("Usage: validate_goals.py <goal_file1> [goal_file2] ...")
        sys.exit(1)

    files = sys.argv[1:]
    all_valid = True

    for file_path in files:
        if not validate_goal_file(file_path):
            all_valid = False

    if not all_valid:
        print("\n[SUMMARY] Some goal files failed validation.")
        sys.exit(1)
    else:
        print("\n[SUMMARY] All goal files passed validation.")
        sys.exit(0)


if __name__ == "__main__":
    main()