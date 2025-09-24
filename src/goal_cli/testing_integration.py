"""
Testing Framework Integration for goal-dev-spec
Provides seamless integration with popular testing frameworks and automated test generation.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import subprocess


class TestingFrameworkIntegration:
    """Integrates goal-dev-spec with testing frameworks"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.testing_path = project_path / ".goal" / "testing"
        self.testing_path.mkdir(exist_ok=True)
        
        # Supported frameworks
        self.supported_frameworks: Dict[str, Dict[str, Any]] = {
            "pytest": {
                "config_file": "pytest.ini",
                "test_dir": "tests",
                "command": "pytest",
                "generator": self._generate_pytest_tests
            },
            "unittest": {
                "config_file": "setup.cfg",
                "test_dir": "tests",
                "command": "python -m unittest",
                "generator": self._generate_unittest_tests
            },
            "jest": {
                "config_file": "jest.config.js",
                "test_dir": "__tests__",
                "command": "jest",
                "generator": self._generate_jest_tests
            },
            "mocha": {
                "config_file": "mocha.opts",
                "test_dir": "test",
                "command": "mocha",
                "generator": self._generate_mocha_tests
            }
        }
    
    def detect_testing_framework(self) -> Optional[str]:
        """Detect which testing framework is being used in the project"""
        for framework, config in self.supported_frameworks.items():
            config_path = self.project_path / config["config_file"]
            if config_path.exists():
                return framework
        return None
    
    def setup_testing_framework(self, framework: str = "pytest") -> Dict:
        """Set up testing framework integration"""
        if framework not in self.supported_frameworks:
            return {
                "success": False,
                "error": f"Unsupported framework: {framework}",
                "supported_frameworks": list(self.supported_frameworks.keys())
            }
        
        # Create test directory
        test_dir = self.project_path / self.supported_frameworks[framework]["test_dir"]
        test_dir.mkdir(exist_ok=True)
        
        # Create framework-specific configuration
        config_result = self._create_framework_config(framework)
        
        # Create integration configuration
        integration_config = {
            "framework": framework,
            "test_directory": str(test_dir.relative_to(self.project_path)),
            "config_file": self.supported_frameworks[framework]["config_file"],
            "test_generation": {
                "enabled": True,
                "from_acceptance_criteria": True,
                "from_user_stories": True,
                "templates_dir": str(self.testing_path / "templates"),
                "output_format": "auto"
            },
            "quality_gates": {
                "pre_commit": True,
                "pre_merge": True,
                "release": True
            },
            "coverage": {
                "target": 0.8,
                "enforce": True
            }
        }
        
        # Save integration configuration
        config_file = self.testing_path / f"integration_{framework}.json"
        with open(config_file, 'w') as f:
            json.dump(integration_config, f, indent=2)
        
        return {
            "success": True,
            "framework": framework,
            "config": integration_config,
            "config_result": config_result
        }
    
    def _create_framework_config(self, framework: str) -> Dict:
        """Create framework-specific configuration files"""
        if framework == "pytest":
            return self._create_pytest_config()
        elif framework == "unittest":
            return self._create_unittest_config()
        elif framework == "jest":
            return self._create_jest_config()
        elif framework == "mocha":
            return self._create_mocha_config()
        else:
            return {"success": False, "error": f"No config generator for {framework}"}
    
    def _create_pytest_config(self) -> Dict:
        """Create pytest configuration"""
        config_content = """[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
"""
        
        config_file = self.project_path / "pytest.ini"
        if not config_file.exists():
            with open(config_file, 'w') as f:
                f.write(config_content)
            return {"created": True, "file": str(config_file)}
        else:
            return {"created": False, "file": str(config_file), "reason": "already exists"}
    
    def _create_unittest_config(self) -> Dict:
        """Create unittest configuration"""
        config_content = """[unittest]
test-file-pattern = test_*.py
test-suite-pattern = Test*
"""
        
        config_file = self.project_path / "setup.cfg"
        if not config_file.exists():
            with open(config_file, 'w') as f:
                f.write(config_content)
            return {"created": True, "file": str(config_file)}
        else:
            return {"created": False, "file": str(config_file), "reason": "already exists"}
    
    def _create_jest_config(self) -> Dict:
        """Create Jest configuration"""
        config_content = """module.exports = {
  testEnvironment: 'node',
  testMatch: ['**/__tests__/**/*.js', '**/?(*.)+(spec|test).js'],
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
"""
        
        config_file = self.project_path / "jest.config.js"
        if not config_file.exists():
            with open(config_file, 'w') as f:
                f.write(config_content)
            return {"created": True, "file": str(config_file)}
        else:
            return {"created": False, "file": str(config_file), "reason": "already exists"}
    
    def _create_mocha_config(self) -> Dict:
        """Create Mocha configuration"""
        config_content = """--recursive
--reporter spec
--timeout 5000
"""
        
        config_file = self.project_path / "mocha.opts"
        if not config_file.exists():
            with open(config_file, 'w') as f:
                f.write(config_content)
            return {"created": True, "file": str(config_file)}
        else:
            return {"created": False, "file": str(config_file), "reason": "already exists"}
    
    def generate_tests_from_spec(self, spec_data: Dict, framework: Optional[str] = None) -> Dict:
        """Generate test cases from specification data"""
        if framework is None:
            framework = self.detect_testing_framework() or "pytest"
        
        if framework not in self.supported_frameworks:
            return {
                "success": False,
                "error": f"Unsupported framework: {framework}",
                "supported_frameworks": list(self.supported_frameworks.keys())
            }
        
        # Use framework-specific generator
        generator = self.supported_frameworks[framework]["generator"]
        test_files = generator(spec_data, framework)  # type: ignore[misc]
        
        return {
            "success": True,
            "framework": framework,
            "test_files_created": test_files,
            "spec_id": spec_data.get("id", "unknown")
        }
    
    def _generate_pytest_tests(self, spec_data: Dict, framework: str) -> List[str]:
        """Generate pytest test files"""
        test_files = []
        spec_id = spec_data.get("id", "spec")
        
        # Create test directory for this spec
        spec_test_dir = self.project_path / "tests" / f"test_{spec_id}"
        spec_test_dir.mkdir(exist_ok=True)
        
        # Generate tests from acceptance criteria
        acceptance_tests = self._generate_acceptance_tests_pytest(spec_data, spec_id)
        if acceptance_tests:
            test_file = spec_test_dir / "test_acceptance.py"
            with open(test_file, 'w') as f:
                f.write(acceptance_tests)
            test_files.append(str(test_file.relative_to(self.project_path)))
        
        # Generate tests from user stories
        user_story_tests = self._generate_user_story_tests_pytest(spec_data, spec_id)
        if user_story_tests:
            test_file = spec_test_dir / "test_user_stories.py"
            with open(test_file, 'w') as f:
                f.write(user_story_tests)
            test_files.append(str(test_file.relative_to(self.project_path)))
        
        return test_files
    
    def _generate_acceptance_tests_pytest(self, spec_data: Dict, spec_id: str) -> str:
        """Generate pytest tests from acceptance criteria"""
        test_content = f"""#!/usr/bin/env python3
\"\"\"
Acceptance tests for {spec_data.get('title', spec_id)}
Generated from specification acceptance criteria
\"\"\"

import pytest

# Import the module to be tested
# from your_module import your_function

def test_spec_metadata():
    \"\"\"Test that the specification has proper metadata\"\"\"
    assert "{spec_id}" == "{spec_id}"
    assert "{spec_data.get('title', '')}" != ""

"""
        
        acceptance_criteria = spec_data.get("acceptance_criteria", [])
        for i, criterion in enumerate(acceptance_criteria):
            if isinstance(criterion, str):
                # Create a test for each acceptance criterion
                clean_criterion = "".join(c for c in criterion if c.isalnum() or c.isspace()).split()
                test_name = "_".join(clean_criterion[:5]).lower() if clean_criterion else f"criterion_{i+1}"
                
                test_content += f"""
def test_acceptance_{test_name}():
    \"\"\"Test acceptance criterion: {criterion[:50]}...\"\"\"
    # TODO: Implement test for this acceptance criterion
    # Given [precondition]
    # When [action]
    # Then [expected outcome]
    pytest.skip("Test not yet implemented")
"""
            elif isinstance(criterion, dict):
                test_name = criterion.get("title", f"criterion_{i+1}").replace(" ", "_").lower()
                test_content += f"""
def test_acceptance_{test_name}():
    \"\"\"Test acceptance criterion: {criterion.get('title', f'Criterion {i+1}')}\"\"\"
    # TODO: Implement test for this acceptance criterion
    # Given [precondition]
    # When [action]
    # Then [expected outcome]
    pytest.skip("Test not yet implemented")
"""
        
        return test_content
    
    def _generate_user_story_tests_pytest(self, spec_data: Dict, spec_id: str) -> str:
        """Generate pytest tests from user stories"""
        test_content = f"""#!/usr/bin/env python3
\"\"\"
User story tests for {spec_data.get('title', spec_id)}
Generated from specification user stories
\"\"\"

import pytest

# Import the module to be tested
# from your_module import your_function

"""
        
        user_stories = spec_data.get("user_stories", [])
        for i, story in enumerate(user_stories):
            if isinstance(story, str):
                # Create a test for each user story
                clean_story = "".join(c for c in story if c.isalnum() or c.isspace()).split()
                test_name = "_".join(clean_story[:5]).lower() if clean_story else f"story_{i+1}"
                
                test_content += f"""
def test_user_story_{test_name}():
    \"\"\"Test user story: {story[:50]}...\"\"\"
    # TODO: Implement test for this user story
    # As a [user role]
    # I want [goal]
    # So that [benefit]
    pytest.skip("Test not yet implemented")
"""
            elif isinstance(story, dict):
                test_name = story.get("title", f"story_{i+1}").replace(" ", "_").lower()
                test_content += f"""
def test_user_story_{test_name}():
    \"\"\"Test user story: {story.get('title', f'Story {i+1}')}\"\"\"
    # TODO: Implement test for this user story
    # As a [user role]
    # I want [goal]
    # So that [benefit]
    pytest.skip("Test not yet implemented")
"""
        
        return test_content
    
    def _generate_unittest_tests(self, spec_data: Dict, framework: str) -> List[str]:
        """Generate unittest test files"""
        # Similar implementation for unittest
        test_files = []
        spec_id = spec_data.get("id", "spec")
        
        # Create test directory for this spec
        spec_test_dir = self.project_path / "tests" / f"test_{spec_id}"
        spec_test_dir.mkdir(exist_ok=True)
        
        # Generate a simple unittest file
        test_content = f"""#!/usr/bin/env python3
\"\"\"
Unit tests for {spec_data.get('title', spec_id)}
Generated from specification
\"\"\"

import unittest

class Test{spec_id.replace('-', '_').title()}(unittest.TestCase):
    def test_spec_exists(self):
        \"\"\"Test that the specification exists\"\"\"
        self.assertEqual("{spec_id}", "{spec_id}")

if __name__ == '__main__':
    unittest.main()
"""
        
        test_file = spec_test_dir / f"test_{spec_id}.py"
        with open(test_file, 'w') as f:
            f.write(test_content)
        test_files.append(str(test_file.relative_to(self.project_path)))
        
        return test_files
    
    def _generate_jest_tests(self, spec_data: Dict, framework: str) -> List[str]:
        """Generate Jest test files"""
        test_files = []
        spec_id = spec_data.get("id", "spec")
        
        # Create test directory for this spec
        spec_test_dir = self.project_path / "__tests__" / spec_id
        spec_test_dir.mkdir(exist_ok=True)
        
        # Generate a simple Jest test file
        test_content = f"""/**
 * Tests for {spec_data.get('title', spec_id)}
 * Generated from specification
 */

describe('{spec_id}', () => {{
  test('spec should exist', () => {{
    expect('{spec_id}').toBe('{spec_id}');
  }});
}});
"""
        
        test_file = spec_test_dir / f"{spec_id}.test.js"
        with open(test_file, 'w') as f:
            f.write(test_content)
        test_files.append(str(test_file.relative_to(self.project_path)))
        
        return test_files
    
    def _generate_mocha_tests(self, spec_data: Dict, framework: str) -> List[str]:
        """Generate Mocha test files"""
        test_files = []
        spec_id = spec_data.get("id", "spec")
        
        # Create test directory for this spec
        spec_test_dir = self.project_path / "test" / spec_id
        spec_test_dir.mkdir(exist_ok=True)
        
        # Generate a simple Mocha test file
        test_content = f"""/**
 * Tests for {spec_data.get('title', spec_id)}
 * Generated from specification
 */

const {{ expect }} = require('chai');

describe('{spec_id}', function() {{
  it('spec should exist', function() {{
    expect('{spec_id}').to.equal('{spec_id}');
  }});
}});
"""
        
        test_file = spec_test_dir / f"{spec_id}.js"
        with open(test_file, 'w') as f:
            f.write(test_content)
        test_files.append(str(test_file.relative_to(self.project_path)))
        
        return test_files
    
    def run_tests(self, framework: Optional[str] = None, pattern: Optional[str] = None) -> Dict:
        """Run tests using the configured framework"""
        if framework is None:
            framework = self.detect_testing_framework() or "pytest"
        
        if framework not in self.supported_frameworks:
            return {
                "success": False,
                "error": f"Unsupported framework: {framework}",
                "supported_frameworks": list(self.supported_frameworks.keys())
            }
        
        command = self.supported_frameworks[framework]["command"]
        if pattern:
            command += f" {pattern}"  # type: ignore[operator]
        
        try:
            # Run the test command
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(self.project_path),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return {
                "success": result.returncode == 0,
                "command": command,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "timestamp": datetime.now().isoformat()
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Test execution timed out",
                "command": command,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": command,
                "timestamp": datetime.now().isoformat()
            }
    
    def generate_coverage_report(self, framework: Optional[str] = None) -> Dict:
        """Generate test coverage report"""
        if framework is None:
            framework = self.detect_testing_framework() or "pytest"
        
        # This would depend on the specific framework's coverage tools
        coverage_commands = {
            "pytest": "pytest --cov=. --cov-report=html --cov-report=term",
            "unittest": "coverage run -m unittest && coverage report && coverage html",
            "jest": "jest --coverage",
            "mocha": "nyc npm test"
        }
        
        if framework not in coverage_commands:
            return {
                "success": False,
                "error": f"No coverage command for framework: {framework}"
            }
        
        command = coverage_commands[framework]
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout for coverage
            )
            
            return {
                "success": result.returncode == 0,
                "command": command,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "timestamp": datetime.now().isoformat()
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Coverage report generation timed out",
                "command": command,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": command,
                "timestamp": datetime.now().isoformat()
            }
    
    def integrate_with_ci(self, ci_provider: str = "github") -> Dict:
        """Integrate testing with CI/CD providers"""
        ci_configs = {
            "github": self._generate_github_actions_config,
            "gitlab": self._generate_gitlab_ci_config,
            "jenkins": self._generate_jenkins_config,
            "circleci": self._generate_circleci_config
        }
        
        if ci_provider not in ci_configs:
            return {
                "success": False,
                "error": f"Unsupported CI provider: {ci_provider}",
                "supported_providers": list(ci_configs.keys())
            }
        
        generator = ci_configs[ci_provider]
        config_result = generator()
        
        return {
            "success": True,
            "provider": ci_provider,
            "config_result": config_result
        }
    
    def _generate_github_actions_config(self) -> Dict:
        """Generate GitHub Actions configuration"""
        workflows_dir = self.project_path / ".github" / "workflows"
        workflows_dir.mkdir(exist_ok=True, parents=True)
        
        workflow_content = """name: Test and Validate
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .
        pip install pytest pytest-cov
    
    - name: Run tests with coverage
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
"""
        
        workflow_file = workflows_dir / "test.yml"
        with open(workflow_file, 'w') as f:
            f.write(workflow_content)
        
        return {
            "created": True,
            "file": str(workflow_file.relative_to(self.project_path))
        }
    
    def _generate_gitlab_ci_config(self) -> Dict:
        """Generate GitLab CI configuration"""
        config_content = """stages:
  - test

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - venv/

before_script:
  - python -V
  - pip install virtualenv
  - virtualenv venv
  - source venv/bin/activate
  - pip install -e .
  - pip install pytest pytest-cov

test:
  stage: test
  script:
    - pytest --cov=. --cov-report=xml
  coverage: '/TOTAL.*\\s+(\\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
"""
        
        config_file = self.project_path / ".gitlab-ci.yml"
        if not config_file.exists():
            with open(config_file, 'w') as f:
                f.write(config_content)
            return {
                "created": True,
                "file": str(config_file.relative_to(self.project_path))
            }
        else:
            return {
                "created": False,
                "file": str(config_file.relative_to(self.project_path)),
                "reason": "already exists"
            }
    
    def _generate_jenkins_config(self) -> Dict:
        """Generate Jenkins pipeline configuration"""
        pipeline_content = """pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'python -V'
                sh 'pip install -e .'
                sh 'pip install pytest pytest-cov'
            }
        }
        
        stage('Test') {
            steps {
                sh 'pytest --cov=. --cov-report=xml'
            }
            post {
                always {
                    publishCoverage adapters: [coberturaAdapter(mergeToOneReport: true, path: 'coverage.xml')]
                }
            }
        }
    }
}
"""
        
        pipeline_file = self.project_path / "Jenkinsfile"
        if not pipeline_file.exists():
            with open(pipeline_file, 'w') as f:
                f.write(pipeline_content)
            return {
                "created": True,
                "file": str(pipeline_file.relative_to(self.project_path))
            }
        else:
            return {
                "created": False,
                "file": str(pipeline_file.relative_to(self.project_path)),
                "reason": "already exists"
            }
    
    def _generate_circleci_config(self) -> Dict:
        """Generate CircleCI configuration"""
        circleci_dir = self.project_path / ".circleci"
        circleci_dir.mkdir(exist_ok=True)
        
        config_content = """version: 2.1

orbs:
  python: circleci/python@2.1.1

jobs:
  build-and-test:
    executor: python/default
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
          args: install -e . pytest pytest-cov
      - run:
          name: Run tests
          command: pytest --cov=. --cov-report=xml
      - store_test_results:
          path: test-results
      - store_artifacts:
          path: htmlcov

workflows:
  main:
    jobs:
      - build-and-test
"""
        
        config_file = circleci_dir / "config.yml"
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        return {
            "created": True,
            "file": str(config_file.relative_to(self.project_path))
        }


# CLI Integration
def testing_cli():
    """CLI commands for testing framework integration"""
    import typer
    from rich.console import Console
    
    app = typer.Typer()
    console = Console()
    
    @app.command()
    def setup(framework: str = typer.Option("pytest", help="Testing framework to set up")):
        """Set up testing framework integration"""
        try:
            project_path = Path.cwd()
            # Find project root
            while project_path != project_path.parent:
                if (project_path / ".goal" / "goal.yaml").exists():
                    break
                project_path = project_path.parent
            else:
                console.print("[red]Error:[/red] Not in a goal-dev-spec project")
                return
            
            # Initialize testing integration
            testing_integration = TestingFrameworkIntegration(project_path)
            
            # Set up framework
            result = testing_integration.setup_testing_framework(framework)
            
            if result["success"]:
                console.print(f"[green]✓[/green] Successfully set up {framework} integration")
                console.print(f"Configuration saved to: {result['config_result']['file']}")
            else:
                console.print(f"[red]✗[/red] Failed to set up {framework} integration")
                console.print(f"Error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def detect():
        """Detect testing framework in use"""
        try:
            project_path = Path.cwd()
            # Find project root
            while project_path != project_path.parent:
                if (project_path / ".goal" / "goal.yaml").exists():
                    break
                project_path = project_path.parent
            else:
                console.print("[red]Error:[/red] Not in a goal-dev-spec project")
                return
            
            # Initialize testing integration
            testing_integration = TestingFrameworkIntegration(project_path)
            
            # Detect framework
            framework = testing_integration.detect_testing_framework()
            
            if framework:
                console.print(f"[green]✓[/green] Detected testing framework: {framework}")
            else:
                console.print("[yellow]⚠[/yellow] No testing framework detected")
                console.print("Supported frameworks:", ", ".join(testing_integration.supported_frameworks.keys()))
                
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def run(pattern: str = typer.Option(None, help="Test pattern to run")):
        """Run tests"""
        try:
            project_path = Path.cwd()
            # Find project root
            while project_path != project_path.parent:
                if (project_path / ".goal" / "goal.yaml").exists():
                    break
                project_path = project_path.parent
            else:
                console.print("[red]Error:[/red] Not in a goal-dev-spec project")
                return
            
            # Initialize testing integration
            testing_integration = TestingFrameworkIntegration(project_path)
            
            # Run tests
            result = testing_integration.run_tests(pattern=pattern)
            
            if result["success"]:
                console.print("[green]✓[/green] Tests completed successfully")
                if result["stdout"]:
                    console.print("\n[bold]Output:[/bold]")
                    console.print(result["stdout"])
            else:
                console.print("[red]✗[/red] Tests failed")
                if result["stdout"]:
                    console.print("\n[bold]Output:[/bold]")
                    console.print(result["stdout"])
                if result["stderr"]:
                    console.print("\n[bold]Errors:[/bold]")
                    console.print(result["stderr"])
                
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    return app


# Integration with main CLI
def integrate_testing_with_main_cli(main_app):
    """Integrate testing commands with main CLI"""
    testing_app = testing_cli()
    main_app.add_typer(testing_app, name="test")
    return main_app