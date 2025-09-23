"""
Continuous Integration and Deployment Pipelines for goal-dev-spec
Exceeds spec-kit functionality with sophisticated CI/CD pipeline management.
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib


@dataclass
class PipelineRequest:
    """Data class for CI/CD pipeline requests"""
    id: str
    pipeline_type: str  # ci, cd, cicd
    provider: str  # github, gitlab, jenkins, circleci, travis, azure
    config_path: str
    created_at: str
    status: str = "pending"
    result: Optional[str] = None
    error: Optional[str] = None


class CICDPipelineManager:
    """CI/CD pipeline management system"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.ci_path = project_path / ".goal" / "ci"
        self.ci_path.mkdir(exist_ok=True)
        
        # Pipeline requests storage
        self.pipeline_requests_file = self.ci_path / "pipeline_requests.json"
        self.pipeline_requests = self._load_pipeline_requests()
        
        # Supported CI/CD providers
        self.supported_providers = {
            "github": {
                "name": "GitHub Actions",
                "config_dir": ".github/workflows",
                "file_extension": ".yml"
            },
            "gitlab": {
                "name": "GitLab CI/CD",
                "config_file": ".gitlab-ci.yml",
                "file_extension": ".yml"
            },
            "jenkins": {
                "name": "Jenkins",
                "config_file": "Jenkinsfile",
                "file_extension": ""
            },
            "circleci": {
                "name": "CircleCI",
                "config_dir": ".circleci",
                "file_extension": ".yml"
            },
            "travis": {
                "name": "Travis CI",
                "config_file": ".travis.yml",
                "file_extension": ".yml"
            },
            "azure": {
                "name": "Azure Pipelines",
                "config_file": "azure-pipelines.yml",
                "file_extension": ".yml"
            }
        }
        
        # Supported pipeline types
        self.supported_pipeline_types = {
            "ci": "Continuous Integration",
            "cd": "Continuous Deployment",
            "cicd": "CI/CD Pipeline"
        }
    
    def _load_pipeline_requests(self) -> Dict[str, PipelineRequest]:
        """Load pipeline requests from file"""
        if self.pipeline_requests_file.exists():
            try:
                with open(self.pipeline_requests_file, 'r') as f:
                    data = json.load(f)
                requests = {}
                for req_data in data:
                    req_data['status'] = req_data.get('status', 'pending')
                    request = PipelineRequest(**req_data)
                    requests[request.id] = request
                return requests
            except Exception as e:
                print(f"Warning: Could not load pipeline requests: {e}")
        return {}
    
    def _save_pipeline_requests(self):
        """Save pipeline requests to file"""
        data = [asdict(req) for req in self.pipeline_requests.values()]
        with open(self.pipeline_requests_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_pipeline(self, pipeline_type: str, provider: str, 
                       config_path: str = None, pipeline_config: Dict = None) -> str:
        """
        Create a CI/CD pipeline configuration
        
        Args:
            pipeline_type: Type of pipeline (ci, cd, cicd)
            provider: CI/CD provider (github, gitlab, jenkins, circleci, travis, azure)
            config_path: Path where to save the pipeline configuration
            pipeline_config: Custom pipeline configuration
            
        Returns:
            ID of the pipeline request
        """
        # Validate pipeline type
        if pipeline_type not in self.supported_pipeline_types:
            raise ValueError(f"Unsupported pipeline type: {pipeline_type}")
        
        # Validate provider
        if provider not in self.supported_providers:
            raise ValueError(f"Unsupported provider: {provider}")
        
        # Create pipeline request
        request_id = hashlib.md5(f"{pipeline_type}_{provider}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        if config_path is None:
            # Generate default config path based on provider
            provider_info = self.supported_providers[provider]
            if "config_dir" in provider_info:
                config_path = f"{provider_info['config_dir']}/{pipeline_type}_pipeline{provider_info['file_extension']}"
            else:
                config_path = f"{provider_info['config_file']}"
        
        request = PipelineRequest(
            id=request_id,
            pipeline_type=pipeline_type,
            provider=provider,
            config_path=config_path,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.pipeline_requests[request_id] = request
        self._save_pipeline_requests()
        
        # Process request
        self._process_pipeline_request(request_id, pipeline_config or {})
        
        return request_id
    
    def _process_pipeline_request(self, request_id: str, pipeline_config: Dict):
        """Process a pipeline request"""
        if request_id not in self.pipeline_requests:
            return
        
        request = self.pipeline_requests[request_id]
        request.status = "processing"
        self._save_pipeline_requests()
        
        try:
            # Generate pipeline configuration based on provider and type
            if request.provider == "github":
                pipeline_content = self._generate_github_pipeline(request.pipeline_type, pipeline_config)
            elif request.provider == "gitlab":
                pipeline_content = self._generate_gitlab_pipeline(request.pipeline_type, pipeline_config)
            elif request.provider == "jenkins":
                pipeline_content = self._generate_jenkins_pipeline(request.pipeline_type, pipeline_config)
            elif request.provider == "circleci":
                pipeline_content = self._generate_circleci_pipeline(request.pipeline_type, pipeline_config)
            elif request.provider == "travis":
                pipeline_content = self._generate_travis_pipeline(request.pipeline_type, pipeline_config)
            elif request.provider == "azure":
                pipeline_content = self._generate_azure_pipeline(request.pipeline_type, pipeline_config)
            else:
                # Generic pipeline
                pipeline_content = self._generate_generic_pipeline(request.pipeline_type, pipeline_config)
            
            # Save pipeline configuration to file
            config_file = self.project_path / request.config_path
            config_file.parent.mkdir(exist_ok=True, parents=True)
            
            with open(config_file, 'w') as f:
                f.write(pipeline_content)
            
            # Update request
            request.status = "completed"
            request.result = pipeline_content
            
        except Exception as e:
            request.status = "failed"
            request.error = str(e)
        
        self._save_pipeline_requests()
    
    def _generate_github_pipeline(self, pipeline_type: str, config: Dict) -> str:
        """Generate GitHub Actions pipeline"""
        project_name = config.get("project_name", "project")
        
        if pipeline_type == "ci" or pipeline_type == "cicd":
            pipeline = f"""name: CI Pipeline for {project_name}

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

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
    
    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
"""
            
            if pipeline_type == "cicd":
                pipeline += f"""
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Deploying {project_name} to production"
        # Add deployment commands here
"""
        
        elif pipeline_type == "cd":
            pipeline = f"""name: CD Pipeline for {project_name}

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Deploying {project_name} to production"
        # Add deployment commands here
"""
        
        else:
            pipeline = f"""name: {pipeline_type.upper()} Pipeline for {project_name}

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .
    
    - name: Run checks
      run: |
        # Add your checks here
        echo "Pipeline executed successfully"
"""
        
        return pipeline
    
    def _generate_gitlab_pipeline(self, pipeline_type: str, config: Dict) -> str:
        """Generate GitLab CI/CD pipeline"""
        project_name = config.get("project_name", "project")
        
        pipeline = f"""stages:
  - test
  - deploy

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
"""
        
        if pipeline_type == "ci" or pipeline_type == "cicd":
            pipeline += f"""
test:
  stage: test
  script:
    - pip install pytest pytest-cov
    - pytest --cov=. --cov-report=xml
  coverage: '/TOTAL.*\\s+(\\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
"""
        
        if pipeline_type == "cd" or pipeline_type == "cicd":
            pipeline += f"""
deploy:
  stage: deploy
  script:
    - echo "Deploying {project_name} to production"
    # Add deployment commands here
  only:
    - main
"""
        
        return pipeline
    
    def _generate_jenkins_pipeline(self, pipeline_type: str, config: Dict) -> str:
        """Generate Jenkins pipeline"""
        project_name = config.get("project_name", "project")
        
        pipeline = f"""pipeline {{
    agent any
    
    stages {{
        stage('Setup') {{
            steps {{
                sh 'python -V'
                sh 'pip install -e .'
"""
        
        if pipeline_type == "ci" or pipeline_type == "cicd":
            pipeline += f"""
                sh 'pip install pytest pytest-cov'
"""
        
        pipeline += f"""
            }}
        }}
"""
        
        if pipeline_type == "ci" or pipeline_type == "cicd":
            pipeline += f"""
        stage('Test') {{
            steps {{
                sh 'pytest --cov=. --cov-report=xml'
            }}
            post {{
                always {{
                    publishCoverage adapters: [coberturaAdapter(mergeToOneReport: true, path: 'coverage.xml')]
                }}
            }}
        }}
"""
        
        if pipeline_type == "cd" or pipeline_type == "cicd":
            pipeline += f"""
        stage('Deploy') {{
            steps {{
                sh 'echo "Deploying {project_name} to production"'
                // Add deployment commands here
            }}
        }}
"""
        
        pipeline += f"""
    }}
}}"""
        
        return pipeline
    
    def _generate_circleci_pipeline(self, pipeline_type: str, config: Dict) -> str:
        """Generate CircleCI pipeline"""
        project_name = config.get("project_name", "project")
        
        pipeline = f"""version: 2.1

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
"""
        
        if pipeline_type == "ci" or pipeline_type == "cicd":
            pipeline += f"""
      - run:
          name: Run tests
          command: pytest --cov=. --cov-report=xml
      - store_test_results:
          path: test-results
      - store_artifacts:
          path: htmlcov
"""
        
        if pipeline_type == "cd" or pipeline_type == "cicd":
            pipeline += f"""
  deploy:
    executor: python/default
    steps:
      - checkout
      - run:
          name: Deploy to production
          command: |
            echo "Deploying {project_name} to production"
            # Add deployment commands here
"""
        
        pipeline += f"""
workflows:
  main:
    jobs:
      - build-and-test
"""
        
        if pipeline_type == "cd" or pipeline_type == "cicd":
            pipeline += f"""
      - deploy:
          requires:
            - build-and-test
          filters:
            branches:
              only: main
"""
        
        return pipeline
    
    def _generate_travis_pipeline(self, pipeline_type: str, config: Dict) -> str:
        """Generate Travis CI pipeline"""
        project_name = config.get("project_name", "project")
        
        pipeline = f"""language: python
python:
  - "3.8"
  - "3.9"
  - "3.10"

install:
  - pip install -e .
"""
        
        if pipeline_type == "ci" or pipeline_type == "cicd":
            pipeline += f"""
  - pip install pytest pytest-cov

script:
  - pytest --cov=. --cov-report=xml
"""
        
        if pipeline_type == "cd" or pipeline_type == "cicd":
            pipeline += f"""
deploy:
  provider: script
  script: echo "Deploying {project_name} to production"
  on:
    branch: main
"""
        
        return pipeline
    
    def _generate_azure_pipeline(self, pipeline_type: str, config: Dict) -> str:
        """Generate Azure Pipelines"""
        project_name = config.get("project_name", "project")
        
        pipeline = f"""trigger:
- main
- develop

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.10'
    addToPath: true

- script: |
    python -m pip install --upgrade pip
    pip install -e .
  displayName: 'Install dependencies'
"""
        
        if pipeline_type == "ci" or pipeline_type == "cicd":
            pipeline += f"""
- script: |
    pip install pytest pytest-cov
    pytest --cov=. --cov-report=xml
  displayName: 'Run tests'
"""
        
        if pipeline_type == "cd" or pipeline_type == "cicd":
            pipeline += f"""
- script: |
    echo "Deploying {project_name} to production"
    # Add deployment commands here
  displayName: 'Deploy to production'
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
"""
        
        return pipeline
    
    def _generate_generic_pipeline(self, pipeline_type: str, config: Dict) -> str:
        """Generate generic pipeline"""
        return f"""# {pipeline_type.upper()} Pipeline Configuration

# This is a generic pipeline configuration
# In a real implementation, this would be provider-specific

pipeline_type: {pipeline_type}
created_at: {datetime.now().isoformat()}
configuration:
  # Add your pipeline configuration here
  steps:
    - setup
    - test
    - deploy
"""
    
    def get_pipeline_status(self, request_id: str) -> Optional[Dict]:
        """Get the status of a pipeline request"""
        if request_id in self.pipeline_requests:
            request = self.pipeline_requests[request_id]
            return asdict(request)
        return None
    
    def list_pipeline_requests(self) -> List[Dict]:
        """List all pipeline requests"""
        return [asdict(req) for req in self.pipeline_requests.values()]
    
    def generate_standard_pipelines(self, providers: List[str] = None, 
                                  pipeline_types: List[str] = None) -> List[str]:
        """
        Generate standard CI/CD pipelines for common providers
        
        Args:
            providers: List of providers to generate pipelines for
            pipeline_types: List of pipeline types to generate
            
        Returns:
            List of generated pipeline request IDs
        """
        if providers is None:
            providers = list(self.supported_providers.keys())
        
        if pipeline_types is None:
            pipeline_types = list(self.supported_pipeline_types.keys())
        
        request_ids = []
        
        # Extract project information
        project_info = self._extract_project_info()
        
        # Generate pipelines for each provider and type combination
        for provider in providers:
            if provider not in self.supported_providers:
                continue
                
            for pipeline_type in pipeline_types:
                if pipeline_type not in self.supported_pipeline_types:
                    continue
                
                try:
                    # Create pipeline
                    request_id = self.create_pipeline(
                        pipeline_type,
                        provider,
                        pipeline_config={
                            "project_name": project_info.get("name", "Project"),
                            "project_description": project_info.get("description", "Project description")
                        }
                    )
                    request_ids.append(request_id)
                except Exception as e:
                    print(f"Warning: Could not generate {pipeline_type} pipeline for {provider}: {e}")
        
        return request_ids
    
    def _extract_project_info(self) -> Dict:
        """Extract project information from configuration files"""
        info = {
            "name": "Project",
            "description": "Project description",
            "version": "0.1.0"
        }
        
        # Try to read from goal.yaml
        goal_yaml = self.project_path / ".goal" / "goal.yaml"
        if goal_yaml.exists():
            try:
                with open(goal_yaml, 'r') as f:
                    goal_config = yaml.safe_load(f)
                if "project" in goal_config:
                    project_info = goal_config["project"]
                    info["name"] = project_info.get("name", info["name"])
                    info["description"] = project_info.get("description", info["description"])
                    info["version"] = project_info.get("version", info["version"])
            except Exception:
                pass
        
        # Try to read from pyproject.toml
        pyproject_toml = self.project_path / "pyproject.toml"
        if pyproject_toml.exists():
            try:
                import toml
                with open(pyproject_toml, 'r') as f:
                    pyproject_config = toml.load(f)
                if "project" in pyproject_config:
                    project_info = pyproject_config["project"]
                    info["name"] = project_info.get("name", info["name"])
                    info["description"] = project_info.get("description", info["description"])
                    info["version"] = project_info.get("version", info["version"])
            except Exception:
                pass
        
        return info
    
    def validate_pipeline(self, config_path: str) -> Dict:
        """
        Validate a pipeline configuration
        
        Args:
            config_path: Path to pipeline configuration file
            
        Returns:
            Validation results
        """
        config_file = self.project_path / config_path
        if not config_file.exists():
            return {
                "valid": False,
                "errors": [f"Configuration file not found: {config_path}"]
            }
        
        try:
            # Try to parse the configuration based on file extension
            if config_file.suffix in [".yml", ".yaml"]:
                with open(config_file, 'r') as f:
                    yaml.safe_load(f)
            elif config_file.name == "Jenkinsfile":
                # For Jenkinsfile, we could do more sophisticated validation
                with open(config_file, 'r') as f:
                    content = f.read()
                    if "pipeline" not in content:
                        return {
                            "valid": False,
                            "errors": ["Jenkinsfile does not contain 'pipeline' block"]
                        }
            
            return {
                "valid": True,
                "message": "Pipeline configuration is valid"
            }
        except Exception as e:
            return {
                "valid": False,
                "errors": [str(e)]
            }


# CLI Integration
def cicd_cli():
    """CLI commands for CI/CD pipeline management"""
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    app = typer.Typer()
    console = Console()
    
    @app.command()
    def create(
        type: str = typer.Argument(..., help="Pipeline type (ci, cd, cicd)"),
        provider: str = typer.Argument(..., help="CI/CD provider (github, gitlab, jenkins, circleci, travis, azure)"),
        config: str = typer.Option(None, help="Configuration file path"),
        vars: str = typer.Option("", help="Pipeline variables as JSON string")
    ):
        """Create a CI/CD pipeline configuration"""
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
            
            # Parse pipeline variables
            pipeline_vars = {}
            if vars:
                try:
                    pipeline_vars = json.loads(vars)
                except json.JSONDecodeError as e:
                    console.print(f"[red]Error parsing pipeline variables: {e}[/red]")
                    return
            
            # Initialize CI/CD manager
            cicd_manager = CICDPipelineManager(project_path)
            
            # Create pipeline
            request_id = cicd_manager.create_pipeline(type, provider, config, pipeline_vars)
            
            console.print(f"[green]✓[/green] CI/CD pipeline creation request created with ID: {request_id}")
            console.print(f"Check status with: goal cicd status {request_id}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def status(request_id: str = typer.Argument(..., help="Request ID")):
        """Check the status of a pipeline creation request"""
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
            
            # Initialize CI/CD manager
            cicd_manager = CICDPipelineManager(project_path)
            
            # Check status
            status = cicd_manager.get_pipeline_status(request_id)
            if status:
                console.print(Panel(f"[bold]CI/CD Pipeline Creation Status: {request_id}[/bold]", expand=False))
                console.print(f"Type: {status['pipeline_type']}")
                console.print(f"Provider: {status['provider']}")
                console.print(f"Status: {status['status']}")
                console.print(f"Config Path: {status['config_path']}")
                if status.get('error'):
                    console.print(f"[red]Error:[/red] {status['error']}")
            else:
                console.print(f"[red]Request {request_id} not found[/red]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def list():
        """List all pipeline creation requests"""
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
            
            # Initialize CI/CD manager
            cicd_manager = CICDPipelineManager(project_path)
            
            # List requests
            requests = cicd_manager.list_pipeline_requests()
            if requests:
                console.print(Panel(f"[bold]CI/CD Pipeline Requests ({len(requests)})[/bold]", expand=False))
                
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("ID", style="cyan")
                table.add_column("Type", style="green")
                table.add_column("Provider", style="yellow")
                table.add_column("Status", style="blue")
                table.add_column("Config Path", style="dim")
                table.add_column("Created", style="dim")
                
                for req in requests:
                    created = datetime.fromisoformat(req['created_at']).strftime("%Y-%m-%d %H:%M")
                    table.add_row(
                        req['id'][:8],
                        req['pipeline_type'],
                        req['provider'],
                        req['status'],
                        req['config_path'][:20] + "..." if len(req['config_path']) > 20 else req['config_path'],
                        created
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No pipeline requests found[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def standard(
        providers: str = typer.Option("", help="Comma-separated list of providers (github,gitlab,jenkins,circleci,travis,azure)"),
        types: str = typer.Option("", help="Comma-separated list of types (ci,cd,cicd)")
    ):
        """Generate standard CI/CD pipelines for common providers"""
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
            
            # Parse providers and types
            provider_list = [p.strip() for p in providers.split(",") if p.strip()] if providers else None
            type_list = [t.strip() for t in types.split(",") if t.strip()] if types else None
            
            # Initialize CI/CD manager
            cicd_manager = CICDPipelineManager(project_path)
            
            # Generate standard pipelines
            request_ids = cicd_manager.generate_standard_pipelines(provider_list, type_list)
            
            console.print(f"[green]✓[/green] Generated {len(request_ids)} standard pipelines:")
            for req_id in request_ids:
                status = cicd_manager.get_pipeline_status(req_id)
                if status:
                    console.print(f"  - {status['config_path']} ({status['provider']}/{status['pipeline_type']}): {status['status']}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def validate(config_path: str = typer.Argument(..., help="Path to pipeline configuration file")):
        """Validate a pipeline configuration"""
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
            
            # Initialize CI/CD manager
            cicd_manager = CICDPipelineManager(project_path)
            
            # Validate pipeline
            result = cicd_manager.validate_pipeline(config_path)
            
            if result["valid"]:
                console.print(f"[green]✓[/green] Pipeline configuration is valid")
                console.print(f"[dim]{result.get('message', 'No additional information')}[/dim]")
            else:
                console.print(f"[red]✗[/red] Pipeline configuration is invalid")
                for error in result.get("errors", []):
                    console.print(f"[red]  - {error}[/red]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    return app


# Integration with main CLI
def integrate_cicd_with_main_cli(main_app):
    """Integrate CI/CD pipeline commands with main CLI"""
    cicd_app = cicd_cli()
    main_app.add_typer(cicd_app, name="cicd")
    return main_app