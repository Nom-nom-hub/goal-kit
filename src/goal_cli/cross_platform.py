"""
Cross-Platform Scripting Capabilities for goal-dev-spec
Exceeds spec-kit functionality with advanced cross-platform scripting support.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Optional, Union
import yaml
import json


class CrossPlatformScriptManager:
    """Manages cross-platform scripting capabilities"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.scripts_path = project_path / "scripts"
        self.scripts_path.mkdir(exist_ok=True)
        
        # Platform detection
        self.platform = platform.system().lower()
        self.is_windows = self.platform == "windows"
        self.is_linux = self.platform == "linux"
        self.is_mac = self.platform == "darwin"
        
        # Script extensions by platform
        self.script_extensions = {
            "windows": ".ps1",  # PowerShell
            "linux": ".sh",     # Bash
            "darwin": ".sh"     # Bash
        }
        
        # Default script extension for current platform
        self.default_extension = self.script_extensions.get(self.platform, ".sh")
        
        # Script interpreters by platform
        self.script_interpreters = {
            "windows": "powershell.exe",
            "linux": "/bin/bash",
            "darwin": "/bin/bash"
        }
        
        # Default interpreter for current platform
        self.default_interpreter = self.script_interpreters.get(self.platform, "/bin/bash")
    
    def create_script(self, name: str, content: str, platform: str = None, 
                     interpreter: str = None) -> str:
        """
        Create a cross-platform script
        
        Args:
            name: Script name (without extension)
            content: Script content
            platform: Target platform (windows, linux, darwin) or None for current
            interpreter: Script interpreter or None for default
            
        Returns:
            Path to created script
        """
        if platform is None:
            platform = self.platform
            
        extension = self.script_extensions.get(platform, ".sh")
        script_path = self.scripts_path / f"{name}{extension}"
        
        # Write script content
        with open(script_path, 'w', newline='\n') as f:
            # Add shebang for Unix-like systems
            if platform in ["linux", "darwin"]:
                interp = interpreter or self.script_interpreters.get(platform, "/bin/bash")
                f.write(f"#!/usr/bin/env {interp}\n\n")
            f.write(content)
        
        # Make script executable on Unix-like systems
        if platform in ["linux", "darwin"]:
            os.chmod(script_path, 0o755)
        
        return str(script_path)
    
    def create_cross_platform_script(self, name: str, scripts: Dict[str, str]) -> Dict[str, str]:
        """
        Create scripts for multiple platforms
        
        Args:
            name: Base script name
            scripts: Dictionary with platform as key and script content as value
                        e.g., {"windows": "...", "linux": "...", "darwin": "..."}
                        
        Returns:
            Dictionary with platform as key and script path as value
        """
        created_scripts = {}
        
        for plat, content in scripts.items():
            if plat in self.script_extensions:
                path = self.create_script(name, content, platform=plat)
                created_scripts[plat] = path
        
        return created_scripts
    
    def execute_script(self, script_path: Union[str, Path], 
                      arguments: List[str] = None,
                      capture_output: bool = True,
                      timeout: int = 300) -> Dict:
        """
        Execute a script in a cross-platform manner
        
        Args:
            script_path: Path to script file
            arguments: List of arguments to pass to script
            capture_output: Whether to capture stdout/stderr
            timeout: Timeout in seconds
            
        Returns:
            Dictionary with execution results
        """
        script_path = Path(script_path)
        arguments = arguments or []
        
        # Determine interpreter based on script extension
        if script_path.suffix == ".ps1":
            # PowerShell script
            if self.is_windows:
                cmd = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", str(script_path)] + arguments
            else:
                # Try to use pwsh if available on Unix-like systems
                if self._is_command_available("pwsh"):
                    cmd = ["pwsh", "-ExecutionPolicy", "Bypass", "-File", str(script_path)] + arguments
                else:
                    return {
                        "success": False,
                        "error": "PowerShell not available on this platform",
                        "return_code": -1
                    }
        elif script_path.suffix == ".sh":
            # Shell script
            if self.is_windows:
                # Try to use bash if available on Windows (WSL, Git Bash, etc.)
                if self._is_command_available("bash"):
                    cmd = ["bash", str(script_path)] + arguments
                else:
                    return {
                        "success": False,
                        "error": "Bash not available on this platform",
                        "return_code": -1
                    }
            else:
                # Unix-like system
                cmd = [str(script_path)] + arguments
        else:
            # Unknown script type, try to execute directly
            cmd = [str(script_path)] + arguments
        
        try:
            # Execute script
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=capture_output,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "return_code": result.returncode,
                "stdout": result.stdout if capture_output else "",
                "stderr": result.stderr if capture_output else "",
                "command": " ".join(cmd)
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Script execution timed out after {timeout} seconds",
                "return_code": -1,
                "command": " ".join(cmd)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "return_code": -1,
                "command": " ".join(cmd)
            }
    
    def _is_command_available(self, command: str) -> bool:
        """Check if a command is available in the system"""
        try:
            subprocess.run(
                ["which" if not self.is_windows else "where", command],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def create_unified_script_interface(self, name: str, operations: Dict[str, str]) -> str:
        """
        Create a unified script interface that works across platforms
        
        Args:
            name: Script name
            operations: Dictionary with operation name as key and command as value
            
        Returns:
            Path to created unified script
        """
        if self.is_windows:
            # Create PowerShell script
            content = "# Unified Script Interface (PowerShell)\n\n"
            content += f"# Script: {name}\n\n"
            
            # Add operation functions
            for op_name, command in operations.items():
                content += f"function {op_name.replace('-', '_')} {{\n"
                content += f"    Write-Host \"Executing {op_name}...\"\n"
                content += f"    {command}\n"
                content += "}\n\n"
            
            # Add main execution logic
            content += "param(\n"
            content += "    [string]$Operation\n"
            content += ")\n\n"
            content += "switch ($Operation) {\n"
            for op_name in operations.keys():
                func_name = op_name.replace('-', '_')
                content += f"    '{op_name}' {{ {func_name}; break }}\n"
            content += "    default { Write-Host \"Unknown operation: $Operation\"; exit 1 }\n"
            content += "}\n"
            
            return self.create_script(name, content, platform="windows")
        else:
            # Create Bash script
            content = "#!/bin/bash\n\n"
            content += f"# Unified Script Interface (Bash)\n"
            content += f"# Script: {name}\n\n"
            
            # Add operation functions
            for op_name, command in operations.items():
                func_name = op_name.replace('-', '_')
                content += f"{func_name}() {{\n"
                content += f"    echo \"Executing {op_name}...\"\n"
                content += f"    {command}\n"
                content += "}\n\n"
            
            # Add main execution logic
            content += "OPERATION=\"$1\"\n\n"
            content += "case \"$OPERATION\" in\n"
            for op_name in operations.keys():
                func_name = op_name.replace('-', '_')
                content += f"    {op_name}) {func_name} ;;\n"
            content += "    *) echo \"Unknown operation: $OPERATION\"; exit 1 ;;\n"
            content += "esac\n"
            
            return self.create_script(name, content, platform=self.platform)
    
    def get_platform_info(self) -> Dict:
        """Get information about the current platform"""
        return {
            "platform": self.platform,
            "is_windows": self.is_windows,
            "is_linux": self.is_linux,
            "is_mac": self.is_mac,
            "default_extension": self.default_extension,
            "default_interpreter": self.default_interpreter,
            "script_extensions": self.script_extensions,
            "script_interpreters": self.script_interpreters
        }
    
    def list_available_scripts(self) -> List[Dict]:
        """List all available scripts in the project"""
        scripts = []
        
        if self.scripts_path.exists():
            for script_file in self.scripts_path.iterdir():
                if script_file.is_file():
                    scripts.append({
                        "name": script_file.stem,
                        "path": str(script_file),
                        "extension": script_file.suffix,
                        "platform": self._detect_script_platform(script_file.suffix),
                        "size": script_file.stat().st_size
                    })
        
        return scripts
    
    def _detect_script_platform(self, extension: str) -> str:
        """Detect platform based on script extension"""
        extension_map = {
            ".ps1": "windows",
            ".sh": "unix",  # Could be linux or darwin
            ".bat": "windows",
            ".cmd": "windows"
        }
        return extension_map.get(extension, "unknown")


# CLI Integration
def cross_platform_cli():
    """CLI commands for cross-platform scripting"""
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    app = typer.Typer()
    console = Console()
    
    @app.command()
    def create(
        name: str = typer.Argument(..., help="Script name"),
        content: str = typer.Argument(..., help="Script content"),
        platform: str = typer.Option(None, help="Target platform (windows, linux, darwin)"),
        interpreter: str = typer.Option(None, help="Script interpreter")
    ):
        """Create a cross-platform script"""
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
            
            # Initialize script manager
            script_manager = CrossPlatformScriptManager(project_path)
            
            # Create script
            script_path = script_manager.create_script(name, content, platform, interpreter)
            
            console.print(f"[green]✓[/green] Created script: {script_path}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def execute(
        script_path: str = typer.Argument(..., help="Path to script file"),
        arguments: str = typer.Option("", help="Arguments to pass to script (comma-separated)")
    ):
        """Execute a script"""
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
            
            # Initialize script manager
            script_manager = CrossPlatformScriptManager(project_path)
            
            # Parse arguments
            arg_list = [arg.strip() for arg in arguments.split(",") if arg.strip()] if arguments else []
            
            # Execute script
            result = script_manager.execute_script(script_path, arg_list)
            
            if result["success"]:
                console.print(f"[green]✓[/green] Script executed successfully")
                if result.get("stdout"):
                    console.print("\n[bold]Output:[/bold]")
                    console.print(result["stdout"])
            else:
                console.print(f"[red]✗[/red] Script execution failed")
                if result.get("error"):
                    console.print(f"[red]Error:[/red] {result['error']}")
                if result.get("stderr"):
                    console.print("\n[bold]Error Output:[/bold]")
                    console.print(result["stderr"])
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def info():
        """Show platform information"""
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
            
            # Initialize script manager
            script_manager = CrossPlatformScriptManager(project_path)
            
            # Get platform info
            info = script_manager.get_platform_info()
            
            console.print(Panel("[bold]Cross-Platform Scripting Information[/bold]", expand=False))
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Property", style="dim")
            table.add_column("Value")
            
            for key, value in info.items():
                table.add_row(key, str(value))
            
            console.print(table)
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def list():
        """List available scripts"""
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
            
            # Initialize script manager
            script_manager = CrossPlatformScriptManager(project_path)
            
            # List scripts
            scripts = script_manager.list_available_scripts()
            
            if scripts:
                console.print(Panel(f"[bold]Available Scripts ({len(scripts)})[/bold]", expand=False))
                
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Name", style="cyan")
                table.add_column("Platform", style="green")
                table.add_column("Path", style="dim")
                table.add_column("Size", style="yellow")
                
                for script in scripts:
                    table.add_row(
                        script["name"],
                        script["platform"],
                        script["path"],
                        f"{script['size']} bytes"
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No scripts found in the project[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    return app


# Integration with main CLI
def integrate_cross_platform_with_main_cli(main_app):
    """Integrate cross-platform scripting commands with main CLI"""
    cross_platform_app = cross_platform_cli()
    main_app.add_typer(cross_platform_app, name="script")
    return main_app