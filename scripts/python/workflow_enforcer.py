#!/usr/bin/env python3
"""
Workflow Enforcement System for Goal Kit Methodology
Ensures agents follow proper workflow instructions and run scripts correctly
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# Add the common Python utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common import (
    write_info,
    write_success,
    write_error,
    write_warning,
    write_step,
    test_git_repo,
    get_git_root
)


@dataclass
class WorkflowViolation:
    """Represents a workflow violation detected by the enforcer"""
    violation_type: str  # 'script_bypass', 'manual_directory_creation', 'missing_script_execution'
    severity: str  # 'critical', 'high', 'medium', 'low'
    description: str
    detected_file: str
    expected_action: str
    remediation_steps: List[str]
    timestamp: str


@dataclass
class WorkflowCheck:
    """Result of a workflow compliance check"""
    is_compliant: bool
    violations: List[WorkflowViolation]
    recommendations: List[str]
    next_actions: List[str]


class WorkflowEnforcer:
    """Enforces proper Goal Kit workflow compliance"""

    def __init__(self, project_root: str = None):
        self.project_root = project_root or get_git_root()
        if not self.project_root:
            raise ValueError("Must be run from a git repository")

        self.goals_dir = os.path.join(self.project_root, ".goalkit", "goals")
        self.violation_log = os.path.join(self.project_root, ".goalkit", "workflow_violations.json")

        # Create .goalkit directory if it doesn't exist
        os.makedirs(os.path.join(self.project_root, ".goalkit"), exist_ok=True)

    def check_workflow_compliance(self) -> WorkflowCheck:
        """Check if current project state complies with workflow requirements"""
        violations = []
        recommendations = []
        next_actions = []

        # Check 1: Verify that goals were created through proper script execution
        script_bypass_violations = self._check_script_bypass_violations()
        violations.extend(script_bypass_violations)

        # Check 2: Verify no manual directory creation occurred
        manual_creation_violations = self._check_manual_creation_violations()
        violations.extend(manual_creation_violations)

        # Check 3: Verify required files exist and have proper structure
        structure_violations = self._check_structure_violations()
        violations.extend(structure_violations)

        # Check 4: Verify git branch management compliance
        branch_violations = self._check_branch_compliance()
        violations.extend(branch_violations)

        # Generate recommendations based on violations
        if violations:
            recommendations = self._generate_recommendations(violations)
            next_actions = self._generate_next_actions(violations)

        is_compliant = len(violations) == 0

        return WorkflowCheck(
            is_compliant=is_compliant,
            violations=violations,
            recommendations=recommendations,
            next_actions=next_actions
        )

    def _check_script_bypass_violations(self) -> List[WorkflowViolation]:
        """Check if goals were created by bypassing the required scripts"""
        violations = []

        if not os.path.exists(self.goals_dir):
            return violations

        # Check each goal directory for proper structure
        for item in os.listdir(self.goals_dir):
            goal_path = os.path.join(self.goals_dir, item)
            if not os.path.isdir(goal_path):
                continue

            # Check if goal.md exists and has proper script-generated content
            goal_file = os.path.join(goal_path, "goal.md")
            write_info(f"Debug: Checking goal file: {goal_file}")
            if os.path.exists(goal_file):
                with open(goal_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                write_info(f"Debug: Goal file exists, content length: {len(content)}")
                write_info(f"Debug: First 100 chars: {content[:100]}")

                # Check for script-generated markers
                has_script_markers = (
                    "Methodology: Goal-Driven Development" in content and
                    "Branch:" in content and
                    "Created:" in content and
                    "Status: Draft" in content and
                    content.count("**") >= 5  # Script-generated content has consistent formatting
                )

                # Also check for manual creation indicators
                manual_indicators = [
                    "Manual Goal Creation" in content,
                    "manual-branch" in content,
                    "Status: Manual" in content,
                    "created manually" in content.lower()
                ]

                write_info(f"Debug: Has script markers: {has_script_markers}")
                write_info(f"Debug: Manual indicators found: {manual_indicators}")

                # Check if this looks like manual creation
                manual_indicators_found = [
                    indicator for indicator in [
                        "Manual Goal Creation",
                        "manual-branch",
                        "Status: Manual",
                        "created manually",
                        "Manual Creation"  # This should catch the methodology field
                    ] if indicator in content
                ]

                # Debug output
                if manual_indicators_found:
                    write_info(f"Debug: Found manual indicators in {goal_file}: {manual_indicators_found}")

                manual_creation_detected = (
                    not has_script_markers or
                    len(manual_indicators_found) > 0
                )

                if manual_creation_detected:
                    violations.append(WorkflowViolation(
                        violation_type="script_bypass",
                        severity="critical",
                        description=f"Goal '{item}' appears to have been created manually, bypassing required Python script",
                        detected_file=goal_file,
                        expected_action="Run create_new_goal.py script with proper JSON arguments",
                        remediation_steps=[
                            f"Delete the manually created directory: {goal_path}",
                            f"Run the proper script: python scripts/python/create_new_goal.py --json \"Your goal description\"",
                            "Complete the goal definition in the script-generated goal.md file",
                            "Follow with /goalkit.strategies to explore implementation approaches"
                        ],
                        timestamp=datetime.now().isoformat()
                    ))

        return violations

    def _check_manual_creation_violations(self) -> List[WorkflowViolation]:
        """Check for evidence of manual directory creation"""
        violations = []

        if not os.path.exists(self.goals_dir):
            return violations

        # Check git history for manual creation patterns
        try:
            # Look for commits that might indicate manual creation
            result = subprocess.run([
                "git", "log", "--oneline", "--grep", "manual",
                "--grep", "create.*directory", "--grep", "mkdir",
                "-i", "--all"
            ], cwd=self.project_root, capture_output=True, text=True, timeout=10)

            if result.returncode == 0 and result.stdout.strip():
                manual_commits = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                if manual_commits:
                    violations.append(WorkflowViolation(
                        violation_type="manual_directory_creation",
                        severity="high",
                        description=f"Found {len(manual_commits)} commits suggesting manual directory creation",
                        detected_file="git_history",
                        expected_action="Use only script-based goal creation, never manual directory creation",
                        remediation_steps=[
                            "Review git history for manual creation patterns",
                            "Remove any manually created goal directories",
                            "Re-create goals using proper Python scripts",
                            "Ensure all future goals use create_new_goal.py script"
                        ],
                        timestamp=datetime.now().isoformat()
                    ))

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            pass  # Git log check failed, continue with other checks

        return violations

    def _check_structure_violations(self) -> List[WorkflowViolation]:
        """Check for proper file structure and required components"""
        violations = []

        if not os.path.exists(self.goals_dir):
            return violations

        # Check each goal directory
        for item in os.listdir(self.goals_dir):
            goal_path = os.path.join(self.goals_dir, item)
            if not os.path.isdir(goal_path):
                continue

            # Check for required files
            required_files = ["goal.md"]
            for req_file in required_files:
                file_path = os.path.join(goal_path, req_file)
                if not os.path.exists(file_path):
                    violations.append(WorkflowViolation(
                        violation_type="missing_required_file",
                        severity="high",
                        description=f"Missing required file {req_file} in goal directory {item}",
                        detected_file=goal_path,
                        expected_action=f"Create {req_file} using proper workflow scripts",
                        remediation_steps=[
                            f"Ensure {req_file} exists in {goal_path}",
                            "Use workflow scripts to generate proper file structure",
                            "Verify all required files are present before proceeding"
                        ],
                        timestamp=datetime.now().isoformat()
                    ))

        return violations

    def _check_branch_compliance(self) -> List[WorkflowViolation]:
        """Check if git branches are properly managed"""
        violations = []

        try:
            # Get current branch
            result = subprocess.run([
                "git", "branch", "--show-current"
            ], cwd=self.project_root, capture_output=True, text=True, timeout=5)

            if result.returncode == 0:
                current_branch = result.stdout.strip()

                # Check if we're on a goal-specific branch
                if current_branch and not current_branch.startswith("goal-") and current_branch != "main" and current_branch != "master":
                    violations.append(WorkflowViolation(
                        violation_type="branch_noncompliance",
                        severity="medium",
                        description=f"Current branch '{current_branch}' does not follow goal-specific naming convention",
                        detected_file="git_branch",
                        expected_action="Use goal-specific branch names (goal-xxx format) for all goal work",
                        remediation_steps=[
                            "Create proper goal-specific branch using create_new_goal.py script",
                            "Switch to the correct goal branch",
                            "Ensure all goal work happens on goal-specific branches"
                        ],
                        timestamp=datetime.now().isoformat()
                    ))

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            pass  # Git branch check failed

        return violations

    def _generate_recommendations(self, violations: List[WorkflowViolation]) -> List[str]:
        """Generate recommendations based on detected violations"""
        recommendations = []

        critical_count = len([v for v in violations if v.severity == "critical"])
        high_count = len([v for v in violations if v.severity == "high"])

        if critical_count > 0:
            recommendations.append(f"🚨 CRITICAL: {critical_count} critical workflow violations require immediate attention")
            recommendations.append("Stop all current work and fix critical violations before proceeding")

        if high_count > 0:
            recommendations.append(f"⚠️ HIGH PRIORITY: {high_count} high-severity violations need prompt resolution")

        # General recommendations
        recommendations.extend([
            "Always run Python scripts first for any goal-related operations",
            "Never manually create goal directories - use create_new_goal.py script",
            "Follow the exact workflow sequence: vision → goal → strategies → milestones → execute",
            "Use --json flag when running goal creation scripts for proper integration"
        ])

        return recommendations

    def _generate_next_actions(self, violations: List[WorkflowViolation]) -> List[str]:
        """Generate specific next actions to resolve violations"""
        actions = []

        if any(v.violation_type == "script_bypass" for v in violations):
            actions.append("🛠️ Run: python scripts/python/create_new_goal.py --json 'Your goal description'")
            actions.append("📝 Complete the generated goal.md file with proper success metrics")
            actions.append("🔄 Use /goalkit.strategies to explore implementation approaches")

        if any(v.violation_type == "manual_directory_creation" for v in violations):
            actions.append("🗑️ Remove manually created directories")
            actions.append("🔄 Re-create goals using proper Python scripts")
            actions.append("📚 Review workflow documentation in templates/")

        if any(v.violation_type == "missing_required_file" for v in violations):
            actions.append("📄 Generate missing required files using workflow scripts")
            actions.append("✅ Verify all goal directories have complete file structure")

        if any(v.violation_type == "branch_noncompliance" for v in violations):
            actions.append("🌿 Create and switch to proper goal-specific branch")
            actions.append("🔀 Ensure all goal work happens on goal branches")

        return actions

    def log_violations(self, violations: List[WorkflowViolation]):
        """Log violations for historical tracking"""
        try:
            existing_violations = []
            if os.path.exists(self.violation_log):
                with open(self.violation_log, 'r', encoding='utf-8') as f:
                    existing_violations = json.load(f)

            # Add new violations
            violation_data = [asdict(v) for v in violations]
            existing_violations.extend(violation_data)

            # Keep only last 100 violations to prevent log bloat
            if len(existing_violations) > 100:
                existing_violations = existing_violations[-100:]

            with open(self.violation_log, 'w', encoding='utf-8') as f:
                json.dump(existing_violations, f, indent=2)

        except Exception as e:
            write_warning(f"Could not log violations: {e}")

    def generate_compliance_report(self) -> str:
        """Generate a comprehensive workflow compliance report"""
        check = self.check_workflow_compliance()

        lines = []
        lines.append("=" * 80)
        lines.append("GOAL KIT WORKFLOW COMPLIANCE REPORT")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)

        if check.is_compliant:
            lines.append("✅ WORKFLOW COMPLIANT")
            lines.append("All workflow requirements are properly followed.")
        else:
            lines.append("❌ WORKFLOW VIOLATIONS DETECTED")
            lines.append(f"Found {len(check.violations)} violations requiring attention.")

            # Group violations by severity
            critical = [v for v in check.violations if v.severity == "critical"]
            high = [v for v in check.violations if v.severity == "high"]
            medium = [v for v in check.violations if v.severity == "medium"]
            low = [v for v in check.violations if v.severity == "low"]

            if critical:
                lines.append(f"\n🚨 CRITICAL VIOLATIONS ({len(critical)}):")
                for v in critical:
                    lines.append(f"  • {v.description}")
                    lines.append(f"    File: {v.detected_file}")
                    lines.append("    Expected: " + v.expected_action)

            if high:
                lines.append(f"\n⚠️ HIGH PRIORITY VIOLATIONS ({len(high)}):")
                for v in high:
                    lines.append(f"  • {v.description}")

            if medium:
                lines.append(f"\n📋 MEDIUM PRIORITY VIOLATIONS ({len(medium)}):")
                for v in medium:
                    lines.append(f"  • {v.description}")

            if low:
                lines.append(f"\n📝 LOW PRIORITY VIOLATIONS ({len(low)}):")
                for v in low:
                    lines.append(f"  • {v.description}")

        if check.recommendations:
            lines.append("\n💡 RECOMMENDATIONS:")
            for rec in check.recommendations:
                lines.append(f"  • {rec}")

        if check.next_actions:
            lines.append("\n🚀 NEXT ACTIONS:")
            for action in check.next_actions:
                lines.append(f"  • {action}")

        lines.append("=" * 80)
        return "\n".join(lines)


def enforce_workflow_compliance():
    """Main function to enforce workflow compliance"""
    if not test_git_repo():
        write_error("Not in a git repository")
        write_info("Please run this from the root of a Goal Kit project")
        sys.exit(1)

    try:
        enforcer = WorkflowEnforcer()
        check = enforcer.check_workflow_compliance()

        # Log violations if any found
        if check.violations:
            enforcer.log_violations(check.violations)

        # Generate and display report
        report = enforcer.generate_compliance_report()
        print(report)

        # Exit with error code if violations found
        if not check.is_compliant:
            write_error("Workflow violations detected. Please address them before proceeding.")
            sys.exit(1)
        else:
            write_success("Workflow compliance verified!")

    except Exception as e:
        write_error(f"Error during workflow enforcement: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Goal Kit Workflow Enforcement System')
    parser.add_argument('--check', action='store_true', help='Check workflow compliance')
    parser.add_argument('--report', action='store_true', help='Generate compliance report')
    parser.add_argument('--enforce', action='store_true', help='Enforce compliance and exit with error on violations')

    args = parser.parse_args()

    if args.check or args.enforce or args.report:
        enforce_workflow_compliance()
    else:
        # Default: show help
        parser.print_help()


if __name__ == "__main__":
    main()