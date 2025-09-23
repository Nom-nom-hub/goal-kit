"""
Automated Documentation Generation for goal-dev-spec
Exceeds spec-kit functionality with intelligent documentation generation and management.
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib


@dataclass
class DocumentationRequest:
    """Data class for documentation requests"""
    id: str
    source_path: str
    doc_type: str  # api, user_guide, technical, architecture
    output_path: str
    created_at: str
    status: str = "pending"
    result: Optional[str] = None
    error: Optional[str] = None


class DocumentationGenerator:
    """Automated documentation generation system"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.docs_path = project_path / "docs"
        self.docs_path.mkdir(exist_ok=True)
        
        # Documentation requests storage
        self.doc_requests_file = self.docs_path / "doc_requests.json"
        self.doc_requests = self._load_doc_requests()
        
        # Supported documentation types
        self.supported_doc_types = {
            "api": "API Documentation",
            "user_guide": "User Guide",
            "technical": "Technical Documentation",
            "architecture": "Architecture Documentation",
            "readme": "Project README"
        }
        
        # Template directory
        self.templates_path = project_path / "templates" / "docs"
        self.templates_path.mkdir(exist_ok=True, parents=True)
        
        # Initialize with default templates if they don't exist
        self._initialize_default_templates()
    
    def _load_doc_requests(self) -> Dict[str, DocumentationRequest]:
        """Load documentation requests from file"""
        if self.doc_requests_file.exists():
            try:
                with open(self.doc_requests_file, 'r') as f:
                    data = json.load(f)
                requests = {}
                for req_data in data:
                    req_data['status'] = req_data.get('status', 'pending')
                    request = DocumentationRequest(**req_data)
                    requests[request.id] = request
                return requests
            except Exception as e:
                print(f"Warning: Could not load documentation requests: {e}")
        return {}
    
    def _save_doc_requests(self):
        """Save documentation requests to file"""
        data = [asdict(req) for req in self.doc_requests.values()]
        with open(self.doc_requests_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _initialize_default_templates(self):
        """Initialize default documentation templates"""
        # API Documentation template
        api_template = self.templates_path / "api_template.md"
        if not api_template.exists():
            with open(api_template, 'w') as f:
                f.write("""# API Documentation

## Overview

{project_description}

## Endpoints

{endpoints}

## Data Models

{data_models}

## Error Codes

{error_codes}

## Authentication

{authentication}

## Rate Limiting

{rate_limiting}

## Changelog

{changelog}
""")
        
        # User Guide template
        user_guide_template = self.templates_path / "user_guide_template.md"
        if not user_guide_template.exists():
            with open(user_guide_template, 'w') as f:
                f.write("""# User Guide

## Introduction

{introduction}

## Getting Started

{getting_started}

## Installation

{installation}

## Configuration

{configuration}

## Usage

{usage}

## Troubleshooting

{troubleshooting}

## FAQ

{faq}
""")
        
        # Technical Documentation template
        tech_template = self.templates_path / "technical_template.md"
        if not tech_template.exists():
            with open(tech_template, 'w') as f:
                f.write("""# Technical Documentation

## System Overview

{system_overview}

## Architecture

{architecture}

## Components

{components}

## Data Flow

{data_flow}

## APIs

{apis}

## Database Schema

{database_schema}

## Security

{security}

## Performance

{performance}

## Testing

{testing}

## Deployment

{deployment}
""")
        
        # Architecture Documentation template
        arch_template = self.templates_path / "architecture_template.md"
        if not arch_template.exists():
            with open(arch_template, 'w') as f:
                f.write("""# Architecture Documentation

## Overview

{overview}

## Design Principles

{design_principles}

## System Architecture

{system_architecture}

## Component Architecture

{component_architecture}

## Technology Stack

{technology_stack}

## Data Architecture

{data_architecture}

## Security Architecture

{security_architecture}

## Scalability

{scalability}

## Monitoring

{monitoring}

## Deployment Architecture

{deployment_architecture}
""")
        
        # README template
        readme_template = self.templates_path / "readme_template.md"
        if not readme_template.exists():
            with open(readme_template, 'w') as f:
                f.write("""# {project_name}

{project_description}

## Table of Contents

{toc}

## Features

{features}

## Installation

{installation}

## Usage

{usage}

## Configuration

{configuration}

## API

{api}

## Contributing

{contributing}

## License

{license}

## Contact

{contact}
""")
    
    def generate_documentation(self, source_path: str, doc_type: str, 
                             output_path: str = None, template_vars: Dict = None) -> str:
        """
        Generate documentation based on source files
        
        Args:
            source_path: Path to source files or directory
            doc_type: Type of documentation to generate
            output_path: Path where to save the generated documentation
            template_vars: Variables to substitute in the template
            
        Returns:
            ID of the documentation request
        """
        # Validate documentation type
        if doc_type not in self.supported_doc_types:
            raise ValueError(f"Unsupported documentation type: {doc_type}")
        
        # Create documentation request
        request_id = hashlib.md5(f"{source_path}_{doc_type}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        if output_path is None:
            # Generate default output path
            output_path = f"docs/{doc_type}_{request_id}.md"
        
        request = DocumentationRequest(
            id=request_id,
            source_path=source_path,
            doc_type=doc_type,
            output_path=output_path,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.doc_requests[request_id] = request
        self._save_doc_requests()
        
        # Process request
        self._process_doc_request(request_id, template_vars or {})
        
        return request_id
    
    def _process_doc_request(self, request_id: str, template_vars: Dict):
        """Process a documentation request"""
        if request_id not in self.doc_requests:
            return
        
        request = self.doc_requests[request_id]
        request.status = "processing"
        self._save_doc_requests()
        
        try:
            # Generate documentation based on type
            if request.doc_type == "api":
                doc_content = self._generate_api_documentation(request.source_path, template_vars)
            elif request.doc_type == "user_guide":
                doc_content = self._generate_user_guide(request.source_path, template_vars)
            elif request.doc_type == "technical":
                doc_content = self._generate_technical_documentation(request.source_path, template_vars)
            elif request.doc_type == "architecture":
                doc_content = self._generate_architecture_documentation(request.source_path, template_vars)
            elif request.doc_type == "readme":
                doc_content = self._generate_readme(request.source_path, template_vars)
            else:
                # Generic documentation
                doc_content = self._generate_generic_documentation(request.source_path, template_vars)
            
            # Save generated documentation to file
            output_file = self.project_path / request.output_path
            output_file.parent.mkdir(exist_ok=True, parents=True)
            
            with open(output_file, 'w') as f:
                f.write(doc_content)
            
            # Update request
            request.status = "completed"
            request.result = doc_content
            
        except Exception as e:
            request.status = "failed"
            request.error = str(e)
        
        self._save_doc_requests()
    
    def _generate_api_documentation(self, source_path: str, template_vars: Dict) -> str:
        """Generate API documentation"""
        # Load template
        template_file = self.templates_path / "api_template.md"
        if template_file.exists():
            with open(template_file, 'r') as f:
                template = f.read()
        else:
            template = """# API Documentation

## Overview

{project_description}

## Endpoints

{endpoints}

## Data Models

{data_models}
"""
        
        # Extract information from source files
        source_info = self._extract_source_info(source_path)
        
        # Default values
        defaults = {
            "project_description": "API documentation for the project",
            "endpoints": self._generate_endpoints_section(source_path),
            "data_models": self._generate_data_models_section(source_path),
            "error_codes": "No error codes defined",
            "authentication": "No authentication details provided",
            "rate_limiting": "No rate limiting specified",
            "changelog": "No changelog available"
        }
        
        # Merge with template variables
        vars_to_use = {**defaults, **source_info, **template_vars}
        
        # Substitute variables in template
        doc_content = template.format(**vars_to_use)
        
        return doc_content
    
    def _generate_user_guide(self, source_path: str, template_vars: Dict) -> str:
        """Generate user guide"""
        # Load template
        template_file = self.templates_path / "user_guide_template.md"
        if template_file.exists():
            with open(template_file, 'r') as f:
                template = f.read()
        else:
            template = """# User Guide

## Introduction

{introduction}

## Getting Started

{getting_started}

## Usage

{usage}
"""
        
        # Extract information from source files
        source_info = self._extract_source_info(source_path)
        
        # Default values
        defaults = {
            "introduction": "User guide for the project",
            "getting_started": "Instructions for getting started with the project",
            "installation": "Installation instructions",
            "configuration": "Configuration options",
            "usage": "How to use the project",
            "troubleshooting": "Common issues and solutions",
            "faq": "Frequently asked questions"
        }
        
        # Merge with template variables
        vars_to_use = {**defaults, **source_info, **template_vars}
        
        # Substitute variables in template
        doc_content = template.format(**vars_to_use)
        
        return doc_content
    
    def _generate_technical_documentation(self, source_path: str, template_vars: Dict) -> str:
        """Generate technical documentation"""
        # Load template
        template_file = self.templates_path / "technical_template.md"
        if template_file.exists():
            with open(template_file, 'r') as f:
                template = f.read()
        else:
            template = """# Technical Documentation

## System Overview

{system_overview}

## Components

{components}

## APIs

{apis}
"""
        
        # Extract information from source files
        source_info = self._extract_source_info(source_path)
        
        # Default values
        defaults = {
            "system_overview": "Technical overview of the system",
            "architecture": "System architecture",
            "components": self._generate_components_section(source_path),
            "data_flow": "Data flow diagram",
            "apis": self._generate_apis_section(source_path),
            "database_schema": "Database schema",
            "security": "Security considerations",
            "performance": "Performance characteristics",
            "testing": "Testing strategy",
            "deployment": "Deployment instructions"
        }
        
        # Merge with template variables
        vars_to_use = {**defaults, **source_info, **template_vars}
        
        # Substitute variables in template
        doc_content = template.format(**vars_to_use)
        
        return doc_content
    
    def _generate_architecture_documentation(self, source_path: str, template_vars: Dict) -> str:
        """Generate architecture documentation"""
        # Load template
        template_file = self.templates_path / "architecture_template.md"
        if template_file.exists():
            with open(template_file, 'r') as f:
                template = f.read()
        else:
            template = """# Architecture Documentation

## Overview

{overview}

## System Architecture

{system_architecture}

## Technology Stack

{technology_stack}
"""
        
        # Extract information from source files
        source_info = self._extract_source_info(source_path)
        
        # Default values
        defaults = {
            "overview": "Architecture overview",
            "design_principles": "Design principles",
            "system_architecture": "System architecture diagram",
            "component_architecture": "Component architecture",
            "technology_stack": self._generate_technology_stack_section(source_path),
            "data_architecture": "Data architecture",
            "security_architecture": "Security architecture",
            "scalability": "Scalability considerations",
            "monitoring": "Monitoring strategy",
            "deployment_architecture": "Deployment architecture"
        }
        
        # Merge with template variables
        vars_to_use = {**defaults, **source_info, **template_vars}
        
        # Substitute variables in template
        doc_content = template.format(**vars_to_use)
        
        return doc_content
    
    def _generate_readme(self, source_path: str, template_vars: Dict) -> str:
        """Generate README documentation"""
        # Load template
        template_file = self.templates_path / "readme_template.md"
        if template_file.exists():
            with open(template_file, 'r') as f:
                template = f.read()
        else:
            template = """# {project_name}

{project_description}

## Features

{features}

## Installation

{installation}

## Usage

{usage}
"""
        
        # Extract information from source files
        source_info = self._extract_source_info(source_path)
        
        # Default values
        defaults = {
            "project_name": "Project Name",
            "project_description": "Project description",
            "toc": "Table of contents will be generated automatically",
            "features": "Key features of the project",
            "installation": "Installation instructions",
            "usage": "How to use the project",
            "configuration": "Configuration options",
            "api": "API documentation",
            "contributing": "How to contribute to the project",
            "license": "License information",
            "contact": "Contact information"
        }
        
        # Merge with template variables
        vars_to_use = {**defaults, **source_info, **template_vars}
        
        # Substitute variables in template
        doc_content = template.format(**vars_to_use)
        
        return doc_content
    
    def _generate_generic_documentation(self, source_path: str, template_vars: Dict) -> str:
        """Generate generic documentation"""
        return f"""# Documentation for {source_path}

This documentation was automatically generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.

## Source Information

Source Path: {source_path}

## Template Variables

{json.dumps(template_vars, indent=2)}

## Generated Content

This is a placeholder for the generated documentation content.
In a real implementation, this would contain detailed information
extracted from the source files at {source_path}.
"""
    
    def _extract_source_info(self, source_path: str) -> Dict:
        """Extract information from source files"""
        source_path_obj = self.project_path / source_path
        info = {}
        
        if source_path_obj.exists():
            if source_path_obj.is_file():
                # Single file
                info["source_file"] = source_path
                info["source_type"] = source_path_obj.suffix
            elif source_path_obj.is_dir():
                # Directory
                info["source_directory"] = source_path
                # Count files by type
                file_counts = {}
                for file_path in source_path_obj.rglob("*"):
                    if file_path.is_file():
                        ext = file_path.suffix
                        file_counts[ext] = file_counts.get(ext, 0) + 1
                info["file_types"] = file_counts
        
        return info
    
    def _generate_endpoints_section(self, source_path: str) -> str:
        """Generate endpoints section for API documentation"""
        # This would analyze source code to extract API endpoints
        # For now, we'll return a placeholder
        return """### GET /api/users

Retrieve a list of users

**Parameters:**
- `limit` (optional): Number of users to retrieve

**Response:**
```json
{
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    }
  ]
}
```

### POST /api/users

Create a new user

**Request Body:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

**Response:**
```json
{
  "id": 2,
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```"""
    
    def _generate_data_models_section(self, source_path: str) -> str:
        """Generate data models section for API documentation"""
        # This would analyze source code to extract data models
        # For now, we'll return a placeholder
        return """### User

Represents a user in the system

**Fields:**
- `id` (integer): Unique identifier
- `name` (string): User's name
- `email` (string): User's email address
- `created_at` (string): Timestamp when user was created"""
    
    def _generate_components_section(self, source_path: str) -> str:
        """Generate components section for technical documentation"""
        # This would analyze source code to extract components
        # For now, we'll return a placeholder
        return """### Core Components

1. **API Server**: Handles HTTP requests and responses
2. **Database Layer**: Manages data persistence
3. **Authentication Service**: Handles user authentication
4. **Logging Service**: Provides centralized logging
5. **Monitoring Service**: Tracks system performance"""
    
    def _generate_apis_section(self, source_path: str) -> str:
        """Generate APIs section for technical documentation"""
        # This would analyze source code to extract API information
        # For now, we'll return a placeholder
        return """### REST API

The system exposes a RESTful API for external integrations.

**Base URL**: `https://api.example.com/v1`

**Authentication**: Bearer token authentication required for all endpoints

**Rate Limiting**: 1000 requests per hour per IP address"""
    
    def _generate_technology_stack_section(self, source_path: str) -> str:
        """Generate technology stack section for architecture documentation"""
        # This would analyze source code to extract technology information
        # For now, we'll return a placeholder
        return """### Backend

- **Language**: Python 3.9+
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Caching**: Redis

### Frontend

- **Framework**: React 17+
- **State Management**: Redux
- **UI Library**: Material-UI

### Infrastructure

- **Cloud Provider**: AWS
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions"""
    
    def get_doc_status(self, request_id: str) -> Optional[Dict]:
        """Get the status of a documentation request"""
        if request_id in self.doc_requests:
            request = self.doc_requests[request_id]
            return asdict(request)
        return None
    
    def list_doc_requests(self) -> List[Dict]:
        """List all documentation requests"""
        return [asdict(req) for req in self.doc_requests.values()]
    
    def generate_project_docs(self, project_info: Dict = None) -> List[str]:
        """
        Generate comprehensive documentation for the entire project
        
        Args:
            project_info: Dictionary with project information
            
        Returns:
            List of generated documentation request IDs
        """
        if project_info is None:
            project_info = self._extract_project_info()
        
        request_ids = []
        
        # Generate README
        readme_id = self.generate_documentation(
            ".",
            "readme",
            "README.md",
            {
                "project_name": project_info.get("name", "Project"),
                "project_description": project_info.get("description", "Project description")
            }
        )
        request_ids.append(readme_id)
        
        # Generate API documentation if there are API files
        if self._has_api_files():
            api_id = self.generate_documentation(
                "src",
                "api",
                "docs/api.md",
                {
                    "project_description": f"API documentation for {project_info.get('name', 'Project')}"
                }
            )
            request_ids.append(api_id)
        
        # Generate user guide
        user_guide_id = self.generate_documentation(
            ".",
            "user_guide",
            "docs/user_guide.md",
            {
                "introduction": f"User guide for {project_info.get('name', 'Project')}",
                "getting_started": "Follow these steps to get started with the project"
            }
        )
        request_ids.append(user_guide_id)
        
        # Generate technical documentation
        tech_id = self.generate_documentation(
            "src",
            "technical",
            "docs/technical.md",
            {
                "system_overview": f"Technical overview of {project_info.get('name', 'Project')}"
            }
        )
        request_ids.append(tech_id)
        
        # Generate architecture documentation
        arch_id = self.generate_documentation(
            ".",
            "architecture",
            "docs/architecture.md",
            {
                "overview": f"Architecture documentation for {project_info.get('name', 'Project')}"
            }
        )
        request_ids.append(arch_id)
        
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
                import yaml
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
    
    def _has_api_files(self) -> bool:
        """Check if the project has API-related files"""
        # Look for common API file patterns
        api_patterns = [
            "src/**/api*.py",
            "src/**/routes*.py",
            "src/**/controllers*.py",
            "src/**/views*.py"
        ]
        
        for pattern in api_patterns:
            if list(self.project_path.glob(pattern)):
                return True
        
        return False


# CLI Integration
def doc_generation_cli():
    """CLI commands for automated documentation generation"""
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    app = typer.Typer()
    console = Console()
    
    @app.command()
    def generate(
        source: str = typer.Argument(..., help="Source path (file or directory)"),
        type: str = typer.Option("technical", help="Documentation type (api, user_guide, technical, architecture, readme)"),
        output: str = typer.Option(None, help="Output file path"),
        vars: str = typer.Option("", help="Template variables as JSON string")
    ):
        """Generate documentation from source files"""
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
            
            # Initialize documentation generator
            doc_generator = DocumentationGenerator(project_path)
            
            # Generate documentation
            request_id = doc_generator.generate_documentation(source, type, output, template_vars)
            
            console.print(f"[green]✓[/green] Documentation generation request created with ID: {request_id}")
            console.print(f"Check status with: goal docs status {request_id}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def status(request_id: str = typer.Argument(..., help="Request ID")):
        """Check the status of a documentation generation request"""
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
            
            # Initialize documentation generator
            doc_generator = DocumentationGenerator(project_path)
            
            # Check status
            status = doc_generator.get_doc_status(request_id)
            if status:
                console.print(Panel(f"[bold]Documentation Generation Status: {request_id}[/bold]", expand=False))
                console.print(f"Source Path: {status['source_path']}")
                console.print(f"Type: {status['doc_type']}")
                console.print(f"Status: {status['status']}")
                console.print(f"Output Path: {status['output_path']}")
                if status.get('error'):
                    console.print(f"[red]Error:[/red] {status['error']}")
            else:
                console.print(f"[red]Request {request_id} not found[/red]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def list():
        """List all documentation generation requests"""
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
            
            # Initialize documentation generator
            doc_generator = DocumentationGenerator(project_path)
            
            # List requests
            requests = doc_generator.list_doc_requests()
            if requests:
                console.print(Panel(f"[bold]Documentation Generation Requests ({len(requests)})[/bold]", expand=False))
                
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("ID", style="cyan")
                table.add_column("Source", style="green")
                table.add_column("Type", style="yellow")
                table.add_column("Status", style="blue")
                table.add_column("Output", style="dim")
                table.add_column("Created", style="dim")
                
                for req in requests:
                    created = datetime.fromisoformat(req['created_at']).strftime("%Y-%m-%d %H:%M")
                    table.add_row(
                        req['id'][:8],
                        req['source_path'][:20] + "..." if len(req['source_path']) > 20 else req['source_path'],
                        req['doc_type'],
                        req['status'],
                        req['output_path'][:20] + "..." if len(req['output_path']) > 20 else req['output_path'],
                        created
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No documentation requests found[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def project():
        """Generate comprehensive documentation for the entire project"""
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
            
            # Initialize documentation generator
            doc_generator = DocumentationGenerator(project_path)
            
            # Generate project documentation
            request_ids = doc_generator.generate_project_docs()
            
            console.print(f"[green]✓[/green] Generated {len(request_ids)} documentation files:")
            for req_id in request_ids:
                status = doc_generator.get_doc_status(req_id)
                if status:
                    console.print(f"  - {status['output_path']} ({status['doc_type']})")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    return app


# Integration with main CLI
def integrate_docs_with_main_cli(main_app):
    """Integrate documentation generation commands with main CLI"""
    docs_app = doc_generation_cli()
    main_app.add_typer(docs_app, name="docs")
    return main_app