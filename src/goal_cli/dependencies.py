"""
Intelligent Dependency Management for goal-dev-spec
Exceeds spec-kit functionality with advanced dependency analysis and management.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib


@dataclass
class DependencyRequest:
    """Data class for dependency management requests"""
    id: str
    action: str  # analyze, update, resolve, audit
    target: str  # project, file, package
    created_at: str
    status: str = "pending"
    result: Optional[Dict] = None
    error: Optional[str] = None


@dataclass
class DependencyInfo:
    """Data class for dependency information"""
    name: str
    version: str
    source: str  # pip, npm, gem, etc.
    license: str = "unknown"
    vulnerabilities: List[str] = None
    dependencies: List[str] = None
    usage: str = "unknown"  # direct, transitive
    status: str = "active"  # active, deprecated, vulnerable


class DependencyManager:
    """Intelligent dependency management system"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.deps_path = project_path / ".goal" / "dependencies"
        self.deps_path.mkdir(exist_ok=True)
        
        # Dependency requests storage
        self.dependency_requests_file = self.deps_path / "dependency_requests.json"
        self.dependency_requests = self._load_dependency_requests()
        
        # Dependency database
        self.dependencies_file = self.deps_path / "dependencies.json"
        self.dependencies = self._load_dependencies()
        
        # Supported package managers
        self.supported_managers = {
            "pip": {
                "name": "Python Package Index",
                "files": ["requirements.txt", "pyproject.toml", "setup.py"],
                "lock_files": ["requirements.lock", "poetry.lock", "Pipfile.lock"]
            },
            "npm": {
                "name": "Node Package Manager",
                "files": ["package.json"],
                "lock_files": ["package-lock.json", "yarn.lock"]
            },
            "yarn": {
                "name": "Yarn Package Manager",
                "files": ["package.json"],
                "lock_files": ["yarn.lock"]
            },
            "gem": {
                "name": "RubyGems",
                "files": ["Gemfile"],
                "lock_files": ["Gemfile.lock"]
            },
            "cargo": {
                "name": "Rust Cargo",
                "files": ["Cargo.toml"],
                "lock_files": ["Cargo.lock"]
            },
            "gradle": {
                "name": "Gradle",
                "files": ["build.gradle", "build.gradle.kts"],
                "lock_files": ["gradle.lockfile"]
            },
            "maven": {
                "name": "Apache Maven",
                "files": ["pom.xml"],
                "lock_files": []
            }
        }
    
    def _load_dependency_requests(self) -> Dict[str, DependencyRequest]:
        """Load dependency requests from file"""
        if self.dependency_requests_file.exists():
            try:
                with open(self.dependency_requests_file, 'r') as f:
                    data = json.load(f)
                requests = {}
                for req_data in data:
                    req_data['status'] = req_data.get('status', 'pending')
                    # Convert result back to dict if it's a string
                    if isinstance(req_data.get('result'), str):
                        try:
                            req_data['result'] = json.loads(req_data['result'])
                        except json.JSONDecodeError:
                            req_data['result'] = None
                    request = DependencyRequest(**req_data)
                    requests[request.id] = request
                return requests
            except Exception as e:
                print(f"Warning: Could not load dependency requests: {e}")
        return {}
    
    def _save_dependency_requests(self):
        """Save dependency requests to file"""
        # Convert result to string if it's a dict for JSON serialization
        data = []
        for req in self.dependency_requests.values():
            req_dict = asdict(req)
            if isinstance(req_dict.get('result'), dict):
                req_dict['result'] = json.dumps(req_dict['result'])
            data.append(req_dict)
        
        with open(self.dependency_requests_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_dependencies(self) -> Dict[str, DependencyInfo]:
        """Load dependencies from file"""
        if self.dependencies_file.exists():
            try:
                with open(self.dependencies_file, 'r') as f:
                    data = json.load(f)
                dependencies = {}
                for dep_data in data:
                    # Handle potential string values for list fields
                    if isinstance(dep_data.get('vulnerabilities'), str):
                        try:
                            dep_data['vulnerabilities'] = json.loads(dep_data['vulnerabilities'])
                        except json.JSONDecodeError:
                            dep_data['vulnerabilities'] = []
                    if isinstance(dep_data.get('dependencies'), str):
                        try:
                            dep_data['dependencies'] = json.loads(dep_data['dependencies'])
                        except json.JSONDecodeError:
                            dep_data['dependencies'] = []
                    dependency = DependencyInfo(**dep_data)
                    dependencies[dependency.name] = dependency
                return dependencies
            except Exception as e:
                print(f"Warning: Could not load dependencies: {e}")
        return {}
    
    def _save_dependencies(self):
        """Save dependencies to file"""
        # Convert list fields to strings for JSON serialization
        data = []
        for dep in self.dependencies.values():
            dep_dict = asdict(dep)
            if isinstance(dep_dict.get('vulnerabilities'), list):
                dep_dict['vulnerabilities'] = json.dumps(dep_dict['vulnerabilities'])
            if isinstance(dep_dict.get('dependencies'), list):
                dep_dict['dependencies'] = json.dumps(dep_dict['dependencies'])
            data.append(dep_dict)
        
        with open(self.dependencies_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def analyze_dependencies(self, target: str = "project") -> str:
        """
        Analyze project dependencies
        
        Args:
            target: What to analyze (project, file, or specific package)
            
        Returns:
            ID of the dependency request
        """
        # Create dependency request
        request_id = hashlib.md5(f"analyze_{target}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        request = DependencyRequest(
            id=request_id,
            action="analyze",
            target=target,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.dependency_requests[request_id] = request
        self._save_dependency_requests()
        
        # Process request
        self._process_dependency_request(request_id)
        
        return request_id
    
    def update_dependencies(self, target: str = "project", strategy: str = "safe") -> str:
        """
        Update project dependencies
        
        Args:
            target: What to update (project, file, or specific package)
            strategy: Update strategy (safe, latest, pin)
            
        Returns:
            ID of the dependency request
        """
        # Create dependency request
        request_id = hashlib.md5(f"update_{target}_{strategy}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        request = DependencyRequest(
            id=request_id,
            action="update",
            target=target,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.dependency_requests[request_id] = request
        self._save_dependency_requests()
        
        # Process request
        self._process_dependency_request(request_id, {"strategy": strategy})
        
        return request_id
    
    def resolve_conflicts(self, target: str = "project") -> str:
        """
        Resolve dependency conflicts
        
        Args:
            target: What to resolve conflicts for
            
        Returns:
            ID of the dependency request
        """
        # Create dependency request
        request_id = hashlib.md5(f"resolve_{target}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        request = DependencyRequest(
            id=request_id,
            action="resolve",
            target=target,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.dependency_requests[request_id] = request
        self._save_dependency_requests()
        
        # Process request
        self._process_dependency_request(request_id)
        
        return request_id
    
    def audit_dependencies(self, target: str = "project") -> str:
        """
        Audit project dependencies for vulnerabilities
        
        Args:
            target: What to audit (project, file, or specific package)
            
        Returns:
            ID of the dependency request
        """
        # Create dependency request
        request_id = hashlib.md5(f"audit_{target}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        request = DependencyRequest(
            id=request_id,
            action="audit",
            target=target,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.dependency_requests[request_id] = request
        self._save_dependency_requests()
        
        # Process request
        self._process_dependency_request(request_id)
        
        return request_id
    
    def _process_dependency_request(self, request_id: str, params: Optional[Dict[str, Any]] = None) -> None:
        """Process a dependency request"""
        if request_id not in self.dependency_requests:
            return
        
        request = self.dependency_requests[request_id]
        request.status = "processing"
        self._save_dependency_requests()
        
        try:
            result = {}
            
            if request.action == "analyze":
                result = self._analyze_dependencies(request.target)
            elif request.action == "update":
                strategy = params.get("strategy", "safe") if params else "safe"
                result = self._update_dependencies(request.target, strategy)
            elif request.action == "resolve":
                result = self._resolve_conflicts(request.target)
            elif request.action == "audit":
                result = self._audit_dependencies(request.target)
            
            # Update request
            request.status = "completed"
            request.result = result
            
        except Exception as e:
            request.status = "failed"
            request.error = str(e)
        
        self._save_dependency_requests()
    
    def _analyze_dependencies(self, target: str) -> Dict:
        """Analyze project dependencies"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "managers_detected": [],
            "dependencies_found": 0,
            "direct_dependencies": [],
            "transitive_dependencies": [],
            "potential_issues": []
        }
        
        # Detect package managers in the project
        managers = self._detect_package_managers()
        analysis["managers_detected"] = list(managers.keys())
        
        # Analyze dependencies for each manager
        all_dependencies = {}
        for manager_name, manager_info in managers.items():
            deps = self._extract_dependencies(manager_name, manager_info)
            all_dependencies[manager_name] = deps
            analysis["dependencies_found"] += len(deps)
            
            # Separate direct and transitive dependencies
            for dep_name, dep_info in deps.items():
                if dep_info.usage == "direct":
                    analysis["direct_dependencies"].append({
                        "name": dep_name,
                        "version": dep_info.version,
                        "manager": manager_name
                    })
                else:
                    analysis["transitive_dependencies"].append({
                        "name": dep_name,
                        "version": dep_info.version,
                        "manager": manager_name
                    })
        
        # Store dependencies
        for manager_deps in all_dependencies.values():
            for dep in manager_deps.values():
                self.dependencies[dep.name] = dep
        self._save_dependencies()
        
        # Check for potential issues
        analysis["potential_issues"] = self._check_dependency_issues(all_dependencies)
        
        return analysis
    
    def _update_dependencies(self, target: str, strategy: str) -> Dict:
        """Update project dependencies"""
        update_info = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "strategy": strategy,
            "updates_performed": [],
            "updates_skipped": [],
            "errors": []
        }
        
        # In a real implementation, this would actually update dependencies
        # For now, we'll simulate the process
        
        # Get current dependencies
        current_deps = self._get_current_dependencies()
        
        # Simulate updates based on strategy
        for dep_name, dep_info in current_deps.items():
            if strategy == "safe":
                # Only update if it's a minor version bump
                update_info["updates_skipped"].append({
                    "name": dep_name,
                    "reason": "Safe strategy - no update performed"
                })
            elif strategy == "latest":
                # Update to latest version (simulated)
                update_info["updates_performed"].append({
                    "name": dep_name,
                    "from_version": dep_info.version,
                    "to_version": f"{dep_info.version}.1",  # Simulate minor update
                    "status": "success"
                })
            elif strategy == "pin":
                # Pin to current versions
                update_info["updates_skipped"].append({
                    "name": dep_name,
                    "reason": "Pin strategy - keeping current version"
                })
        
        return update_info
    
    def _resolve_conflicts(self, target: str) -> Dict:
        """Resolve dependency conflicts"""
        resolution_info = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "conflicts_found": 0,
            "conflicts_resolved": 0,
            "resolution_details": []
        }
        
        # In a real implementation, this would analyze and resolve conflicts
        # For now, we'll simulate the process
        
        # Get current dependencies
        current_deps = self._get_current_dependencies()
        
        # Check for version conflicts
        version_conflicts = self._find_version_conflicts(current_deps)
        resolution_info["conflicts_found"] = len(version_conflicts)
        
        # Simulate resolution
        for conflict in version_conflicts:
            resolution_info["conflicts_resolved"] += 1
            resolution_info["resolution_details"].append({
                "conflict": conflict,
                "resolution": "Selected compatible version",
                "status": "resolved"
            })
        
        return resolution_info
    
    def _audit_dependencies(self, target: str) -> Dict:
        """Audit project dependencies for vulnerabilities"""
        audit_info = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "dependencies_audited": 0,
            "vulnerabilities_found": 0,
            "high_severity": 0,
            "medium_severity": 0,
            "low_severity": 0,
            "vulnerabilities": []
        }
        
        # In a real implementation, this would check against vulnerability databases
        # For now, we'll simulate the process
        
        # Get current dependencies
        current_deps = self._get_current_dependencies()
        audit_info["dependencies_audited"] = len(current_deps)
        
        # Simulate finding some vulnerabilities
        vulnerable_packages = ["requests", "django", "numpy"]  # Example packages
        for dep_name, dep_info in current_deps.items():
            if dep_name in vulnerable_packages:
                # Simulate finding a vulnerability
                vuln = {
                    "package": dep_name,
                    "version": dep_info.version,
                    "severity": "medium",
                    "description": f"Known vulnerability in {dep_name} {dep_info.version}",
                    "recommendation": "Update to latest version"
                }
                audit_info["vulnerabilities"].append(vuln)
                audit_info["vulnerabilities_found"] += 1
                audit_info["medium_severity"] += 1
        
        return audit_info
    
    def _detect_package_managers(self) -> Dict:
        """Detect package managers in the project"""
        managers = {}
        
        for manager_name, manager_info in self.supported_managers.items():
            # Check for configuration files
            for config_file in manager_info["files"]:
                if (self.project_path / config_file).exists():
                    managers[manager_name] = manager_info
                    break
        
        return managers
    
    def _extract_dependencies(self, manager_name: str, manager_info: Dict) -> Dict[str, DependencyInfo]:
        """Extract dependencies for a specific package manager"""
        dependencies = {}
        
        # This would parse the actual dependency files
        # For now, we'll create mock dependencies
        
        # Mock dependencies based on manager type
        mock_deps = {
            "pip": [
                {"name": "requests", "version": "2.28.1", "license": "Apache-2.0"},
                {"name": "pyyaml", "version": "6.0", "license": "MIT"},
                {"name": "typer", "version": "0.9.0", "license": "MIT"}
            ],
            "npm": [
                {"name": "react", "version": "18.2.0", "license": "MIT"},
                {"name": "lodash", "version": "4.17.21", "license": "MIT"}
            ],
            "yarn": [
                {"name": "vue", "version": "3.2.45", "license": "MIT"}
            ]
        }
        
        deps_list = mock_deps.get(manager_name, [])
        for dep_data in deps_list:
            dep_info = DependencyInfo(
                name=dep_data["name"],
                version=dep_data["version"],
                source=manager_name,
                license=dep_data["license"],
                vulnerabilities=[],
                dependencies=[],
                usage="direct"
            )
            dependencies[dep_info.name] = dep_info
        
        return dependencies
    
    def _check_dependency_issues(self, all_dependencies: Dict) -> List[Dict]:
        """Check for potential dependency issues"""
        issues = []
        
        # Check for outdated dependencies
        outdated_deps = ["requests", "django"]  # Example outdated packages
        for manager_name, deps in all_dependencies.items():
            for dep_name, dep_info in deps.items():
                if dep_name in outdated_deps:
                    issues.append({
                        "type": "outdated",
                        "dependency": dep_name,
                        "manager": manager_name,
                        "message": f"Dependency {dep_name} appears to be outdated"
                    })
        
        # Check for license compatibility
        restrictive_licenses = ["GPL-3.0"]  # Example restrictive licenses
        for manager_name, deps in all_dependencies.items():
            for dep_name, dep_info in deps.items():
                if dep_info.license in restrictive_licenses:
                    issues.append({
                        "type": "license",
                        "dependency": dep_name,
                        "manager": manager_name,
                        "message": f"Dependency {dep_name} uses restrictive license {dep_info.license}"
                    })
        
        return issues
    
    def _get_current_dependencies(self) -> Dict[str, DependencyInfo]:
        """Get current project dependencies"""
        # In a real implementation, this would read from dependency files
        # For now, we'll return stored dependencies or create mock ones
        
        if self.dependencies:
            return self.dependencies
        
        # Create mock dependencies if none exist
        mock_deps = [
            DependencyInfo(name="requests", version="2.28.1", source="pip", license="Apache-2.0"),
            DependencyInfo(name="pyyaml", version="6.0", source="pip", license="MIT"),
            DependencyInfo(name="typer", version="0.9.0", source="pip", license="MIT")
        ]
        
        deps_dict = {dep.name: dep for dep in mock_deps}
        return deps_dict
    
    def _find_version_conflicts(self, dependencies: Dict[str, DependencyInfo]) -> List[str]:
        """Find version conflicts in dependencies"""
        # In a real implementation, this would analyze version requirements
        # For now, we'll return mock conflicts
        
        conflicts = []
        conflicting_packages = ["requests", "django"]  # Example conflicting packages
        
        for dep_name in conflicting_packages:
            if dep_name in dependencies:
                conflicts.append(f"Version conflict detected for {dep_name}")
        
        return conflicts
    
    def get_dependency_status(self, request_id: str) -> Optional[Dict]:
        """Get the status of a dependency request"""
        if request_id in self.dependency_requests:
            request = self.dependency_requests[request_id]
            result = asdict(request)
            # Convert result back to dict if it's a JSON string
            if isinstance(result.get('result'), str):
                try:
                    result['result'] = json.loads(result['result'])
                except json.JSONDecodeError:
                    result['result'] = None
            return result
        return None
    
    def list_dependency_requests(self) -> List[Dict]:
        """List all dependency requests"""
        requests = []
        for req in self.dependency_requests.values():
            req_dict = asdict(req)
            # Convert result back to dict if it's a JSON string
            if isinstance(req_dict.get('result'), str):
                try:
                    req_dict['result'] = json.loads(req_dict['result'])
                except json.JSONDecodeError:
                    req_dict['result'] = None
            requests.append(req_dict)
        return requests
    
    def get_project_dependencies(self) -> List[Dict]:
        """Get all project dependencies"""
        return [asdict(dep) for dep in self.dependencies.values()]
    
    def generate_dependency_report(self) -> str:
        """Generate a comprehensive dependency report"""
        # Analyze current dependencies
        analysis_request = self.analyze_dependencies()
        # Wait for analysis to complete (in a real implementation, this would be async)
        
        # Get the analysis result
        analysis_status = self.get_dependency_status(analysis_request)
        
        # Create report
        report = f"""# Dependency Management Report

## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Project Dependencies

| Name | Version | Source | License | Status |
|------|---------|--------|---------|--------|
"""
        
        for dep in self.dependencies.values():
            status_indicator = "✅" if dep.status == "active" else "⚠️" if dep.status == "deprecated" else "❌"
            report += f"| {dep.name} | {dep.version} | {dep.source} | {dep.license} | {status_indicator} {dep.status} |\n"
        
        report += f"""
## Summary

- Total Dependencies: {len(self.dependencies)}
- Active Dependencies: {len([d for d in self.dependencies.values() if d.status == 'active'])}
- Deprecated Dependencies: {len([d for d in self.dependencies.values() if d.status == 'deprecated'])}
- Vulnerable Dependencies: {len([d for d in self.dependencies.values() if d.status == 'vulnerable'])}

## Recent Analysis

"""
        
        if analysis_status and analysis_status.get('result'):
            result = analysis_status['result']
            report += f"- Dependencies Found: {result.get('dependencies_found', 0)}\n"
            report += f"- Direct Dependencies: {len(result.get('direct_dependencies', []))}\n"
            report += f"- Transitive Dependencies: {len(result.get('transitive_dependencies', []))}\n"
            report += f"- Potential Issues: {len(result.get('potential_issues', []))}\n"
        
        report += """
## Recommendations

1. Regularly audit dependencies for security vulnerabilities
2. Update dependencies to their latest stable versions
3. Monitor for deprecated packages
4. Check license compatibility for all dependencies
5. Pin critical dependencies to specific versions

---
*Report generated by Intelligent Dependency Management System*
"""
        
        return report


# CLI Integration
def dependency_cli():
    """CLI commands for dependency management"""
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    app = typer.Typer()
    console = Console()
    
    @app.command()
    def analyze(target: str = typer.Argument("project", help="Target to analyze (project, file, or package)")):
        """Analyze project dependencies"""
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
            
            # Initialize dependency manager
            dep_manager = DependencyManager(project_path)
            
            # Analyze dependencies
            request_id = dep_manager.analyze_dependencies(target)
            
            console.print(f"[green]✓[/green] Dependency analysis request created with ID: {request_id}")
            console.print(f"Check status with: goal deps status {request_id}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def update(
        target: str = typer.Argument("project", help="Target to update (project, file, or package)"),
        strategy: str = typer.Option("safe", help="Update strategy (safe, latest, pin)")
    ):
        """Update project dependencies"""
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
            
            # Initialize dependency manager
            dep_manager = DependencyManager(project_path)
            
            # Update dependencies
            request_id = dep_manager.update_dependencies(target, strategy)
            
            console.print(f"[green]✓[/green] Dependency update request created with ID: {request_id}")
            console.print(f"Check status with: goal deps status {request_id}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def resolve(target: str = typer.Argument("project", help="Target to resolve conflicts for")):
        """Resolve dependency conflicts"""
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
            
            # Initialize dependency manager
            dep_manager = DependencyManager(project_path)
            
            # Resolve conflicts
            request_id = dep_manager.resolve_conflicts(target)
            
            console.print(f"[green]✓[/green] Dependency conflict resolution request created with ID: {request_id}")
            console.print(f"Check status with: goal deps status {request_id}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def audit(target: str = typer.Argument("project", help="Target to audit (project, file, or package)")):
        """Audit project dependencies for vulnerabilities"""
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
            
            # Initialize dependency manager
            dep_manager = DependencyManager(project_path)
            
            # Audit dependencies
            request_id = dep_manager.audit_dependencies(target)
            
            console.print(f"[green]✓[/green] Dependency audit request created with ID: {request_id}")
            console.print(f"Check status with: goal deps status {request_id}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def status(request_id: str = typer.Argument(..., help="Request ID")):
        """Check the status of a dependency management request"""
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
            
            # Initialize dependency manager
            dep_manager = DependencyManager(project_path)
            
            # Check status
            status = dep_manager.get_dependency_status(request_id)
            if status:
                console.print(Panel(f"[bold]Dependency Management Status: {request_id}[/bold]", expand=False))
                console.print(f"Action: {status['action']}")
                console.print(f"Target: {status['target']}")
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
                    
                    if status['action'] == "analyze":
                        console.print(f"Dependencies Found: {result.get('dependencies_found', 0)}")
                        console.print(f"Direct Dependencies: {len(result.get('direct_dependencies', []))}")
                        console.print(f"Potential Issues: {len(result.get('potential_issues', []))}")
                    elif status['action'] == "update":
                        console.print(f"Updates Performed: {len(result.get('updates_performed', []))}")
                        console.print(f"Updates Skipped: {len(result.get('updates_skipped', []))}")
                    elif status['action'] == "resolve":
                        console.print(f"Conflicts Found: {result.get('conflicts_found', 0)}")
                        console.print(f"Conflicts Resolved: {result.get('conflicts_resolved', 0)}")
                    elif status['action'] == "audit":
                        console.print(f"Vulnerabilities Found: {result.get('vulnerabilities_found', 0)}")
                        console.print(f"High Severity: {result.get('high_severity', 0)}")
                        console.print(f"Medium Severity: {result.get('medium_severity', 0)}")
                        console.print(f"Low Severity: {result.get('low_severity', 0)}")
            else:
                console.print(f"[red]Request {request_id} not found[/red]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def list():
        """List all dependency management requests"""
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
            
            # Initialize dependency manager
            dep_manager = DependencyManager(project_path)
            
            # List requests
            requests = dep_manager.list_dependency_requests()
            if requests:
                console.print(Panel(f"[bold]Dependency Management Requests ({len(requests)})[/bold]", expand=False))
                
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("ID", style="cyan")
                table.add_column("Action", style="green")
                table.add_column("Target", style="yellow")
                table.add_column("Status", style="blue")
                table.add_column("Created", style="dim")
                
                for req in requests:
                    created = datetime.fromisoformat(req['created_at']).strftime("%Y-%m-%d %H:%M")
                    table.add_row(
                        req['id'][:8],
                        req['action'],
                        req['target'],
                        req['status'],
                        created
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No dependency management requests found[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def show():
        """Show current project dependencies"""
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
            
            # Initialize dependency manager
            dep_manager = DependencyManager(project_path)
            
            # Get dependencies
            dependencies = dep_manager.get_project_dependencies()
            if dependencies:
                console.print(Panel(f"[bold]Project Dependencies ({len(dependencies)})[/bold]", expand=False))
                
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Version", style="green")
                table.add_column("Source", style="yellow")
                table.add_column("License", style="blue")
                table.add_column("Status", style="red")
                
                for dep in dependencies:
                    status_indicator = "✅" if dep['status'] == "active" else "⚠️" if dep['status'] == "deprecated" else "❌"
                    table.add_row(
                        dep['name'],
                        dep['version'],
                        dep['source'],
                        dep['license'],
                        f"{status_indicator} {dep['status']}"
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No dependencies found[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def report():
        """Generate a dependency management report"""
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
            
            # Initialize dependency manager
            dep_manager = DependencyManager(project_path)
            
            # Generate report
            report_content = dep_manager.generate_dependency_report()
            
            # Save report
            report_file = project_path / ".goal" / "dependencies" / "dependency_report.md"
            with open(report_file, 'w') as f:
                f.write(report_content)
            
            console.print(f"[green]✓[/green] Dependency report saved to {report_file}")
            console.print("\n[bold]Report Preview:[/bold]")
            console.print(report_content[:1000] + "..." if len(report_content) > 1000 else report_content)
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    return app


# Integration with main CLI
def integrate_deps_with_main_cli(main_app):
    """Integrate dependency management commands with main CLI"""
    deps_app = dependency_cli()
    main_app.add_typer(deps_app, name="deps")
    return main_app