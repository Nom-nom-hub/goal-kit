#!/usr/bin/env python3
"""
Goal-Dev-Spec CLI - A goal-driven development specification system using YAML
"""

import os
import sys
import subprocess
from pathlib import Path

import typer
import yaml  # type: ignore[import-untyped]
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

# Import our modules
from .goals import GoalManager
from .specs import SpecManager
from .ui_components import (
    show_banner,
    BannerGroup,
    # StepTracker is imported but not used - keeping for potential re-export
    AI_CHOICES,
    SCRIPT_TYPE_CHOICES,
    check_tool,
    ensure_executable_scripts
)
from .analytics import PredictiveAnalyticsEngine, integrate_analytics_with_main_cli
from .enhanced_ui import EnhancedStepTracker, ProgressDisplayManager, NotificationManager, ErrorHandler
from .governance_system import GovernanceSystem
from .enhanced_quality_assurance import integrate_quality_assurance_with_main_cli
from .testing_integration import integrate_testing_with_main_cli
from .real_time_monitoring import integrate_monitoring_with_main_cli
from .automation import integrate_automation_with_main_cli
from .cross_platform import integrate_cross_platform_with_main_cli
from .ai_code import integrate_ai_code_with_main_cli
from .documentation import integrate_docs_with_main_cli
from .cicd import integrate_cicd_with_main_cli
from .dependencies import integrate_deps_with_main_cli
from .scaffolding import integrate_scaffold_with_main_cli
from .testing_quality import integrate_testing_with_main_cli as integrate_testing_quality_with_main_cli
from .performance_tools import integrate_performance_with_main_cli
from .security_scanner import integrate_security_with_main_cli

# Initialize Rich console
console = Console()

# Initialize Typer app with custom banner group
app = typer.Typer(
    name="goal",
    help="Goal-driven development specification system using YAML",
    add_completion=False,
    cls=BannerGroup,
    invoke_without_command=True,
)

def get_project_path() -> Path:
    """Find the project root directory."""
    current_path = Path.cwd()
    while current_path != current_path.parent:
        if (current_path / ".goal" / "goal.yaml").exists():
            return current_path
        current_path = current_path.parent
    raise ValueError("Not in a goal-dev-spec project directory. Run 'goal init' first.")



@app.command()
def init(
    project_name: str = typer.Argument(None, help="Name of the project directory to create. If not provided, you'll be prompted to enter one."),
    ai_assistant: str = typer.Option(None, "--ai", help="AI assistant to use: claude, gemini, copilot, cursor, qwen, opencode, codex, windsurf, kilocode, or auggie"),
    script_type: str = typer.Option(None, "--script", help="Script type to use: sh or ps"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    force: bool = typer.Option(False, "--force", "-f", help="Force creation even if directory exists"),
    here: bool = typer.Option(False, "--here", help="Initialize project in the current directory instead of creating a new one")
):
    """
    Initialize a new goal-dev-spec project with advanced features.
    
    This command will:
    1. Let you choose your AI assistant (Claude Code, Gemini CLI, GitHub Copilot, Cursor, Qwen Code, opencode, Codex CLI, Windsurf, Kilo Code, or Auggie CLI)
    2. Set up the appropriate project structure with templates
    3. Initialize a fresh git repository (if not --no-git and no existing repo)
    4. Provide interactive setup with live progress tracking
    
    Examples:
        goal init my-project
        goal init my-project --ai claude
        goal init my-project --ai gemini
        goal init my-project --ai copilot --no-git
        goal init --here --ai claude
        goal init --here
    """
    try:
        # Show banner first
        show_banner()
        
        # Validate arguments
        if here and project_name:
            console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
            raise typer.Exit(1)
        
        if not here and not project_name:
            # If no project name provided, ask the user
            from .ui_components import get_user_input, validate_project_name
            project_name = get_user_input("Enter project name", "my-goal-project", validate_project_name)
        
        # Ask for project description
        from .ui_components import get_user_input
        project_description = get_user_input(
            "Enter project description",
            "A goal-driven development project",
            lambda x: x  # No validation needed for description
        )
        
        # Determine project directory
        if here:
            project_name = Path.cwd().name
            project_path = Path.cwd()
            
            # Check if current directory has any files
            existing_items = [item for item in project_path.iterdir()]
            if existing_items and not force:
                console.print(f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)")
                console.print("[yellow]Template files will be merged with existing content and may overwrite existing files[/yellow]")
                # Ask for confirmation
                response = typer.confirm("Do you want to continue?")
                if not response:
                    console.print("[yellow]Operation cancelled[/yellow]")
                    raise typer.Exit(0)
        else:
            project_path = Path(project_name).resolve()
            # Check if project directory already exists
            if project_path.exists() and not force:
                error_panel = Panel(
                    f"Directory '[cyan]{project_name}[/cyan]' already exists\n"
                    "Please choose a different project name or remove the existing directory.",
                    title="[red]Directory Conflict[/red]",
                    border_style="red",
                    padding=(1, 2)
                )
                console.print()
                console.print(error_panel)
                raise typer.Exit(1)
        
        # Create formatted setup info with column alignment
        current_dir = Path.cwd()
        
        setup_lines = [
            "[cyan]Goal-Dev-Spec Project Setup[/cyan]",
            "",
            f"{'Project':<15} [green]{project_path.name}[/green]",
            f"{'Working Path':<15} [dim]{current_dir}[/dim]",
        ]
        
        # Add target path only if different from working dir
        if not here:
            setup_lines.append(f"{'Target Path':<15} [dim]{project_path}[/dim]")
        
        console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))
        
        # AI assistant selection
        if ai_assistant:
            from .ui_components import validate_ai_assistant
            try:
                validate_ai_assistant(ai_assistant, AI_CHOICES)
                selected_ai = ai_assistant
                
                # Check if the selected AI assistant tool is installed
                ai_tool_map = {
                    "claude": "claude",
                    "gemini": "gemini",
                    "copilot": "code",  # GitHub Copilot is typically available in VS Code
                    "cursor": "cursor-agent",
                    "qwen": "qwen",
                    "opencode": "opencode",
                    "codex": "codex",
                    "windsurf": "windsurf",
                    "kilocode": "kilocode",
                    "auggie": "auggie",
                }
                
                if selected_ai in ai_tool_map:
                    ai_tool = ai_tool_map[selected_ai]
                    if not check_tool(ai_tool):
                        install_urls = {
                            "claude": "https://docs.anthropic.com/en/docs/claude-code/setup",
                            "gemini": "https://github.com/google-gemini/gemini-cli",
                            "qwen": "https://github.com/QwenLM/qwen-code",
                            "opencode": "https://opencode.ai",
                            "codex": "https://github.com/openai/codex",
                            "auggie": "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli",
                            # GitHub Copilot and Cursor checks are not needed as they're typically available in supported IDEs
                        }
                        
                        if ai_tool in install_urls:
                            install_url = install_urls[ai_tool]
                            warning_panel = Panel(
                                f"[cyan]{selected_ai}[/cyan] not found\n"
                                f"Install with: [cyan]{install_url}[/cyan]\n"
                                f"{AI_CHOICES[selected_ai]} is required to continue with this project type.\n\n"
                                "Tip: Install the AI assistant tool or use a different assistant",
                                title="[yellow]AI Assistant Not Found[/yellow]",
                                border_style="yellow",
                                padding=(1, 2)
                            )
                            console.print()
                            console.print(warning_panel)
                            raise typer.Exit(1)
            except ValueError as e:
                console.print(f"[red]Error:[/red] {e}")
                raise typer.Exit(1)
        else:
            # Use arrow-key selection interface
            from .ui_components import select_with_arrows
            selected_ai = select_with_arrows(
                AI_CHOICES,
                "Choose your AI assistant:",
                "claude"
            )

            # Check if the selected AI assistant tool is installed
            ai_tool_map = {
                "claude": "claude",
                "gemini": "gemini",
                "copilot": "code",  # GitHub Copilot is typically available in VS Code
                "cursor": "cursor-agent",
                "qwen": "qwen",
                "opencode": "opencode",
                "codex": "codex",
                "windsurf": "windsurf",
                "kilocode": "kilocode",
                "auggie": "auggie",
            }

            if selected_ai in ai_tool_map:
                ai_tool = ai_tool_map[selected_ai]
                if not check_tool(ai_tool):
                    install_urls = {
                        "claude": "https://docs.anthropic.com/en/docs/claude-code/setup",
                        "gemini": "https://github.com/google-gemini/gemini-cli",
                        "qwen": "https://github.com/QwenLM/qwen-code",
                        "opencode": "https://opencode.ai",
                        "codex": "https://github.com/openai/codex",
                        "auggie": "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli",
                        # GitHub Copilot and Cursor checks are not needed as they're typically available in supported IDEs
                    }

                    if ai_tool in install_urls:
                        install_url = install_urls[ai_tool]
                        warning_panel = Panel(
                            f"[cyan]{selected_ai}[/cyan] not found\n"
                            f"Install with: [cyan]{install_url}[/cyan]\n"
                            f"{AI_CHOICES[selected_ai]} is required to continue with this project type.\n\n"
                            "Tip: Install the AI assistant tool or use a different assistant",
                            title="[yellow]AI Assistant Not Found[/yellow]",
                            border_style="yellow",
                            padding=(1, 2)
                        )
                        console.print()
                        console.print(warning_panel)
                        raise typer.Exit(1)

            # Determine script type (explicit, interactive, or OS default)
        if script_type:
            if script_type not in SCRIPT_TYPE_CHOICES:
                console.print(f"[red]Error:[/red] Invalid script type '{script_type}'. Choose from: {', '.join(SCRIPT_TYPE_CHOICES.keys())}")
                raise typer.Exit(1)
            selected_script = script_type
        else:
            # Auto-detect default
            default_script = "ps" if os.name == "nt" else "sh"
            # Provide interactive selection similar to AI if stdin is a TTY
            if sys.stdin.isatty():
                from .ui_components import select_with_arrows
                selected_script = select_with_arrows(SCRIPT_TYPE_CHOICES, "Choose script type", default_script)
            else:
                selected_script = default_script
        
        console.print(f"[cyan]Selected AI assistant:[/cyan] {selected_ai}")
        console.print(f"[cyan]Selected script type:[/cyan] {selected_script}")
        
        # Create project with enhanced step tracking
        tracker = EnhancedStepTracker("Initialize Goal-Dev-Spec Project", total_steps=8)
        progress_manager = ProgressDisplayManager(tracker)
        notification_manager = NotificationManager()
        error_handler = ErrorHandler(tracker)
        
        # Pre steps recorded as completed before live rendering
        tracker.add("precheck", "Check required tools")
        tracker.complete("precheck", "ok")
        tracker.add("ai-select", "Select AI assistant")
        tracker.complete("ai-select", f"{selected_ai}")
        tracker.add("script-select", "Select script type")
        tracker.complete("script-select", selected_script)
        for key, label in [
            ("create-dirs", "Create directory structure"),
            ("config", "Create configuration files"),
            ("templates", "Create template files"),
            ("git", "Initialize git repository"),
            ("final", "Finalize")
        ]:
            tracker.add(key, label)

        # Start the enhanced progress display
        progress_manager.start()
        
        try:
            # Create project directory
            if not here:
                project_path.mkdir(parents=True, exist_ok=True)
            
            tracker.start("create-dirs", "Creating project structure")
            # Create directory structure
            dirs_to_create = [
                ".goal",
                ".goal/goals",
                ".goal/specs",
                ".goal/plans",
                ".goal/tasks",
                ".goal/templates",
                ".goal/agents",
                ".goal/analytics",
                f"scripts/{'powershell' if selected_script == 'ps' else 'bash'}",
                f".goal/agents/{selected_ai}"
            ]
            
            for dir_name in dirs_to_create:
                (project_path / dir_name).mkdir(parents=True, exist_ok=True)
            
            tracker.complete("create-dirs", "Project structure created")
            
            # Create initial configuration file
            tracker.start("config", "Creating configuration files")
            config = {
                "project": {
                    "name": project_name,
                    "version": "0.1.0",
                    "description": project_description
                },
                "settings": {
                    "default_agent": selected_ai
                }
            }
                    
            with open(project_path / ".goal" / "goal.yaml", "w") as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            tracker.complete("config", "Configuration files created")
                    
            # Create template files
            tracker.start("templates", "Creating template files")
            templates_dir = project_path / ".goal" / "templates"
            
            # Create directories for different template types
            md_templates_dir = templates_dir / "md"
            md_templates_dir.mkdir(exist_ok=True)
            
            commands_templates_dir = md_templates_dir / "commands"
            commands_templates_dir.mkdir(exist_ok=True)
            
            # Copy advanced Markdown templates
            import shutil
            package_templates_dir = Path(__file__).parent.parent.parent / "templates" / "md"
            if package_templates_dir.exists():
                # Copy all markdown templates
                for template_file in package_templates_dir.glob("*.md"):
                    shutil.copy2(template_file, md_templates_dir)
                
                # Copy commands templates if they exist
                commands_source_dir = package_templates_dir / "commands"
                if commands_source_dir.exists():
                    for cmd_template in commands_source_dir.glob("*.md"):
                        shutil.copy2(cmd_template, commands_templates_dir)
            
            # Copy script templates
            package_scripts_dir = Path(__file__).parent.parent.parent / "scripts"
            if package_scripts_dir.exists():
                scripts_target_dir = project_path / "scripts"
                scripts_target_dir.mkdir(exist_ok=True)
                
                # Copy bash scripts
                bash_source_dir = package_scripts_dir / "bash"
                bash_target_dir = scripts_target_dir / "bash"
                bash_target_dir.mkdir(exist_ok=True)
                if bash_source_dir.exists():
                    for script_file in bash_source_dir.glob("*.sh"):
                        shutil.copy2(script_file, bash_target_dir)
                
                # Copy PowerShell scripts
                ps_source_dir = package_scripts_dir / "powershell"
                ps_target_dir = scripts_target_dir / "powershell"
                ps_target_dir.mkdir(exist_ok=True)
                if ps_source_dir.exists():
                    for script_file in ps_source_dir.glob("*.ps1"):
                        shutil.copy2(script_file, ps_target_dir)
            
            # Goal YAML template (for backward compatibility)
            goal_template = {
                "id": "",
                "title": "",
                "description": "",
                "objectives": [],
                "success_criteria": [],
                "dependencies": [],
                "related_goals": [],
                "priority": "medium",
                "status": "draft",
                "created_at": "",
                "updated_at": "",
                "owner": "",
                "tags": [],
                "metadata": {}
            }
            
            with open(templates_dir / "goal-template.yaml", "w") as f:
                yaml.dump(goal_template, f, default_flow_style=False, sort_keys=False)
            
            # Spec YAML template (for backward compatibility)
            spec_template = {
                "id": "",
                "goal_id": "",
                "title": "",
                "description": "",
                "user_stories": [],
                "acceptance_criteria": [],
                "functional_requirements": [],
                "non_functional_requirements": [],
                "constraints": [],
                "assumptions": [],
                "out_of_scope": [],
                "created_at": "",
                "updated_at": "",
                "status": "draft",
                "metadata": {}
            }
            
            with open(templates_dir / "spec-template.yaml", "w") as f:
                yaml.dump(spec_template, f, default_flow_style=False, sort_keys=False)
            
            # Plan YAML template (for backward compatibility)
            plan_template = {
                "id": "",
                "goal_id": "",
                "spec_id": "",
                "title": "",
                "description": "",
                "tasks": [],
                "timeline": "",
                "resources": [],
                "risks": [],
                "dependencies": [],
                "created_at": "",
                "updated_at": "",
                "status": "draft",
                "metadata": {}
            }
            
            with open(templates_dir / "plan-template.yaml", "w") as f:
                yaml.dump(plan_template, f, default_flow_style=False, sort_keys=False)
                            
            # Tasks YAML template (for backward compatibility)
            tasks_template = {
                "id": "",
                "plan_id": "",
                "title": "",
                "description": "",
                "status": "todo",
                "priority": "medium",
                "assignee": "",
                "due_date": "",
                "dependencies": [],
                "created_at": "",
                "updated_at": "",
                "metadata": {}
            }
            
            with open(templates_dir / "tasks-template.yaml", "w") as f:
                yaml.dump(tasks_template, f, default_flow_style=False, sort_keys=False)
            tracker.complete("templates", "Template files created")
                    
            # Ensure scripts are executable (POSIX)
            tracker.start("chmod", "Setting script permissions")
            ensure_executable_scripts(project_path, tracker=tracker)  # type: ignore[arg-type]
            tracker.complete("chmod", "Script permissions set")
                    
            # Git step
            tracker.start("git", "Initializing git repository")
            if not no_git:
                try:
                    # Check if we're already in a git repository
                    from .ui_components import is_git_repo
                    if is_git_repo(project_path):
                        tracker.complete("git", "existing repo detected")
                    else:
                        # Initialize git repository
                        original_cwd = Path.cwd()
                        os.chdir(project_path)
                        subprocess.run(["git", "init"], check=True, capture_output=True)
                        subprocess.run(["git", "add", "."], check=True, capture_output=True)
                        subprocess.run(["git", "commit", "-m", "Initial commit from Goal-Dev-Spec template"], check=True, capture_output=True)
                        tracker.complete("git", "initialized")
                except subprocess.CalledProcessError as e:
                    tracker.skip("git", f"git not available or failed: {str(e)[:50]}...")
                except Exception as e:
                    tracker.skip("git", f"git error: {str(e)[:50]}...")
                finally:
                    if 'original_cwd' in locals():
                        os.chdir(original_cwd)
            else:
                tracker.skip("git", "--no-git flag")
                    
            tracker.complete("final", "project ready")
        except Exception as e:
            tracker.error("final", str(e))
            notification_manager.notify(f"Initialization failed: {e}", "error")
            console.print(Panel(f"Initialization failed: {e}", title="Failure", border_style="red"))
            if not here and project_path.exists():
                import shutil
                shutil.rmtree(project_path)
            progress_manager.stop()
            raise typer.Exit(1)
        finally:
            # Stop the progress display
            progress_manager.stop()

        # Show completion notification
        notification_manager.notify("Project initialization completed successfully!", "success")
        console.print("\n[bold green]Project ready.[/bold green]")
        
        # Agent folder security notice
        agent_folder_map = {
            "claude": ".claude/",
            "gemini": ".gemini/",
            "cursor": ".cursor/",
            "qwen": ".qwen/",
            "opencode": ".opencode/",
            "codex": ".codex/",
            "windsurf": ".windsurf/",
            "kilocode": ".kilocode/",
            "auggie": ".augment/",
            "copilot": ".github/",
        }
        
        if selected_ai in agent_folder_map:
            agent_folder = agent_folder_map[selected_ai]
            security_notice = Panel(
                f"Some agents may store credentials, auth tokens, or other identifying and private artifacts in the agent folder within your project.\n"
                f"Consider adding [cyan]{agent_folder}[/cyan] (or parts of it) to [cyan].gitignore[/cyan] to prevent accidental credential leakage.",
                title="[yellow]Agent Folder Security[/yellow]",
                border_style="yellow",
                padding=(1, 2)
            )
            console.print()
            console.print(security_notice)
        
        # Boxed "Next steps" section
        steps_lines = []
        if not here:
            steps_lines.append(f"1. Go to the project folder: [cyan]cd {project_name}[/cyan]")
            step_num = 2
        else:
            steps_lines.append("1. You're already in the project directory!")
            step_num = 2

        steps_lines.append(f"{step_num}. Start creating goals and specifications:")
        steps_lines.append('   2.1 [cyan]goal create "Your first goal"[/]')
        steps_lines.append("   2.2 [cyan]goal plan <goal-id>[/] - Create implementation plans")
        steps_lines.append("   2.3 [cyan]goal tasks <plan-id>[/] - Generate actionable tasks")
        steps_lines.append("   2.4 [cyan]goal track[/] - Track progress")

        steps_panel = Panel("\n".join(steps_lines), title="Next Steps", border_style="cyan", padding=(1,2))
        console.print()
        console.print(steps_panel)
        
    except typer.Exit:
        # Re-raise typer.Exit exceptions
        raise
    except Exception as e:
        console.print(f"[red]Unexpected error during initialization:[/red] {e}")
        raise typer.Exit(1)

@app.command()
def create(
    goal_description: str = typer.Argument(..., help="Description of the goal to create. This should be a clear, concise statement of what you want to accomplish.")
):
    """
    Create a new goal specification with predictive analytics.
    
    This command creates a new goal with the specified description and automatically 
    generates a corresponding feature specification. The goal will be created with:
    - A unique ID
    - The provided description as the title
    - Default status of 'draft'
    - Current timestamp for creation date
    - Predictive analytics for complexity, estimated completion time, and risk factors
    
    Examples:
        goal create "Implement user authentication system"
        goal create "Add real-time chat functionality to the application"
        goal create "Optimize database queries for better performance"
    """
    try:
        project_path = get_project_path()
        goal_manager = GoalManager(project_path)
        
        # For simplicity, we'll use the first few words as the title
        title = goal_description.split(".")[0][:50]  # First sentence, max 50 chars
        if len(title) < len(goal_description.split(".")[0]):
            title += "..."
        
        # Validate inputs
        if not title.strip():
            console.print("[red]Error:[/red] Goal title cannot be empty")
            raise typer.Exit(1)
            
        if not goal_description.strip():
            console.print("[red]Error:[/red] Goal description cannot be empty")
            raise typer.Exit(1)
        
        # Create initial goal data
        goal_data = {
            "title": title.strip(),
            "description": goal_description.strip(),
            "objectives": [],
            "success_criteria": [],
            "dependencies": [],
            "related_goals": [],
            "priority": "medium",
            "status": "draft",
            "owner": "",
            "tags": [],
            "metadata": {}
        }
        
        # Apply predictive analytics
        console.print("[cyan]Analyzing goal with predictive analytics...[/cyan]")
        analytics_engine = PredictiveAnalyticsEngine(project_path)
        enhanced_goal = analytics_engine.enhance_goal_with_analytics(goal_data)
        
        # Create goal with enhanced data
        goal_id = goal_manager.create_goal_from_data(enhanced_goal)
        console.print(f"[green][+][/green] Created goal [bold]{title}[/bold] with ID: {goal_id}")
        
        # Show analytics results
        analytics = enhanced_goal['metadata']['predictive_analytics']
        console.print(f"[cyan]Estimated completion:[/cyan] {analytics['estimated_completion_days']} days")
        if analytics['risk_factors']:
            console.print(f"[yellow]Risk factors identified:[/yellow] {', '.join(analytics['risk_factors'])}")
        
        # Also create a specification for this goal
        spec_manager = SpecManager(project_path)
        spec_id = spec_manager.create_spec(goal_id, title, goal_description)
        console.print(f"[green][+][/green] Created specification with ID: {spec_id}")
        
    except ValueError as e:
        console.print(f"[red]Validation error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)

@app.command()
def plan(
    goal_id: str = typer.Argument(..., help="ID of the goal to create a plan for. You can find goal IDs using 'goal list'")
):
    """
    Create an implementation plan for a goal.
    
    This command generates an implementation plan for the specified goal, including:
    - Task breakdown with estimated effort
    - Timeline and milestone definition
    - Resource allocation recommendations
    - Risk identification and mitigation strategies
    
    Examples:
        goal plan abc123
        goal plan xyz789
    """
    console.print(f"[green][+][/green] Creating plan for goal: {goal_id}")
    # TODO: Implement plan creation logic

@app.command()
def tasks(
    plan_id: str = typer.Argument(..., help="ID of the plan to generate tasks for. You can find plan IDs in the plans directory")
):
    """
    Generate task breakdown for implementation.
    
    This command breaks down an implementation plan into actionable tasks with:
    - Specific task descriptions
    - Assignees and due dates
    - Dependencies between tasks
    - Priority levels
    - Status tracking
    
    Examples:
        goal tasks plan-abc123
        goal tasks plan-xyz789
    """
    console.print(f"[green][+][/green] Generating tasks for plan: {plan_id}")
    # TODO: Implement task generation logic

@app.command()
def list():
    """
    List all goals in the project.
    
    This command displays all goals in the current project with:
    - Goal ID
    - Title
    - Creation date
    - Current status
    
    Use 'goal show <goal-id>' to view details of a specific goal.
    """
    try:
        project_path = get_project_path()
        goal_manager = GoalManager(project_path)
        
        goals = goal_manager.list_goals()
        if not goals:
            console.print("[yellow]No goals found in this project.[/yellow]")
            return
        
        table = Table(title="Goals")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Created", style="green")
        
        for goal in goals:
            table.add_row(
                goal["id"],
                goal["title"],
                goal["created_at"] if "created_at" in goal else "Unknown"
            )
        
        console.print(table)
        
    except ValueError as e:
        console.print(f"[red]Validation error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)

@app.command()
def show(
    goal_id: str = typer.Argument(..., help="ID of the goal to show. You can find goal IDs using 'goal list'")
):
    """
    Show details of a specific goal.
    
    This command displays detailed information about a specific goal, including:
    - Full goal description
    - Objectives and success criteria
    - Dependencies and related goals
    - Priority and status
    - Creation and update timestamps
    - Owner and tags
    
    Examples:
        goal show abc123
        goal show xyz789
    """
    try:
        project_path = get_project_path()
        goal_manager = GoalManager(project_path)
        
        goal = goal_manager.get_goal(goal_id)
        if not goal:
            console.print(f"[red]Error:[/red] Goal with ID '[bold]{goal_id}[/bold]' not found.")
            raise typer.Exit(1)
        
        console.print(Panel(f"[bold]{goal['title']}[/bold]", expand=False))
        console.print(f"ID: {goal['id']}")
        console.print(f"Status: {goal['status']}")
        console.print(f"Priority: {goal['priority']}")
        console.print(f"Description: {goal['description']}")
        
        if goal.get('objectives'):
            console.print("\n[bold]Objectives:[/bold]")
            for obj in goal['objectives']:
                console.print(f"  [*] {obj}")
        
        if goal.get('dependencies'):
            console.print("\n[bold]Dependencies:[/bold]")
            for dep in goal['dependencies']:
                console.print(f"  [*] {dep}")
        
    except ValueError as e:
        console.print(f"[red]Validation error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)

@app.command()
def track():
    """
    Track progress of goals and tasks with enhanced analytics.
    
    This command shows progress tracking information for all goals and tasks in the project:
    - Overall project progress with estimated completion times
    - Goal completion status with complexity analysis
    - Task completion rates
    - Upcoming deadlines
    - Risk factors and notifications
    - Resource utilization
    
    This helps project managers and team members stay informed about project status.
    """
    try:
        project_path = get_project_path()
        goal_manager = GoalManager(project_path)
        
        # Get all goals
        goals = goal_manager.list_goals()
        if not goals:
            console.print("[yellow]No goals found in this project.[/yellow]")
            return
        
        # Initialize analytics engine
        analytics_engine = PredictiveAnalyticsEngine(project_path)
        
        # Create a progress tracker for display
        tracker = EnhancedStepTracker("Project Progress Tracking", total_steps=len(goals))
        
        # Add all goals to the tracker
        for goal_info in goals:
            tracker.add(goal_info["id"], goal_info["title"])
        
        # Analyze each goal
        total_goals = len(goals)
        completed_goals = 0
        total_complexity = 0
        risk_factors = []
        
        console.print("[cyan]Analyzing project progress...[/cyan]")
        
        for goal_info in goals:
            goal = goal_manager.get_goal(goal_info["id"])
            if goal:
                # Update tracker
                status = goal.get("status", "draft")
                if status == "completed":
                    tracker.complete(goal_info["id"], "Completed")
                    completed_goals += 1
                elif status == "in_progress":
                    tracker.start(goal_info["id"], "In Progress")
                elif status == "blocked":
                    tracker.error(goal_info["id"], "Blocked")
                else:
                    tracker.add(goal_info["id"], goal_info["title"])
                
                # Analyze goal complexity
                complexity = analytics_engine.analyze_goal_complexity(goal)
                total_complexity += complexity["total_score"]
                
                # Collect risk factors
                risks = analytics_engine.identify_risk_factors(goal)
                for risk in risks:
                    if risk not in risk_factors:
                        risk_factors.append(risk)
        
        # Show progress summary
        console.print("\n[bold cyan]Project Progress Summary[/bold cyan]")
        progress_percentage = (completed_goals / total_goals) * 100 if total_goals > 0 else 0
        console.print(f"Goals Completed: {completed_goals}/{total_goals} ({progress_percentage:.1f}%)")
        
        # Average complexity
        avg_complexity = total_complexity / total_goals if total_goals > 0 else 0
        complexity_level = "Low" if avg_complexity < 4 else "Medium" if avg_complexity < 7 else "High"
        console.print(f"Average Complexity: {avg_complexity:.1f}/10 ({complexity_level})")
        
        # Risk factors
        if risk_factors:
            console.print(f"Identified Risk Factors: {', '.join(risk_factors)}")
        else:
            console.print("No significant risk factors identified")
        
        # Show detailed tracker view
        console.print("\n[bold cyan]Detailed Goal Status[/bold cyan]")
        console.print(tracker.render())
        
    except ValueError as e:
        console.print(f"[red]Validation error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def governance(
    action: str = typer.Argument(..., help="Action to perform: init, report, validate, compliance, security, quality, performance, reviews, version"),
    artifact_type: str = typer.Option(None, "--type", "-t", help="Type of artifact for validation"),
    artifact_id: str = typer.Option(None, "--id", "-i", help="ID of artifact for validation")
):
    """
    Manage project governance, compliance, and quality assurance.
    
    This command provides various governance functions:
    - init: Initialize project constitution
    - report: Generate comprehensive governance report
    - validate: Validate artifacts against governance rules
    - compliance: Check compliance with standards and regulations
    - security: Scan for security vulnerabilities and policy compliance
    - quality: Validate quality gates
    - performance: Monitor performance metrics
    - reviews: Manage review processes
    - version: Manage versioning and breaking changes
    
    Examples:
        goal governance init
        goal governance report
        goal governance validate --type goal --id abc123
        goal governance compliance
        goal governance security
        goal governance quality
        goal governance performance
        goal governance reviews
        goal governance version
    """
    try:
        project_path = get_project_path()
        governance_system = GovernanceSystem(project_path)
        
        if action == "init":
            # Initialize project constitution
            project_name = project_path.name
            constitution_path = governance_system.initialize_project_constitution(project_name)
            console.print(f"[green][+][/green] Project constitution created at: {constitution_path}")
            
        elif action == "report":
            # Generate comprehensive governance report
            console.print("[cyan]Generating governance report...[/cyan]")
            
            # Collect project data for analysis
            goal_manager = GoalManager(project_path)
            goals = goal_manager.list_goals()
            
            project_data = {
                "goals": goals,
                "specs": []  # In a full implementation, we would collect spec data too
            }
            
            report = governance_system.generate_governance_report(project_data)
            console.print("\n[bold cyan]Governance Report[/bold cyan]")
            console.print(report)
            
        elif action == "validate":
            # Validate an artifact
            if not artifact_type or not artifact_id:
                console.print("[red]Error:[/red] Both --type and --id are required for validation")
                raise typer.Exit(1)
            
            # Load the artifact
            if artifact_type == "goal":
                goal_manager = GoalManager(project_path)
                artifact_data = goal_manager.get_goal(artifact_id)
                if not artifact_data:
                    console.print(f"[red]Error:[/red] Goal with ID '{artifact_id}' not found")
                    raise typer.Exit(1)
            else:
                console.print(f"[red]Error:[/red] Validation for artifact type '{artifact_type}' not implemented")
                raise typer.Exit(1)
            
            # Validate the artifact
            console.print(f"[cyan]Validating {artifact_type} {artifact_id}...[/cyan]")
            validation_result = governance_system.validate_artifact(artifact_type, artifact_data)
            
            if validation_result["passed"]:
                console.print("[green][✓][/green] Artifact validation passed")
            else:
                console.print("[red][✗][/red] Artifact validation failed")
                if validation_result["violations"]:
                    console.print("\n[bold red]Violations:[/bold red]")
                    for violation in validation_result["violations"]:
                        console.print(f"  - {violation}")
                if validation_result["warnings"]:
                    console.print("\n[bold yellow]Warnings:[/bold yellow]")
                    for warning in validation_result["warnings"]:
                        console.print(f"  - {warning}")
            
        elif action == "compliance":
            # Check compliance
            console.print("[cyan]Checking compliance...[/cyan]")
            
            # Collect project data
            goal_manager = GoalManager(project_path)
            goals = goal_manager.list_goals()
            
            project_data = {
                "goals": goals,
                "specs": []
            }
            
            compliance_results = governance_system.check_compliance(project_data)
            
            if compliance_results["overall_compliant"]:
                console.print("[green][✓][/green] All compliance standards met")
            else:
                console.print("[red][✗][/red] Compliance issues detected")
                for standard, result in compliance_results["standards"].items():
                    if not result["compliant"]:
                        console.print(f"\n[bold red]{result['name']} ({standard})[/bold red]")
                        # In a full implementation, we would show details
                        
        elif action == "security":
            # Check security
            console.print("[cyan]Checking security...[/cyan]")
            
            # Collect project data
            goal_manager = GoalManager(project_path)
            goals = goal_manager.list_goals()
            
            project_data = {
                "goals": goals,
                "specs": []
            }
            
            security_results = governance_system.check_security_policies(project_data)
            
            if security_results["overall_compliant"]:
                console.print("[green][✓][/green] All security policies compliant")
            else:
                console.print("[red][✗][/red] Security policy violations detected")
                for policy, result in security_results["policies"].items():
                    if not result["compliant"]:
                        console.print(f"\n[bold red]{result['name']}[/bold red]")
                        # In a full implementation, we would show details
                        
        elif action == "quality":
            # Validate quality gates
            console.print("[cyan]Validating quality gates...[/cyan]")
            # In a full implementation, we would validate specific gates
            
        elif action == "performance":
            # Monitor performance
            console.print("[cyan]Monitoring performance...[/cyan]")
            # In a full implementation, we would show performance metrics
            
        elif action == "reviews":
            # Manage reviews
            console.print("[cyan]Managing reviews...[/cyan]")
            # In a full implementation, we would show review status
            
        elif action == "version":
            # Manage versioning
            console.print("[cyan]Managing versioning...[/cyan]")
            # In a full implementation, we would show version information
            
        else:
            console.print(f"[red]Error:[/red] Unknown governance action '{action}'")
            console.print("Valid actions: init, report, validate, compliance, security, quality, performance, reviews, version")
            raise typer.Exit(1)
            
    except ValueError as e:
        console.print(f"[red]Validation error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)

@app.callback()
def callback(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="Show version and exit")
):
    """
    Goal-Dev-Spec - A goal-driven development specification system using YAML
    
    Enhanced Quality Assurance Features:
    - Advanced validation algorithms for goals, specs, plans, and tasks
    - Automated quality scoring systems with comprehensive metrics
    - Consistency checking across related artifacts
    - Predictive quality analytics with risk assessment
    - Real-time quality monitoring with threshold alerts
    - Automated testing framework integration
    - Code quality assessment tools
    - Security vulnerability scanning
    - Performance benchmarking
    - Compliance validation against industry standards
    
    Use 'goal quality', 'goal test', and 'goal monitor' commands for enhanced QA features.
    """
    if version:
        console.print("goal-dev-spec version 0.1.0")
        raise typer.Exit()
    
    # Show banner only when running without arguments
    # (help is handled by BannerGroup)
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center("[dim]Run 'goal --help' for usage information[/dim]"))
        console.print()

def main():
    # Integrate analytics commands
    global app
    app = integrate_analytics_with_main_cli(app)
    
    # Integrate quality assurance commands
    app = integrate_quality_assurance_with_main_cli(app)
    
    # Integrate testing commands
    app = integrate_testing_with_main_cli(app)
    
    # Integrate monitoring commands
    app = integrate_monitoring_with_main_cli(app)
    
    # Integrate automation commands
    app = integrate_automation_with_main_cli(app)
    
    # Integrate cross-platform scripting commands
    app = integrate_cross_platform_with_main_cli(app)
    
    # Integrate AI code generation commands
    app = integrate_ai_code_with_main_cli(app)
    
    # Integrate documentation generation commands
    app = integrate_docs_with_main_cli(app)
    
    # Integrate CI/CD pipeline commands
    app = integrate_cicd_with_main_cli(app)
    
    # Integrate dependency management commands
    app = integrate_deps_with_main_cli(app)
    
    # Integrate project scaffolding commands
    app = integrate_scaffold_with_main_cli(app)
    
    # Integrate testing and quality gates commands
    app = integrate_testing_quality_with_main_cli(app)
    
    # Integrate performance optimization commands
    app = integrate_performance_with_main_cli(app)
    
    # Integrate security scanning commands
    app = integrate_security_with_main_cli(app)
    
    app()

if __name__ == "__main__":
    main()