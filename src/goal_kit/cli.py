"""Goal Kit CLI - A goal-driven development framework."""
import click
import sys
from pathlib import Path


@click.group()
@click.version_option()
def main():
    """Goal-Driven Development Framework - Focus on outcomes rather than specifications."""
    pass


@main.command()
@click.argument('project_name', required=False)
@click.option('--dir', default='.', help='Directory to initialize the project in')
def init(project_name, dir):
    """Initialize a new goal-driven project."""
    target_dir = Path(dir)
    if project_name:
        target_dir = target_dir / project_name
    
    if target_dir.exists():
        if not click.confirm(f"Directory {target_dir} already exists. Initialize here?"):
            return
    
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Create basic goal-driven project structure
    (target_dir / '.goals').mkdir(exist_ok=True)
    (target_dir / '.strategies').mkdir(exist_ok=True)
    (target_dir / '.plans').mkdir(exist_ok=True)
    
    # Create initial goal file
    goal_file = target_dir / '.goals' / 'main.goal.md'
    goal_file.write_text("""# Main Goal

## Objective
Define your primary objective here.

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Constraints
- Technical constraints
- Time constraints
- Resource constraints
""", encoding='utf-8')
    
    # Create README
    readme_file = target_dir / 'README.md'
    readme_content = f"""# {project_name or 'New Goal-Driven Project'}

This project follows the **Goal-Driven Development** methodology.
"""
    readme_file.write_text(readme_content, encoding='utf-8')
    
    click.echo(f"Initialized goal-driven project in {target_dir}")
    click.echo("Project structure created:")
    click.echo("  .goals/          - Define your project goals")
    click.echo("  .strategies/     - Document implementation strategies") 
    click.echo("  .plans/          - Create technical implementation plans")
    click.echo("  README.md        - Project documentation")


@main.command()
def goals():
    """List and manage project goals."""
    goals_dir = Path('.') / '.goals'
    if not goals_dir.exists():
        click.echo("No .goals directory found. Run 'goal init' first.")
        return
    
    goal_files = list(goals_dir.glob('*.goal.md'))
    if not goal_files:
        click.echo("No goals defined yet. Create a .goal.md file in the .goals directory.")
        return
    
    click.echo("Project Goals:")
    for goal_file in goal_files:
        content = goal_file.read_text(encoding='utf-8')
        # Extract the first line as the goal title
        title = content.split('\n')[0].replace('# ', '').strip()
        click.echo(f"  - {title} ({goal_file.name})")


@main.command()
def clarify():
    """Clarify and validate project goals."""
    click.echo("Clarification process started...")
    click.echo("This command would help refine and validate your project goals.")
    

@main.command()
def strategize():
    """Develop implementation strategies."""
    click.echo("Strategy development started...")
    click.echo("This command would help develop multiple implementation strategies.")


@main.command()
def plan():
    """Create technical implementation plans."""
    click.echo("Planning started...")
    click.echo("This command would help create detailed technical plans.")


@main.command()
def tasks():
    """Generate actionable tasks from plans."""
    click.echo("Task generation started...")
    click.echo("This command would generate actionable tasks from your plans.")


@main.command()
def implement():
    """Execute the implementation."""
    click.echo("Implementation started...")
    click.echo("This command would help execute your implementation plan.")


@main.command()
def check():
    """Check for installed tools (git, AI agents, etc.) and system requirements."""
    import subprocess
    import platform
    
    print("[INFO] Checking system requirements and installed tools...")
    print()
    
    # Check Git
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"[OK] Git: {result.stdout.strip()}")
        else:
            print("[ERROR] Git: Not found")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("[ERROR] Git: Not found")
    
    # Check common AI agent tools
    ai_agents = [
        ('Claude Code', 'claude'),
        ('GitHub Copilot', 'gh'),
        ('Cursor', 'cursor'),
        ('Qwen Code', 'qwen'),
        ('Windsurf', 'windsurf'),
        ('DeepSeek', 'deepseek'),
        ('Tabnine', 'tabnine'),
        ('Grok', 'grok'),
        ('CodeWhisperer', 'codewhisperer')
    ]
    
    print("\n[INFO] Checking AI agent tools:")
    for name, cmd in ai_agents:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"[OK] {name}: {result.stdout.strip()}")
            else:
                # Some tools might use different version commands
                result = subprocess.run([cmd, '-V'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"[OK] {name}: {result.stdout.strip()}")
                else:
                    print(f"[ERROR] {name}: Not found")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"[ERROR] {name}: Not found")
    
    # Check Python version
    import sys
    print(f"\n[INFO] Python: {sys.version}")
    
    # Check OS information
    print(f"[INFO] OS: {platform.system()} {platform.release()}")
    
    # Check uv (since it's required for installation)
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"[OK] uv: {result.stdout.strip()}")
        else:
            print("[ERROR] uv: Not found (required for installation)")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("[ERROR] uv: Not found (required for installation)")
    
    print("\n[SUCCESS] System check completed!")


if __name__ == '__main__':
    main()