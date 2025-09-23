# Extract just the Jenkins function to isolate the issue
from typing import Dict

def _generate_jenkins_pipeline(self, pipeline_type: str, config: Dict) -> str:
    """Generate Jenkins pipeline"""
    project_name = config.get("project_name", "project")
    
    pipeline = """pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'python -V'
                sh 'pip install -e .'
"""
    
    if pipeline_type == "ci" or pipeline_type == "cicd":
        pipeline += """
                sh 'pip install pytest pytest-cov'
"""
    
    pipeline += """
            }
"""
    
    if pipeline_type == "ci" or pipeline_type == "cicd":
        pipeline += """
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
    
    pipeline += """
     }
 }"""
    
    return pipeline