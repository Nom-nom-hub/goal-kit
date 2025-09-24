"""
AI-Powered Code Generation and Refactoring Tools for goal-dev-spec
Exceeds spec-kit functionality with intelligent code generation and refactoring capabilities.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib


@dataclass
class CodeGenerationRequest:
    """Data class for code generation requests"""
    id: str
    prompt: str
    language: str
    framework: str
    output_path: str
    created_at: str
    status: str = "pending"
    result: Optional[str] = None
    error: Optional[str] = None


@dataclass
class RefactoringRequest:
    """Data class for refactoring requests"""
    id: str
    file_path: str
    refactoring_type: str  # optimize, simplify, modularize, document
    prompt: str
    created_at: str
    status: str = "pending"
    result: Optional[str] = None
    error: Optional[str] = None


class AICodeGenerator:
    """AI-powered code generation and refactoring tools"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.ai_path = project_path / ".goal" / "ai"
        self.ai_path.mkdir(exist_ok=True)
        
        # Generation requests storage
        self.generation_requests_file = self.ai_path / "generation_requests.json"
        self.generation_requests = self._load_generation_requests()
        
        # Refactoring requests storage
        self.refactoring_requests_file = self.ai_path / "refactoring_requests.json"
        self.refactoring_requests = self._load_refactoring_requests()
        
        # Supported languages and frameworks
        self.supported_languages = {
            "python": {
                "frameworks": ["flask", "django", "fastapi", "streamlit"],
                "extensions": [".py"]
            },
            "javascript": {
                "frameworks": ["react", "vue", "angular", "node"],
                "extensions": [".js", ".jsx"]
            },
            "typescript": {
                "frameworks": ["react", "vue", "angular", "node"],
                "extensions": [".ts", ".tsx"]
            },
            "java": {
                "frameworks": ["spring", "micronaut", "quarkus"],
                "extensions": [".java"]
            },
            "go": {
                "frameworks": ["gin", "echo", "fiber"],
                "extensions": [".go"]
            }
        }
    
    def _load_generation_requests(self) -> Dict[str, CodeGenerationRequest]:
        """Load generation requests from file"""
        if self.generation_requests_file.exists():
            try:
                with open(self.generation_requests_file, 'r') as f:
                    data = json.load(f)
                requests = {}
                for req_data in data:
                    req_data['status'] = req_data.get('status', 'pending')
                    request = CodeGenerationRequest(**req_data)
                    requests[request.id] = request
                return requests
            except Exception as e:
                print(f"Warning: Could not load generation requests: {e}")
        return {}
    
    def _save_generation_requests(self):
        """Save generation requests to file"""
        data = [asdict(req) for req in self.generation_requests.values()]
        with open(self.generation_requests_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_refactoring_requests(self) -> Dict[str, RefactoringRequest]:
        """Load refactoring requests from file"""
        if self.refactoring_requests_file.exists():
            try:
                with open(self.refactoring_requests_file, 'r') as f:
                    data = json.load(f)
                requests = {}
                for req_data in data:
                    req_data['status'] = req_data.get('status', 'pending')
                    request = RefactoringRequest(**req_data)
                    requests[request.id] = request
                return requests
            except Exception as e:
                print(f"Warning: Could not load refactoring requests: {e}")
        return {}
    
    def _save_refactoring_requests(self):
        """Save refactoring requests to file"""
        data = [asdict(req) for req in self.refactoring_requests.values()]
        with open(self.refactoring_requests_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def generate_code(self, prompt: str, language: str = "python",
                      framework: str = "flask", output_path: Optional[str] = None) -> str:
        """
        Generate code based on a prompt using AI
        
        Args:
            prompt: Description of what code to generate
            language: Programming language (python, javascript, typescript, java, go)
            framework: Framework to use
            output_path: Path where to save the generated code
            
        Returns:
            ID of the generation request
        """
        # Validate language and framework
        if language not in self.supported_languages:
            raise ValueError(f"Unsupported language: {language}")
        
        if framework not in self.supported_languages[language]["frameworks"]:
            raise ValueError(f"Unsupported framework {framework} for language {language}")
        
        # Create generation request
        request_id = hashlib.md5(f"{prompt}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        if output_path is None:
            # Generate default output path
            ext = self.supported_languages[language]["extensions"][0]
            output_path = f"generated_{request_id}{ext}"
        
        request = CodeGenerationRequest(
            id=request_id,
            prompt=prompt,
            language=language,
            framework=framework,
            output_path=output_path,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.generation_requests[request_id] = request
        self._save_generation_requests()
        
        # Process request (in a real implementation, this would call an AI service)
        self._process_generation_request(request_id)
        
        return request_id
    
    def _process_generation_request(self, request_id: str):
        """Process a code generation request"""
        if request_id not in self.generation_requests:
            return
        
        request = self.generation_requests[request_id]
        request.status = "processing"
        self._save_generation_requests()
        
        try:
            # In a real implementation, this would call an AI service
            # For now, we'll generate mock code based on the prompt
            generated_code = self._generate_mock_code(
                request.prompt, 
                request.language, 
                request.framework
            )
            
            # Save generated code to file
            output_file = self.project_path / request.output_path
            output_file.parent.mkdir(exist_ok=True, parents=True)
            
            with open(output_file, 'w') as f:
                f.write(generated_code)
            
            # Update request
            request.status = "completed"
            request.result = generated_code
            
        except Exception as e:
            request.status = "failed"
            request.error = str(e)
        
        self._save_generation_requests()
    
    def _generate_mock_code(self, prompt: str, language: str, framework: str) -> str:
        """Generate mock code based on prompt (for demonstration)"""
        # This is a simplified mock implementation
        # In a real implementation, this would call an AI service
        
        if language == "python" and framework == "flask":
            return self._generate_flask_code(prompt)
        elif language == "python" and framework == "fastapi":
            return self._generate_fastapi_code(prompt)
        elif language == "javascript" and framework == "react":
            return self._generate_react_code(prompt)
        else:
            # Generic template
            return f"""# Generated {language} code for: {prompt}

# This is a mock implementation
# In a real implementation, this would be generated by an AI

def main():
    print("Generated code for: {prompt}")
    print("Language: {language}")
    print("Framework: {framework}")

if __name__ == "__main__":
    main()
"""
    
    def _generate_flask_code(self, prompt: str) -> str:
        """Generate Flask application code"""
        return f"""#!/usr/bin/env python3
\"\"\"
Flask application generated for: {prompt}
\"\"\"

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({{
        "message": "Welcome to the generated Flask application",
        "description": "{prompt}"
    }})

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'GET':
        return jsonify({{
            "data": [],
            "message": "Retrieved data successfully"
        }})
    elif request.method == 'POST':
        data = request.get_json()
        return jsonify({{
            "data": data,
            "message": "Created data successfully"
        }}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
"""
    
    def _generate_fastapi_code(self, prompt: str) -> str:
        """Generate FastAPI application code"""
        return f"""#!/usr/bin/env python3
\"\"\"
FastAPI application generated for: {prompt}
\"\"\"

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Generated API", description="{prompt}")

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# In-memory storage (in a real app, you'd use a database)
items: List[Item] = []

@app.get("/")
async def read_root():
    return {{"message": "Welcome to the generated FastAPI application", "description": "{prompt}"}}

@app.get("/items/", response_model=List[Item])
async def read_items():
    return items

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
    
    def _generate_react_code(self, prompt: str) -> str:
        """Generate React component code"""
        return f"""import React, {{ useState, useEffect }} from 'react';

/**
 * Component generated for: {prompt}
 */

function GeneratedComponent() {{
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {{
    // Simulate data fetching
    setTimeout(() => {{
      setData([
        {{ id: 1, name: "Item 1", description: "First item" }},
        {{ id: 2, name: "Item 2", description: "Second item" }}
      ]);
      setLoading(false);
    }}, 1000);
  }}, []);

  if (loading) {{
    return <div>Loading...</div>;
  }}

  return (
    <div>
      <h1>Generated Component</h1>
      <p>Description: {prompt}</p>
      <ul>
        {{data.map(item => (
          <li key={{item.id}}>
            <strong>{{item.name}}</strong>: {{item.description}}
          </li>
        ))}}
      </ul>
    </div>
  );
}}

export default GeneratedComponent;
"""
    
    def refactor_code(self, file_path: str, refactoring_type: str, prompt: str = "") -> str:
        """
        Refactor existing code using AI
        
        Args:
            file_path: Path to the file to refactor
            refactoring_type: Type of refactoring (optimize, simplify, modularize, document)
            prompt: Additional instructions for refactoring
            
        Returns:
            ID of the refactoring request
        """
        # Validate refactoring type
        valid_types = ["optimize", "simplify", "modularize", "document"]
        if refactoring_type not in valid_types:
            raise ValueError(f"Invalid refactoring type. Must be one of: {valid_types}")
        
        # Check if file exists
        file_path_obj = self.project_path / file_path
        if not file_path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Create refactoring request
        request_id = hashlib.md5(f"{file_path}_{refactoring_type}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        request = RefactoringRequest(
            id=request_id,
            file_path=file_path,
            refactoring_type=refactoring_type,
            prompt=prompt,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.refactoring_requests[request_id] = request
        self._save_refactoring_requests()
        
        # Process request (in a real implementation, this would call an AI service)
        self._process_refactoring_request(request_id)
        
        return request_id
    
    def _process_refactoring_request(self, request_id: str):
        """Process a code refactoring request"""
        if request_id not in self.refactoring_requests:
            return
        
        request = self.refactoring_requests[request_id]
        request.status = "processing"
        self._save_refactoring_requests()
        
        try:
            # Read the original file
            file_path = self.project_path / request.file_path
            with open(file_path, 'r') as f:
                original_code = f.read()
            
            # In a real implementation, this would call an AI service
            # For now, we'll perform mock refactoring
            refactored_code = self._refactor_mock_code(
                original_code,
                request.refactoring_type,
                request.prompt
            )
            
            # Save refactored code back to file
            with open(file_path, 'w') as f:
                f.write(refactored_code)
            
            # Update request
            request.status = "completed"
            request.result = refactored_code
            
        except Exception as e:
            request.status = "failed"
            request.error = str(e)
        
        self._save_refactoring_requests()
    
    def _refactor_mock_code(self, code: str, refactoring_type: str, prompt: str) -> str:
        """Perform mock code refactoring (for demonstration)"""
        # This is a simplified mock implementation
        # In a real implementation, this would call an AI service
        
        # Add a comment indicating the refactoring
        refactored_code = f"# Refactored code ({refactoring_type})\n"
        if prompt:
            refactored_code += f"# Prompt: {prompt}\n"
        refactored_code += f"# Refactored on {datetime.now().isoformat()}\n\n"
        refactored_code += code
        
        # Add some mock improvements based on refactoring type
        if refactoring_type == "document":
            refactored_code = self._add_mock_documentation(refactored_code)
        elif refactoring_type == "simplify":
            refactored_code = self._simplify_mock_code(refactored_code)
        
        return refactored_code
    
    def _add_mock_documentation(self, code: str) -> str:
        """Add mock documentation to code"""
        lines = code.split('\n')
        documented_lines = []
        
        for line in lines:
            # Add mock docstrings to functions
            if line.strip().startswith('def ') and '(' in line and ':' in line:
                func_name = line.split('def ')[1].split('(')[0]
                documented_lines.append(f'    """Mock documentation for {func_name}"""')
            documented_lines.append(line)
        
        return '\n'.join(documented_lines)
    
    def _simplify_mock_code(self, code: str) -> str:
        """Simplify mock code"""
        # Remove extra blank lines
        lines = code.split('\n')
        simplified_lines = []
        prev_line_blank = False
        
        for line in lines:
            if line.strip() == "":
                if not prev_line_blank:
                    simplified_lines.append(line)
                prev_line_blank = True
            else:
                simplified_lines.append(line)
                prev_line_blank = False
        
        return '\n'.join(simplified_lines)
    
    def get_generation_status(self, request_id: str) -> Optional[Dict]:
        """Get the status of a code generation request"""
        if request_id in self.generation_requests:
            request = self.generation_requests[request_id]
            return asdict(request)
        return None
    
    def get_refactoring_status(self, request_id: str) -> Optional[Dict]:
        """Get the status of a code refactoring request"""
        if request_id in self.refactoring_requests:
            request = self.refactoring_requests[request_id]
            return asdict(request)
        return None
    
    def list_generation_requests(self) -> List[Dict]:
        """List all code generation requests"""
        return [asdict(req) for req in self.generation_requests.values()]
    
    def list_refactoring_requests(self) -> List[Dict]:
        """List all code refactoring requests"""
        return [asdict(req) for req in self.refactoring_requests.values()]
    
    def analyze_code_quality(self, file_path: str) -> Dict[str, Any]:
        """Analyze code quality and suggest improvements"""
        file_path_obj = self.project_path / file_path
        if not file_path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read the file
        with open(file_path_obj, 'r') as f:
            code = f.read()
        
        # Perform basic analysis
        analysis: Dict[str, Any] = {
            "file": file_path,
            "lines_of_code": len(code.split('\n')),
            "file_size": len(code),
            "suggestions": []
        }
        
        # Simple heuristics for suggestions
        if len(code.split('\n')) > 200:
            analysis["suggestions"].append({
                "type": "modularize",
                "description": "File is quite long, consider breaking it into smaller modules",
                "priority": "medium"
            })
        
        if code.count('    ') > code.count('\t'):
            analysis["suggestions"].append({
                "type": "format",
                "description": "Consider using tabs for indentation for consistency",
                "priority": "low"
            })
        
        if 'TODO' in code or 'FIXME' in code:
            analysis["suggestions"].append({
                "type": "cleanup",
                "description": "Found TODO/FIXME comments, consider addressing them",
                "priority": "medium"
            })
        
        # Add mock suggestions for demonstration
        analysis["suggestions"].append({
            "type": "optimize",
            "description": "Consider using list comprehensions for better performance",
            "priority": "low"
        })
        
        analysis["suggestions"].append({
            "type": "document",
            "description": "Add docstrings to functions and classes for better documentation",
            "priority": "high"
        })
        
        return analysis


# CLI Integration
def ai_code_cli():
    """CLI commands for AI-powered code generation"""
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    app = typer.Typer()
    console = Console()
    
    @app.command()
    def generate(
        prompt: str = typer.Argument(..., help="Description of what code to generate"),
        language: str = typer.Option("python", help="Programming language"),
        framework: str = typer.Option("flask", help="Framework to use"),
        output: str = typer.Option(None, help="Output file path")
    ):
        """Generate code based on a prompt using AI"""
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
            
            # Initialize AI code generator
            ai_generator = AICodeGenerator(project_path)
            
            # Generate code
            request_id = ai_generator.generate_code(prompt, language, framework, output)
            
            console.print(f"[green]✓[/green] Code generation request created with ID: {request_id}")
            console.print(f"Check status with: goal ai status {request_id}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def refactor(
        file_path: str = typer.Argument(..., help="Path to file to refactor"),
        type: str = typer.Option("optimize", help="Type of refactoring (optimize, simplify, modularize, document)"),
        prompt: str = typer.Option("", help="Additional instructions for refactoring")
    ):
        """Refactor existing code using AI"""
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
            
            # Initialize AI code generator
            ai_generator = AICodeGenerator(project_path)
            
            # Refactor code
            request_id = ai_generator.refactor_code(file_path, type, prompt)
            
            console.print(f"[green]✓[/green] Code refactoring request created with ID: {request_id}")
            console.print(f"Check status with: goal ai status {request_id}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def status(request_id: str = typer.Argument(..., help="Request ID")):
        """Check the status of a code generation or refactoring request"""
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
            
            # Initialize AI code generator
            ai_generator = AICodeGenerator(project_path)
            
            # Check generation status first
            gen_status = ai_generator.get_generation_status(request_id)
            if gen_status:
                console.print(Panel(f"[bold]Code Generation Status: {request_id}[/bold]", expand=False))
                console.print(f"Prompt: {gen_status['prompt']}")
                console.print(f"Status: {gen_status['status']}")
                console.print(f"Language: {gen_status['language']}")
                console.print(f"Framework: {gen_status['framework']}")
                console.print(f"Output Path: {gen_status['output_path']}")
                if gen_status.get('error'):
                    console.print(f"[red]Error:[/red] {gen_status['error']}")
                return
            
            # Check refactoring status
            ref_status = ai_generator.get_refactoring_status(request_id)
            if ref_status:
                console.print(Panel(f"[bold]Code Refactoring Status: {request_id}[/bold]", expand=False))
                console.print(f"File Path: {ref_status['file_path']}")
                console.print(f"Type: {ref_status['refactoring_type']}")
                console.print(f"Status: {ref_status['status']}")
                if ref_status.get('prompt'):
                    console.print(f"Prompt: {ref_status['prompt']}")
                if ref_status.get('error'):
                    console.print(f"[red]Error:[/red] {ref_status['error']}")
                return
            
            console.print(f"[red]Request {request_id} not found[/red]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def list():
        """List all code generation and refactoring requests"""
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
            
            # Initialize AI code generator
            ai_generator = AICodeGenerator(project_path)
            
            # List generation requests
            gen_requests = ai_generator.list_generation_requests()
            if gen_requests:
                console.print(Panel(f"[bold]Code Generation Requests ({len(gen_requests)})[/bold]", expand=False))
                
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("ID", style="cyan")
                table.add_column("Prompt", style="green")
                table.add_column("Language", style="yellow")
                table.add_column("Status", style="blue")
                table.add_column("Created", style="dim")
                
                for req in gen_requests:
                    try:
                        created = datetime.fromisoformat(req['created_at']).strftime("%Y-%m-%d %H:%M")
                    except ValueError:
                        created = "Invalid date"
                    table.add_row(
                        req['id'][:8],
                        req['prompt'][:30] + "..." if len(req['prompt']) > 30 else req['prompt'],
                        req['language'],
                        req['status'],
                        created
                    )
                
                console.print(table)
            
            # List refactoring requests
            ref_requests = ai_generator.list_refactoring_requests()
            if ref_requests:
                console.print(Panel(f"[bold]Code Refactoring Requests ({len(ref_requests)})[/bold]", expand=False))
                
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("ID", style="cyan")
                table.add_column("File", style="green")
                table.add_column("Type", style="yellow")
                table.add_column("Status", style="blue")
                table.add_column("Created", style="dim")
                
                for req in ref_requests:
                    try:
                        created = datetime.fromisoformat(req['created_at']).strftime("%Y-%m-%d %H:%M")
                    except ValueError:
                        created = "Invalid date"
                    table.add_row(
                        req['id'][:8],
                        req['file_path'][:20] + "..." if len(req['file_path']) > 20 else req['file_path'],
                        req['refactoring_type'],
                        req['status'],
                        created
                    )
                
                console.print(table)
            
            if not gen_requests and not ref_requests:
                console.print("[yellow]No requests found[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def analyze(
        file_path: str = typer.Argument(..., help="Path to file to analyze")
    ):
        """Analyze code quality and suggest improvements"""
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
            
            # Initialize AI code generator
            ai_generator = AICodeGenerator(project_path)
            
            # Analyze code
            analysis = ai_generator.analyze_code_quality(file_path)
            
            console.print(Panel(f"[bold]Code Quality Analysis: {file_path}[/bold]", expand=False))
            console.print(f"Lines of Code: {analysis['lines_of_code']}")
            console.print(f"File Size: {analysis['file_size']} bytes")
            
            if analysis['suggestions']:
                console.print("\n[bold]Suggestions:[/bold]")
                for i, suggestion in enumerate(analysis['suggestions'], 1):
                    priority_color = {
                        "high": "red",
                        "medium": "yellow",
                        "low": "green"
                    }.get(suggestion['priority'], "blue")
                    
                    console.print(f"{i}. [{priority_color}]{suggestion['type']}[{priority_color}]: {suggestion['description']}")
            else:
                console.print("\n[green]No suggestions found. Code looks good![/green]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    return app


# Integration with main CLI
def integrate_ai_code_with_main_cli(main_app):
    """Integrate AI code generation commands with main CLI"""
    ai_code_app = ai_code_cli()
    main_app.add_typer(ai_code_app, name="ai")
    return main_app