"""
Advanced Project Scaffolding for goal-dev-spec
Exceeds spec-kit functionality with intelligent project structure generation.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Union, cast
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib


@dataclass
class ScaffoldingRequest:
    """Data class for project scaffolding requests"""
    id: str
    template: str
    project_name: str
    output_path: str
    created_at: str
    status: str = "pending"
    result: Optional[Dict] = None
    error: Optional[str] = None


class ProjectScaffolder:
    """Advanced project scaffolding system"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.scaffold_path = project_path / ".goal" / "scaffolding"
        self.scaffold_path.mkdir(exist_ok=True, parents=True)
        
        # Scaffolding requests storage
        self.scaffolding_requests_file = self.scaffold_path / "scaffolding_requests.json"
        self.scaffolding_requests = self._load_scaffolding_requests()
        
        # Template directory
        self.templates_path = project_path / "templates" / "scaffolding"
        self.templates_path.mkdir(exist_ok=True, parents=True)
        
        # Initialize with default templates if they don't exist
        self._initialize_default_templates()
        
        # Supported project templates
        self.supported_templates = {
            "python_basic": {
                "name": "Basic Python Project",
                "description": "A simple Python project structure",
                "language": "python"
            },
            "python_web": {
                "name": "Python Web Application",
                "description": "A web application with Flask/FastAPI",
                "language": "python"
            },
            "python_ml": {
                "name": "Python Machine Learning",
                "description": "A machine learning project with scikit-learn",
                "language": "python"
            },
            "node_basic": {
                "name": "Basic Node.js Project",
                "description": "A simple Node.js project structure",
                "language": "javascript"
            },
            "node_web": {
                "name": "Node.js Web Application",
                "description": "A web application with Express.js",
                "language": "javascript"
            },
            "react_app": {
                "name": "React Application",
                "description": "A React.js frontend application",
                "language": "javascript"
            },
            "vue_app": {
                "name": "Vue.js Application",
                "description": "A Vue.js frontend application",
                "language": "javascript"
            },
            "java_basic": {
                "name": "Basic Java Project",
                "description": "A simple Java project structure",
                "language": "java"
            },
            "java_spring": {
                "name": "Java Spring Boot",
                "description": "A Spring Boot web application",
                "language": "java"
            },
            "go_basic": {
                "name": "Basic Go Project",
                "description": "A simple Go project structure",
                "language": "go"
            },
            "go_web": {
                "name": "Go Web Application",
                "description": "A web application with Gin/Echo",
                "language": "go"
            }
        }

    def _sanitize_path(self, path: str) -> str:
        """Sanitize a path by removing or replacing invalid characters"""
        if not path:
            return path

        # Remove control characters except tab, newline, carriage return
        sanitized = ''.join(c for c in path if ord(c) >= 32 or c in '\t\n\r')

        # Log if sanitization occurred
        if sanitized != path:
            print(f"DEBUG: Sanitized path from {repr(path)} to {repr(sanitized)}")

        return sanitized

    def _validate_path(self, path: str) -> bool:
        """Validate if a path contains only valid characters"""
        invalid_chars = [c for c in path if ord(c) < 32 and c not in '\t\n\r']
        if invalid_chars:
            print(f"ERROR: Path contains invalid characters: {repr(invalid_chars)} in {repr(path)}")
            return False
        return True
    
    def _load_scaffolding_requests(self) -> Dict[str, ScaffoldingRequest]:
        """Load scaffolding requests from file"""
        if self.scaffolding_requests_file.exists():
            try:
                with open(self.scaffolding_requests_file, 'r') as f:
                    data = json.load(f)
                requests = {}
                for req_data in data:
                    req_data['status'] = req_data.get('status', 'pending')

                    # Log output_path for debugging
                    output_path = req_data.get('output_path', '')
                    print(f"DEBUG: Loading request with output_path: {repr(output_path)}")
                    if '\x07' in output_path:
                        print(f"ERROR: Found bell character in output_path: {output_path!r}")
                        # Sanitize the output_path by removing invalid characters
                        req_data['output_path'] = ''.join(c for c in output_path if ord(c) >= 32 or c in '\t\n\r')

                    # Convert result back to dict if it's a string
                    if isinstance(req_data.get('result'), str):
                        result_str = req_data['result']
                        print(f"DEBUG: Parsing result JSON: {repr(result_str[:100])}")
                        if '\x07' in result_str:
                            print("ERROR: Found bell character in result JSON")
                            req_data['result'] = None
                        else:
                            try:
                                req_data['result'] = json.loads(result_str)
                            except json.JSONDecodeError:
                                req_data['result'] = None

                    request = ScaffoldingRequest(**req_data)
                    requests[request.id] = request
                return requests
            except Exception as e:
                print(f"Warning: Could not load scaffolding requests: {e}")
        return {}
    
    def _save_scaffolding_requests(self):
        """Save scaffolding requests to file"""
        # Convert result to string if it's a dict for JSON serialization
        data = []
        for req in self.scaffolding_requests.values():
            req_dict = asdict(req)
            if isinstance(req_dict.get('result'), dict):
                req_dict['result'] = json.dumps(req_dict['result'])
            data.append(req_dict)
        
        with open(self.scaffolding_requests_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _initialize_default_templates(self):
        """Initialize default project templates"""
        # Python basic template
        python_basic_template = self.templates_path / "python_basic"
        if not python_basic_template.exists():
            python_basic_template.mkdir(exist_ok=True)
            
            # Create template structure
            (python_basic_template / "src").mkdir(exist_ok=True)
            (python_basic_template / "tests").mkdir(exist_ok=True)
            
            # Create template files
            with open(python_basic_template / "README.md", 'w') as f:
                f.write("""# {project_name}

{project_description}

## Installation

```bash
pip install -e .
```

## Usage

```python
from src.{project_slug} import main

if __name__ == "__main__":
    main()
```
""")
            
            with open(python_basic_template / "setup.py", 'w') as f:
                f.write("""from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="{project_slug}",
    version="0.1.0",
    author="{author}",
    author_email="{email}",
    description="{project_description}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[],
)
""")
            
            with open(python_basic_template / "src" / "__init__.py", 'w') as f:
                f.write('"""{project_name} package."""\n')
            
            with open(python_basic_template / "src" / "main.py", 'w') as f:
                f.write('''"""Main module for {project_name}."""

def main():
    """Main function."""
    print("Hello from {project_name}!")

if __name__ == "__main__":
    main()
''')
            
            with open(python_basic_template / "tests" / "__init__.py", 'w') as f:
                f.write('"""Test package for {project_name}."""\n')
            
            with open(python_basic_template / "tests" / "test_main.py", 'w') as f:
                f.write('''"""Tests for main module."""

import unittest
from src.{project_slug} import main

class TestMain(unittest.TestCase):
    """Test cases for main function."""
    
    def test_main(self):
        """Test main function."""
        # This is a simple test that just verifies the function exists
        self.assertTrue(callable(main))

if __name__ == "__main__":
    unittest.main()
''')
            
            with open(python_basic_template / "requirements.txt", 'w') as f:
                f.write("# Project dependencies\n")
        
        # Python web template
        python_web_template = self.templates_path / "python_web"
        if not python_web_template.exists():
            python_web_template.mkdir(exist_ok=True)
            
            # Create template structure
            (python_web_template / "src").mkdir(exist_ok=True)
            (python_web_template / "src" / "api").mkdir(exist_ok=True)
            (python_web_template / "src" / "models").mkdir(exist_ok=True)
            (python_web_template / "src" / "schemas").mkdir(exist_ok=True)
            (python_web_template / "tests").mkdir(exist_ok=True)
            
            # Create template files
            with open(python_web_template / "README.md", 'w') as f:
                f.write("""# {project_name}

{project_description}

## Installation

```bash
pip install -e .
```

## Running the Application

```bash
python -m src.{project_slug}
```

## API Documentation

API documentation is available at `/docs` when the application is running.
""")
            
            with open(python_web_template / "setup.py", 'w') as f:
                f.write("""from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="{project_slug}",
    version="0.1.0",
    author="{author}",
    author_email="{email}",
    description="{project_description}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.0"
    ],
)
""")
            
            with open(python_web_template / "src" / "__init__.py", 'w') as f:
                f.write('"""{project_name} web application package."""\n')
            
            with open(python_web_template / "src" / "main.py", 'w') as f:
                f.write('''"""Main application module for {project_name}."""

from fastapi import FastAPI

app = FastAPI(title="{project_name}", description="{project_description}")

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to {project_name}!"}

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
''')
            
            with open(python_web_template / "src" / "api" / "__init__.py", 'w') as f:
                f.write('"""API endpoints for {project_name}."""\n')
            
            with open(python_web_template / "src" / "models" / "__init__.py", 'w') as f:
                f.write('"""Data models for {project_name}."""\n')
            
            with open(python_web_template / "src" / "schemas" / "__init__.py", 'w') as f:
                f.write('"""Pydantic schemas for {project_name}."""\n')
            
            with open(python_web_template / "tests" / "__init__.py", 'w') as f:
                f.write('"""Test package for {project_name}."""\n')
            
            with open(python_web_template / "requirements.txt", 'w') as f:
                f.write("# Web application dependencies\nfastapi>=0.68.0\nuvicorn>=0.15.0\npydantic>=1.8.0\n")
        
        # React app template
        react_template = self.templates_path / "react_app"
        if not react_template.exists():
            react_template.mkdir(exist_ok=True)
            
            # Create template structure
            (react_template / "src").mkdir(exist_ok=True)
            (react_template / "src" / "components").mkdir(exist_ok=True)
            
            # Create template files
            with open(react_template / "README.md", 'w') as f:
                f.write("""# {project_name}

{project_description}

## Installation

```bash
npm install
```

## Running the Application

```bash
npm start
```

## Building for Production

```bash
npm run build
```
""")
            
            with open(react_template / "package.json", 'w') as f:
                f.write('''{
  "name": "{project_slug}",
  "version": "0.1.0",
  "description": "{project_description}",
  "main": "src/index.js",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
''')
            
            with open(react_template / "src" / "index.js", 'w') as f:
                f.write('''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
''')
            
            with open(react_template / "src" / "App.js", 'w') as f:
                f.write('''import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to {project_name}</h1>
        <p>{project_description}</p>
      </header>
    </div>
  );
}

export default App;
''')
            
            with open(react_template / "src" / "App.css", 'w') as f:
                f.write('''.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
}
''')
    
    def scaffold_project(self, template: str, project_name: str,
                        output_path: Optional[str] = None, template_vars: Optional[Dict] = None) -> str:
        """
        Scaffold a new project from a template
        
        Args:
            template: Template to use for scaffolding
            project_name: Name of the new project
            output_path: Path where to create the project
            template_vars: Variables to substitute in the template
            
        Returns:
            ID of the scaffolding request
        """
        # Validate template
        if template not in self.supported_templates:
            raise ValueError(f"Unsupported template: {template}")
        
        # Create scaffolding request
        request_id = hashlib.md5(f"{template}_{project_name}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        if output_path is None:
            # Generate default output path
            output_path = project_name
        
        request = ScaffoldingRequest(
            id=request_id,
            template=template,
            project_name=project_name,
            output_path=output_path,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.scaffolding_requests[request_id] = request
        self._save_scaffolding_requests()
        
        # Process request
        self._process_scaffolding_request(request_id, template_vars or {})
        
        return request_id
    
    def _process_scaffolding_request(self, request_id: str, template_vars: Dict):
        """Process a scaffolding request"""
        if request_id not in self.scaffolding_requests:
            return

        request = self.scaffolding_requests[request_id]
        request.status = "processing"
        self._save_scaffolding_requests()

        try:
            # Sanitize and validate output_path
            output_path = self._sanitize_path(request.output_path)
            print(f"DEBUG: Processing request with output_path: {repr(output_path)}")

            # Validate the path
            if not self._validate_path(output_path):
                raise ValueError(f"Invalid characters found in path: {output_path!r}")

            # Create project directory with sanitized path
            project_dir = self.project_path / output_path
            print(f"DEBUG: Creating directory: {project_dir}")

            # Additional validation before creating directory
            try:
                project_dir.mkdir(exist_ok=True, parents=True)
                print(f"DEBUG: Successfully created directory: {project_dir}")
            except OSError as e:
                print(f"ERROR: Failed to create directory {project_dir}: {e}")
                raise
            
            # Get template directory
            template_dir = self.templates_path / request.template
            
            # Copy template files
            if template_dir.exists():
                result = self._copy_template(template_dir, project_dir, request, template_vars)
            else:
                # Create a basic project structure
                result = self._create_basic_structure(project_dir, request, template_vars)
            
            # Update request
            request.status = "completed"
            request.result = result
            
        except Exception as e:
            request.status = "failed"
            request.error = str(e)
        
        self._save_scaffolding_requests()
    
    def _copy_template(self, template_dir: Path, project_dir: Path,
                      request: ScaffoldingRequest, template_vars: Dict) -> Dict:
        """Copy template files to project directory"""
        result: Dict[str, Union[List[str], str]] = {
            "files_created": [],
            "directories_created": [],
            "template_used": request.template
        }
        
        # Default template variables
        defaults = {
            "project_name": request.project_name,
            "project_slug": request.project_name.lower().replace(" ", "_").replace("-", "_"),
            "project_description": f"A project scaffolded from the {request.template} template",
            "author": "Generated by goal-dev-spec",
            "email": "example@example.com",
            "year": datetime.now().year
        }
        
        # Merge with provided variables
        vars_to_use = {**defaults, **template_vars}
        
        # Copy all files and directories from template
        for item in template_dir.rglob("*"):
            if item.is_file():
                # Calculate relative path and sanitize it
                relative_path = item.relative_to(template_dir)
                relative_path_str = str(relative_path)
                sanitized_relative_path = self._sanitize_path(relative_path_str)

                # Create destination path with sanitized relative path
                dest_path = project_dir / sanitized_relative_path
                
                # Create parent directories if they don't exist
                dest_path.parent.mkdir(exist_ok=True, parents=True)
                
                # Read template file
                with open(item, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Substitute variables in content
                for var_name, var_value in vars_to_use.items():
                    placeholder = "{" + var_name + "}"
                    content = content.replace(placeholder, str(var_value))
                
                # Write file with substituted content
                with open(dest_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                cast(List[str], result["files_created"]).append(str(relative_path))
            elif item.is_dir():
                # Calculate relative path and sanitize it
                relative_path = item.relative_to(template_dir)
                relative_path_str = str(relative_path)
                sanitized_relative_path = self._sanitize_path(relative_path_str)

                # Create destination directory with sanitized path
                dest_path = project_dir / sanitized_relative_path
                if not dest_path.exists():
                    try:
                        dest_path.mkdir(exist_ok=True, parents=True)
                        print(f"DEBUG: Created directory: {dest_path}")
                        cast(List[str], result["directories_created"]).append(sanitized_relative_path)
                    except OSError as e:
                        print(f"ERROR: Failed to create directory {dest_path}: {e}")
                        raise
        
        return result
    
    def _create_basic_structure(self, project_dir: Path,
                               request: ScaffoldingRequest, template_vars: Dict) -> Dict:
        """Create a basic project structure"""
        result: Dict[str, Union[List[str], str]] = {
            "files_created": [],
            "directories_created": [],
            "template_used": "basic"
        }
        
        # Default template variables
        defaults = {
            "project_name": request.project_name,
            "project_slug": request.project_name.lower().replace(" ", "_").replace("-", "_"),
            "project_description": "A project scaffolded by goal-dev-spec",
            "author": "Generated by goal-dev-spec",
            "email": "example@example.com",
            "year": datetime.now().year
        }
        
        # Merge with provided variables
        vars_to_use = {**defaults, **template_vars}
        
        # Create basic directory structure
        dirs_to_create = ["src", "tests", "docs"]
        for dir_name in dirs_to_create:
            dir_path = project_dir / dir_name
            dir_path.mkdir(exist_ok=True)
            cast(List[str], result["directories_created"]).append(dir_name)
        
        # Create basic files
        files_to_create = {
            "README.md": """# {project_name}

{project_description}

## Getting Started

Instructions for getting started with {project_name}.
""",
            "LICENSE": """MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
            ".gitignore": """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/
""",
            "src/__init__.py": '"""{project_name} package."""\n',
            "tests/__init__.py": '"""Tests for {project_name}."""\n'
        }
        
        for file_path, content in files_to_create.items():
            # Substitute variables in content
            for var_name, var_value in vars_to_use.items():
                placeholder = "{" + var_name + "}"
                content = content.replace(placeholder, str(var_value))
            
            # Create file
            full_path = project_dir / file_path
            full_path.parent.mkdir(exist_ok=True, parents=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            cast(List[str], result["files_created"]).append(file_path)
        
        return result
    
    def get_scaffolding_status(self, request_id: str) -> Optional[Dict]:
        """Get the status of a scaffolding request"""
        if request_id in self.scaffolding_requests:
            request = self.scaffolding_requests[request_id]
            result = asdict(request)
            # Convert result back to dict if it's a JSON string
            if isinstance(result.get('result'), str):
                try:
                    result['result'] = json.loads(result['result'])
                except json.JSONDecodeError:
                    result['result'] = None
            return result
        return None
    
    def list_scaffolding_requests(self) -> List[Dict]:
        """List all scaffolding requests"""
        requests = []
        for req in self.scaffolding_requests.values():
            req_dict = asdict(req)
            # Convert result back to dict if it's a JSON string
            if isinstance(req_dict.get('result'), str):
                try:
                    req_dict['result'] = json.loads(req_dict['result'])
                except json.JSONDecodeError:
                    req_dict['result'] = None
            requests.append(req_dict)
        return requests
    
    def list_templates(self) -> Dict:
        """List all available templates"""
        return self.supported_templates
    
    def generate_project_from_spec(self, spec_file: str, output_path: Optional[str] = None) -> str:
        """
        Generate a project structure based on a specification file
        
        Args:
            spec_file: Path to specification file (YAML or JSON)
            output_path: Path where to create the project
            
        Returns:
            ID of the scaffolding request
        """
        # Read specification file
        spec_path = self.project_path / spec_file
        if not spec_path.exists():
            raise FileNotFoundError(f"Specification file not found: {spec_file}")
        
        # Parse specification
        if spec_path.suffix.lower() in [".yml", ".yaml"]:
            with open(spec_path, 'r') as f:
                spec_data = yaml.safe_load(f)
        elif spec_path.suffix.lower() == ".json":
            with open(spec_path, 'r') as f:
                spec_data = json.load(f)
        else:
            raise ValueError(f"Unsupported specification file format: {spec_path.suffix}")
        
        # Extract project information
        project_name = spec_data.get("project", {}).get("name", "generated-project")
        project_description = spec_data.get("project", {}).get("description", "Generated from specification")
        
        # Determine template based on specification
        template = self._determine_template_from_spec(spec_data)
        
        # Create scaffolding request
        request_id = self.scaffold_project(
            template,
            project_name,
            output_path,
            {
                "project_description": project_description,
                "spec_file": spec_file
            }
        )
        
        return request_id
    
    def _determine_template_from_spec(self, spec_data: Dict) -> str:
        """Determine the best template based on specification data"""
        # This would analyze the specification to determine the best template
        # For now, we'll return a default template
        
        # Check for web-related keywords
        spec_text = str(spec_data).lower()
        if "web" in spec_text or "api" in spec_text or "http" in spec_text:
            return "python_web"
        elif "machine learning" in spec_text or "ml" in spec_text:
            return "python_ml"
        else:
            return "python_basic"


# CLI Integration
def scaffolding_cli():
    """CLI commands for project scaffolding"""
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    app = typer.Typer()
    console = Console()
    
    @app.command()
    def create(
        template: str = typer.Argument(..., help="Template to use for scaffolding"),
        name: str = typer.Argument(..., help="Name of the new project"),
        output: str = typer.Option(None, help="Output directory path"),
        vars: str = typer.Option("", help="Template variables as JSON string")
    ):
        """Scaffold a new project from a template"""
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
            
            # Parse template variables
            template_vars = {}
            if vars:
                try:
                    template_vars = json.loads(vars)
                except json.JSONDecodeError as e:
                    console.print(f"[red]Error parsing template variables: {e}[/red]")
                    return
            
            # Initialize project scaffolder
            scaffolder = ProjectScaffolder(project_path)
            
            # Scaffold project
            request_id = scaffolder.scaffold_project(template, name, output, template_vars)
            
            console.print(f"[green]✓[/green] Project scaffolding request created with ID: {request_id}")
            console.print(f"Check status with: goal scaffold status {request_id}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def status(request_id: str = typer.Argument(..., help="Request ID")):
        """Check the status of a scaffolding request"""
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
            
            # Initialize project scaffolder
            scaffolder = ProjectScaffolder(project_path)
            
            # Check status
            status = scaffolder.get_scaffolding_status(request_id)
            if status:
                console.print(Panel(f"[bold]Project Scaffolding Status: {request_id}[/bold]", expand=False))
                console.print(f"Template: {status['template']}")
                console.print(f"Project Name: {status['project_name']}")
                console.print(f"Output Path: {status['output_path']}")
                console.print(f"Status: {status['status']}")
                if status.get('error'):
                    console.print(f"[red]Error:[/red] {status['error']}")
                elif status.get('result'):
                    result = status['result']
                    if isinstance(result, str):
                        try:
                            result = json.loads(result)
                        except json.JSONDecodeError:
                            result = {"output": result}
                    
                    console.print(f"Template Used: {result.get('template_used', 'unknown')}")
                    console.print(f"Files Created: {len(result.get('files_created', []))}")
                    console.print(f"Directories Created: {len(result.get('directories_created', []))}")
            else:
                console.print(f"[red]Request {request_id} not found[/red]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def list():
        """List all scaffolding requests"""
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
            
            # Initialize project scaffolder
            scaffolder = ProjectScaffolder(project_path)
            
            # List requests
            requests = scaffolder.list_scaffolding_requests()
            if requests:
                console.print(Panel(f"[bold]Project Scaffolding Requests ({len(requests)})[/bold]", expand=False))
                
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("ID", style="cyan")
                table.add_column("Template", style="green")
                table.add_column("Project", style="yellow")
                table.add_column("Status", style="blue")
                table.add_column("Output", style="dim")
                table.add_column("Created", style="dim")
                
                for req in requests:
                    created = datetime.fromisoformat(req['created_at']).strftime("%Y-%m-%d %H:%M")
                    table.add_row(
                        req['id'][:8],
                        req['template'],
                        req['project_name'],
                        req['status'],
                        req['output_path'][:20] + "..." if len(req['output_path']) > 20 else req['output_path'],
                        created
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No scaffolding requests found[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def templates():
        """List all available templates"""
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
            
            # Initialize project scaffolder
            scaffolder = ProjectScaffolder(project_path)
            
            # List templates
            templates = scaffolder.list_templates()
            if templates:
                console.print(Panel(f"[bold]Available Templates ({len(templates)})[/bold]", expand=False))
                
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Template", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Language", style="yellow")
                table.add_column("Description", style="dim")
                
                for template_id, template_info in templates.items():
                    table.add_row(
                        template_id,
                        template_info['name'],
                        template_info['language'],
                        template_info['description']
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No templates found[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def from_spec(
        spec: str = typer.Argument(..., help="Path to specification file"),
        output: str = typer.Option(None, help="Output directory path")
    ):
        """Generate a project structure based on a specification file"""
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
            
            # Initialize project scaffolder
            scaffolder = ProjectScaffolder(project_path)
            
            # Generate project from specification
            request_id = scaffolder.generate_project_from_spec(spec, output)
            
            console.print(f"[green]✓[/green] Project generation request created with ID: {request_id}")
            console.print(f"Check status with: goal scaffold status {request_id}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    return app


# Integration with main CLI
def integrate_scaffold_with_main_cli(main_app):
    """Integrate project scaffolding commands with main CLI"""
    scaffold_app = scaffolding_cli()
    main_app.add_typer(scaffold_app, name="scaffold")
    return main_app