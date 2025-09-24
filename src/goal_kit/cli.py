"""Goal Kit CLI - A goal-driven development framework."""
import click
import sys
from pathlib import Path
import os


@click.group()
@click.version_option()
def main():
    """Goal-Driven Development Framework - Focus on outcomes rather than specifications."""
    pass


@main.command()
@click.argument('project_name', required=False)
@click.option('--dir', default='.', help='Directory to initialize the project in')
@click.option('--ai', type=click.Choice([
    'claude', 'gemini', 'copilot', 'cursor', 'qwen', 'opencode',
    'codex', 'windsurf', 'kilocode', 'auggie', 'roo', 'deepseek',
    'tabnine', 'grok', 'codewhisperer'
]), help='AI assistant to use for goal-driven development')
@click.option('--script', type=click.Choice(['sh', 'ps']), default='sh',
              help='Script variant to use: sh (bash/zsh) or ps (PowerShell)')
@click.option('--ignore-agent-tools', is_flag=True,
              help='Skip checks for AI agent tools')
@click.option('--no-git', is_flag=True,
              help='Skip git repository initialization')
@click.option('--here', is_flag=True,
              help='Initialize project in the current directory')
@click.option('--force', is_flag=True,
              help='Force overwrite when using --here in non-empty directory')
def init(project_name, dir, ai, script, ignore_agent_tools, no_git, here, force):
    """Initialize a new goal-driven project with AI agent support.

    --dir and --here cannot be used together.
    If --here is specified, the project will be initialized in the current directory.
    If --dir is specified, the project will be initialized in the given directory.
    """
    if here and dir != '.':
        click.echo("Error: --here and --dir cannot be used together. Please specify only one.", err=True)
        sys.exit(1)
    if here:
        dir = os.getcwd()
    
    # Determine target directory
    target_dir = Path(dir)
    if project_name:
        target_dir = target_dir / project_name
    else:
        if not here:
            click.echo("Error: Please provide a project name or use --here flag")
            return
    
    if not force and any(target_dir.iterdir()) and (not click.confirm(f"Directory {target_dir} is not empty. Initialize here anyway?")):
        return
    
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize git if not --no-git
    if not no_git:
        git_dir = target_dir / '.git'
        import subprocess
        import os

        def is_valid_git_repo(path):
            try:
                result = subprocess.run(
                    ['git', 'status'],
                    cwd=path,
                    check=True,
                    capture_output=True
                )
                return result.returncode == 0
            except subprocess.CalledProcessError:
                return False
            except FileNotFoundError:
                return False

        if not git_dir.exists():
            try:
                subprocess.run(['git', 'init'], cwd=target_dir, check=True, capture_output=True)
                subprocess.run(['git', 'checkout', '-b', 'main'], cwd=target_dir, check=True, capture_output=True)
                click.echo("  [SUCCESS] Git repository initialized")
            except (subprocess.CalledProcessError, FileNotFoundError):
                click.echo("  [WARNING] Git not available or failed to initialize")
        else:
            # .git exists, check if it's a valid repo
            if not is_valid_git_repo(target_dir):
                click.echo("  [WARNING] Existing .git directory is not a valid git repository. Re-initializing...")
                try:
                    # Remove the invalid .git directory
                    import shutil
                    shutil.rmtree(git_dir)
                    subprocess.run(['git', 'init'], cwd=target_dir, check=True, capture_output=True)
                    subprocess.run(['git', 'checkout', '-b', 'main'], cwd=target_dir, check=True, capture_output=True)
                    click.echo("  [SUCCESS] Git repository re-initialized")
                except Exception as e:
                    click.echo(f"  [ERROR] Failed to re-initialize git repository: {e}")
            else:
                click.echo("  [INFO] Valid git repository already exists")
    
    # Create comprehensive goal-driven project structure
    (target_dir / '.goals').mkdir(exist_ok=True)
    (target_dir / '.strategies').mkdir(exist_ok=True)
    (target_dir / '.plans').mkdir(exist_ok=True)
    (target_dir / '.tasks').mkdir(exist_ok=True)
    (target_dir / '.analysis').mkdir(exist_ok=True)
    (target_dir / 'memory').mkdir(exist_ok=True)
    (target_dir / 'docs').mkdir(exist_ok=True)
    
    # Create initial constitution document
    constitution_file = target_dir / 'memory' / 'constitution.md'
    constitution_file.write_text("""# Project Constitution

## Core Principles
- Focus on outcomes rather than specifications
- Ensure every technical decision supports meaningful results
- Maintain stakeholder alignment throughout development
- Embrace iterative validation and course correction

## Quality Standards
- Code quality and documentation excellence
- Comprehensive testing strategy
- Performance and security considerations
- Maintainability and scalability

## Decision-Making Framework
- Prioritize goal achievement over technical perfection
- Consider long-term maintainability
- Balance innovation with stability
- Align with stakeholder needs and expectations
""", encoding='utf-8')
    
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
    
    # Create initial strategy file
    strategy_file = target_dir / '.strategies' / 'main.strategy.md'
    strategy_file.write_text("""# Main Strategy

## Approach
Describe your primary implementation approach.

## Alternatives Considered
- Alternative 1
- Alternative 2
- Alternative 3

## Rationale
Explain why this approach was chosen.
""", encoding='utf-8')
    
    # Create initial plan file
    plan_file = target_dir / '.plans' / 'main.plan.md'
    plan_file.write_text("""# Main Plan

## Implementation Approach
Describe your technical implementation plan.

## Components
- Component 1
- Component 2
- Component 3

## Timeline
- Phase 1
- Phase 2
- Phase 3
""", encoding='utf-8')
    
    # Create README
    readme_file = target_dir / 'README.md'
    readme_content = f"""# {project_name or 'New Goal-Driven Project'}

This project follows the **Goal-Driven Development** methodology.

## Getting Started

1. Define your goals in the `.goals/` directory
2. Develop strategies in the `.strategies/` directory
3. Create implementation plans in the `.plans/` directory
4. Use the `goal` CLI commands to manage your project

## AI Assistant Integration

This project is configured for goal-driven development with AI assistance.
In your AI coding environment, you can use slash commands like:
- `/constitution` - Update project principles
- `/goals` - Define project outcomes
- `/clarify` - Refine requirements
- `/strategize` - Evaluate approaches
- `/plan` - Create technical plans
- `/tasks` - Generate work breakdown
- `/analyze` - Check consistency
- `/implement` - Execute implementation
"""
    readme_file.write_text(readme_content, encoding='utf-8')
    
    # Create AI agent configuration if specified
    if ai:
        try:
            create_agent_config(target_dir, ai, script)
        except Exception as e:
            click.echo(f"Error creating AI agent configuration: {e}", err=True)
    
    click.echo(f"Initialized goal-driven project in {target_dir}")
    click.echo("Project structure created:")
    click.echo("  .goals/          - Define your project goals")
    click.echo("  .strategies/     - Document implementation strategies") 
    click.echo("  .plans/          - Create technical implementation plans")
    click.echo("  .tasks/          - Track implementation tasks")
    click.echo("  .analysis/       - Store analysis reports")
    click.echo("  memory/          - Store project constitution and guidelines")
    click.echo("  README.md        - Project documentation")
    if ai:
        click.echo(f"  .{ai}/          - AI agent configuration for {ai}")


def create_agent_config(project_dir, ai_agent, script_type):
    """Create agent-specific configuration files for goal-driven development."""
    agent_dir = project_dir / f".{ai_agent}"
    if agent_dir.exists():
        if not agent_dir.is_dir():
            raise RuntimeError(f"Cannot create agent config directory: {agent_dir} exists and is not a directory.")
    else:
        agent_dir.mkdir(exist_ok=True)
    
    if ai_agent in ['claude', 'cursor', 'opencode', 'windsurf', 'kilocode', 'auggie', 'roo']:
        # Create markdown-based command files for these agents
        commands_dir = agent_dir / 'commands'
        commands_dir.mkdir(exist_ok=True)
        
        # Create constitution command
        constitution_cmd = commands_dir / 'constitution.md'
        constitution_cmd.write_text(f"""---
name: constitution
description: Create or update project constitution and foundational principles
---

# /constitution Command

Create project constitution document establishing principles, values, and guidelines.

## Overview
The `/constitution` command creates a foundational document that establishes the principles, values, and guidelines for your project. This serves as the "constitution" that guides all project decisions and practices.

## Usage
```
/constitution [PRINCIPLES]
```

## Execution Flow
```
1. Parse user input from command arguments
2. Generate constitution document with principles
3. Save to memory/constitution.md
4. Provide feedback and next steps
```

## Guidelines for AI Generation
- Focus on project principles and values
- Include quality standards and decision-making frameworks
- Consider stakeholder needs and expectations
- Think about long-term project sustainability

## Implementation
When user runs `/constitution $ARGUMENTS`, create or update the constitution document in the memory/ directory based on the goal-driven methodology.

# Constitution Structure
The generated constitution includes:
- Core principles and project values
- Quality standards for code and deliverables
- Collaboration guidelines for team interaction
- Innovation practices for continuous improvement
- Decision-making framework for technical choices
- Success metrics to measure project health
- Code of conduct for project participation

$ARGUMENTS
""", encoding='utf-8')
        
        # Create goals command
        goals_cmd = commands_dir / 'goals.md'
        goals_cmd.write_text(f"""---
name: goals
description: Define project goals and desired outcomes
---

# /goals Command

Define project goals focusing on outcomes and objectives.

## Overview
The `/goals` command helps establish what outcomes you want to achieve and why they matter. Focus on the "what" and "why", not the technical implementation.

## Usage
```
/goals [USER_GOALS]
```

## Execution Flow
```
1. Parse user goals from command arguments
2. Extract key objectives and outcomes
3. Generate structured goal document
4. Save to .goals/ directory
5. Provide feedback and next steps
```

## Guidelines for AI Generation
- Focus on WHAT outcomes we want to achieve and WHY
- Avoid HOW to implement (no tech stack, APIs, code structure)
- Written for stakeholders, not developers
- Define measurable success criteria
- Think like a product manager focused on value

## Implementation
When user runs `/goals $ARGUMENTS`, create a structured goal document in the .goals/ directory based on the goal-driven methodology.

## Goal Requirements
- Primary project objectives
- Key Performance Indicators (KPIs)
- Success criteria (measurable outcomes)
- Stakeholder analysis
- Impact assessment

$ARGUMENTS
""", encoding='utf-8')
        
        # Create clarify command
        clarify_cmd = commands_dir / 'clarify.md'
        clarify_cmd.write_text(f"""---
name: clarify
description: Clarify and validate project goals
---

# /clarify Command

Clarify and validate project goals by addressing ambiguities.

## Overview
The `/clarify` command addresses any ambiguities or underspecified areas in the goals before moving to strategy development. This reduces rework downstream.

## Usage
```
/clarify
```

## Execution Flow
```
1. Read existing goal document
2. Identify underspecified areas
3. Ask clarifying questions systematically
4. Document answers and decisions
5. Validate requirements against goals
```

## Guidelines for AI Generation
- Identify areas that need clarification
- Formulate specific questions to resolve ambiguities
- Document answers to maintain consistency
- Validate that clarifications align with original goals
- Mark all ambiguities with [NEEDS CLARIFICATION: specific question]

## Implementation
When user runs `/clarify`, review existing goals and ask targeted questions to resolve uncertainties.

$ARGUMENTS
""", encoding='utf-8')
        
        # Create strategize command
        strategize_cmd = commands_dir / 'strategize.md'
        strategize_cmd.write_text(f"""---
name: strategize
description: Develop implementation strategies for achieving goals
---

# /strategize Command

Evaluate different technical approaches for achieving defined goals.

## Overview
The `/strategize` command evaluates different implementation strategies before committing to a specific technical approach. Considers technical feasibility, resource requirements, and goal alignment.

## Usage
```
/strategize [STRATEGY_OPTIONS]
```

## Execution Flow
```
1. Parse strategy options from command arguments
2. Generate multiple implementation strategies
3. Evaluate strategies against selection criteria
4. Compare approaches objectively
5. Document evaluation results
6. Select optimal strategy with justification
```

## Guidelines for AI Generation
- Generate multiple implementation strategies
- Evaluate against: goal alignment, technical feasibility, resource requirements, risk factors, scalability
- Compare approaches objectively
- Document selection rationale clearly
- Consider long-term maintainability

## Implementation
When user runs `/strategize $ARGUMENTS`, create strategy evaluation documents in the .strategies/ directory.

$ARGUMENTS
""", encoding='utf-8')
        
        # Create plan command
        plan_cmd = commands_dir / 'plan.md'
        plan_cmd.write_text(f"""---
name: plan
description: Create technical implementation plans based on chosen strategy
---

# /plan Command

Create detailed technical implementation plans based on chosen strategy.

## Overview
The `/plan` command creates detailed technical implementation plans based on the selected strategy. Translates strategic decisions into specific technical specifications.

## Usage
```
/plan [TECHNICAL_APPROACH]
```

## Execution Flow
```
1. Parse technical approach from command arguments
2. Create detailed technical specifications
3. Design system architecture
4. Define implementation phases
5. Plan testing and validation approaches
6. Document technical decisions and rationale
```

## Guidelines for AI Generation
- Align with selected strategy
- Include system architecture design
- Define implementation phases
- Plan testing strategy
- Document technical decisions
- Consider non-functional requirements

## Implementation
When user runs `/plan $ARGUMENTS`, create technical plan document in the .plans/ directory.

$ARGUMENTS
""", encoding='utf-8')
        
        # Create tasks command
        tasks_cmd = commands_dir / 'tasks.md'
        tasks_cmd.write_text(f"""---
name: tasks
description: Generate actionable tasks from implementation plans
---

# /tasks Command

Generate actionable task list from implementation plans.

## Overview
The `/tasks` command breaks down the implementation plan into actionable work items that can be executed systematically.

## Usage
```
/tasks
```

## Execution Flow
```
1. Read selected strategy and implementation plan
2. Break implementation plan into discrete tasks
3. Define task dependencies and priorities
4. Estimate effort and resources needed
5. Create task execution schedule
6. Plan for parallel execution where appropriate
```

## Guidelines for AI Generation
- Break into specific, actionable tasks
- Define dependencies clearly
- Consider execution order
- Estimate effort for each task
- Identify parallelizable work
- Create executable task list

## Implementation
When user runs `/tasks`, create task breakdown based on plans in .plans/ directory.

$ARGUMENTS
""", encoding='utf-8')
        
        # Create analyze command
        analyze_cmd = commands_dir / 'analyze.md'
        analyze_cmd.write_text(f"""---
name: analyze
description: Cross-artifact consistency & coverage analysis
---

# /analyze Command

Validate project alignment and surface inconsistencies across artifacts.

## Overview
The `/analyze` command examines project structure to validate that all components align with goals, strategies, and plans. Identifies inconsistencies, gaps, and areas for improvement.

## Usage
```
/analyze
```

## Execution Flow
```
1. Scan project structure and files
2. Review goals, strategies, plans, and tasks
3. Check alignment between components
4. Identify gaps and inconsistencies
5. Assess project health and risks
6. Generate analysis report
```

## Analysis Scope
- Goal alignment across all components
- Technical consistency in architecture
- Project structure completeness
- Documentation coverage
- Testing strategy adequacy

## Guidelines for AI Generation
- Check consistency between artifacts
- Verify complete coverage of goals
- Identify potential gaps or conflicts
- Validate artifact alignment
- Assess project health metrics

## Implementation
When user runs `/analyze`, create analysis report in .analysis/ directory.

$ARGUMENTS
""", encoding='utf-8')
        
        # Create implement command
        implement_cmd = commands_dir / 'implement.md'
        implement_cmd.write_text(f"""---
name: implement
description: Execute implementation plan according to defined tasks
---

# /implement Command

Execute the implementation plan according to defined tasks.

## Overview
The `/implement` command executes planned tasks to build the solution according to defined strategy and plan while maintaining focus on goal achievement.

## Usage
```
/implement
```

## Execution Flow
```
1. Validate prerequisites (constitution, goals, strategy, plan, tasks)
2. Parse task breakdown from tasks document
3. Execute tasks in planned order respecting dependencies
4. Validate implementation against goals continuously
5. Adapt approach as needed while maintaining goal alignment
6. Document implementation decisions and changes
7. Conduct ongoing validation and testing
```

## Guidelines for AI Generation
- Execute tasks systematically
- Validate continuously against goals
- Adapt approach when needed
- Document changes and decisions
- Conduct thorough testing
- Maintain goal alignment

## Implementation
When user runs `/implement`, execute the implementation plan following TDD approach defined in tasks.

$ARGUMENTS
""", encoding='utf-8')
        
    elif ai_agent in ['gemini', 'qwen']:
        # Create TOML-based command files for these agents
        commands_dir = agent_dir / 'commands'
        commands_dir.mkdir(exist_ok=True)
        
        # Create constitution command (TOML format)
        constitution_cmd = commands_dir / 'constitution.toml'
        constitution_cmd.write_text(f"""name = "constitution"
description = "Create or update project constitution and foundational principles"

[prompt]
text = '''
# /constitution Command

Create project constitution document establishing principles, values, and guidelines.

## Overview
The `/constitution` command creates a foundational document that establishes the principles, values, and guidelines for your project. This serves as the "constitution" that guides all project decisions and practices.

## Usage
```
/constitution [PRINCIPLES]
```

## Execution Flow
```
1. Parse user input from command arguments
2. Generate constitution document with principles
3. Save to memory/constitution.md
4. Provide feedback and next steps
```

## Guidelines for AI Generation
- Focus on project principles and values
- Include quality standards and decision-making frameworks
- Consider stakeholder needs and expectations
- Think about long-term project sustainability

## Implementation
When user runs `/constitution {{args}}`, create or update the constitution document in the memory/ directory based on the goal-driven methodology.

# Constitution Structure
The generated constitution includes:
- Core principles and project values
- Quality standards for code and deliverables
- Collaboration guidelines for team interaction
- Innovation practices for continuous improvement
- Decision-making framework for technical choices
- Success metrics to measure project health
- Code of conduct for project participation

{{args}}
'''
""")
        
        # Create goals command (TOML format)
        goals_cmd = commands_dir / 'goals.toml'
        goals_cmd.write_text(f"""name = "goals"
description = "Define project goals and desired outcomes"

[prompt]
text = '''
# /goals Command

Define project goals focusing on outcomes and objectives.

## Overview
The `/goals` command helps establish what outcomes you want to achieve and why they matter. Focus on the "what" and "why", not the technical implementation.

## Usage
```
/goals [USER_GOALS]
```

## Execution Flow
```
1. Parse user goals from command arguments
2. Extract key objectives and outcomes
3. Generate structured goal document
4. Save to .goals/ directory
5. Provide feedback and next steps
```

## Guidelines for AI Generation
- Focus on WHAT outcomes we want to achieve and WHY
- Avoid HOW to implement (no tech stack, APIs, code structure)
- Written for stakeholders, not developers
- Define measurable success criteria
- Think like a product manager focused on value

## Implementation
When user runs `/goals {{args}}`, create a structured goal document in the .goals/ directory based on the goal-driven methodology.

## Goal Requirements
- Primary project objectives
- Key Performance Indicators (KPIs)
- Success criteria (measurable outcomes)
- Stakeholder analysis
- Impact assessment

{{args}}
'''
""")
        
        # Create other commands in TOML format as well...
        clarify_content = f"""# /clarify Command

Clarify and validate project goals by addressing ambiguities.

## Overview
The `/clarify` command addresses any ambiguities or underspecified areas in the goals before moving to strategy development. This reduces rework downstream.

## Usage
```
/clarify
```

## Execution Flow
```
1. Read existing goal document
2. Identify underspecified areas
3. Ask clarifying questions systematically
4. Document answers and decisions
5. Validate requirements against goals
```

## Guidelines for AI Generation
- Identify areas that need clarification
- Formulate specific questions to resolve ambiguities
- Document answers to maintain consistency
- Validate that clarifications align with original goals
- Mark all ambiguities with [NEEDS CLARIFICATION: specific question]

## Implementation
When user runs `/clarify`, review existing goals and ask targeted questions to resolve uncertainties.

{{args}}
"""
        create_toml_command(commands_dir, 'clarify', 'Clarify and validate project goals', clarify_content)
        
        strategize_content = f"""# /strategize Command

Evaluate different technical approaches for achieving defined goals.

## Overview
The `/strategize` command evaluates different implementation strategies before committing to a specific technical approach. Considers technical feasibility, resource requirements, and goal alignment.

## Usage
```
/strategize [STRATEGY_OPTIONS]
```

## Execution Flow
```
1. Parse strategy options from command arguments
2. Generate multiple implementation strategies
3. Evaluate strategies against selection criteria
4. Compare approaches objectively
5. Document evaluation results
6. Select optimal strategy with justification
```

## Guidelines for AI Generation
- Generate multiple implementation strategies
- Evaluate against: goal alignment, technical feasibility, resource requirements, risk factors, scalability
- Compare approaches objectively
- Document selection rationale clearly
- Consider long-term maintainability

## Implementation
When user runs `/strategize {{args}}`, create strategy evaluation documents in the .strategies/ directory.

{{args}}
"""
        create_toml_command(commands_dir, 'strategize', 'Develop implementation strategies for achieving goals', strategize_content)
        
        plan_content = f"""# /plan Command

Create detailed technical implementation plans based on chosen strategy.

## Overview
The `/plan` command creates detailed technical implementation plans based on the selected strategy. Translates strategic decisions into specific technical specifications.

## Usage
```
/plan [TECHNICAL_APPROACH]
```

## Execution Flow
```
1. Parse technical approach from command arguments
2. Create detailed technical specifications
3. Design system architecture
4. Define implementation phases
5. Plan testing and validation approaches
6. Document technical decisions and rationale
```

## Guidelines for AI Generation
- Align with selected strategy
- Include system architecture design
- Define implementation phases
- Plan testing strategy
- Document technical decisions
- Consider non-functional requirements

## Implementation
When user runs `/plan {{args}}`, create technical plan document in the .plans/ directory.

{{args}}
"""
        create_toml_command(commands_dir, 'plan', 'Create technical implementation plans based on chosen strategy', plan_content)
        
        tasks_content = f"""# /tasks Command

Generate actionable task list from implementation plans.

## Overview
The `/tasks` command breaks down the implementation plan into actionable work items that can be executed systematically.

## Usage
```
/tasks
```

## Execution Flow
```
1. Read selected strategy and implementation plan
2. Break implementation plan into discrete tasks
3. Define task dependencies and priorities
4. Estimate effort and resources needed
5. Create task execution schedule
6. Plan for parallel execution where appropriate
```

## Guidelines for AI Generation
- Break into specific, actionable tasks
- Define dependencies clearly
- Consider execution order
- Estimate effort for each task
- Identify parallelizable work
- Create executable task list

## Implementation
When user runs `/tasks`, create task breakdown based on plans in .plans/ directory.

{{args}}
"""
        create_toml_command(commands_dir, 'tasks', 'Generate actionable tasks from implementation plans', tasks_content)
        
        analyze_content = f"""# /analyze Command

Validate project alignment and surface inconsistencies across artifacts.

## Overview
The `/analyze` command examines project structure to validate that all components align with goals, strategies, and plans. Identifies inconsistencies, gaps, and areas for improvement.

## Usage
```
/analyze
```

## Execution Flow
```
1. Scan project structure and files
2. Review goals, strategies, plans, and tasks
3. Check alignment between components
4. Identify gaps and inconsistencies
5. Assess project health and risks
6. Generate analysis report
```

## Analysis Scope
- Goal alignment across all components
- Technical consistency in architecture
- Project structure completeness
- Documentation coverage
- Testing strategy adequacy

## Guidelines for AI Generation
- Check consistency between artifacts
- Verify complete coverage of goals
- Identify potential gaps or conflicts
- Validate artifact alignment
- Assess project health metrics

## Implementation
When user runs `/analyze`, create analysis report in .analysis/ directory.

{{args}}
"""
        create_toml_command(commands_dir, 'analyze', 'Cross-artifact consistency & coverage analysis', analyze_content)
        
        implement_content = f"""# /implement Command

Execute the implementation plan according to defined tasks.

## Overview
The `/implement` command executes planned tasks to build the solution according to defined strategy and plan while maintaining focus on goal achievement.

## Usage
```
/implement
```

## Execution Flow
```
1. Validate prerequisites (constitution, goals, strategy, plan, tasks)
2. Parse task breakdown from tasks document
3. Execute tasks in planned order respecting dependencies
4. Validate implementation against goals continuously
5. Adapt approach as needed while maintaining goal alignment
6. Document implementation decisions and changes
7. Conduct ongoing validation and testing
```

## Guidelines for AI Generation
- Execute tasks systematically
- Validate continuously against goals
- Adapt approach when needed
- Document changes and decisions
- Conduct thorough testing
- Maintain goal alignment

## Implementation
When user runs `/implement`, execute the implementation plan following TDD approach defined in tasks.

{{args}}
"""
        create_toml_command(commands_dir, 'implement', 'Execute implementation plan according to defined tasks', implement_content)


def create_toml_command(commands_dir, name, description, content):
    """Helper function to create a TOML command file."""
    cmd_file = commands_dir / f'{name}.toml'
    toml_content = f"""name = "{name}"
description = "{description}"

[prompt]
text = {repr(content)}
"""
    with open(cmd_file, 'w', encoding='utf-8') as f:
        f.write(toml_content)


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
    goals_dir = Path('.') / '.goals'
    if not goals_dir.exists():
        click.echo("No .goals directory found. Run 'goal init' first.")
        return
    
    goal_files = list(goals_dir.glob('*.goal.md'))
    if not goal_files:
        click.echo("No goals defined yet. Use 'goal goals' to define goals first.")
        return
    
    click.echo("Clarification process started...")
    click.echo("Reviewing existing goals for clarity and completeness:")
    for goal_file in goal_files:
        content = goal_file.read_text(encoding='utf-8')
        click.echo(f"\nAnalyzing: {goal_file.name}")
        click.echo(content)


@main.command()
def strategize():
    """Develop implementation strategies."""
    strategies_dir = Path('.') / '.strategies'
    if not strategies_dir.exists():
        click.echo("No .strategies directory found. Run 'goal init' first.")
        return
    
    strategy_files = list(strategies_dir.glob('*.strategy.md'))
    click.echo("Strategy development started...")
    click.echo("Current strategies:")
    for strategy_file in strategy_files:
        content = strategy_file.read_text(encoding='utf-8')
        title = content.split('\n')[0].replace('# ', '').strip()
        click.echo(f"  - {title} ({strategy_file.name})")
    
    if not strategy_files:
        click.echo("No strategies defined yet. Create a .strategy.md file in the .strategies directory.")


@main.command()
def plan():
    """Create technical implementation plans."""
    plans_dir = Path('.') / '.plans'
    if not plans_dir.exists():
        click.echo("No .plans directory found. Run 'goal init' first.")
        return
    
    plan_files = list(plans_dir.glob('*.plan.md'))
    click.echo("Planning started...")
    click.echo("Current plans:")
    for plan_file in plan_files:
        content = plan_file.read_text(encoding='utf-8')
        title = content.split('\n')[0].replace('# ', '').strip()
        click.echo(f"  - {title} ({plan_file.name})")
    
    if not plan_files:
        click.echo("No plans defined yet. Create a .plan.md file in the .plans directory.")


@main.command()
def tasks():
    """Generate actionable tasks from plans."""
    tasks_dir = Path('.') / '.tasks'
    if not tasks_dir.exists():
        click.echo("No .tasks directory found. Run 'goal init' first.")
        return
    
    task_files = list(tasks_dir.glob('*.task.md'))
    click.echo("Task generation started...")
    click.echo("Current tasks:")
    for task_file in task_files:
        content = task_file.read_text(encoding='utf-8')
        title = content.split('\n')[0].replace('# ', '').strip()
        click.echo(f"  - {title} ({task_file.name})")
    
    if not task_files:
        click.echo("No tasks defined yet. Create a .task.md file in the .tasks directory.")


@main.command()
def analyze():
    """Analyze project alignment and consistency."""
    analysis_dir = Path('.') / '.analysis'
    if not analysis_dir.exists():
        click.echo("No .analysis directory found. Run 'goal init' first.")
        return
    
    # Check for existing analysis files
    analysis_files = list(analysis_dir.glob('*.md'))
    
    click.echo("Project analysis started...")
    click.echo("Analyzing project structure and alignment:")
    
    # Check goals
    goals_dir = Path('.') / '.goals'
    if goals_dir.exists():
        goal_files = list(goals_dir.glob('*.goal.md'))
        click.echo(f"  - Goals: {len(goal_files)} files")
    
    # Check strategies
    strategies_dir = Path('.') / '.strategies'
    if strategies_dir.exists():
        strategy_files = list(strategies_dir.glob('*.strategy.md'))
        click.echo(f"  - Strategies: {len(strategy_files)} files")
    
    # Check plans
    plans_dir = Path('.') / '.plans'
    if plans_dir.exists():
        plan_files = list(plans_dir.glob('*.plan.md'))
        click.echo(f"  - Plans: {len(plan_files)} files")
    
    # Check tasks
    tasks_dir = Path('.') / '.tasks'
    if tasks_dir.exists():
        task_files = list(tasks_dir.glob('*.task.md'))
        click.echo(f"  - Tasks: {len(task_files)} files")
    
    # Generate analysis report
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    analysis_file = analysis_dir / f'analysis_report_{timestamp}.md'
    
    analysis_content = f"""# Analysis Report
Generated: {datetime.datetime.now()}

## Summary
- Goals: {len(list(goals_dir.glob('*.goal.md'))) if goals_dir.exists() else 0}
- Strategies: {len(list(strategies_dir.glob('*.strategy.md'))) if strategies_dir.exists() else 0}
- Plans: {len(list(plans_dir.glob('*.plan.md'))) if plans_dir.exists() else 0}
- Tasks: {len(list(tasks_dir.glob('*.task.md'))) if tasks_dir.exists() else 0}

## Alignment Check
This report analyzes the alignment between goals, strategies, plans, and tasks.
"""
    
    analysis_file.write_text(analysis_content, encoding='utf-8')
    click.echo(f"Analysis report saved to: {analysis_file}")
    click.echo("Analysis completed.")


@main.command()
def implement():
    """Execute the implementation."""
    click.echo("Implementation started...")
    click.echo("This command would help execute your implementation plan.")

    # Check project structure
    goals_dir = Path('.') / '.goals'
    plans_dir = Path('.') / '.plans'
    tasks_dir = Path('.') / '.tasks'

    if not all(d.exists() for d in [goals_dir, plans_dir, tasks_dir]):
        click.echo("Project not fully set up. Ensure you have goals, plans, and tasks defined.")
        return

    # List what needs to be implemented
    goal_files = list(goals_dir.glob('*.goal.md')) if goals_dir.exists() else []
    plan_files = list(plans_dir.glob('*.plan.md')) if plans_dir.exists() else []
    task_files = list(tasks_dir.glob('*.task.md')) if tasks_dir.exists() else []

    click.echo("Ready to implement:")
    click.echo(f"  - {len(goal_files)} goal(s)")
    click.echo(f"  - {len(plan_files)} plan(s)")
    click.echo(f"  - {len(task_files)} task(s)")


@main.command()
def check():
    """Check development environment and installed tools."""
    click.echo("Checking development environment...")
    
    # Check for git
    import subprocess
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            click.echo(f"✓ Git: {result.stdout.strip()}")
        else:
            click.echo("✗ Git: Not found")
    except FileNotFoundError:
        click.echo("✗ Git: Not found")
    
    # Check for python
    import sys
    click.echo(f"✓ Python: {sys.version}")
    
    # Check for uv (if installed)
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            click.echo(f"✓ uv: {result.stdout.strip()}")
        else:
            click.echo("⚠ uv: Not found (recommended for package management)")
    except FileNotFoundError:
        click.echo("⚠ uv: Not found (recommended for package management)")
    
    # Check project structure
    required_dirs = ['.goals', '.strategies', '.plans', 'memory']
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            click.echo(f"✓ {dir_name}/ directory: Found")
        else:
            click.echo(f"⚠ {dir_name}/ directory: Missing (run 'goal init' to create)")
    
    # Check for various AI agent tools if in a project directory\n    ai_agents = ['claude', 'gemini', 'cursor', 'qwen', 'copilot', 'windsurf', 'opencode', 'codex', 'grok', 'codewhisperer']\n    for agent in ai_agents:\n        agent_dir = Path(f'.{agent}')\n        if agent_dir.exists():\n            click.echo(f\"[SUCCESS] {agent_dir}/ directory: Found\")\n    \n    click.echo(\"\\nEnvironment check completed.\")\n


@main.command()
def constitution():
    """Create or update project constitution and principles."""
    memory_dir = Path('.') / 'memory'
    if not memory_dir.exists():
        click.echo("Memory directory not found. Run 'goal init' first.")
        return
    
    constitution_file = memory_dir / 'constitution.md'
    if constitution_file.exists():
        click.echo("Project constitution found:")
        click.echo(constitution_file.read_text(encoding='utf-8'))
    else:
        # Create a new constitution file
        constitution_file.write_text("""# Project Constitution

## Core Principles
- Focus on outcomes rather than specifications
- Ensure every technical decision supports meaningful results
- Maintain stakeholder alignment throughout development
- Embrace iterative validation and course correction

## Quality Standards
- Code quality and documentation excellence
- Comprehensive testing strategy
- Performance and security considerations
- Maintainability and scalability

## Decision-Making Framework
- Prioritize goal achievement over technical perfection
- Consider long-term maintainability
- Balance innovation with stability
- Align with stakeholder needs and expectations
""", encoding='utf-8')
        click.echo(f"Created new constitution file at {constitution_file}")


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
    goals_dir = Path('.') / '.goals'
    if not goals_dir.exists():
        click.echo("No .goals directory found. Run 'goal init' first.")
        return
    
    goal_files = list(goals_dir.glob('*.goal.md'))
    if not goal_files:
        click.echo("No goals defined yet. Use 'goal goals' to define goals first.")
        return
    
    click.echo("Clarification process started...")
    click.echo("Reviewing existing goals for clarity and completeness:")
    for goal_file in goal_files:
        content = goal_file.read_text(encoding='utf-8')
        click.echo(f"\nAnalyzing: {goal_file.name}")
        click.echo(content)


@main.command()
def strategize():
    """Develop implementation strategies."""
    strategies_dir = Path('.') / '.strategies'
    if not strategies_dir.exists():
        click.echo("No .strategies directory found. Run 'goal init' first.")
        return
    
    strategy_files = list(strategies_dir.glob('*.strategy.md'))
    click.echo("Strategy development started...")
    click.echo("Current strategies:")
    for strategy_file in strategy_files:
        content = strategy_file.read_text(encoding='utf-8')
        title = content.split('\n')[0].replace('# ', '').strip()
        click.echo(f"  - {title} ({strategy_file.name})")
    
    if not strategy_files:
        click.echo("No strategies defined yet. Create a .strategy.md file in the .strategies directory.")


@main.command()
def plan():
    """Create technical implementation plans."""
    plans_dir = Path('.') / '.plans'
    if not plans_dir.exists():
        click.echo("No .plans directory found. Run 'goal init' first.")
        return
    
    plan_files = list(plans_dir.glob('*.plan.md'))
    click.echo("Planning started...")
    click.echo("Current plans:")
    for plan_file in plan_files:
        content = plan_file.read_text(encoding='utf-8')
        title = content.split('\n')[0].replace('# ', '').strip()
        click.echo(f"  - {title} ({plan_file.name})")
    
    if not plan_files:
        click.echo("No plans defined yet. Create a .plan.md file in the .plans directory.")


@main.command()
def tasks():
    """Generate actionable tasks from plans."""
    tasks_dir = Path('.') / '.tasks'
    if not tasks_dir.exists():
        click.echo("No .tasks directory found. Run 'goal init' first.")
        return
    
    task_files = list(tasks_dir.glob('*.task.md'))
    click.echo("Task generation started...")
    click.echo("Current tasks:")
    for task_file in task_files:
        content = task_file.read_text(encoding='utf-8')
        title = content.split('\n')[0].replace('# ', '').strip()
        click.echo(f"  - {title} ({task_file.name})")
    
    if not task_files:
        click.echo("No tasks defined yet. Create a .task.md file in the .tasks directory.")


@main.command()
def analyze():
    """Analyze project alignment and consistency."""
    analysis_dir = Path('.') / '.analysis'
    if not analysis_dir.exists():
        click.echo("No .analysis directory found. Run 'goal init' first.")
        return
    
    # Check for existing analysis files
    analysis_files = list(analysis_dir.glob('*.md'))
    
    click.echo("Project analysis started...")
    click.echo("Analyzing project structure and alignment:")
    
    # Check goals
    goals_dir = Path('.') / '.goals'
    if goals_dir.exists():
        goal_files = list(goals_dir.glob('*.goal.md'))
        click.echo(f"  - Goals: {len(goal_files)} files")
    
    # Check strategies
    strategies_dir = Path('.') / '.strategies'
    if strategies_dir.exists():
        strategy_files = list(strategies_dir.glob('*.strategy.md'))
        click.echo(f"  - Strategies: {len(strategy_files)} files")
    
    # Check plans
    plans_dir = Path('.') / '.plans'
    if plans_dir.exists():
        plan_files = list(plans_dir.glob('*.plan.md'))
        click.echo(f"  - Plans: {len(plan_files)} files")
    
    # Check tasks
    tasks_dir = Path('.') / '.tasks'
    if tasks_dir.exists():
        task_files = list(tasks_dir.glob('*.task.md'))
        click.echo(f"  - Tasks: {len(task_files)} files")
    
    # Generate analysis report
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    analysis_file = analysis_dir / f'analysis_report_{timestamp}.md'
    
    analysis_content = f"""# Analysis Report
Generated: {datetime.datetime.now()}

## Summary
- Goals: {len(list(goals_dir.glob('*.goal.md'))) if goals_dir.exists() else 0}
- Strategies: {len(list(strategies_dir.glob('*.strategy.md'))) if strategies_dir.exists() else 0}
- Plans: {len(list(plans_dir.glob('*.plan.md'))) if plans_dir.exists() else 0}
- Tasks: {len(list(tasks_dir.glob('*.task.md'))) if tasks_dir.exists() else 0}

## Alignment Check
This report analyzes the alignment between goals, strategies, plans, and tasks.
"""
    
    analysis_file.write_text(analysis_content, encoding='utf-8')
    click.echo(f"Analysis report saved to: {analysis_file}")
    click.echo("Analysis completed.")


@main.command()
def implement():
    """Execute the implementation."""
    click.echo("Implementation started...")
    click.echo("This command would help execute your implementation plan.")
    
    # Check project structure
    goals_dir = Path('.') / '.goals'
    plans_dir = Path('.') / '.plans'
    tasks_dir = Path('.') / '.tasks'
    
    if not all(d.exists() for d in [goals_dir, plans_dir, tasks_dir]):
        click.echo("Project not fully set up. Ensure you have goals, plans, and tasks defined.")
        return
    
    # List what needs to be implemented
    goal_files = list(goals_dir.glob('*.goal.md')) if goals_dir.exists() else []
    plan_files = list(plans_dir.glob('*.plan.md')) if plans_dir.exists() else []
    task_files = list(tasks_dir.glob('*.task.md')) if tasks_dir.exists() else []
    
    click.echo(f"Ready to implement:")
    click.echo(f"  - {len(goal_files)} goal(s)")
    click.echo(f"  - {len(plan_files)} plan(s)")
    click.echo(f"  - {len(task_files)} task(s)")


@main.command()
def check():
    """Check development environment and installed tools."""
    click.echo("Checking development environment...")
    
    # Check for git
    import subprocess
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            click.echo(f"✓ Git: {result.stdout.strip()}")
        else:
            click.echo("✗ Git: Not found")
    except FileNotFoundError:
        click.echo("✗ Git: Not found")
    
    # Check for python
    import sys
    click.echo(f"✓ Python: {sys.version}")
    
    # Check for uv (if installed)
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            click.echo(f"✓ uv: {result.stdout.strip()}")
        else:
            click.echo("⚠ uv: Not found (recommended for package management)")
    except FileNotFoundError:
        click.echo("⚠ uv: Not found (recommended for package management)")
    
    # Check project structure
    required_dirs = ['.goals', '.strategies', '.plans', 'memory']
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            click.echo(f"✓ {dir_name}/ directory: Found")
        else:
            click.echo(f"⚠ {dir_name}/ directory: Missing (run 'goal init' to create)")
    
    click.echo("\nEnvironment check completed.")


if __name__ == '__main__':
    main()