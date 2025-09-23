from typing import Dict

def _generate_gitlab_pipeline(self, pipeline_type: str, config: Dict) -> str:
    """Generate GitLab CI/CD pipeline"""
    project_name = config.get("project_name", "project")

    pipeline = """stages:
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
        pipeline += """
test:
  stage: test
  script:
    - pip install pytest pytest-cov
    - pytest --cov=. --cov-report=xml
  coverage: '/TOTAL.*\\\\s+(\\\\d+%)$/'
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
    - develop
"""

    return pipeline