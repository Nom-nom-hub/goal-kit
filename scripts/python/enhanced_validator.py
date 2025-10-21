#!/usr/bin/env python3
"""
Enhanced Validation Engine for Goal Kit Methodology
Multi-layered validation with content analysis and quality scoring (1-10 scale)
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

# Add the common Python utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common import (
    write_info,
    write_success,
    write_error,
    write_warning,
    test_git_repo,
    get_git_root
)


@dataclass
class ValidationResult:
    """Structured validation result with detailed feedback"""
    file_path: str
    file_type: str  # 'vision', 'goal', 'strategies', 'milestones', 'execution'
    overall_score: float  # 1-10 quality score
    max_score: float  # Maximum possible score for this file type
    passed: bool
    issues: List[str]
    strengths: List[str]
    recommendations: List[str]
    metrics: Dict[str, Any]


@dataclass
class QualityMetrics:
    """Quality metrics for different aspects of methodology components"""
    completeness: float      # 1-10: How complete is the content?
    specificity: float       # 1-10: How specific and actionable?
    measurability: float     # 1-10: How measurable are the outcomes?
    clarity: float          # 1-10: How clear and well-written?
    structure: float        # 1-10: How well-structured and organized?
    alignment: float        # 1-10: How well-aligned with methodology?


class EnhancedValidator:
    """Enhanced validation engine with multi-layered analysis"""

    def __init__(self, project_root: str = None):
        self.project_root = project_root or get_git_root()
        if not self.project_root:
            raise ValueError("Must be run from a git repository")

        self.vision_file = os.path.join(self.project_root, ".goalkit", "vision.md")
        self.goals_dir = os.path.join(self.project_root, ".goalkit", "goals")

        # Quality scoring weights for different file types
        self.weights = {
            'vision': {'completeness': 0.25, 'specificity': 0.20, 'measurability': 0.20, 'clarity': 0.20, 'structure': 0.15},
            'goal': {'completeness': 0.20, 'specificity': 0.25, 'measurability': 0.30, 'clarity': 0.15, 'structure': 0.10},
            'strategies': {'completeness': 0.25, 'specificity': 0.25, 'measurability': 0.15, 'clarity': 0.20, 'structure': 0.15},
            'milestones': {'completeness': 0.20, 'specificity': 0.20, 'measurability': 0.30, 'clarity': 0.15, 'structure': 0.15},
            'execution': {'completeness': 0.25, 'specificity': 0.25, 'measurability': 0.20, 'clarity': 0.15, 'structure': 0.15}
        }

    def validate_project(self, output_format: str = 'text') -> Dict[str, Any]:
        """Validate entire project methodology"""
        results = {
            'project': os.path.basename(self.project_root),
            'timestamp': datetime.now().isoformat(),
            'validation_results': [],
            'summary': {}
        }

        # Validate vision if exists
        if os.path.exists(self.vision_file):
            vision_result = self.validate_vision_file()
            results['validation_results'].append(vision_result)
            results['summary']['vision'] = {
                'score': vision_result.overall_score,
                'passed': vision_result.passed
            }

        # Validate all goals
        if os.path.exists(self.goals_dir):
            goal_results = self.validate_all_goals()
            results['validation_results'].extend(goal_results)

            if goal_results:
                scores = [r.overall_score for r in goal_results]
                results['summary']['goals'] = {
                    'count': len(goal_results),
                    'average_score': sum(scores) / len(scores),
                    'passed_count': sum(1 for r in goal_results if r.passed)
                }

        if output_format == 'json':
            print(json.dumps(results, indent=2))
        else:
            self._print_text_report(results)

        return results

    def validate_vision_file(self) -> ValidationResult:
        """Enhanced validation for vision.md"""
        if not os.path.exists(self.vision_file):
            return ValidationResult(
                file_path=self.vision_file,
                file_type='vision',
                overall_score=0,
                max_score=10,
                passed=False,
                issues=["Vision file does not exist"],
                strengths=[],
                recommendations=["Create vision.md using /goalkit.vision"],
                metrics={}
            )

        with open(self.vision_file, 'r', encoding='utf-8') as f:
            content = f.read()

        return self._analyze_vision_content(content)

    def _analyze_vision_content(self, content: str) -> ValidationResult:
        """Analyze vision content for quality and completeness"""
        issues = []
        strengths = []
        recommendations = []
        metrics = {}

        # Basic structure checks
        required_sections = [
            'Project Purpose', 'Success Metrics', 'Guiding Principles',
            'Project Goals', 'Project Scope'
        ]

        found_sections = []
        for section in required_sections:
            if section in content:
                found_sections.append(section)
            else:
                issues.append(f"Missing section: {section}")

        metrics['section_completeness'] = len(found_sections) / len(required_sections)

        # Content quality analysis
        word_count = len(content.split())
        metrics['word_count'] = word_count

        if word_count < 200:
            issues.append("Vision seems too brief (< 200 words)")
            recommendations.append("Expand vision with more specific details about purpose and outcomes")
        elif word_count > 1000:
            strengths.append("Comprehensive vision with good detail level")
        else:
            strengths.append("Good vision length and detail level")

        # Check for specific, measurable outcomes
        measurable_patterns = [
            r'\d+%',           # Percentages
            r'\d+\s*(users?|customers?)',  # User numbers
            r'\$\d+',          # Dollar amounts
            r'\d+\s*(days?|weeks?|months?)',  # Time frames
            r'target.*\d+',    # Target numbers
            r'goal.*\d+',      # Goal numbers
        ]

        measurable_count = 0
        for pattern in measurable_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            measurable_count += len(matches)

        metrics['measurable_elements'] = measurable_count

        if measurable_count < 3:
            issues.append("Vision lacks specific, measurable success criteria")
            recommendations.append("Add specific targets (percentages, user counts, timeframes, dollar amounts)")
        else:
            strengths.append(f"Good use of measurable criteria ({measurable_count} specific targets found)")

        # Check for actionable principles
        principle_count = len(re.findall(r'^###?\s+', content, re.MULTILINE))
        metrics['principle_count'] = principle_count

        if principle_count < 3:
            issues.append("Vision needs more guiding principles")
            recommendations.append("Add 4-6 actionable principles that guide AI decision-making")
        else:
            strengths.append(f"Good number of guiding principles ({principle_count})")

        # Calculate quality metrics
        quality = self._calculate_quality_metrics(content, 'vision', metrics)

        # Calculate overall score
        overall_score = self._calculate_overall_score(quality, 'vision')

        # Determine pass/fail (threshold: 6.0)
        passed = overall_score >= 6.0

        if not passed:
            recommendations.append("Review and enhance vision to meet quality standards before proceeding")

        return ValidationResult(
            file_path=self.vision_file,
            file_type='vision',
            overall_score=round(overall_score, 2),
            max_score=10.0,
            passed=passed,
            issues=issues,
            strengths=strengths,
            recommendations=recommendations,
            metrics=metrics
        )

    def validate_goal_file(self, goal_path: str) -> ValidationResult:
        """Enhanced validation for individual goal files"""
        if not os.path.exists(goal_path):
            return ValidationResult(
                file_path=goal_path,
                file_type='goal',
                overall_score=0,
                max_score=10,
                passed=False,
                issues=["Goal file does not exist"],
                strengths=[],
                recommendations=["Complete goal definition with success metrics"],
                metrics={}
            )

        with open(goal_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return self._analyze_goal_content(content, goal_path)

    def _analyze_goal_content(self, content: str, file_path: str) -> ValidationResult:
        """Analyze goal content for quality and methodology compliance"""
        issues = []
        strengths = []
        recommendations = []
        metrics = {}

        # Required sections for goals
        required_sections = [
            'Goal Statement', 'Success Metrics', 'Validation Strategy',
            'Goal Breakdown', 'Review Process', 'Completion Criteria'
        ]

        found_sections = []
        for section in required_sections:
            if section in content:
                found_sections.append(section)
            else:
                issues.append(f"Missing section: {section}")

        metrics['section_completeness'] = len(found_sections) / len(required_sections)

        # Goal statement quality
        goal_match = re.search(r'Goal Statement[:\s]+(.+?)(?=\n\n|\n#|$)', content, re.IGNORECASE | re.DOTALL)
        if goal_match:
            goal_statement = goal_match.group(1).strip()
            metrics['goal_statement_length'] = len(goal_statement)

            if len(goal_statement) < 50:
                issues.append("Goal statement is too brief (< 50 characters)")
                recommendations.append("Expand goal statement to clearly describe the desired outcome")
            else:
                strengths.append("Clear, descriptive goal statement")

            # Check for implementation details in goal (should focus on outcomes)
            implementation_keywords = [
                'react', 'python', 'javascript', 'api', 'database', 'framework',
                'library', 'technology', 'platform', 'language', 'server', 'client'
            ]

            impl_count = sum(1 for keyword in implementation_keywords if keyword.lower() in goal_statement.lower())
            metrics['implementation_details'] = impl_count

            if impl_count > 0:
                issues.append("Goal statement contains implementation details (should focus on outcomes)")
                recommendations.append("Remove technology/framework references - focus on user/business outcomes")
        else:
            issues.append("No clear goal statement found")
            recommendations.append("Add a clear goal statement describing the desired outcome")

        # Success metrics analysis
        success_section = re.search(r'Success Metrics.*?(\n\n|\n#|$)', content, re.IGNORECASE | re.DOTALL)
        if success_section:
            success_content = success_section.group(0)

            # Look for specific targets
            target_patterns = [
                r'Target:\s*[\w\s\d%$\.+-]+',
                r'target.*\d+',
                r'goal.*\d+',
                r'objective.*\d+'
            ]

            targets_found = []
            for pattern in target_patterns:
                matches = re.findall(pattern, success_content, re.IGNORECASE)
                targets_found.extend(matches)

            metrics['specific_targets'] = len(targets_found)

            if len(targets_found) < 2:
                issues.append("Success metrics lack specific, quantifiable targets")
                recommendations.append("Add specific targets (numbers, percentages, timeframes) for each metric")
            else:
                strengths.append(f"Good use of specific targets ({len(targets_found)} targets found)")

            # Check for measurement approach
            if 'Measurement Approach' not in success_content:
                issues.append("No clear measurement approach defined")
                recommendations.append("Add data sources, measurement frequency, and success thresholds")
        else:
            issues.append("No success metrics section found")
            recommendations.append("Add success metrics with specific, measurable targets")

        # Risk assessment
        if 'Risk Assessment' in content:
            strengths.append("Risk assessment included")
        else:
            issues.append("No risk assessment found")
            recommendations.append("Add risk assessment with mitigation strategies")

        # Calculate quality metrics
        quality = self._calculate_quality_metrics(content, 'goal', metrics)

        # Calculate overall score
        overall_score = self._calculate_overall_score(quality, 'goal')

        # Determine pass/fail (threshold: 7.0 for goals - higher standard)
        passed = overall_score >= 7.0

        if not passed:
            recommendations.append("Enhance goal definition to meet quality standards before proceeding to strategies")

        return ValidationResult(
            file_path=file_path,
            file_type='goal',
            overall_score=round(overall_score, 2),
            max_score=10.0,
            passed=passed,
            issues=issues,
            strengths=strengths,
            recommendations=recommendations,
            metrics=metrics
        )

    def validate_all_goals(self) -> List[ValidationResult]:
        """Validate all goals in the project"""
        if not os.path.exists(self.goals_dir):
            return []

        results = []
        for item in os.listdir(self.goals_dir):
            goal_path = os.path.join(self.goals_dir, item)
            if os.path.isdir(goal_path):
                goal_file = os.path.join(goal_path, "goal.md")
                if os.path.exists(goal_file):
                    result = self.validate_goal_file(goal_file)
                    results.append(result)

        return results

    def _calculate_quality_metrics(self, content: str, file_type: str, existing_metrics: Dict) -> QualityMetrics:
        """Calculate quality metrics for content"""
        # Completeness (based on section coverage and content length)
        base_completeness = existing_metrics.get('section_completeness', 0)
        word_count = len(content.split())
        length_factor = min(word_count / 500, 1.0)  # Normalize to 500 words
        completeness = (base_completeness * 0.7 + length_factor * 0.3) * 10

        # Specificity (based on specific targets and concrete language)
        specific_indicators = [
            bool(re.search(r'\d+%', content)),  # Percentages
            bool(re.search(r'\d+\s*(user|customer|people)', content, re.IGNORECASE)),  # User numbers
            bool(re.search(r'\$\d+', content)),  # Dollar amounts
            bool(re.search(r'\d+\s*(day|week|month|year)', content, re.IGNORECASE)),  # Time frames
            len(re.findall(r'\b(target|goal|objective|metric)\b', content, re.IGNORECASE)) >= 3
        ]
        specificity = (sum(specific_indicators) / len(specific_indicators)) * 10

        # Measurability (based on measurement approaches and validation)
        measurement_indicators = [
            'Measurement Approach' in content,
            'Success Threshold' in content,
            'Validation Strategy' in content,
            'Data Sources' in content,
            existing_metrics.get('measurable_elements', 0) >= 2
        ]
        measurability = (sum(measurement_indicators) / len(measurement_indicators)) * 10

        # Clarity (based on structure and readability)
        section_count = len(re.findall(r'^#{1,3}\s+', content, re.MULTILINE))
        avg_section_length = word_count / max(section_count, 1)
        structure_factor = min(section_count / 8, 1.0)  # Normalize to 8 sections
        length_factor = 1.0 if 50 <= avg_section_length <= 200 else 0.7
        clarity = (structure_factor * 0.6 + length_factor * 0.4) * 10

        # Structure (based on organization and flow)
        has_intro = bool(re.search(r'^#{1,2}\s+', content, re.MULTILINE))
        has_conclusion = bool(re.search(r'completion|summary|next steps', content, re.IGNORECASE))
        logical_flow = 1.0 if has_intro and has_conclusion else 0.8
        structure = logical_flow * 10

        # Alignment (based on methodology compliance)
        methodology_keywords = [
            'goal-driven', 'measurable', 'outcome', 'success criteria',
            'strategy', 'milestone', 'validation', 'learning'
        ]
        methodology_count = sum(1 for keyword in methodology_keywords if keyword.lower() in content.lower())
        alignment = min(methodology_count / 4, 1.0) * 10  # Normalize to 4 methodology keywords

        return QualityMetrics(
            completeness=round(completeness, 2),
            specificity=round(specificity, 2),
            measurability=round(measurability, 2),
            clarity=round(clarity, 2),
            structure=round(structure, 2),
            alignment=round(alignment, 2)
        )

    def _calculate_overall_score(self, quality: QualityMetrics, file_type: str) -> float:
        """Calculate weighted overall score"""
        weights = self.weights[file_type]

        overall = (
            quality.completeness * weights['completeness'] +
            quality.specificity * weights['specificity'] +
            quality.measurability * weights['measurability'] +
            quality.clarity * weights['clarity'] +
            quality.structure * weights['structure']
        )

        # For goals, add alignment bonus/penalty
        if file_type == 'goal':
            overall += quality.alignment * 0.1  # Bonus for methodology alignment

        return min(overall, 10.0)

    def _print_text_report(self, results: Dict[str, Any]):
        """Print comprehensive text report"""
        print(f"\n{'='*80}")
        print("GOAL KIT ENHANCED VALIDATION REPORT")
        print(f"Project: {results['project']}")
        print(f"Generated: {results['timestamp']}")
        print(f"{'='*80}")

        for result in results['validation_results']:
            print(f"\n📄 {result.file_type.upper()}: {os.path.basename(result.file_path)}")
            print(f"   Score: {result.overall_score:.1f}/10.0 {'✅' if result.passed else '❌'}")

            if result.issues:
                print("   Issues:")
                for issue in result.issues[:3]:  # Show top 3 issues
                    print(f"     ❌ {issue}")

            if result.strengths:
                print("   Strengths:")
                for strength in result.strengths[:3]:  # Show top 3 strengths
                    print(f"     ✅ {strength}")

            if result.recommendations:
                print("   Recommendations:")
                for rec in result.recommendations[:2]:  # Show top 2 recommendations
                    print(f"     💡 {rec}")

        # Summary section
        print(f"\n{'='*80}")
        print("SUMMARY")
        print(f"{'='*80}")

        if 'vision' in results['summary']:
            vision = results['summary']['vision']
            print(f"Vision: Score {vision['score']:.1f}/10.0 {'✅' if vision['passed'] else '❌'}")

        if 'goals' in results['summary']:
            goals = results['summary']['goals']
            avg_score = goals['average_score']
            passed_pct = (goals['passed_count'] / goals['count']) * 100
            print(f"Goals: {goals['passed_count']}/{goals['count']} passed ({passed_pct:.1f}%)")
            print(f"       Average Score: {avg_score:.1f}/10.0")

        print(f"\n{'='*80}")


def main():
    """Main validation function"""
    if not test_git_repo():
        write_error("Not in a git repository")
        write_info("Please run this from the root of a Goal Kit project")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(description='Enhanced Goal Kit Methodology Validation')
    parser.add_argument('--json', action='store_true', help='Output results in JSON format')
    parser.add_argument('--goal', help='Validate specific goal file')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')

    args = parser.parse_args()

    try:
        validator = EnhancedValidator()
    except ValueError as e:
        write_error(str(e))
        sys.exit(1)

    if args.goal:
        result = validator.validate_goal_file(args.goal)
        if args.format == 'json':
            print(json.dumps({
                'file_path': result.file_path,
                'file_type': result.file_type,
                'overall_score': result.overall_score,
                'passed': result.passed,
                'issues': result.issues,
                'strengths': result.strengths,
                'recommendations': result.recommendations,
                'metrics': result.metrics
            }, indent=2))
        else:
            print(f"\n📄 Goal Validation: {os.path.basename(result.file_path)}")
            print(f"Score: {result.overall_score:.1f}/10.0 {'✅' if result.passed else '❌'}")

            if result.issues:
                print("\nIssues:")
                for issue in result.issues:
                    print(f"  ❌ {issue}")

            if result.strengths:
                print("\nStrengths:")
                for strength in result.strengths:
                    print(f"  ✅ {strength}")

            if result.recommendations:
                print("\nRecommendations:")
                for rec in result.recommendations:
                    print(f"  💡 {rec}")
    else:
        validator.validate_project(args.format)


if __name__ == "__main__":
    main()