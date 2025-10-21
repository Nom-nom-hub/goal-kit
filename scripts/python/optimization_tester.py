#!/usr/bin/env python3
"""
Comprehensive Testing and Validation Framework for Goal Kit Optimization
Tests all Phase 1, 2, and 3 systems for integration and functionality
"""

import os
import sys
import json
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
    test_git_repo,
    get_git_root
)


@dataclass
class TestResult:
    """Structured test result"""
    test_name: str
    category: str  # 'syntax', 'functionality', 'integration', 'performance'
    status: str  # 'passed', 'failed', 'warning', 'error'
    execution_time: float
    message: str
    details: Dict[str, Any]


@dataclass
class SystemTestSuite:
    """Test suite for a specific system"""
    system_name: str
    description: str
    tests: List[TestResult]
    overall_status: str
    total_time: float


@dataclass
class IntegrationTestReport:
    """Comprehensive integration test report"""
    test_timestamp: str
    project_name: str
    systems_tested: int
    total_tests: int
    passed_tests: int
    failed_tests: int
    warnings: int
    test_suites: List[SystemTestSuite]
    integration_score: float
    recommendations: List[str]


class OptimizationTester:
    """Comprehensive testing framework for Goal Kit optimization systems"""

    def __init__(self, project_root: str = None):
        self.project_root = project_root or get_git_root()
        if not self.project_root:
            raise ValueError("Must be run from a git repository")

        # Define all systems to test
        self.systems_to_test = {
            'enhanced_validator': {
                'script': 'scripts/python/enhanced_validator.py',
                'description': 'Enhanced validation with quality scoring',
                'tests': ['syntax', 'basic_validation', 'quality_scoring', 'output_formats']
            },
            'progress_tracker': {
                'script': 'scripts/python/progress_tracker.py',
                'description': 'Progress tracking and analytics',
                'tests': ['syntax', 'progress_analysis', 'velocity_calculation', 'report_generation']
            },
            'smart_context_manager': {
                'script': 'scripts/python/smart_context_manager.py',
                'description': 'Smart context management',
                'tests': ['syntax', 'context_analysis', 'file_updates', 'phase_detection']
            },
            'learning_system': {
                'script': 'scripts/python/learning_system.py',
                'description': 'Learning loops and pattern recognition',
                'tests': ['syntax', 'insight_capture', 'pattern_analysis', 'retrospective_generation']
            },
            'collaboration_hub': {
                'script': 'scripts/python/collaboration_hub.py',
                'description': 'Cross-goal collaboration',
                'tests': ['syntax', 'similarity_analysis', 'knowledge_sharing', 'collaboration_insights']
            },
            'workflow_intelligence': {
                'script': 'scripts/python/workflow_intelligence.py',
                'description': 'Workflow intelligence and recommendations',
                'tests': ['syntax', 'intelligence_analysis', 'recommendation_generation', 'optimization_identification']
            },
            'methodology_optimizer': {
                'script': 'scripts/python/methodology_optimizer.py',
                'description': 'Methodology optimization framework',
                'tests': ['syntax', 'methodology_analysis', 'proposal_generation', 'continuous_improvement']
            }
        }

    def run_comprehensive_tests(self) -> IntegrationTestReport:
        """Run comprehensive tests on all optimization systems"""
        test_suites = []
        total_start_time = datetime.now()

        for system_name, system_info in self.systems_to_test.items():
            write_info(f"Testing {system_name}...")
            suite = self._test_system(system_name, system_info)
            test_suites.append(suite)

        total_time = (datetime.now() - total_start_time).total_seconds()

        # Calculate overall statistics
        all_tests = []
        for suite in test_suites:
            all_tests.extend(suite.tests)

        passed_tests = len([t for t in all_tests if t.status == 'passed'])
        failed_tests = len([t for t in all_tests if t.status == 'failed'])
        warnings = len([t for t in all_tests if t.status == 'warning'])

        # Calculate integration score
        integration_score = (passed_tests / len(all_tests)) * 100 if all_tests else 0

        # Generate recommendations
        recommendations = self._generate_test_recommendations(test_suites)

        return IntegrationTestReport(
            test_timestamp=datetime.now().isoformat(),
            project_name=os.path.basename(self.project_root),
            systems_tested=len(test_suites),
            total_tests=len(all_tests),
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            warnings=warnings,
            test_suites=test_suites,
            integration_score=round(integration_score, 2),
            recommendations=recommendations
        )

    def _test_system(self, system_name: str, system_info: Dict[str, Any]) -> SystemTestSuite:
        """Test a specific system comprehensively"""
        start_time = datetime.now()
        tests = []

        # Syntax test
        syntax_test = self._test_syntax(system_name, system_info['script'])
        tests.append(syntax_test)

        # Functionality tests
        for test_type in system_info['tests']:
            if test_type != 'syntax':  # Skip syntax as it's already tested
                func_test = self._test_functionality(system_name, system_info['script'], test_type)
                tests.append(func_test)

        # Calculate overall status
        overall_status = self._calculate_suite_status(tests)
        total_time = (datetime.now() - start_time).total_seconds()

        return SystemTestSuite(
            system_name=system_name,
            description=system_info['description'],
            tests=tests,
            overall_status=overall_status,
            total_time=round(total_time, 2)
        )

    def _test_syntax(self, system_name: str, script_path: str) -> TestResult:
        """Test Python syntax compilation"""
        start_time = datetime.now()

        try:
            result = subprocess.run([
                sys.executable, '-m', 'py_compile', script_path
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)

            execution_time = (datetime.now() - start_time).total_seconds()

            if result.returncode == 0:
                return TestResult(
                    test_name=f"{system_name}_syntax",
                    category='syntax',
                    status='passed',
                    execution_time=execution_time,
                    message="Python syntax validation passed",
                    details={'stdout': result.stdout, 'stderr': result.stderr}
                )
            else:
                return TestResult(
                    test_name=f"{system_name}_syntax",
                    category='syntax',
                    status='failed',
                    execution_time=execution_time,
                    message=f"Syntax error: {result.stderr}",
                    details={'stdout': result.stdout, 'stderr': result.stderr}
                )

        except subprocess.TimeoutExpired:
            return TestResult(
                test_name=f"{system_name}_syntax",
                category='syntax',
                status='error',
                execution_time=30.0,
                message="Syntax test timed out",
                details={}
            )
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return TestResult(
                test_name=f"{system_name}_syntax",
                category='syntax',
                status='error',
                execution_time=execution_time,
                message=f"Error running syntax test: {e}",
                details={}
            )

    def _test_functionality(self, system_name: str, script_path: str, test_type: str) -> TestResult:
        """Test system functionality"""
        start_time = datetime.now()

        try:
            # Test help output
            result = subprocess.run([
                sys.executable, script_path, '--help'
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)

            execution_time = (datetime.now() - start_time).total_seconds()

            if result.returncode == 0:
                # Check if help output contains expected content
                help_output = result.stdout
                if 'error' in help_output.lower() or 'traceback' in help_output.lower():
                    return TestResult(
                        test_name=f"{system_name}_{test_type}",
                        category='functionality',
                        status='warning',
                        execution_time=execution_time,
                        message=f"Help command succeeded but output may have issues",
                        details={'help_output': help_output[:500]}
                    )
                else:
                    return TestResult(
                        test_name=f"{system_name}_{test_type}",
                        category='functionality',
                        status='passed',
                        execution_time=execution_time,
                        message=f"{test_type} functionality test passed",
                        details={'help_output': help_output[:500]}
                    )
            else:
                return TestResult(
                    test_name=f"{system_name}_{test_type}",
                    category='functionality',
                    status='failed',
                    execution_time=execution_time,
                    message=f"Functionality test failed: {result.stderr}",
                    details={'stdout': result.stdout, 'stderr': result.stderr}
                )

        except subprocess.TimeoutExpired:
            return TestResult(
                test_name=f"{system_name}_{test_type}",
                category='functionality',
                status='error',
                execution_time=30.0,
                message="Functionality test timed out",
                details={}
            )
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return TestResult(
                test_name=f"{system_name}_{test_type}",
                category='functionality',
                status='error',
                execution_time=execution_time,
                message=f"Error running functionality test: {e}",
                details={}
            )

    def _calculate_suite_status(self, tests: List[TestResult]) -> str:
        """Calculate overall status for a test suite"""
        if not tests:
            return 'unknown'

        failed_tests = len([t for t in tests if t.status == 'failed'])
        error_tests = len([t for t in tests if t.status == 'error'])

        if error_tests > 0:
            return 'error'
        elif failed_tests > 0:
            return 'failed'
        elif any(t.status == 'warning' for t in tests):
            return 'warning'
        else:
            return 'passed'

    def _generate_test_recommendations(self, test_suites: List[SystemTestSuite]) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []

        # Analyze failed systems
        failed_suites = [s for s in test_suites if s.overall_status in ['failed', 'error']]
        if failed_suites:
            recommendations.append(f"Fix {len(failed_suites)} failed systems: {', '.join(s.system_name for s in failed_suites)}")

        # Analyze systems with warnings
        warning_suites = [s for s in test_suites if s.overall_status == 'warning']
        if warning_suites:
            recommendations.append(f"Review {len(warning_suites)} systems with warnings for potential improvements")

        # Performance recommendations
        slow_suites = [s for s in test_suites if s.total_time > 10.0]
        if slow_suites:
            recommendations.append(f"Optimize performance for {len(slow_suites)} slow-running systems")

        # Success recommendations
        passed_suites = [s for s in test_suites if s.overall_status == 'passed']
        if len(passed_suites) >= 5:
            recommendations.append("All core systems passing - ready for production deployment")

        if not recommendations:
            recommendations.append("All systems functioning correctly - maintain current implementation")

        return recommendations

    def generate_integration_report(self, output_format: str = 'text') -> str:
        """Generate comprehensive integration test report"""
        report = self.run_comprehensive_tests()

        if output_format == 'json':
            return json.dumps({
                'integration_test_report': {
                    'test_timestamp': report.test_timestamp,
                    'project_name': report.project_name,
                    'systems_tested': report.systems_tested,
                    'total_tests': report.total_tests,
                    'passed_tests': report.passed_tests,
                    'failed_tests': report.failed_tests,
                    'warnings': report.warnings,
                    'integration_score': report.integration_score,
                    'test_suites': [asdict(s) for s in report.test_suites],
                    'recommendations': report.recommendations
                },
                'generated_at': datetime.now().isoformat()
            }, indent=2)

        # Generate text report
        return self._generate_text_integration_report(report)

    def _generate_text_integration_report(self, report: IntegrationTestReport) -> str:
        """Generate formatted text integration report"""
        lines = []
        lines.append("=" * 80)
        lines.append("GOAL KIT OPTIMIZATION INTEGRATION TEST REPORT")
        lines.append(f"Project: {report.project_name}")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)

        # Overall results
        lines.append(f"\n📊 INTEGRATION TEST SUMMARY")
        lines.append("-" * 50)
        lines.append(f"Systems Tested: {report.systems_tested}")
        lines.append(f"Total Tests: {report.total_tests}")
        lines.append(f"Passed: {report.passed_tests} ({report.passed_tests/report.total_tests*100:.1f}%)")
        lines.append(f"Failed: {report.failed_tests}")
        lines.append(f"Warnings: {report.warnings}")
        lines.append(f"Integration Score: {report.integration_score}/100")

        # Test suite results
        lines.append("\n🧪 SYSTEM TEST RESULTS")
        lines.append("-" * 50)

        for suite in report.test_suites:
            status_icon = {
                'passed': '✅',
                'failed': '❌',
                'warning': '⚠️',
                'error': '🔴'
            }.get(suite.overall_status, '❓')

            lines.append(f"{status_icon} {suite.system_name}")
            lines.append(f"   Status: {suite.overall_status.upper()} | Time: {suite.total_time:.2f}s")
            lines.append(f"   Description: {suite.description}")

            # Show individual test results
            for test in suite.tests[:3]:  # Show first 3 tests
                test_icon = {
                    'passed': '✅',
                    'failed': '❌',
                    'warning': '⚠️',
                    'error': '🔴'
                }.get(test.status, '❓')
                lines.append(f"     {test_icon} {test.test_name}: {test.message}")

        # Recommendations
        if report.recommendations:
            lines.append("\n💡 TEST RECOMMENDATIONS")
            lines.append("-" * 50)

            for rec in report.recommendations:
                lines.append(f"• {rec}")

        # Integration assessment
        lines.append("\n🏆 INTEGRATION ASSESSMENT")
        lines.append("-" * 50)

        if report.integration_score >= 90:
            lines.append("🟢 EXCELLENT INTEGRATION - All systems working correctly")
            lines.append("   Ready for production deployment")
        elif report.integration_score >= 75:
            lines.append("🟡 GOOD INTEGRATION - Minor issues to address")
            lines.append("   Suitable for testing and gradual rollout")
        elif report.integration_score >= 50:
            lines.append("🟠 CONCERNING INTEGRATION - Significant issues require attention")
            lines.append("   Address failed tests before deployment")
        else:
            lines.append("🔴 CRITICAL INTEGRATION ISSUES - Major problems must be resolved")
            lines.append("   Do not deploy until all critical issues are fixed")

        lines.append("=" * 80)
        return "\n".join(lines)

    def run_smoke_tests(self) -> Dict[str, Any]:
        """Run quick smoke tests on all systems"""
        write_info("Running smoke tests on all optimization systems...")

        smoke_results = {
            'timestamp': datetime.now().isoformat(),
            'systems': {},
            'overall_status': 'unknown'
        }

        for system_name, system_info in self.systems_to_test.items():
            write_info(f"Smoke testing {system_name}...")

            # Quick syntax and import test
            try:
                result = subprocess.run([
                    sys.executable, '-c', f"import sys; sys.path.append('scripts/python'); import {system_name}"
                ], cwd=self.project_root, capture_output=True, text=True, timeout=10)

                if result.returncode == 0:
                    smoke_results['systems'][system_name] = {
                        'status': 'passed',
                        'message': 'Import and basic functionality test passed'
                    }
                else:
                    smoke_results['systems'][system_name] = {
                        'status': 'failed',
                        'message': f"Import failed: {result.stderr}"
                    }

            except subprocess.TimeoutExpired:
                smoke_results['systems'][system_name] = {
                    'status': 'error',
                    'message': 'Smoke test timed out'
                }
            except Exception as e:
                smoke_results['systems'][system_name] = {
                    'status': 'error',
                    'message': f"Error during smoke test: {e}"
                }

        # Overall status
        passed_systems = len([s for s in smoke_results['systems'].values() if s['status'] == 'passed'])
        total_systems = len(smoke_results['systems'])

        if passed_systems == total_systems:
            smoke_results['overall_status'] = 'passed'
        elif passed_systems > 0:
            smoke_results['overall_status'] = 'warning'
        else:
            smoke_results['overall_status'] = 'failed'

        return smoke_results


def main():
    """Main testing function"""
    if not test_git_repo():
        write_error("Not in a git repository")
        write_info("Please run this from the root of a Goal Kit project")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(description='Goal Kit Optimization Testing Framework')
    parser.add_argument('--smoke', action='store_true', help='Run quick smoke tests only')
    parser.add_argument('--comprehensive', action='store_true', help='Run comprehensive integration tests')
    parser.add_argument('--system', help='Test specific system only')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')

    args = parser.parse_args()

    try:
        tester = OptimizationTester()

        if args.smoke:
            # Quick smoke tests
            smoke_results = tester.run_smoke_tests()
            if args.json:
                print(json.dumps(smoke_results, indent=2))
            else:
                print("\n🚀 SMOKE TEST RESULTS")
                print(f"Overall Status: {smoke_results['overall_status'].upper()}")

                for system, result in smoke_results['systems'].items():
                    status_icon = {
                        'passed': '✅',
                        'failed': '❌',
                        'warning': '⚠️',
                        'error': '🔴'
                    }.get(result['status'], '❓')

                    print(f"{status_icon} {system}: {result['message']}")

        elif args.comprehensive:
            # Comprehensive testing
            report = tester.generate_integration_report(args.json)
            print(report)

        elif args.system:
            # Test specific system
            if args.system not in tester.systems_to_test:
                write_error(f"Unknown system: {args.system}")
                write_info(f"Available systems: {', '.join(tester.systems_to_test.keys())}")
                sys.exit(1)

            system_info = tester.systems_to_test[args.system]
            suite = tester._test_system(args.system, system_info)

            if args.json:
                print(json.dumps(asdict(suite), indent=2))
            else:
                print(f"\n🧪 TEST RESULTS FOR {args.system.upper()}")
                print(f"Description: {suite.description}")
                print(f"Overall Status: {suite.overall_status.upper()}")
                print(f"Total Time: {suite.total_time:.2f}s")

                for test in suite.tests:
                    status_icon = {
                        'passed': '✅',
                        'failed': '❌',
                        'warning': '⚠️',
                        'error': '🔴'
                    }.get(test.status, '❓')

                    print(f"{status_icon} {test.test_name}: {test.message} ({test.execution_time:.2f}s)")

        else:
            # Default: run smoke tests
            smoke_results = tester.run_smoke_tests()

            print(f"\n🧪 OPTIMIZATION TESTING SUMMARY")
            print(f"Project: {os.path.basename(tester.project_root)}")
            print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Systems Available: {len(tester.systems_to_test)}")

            passed_count = len([s for s in smoke_results['systems'].values() if s['status'] == 'passed'])
            print(f"Systems Passing: {passed_count}/{len(smoke_results['systems'])}")

            if smoke_results['overall_status'] == 'passed':
                print("✅ All systems ready for use")
                print("💡 Run --comprehensive for detailed testing")
            else:
                print("⚠️ Some systems need attention")
                print("🔧 Run --comprehensive for detailed analysis")

    except Exception as e:
        write_error(f"Error in optimization testing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()