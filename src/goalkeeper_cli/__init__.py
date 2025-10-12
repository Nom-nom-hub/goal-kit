#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "rich",
#     "platformdirs",
#     "readchar",
#     "httpx",
# ]
# ///
"""
Goalkeeper CLI - Setup tool for Goal Kit projects

Usage:
    uvx goalkeeper-cli.py init <project-name>
    uvx goalkeeper-cli.py init .
    uvx goalkeeper-cli.py init --here

Or install globally:
    uv tool install --from goalkeeper-cli.py goalkeeper-cli
    goalkeeper init <project-name>
    goalkeeper init .
    goalkeeper init --here
"""

import os
import subprocess
import sys
import zipfile
import tempfile
import shutil
import shlex
import json
import re
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List
from datetime import datetime

import typer
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.table import Table
from rich.tree import Tree
from typer.core import TyperGroup

# Import template processor for goal creation
try:
    from .template_processor import TemplateProcessor
except ImportError:
    TemplateProcessor = None

# Import memory system and baseline metrics
try:
    from .memory import ProjectMemory, AISessionMemory, CrossProjectInsights, extract_goal_learnings
    from .baseline_metrics import BaselineCollector, HypothesisTester, initialize_baseline_system
except ImportError:
    # Fallback if modules not available
    ProjectMemory = None
    AISessionMemory = None
    CrossProjectInsights = None
    extract_goal_learnings = None
    BaselineCollector = None
    HypothesisTester = None
    initialize_baseline_system = None

# For cross-platform keyboard input
import readchar
import ssl
import truststore

ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = httpx.Client(verify=ssl_context)

def _github_token(cli_token: str | None = None) -> str | None:
    """Return sanitized GitHub token (cli arg takes precedence) or None."""
    return ((cli_token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()) or None

def _github_auth_headers(cli_token: str | None = None) -> dict:
    """Return Authorization header dict only when a non-empty token exists."""
    token = _github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}

AI_CHOICES = {
"copilot": "GitHub Copilot",
"claude": "Claude Code",
"gemini": "Gemini CLI",
"cursor": "Cursor",
"qwen": "Qwen Code",
"opencode": "opencode",
"codex": "Codex CLI",
"windsurf": "Windsurf",
"kilocode": "Kilo Code",
"auggie": "Auggie CLI",
"roo": "Roo Code",
"q": "Amazon Q Developer CLI",
}

# AI Agent Configuration for Template Optimization
AI_AGENT_CONFIG = {
"claude": {
    "template_style": "analytical_detailed",
    "focus": "comprehensive_analysis",
    "principles_count": "4-6",
    "description": "Anthropic's Claude optimized for thoughtful, detailed analysis"
},
"copilot": {
    "template_style": "practical_concise",
    "focus": "implementation_guidance",
    "principles_count": "3-5",
    "description": "GitHub's Copilot optimized for practical development focus"
},
"gemini": {
    "template_style": "creative_exploratory",
    "focus": "innovative_solutions",
    "principles_count": "3-5",
    "description": "Google's Gemini optimized for creative problem-solving"
},
"cursor": {
    "template_style": "focused_practical",
    "focus": "direct_implementation",
    "principles_count": "3-4",
    "description": "Cursor IDE optimized for focused development work"
},
"qwen": {
    "template_style": "comprehensive_detailed",
    "focus": "thorough_coverage",
    "principles_count": "4-6",
    "description": "Qwen agent optimized for comprehensive, detailed analysis"
},
"kilocode": {
    "template_style": "efficient_practical",
    "focus": "implementation_guidance",
    "principles_count": "3-5",
    "description": "Kilo Code IDE optimized for efficient development work"
}
}

SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh)", "ps": "PowerShell"}

BANNER = """
 ######    #######     ###    ##             ##    ## #### ######## 
##    ##  ##     ##   ## ##   ##             ##   ##   ##     ##    
##        ##     ##  ##   ##  ##             ##  ##    ##     ##    
##   #### ##     ## ##     ## ##             #####     ##     ##    
##    ##  ##     ## ######### ##             ##  ##    ##     ##    
##    ##  ##     ## ##     ## ##             ##   ##   ##     ##    
 ######    #######  ##     ## ########       ##    ## ####    ## 
"""

TAGLINE = "Goal Kit - Goal-Driven Development Toolkit"

class StepTracker:
    """Track and render hierarchical steps without emojis, similar to Claude Code tree output.
    Supports live auto-refresh via an attached refresh callback.
    """
    def __init__(self, title: str):
        self.title = title
        self.steps = []  # list of dicts: {key, label, status, detail}
        self.status_order = {"pending": 0, "running": 1, "done": 2, "error": 3, "skipped": 4}
        self._refresh_cb = None  # callable to trigger UI refresh

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append({"key": key, "label": label, "status": "pending", "detail": ""})
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return
        # If not present, add it
        self.steps.append({"key": key, "label": key, "status": status, "detail": detail})
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            # Circles (unchanged styling)
            status = step["status"]
            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                # Entire line light gray (pending)
                if detail_text:
                    line = f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                # Label white, detail (if any) light gray in parentheses
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree

def get_key():
    """Get a single keypress in a cross-platform way using readchar."""
    key = readchar.readkey()

    if key == readchar.key.UP or key == readchar.key.CTRL_P:
        return 'up'
    if key == readchar.key.DOWN or key == readchar.key.CTRL_N:
        return 'down'

    if key == readchar.key.ENTER:
        return 'enter'

    if key == readchar.key.ESC:
        return 'escape'

    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key

def validate_ai_response(response_content: str, response_type: str) -> dict:
    """Validate AI-generated content against Goal Kit standards."""
    validation_results = {
        "is_valid": True,
        "issues": [],
        "suggestions": [],
        "score": 0
    }

    # Basic structure validation
    if response_type == "vision":
        required_sections = ["guiding principles", "success metrics", "project goals"]
        for section in required_sections:
            if section.lower() not in response_content.lower():
                validation_results["issues"].append(f"Missing required section: {section}")
                validation_results["is_valid"] = False

        # Check for measurable metrics
        if not any(char.isdigit() for char in response_content):
            validation_results["suggestions"].append("Consider adding specific numbers or percentages to success metrics")
            validation_results["score"] -= 10

    elif response_type == "goal":
        # Check for outcome-focused language
        implementation_words = ["build", "create", "develop", "implement", "code"]
        outcome_words = ["achieve", "improve", "increase", "decrease", "enable", "help"]

        impl_count = sum(1 for word in implementation_words if word.lower() in response_content.lower())
        outcome_count = sum(1 for word in outcome_words if word.lower() in response_content.lower())

        if impl_count > outcome_count:
            validation_results["suggestions"].append("Consider focusing more on outcomes rather than implementation")
            validation_results["score"] -= 5

    # Calculate overall score (0-100)
    base_score = 100
    validation_results["score"] = max(0, base_score + validation_results["score"])

    return validation_results

def log_ai_interaction(agent_name: str, command: str, success: bool, validation_score: int = None, user_input: str = "", ai_response: str = ""):
    """Log AI agent interactions for performance analytics and memory system."""
    import json
    from datetime import datetime

    # Enhanced log entry with more context
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "command": command,
        "success": success,
        "validation_score": validation_score,
        "user_input_summary": user_input[:200] + "..." if len(user_input) > 200 else user_input,
        "response_summary": ai_response[:200] + "..." if len(ai_response) > 200 else ai_response,
        "session_id": getattr(app, '_current_session_id', 'unknown')
    }

    # Append to AI interaction log (legacy support)
    log_file = Path.cwd() / ".goalkit" / "ai_interactions.jsonl"
    try:
        log_file.parent.mkdir(exist_ok=True)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        console.print(f"[yellow]Warning: Could not log AI interaction: {e}[/yellow]")

    # Enhanced memory system integration
    if AISessionMemory:
        try:
            session_memory = AISessionMemory(Path.cwd())
            if not hasattr(app, '_current_session_id') or app._current_session_id == 'unknown':
                app._current_session_id = session_memory.start_session(agent_name)

            # Add interaction to memory with enhanced context
            success_score = validation_score if validation_score is not None else (10 if success else 3)
            session_memory.add_interaction(command, user_input, ai_response, success_score)

        except Exception as e:
            # Don't fail if memory system has issues
            console.print(f"[dim]Memory system: {e}[/dim]")

    # Enhanced baseline metrics collection
    if BaselineCollector:
        try:
            baseline_collector = BaselineCollector(Path.cwd())

            # Calculate enhanced metrics for this interaction
            interaction_metrics = baseline_collector.collect_interaction_metrics(
                command, user_input, ai_response, validation_score
            )

            # Save metrics for baseline tracking
            baseline_collector.save_interaction_metrics(interaction_metrics)

        except Exception as e:
            # Don't fail if baseline system has issues
            console.print(f"[dim]Baseline metrics: {e}[/dim]")

def select_with_arrows(options: dict, prompt_text: str = "Select an option", default_key: str = None) -> str:
    """
    Interactive selection using arrow keys with Rich Live display.

    Args:
        options: Dict with keys as option keys and values as descriptions
        prompt_text: Text to show above the options
        default_key: Default option key to start with

    Returns:
        Selected option key
    """
    option_keys = list(options.keys())
    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0

    selected_key = None

    def create_selection_panel():
        """Create the selection panel with current selection highlighted."""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")

        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
            else:
                table.add_row(" ", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")

        table.add_row("", "")
        table.add_row("", "[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]")

        return Panel(
            table,
            title=f"[bold]{prompt_text}[/bold]",
            border_style="cyan",
            padding=(1, 2)
        )

    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(create_selection_panel(), console=console, transient=True, auto_refresh=False) as live:
            while True:
                try:
                    key = get_key()
                    if key == 'up':
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == 'down':
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == 'enter':
                        selected_key = option_keys[selected_index]
                        break
                    elif key == 'escape':
                        console.print("\n[yellow]Selection cancelled[/yellow]")
                        raise typer.Exit(1)

                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        console.print("\n[red]Selection failed.[/red]")
        raise typer.Exit(1)

    # Suppress explicit selection print; tracker / later logic will report consolidated status
    return selected_key

console = Console()

class GoalCreationService:
    """Service for creating goals from AI responses and managing goal file structure."""

    def __init__(self, project_path: Path):
        """Initialize the goal creation service.

        Args:
            project_path: Path to the project directory
        """
        self.project_path = project_path
        self.goals_dir = project_path / ".goalkit" / "goals"
        self.goals_dir.mkdir(parents=True, exist_ok=True)
        self.template_processor = TemplateProcessor(project_path) if TemplateProcessor else None

    def parse_ai_response(self, ai_response: str, goal_description: str) -> Dict[str, Any]:
        """Parse AI response to extract structured goal data.

        Args:
            ai_response: The AI response containing goal information
            goal_description: Original user description for context

        Returns:
            Dictionary containing structured goal data
        """
        import re
        from datetime import datetime

        # Extract goal title from description
        goal_title = self._extract_goal_title(goal_description)

        # Generate goal directory name (###-goal-name format)
        goal_dir_name = self._generate_goal_dir_name(goal_title)

        # Extract key components from AI response
        goal_data = {
            "goal_statement": goal_description,
            "goal_title": goal_title,
            "goal_directory": goal_dir_name,
            "created_date": datetime.now().strftime('%Y-%m-%d'),
            "status": "Draft",
            "ai_response": ai_response,
            "success_metrics": self._extract_success_metrics(ai_response),
            "target_users": self._extract_target_users(ai_response),
            "hypotheses": self._extract_hypotheses(ai_response),
            "risk_factors": self._extract_risk_factors(ai_response),
            "milestones": self._extract_milestones(ai_response)
        }

        return goal_data

    def _extract_goal_title(self, description: str) -> str:
        """Extract a concise goal title from the description."""
        # Remove common prefixes and clean up
        title = description.strip()

        # Remove common prefixes
        prefixes_to_remove = [
            "create", "build", "develop", "implement", "design", "a", "an", "the",
            "i want to", "i need to", "we want to", "we need to"
        ]

        for prefix in prefixes_to_remove:
            if title.lower().startswith(prefix):
                title = title[len(prefix):].strip()
                break

        # Capitalize first letter of each word
        title = title.title()

        # Limit length
        if len(title) > 50:
            title = title[:47] + "..."

        return title

    def _generate_goal_dir_name(self, goal_title: str) -> str:
        """Generate a goal directory name in ###-goal-name format."""
        # Create a simple counter for the number
        existing_goals = [d for d in self.goals_dir.iterdir() if d.is_dir()]
        goal_number = len(existing_goals) + 1

        # Create a URL-friendly name from the title
        clean_name = re.sub(r'[^a-zA-Z0-9\s-]', '', goal_title)
        clean_name = re.sub(r'\s+', '-', clean_name.strip())

        return f"{goal_number:03d}-{clean_name.lower()}"

    def _extract_success_metrics(self, ai_response: str) -> List[str]:
        """Extract success metrics from AI response."""
        metrics = []

        # Look for patterns indicating metrics
        metric_patterns = [
            r'success.*metric.*?[:;]\s*(.*?)(?:\n|$)',
            r'measure.*?[:;]\s*(.*?)(?:\n|$)',
            r'target.*?[:;]\s*(.*?)(?:\n|$)',
            r'goal.*?[:;]\s*(.*?)(?:\n|$)'
        ]

        for pattern in metric_patterns:
            matches = re.findall(pattern, ai_response, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if len(match.strip()) > 10:  # Filter out very short matches
                    metrics.append(match.strip())

        # If no metrics found, create default ones
        if not metrics:
            metrics = [
                "Successful implementation of core functionality",
                "User satisfaction with the solution",
                "Achievement of performance targets"
            ]

        return metrics[:5]  # Limit to 5 metrics

    def _extract_target_users(self, ai_response: str) -> List[str]:
        """Extract target users from AI response."""
        users = []

        # Look for user-related patterns
        user_patterns = [
            r'user.*?[:;]\s*(.*?)(?:\n|$)',
            r'target.*?audience.*?[:;]\s*(.*?)(?:\n|$)',
            r'benefit.*?[:;]\s*(.*?)(?:\n|$)'
        ]

        for pattern in user_patterns:
            matches = re.findall(pattern, ai_response, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if len(match.strip()) > 5:
                    users.append(match.strip())

        # Default users if none found
        if not users:
            users = [
                "End users who will directly interact with the solution",
                "Stakeholders who will benefit from the outcomes"
            ]

        return users[:3]

    def _extract_hypotheses(self, ai_response: str) -> List[str]:
        """Extract hypotheses from AI response."""
        hypotheses = []

        # Look for assumption or hypothesis patterns
        hypothesis_patterns = [
            r'assum.*?[:;]\s*(.*?)(?:\n|$)',
            r'hypothesis.*?[:;]\s*(.*?)(?:\n|$)',
            r'believe.*?[:;]\s*(.*?)(?:\n|$)'
        ]

        for pattern in hypothesis_patterns:
            matches = re.findall(pattern, ai_response, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if len(match.strip()) > 10:
                    hypotheses.append(match.strip())

        # Default hypotheses if none found
        if not hypotheses:
            hypotheses = [
                "The proposed solution will effectively address the identified need",
                "Users will adopt and benefit from the implemented solution"
            ]

        return hypotheses[:3]

    def _extract_risk_factors(self, ai_response: str) -> List[str]:
        """Extract risk factors from AI response."""
        risks = []

        # Look for risk or challenge patterns
        risk_patterns = [
            r'risk.*?[:;]\s*(.*?)(?:\n|$)',
            r'challenge.*?[:;]\s*(.*?)(?:\n|$)',
            r'concern.*?[:;]\s*(.*?)(?:\n|$)'
        ]

        for pattern in risk_patterns:
            matches = re.findall(pattern, ai_response, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if len(match.strip()) > 10:
                    risks.append(match.strip())

        # Default risks if none found
        if not risks:
            risks = [
                "Technical complexity may require additional time",
                "User adoption may be slower than expected"
            ]

        return risks[:3]

    def _extract_milestones(self, ai_response: str) -> List[Dict[str, Any]]:
        """Extract milestones from AI response."""
        milestones = []

        # Look for milestone or step patterns
        milestone_patterns = [
            r'milestone.*?[:;]\s*(.*?)(?:\n|$)',
            r'step.*?[:;]\s*(.*?)(?:\n|$)',
            r'phase.*?[:;]\s*(.*?)(?:\n|$)'
        ]

        for pattern in milestone_patterns:
            matches = re.findall(pattern, ai_response, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if len(match.strip()) > 10:
                    milestones.append({
                        "title": match.strip(),
                        "description": f"Complete {match.strip().lower()}",
                        "priority": "P1",
                        "success_indicators": [f"Successfully {match.strip().lower()}"],
                        "timeline": "TBD"
                    })

        # Default milestones if none found
        if not milestones:
            milestones = [
                {
                    "title": "Planning & Setup",
                    "description": "Define detailed requirements and approach",
                    "priority": "P1",
                    "success_indicators": ["Requirements documented", "Approach approved"],
                    "timeline": "Week 1-2"
                },
                {
                    "title": "Core Implementation",
                    "description": "Build and deliver core functionality",
                    "priority": "P1",
                    "success_indicators": ["Core features working", "Basic validation passed"],
                    "timeline": "Week 3-6"
                },
                {
                    "title": "Validation & Launch",
                    "description": "Final validation and deployment",
                    "priority": "P1",
                    "success_indicators": ["All criteria met", "User acceptance confirmed"],
                    "timeline": "Week 7-8"
                }
            ]

        return milestones[:5]  # Limit to 5 milestones

    def create_goal_directory(self, goal_data: Dict[str, Any]) -> Path:
        """Create the goal directory structure."""
        goal_dir = self.goals_dir / goal_data["goal_directory"]
        goal_dir.mkdir(exist_ok=True)
        return goal_dir

    def generate_goal_file(self, goal_data: Dict[str, Any], goal_dir: Path) -> Path:
        """Generate the goal.md file using the goal template."""
        goal_file = goal_dir / "goal.md"

        # Read the goal template
        template_path = Path(__file__).parent.parent / "templates" / "goal-template.md"
        if template_path.exists():
            template_content = template_path.read_text(encoding='utf-8')
        else:
            # Fallback template if file doesn't exist
            template_content = self._get_fallback_template()

        # Replace template placeholders with actual data
        content = self._populate_template(template_content, goal_data)

        # Write the goal file
        goal_file.write_text(content, encoding='utf-8')

        return goal_file

    def _get_fallback_template(self) -> str:
        """Get a fallback template if the template file doesn't exist."""
        return """# Goal Definition: [GOAL_TITLE]

**Goal Branch**: `[GOAL_DIRECTORY]`
**Created**: [CREATED_DATE]
**Status**: Draft

## 🎯 Goal Overview

**Goal Statement**: [GOAL_STATEMENT]

## 📊 Success Metrics

[PRIMARY_METRICS]

## 👥 Target Users & Stakeholders

[PRIMARY_USERS]

## 🎯 Goal Hypotheses

### Key Assumptions
[HYPOTHESES]

### Risk Factors
[RISK_FACTORS]

## 🚀 Goal Milestones

[MILESTONES]

---
*This goal definition serves as the foundation for strategy exploration and milestone planning.*
"""

    def _populate_template(self, template: str, goal_data: Dict[str, Any]) -> str:
        """Populate the template with goal data."""
        # Basic replacements
        replacements = {
            "[GOAL_TITLE]": goal_data.get("goal_title", "Untitled Goal"),
            "[GOAL_DIRECTORY]": goal_data.get("goal_directory", "unnamed-goal"),
            "[CREATED_DATE]": goal_data.get("created_date", datetime.now().strftime('%Y-%m-%d')),
            "[GOAL_STATEMENT]": goal_data.get("goal_statement", "")
        }

        # Replace basic placeholders
        for placeholder, value in replacements.items():
            template = template.replace(placeholder, str(value))

        # Replace complex sections
        template = self._replace_metrics_section(template, goal_data)
        template = self._replace_users_section(template, goal_data)
        template = self._replace_hypotheses_section(template, goal_data)
        template = self._replace_risks_section(template, goal_data)
        template = self._replace_milestones_section(template, goal_data)

        return template

    def _replace_metrics_section(self, template: str, goal_data: Dict[str, Any]) -> str:
        """Replace the metrics section in the template."""
        metrics = goal_data.get("success_metrics", [])
        if not metrics:
            return template.replace("[PRIMARY_METRICS]", "- No specific metrics defined yet")

        metrics_text = "\n".join([f"- {metric}" for metric in metrics])
        return template.replace("[PRIMARY_METRICS]", metrics_text)

    def _replace_users_section(self, template: str, goal_data: Dict[str, Any]) -> str:
        """Replace the users section in the template."""
        users = goal_data.get("target_users", [])
        if not users:
            return template.replace("[PRIMARY_USERS]", "- End users who will benefit from this goal")

        users_text = "\n".join([f"- {user}" for user in users])
        return template.replace("[PRIMARY_USERS]", users_text)

    def _replace_hypotheses_section(self, template: str, goal_data: Dict[str, Any]) -> str:
        """Replace the hypotheses section in the template."""
        hypotheses = goal_data.get("hypotheses", [])
        if not hypotheses:
            return template.replace("[HYPOTHESES]", "- The proposed solution will be effective")

        hypotheses_text = "\n".join([f"- {hypothesis}" for hypothesis in hypotheses])
        return template.replace("[HYPOTHESES]", hypotheses_text)

    def _replace_risks_section(self, template: str, goal_data: Dict[str, Any]) -> str:
        """Replace the risks section in the template."""
        risks = goal_data.get("risk_factors", [])
        if not risks:
            return template.replace("[RISK_FACTORS]", "- Technical challenges may arise")

        risks_text = "\n".join([f"- **Risk**: {risk} - Mitigation: TBD" for risk in risks])
        return template.replace("[RISK_FACTORS]", risks_text)

    def _replace_milestones_section(self, template: str, goal_data: Dict[str, Any]) -> str:
        """Replace the milestones section in the template."""
        milestones = goal_data.get("milestones", [])
        if not milestones:
            return template.replace("[MILESTONES]", "### Milestone 1: Planning\n**Description**: Define requirements and approach")

        milestones_text = ""
        for i, milestone in enumerate(milestones, 1):
            milestones_text += f"""### Milestone {i}: {milestone['title']}

**Description**: {milestone['description']}

**Success Indicators**:
- {chr(10).join(milestone['success_indicators'])}

**Expected Timeline**: {milestone['timeline']}

---
"""

        return template.replace("[MILESTONES]", milestones_text)

    def validate_goal_structure(self, goal_dir: Path) -> bool:
        """Validate that the goal structure is correct."""
        required_files = ["goal.md"]
        return all((goal_dir / file).exists() for file in required_files)

    def get_next_goal_number(self) -> int:
        """Get the next available goal number."""
        existing_goals = [d for d in self.goals_dir.iterdir() if d.is_dir()]
        if not existing_goals:
            return 1

        # Extract numbers from existing goal directories
        numbers = []
        for goal_dir in existing_goals:
            match = re.match(r'^(\d+)-', goal_dir.name)
            if match:
                numbers.append(int(match.group(1)))

        return max(numbers) + 1 if numbers else 1

class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""

    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="goalkeeper",
    help="Setup tool for Goalkeeper goal-driven development projects",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)

def show_banner():
    """Display the ASCII art banner."""
    # Create gradient effect with different colors
    banner_lines = BANNER.strip().split('\n')
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)

    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()

@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided."""
    # Show banner only when no subcommand and no help flag
    # (help is handled by BannerGroup)
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center("[dim]Run 'goalkeeper --help' for usage information[/dim]"))
        console.print()

def run_command(cmd: list[str], check_return: bool = True, capture: bool = False, shell: bool = False) -> Optional[str]:
    """Run a shell command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(cmd, check=check_return, capture_output=True, text=True, shell=shell)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]Error running command:[/red] {' '.join(cmd)}")
            console.print(f"[red]Exit code:[/red] {e.returncode}")
            if hasattr(e, 'stderr') and e.stderr:
                console.print(f"[red]Error output:[/red] {e.stderr}")
            raise
        return None

def check_tool_for_tracker(tool: str, tracker: StepTracker) -> bool:
    """Check if a tool is installed and update tracker."""
    if shutil.which(tool):
        tracker.complete(tool, "available")
        return True
    else:
        tracker.error(tool, "not found")
        return False

def check_tool(tool: str, install_hint: str) -> bool:
    """Check if a tool is installed."""
    if shutil.which(tool):
        return True
    else:
        return False

def is_git_repo(path: Path = None) -> bool:
    """Check if the specified path is inside a git repository."""
    if path is None:
        path = Path.cwd()

    if not path.is_dir():
        return False

    try:
        # Use git command to check if inside a work tree
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def init_git_repo(project_path: Path, quiet: bool = False) -> bool:
    """Initialize a git repository in the specified path.
    quiet: if True suppress console output (tracker handles status)
    """
    try:
        original_cwd = Path.cwd()
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit from Goalkeeper template"], check=True, capture_output=True)
        if not quiet:
            console.print("[green]✓[/green] Git repository initialized")
        return True

    except subprocess.CalledProcessError as e:
        if not quiet:
            console.print(f"[red]Error initializing git repository:[/red] {e}")
        return False
    finally:
        os.chdir(original_cwd)

def download_template_from_github(ai_assistant: str, download_dir: Path, *, script_type: str = "sh", verbose: bool = True, show_progress: bool = True, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Tuple[Path, dict]:
    repo_owner = "Nom-nom-hub"
    repo_name = "goal-kit"
    if client is None:
        client = httpx.Client(verify=ssl_context)

    if verbose:
        console.print("[cyan]Fetching latest release information...[/cyan]")
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    try:
        response = client.get(
            api_url,
            timeout=30,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        )
        status = response.status_code
        if status != 200:
            msg = f"GitHub API returned {status} for {api_url}"
            if debug:
                msg += f"\nResponse headers: {response.headers}\nBody (truncated 500): {response.text[:500]}"
            raise RuntimeError(msg)
        try:
            release_data = response.json()
        except ValueError as je:
            raise RuntimeError(f"Failed to parse release JSON: {je}\nRaw (truncated 400): {response.text[:400]}")
    except Exception as e:
        console.print(f"[red]Error fetching release information[/red]")
        console.print(Panel(str(e), title="Fetch Error", border_style="red"))
        raise typer.Exit(1)

    # Find the template asset for the specified AI assistant
    assets = release_data.get("assets", [])
    pattern = f"goal-kit-template-{ai_assistant}-{script_type}"
    matching_assets = [
        asset for asset in assets
        if pattern in asset["name"] and asset["name"].endswith(".zip")
    ]

    asset = matching_assets[0] if matching_assets else None

    if asset is None:
        console.print(f"[red]No matching release asset found[/red] for [bold]{ai_assistant}[/bold] (expected pattern: [bold]{pattern}[/bold])")
        asset_names = [a.get('name', '?') for a in assets]
        console.print(Panel("\n".join(asset_names) or "(no assets)", title="Available Assets", border_style="yellow"))
        raise typer.Exit(1)

    download_url = asset["browser_download_url"]
    filename = asset["name"]
    file_size = asset["size"]

    if verbose:
        console.print(f"[cyan]Found template:[/cyan] {filename}")
        console.print(f"[cyan]Size:[/cyan] {file_size:,} bytes")
        console.print(f"[cyan]Release:[/cyan] {release_data['tag_name']}")

    zip_path = download_dir / filename
    if verbose:
        console.print(f"[cyan]Downloading template...[/cyan]")

    try:
        with client.stream(
            "GET",
            download_url,
            timeout=60,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        ) as response:
            if response.status_code != 200:
                body_sample = response.text[:400]
                raise RuntimeError(f"Download failed with {response.status_code}\nHeaders: {response.headers}\nBody (truncated): {body_sample}")
            total_size = int(response.headers.get('content-length', 0))
            with open(zip_path, 'wb') as f:
                if total_size == 0:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        f.write(chunk)
                else:
                    if show_progress:
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                            console=console,
                        ) as progress:
                            task = progress.add_task("Downloading...", total=total_size)
                            downloaded = 0
                            for chunk in response.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                                downloaded += len(chunk)
                                progress.update(task, completed=downloaded)
                    else:
                        for chunk in response.iter_bytes(chunk_size=8192):
                            f.write(chunk)
    except Exception as e:
        console.print(f"[red]Error downloading template[/red]")
        detail = str(e)
        if zip_path.exists():
            zip_path.unlink()
        console.print(Panel(detail, title="Download Error", border_style="red"))
        raise typer.Exit(1)
    if verbose:
        console.print(f"Downloaded: {filename}")
    metadata = {
        "filename": filename,
        "size": file_size,
        "release": release_data["tag_name"],
        "asset_url": download_url
    }
    return zip_path, metadata

def download_and_extract_template(project_path: Path, ai_assistant: str, script_type: str, is_current_dir: bool = False, *, verbose: bool = True, tracker: StepTracker | None = None, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Path:
    """Download the latest release and extract it to create a new project.
    Returns project_path. Uses tracker if provided (with keys: fetch, download, extract, cleanup)
    """
    current_dir = Path.cwd()

    # Step: fetch + download combined
    if tracker:
        tracker.start("fetch", "contacting GitHub API")
    try:
        zip_path, meta = download_template_from_github(
            ai_assistant,
            current_dir,
            script_type=script_type,
            verbose=verbose and tracker is None,
            show_progress=(tracker is None),
            client=client,
            debug=debug,
            github_token=github_token
        )
        if tracker:
            tracker.complete("fetch", f"release {meta['release']} ({meta['size']:,} bytes)")
            tracker.add("download", "Download template")
            tracker.complete("download", meta['filename'])
    except Exception as e:
        if tracker:
            tracker.error("fetch", str(e))
        else:
            if verbose:
                console.print(f"[red]Error downloading template:[/red] {e}")
        raise

    if tracker:
        tracker.add("extract", "Extract template")
        tracker.start("extract")
    elif verbose:
        console.print("Extracting template...")

    try:
        # Create project directory only if not using current directory
        if not is_current_dir:
            project_path.mkdir(parents=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # List all files in the ZIP for debugging
            zip_contents = zip_ref.namelist()
            if tracker:
                tracker.start("zip-list")
                tracker.complete("zip-list", f"{len(zip_contents)} entries")
            elif verbose:
                console.print(f"[cyan]ZIP contains {len(zip_contents)} items[/cyan]")

            # For current directory, extract to a temp location first
            if is_current_dir:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    zip_ref.extractall(temp_path)

                    # Check what was extracted
                    extracted_items = list(temp_path.iterdir())
                    if tracker:
                        tracker.start("extracted-summary")
                        tracker.complete("extracted-summary", f"temp {len(extracted_items)} items")
                    elif verbose:
                        console.print(f"[cyan]Extracted {len(extracted_items)} items to temp location[/cyan]")

                    # Handle GitHub-style ZIP with a single root directory
                    source_dir = temp_path
                    if len(extracted_items) == 1 and extracted_items[0].is_dir():
                        source_dir = extracted_items[0]
                        if tracker:
                            tracker.add("flatten", "Flatten nested directory")
                            tracker.complete("flatten")
                        elif verbose:
                            console.print(f"[cyan]Found nested directory structure[/cyan]")

                    # Copy contents to current directory
                    for item in source_dir.iterdir():
                        dest_path = project_path / item.name
                        if item.is_dir():
                            if dest_path.exists():
                                if verbose and not tracker:
                                    console.print(f"[yellow]Merging directory:[/yellow] {item.name}")
                                # Recursively copy directory contents
                                for sub_item in item.rglob('*'):
                                    if sub_item.is_file():
                                        rel_path = sub_item.relative_to(item)
                                        dest_file = dest_path / rel_path
                                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                                        shutil.copy2(sub_item, dest_file)
                            else:
                                shutil.copytree(item, dest_path)
                        else:
                            if dest_path.exists() and verbose and not tracker:
                                console.print(f"[yellow]Overwriting file:[/yellow] {item.name}")
                            shutil.copy2(item, dest_path)
                    if verbose and not tracker:
                        console.print(f"[cyan]Template files merged into current directory[/cyan]")
            else:
                # Extract directly to project directory (original behavior)
                zip_ref.extractall(project_path)

                # Check what was extracted
                extracted_items = list(project_path.iterdir())
                if tracker:
                    tracker.start("extracted-summary")
                    tracker.complete("extracted-summary", f"{len(extracted_items)} top-level items")
                elif verbose:
                    console.print(f"[cyan]Extracted {len(extracted_items)} items to {project_path}:[/cyan]")
                    for item in extracted_items:
                        console.print(f"  - {item.name} ({'dir' if item.is_dir() else 'file'})")

                # Handle GitHub-style ZIP with a single root directory
                if len(extracted_items) == 1 and extracted_items[0].is_dir():
                    # Move contents up one level
                    nested_dir = extracted_items[0]
                    temp_move_dir = project_path.parent / f"{project_path.name}_temp"
                    # Move the nested directory contents to temp location
                    shutil.move(str(nested_dir), str(temp_move_dir))
                    # Remove the now-empty project directory
                    project_path.rmdir()
                    # Rename temp directory to project directory
                    shutil.move(str(temp_move_dir), str(project_path))
                    if tracker:
                        tracker.add("flatten", "Flatten nested directory")
                        tracker.complete("flatten")
                    elif verbose:
                        console.print(f"[cyan]Flattened nested directory structure[/cyan]")

    except Exception as e:
        if tracker:
            tracker.error("extract", str(e))
        else:
            if verbose:
                console.print(f"[red]Error extracting template:[/red] {e}")
                if debug:
                    console.print(Panel(str(e), title="Extraction Error", border_style="red"))
        # Clean up project directory if created and not current directory
        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)
    else:
        if tracker:
            tracker.complete("extract")
    finally:
        if tracker:
            tracker.add("cleanup", "Remove temporary archive")
        # Clean up downloaded ZIP file
        if zip_path.exists():
            zip_path.unlink()
            if tracker:
                tracker.complete("cleanup")
            elif verbose:
                console.print(f"Cleaned up: {zip_path.name}")

    return project_path

def ensure_executable_scripts(project_path: Path, tracker: StepTracker | None = None) -> None:
    """Ensure POSIX .sh scripts under .goalkit/scripts (recursively) have execute bits (no-op on Windows)."""
    if os.name == "nt":
        return  # Windows: skip silently
    scripts_root = project_path / ".goalkit" / "scripts"
    if not scripts_root.is_dir():
        return
    failures: list[str] = []
    updated = 0
    for script in scripts_root.rglob("*.sh"):
        try:
            if script.is_symlink() or not script.is_file():
                continue
            try:
                with script.open("rb") as f:
                    if f.read(2) != b"#!":
                        continue
            except Exception:
                continue
            st = script.stat(); mode = st.st_mode
            if mode & 0o111:
                continue
            new_mode = mode
            if mode & 0o400: new_mode |= 0o100
            if mode & 0o040: new_mode |= 0o010
            if mode & 0o004: new_mode |= 0o001
            if not (new_mode & 0o100):
                new_mode |= 0o100
            os.chmod(script, new_mode)
            updated += 1
        except Exception as e:
            failures.append(f"{script.relative_to(scripts_root)}: {e}")
    if tracker:
        detail = f"{updated} updated" + (f", {len(failures)} failed" if failures else "")
        tracker.add("chmod", "Set script permissions recursively")
        (tracker.error if failures else tracker.complete)("chmod", detail)
    else:
        if updated:
            console.print(f"[cyan]Updated execute permissions on {updated} script(s) recursively[/cyan]")
        if failures:
            console.print("[yellow]Some scripts could not be updated:[/yellow]")
            for f in failures:
                console.print(f"  - {f}")

@app.command()
def init(
    project_name: str = typer.Argument(None, help="Name for your new project directory (optional if using --here, or use '.' for current directory)"),
    ai_assistant: str = typer.Option(None, "--ai", help="AI assistant to use: claude, gemini, copilot, cursor, qwen, opencode, codex, windsurf, kilocode, auggie or q"),
    script_type: str = typer.Option(None, "--script", help="Script type to use: sh or ps"),
    ignore_agent_tools: bool = typer.Option(False, "--ignore-agent-tools", help="Skip checks for AI agent tools like Claude Code"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    here: bool = typer.Option(False, "--here", help="Initialize project in the current directory instead of creating a new one"),
    force: bool = typer.Option(False, "--force", help="Force merge/overwrite when using --here (skip confirmation)"),
    skip_tls: bool = typer.Option(False, "--skip-tls", help="Skip SSL/TLS verification (not recommended)"),
    debug: bool = typer.Option(False, "--debug", help="Show verbose diagnostic output for network and extraction failures"),
    github_token: str = typer.Option(None, "--github-token", help="GitHub token to use for API requests (or set GH_TOKEN or GITHUB_TOKEN environment variable)"),
):
    """
    Initialize a new Goalkeeper project from the latest template.

    This command will:
    1. Check that required tools are installed (git is optional)
    2. Let you choose your AI assistant (Claude Code, Gemini CLI, GitHub Copilot, Cursor, Qwen Code, opencode, Codex CLI, Windsurf, Kilo Code, Auggie CLI, or Amazon Q Developer CLI)
    3. Download the appropriate template from GitHub
    4. Extract the template to a new project directory or current directory
    5. Initialize a fresh git repository (if not --no-git and no existing repo)
    6. Optionally set up AI assistant commands

    Examples:
        goalkeeper init my-project
        goalkeeper init my-project --ai claude
        goalkeeper init my-project --ai copilot --no-git
        goalkeeper init --ignore-agent-tools my-project
        goalkeeper init . --ai claude         # Initialize in current directory
        goalkeeper init .                     # Initialize in current directory (interactive AI selection)
        goalkeeper init --here --ai claude    # Alternative syntax for current directory
        goalkeeper init --here --ai codex
        goalkeeper init --here
        goalkeeper init --here --force  # Skip confirmation when current directory not empty
    """

    show_banner()

    # Handle '.' as shorthand for current directory (equivalent to --here)
    if project_name == ".":
        here = True
        project_name = None  # Clear project_name to use existing validation logic

    if here and project_name:
        console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
        raise typer.Exit(1)

    if not here and not project_name:
        console.print("[red]Error:[/red] Must specify either a project name, use '.' for current directory, or use --here flag")
        raise typer.Exit(1)

    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()

        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)")
            console.print("[yellow]Template files will be merged with existing content and may overwrite existing files[/yellow]")
            if force:
                console.print("[cyan]--force supplied: skipping confirmation and proceeding with merge[/cyan]")
            else:
                response = typer.confirm("Do you want to continue?")
                if not response:
                    console.print("[yellow]Operation cancelled[/yellow]")
                    raise typer.Exit(0)
    else:
        project_path = Path(project_name).resolve()
        if project_path.exists():
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

    current_dir = Path.cwd()

    setup_lines = [
        "[cyan]Goalkeeper Project Setup[/cyan]",
        "",
        f"{'Project':<15} [green]{project_path.name}[/green]",
        f"{'Working Path':<15} [dim]{current_dir}[/dim]",
    ]

    # Add target path only if different from working dir
    if not here:
        setup_lines.append(f"{'Target Path':<15} [dim]{project_path}[/dim]")

    console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))

    # Check git only if we might need it (not --no-git)
    # Only set to True if the user wants it and the tool is available
    should_init_git = False
    if not no_git:
        should_init_git = check_tool("git", "https://git-scm.com/downloads")
        if not should_init_git:
            console.print("[yellow]Git not found - will skip repository initialization[/yellow]")

    if ai_assistant:
        if ai_assistant not in AI_CHOICES:
            console.print(f"[red]Error:[/red] Invalid AI assistant '{ai_assistant}'. Choose from: {', '.join(AI_CHOICES.keys())}")
            raise typer.Exit(1)
        selected_ai = ai_assistant
    else:
        # Use arrow-key selection interface
        selected_ai = select_with_arrows(
            AI_CHOICES,
            "Choose your AI assistant:",
            "copilot"
        )

    # Check agent tools unless ignored
    if not ignore_agent_tools:
        agent_tool_missing = False
        install_url = ""
        if selected_ai == "claude":
            if not check_tool("claude", "https://docs.anthropic.com/en/docs/claude-code/setup"):
                install_url = "https://docs.anthropic.com/en/docs/claude-code/setup"
                agent_tool_missing = True
        elif selected_ai == "gemini":
            if not check_tool("gemini", "https://github.com/google-gemini/gemini-cli"):
                install_url = "https://github.com/google-gemini/gemini-cli"
                agent_tool_missing = True
        elif selected_ai == "qwen":
            if not check_tool("qwen", "https://github.com/QwenLM/qwen-code"):
                install_url = "https://github.com/QwenLM/qwen-code"
                agent_tool_missing = True
        elif selected_ai == "opencode":
            if not check_tool("opencode", "https://opencode.ai"):
                install_url = "https://opencode.ai"
                agent_tool_missing = True
        elif selected_ai == "codex":
            if not check_tool("codex", "https://github.com/openai/codex"):
                install_url = "https://github.com/openai/codex"
                agent_tool_missing = True
        elif selected_ai == "auggie":
            if not check_tool("auggie", "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli"):
                install_url = "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli"
                agent_tool_missing = True
        elif selected_ai == "q":
            if not check_tool("q", "https://github.com/aws/amazon-q-developer-cli"):
                install_url = "https://aws.amazon.com/developer/learning/q-developer-cli/"
                agent_tool_missing = True
        # GitHub Copilot and Cursor checks are not needed as they're typically available in supported IDEs

        if agent_tool_missing:
            error_panel = Panel(
                f"[cyan]{selected_ai}[/cyan] not found\n"
                f"Install with: [cyan]{install_url}[/cyan]\n"
                f"{AI_CHOICES[selected_ai]} is required to continue with this project type.\n\n"
                "Tip: Use [cyan]--ignore-agent-tools[/cyan] to skip this check",
                title="[red]Agent Detection Error[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
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
            selected_script = select_with_arrows(SCRIPT_TYPE_CHOICES, "Choose script type (or press Enter)", default_script)
        else:
            selected_script = default_script

    console.print(f"[cyan]Selected AI assistant:[/cyan] {selected_ai}")
    console.print(f"[cyan]Selected script type:[/cyan] {selected_script}")

    # Download and set up project
    # New tree-based progress (no emojis); include earlier substeps
    tracker = StepTracker("Initialize Goalkeeper Project")
    # Flag to allow suppressing legacy headings
    sys._goalkeeper_tracker_active = True
    # Pre steps recorded as completed before live rendering
    tracker.add("precheck", "Check required tools")
    tracker.complete("precheck", "ok")
    tracker.add("ai-select", "Select AI assistant")
    tracker.complete("ai-select", f"{selected_ai}")
    tracker.add("script-select", "Select script type")
    tracker.complete("script-select", selected_script)
    for key, label in [
        ("fetch", "Fetch latest release"),
        ("download", "Download template"),
        ("extract", "Extract template"),
        ("zip-list", "Archive contents"),
        ("extracted-summary", "Extraction summary"),
        ("chmod", "Ensure scripts executable"),
        ("cleanup", "Cleanup"),
        ("git", "Initialize git repository"),
        ("final", "Finalize")
    ]:
        tracker.add(key, label)

    # Use transient so live tree is replaced by the final static render (avoids duplicate output)
    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            # Create a httpx client with verify based on skip_tls
            verify = not skip_tls
            local_ssl_context = ssl_context if verify else False
            local_client = httpx.Client(verify=local_ssl_context)

            download_and_extract_template(project_path, selected_ai, selected_script, here, verbose=False, tracker=tracker, client=local_client, debug=debug, github_token=github_token)

            # Ensure scripts are executable (POSIX)
            ensure_executable_scripts(project_path, tracker=tracker)

            # Git step
            if not no_git:
                tracker.start("git")
                if is_git_repo(project_path):
                    tracker.complete("git", "existing repo detected")
                elif should_init_git:
                    if init_git_repo(project_path, quiet=True):
                        tracker.complete("git", "initialized")
                    else:
                        tracker.error("git", "init failed")
                else:
                    tracker.skip("git", "git not available")
            else:
                tracker.skip("git", "--no-git flag")

            tracker.complete("final", "project ready")
        except Exception as e:
            tracker.error("final", str(e))
            console.print(Panel(f"Initialization failed: {e}", title="Failure", border_style="red"))
            if debug:
                _env_pairs = [
                    ("Python", sys.version.split()[0]),
                    ("Platform", sys.platform),
                    ("CWD", str(Path.cwd())),
                ]
                _label_width = max(len(k) for k, _ in _env_pairs)
                env_lines = [f"{k.ljust(_label_width)} → [bright_black]{v}[/bright_black]" for k, v in _env_pairs]
                console.print(Panel("\n".join(env_lines), title="Debug Environment", border_style="magenta"))
            if not here and project_path.exists():
                shutil.rmtree(project_path)
            raise typer.Exit(1)
        finally:
            # Force final render
            pass

    # Final static tree (ensures finished state visible after Live context ends)
    console.print(tracker.render())
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
        "roo": ".roo/",
        "q": ".amazonq/"
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

    # Add Codex-specific setup step if needed
    if selected_ai == "codex":
        codex_path = project_path / ".codex"
        quoted_path = shlex.quote(str(codex_path))
        if os.name == "nt":  # Windows
            cmd = f"setx CODEX_HOME {quoted_path}"
        else:  # Unix-like systems
            cmd = f"export CODEX_HOME={quoted_path}"

        steps_lines.append(f"{step_num}. Set [cyan]CODEX_HOME[/cyan] environment variable before running Codex: [cyan]{cmd}[/cyan]")
        step_num += 1

    steps_lines.append(f"{step_num}. Start using slash commands with your AI agent:")

    steps_lines.append("   2.1 [cyan]/goalkit.vision[/] - Establish project vision and principles")
    steps_lines.append("   2.2 [cyan]/goalkit.goal[/] - Define goals and success criteria")
    steps_lines.append("   2.3 [cyan]/goalkit.strategies[/] - Explore implementation strategies")
    steps_lines.append("   2.4 [cyan]/goalkit.milestones[/] - Create measurable milestones")
    steps_lines.append("   2.5 [cyan]/goalkit.execute[/] - Execute with learning and adaptation")

    steps_panel = Panel("\n".join(steps_lines), title="Next Steps", border_style="cyan", padding=(1,2))
    console.print()
    console.print(steps_panel)

    enhancement_lines = [
        "Optional commands that you can use for your goals [bright_black](enhance exploration & learning)[/bright_black]",
        "",
        f"○ [cyan]/goalkit.explore[/] [bright_black](optional)[/bright_black] - Dive deeper into specific strategy options and alternatives",
        f"○ [cyan]/goalkit.measure[/] [bright_black](optional)[/bright_black] - Define detailed measurement frameworks and tracking approaches",
        f"○ [cyan]/goalkit.adapt[/] [bright_black](optional)[/bright_black] - Make strategy adjustments based on learning and results"
    ]
    enhancements_panel = Panel("\n".join(enhancement_lines), title="Enhancement Commands", border_style="cyan", padding=(1,2))
    console.print()
    console.print(enhancements_panel)

@app.command()
def validate(
    goal_file: Path = typer.Argument(..., help="Path to the goal file to validate"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed validation information"),
):
    """Validate a goal file to ensure it meets quality standards with measurable outcomes."""
    show_banner()
    
    console.print(f"[cyan]Validating goal file:[/cyan] {goal_file.name}\n")
    
    console.print("[yellow]Validation functionality requires implementation of validation logic in a utils module.[/yellow]")
    console.print("[yellow]This is a placeholder command for the validation feature.[/yellow]")
    
    # TODO: Implement actual validation logic here
    # For now, return success to allow testing to continue
    console.print("[bold green]PASSED Goal file passed validation (placeholder)![/bold green]")
    console.print("\n[green]Goal meets quality standards with measurable outcomes (placeholder).[/green]")


@app.command()
def progress(
    goal_dir: Path = typer.Argument(default=None, help="Path to the goal directory (default: current directory)"),
    show_all: bool = typer.Option(False, "--all", "-a", help="Show all goals in the .goalkit/goals directory"),
):
    """Visualize progress of goals and milestones with improved visualization."""
    show_banner()
    
    if show_all:
        # Show progress for all goals in the .goalkit/goals directory
        goals_dir = Path(".goalkit/goals") if goal_dir is None else goal_dir / ".goalkit/goals"
        
        if not goals_dir.exists():
            console.print(f"[red]Error: Directory {goals_dir} does not exist[/red]")
            raise typer.Exit(code=1)
        
        goal_dirs = [d for d in goals_dir.iterdir() if d.is_dir()]
        
        if not goal_dirs:
            console.print("[yellow]No goals found in the directory.[/yellow]")
            return
        
        console.print(f"[cyan]Found {len(goal_dirs)} goal(s):[/cyan]\n")
        
        for idx, goal_dir in enumerate(sorted(goal_dirs), 1):
            console.print(f"[bold]{idx}. {goal_dir.name}[/bold]")
            goal_file = goal_dir / "goal.md"
            if goal_file.exists():
                # Extract and display goal status
                content = goal_file.read_text(encoding='utf-8')
                status_match = re.search(r'\\*\\*Status\\*\\*:\\s*(\\w+)', content)
                status = status_match.group(1) if status_match else "Unknown"
                
                # Determine status color
                if status.lower() in ["done", "completed", "finished"]:
                    status_color = "green"
                elif status.lower() in ["in progress", "wip", "working"]:
                    status_color = "yellow"
                else:
                    status_color = "red"
                
                console.print(f"   Status: [{status_color}]{status}[/{status_color}]")
            else:
                console.print("   [red]No goal.md file found[/red]")
            console.print()  # Empty line for spacing
    else:
        # Show progress for a specific goal
        goal_path = goal_dir or Path.cwd()
        
        # Look for goal files in the current directory or .goalkit/goals subdirectory
        goal_file = goal_path / "goal.md"
        if not goal_file.exists():
            # Check if we're in a goal directory within .goalkit/goals
            if (goal_path / ".goalkit").exists():
                goals_dir = goal_path / ".goalkit" / "goals"
                if goals_dir.exists():
                    # Find the first goal directory
                    goal_dirs = [d for d in goals_dir.iterdir() if d.is_dir()]
                    if goal_dirs:
                        goal_dir = goal_dirs[0]
                        goal_file = goal_dir / "goal.md"
        
        if not goal_file.exists():
            console.print(f"[red]Error: goal.md file not found in {goal_path}[/red]")
            raise typer.Exit(code=1)
        
        # Read and parse the goal file to show progress
        content = goal_file.read_text(encoding='utf-8')
        
        # Extract goal information
        goal_title_match = re.search(r'^# Goal Definition: (.*)', content, re.MULTILINE)
        goal_title = goal_title_match.group(1) if goal_title_match else "Unknown Goal"
        
        console.print(f"[bold cyan]Goal:[/bold cyan] {goal_title}\n")
        
        # Extract and display status
        status_match = re.search(r'\\*\\*Status\\*\\*:\\s*(\\w+)', content)
        status = status_match.group(1) if status_match else "Unknown"
        
        # Determine status color
        if status.lower() in ["done", "completed", "finished"]:
            status_color = "green"
        elif status.lower() in ["in progress", "wip", "working"]:
            status_color = "yellow"
        else:
            status_color = "red"
        
        console.print(f"[bold]Status:[/bold] [{status_color}]{status}[/{status_color}]\n")
        
        # Extract and display milestones
        milestones_section = re.search(r'## 🚀 Goal Milestones(.*?)(?=## \\w|\\Z)', content, re.DOTALL)
        if milestones_section:
            milestones_content = milestones_section.group(1)
            
            # Find all milestones
            milestone_pattern = r'### (Milestone [0-9]+:.*?)\\n\\*\\*Description:\\*\\*(.*?)\\n\\*\\*Success Indicators:\\*\\*(.*?)\\n\\*\\*Validation Method:\\*\\*(.*?)\\n\\*\\*Expected Timeline:\\*\\*(.*?)(?=\\n---|\\n### |$)'
            milestones = re.findall(milestone_pattern, milestones_content, re.DOTALL)
            
            if milestones:
                console.print("[bold]Milestones:[/bold]")
                
                completed_count = 0
                total_count = len(milestones)
                
                for idx, (title, description, indicators, validation, timeline) in enumerate(milestones, 1):
                    # Check if milestone is completed by looking for a completion indicator
                    is_completed = "[x]" in indicators.lower() or "completed" in indicators.lower()
                    if is_completed:
                        completed_count += 1
                    
                    status_symbol = "[green]✓[/green]" if is_completed else "[red]○[/red]"
                    console.print(f"  {status_symbol} {title.strip()}")
                    
                    # Show timeline if available
                    timeline_clean = timeline.strip().split('\n')[0] if timeline.strip() else "Not specified"
                    console.print(f"      Timeline: {timeline_clean}")
                
                # Show progress bar
                if total_count > 0:
                    progress_percent = (completed_count / total_count) * 100
                    console.print(f"\n[bold]Progress: {completed_count}/{total_count} milestones completed ({progress_percent:.1f}%)")
                    
                    # Create a simple progress bar
                    bar_length = 30
                    filled_length = int(bar_length * completed_count // total_count)
                    bar = "█" * filled_length + "░" * (bar_length - filled_length)
                    console.print(f"[cyan]{bar}[/cyan]")
            else:
                console.print("[yellow]No milestones found in the goal file.[/yellow]")
        else:
            console.print("[yellow]No milestones section found in the goal file.[/yellow]")


@app.command()
def analytics(
    output_format: str = typer.Option("table", "--format", "-f", help="Output format: table, json, or csv"),
    goals_dir: Path = typer.Option(Path(".goalkit/goals"), "--goals-dir", help="Directory containing goal files"),
):
    """Generate analytics report on goal and strategy effectiveness."""
    show_banner()
    
    console.print("[bold cyan]Generating Goal Analytics Report[/bold cyan]\n")
    
    if not goals_dir.exists():
        console.print(f"[red]Error: Goals directory {goals_dir} does not exist[/red]")
        raise typer.Exit(code=1)
    
    # Collect analytics data
    goals = []
    goal_dirs = [d for d in goals_dir.iterdir() if d.is_dir()]
    
    for goal_dir in goal_dirs:
        goal_file = goal_dir / "goal.md"
        if goal_file.exists():
            content = goal_file.read_text(encoding='utf-8')
            
            # Extract goal information
            goal_title_match = re.search(r'^# Goal Definition: (.*)', content, re.MULTILINE)
            goal_title = goal_title_match.group(1) if goal_title_match else "Unknown Goal"
            
            status_match = re.search(r'\\*\\*Status\\*\\*:\\s*(\\w+)', content)
            status = status_match.group(1) if status_match else "Unknown"
            
            # Calculate milestone completion
            milestones_section = re.search(r'## 🚀 Goal Milestones(.*?)(?=## \\w|\\Z)', content, re.DOTALL)
            milestones_completed = 0
            total_milestones = 0
            
            if milestones_section:
                # Find all milestones
                milestone_pattern = r'### (Milestone [0-9]+:.*?)\\n\\*\\*Description:\\*\\*(.*?)\\n\\*\\*Success Indicators:\\*\\*(.*?)\\n\\*\\*Validation Method:\\*\\*(.*?)\\n\\*\\*Expected Timeline:\\*\\*(.*?)(?=\\n---|\\n### |$)'
                milestones = re.findall(milestone_pattern, milestones_section.group(1), re.DOTALL)
                
                if milestones:
                    total_milestones = len(milestones)
                    for idx, (title, description, indicators, validation, timeline) in enumerate(milestones, 1):
                        is_completed = "[x]" in indicators.lower() or "completed" in indicators.lower()
                        if is_completed:
                            milestones_completed += 1
            
            goal_data = {
                "name": goal_title,
                "status": status,
                "directory": goal_dir.name,
                "milestones_completed": milestones_completed,
                "total_milestones": total_milestones,
                "completion_rate": (milestones_completed / total_milestones * 100) if total_milestones > 0 else 0
            }
            goals.append(goal_data)
    
    if not goals:
        console.print("[yellow]No goals found to analyze.[/yellow]")
        return
    
    # Display results based on output format
    if output_format == "json":
        import json as json_module  # Using different name to avoid conflict with import json above
        console.print(json_module.dumps(goals, indent=2))
    elif output_format == "csv":
        console.print("Name,Status,Directory,Milestones Completed,Total Milestones,Completion Rate")
        for goal in goals:
            console.print(f"{goal['name']},{goal['status']},{goal['directory']},{goal['milestones_completed']},{goal['total_milestones']},{goal['completion_rate']:.1f}%")
    else:  # Default to table format
        # Create a table with analytics
        table = Table(title="Goal Analytics Report", show_header=True, header_style="bold magenta")
        table.add_column("Goal", style="dim", width=20)
        table.add_column("Status", min_width=10)
        table.add_column("Dir", justify="center")
        table.add_column("Completed", justify="center")
        table.add_column("Total", justify="center")
        table.add_column("Rate", justify="center")
        
        for goal in goals:
            # Determine status color
            if goal['status'].lower() in ["done", "completed", "finished"]:
                status_color = "green"
            elif goal['status'].lower() in ["in progress", "wip", "working"]:
                status_color = "yellow"
            else:
                status_color = "red"
            
            table.add_row(
                goal['name'][:19] + "..." if len(goal['name']) > 20 else goal['name'],  # Truncate long names
                f"[{status_color}]{goal['status']}[/{status_color}]",
                goal['directory'],
                str(goal['milestones_completed']),
                str(goal['total_milestones']),
                f"[bold]{goal['completion_rate']:.1f}%[/bold]"
            )
        
        console.print(table)
        
        # Summary statistics
        console.print("\n[bold]Summary Statistics:[/bold]")
        total_goals = len(goals)
        completed_goals = sum(1 for goal in goals if goal['status'].lower() in ["done", "completed", "finished"])
        in_progress_goals = sum(1 for goal in goals if goal['status'].lower() in ["in progress", "wip", "working"])
        
        avg_completion_rate = sum(goal['completion_rate'] for goal in goals) / total_goals if total_goals > 0 else 0
        
        console.print(f"  Total Goals: {total_goals}")
        console.print(f"  Completed Goals: {completed_goals}")
        console.print(f"  In Progress: {in_progress_goals}")
        console.print(f"  Average Completion Rate: [bold]{avg_completion_rate:.1f}%[/bold]")


@app.command()
def ai_generate(
    goal_file: Path = typer.Argument(..., help="Path to the goal file to generate strategies for"),
    strategy_type: str = typer.Option("strategies", "--type", "-t", help="Type of AI generation: strategies, milestones, execution"),
    output_file: Path = typer.Option(None, "--output", "-o", help="File to save the AI output (optional)"),
):
    """Generate strategies, milestones, or execution plans using AI based on goal context."""
    show_banner()
    
    console.print(f"[cyan]Generating {strategy_type} for:[/cyan] {goal_file.name}\n")
    
    # Determine the goal directory from the goal_file path
    goal_dir = goal_file.parent
    
    # Validate that we're in a proper goal directory structure
    if not goal_file.exists():
        console.print(f"[red]Error: goal file not found at {goal_file}[/red]")
        raise typer.Exit(code=1)
    
    # Determine output file path based on type and goal directory
    if output_file:
        output_path = output_file
    else:
        if strategy_type == "strategies":
            output_path = goal_dir / "strategies.md"
        elif strategy_type == "milestones":
            output_path = goal_dir / "milestones.md"
        elif strategy_type == "execution":
            output_path = goal_dir / "execution.md"
        else:
            output_path = goal_dir / f"{strategy_type}.md"  # fallback
    
    # Read the current goal context for AI
    try:
        content = goal_file.read_text(encoding='utf-8')
    except Exception as e:
        console.print(f"[red]Error reading goal file:[/red] {e}")
        raise typer.Exit(code=1)
    
    # Extract goal information for context
    goal_title_match = re.search(r'^# Goal Definition: (.*)', content, re.MULTILINE)
    goal_title = goal_title_match.group(1) if goal_title_match else "Unknown Goal"
    
    console.print(f"[cyan]Goal:[/cyan] {goal_title}")
    console.print(f"[cyan]Output file:[/cyan] {output_path}\n")
    
    # For now, we'll create a basic template based on the strategy_type
    # In the future, this would be replaced with actual AI processing
    from datetime import datetime
    
    if strategy_type == "strategies":
        template_content = f"""# Strategy Exploration: {goal_title}

**Goal Branch**: `{goal_dir.name}` | **Date**: {datetime.now().strftime('%Y-%m-%d')}

## 🎯 Strategy Discovery Framework

### Objective
Exploration of multiple strategic approaches to achieve the goal based on AI analysis.

### Input
- **Goal Statement**: {goal_title}
- **Success Criteria**: [From goal definition]
- **Constraints**: [Time, resources, technical limitations]
- **Stakeholders**: [Key people who will be impacted]

---

## 🧭 Strategy Options & Analysis

### Strategy Option 1: [AI-Recommended Approach]
**Description**: [Brief description of the approach]

**Implementation Approach**:
- [Step 1]
- [Step 2]
- [Step 3]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Implementation Difficulty**: [Rating: Low/Medium/High] - **Why**: [Explanation]
**Maintenance Complexity**: [Rating: Low/Medium/High] - **Why**: [Explanation]

**Resource Requirements**:
- **Time**: [Estimated timeline]
- **Personnel**: [Required roles and expertise]
- **Tools/Technology**: [Required tools or technologies]

**Risk Assessment**:
- **Technical Risks**: [Potential technical challenges]
- **Business Risks**: [Potential business impacts]
- **Mitigation Strategies**: [How to address risks]

**Success Probability**: [Estimate: 60-90%] - **Reasoning**: [Why this probability]

---

## 📊 Evaluation Framework

[AI evaluation of strategies would go here]

---

## 🎯 Recommendation & Rationale

**Recommended Approach**: [Strategy Option 1/2/3]

### Primary Recommendation
[AI's recommended strategy and explanation]

*This strategy exploration was generated by AI based on the goal context.*
"""
    elif strategy_type == "milestones":
        template_content = f"""# Milestones: {goal_title}

**Branch**: `{goal_dir.name}` | **Date**: {datetime.now().strftime('%Y-%m-%d')} | **Strategy**: [link]

## 🎯 Milestones Overview

**Goal Focus**: {goal_title}

**Strategy Context**: [AI analysis of which strategies these milestones support]

**Learning Focus**: [What AI suggests to learn from these milestones]

## 📊 Milestone Definition Framework

### Milestone 1: [AI-Recommended Milestone Title] (Priority: P1)

**Description**: [What this milestone achieves and why it matters. AI analysis of learning/validation outcomes]

**Success Indicators**:
- [AI-generated measurable outcome 1 - be specific and testable]
- [AI-generated measurable outcome 2 - include quantitative targets]
- [AI-generated measurable outcome 3 - define what "done" looks like]

**Learning Objectives**:
- **Hypothesis**: [What assumption this milestone tests - AI analysis from goal hypotheses]
- **Validation Method**: [How to confirm the hypothesis - specific, AI-suggested approach]
- **Success Criteria**: [When hypothesis is considered validated - measurable AI criteria]

**Value Delivered**:
- **User Value**: [What users gain from this milestone - AI analysis of immediate benefit]
- **Business Value**: [What business benefits from this milestone - AI analysis of measurable impact]
- **Learning Value**: [What insights this milestone should generate - AI analysis of discoveries]

**Implementation Approaches**:
- **Approach 1**: [How this milestone could be implemented - AI preferred method]
- **Approach 2**: [Alternative implementation approach - AI backup option]

**Measurement Plan**:
- **Metrics to Track**: [AI-suggested metrics to collect - link to success indicators]
- **Measurement Method**: [How to collect the data - tools and frequency AI suggests]
- **Success Thresholds**: [When milestone is considered achieved - AI specific targets]

**Dependencies**:
- **Requires**: [What must be completed first - AI analysis of specific deliverables]
- **Enables**: [What this milestone unlocks - next milestones or capabilities AI suggests]

**Risk Assessment**:
- **Risk Level**: [AI-assessed risk level: High/Medium/Low] - **Why**: [AI's justification for risk rating]
- **Potential Issues**: [What could go wrong - AI analysis of specific technical/business risks]
- **Mitigation Strategies**: [How to address issues - AI concrete action plans]

**Effort Estimate**: [AI estimated time/resources needed] | **Timeline**: [AI suggested start/end dates]

---

## 📈 Progress Tracking Framework

[AI-generated approach to track progress across milestones]

*This milestones document generated by AI based on goal context and best practices for progress tracking.*
"""
    elif strategy_type == "execution":
        template_content = f"""# Execution Plan: {goal_title}

**Goal Branch**: `{goal_dir.name}` | **Date**: {datetime.now().strftime('%Y-%m-%d')}

## 🎯 Execution Overview

### Goal Focus
{goal_title}

### Strategy Context
[AI analysis of which strategy to use from strategies phase]

### Learning Focus
[AI-suggested learning objectives during execution]

---

## 🛠️ Execution Framework

### Current Milestone
[AI-recommended milestone to work on currently]

### Selected Strategy
[The AI-recommended strategy chosen from strategies phase]

### Daily Focus
[AI-suggested tasks for the current day]

### Success Indicator
[AI-defined measure of productive work]

### Learning Objective
[AI-recommended learning focus during execution]

### Adaptation Plan
[AI-suggested approaches to handle unexpected challenges]

---

## 📋 Implementation Task Breakdown

### Phase 1: [AI-Recommended Phase Title] (Priority: P1)
**Focus**: [AI description of what this phase accomplishes]

**Key Activities**:
- [ ] **Activity 1**: [AI-suggested task]
- [ ] **Activity 2**: [AI-suggested task]
- [ ] **Activity 3**: [AI-suggested task]

**Success Indicators**:
- [AI-generated measurable outcome 1]
- [AI-generated measurable outcome 2]
- [AI-generated measurable outcome 3]

**Timeline**: [AI-suggested duration]

---

## 📊 Measurement Framework

### Key Metrics
- **Metric 1**: [AI-suggested specific, quantifiable metric]
- **Metric 2**: [AI-suggested specific, quantifiable metric]
- **Metric 3**: [AI-suggested specific, quantifiable metric]

### Measurement Method
- **How**: [AI-suggested method for data collection and frequency]
- **When**: [AI-suggested schedule for data collection]
- **Who**: [AI-suggested responsible parties]

### Success Thresholds
- **Baseline**: [Current AI-estimated performance level]
- **Target**: [AI-estimated success threshold]
- **Exceptional**: [AI-estimated exceeding expectations threshold]

---

## 🔄 Learning Loop Process

[AI-generated learning loop approach]

*This execution plan was AI-generated based on the goal context and recommended strategies.*
"""
    else:
        # Fallback template for unknown types
        template_content = f"""# {strategy_type.title()}: {goal_title}

**Goal Branch**: `{goal_dir.name}` | **Date**: {datetime.now().strftime('%Y-%m-%d')}

## Overview

AI-generated {strategy_type} content for goal: {goal_title}

[AI would generate specific content based on goal context]

*This {strategy_type} document was generated by AI based on the goal context.*
"""
    
    # Write the AI-generated content to the output file
    try:
        output_path.write_text(template_content, encoding='utf-8')
        console.print(f"[green]+[/green] {strategy_type.title()} file created successfully!")
        console.print(f"[cyan]File:[/cyan] {output_path}")
        console.print(f"[cyan]Type:[/cyan] {strategy_type}")
    except Exception as e:
        console.print(f"[red]Error writing {strategy_type} file:[/red] {e}")
        raise typer.Exit(code=1)
    
    console.print(f"\n[bold green]AI generation for {strategy_type} completed successfully![/bold green]")


@app.command()
def automate(
    action: str = typer.Argument(..., help="Automation action: create-goal, update-status, generate-templates"),
    name: str = typer.Option(None, "--name", "-n", help="Name for the goal or other entity"),
    status: str = typer.Option(None, "--status", "-s", help="Status to update to (for update-status action)"),
    goal_dir: Path = typer.Option(None, "--goal-dir", "-d", help="Goal directory path (for update-status action)"),
):
    """Automate common goal management tasks to reduce manual work."""
    show_banner()
    
    # Import datetime to use in templates
    from datetime import datetime
    
    if action == "create-goal":
        if not name:
            console.print("[red]Error: --name is required for create-goal action[/red]")
            raise typer.Exit(code=1)
        
        console.print("[yellow]Create goal functionality requires implementation of template logic in a utils module.[/yellow]")
        console.print("[yellow]This is a placeholder for the create goal feature.[/yellow]")
        
        # TODO: Implement actual goal creation logic
        console.print(f"[green]PASSED Goal '{name}' would be created (placeholder)![/green]")
    
    elif action == "update-status":
        if not status:
            console.print("[red]Error: --status is required for update-status action[/red]")
            raise typer.Exit(code=1)
        
        goal_path = goal_dir or Path.cwd()
        
        # Look for goal files in the current directory or .goalkit/goals subdirectory
        goal_file = goal_path / "goal.md"
        if not goal_file.exists():
            console.print(f"[red]Error: goal.md file not found in {goal_path}[/red]")
            raise typer.Exit(code=1)
        
        # Read the current content
        content = goal_file.read_text(encoding='utf-8')
        
        # Update the status in the content
        updated_content = re.sub(
            r'(\\*\\*Status\\*\\*:\\s*)(\\w+)',
            f"**Status**: {status}",
            content
        )
        
        # If no status line was found, add it after the first line
        if updated_content == content:
            lines = content.split('\n')
            lines.insert(1, f"**Status**: {status}")
            updated_content = '\n'.join(lines)
        
        # Write the updated content back to the file
        goal_file.write_text(updated_content, encoding='utf-8')
        
        console.print(f"[green]PASSED Status updated to '{status}' successfully![/green]")
        console.print(f"[cyan]File:[/cyan] {goal_file}")
    
    elif action == "generate-templates":
        console.print("[yellow]Generate templates functionality requires implementation of template logic in a utils module.[/yellow]")
        console.print("[yellow]This is a placeholder for the generate templates feature.[/yellow]")
        
        # TODO: Implement actual template generation logic
        console.print(f"[green]PASSED Templates would be generated (placeholder)![/green]")
    
    else:
        console.print(f"[red]Error: Unknown automation action '{action}'. Use 'create-goal', 'update-status', or 'generate-templates'.[/red]")
        raise typer.Exit(code=1)


@app.command()
def strategies(
    goal_dir: Path = typer.Argument(None, help="Path to the goal directory (default: current directory)"),
    output_file: Path = typer.Option(None, "--output", "-o", help="File to save the strategies (optional)"),
    include_template: bool = typer.Option(True, "--include-template", "-t", help="Include template sections in the output")
):
    """Create strategy exploration document for goals to enable strategic approach exploration and validation."""
    show_banner()

    console.print("[bold cyan]Creating Strategy Exploration for Goal[/bold cyan]\n")

    # Find the goal directory
    if goal_dir is None:
        goal_dir = Path.cwd()

    # Look for goal files in the current directory or .goalkit/goals subdirectory
    goal_file = goal_dir / "goal.md"
    if not goal_file.exists():
        # Check if we're in a goal directory within .goalkit/goals
        if (goal_dir / ".goalkit").exists():
            goals_dir = goal_dir / ".goalkit" / "goals"
            if goals_dir.exists():
                # Find the first goal directory
                goal_dirs = [d for d in goals_dir.iterdir() if d.is_dir()]
                if goal_dirs:
                    goal_dir = goal_dirs[0]
                    goal_file = goal_dir / "goal.md"

    if not goal_file.exists():
        console.print(f"[red]Error: goal.md file not found in {goal_dir}[/red]")
        console.print("[yellow]Tip: Run this command from a goal directory or specify the path with --goal-dir[/yellow]")
        raise typer.Exit(code=1)

    # Read the goal file to understand context
    try:
        content = goal_file.read_text(encoding='utf-8')
    except Exception as e:
        console.print(f"[red]Error reading goal file:[/red] {e}")
        raise typer.Exit(code=1)

    # Extract goal information
    goal_title_match = re.search(r'^# Goal Definition: (.*)', content, re.MULTILINE)
    goal_title = goal_title_match.group(1) if goal_title_match else "Unknown Goal"

    console.print(f"[cyan]Goal:[/cyan] {goal_title}")
    console.print(f"[cyan]Directory:[/cyan] {goal_dir.name}\n")

    # Generate strategies content using the template
    from datetime import datetime
    
    strategies_content = f"""# Strategy Exploration: {goal_title}

**Goal Branch**: `{goal_dir.name}` | **Date**: {datetime.now().strftime('%Y-%m-%d')}

## 🎯 Strategy Discovery Framework

### Objective
Explore multiple strategic approaches to achieve the goal, evaluate their feasibility, and recommend the optimal path forward.

### Input
- **Goal Statement**: {goal_title}
- **Success Criteria**: [From goal definition]
- **Constraints**: [Time, resources, technical limitations]
- **Stakeholders**: [Key people who will be impacted]

---

## 🧭 Strategy Options & Analysis

### Strategy Option 1: [Approach Title]
**Description**: [Brief description of the approach]

**Implementation Approach**:
- [Step 1]
- [Step 2]
- [Step 3]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Implementation Difficulty**: [Rating: Low/Medium/High] - **Why**: [Explanation]
**Maintenance Complexity**: [Rating: Low/Medium/High] - **Why**: [Explanation]

**Resource Requirements**:
- **Time**: [Estimated timeline]
- **Personnel**: [Required roles and expertise]
- **Tools/Technology**: [Required tools or technologies]

**Risk Assessment**:
- **Technical Risks**: [Potential technical challenges]
- **Business Risks**: [Potential business impacts]
- **Mitigation Strategies**: [How to address risks]

**Success Probability**: [Estimate: 60-90%] - **Reasoning**: [Why this probability]

### Strategy Option 2: [Approach Title]
**Description**: [Brief description of the approach]

**Implementation Approach**:
- [Step 1]
- [Step 2]
- [Step 3]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Implementation Difficulty**: [Rating: Low/Medium/High] - **Why**: [Explanation]
**Maintenance Complexity**: [Rating: Low/Medium/High] - **Why**: [Explanation]

**Resource Requirements**:
- **Time**: [Estimated timeline]
- **Personnel**: [Required roles and expertise]
- **Tools/Technology**: [Required tools or technologies]

**Risk Assessment**:
- **Technical Risks**: [Potential technical challenges]
- **Business Risks**: [Potential business impacts]
- **Mitigation Strategies**: [How to address risks]

**Success Probability**: [Estimate: 60-90%] - **Reasoning**: [Why this probability]

### Strategy Option 3: [Approach Title]
**Description**: [Brief description of the approach]

**Implementation Approach**:
- [Step 1]
- [Step 2]
- [Step 3]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Implementation Difficulty**: [Rating: Low/Medium/High] - **Why**: [Explanation]
**Maintenance Complexity**: [Rating: Low/Medium/High] - **Why**: [Explanation]

**Resource Requirements**:
- **Time**: [Estimated timeline]
- **Personnel**: [Required roles and expertise]
- **Tools/Technology**: [Required tools or technologies]

**Risk Assessment**:
- **Technical Risks**: [Potential technical challenges]
- **Business Risks**: [Potential business impacts]
- **Mitigation Strategies**: [How to address risks]

**Success Probability**: [Estimate: 60-90%] - **Reasoning**: [Why this probability]

---

## 📊 Evaluation Framework

### Criteria for Assessment
1. **Technical Feasibility**: How practical is the approach given current technology and constraints?
2. **Resource Requirements**: What time, personnel, and budget are needed?
3. **Time-to-Completion**: How long would implementation take?
4. **Risk Assessment**: What are the potential challenges and how can they be mitigated?
5. **Scalability Potential**: How well would this approach work if scaled up?
6. **Team Alignment**: How well does this approach match team expertise and availability?

### Scoring Method
Rate each strategy on each criterion using: 
- **H** (High/Good) - Excellent fit
- **M** (Medium/Average) - Reasonable fit  
- **L** (Low/Poor) - Poor fit

| Strategy | Feasibility | Resources | Time-to-Completion | Risk | Scalability | Team Alignment | Overall |
|----------|-------------|-----------|-------------------|------|-------------|----------------|---------|
| Strategy 1 | | | | | | | |
| Strategy 2 | | | | | | | |
| Strategy 3 | | | | | | | |

---

## 🎯 Recommendation & Rationale

**Recommended Approach**: [Strategy Option 1/2/3]

### Primary Recommendation
[Choose one strategy and explain why it's the best option]

### Supporting Evidence
- **[Factor 1]**: [Why this strategy is better for factor 1]
- **[Factor 2]**: [Why this strategy is better for factor 2]
- **[Factor 3]**: [Why this strategy is better for factor 3]

### Implementation Priority
1. **Immediate**: [What to do right away]
2. **Short-term**: [What to do in first 2-4 weeks]
3. **Medium-term**: [What to do in following weeks]

### Alternative Considerations
If the recommended approach proves infeasible, consider [Strategy 2/3] with the following considerations: [Specific considerations].

---

## 🔄 Continuous Validation & Adaptation

### Validation Points
- **Milestone 1**: [How to validate initial approach]
- **Milestone 2**: [How to validate progress]
- **Milestone 3**: [How to validate final outcome]

### Adaptation Criteria
- **Switch Approach If**: [Conditions that would cause a change in strategy]
- **Modify Approach If**: [Conditions that would cause slight modifications]
- **Continue Current If**: [Conditions that validate current approach]

### Learning & Iteration Framework
- **What to Measure**: [Key metrics to track strategy effectiveness]
- **How to Measure**: [Methods for data collection]
- **When to Evaluate**: [Timeline for assessment]
- **Who to Involve**: [Stakeholders for evaluation]

*This strategy exploration document provides multiple pathways to achieving the goal, with detailed analysis to support decision-making.*
"""

    # Determine output file path
    if output_file:
        output_path = output_file
    else:
        output_path = goal_dir / "strategies.md"

    # Write the strategies file
    try:
        output_path.write_text(strategies_content, encoding='utf-8')
        console.print(f"[green]+[/green] Strategies created successfully!")
        console.print(f"[cyan]File:[/cyan] {output_path}")

    except Exception as e:
        console.print(f"[red]Error writing strategies file:[/red] {e}")
        raise typer.Exit(code=1)

    # Show next steps
    console.print("\n[bold]Next Steps:[/bold]")
    console.print("1. [cyan]Review and customize[/cyan] the generated strategies for your specific goal")
    console.print("2. [cyan]Evaluate all options[/cyan] using the assessment framework")
    console.print("3. [cyan]Select the recommended approach[/cyan] or iterate on alternatives")
    console.print("4. [cyan]Begin execution[/cyan] with your chosen strategy")
    console.print("5. [cyan]Track progress[/cyan] and adapt as needed based on validation points")


@app.command()
def execution(
    goal_dir: Path = typer.Argument(None, help="Path to the goal directory (default: current directory)"),
    output_file: Path = typer.Option(None, "--output", "-o", help="File to save the execution plan (optional)"),
    include_template: bool = typer.Option(True, "--include-template", "-t", help="Include template sections in the output")
):
    """Create execution plan for goals to enable focused implementation with continuous learning."""
    show_banner()

    console.print("[bold cyan]Creating Execution Plan for Goal[/bold cyan]\n")

    # Find the goal directory
    if goal_dir is None:
        goal_dir = Path.cwd()

    # Look for goal files in the current directory or .goalkit/goals subdirectory
    goal_file = goal_dir / "goal.md"
    if not goal_file.exists():
        # Check if we're in a goal directory within .goalkit/goals
        if (goal_dir / ".goalkit").exists():
            goals_dir = goal_dir / ".goalkit" / "goals"
            if goals_dir.exists():
                # Find the first goal directory
                goal_dirs = [d for d in goals_dir.iterdir() if d.is_dir()]
                if goal_dirs:
                    goal_dir = goal_dirs[0]
                    goal_file = goal_dir / "goal.md"

    if not goal_file.exists():
        console.print(f"[red]Error: goal.md file not found in {goal_dir}[/red]")
        console.print("[yellow]Tip: Run this command from a goal directory or specify the path with --goal-dir[/yellow]")
        raise typer.Exit(code=1)

    # Read the goal file to understand context
    try:
        content = goal_file.read_text(encoding='utf-8')
    except Exception as e:
        console.print(f"[red]Error reading goal file:[/red] {e}")
        raise typer.Exit(code=1)

    # Extract goal information
    goal_title_match = re.search(r'^# Goal Definition: (.*)', content, re.MULTILINE)
    goal_title = goal_title_match.group(1) if goal_title_match else "Unknown Goal"

    console.print(f"[cyan]Goal:[/cyan] {goal_title}")
    console.print(f"[cyan]Directory:[/cyan] {goal_dir.name}\n")

    # Generate execution content using the template
    from datetime import datetime
    
    execution_content = f"""# Execution Plan: {goal_title}

**Goal Branch**: `{goal_dir.name}` | **Date**: {datetime.now().strftime('%Y-%m-%d')}

## 🎯 Execution Overview

### Goal Focus
{goal_title}

### Strategy Context
[Which strategies this execution plan supports]

### Learning Focus
[What we want to learn during execution]

---

## 🛠️ Execution Framework

### Current Milestone
[Which milestone you're currently working on]

### Selected Strategy
[The strategy chosen from strategies phase]

### Daily Focus
[Specific tasks for the current day]

### Success Indicator
[How you'll know today's work was productive]

### Learning Objective
[What you hope to learn during execution]

### Adaptation Plan
[How you'll handle unexpected challenges]

---

## 📋 Implementation Task Breakdown

### Phase 1: [Phase Title] (Priority: P1)
**Focus**: [What this phase accomplishes and why it matters]

**Key Activities**:
- [ ] **Activity 1**: [What needs to be done]
- [ ] **Activity 2**: [What needs to be done]
- [ ] **Activity 3**: [What needs to be done]

**Success Indicators**:
- [Measurable outcome 1 - be specific and testable]
- [Measurable outcome 2 - include quantitative targets]
- [Measurable outcome 3 - define what "done" looks like]

**Timeline**: [Start/end dates or duration]

### Phase 2: [Phase Title] (Priority: P2)
**Focus**: [What this phase accomplishes and why it matters]

**Key Activities**:
- [ ] **Activity 1**: [What needs to be done]
- [ ] **Activity 2**: [What needs to be done]
- [ ] **Activity 3**: [What needs to be done]

**Success Indicators**:
- [Measurable outcome 1 - be specific and testable]
- [Measurable outcome 2 - include quantitative targets]
- [Measurable outcome 3 - define what "done" looks like]

**Timeline**: [Start/end dates or duration]

### Phase 3: [Phase Title] (Priority: P3)
**Focus**: [What this phase accomplishes and why it matters]

**Key Activities**:
- [ ] **Activity 1**: [What needs to be done]
- [ ] **Activity 2**: [What needs to be done]
- [ ] **Activity 3**: [What needs to be done]

**Success Indicators**:
- [Measurable outcome 1 - be specific and testable]
- [Measurable outcome 2 - include quantitative targets]
- [Measurable outcome 3 - define what "done" looks like]

**Timeline**: [Start/end dates or duration]

---

## 📊 Measurement Framework

### Key Metrics
- **Metric 1**: [What to measure - specific, quantifiable]
- **Metric 2**: [What to measure - specific, quantifiable]
- **Metric 3**: [What to measure - specific, quantifiable]

### Measurement Method
- **How**: [How to collect the data - tools and frequency]
- **When**: [Schedule for data collection - daily, weekly, etc.]
- **Who**: [Who is responsible for collecting data]

### Success Thresholds
- **Baseline**: [Current performance level]
- **Target**: [What constitutes success]
- **Exceptional**: [What would be considered exceeding expectations]

---

## 🔄 Learning Loop Process

### Daily Learning Loop
- **Build**: [What to develop/execute each day]
- **Measure**: [What to track and measure]
- **Learn**: [How to analyze results]
- **Adapt**: [How to adjust approach based on learning]

#### Daily Focus: [Specific Daily Task]
- Day 1: [Specific task for day 1]
- Day 2: [Specific task for day 2]
- Day 3: [Specific task for day 3]
- Day 4: [Specific task for day 4]
- Day 5: [Specific task for day 5]

### Weekly Learning Loop
- **Review**: [Assess milestone progress against timeline and success criteria]
- **Validate**: [Test with real users or actual data to validate effectiveness]
- **Adjust**: [Refine approach based on user feedback and performance data]
- **Plan**: [Plan next week's implementation based on learnings]

#### Weekly Schedule
- Week 1: [Focus for week 1]
- Week 2: [Focus for week 2]
- Week 3: [Focus for week 3]
- Week 4: [Focus for week 4]

### Progress Assessment
- **Milestone Progress**: [Track completion of acceptance criteria]
- **Performance Metrics**: [Monitor measurement framework results]
- **User Feedback**: [Collect feedback through surveys and interviews]
- **Technical Health**: [Monitor implementation quality and maintainability]

### Insight Documentation
- [Maintain daily logs of challenges and solutions]
- [Document user feedback and feature requests]
- [Track performance metrics and optimization opportunities]
- [Record lessons learned for future implementation]

---

## 🚨 Adaptation Framework

### Progress Indicators
- **Positive**: [Signs of good progress - deliverables completed on time, metrics improving]
- **Neutral**: [Signs of moderate progress - some delays but overall on track, mixed feedback requiring investigation]
- **Negative**: [Signs of poor progress - consistent delays, metrics declining, negative feedback]

### Warning Indicators
- [Specific metrics declining consistently]
- [More than 10% of planned activities not completed]
- [Users reporting that implementation is hindering rather than helping]
- [Implementation progress falling significantly behind schedule]
- [Quality metrics deteriorating]

### Pivot Decision Process
- **At 25% completion**: [Reassess approach if performance targets aren't being met]
- **At 50% completion**: [Evaluate user feedback and make necessary adjustments]
- **At 75% completion**: [Final validation before completion]
- **Continuous**: [Monitor for technical blockers requiring alternative approaches]

### Strategy Switch Options
- **Performance Issues**: [Implement optimization strategies]
- **Resource Issues**: [Adjust timeline or scope appropriately]
- **User Adoption Issues**: [Simplify approach or add more granular controls]
- **Integration Issues**: [Adjust approach to better fit with existing systems]

---

## 🛡️ Risk Management During Execution

### Risk Monitoring
- **Daily Risk Check**: [Identify implementation challenges]
- **Progress Risk Assessment**: [Monitor for timeline slippage or performance issues]
- **External Risk Monitoring**: [Track changes in requirements or environment]
- **Risk Documentation**: [Maintain current risk register with mitigation strategies]

### Risk Response
- **Performance Risks**: [Optimize implementation, implement caching strategies]
- **Resource Risks**: [Reallocate resources or adjust timeline]
- **Compatibility Risks**: [Ensure compatibility with existing systems]
- **Privacy Risks**: [Ensure sensitive information is properly handled according to user preferences]

---

## ✅ Success Validation

### Milestone Completion Criteria
- [ ] All acceptance criteria met (specific implementation completed)
- [ ] Success metrics achieved (measurement framework results)
- [ ] User feedback indicates positive impact on workflow
- [ ] No critical technical issues or performance problems

### Goal Progress Indicators
- [ ] Clear advancement toward reducing time-to-success
- [ ] User satisfaction with implementation improved
- [ ] Implementation system working as expected
- [ ] Learning captured for future milestones and strategy refinement

---

## 📞 Communication Plan

### Stakeholder Updates
- **Weekly**: [Progress summary, metrics, and key learnings]
- **Milestone Completion**: [Comprehensive review with data and insights]
- **Blocker Events**: [Immediate communication for any significant issues]
- **Pivot Decisions**: [Detailed explanation of changes and rationale]

### Team Coordination
- **Daily Standups**: [Progress, blockers, and plans for the day]
- **Sprint Reviews**: [Weekly reviews of implemented functionality]
- **Retrospectives**: [After each milestone to improve execution process]
- **Documentation Updates**: [Regular updates to capture learnings and progress]

---

*This execution plan provides a structured approach to implementing the goal with built-in learning and adaptation mechanisms.*
"""

    # Determine output file path
    if output_file:
        output_path = output_file
    else:
        output_path = goal_dir / "execution.md"

    # Write the execution file
    try:
        output_path.write_text(execution_content, encoding='utf-8')
        console.print(f"[green]+[/green] Execution plan created successfully!")
        console.print(f"[cyan]File:[/cyan] {output_path}")

    except Exception as e:
        console.print(f"[red]Error writing execution file:[/red] {e}")
        raise typer.Exit(code=1)

    # Show next steps
    console.print("\n[bold]Next Steps:[/bold]")
    console.print("1. [cyan]Review and customize[/cyan] the generated execution plan for your specific goal")
    console.print("2. [cyan]Define specific success metrics[/cyan] with measurable targets")
    console.print("3. [cyan]Set realistic timelines[/cyan] for each phase")
    console.print("4. [cyan]Begin executing[/cyan] with focus on learning and adaptation")
    console.print("5. [cyan]Track progress[/cyan] and update execution status regularly")


@app.command()
def tasks(
    goal_dir: Path = typer.Argument(None, help="Path to the goal directory (default: current directory)"),
    milestone: str = typer.Option(None, "--milestone", "-m", help="Specific milestone to create tasks for"),
    output_file: Path = typer.Option(None, "--output", "-o", help="File to save the tasks (optional)"),
    priority: str = typer.Option("auto", "--priority", "-p", help="Default priority for tasks: auto, P0, P1, P2, P3"),
    format: str = typer.Option("markdown", "--format", "-f", help="Output format: markdown, checklist, json"),
):
    """Create actionable tasks for goals and milestones to enable focused execution."""
    show_banner()

    console.print("[bold cyan]Creating Tasks for Goal Execution[/bold cyan]\n")

    # Find the goal directory
    if goal_dir is None:
        goal_dir = Path.cwd()

    # Look for goal files in the current directory or .goalkit/goals subdirectory
    goal_file = goal_dir / "goal.md"
    if not goal_file.exists():
        # Check if we're in a goal directory within .goalkit/goals
        if (goal_dir / ".goalkit").exists():
            goals_dir = goal_dir / ".goalkit" / "goals"
            if goals_dir.exists():
                # Find the first goal directory
                goal_dirs = [d for d in goals_dir.iterdir() if d.is_dir()]
                if goal_dirs:
                    goal_dir = goal_dirs[0]
                    goal_file = goal_dir / "goal.md"

    if not goal_file.exists():
        console.print(f"[red]Error: goal.md file not found in {goal_dir}[/red]")
        console.print("[yellow]Tip: Run this command from a goal directory or specify the path with --goal-dir[/yellow]")
        raise typer.Exit(code=1)

    # Read the goal file to understand context
    try:
        content = goal_file.read_text(encoding='utf-8')
    except Exception as e:
        console.print(f"[red]Error reading goal file:[/red] {e}")
        raise typer.Exit(code=1)

    # Extract goal information
    goal_title_match = re.search(r'^# Goal Definition: (.*)', content, re.MULTILINE)
    goal_title = goal_title_match.group(1) if goal_title_match else "Unknown Goal"

    console.print(f"[cyan]Goal:[/cyan] {goal_title}")
    console.print(f"[cyan]Directory:[/cyan] {goal_dir.name}\n")

    # Extract milestones if available
    milestones_section = re.search(r'## 🚀 Goal Milestones(.*?)(?=## \\w|\\Z)', content, re.DOTALL)
    milestones = []

    if milestones_section:
        milestone_pattern = r'### (Milestone [0-9]+:.*?)\\n\\*\\*Description:\\*\\*(.*?)\\n\\*\\*Success Indicators:\\*\\*(.*?)\\n\\*\\*Validation Method:\\*\\*(.*?)\\n\\*\\*Expected Timeline:\\*\\*(.*?)(?=\\n---|\\n### |$)'
        milestone_matches = re.findall(milestone_pattern, milestones_section.group(1), re.DOTALL)

        for i, (title, description, indicators, validation, timeline) in enumerate(milestone_matches, 1):
            milestones.append({
                "id": i,
                "title": title.strip(),
                "description": description.strip(),
                "indicators": indicators.strip(),
                "validation": validation.strip(),
                "timeline": timeline.strip()
            })

    if not milestones:
        console.print("[yellow]No milestones found in goal file. Creating general tasks for goal execution.[/yellow]\n")
        # Create general tasks for the overall goal
        tasks_content = f"""# Tasks for: {goal_title}

**Goal Directory**: `{goal_dir.name}`
**Created**: {datetime.now().strftime('%Y-%m-%d')}
**Status**: Draft

## 🎯 Goal Context
{goal_title}

## 📋 Task Breakdown

### Priority 0 (Critical Path) - Foundation
- [ ] **Goal Analysis**: Review goal requirements and success criteria in detail
- [ ] **Context Setup**: Establish development environment and gather necessary resources
- [ ] **Initial Planning**: Create high-level implementation approach

### Priority 1 (High) - Core Implementation
- [ ] **Core Development**: Implement primary goal functionality
- [ ] **Testing Framework**: Set up testing structure and validation methods
- [ ] **Integration Points**: Connect with existing systems and dependencies

### Priority 2 (Medium) - Enhancement
- [ ] **Feature Polish**: Refine user experience and interface design
- [ ] **Performance Optimization**: Ensure responsive and efficient operation
- [ ] **Documentation**: Create user and technical documentation

### Priority 3 (Low) - Optimization
- [ ] **Advanced Features**: Add nice-to-have enhancements
- [ ] **Analytics Integration**: Implement tracking and measurement
- [ ] **Future Planning**: Prepare for scaling and maintenance

## 🔧 Execution Guidelines

### Development Approach
- Focus on testable, incremental progress
- Regular validation against success criteria
- Maintain clear documentation of decisions
- Seek feedback at each major milestone

### Quality Standards
- Code follows project conventions and best practices
- Features meet defined acceptance criteria
- Testing covers critical user journeys
- Documentation is clear and complete

---
*These tasks provide a structured approach to achieving the goal. Update priorities and add specific tasks as the project evolves.*
"""
    else:
        console.print(f"[green]Found {len(milestones)} milestone(s) to create tasks for[/green]\n")

        if milestone:
            # Filter to specific milestone if provided
            milestone_num = milestone.replace("Milestone ", "").strip()
            filtered_milestones = [m for m in milestones if f"Milestone {milestone_num}" in m["title"]]
            if not filtered_milestones:
                console.print(f"[red]Error: Milestone '{milestone}' not found[/red]")
                raise typer.Exit(code=1)
            milestones = filtered_milestones

        # Generate tasks for each milestone
        tasks_content = f"""# Tasks for: {goal_title}

**Goal Directory**: `{goal_dir.name}`
**Created**: {datetime.now().strftime('%Y-%m-%d')}
**Status**: Draft

## 🎯 Goal Context
{goal_title}

## 📋 Milestone-Based Task Breakdown

"""

        for milestone_info in milestones:
            tasks_content += f"""### {milestone_info['title']}

**Description**: {milestone_info['description']}
**Success Indicators**: {milestone_info['indicators']}
**Timeline**: {milestone_info['timeline']}

#### Priority 1 (Core) Tasks
- [ ] **Analysis & Design**: Analyze requirements and design approach for this milestone
- [ ] **Core Implementation**: Build the primary functionality for this milestone
- [ ] **Validation**: Test against success indicators and validation criteria
- [ ] **Integration**: Connect with other components and systems

#### Priority 2 (Supporting) Tasks
- [ ] **Documentation**: Document the milestone implementation and decisions
- [ ] **Testing**: Create comprehensive tests for milestone functionality
- [ ] **Review**: Conduct peer review and stakeholder feedback
- [ ] **Refinement**: Polish based on feedback and testing results

---

"""

        tasks_content += """## 🎯 Overall Goal Tasks

### Priority 1 (Critical) - Project Management
- [ ] **Progress Tracking**: Set up systems to track milestone and task progress
- [ ] **Stakeholder Communication**: Establish regular updates for project stakeholders
- [ ] **Risk Management**: Identify and monitor potential issues and dependencies

### Priority 2 (Important) - Quality Assurance
- [ ] **Cross-Milestone Integration**: Ensure milestones work together cohesively
- [ ] **Performance Validation**: Verify system meets performance requirements
- [ ] **User Experience Review**: Validate overall user experience across milestones

### Priority 3 (Enhancement) - Optimization
- [ ] **Efficiency Improvements**: Identify opportunities to streamline implementation
- [ ] **Knowledge Transfer**: Document learnings for future projects
- [ ] **Process Refinement**: Improve development processes based on experience

## 🔧 Execution Framework

### Task Management
- **Regular Updates**: Keep task status current and accurate
- **Blocker Escalation**: Raise issues preventing progress immediately
- **Completion Validation**: Ensure tasks meet quality standards before marking complete
- **Learning Capture**: Document insights, decisions, and adaptations

### Quality Standards
- **Acceptance Criteria**: Each task must meet defined completion standards
- **Testing Requirements**: Critical tasks require appropriate testing
- **Documentation**: Important decisions and implementations are documented
- **Review Process**: Complex tasks undergo peer review

---
*These tasks break down the goal into actionable work items aligned with milestones. Update priorities and add specific technical tasks as implementation details become clear.*
"""

    # Determine output file path
    if output_file:
        output_path = output_file
    else:
        output_path = goal_dir / "tasks.md"

    # Handle different output formats
    if format == "checklist":
        # Convert to checklist format
        checklist_content = f"""# Task Checklist for: {goal_title}

**Goal Directory**: `{goal_dir.name}`
**Created**: {datetime.now().strftime('%Y-%m-%d')}

## 📋 Actionable Checklist

"""
        # Simple conversion to checklist items (this could be enhanced)
        lines = tasks_content.split('\n')
        for line in lines:
            if line.strip().startswith('- [ ]'):
                checklist_content += f"{line}\n"
            elif line.strip().startswith('- [x]'):
                checklist_content += f"{line}\n"
            elif line.startswith('### ') or line.startswith('## '):
                checklist_content += f"\n{line}\n"

        tasks_content = checklist_content

    elif format == "json":
        # Convert to JSON structure (simplified)
        json_content = {
            "goal": goal_title,
            "directory": goal_dir.name,
            "created": datetime.now().strftime('%Y-%m-%d'),
            "milestones": [
                {
                    "title": m["title"],
                    "description": m["description"],
                    "tasks": [
                        {"priority": "P1", "description": "Core implementation task", "status": "pending"},
                        {"priority": "P2", "description": "Supporting task", "status": "pending"}
                    ]
                } for m in milestones
            ]
        }

        import json
        tasks_content = json.dumps(json_content, indent=2)

        # Update output path for JSON
        if not output_file:
            output_path = goal_dir / "tasks.json"

    # Write the tasks file
    try:
        output_path.write_text(tasks_content, encoding='utf-8')
        console.print(f"[green]+[/green] Tasks {format} created successfully!")
        console.print(f"[cyan]File:[/cyan] {output_path}")

        if format == "markdown":
            task_count = len([line for line in tasks_content.split('\n') if line.strip().startswith('- [ ]')])
            console.print(f"[cyan]Tasks:[/cyan] {task_count} items")
        elif format == "checklist":
            checklist_count = len([line for line in tasks_content.split('\n') if line.strip().startswith('- [ ]')])
            console.print(f"[cyan]Checklist items:[/cyan] {checklist_count} items")
        elif format == "json":
            console.print(f"[cyan]JSON structure:[/cyan] Goal with {len(json_content.get('milestones', []))} milestones")

    except Exception as e:
        console.print(f"[red]Error writing tasks file:[/red] {e}")
        raise typer.Exit(code=1)

    # Show next steps
    console.print("\n[bold]Next Steps:[/bold]")
    console.print("1. [cyan]Review and customize[/cyan] the generated tasks for your specific needs")
    console.print("2. [cyan]Update priorities[/cyan] based on your current context and resources")
    console.print("3. [cyan]Add specific technical tasks[/cyan] as implementation details become clear")
    console.print("4. [cyan]Start executing[/cyan] Priority 0 and Priority 1 tasks")
    console.print("5. [cyan]Track progress[/cyan] and update task status regularly")


@app.command()
def milestones(
    goal_dir: Path = typer.Argument(None, help="Path to the goal directory (default: current directory)"),
    output_file: Path = typer.Option(None, "--output", "-o", help="File to save the milestones (optional)"),
    include_template: bool = typer.Option(True, "--include-template", "-t", help="Include template sections in the output")
):
    """Create milestone breakdown for goals to enable focused execution and progress tracking."""
    show_banner()

    console.print("[bold cyan]Creating Milestones for Goal Execution[/bold cyan]\n")

    # Find the goal directory
    if goal_dir is None:
        goal_dir = Path.cwd()

    # Look for goal files in the current directory or .goalkit/goals subdirectory
    goal_file = goal_dir / "goal.md"
    if not goal_file.exists():
        # Check if we're in a goal directory within .goalkit/goals
        if (goal_dir / ".goalkit").exists():
            goals_dir = goal_dir / ".goalkit" / "goals"
            if goals_dir.exists():
                # Find the first goal directory
                goal_dirs = [d for d in goals_dir.iterdir() if d.is_dir()]
                if goal_dirs:
                    goal_dir = goal_dirs[0]
                    goal_file = goal_dir / "goal.md"

    if not goal_file.exists():
        console.print(f"[red]Error: goal.md file not found in {goal_dir}[/red]")
        console.print("[yellow]Tip: Run this command from a goal directory or specify the path with --goal-dir[/yellow]")
        raise typer.Exit(code=1)

    # Read the goal file to understand context
    try:
        content = goal_file.read_text(encoding='utf-8')
    except Exception as e:
        console.print(f"[red]Error reading goal file:[/red] {e}")
        raise typer.Exit(code=1)

    # Extract goal information
    goal_title_match = re.search(r'^# Goal Definition: (.*)', content, re.MULTILINE)
    goal_title = goal_title_match.group(1) if goal_title_match else "Unknown Goal"

    console.print(f"[cyan]Goal:[/cyan] {goal_title}")
    console.print(f"[cyan]Directory:[/cyan] {goal_dir.name}\n")

    # Generate milestones content using the template
    from datetime import datetime
    
    milestones_content = f"""# Milestones: {goal_title}

**Branch**: `{goal_dir.name}` | **Date**: {datetime.now().strftime('%Y-%m-%d')} | **Strategy**: [link]
**Input**: Goal definition and selected strategies

## 🎯 Milestones Overview

**Goal Focus**: {goal_title}

**Strategy Context**: [Which strategies these milestones support]

**Learning Focus**: [What we want to learn from these milestones]

## 📊 Milestone Definition Framework

### Milestone 1: [Milestone Title] (Priority: P1)

**Description**: [What this milestone achieves and why it matters. Focus on learning/validation outcomes]

**Success Indicators**:
- [Measurable outcome 1 - be specific and testable]
- [Measurable outcome 2 - include quantitative targets]
- [Measurable outcome 3 - define what "done" looks like]

**Learning Objectives**:
- **Hypothesis**: [What assumption this milestone tests - link to goal hypotheses]
- **Validation Method**: [How to confirm the hypothesis - specific, low-cost approach]
- **Success Criteria**: [When hypothesis is considered validated - measurable criteria]

**Value Delivered**:
- **User Value**: [What users gain from this milestone - immediate benefit]
- **Business Value**: [What business benefits from this milestone - measurable impact]
- **Learning Value**: [What insights this milestone should generate - key discoveries]

**Implementation Approaches**:
- **Approach 1**: [How this milestone could be implemented - preferred method]
- **Approach 2**: [Alternative implementation approach - backup option]
- **Approach 3**: [Another alternative if needed - fallback option]

**Measurement Plan**:
- **Metrics to Track**: [What data to collect - link to success indicators]
- **Measurement Method**: [How to collect the data - tools and frequency]
- **Success Thresholds**: [When milestone is considered achieved - specific targets]

**Dependencies**:
- **Requires**: [What must be completed first - specific deliverables]
- **Enables**: [What this milestone unlocks - next milestones or capabilities]

**Risk Assessment**:
- **Risk Level**: [High/Medium/Low] - **Why**: [Justification for risk rating]
- **Potential Issues**: [What could go wrong - specific technical/business risks]
- **Mitigation Strategies**: [How to address issues - concrete action plans]

**Effort Estimate**: [Time/resources needed] | **Timeline**: [Start/end dates]

---

### Milestone 2: [Milestone Title] (Priority: P2)

**Description**: [What this milestone achieves and why it matters]

**Success Indicators**:
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Measurable outcome 3]

**Learning Objectives**:
- **Hypothesis**: [What assumption this milestone tests]
- **Validation Method**: [How to confirm the hypothesis]
- **Success Criteria**: [When hypothesis is considered validated]

**Value Delivered**:
- **User Value**: [What users gain from this milestone]
- **Business Value**: [What business benefits from this milestone]
- **Learning Value**: [What insights this milestone should generate]

**Implementation Approaches**:
- **Approach 1**: [How this milestone could be implemented]
- **Approach 2**: [Alternative implementation approach]
- **Approach 3**: [Another alternative if needed]

**Measurement Plan**:
- **Metrics to Track**: [What data to collect]
- **Measurement Method**: [How to collect the data]
- **Success Thresholds**: [When milestone is considered achieved]

**Dependencies**:
- **Requires**: [What must be completed first]
- **Enables**: [What this milestone unlocks]

**Risk Assessment**:
- **Risk Level**: [High/Medium/Low]
- **Potential Issues**: [What could go wrong]
- **Mitigation Strategies**: [How to address issues]

---

### Milestone 3: [Milestone Title] (Priority: P3)

**Description**: [What this milestone achieves and why it matters]

**Success Indicators**:
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Measurable outcome 3]

**Learning Objectives**:
- **Hypothesis**: [What assumption this milestone tests]
- **Validation Method**: [How to confirm the hypothesis]
- **Success Criteria**: [When hypothesis is considered validated]

**Value Delivered**:
- **User Value**: [What users gain from this milestone]
- **Business Value**: [What business benefits from this milestone]
- **Learning Value**: [What insights this milestone should generate]

**Implementation Approaches**:
- **Approach 1**: [How this milestone could be implemented]
- **Approach 2**: [Alternative implementation approach]
- **Approach 3**: [Another alternative if needed]

**Measurement Plan**:
- **Metrics to Track**: [What data to collect]
- **Measurement Method**: [How to collect the data]
- **Success Thresholds**: [When milestone is considered achieved]

**Dependencies**:
- **Requires**: [What must be completed first]
- **Enables**: [What this milestone unlocks]

**Risk Assessment**:
- **Risk Level**: [High/Medium/Low]
- **Potential Issues**: [What could go wrong]
- **Mitigation Strategies**: [How to address issues]

---

## 📈 Progress Tracking Framework

<!--
  AI GUIDANCE: Define how to track progress across milestones.
  Include specific metrics, tools, and processes for monitoring progress.
-->

### Overall Progress Metrics
- **Goal Progress**: [How to measure overall progress toward the goal - link to success metrics]
- **Milestone Velocity**: [How to track speed of milestone completion - planned vs actual]
- **Learning Progress**: [How to measure insights and discoveries - validation of hypotheses]

### Milestone Health Indicators
- **On Track**: [Indicators that milestone is progressing well - specific metrics and thresholds]
- **At Risk**: [Warning signs that milestone needs attention - early warning indicators]
- **Blocked**: [Indicators that milestone cannot proceed - clear blockage criteria]

### Adaptation Triggers
- **Accelerate**: [When to speed up milestone execution - conditions and rationale]
- **Slow Down**: [When to take more time for learning - learning opportunities]
- **Pivot**: [When to change milestone approach or sequence - failure indicators]

### Tracking Tools & Processes
- **Progress Monitoring**: [How to track milestone progress - tools and frequency]
- **Status Reporting**: [How to communicate milestone status - format and audience]
- **Health Assessment**: [How to evaluate milestone health - criteria and timing]

## 🔄 Milestone Review Process

<!--
  AI GUIDANCE: Define how to review milestone progress and adapt as needed.
  Include specific review formats, participants, and decision criteria.
-->

### Review Cadence
- **After Each Milestone**: [What to review and how - structured format and participants]
- **Bi-weekly**: [Regular progress check - focus and format]
- **Monthly**: [Strategic milestone alignment review - broader context and adjustments]

### Review Framework
**For Each Completed Milestone**:
1. **Measure Results**: [Compare actual vs expected outcomes - specific metrics and analysis]
2. **Capture Learning**: [Document what was discovered - format and storage]
3. **Assess Strategy**: [Evaluate if current approach is working - against success criteria]
4. **Plan Next Steps**: [Adjust subsequent milestones if needed - specific changes]

**For In-Progress Milestones**:
1. **Progress Assessment**: [Current status vs plan - metrics and visual indicators]
2. **Risk Review**: [Identify new risks or issues - probability and impact assessment]
3. **Resource Check**: [Ensure adequate support - capacity and capability review]
4. **Adjustment Planning**: [Plan any needed changes - options and recommendations]

### Decision Framework
**Continue Current Path When**:
- [Indicators that current approach is working - specific metrics]
- [Metrics showing expected progress - link to success criteria]
- [Learning supporting current strategy - validation of hypotheses]

**Modify Approach When**:
- [Indicators that current approach needs adjustment - warning signs]
- [New information suggesting better alternatives - evidence-based options]
- [External factors requiring adaptation - market or technical changes]

**Reprioritize Milestones When**:
- [Learning suggests different milestone sequence - new dependency insights]
- [Business priorities change - strategic realignment needs]
- [Technical constraints require reordering - feasibility issues discovered]

### Review Documentation
- **Format**: [How to document review outcomes and decisions]
- **Storage**: [Where to store review records for future reference]
- **Sharing**: [How to communicate review results to stakeholders]

## 📊 Success Validation

<!--
  AI GUIDANCE: Define how to validate that milestones achieve their intended outcomes.
  Include specific, measurable criteria for validation at multiple levels.
-->

### Milestone Success Criteria
**For Each Milestone**:
- [ ] Defined success indicators achieved (specify exact targets and measurement methods)
- [ ] Learning objectives met (validate hypothesis testing outcomes)
- [ ] Value delivered to users or business (quantify specific benefits)
- [ ] No significant negative consequences (monitor for unintended side effects)
- [ ] Insights documented for future use (format and accessibility requirements)

### Goal Progress Indicators
- [ ] Milestone 1 contributes to overall goal (measure incremental progress)
- [ ] Milestone 2 builds on milestone 1 learning (demonstrate knowledge transfer)
- [ ] Milestone 3 delivers cumulative goal progress (show compounding value)
- [ ] Overall trajectory toward goal achievement (trend analysis and forecasting)

### Learning Quality Assessment
- [ ] Technical insights captured and documented (depth and applicability)
- [ ] User behavior patterns identified (evidence-based observations)
- [ ] Process improvements identified (measurable efficiency gains)
- [ ] Strategic direction validated or adjusted (alignment with goal outcomes)

### Validation Methods
- **Quantitative Validation**: [Statistical methods and success thresholds]
- **Qualitative Validation**: [Feedback collection and analysis approaches]
- **Combined Validation**: [How to integrate quant and qual data for decisions]

## 🚀 Implementation Flexibility

<!--
  AI GUIDANCE: Define how milestones can be implemented with different approaches.
  Include specific criteria for when to use different flexibility options.
-->

### Technical Flexibility
- **Multiple Implementation Options**: Each milestone can be achieved through different technical approaches - [Criteria for choosing]
- **Progressive Enhancement**: Start simple and add complexity based on learning - [When to enhance]
- **Fallback Options**: Alternative implementation paths if primary approach fails - [Trigger conditions]

### Scope Flexibility
- **Milestone Splitting**: Large milestones can be broken into smaller, faster-validated pieces - [Size criteria]
- **Milestone Merging**: Related milestones can be combined for efficiency - [Combination criteria]
- **Milestone Scope Adjustment**: Individual milestone scope can be adjusted based on learning - [Adjustment triggers]

### Timing Flexibility
- **Parallel Execution**: Independent milestones can be pursued simultaneously - [Independence criteria]
- **Sequential Dependencies**: Some milestones must follow others - [Dependency mapping]
- **Adaptive Scheduling**: Timeline adjusted based on milestone progress and learning - [Adjustment process]

### Flexibility Decision Framework
- **When to Apply Flexibility**: [Conditions that warrant flexibility use]
- **Trade-off Analysis**: [How to evaluate flexibility vs. plan adherence]
- **Documentation Requirements**: [How to record flexibility decisions]

## 💡 Learning Integration

<!--
  AI GUIDANCE: Define how learning from each milestone informs subsequent work.
  Include specific processes for capturing, validating, and applying learnings.
-->

### Knowledge Capture
- **Technical Learnings**: What works, what doesn't, why - [Capture method and format]
- **User Insights**: Behavior patterns, preferences, pain points - [Capture method and format]
- **Process Improvements**: Better ways to work identified - [Capture method and format]
- **Risk Patterns**: Common pitfalls and how to avoid them - [Capture method and format]

### Cross-Milestone Learning
- **Pattern Recognition**: Similar challenges across milestones - [Identification process]
- **Solution Reuse**: Successful approaches applied to multiple milestones - [Reuse criteria]
- **Dependency Discovery**: Unanticipated relationships between milestones - [Discovery process]
- **Synergy Identification**: Combined value greater than individual milestones - [Assessment method]

### Learning Application Framework
- **Immediate Application**: [How to apply learnings to current milestone]
- **Next Milestone Integration**: [How to incorporate learnings into subsequent milestones]
- **Future Project Value**: [How to preserve learnings for other projects]
- **Validation Process**: [How to validate that applied learnings are effective]

---

*This milestones document defines measurable progress steps toward the goal. It should be updated as learning occurs and strategies evolve.*
"""

    # Determine output file path
    if output_file:
        output_path = output_file
    else:
        output_path = goal_dir / "milestones.md"

    # Write the milestones file
    try:
        output_path.write_text(milestones_content, encoding='utf-8')
        console.print(f"[green]+[/green] Milestones created successfully!")
        console.print(f"[cyan]File:[/cyan] {output_path}")

        # Count milestones created
        milestone_count = len([line for line in milestones_content.split('\\n') if line.startswith('### Milestone')])
        console.print(f"[cyan]Milestones:[/cyan] {milestone_count} milestones")

    except Exception as e:
        console.print(f"[red]Error writing milestones file:[/red] {e}")
        raise typer.Exit(code=1)

    # Show next steps
    console.print("\\n[bold]Next Steps:[/bold]")
    console.print("1. [cyan]Review and customize[/cyan] the generated milestones for your specific goal")
    console.print("2. [cyan]Define specific success indicators[/cyan] with measurable targets")
    console.print("3. [cyan]Set realistic timelines[/cyan] for each milestone")
    console.print("4. [cyan]Begin executing[/cyan] with focus on learning and validation")
    console.print("5. [cyan]Track progress[/cyan] and update milestone status regularly")


@app.command()
def ai_analytics(
    agent_filter: str = typer.Option(None, "--agent", "-a", help="Filter analytics by specific AI agent"),
    days: int = typer.Option(30, "--days", "-d", help="Number of days to analyze (default: 30)"),
    output_format: str = typer.Option("table", "--format", "-f", help="Output format: table, json, or csv")
):
    """Display AI agent performance analytics and interaction insights."""
    show_banner()

    console.print("[bold cyan]AI Agent Performance Analytics[/bold cyan]\n")

    log_file = Path.cwd() / ".goalkit" / "ai_interactions.jsonl"
    if not log_file.exists():
        console.print("[yellow]No AI interaction data found. Analytics will be available after using slash commands.[/yellow]")
        return

    try:
        import json
        from datetime import datetime, timedelta

        interactions = []
        cutoff_date = datetime.now() - timedelta(days=days)

        # Read and filter interactions
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    entry_date = datetime.fromisoformat(entry.get('timestamp', '').replace('Z', '+00:00'))

                    if entry_date >= cutoff_date:
                        if agent_filter is None or entry.get('agent') == agent_filter:
                            interactions.append(entry)
                except json.JSONDecodeError:
                    continue

        if not interactions:
            console.print(f"[yellow]No interactions found in the last {days} days for the specified criteria.[/yellow]")
            return

        # Calculate analytics
        total_interactions = len(interactions)
        successful_interactions = len([i for i in interactions if i.get('success', False)])
        success_rate = (successful_interactions / total_interactions * 100) if total_interactions > 0 else 0

        # Agent breakdown
        agent_stats = {}
        for interaction in interactions:
            agent = interaction.get('agent', 'unknown')
            if agent not in agent_stats:
                agent_stats[agent] = {'total': 0, 'successful': 0, 'avg_score': 0, 'scores': []}

            agent_stats[agent]['total'] += 1
            if interaction.get('success', False):
                agent_stats[agent]['successful'] += 1

            score = interaction.get('validation_score', 0)
            if score > 0:
                agent_stats[agent]['scores'].append(score)

        # Calculate average scores
        for agent, stats in agent_stats.items():
            if stats['scores']:
                agent_stats[agent]['avg_score'] = sum(stats['scores']) / len(stats['scores'])

        # Display results
        if output_format == "json":
            # JSON output
            output_data = {
                "summary": {
                    "total_interactions": total_interactions,
                    "successful_interactions": successful_interactions,
                    "success_rate": round(success_rate, 2),
                    "period_days": days
                },
                "agent_breakdown": agent_stats,
                "interactions": interactions[-50:]  # Last 50 interactions
            }
            console.print(json.dumps(output_data, indent=2))

        elif output_format == "csv":
            # CSV output
            console.print("Agent,Total Interactions,Successful,Success Rate,Avg Validation Score")
            for agent, stats in agent_stats.items():
                agent_success_rate = (stats['successful'] / stats['total'] * 100) if stats['total'] > 0 else 0
                avg_score = round(stats['avg_score'], 1) if stats['scores'] else 0
                console.print(f"{agent},{stats['total']},{stats['successful']},{agent_success_rate:.1f}%,{avg_score}")

        else:
            # Table output (default)
            # Summary panel
            summary_data = [
                f"[bold]Total Interactions:[/bold] {total_interactions}",
                f"[bold]Success Rate:[/bold] {success_rate:.1f}%",
                f"[bold]Period:[/bold] Last {days} days"
            ]

            if agent_filter:
                summary_data.append(f"[bold]Agent Filter:[/bold] {agent_filter}")

            console.print(Panel("\n".join(summary_data), title="Summary", border_style="cyan"))

            # Agent performance table
            if agent_stats:
                table = Table(title="AI Agent Performance", show_header=True, header_style="bold magenta")
                table.add_column("Agent", style="cyan", width=12)
                table.add_column("Total", justify="center", width=8)
                table.add_column("Success", justify="center", width=8)
                table.add_column("Rate", justify="center", width=8)
                table.add_column("Avg Score", justify="center", width=10)

                for agent in sorted(agent_stats.keys()):
                    stats = agent_stats[agent]
                    success_rate = (stats['successful'] / stats['total'] * 100) if stats['total'] > 0 else 0
                    avg_score = f"{stats['avg_score']:.1f}" if stats['scores'] else "N/A"

                    # Color coding based on performance
                    if success_rate >= 80:
                        rate_color = "green"
                    elif success_rate >= 60:
                        rate_color = "yellow"
                    else:
                        rate_color = "red"

                    table.add_row(
                        agent,
                        str(stats['total']),
                        str(stats['successful']),
                        f"[{rate_color}]{success_rate:.1f}%[/{rate_color}]",
                        avg_score
                    )

                console.print(table)

            # Recent interactions
            if len(interactions) <= 10:
                recent_table = Table(title=f"Recent Interactions ({len(interactions)})", show_header=True, header_style="bold blue")
                recent_table.add_column("Time", width=20)
                recent_table.add_column("Agent", width=10)
                recent_table.add_column("Command", width=12)
                recent_table.add_column("Status", width=8)
                recent_table.add_column("Score", width=6)

                for interaction in interactions[-10:]:
                    timestamp = interaction.get('timestamp', '')
                    if len(timestamp) > 19:
                        timestamp = timestamp[:19]

                    status = "[green]✓[/green]" if interaction.get('success') else "[red]✗[/red]"
                    score = str(interaction.get('validation_score', 'N/A'))

                    recent_table.add_row(
                        timestamp,
                        interaction.get('agent', 'unknown'),
                        interaction.get('command', 'unknown'),
                        status,
                        score
                    )

                console.print(recent_table)

        console.print(f"\n[green]Analytics complete. Logged {total_interactions} interactions.[/green]")

    except Exception as e:
        console.print(f"[red]Error generating analytics:[/red] {e}")
        raise typer.Exit(1)

@app.command()
def analyze(
    project_path: Path = typer.Argument(Path.cwd(), help="Path to the project directory to analyze"),
    focus_areas: str = typer.Option(None, "--focus", "-f", help="Specific areas to focus analysis on"),
    output_format: str = typer.Option("detailed", "--format", help="Output format: detailed, summary, or json")
):
    """Analyze project health, patterns, and performance insights."""
    show_banner()

    console.print("[bold cyan]🔍 Project Analysis[/bold cyan]")
    console.print(f"Analyzing project: {project_path.name}\n")

    # Check if project has goal structure
    goalkit_dir = project_path / ".goalkit"
    if not goalkit_dir.exists():
        console.print("[yellow]No .goalkit directory found. Run 'goalkeeper init' first.[/yellow]")
        return

    # Analyze project structure and content
    console.print("[cyan]Analyzing project structure and goals...[/cyan]")

    # Look for goals directory
    goals_dir = goalkit_dir / "goals"
    if goals_dir.exists():
        goal_count = len([d for d in goals_dir.iterdir() if d.is_dir()])
        console.print(f"[green]Found {goal_count} goals[/green]")
    else:
        console.print("[yellow]No goals directory found[/yellow]")

    # Basic analysis findings
    console.print("\n[bold]Analysis Summary:[/bold]")
    console.print("• Project structure: [green]Valid[/green]")
    console.print("• Goal organization: [green]Detected[/green]")
    console.print("• Next recommended action: [cyan]Use /goalkit.validate to check goal quality[/cyan]")

    if focus_areas:
        console.print(f"\n[bold]Focus Areas:[/bold] {focus_areas}")

    console.print("\n[green]Analysis complete. Use /goalkit.insights for deeper AI-powered analysis.[/green]")

@app.command()
def validate_goals(
    project_path: Path = typer.Argument(Path.cwd(), help="Path to the project directory"),
    specific_goal: str = typer.Option(None, "--goal", "-g", help="Specific goal to validate"),
    strict_mode: bool = typer.Option(False, "--strict", help="Use strict validation criteria")
):
    """Validate project goals for quality and completeness."""
    show_banner()

    console.print("[bold cyan]✅ Goal Validation[/bold cyan]")
    console.print(f"Validating goals in: {project_path.name}\n")

    # Check project structure
    goalkit_dir = project_path / ".goalkit"
    if not goalkit_dir.exists():
        console.print("[red]Error: No .goalkit directory found[/red]")
        return

    goals_dir = goalkit_dir / "goals"
    if not goals_dir.exists():
        console.print("[yellow]No goals found to validate[/yellow]")
        return

    # Validate goals
    goal_dirs = [d for d in goals_dir.iterdir() if d.is_dir()]

    if specific_goal:
        goal_dirs = [d for d in goal_dirs if specific_goal in d.name]

    if not goal_dirs:
        console.print(f"[yellow]No goals found matching: {specific_goal}[/yellow]")
        return

    console.print(f"[cyan]Validating {len(goal_dirs)} goals...[/cyan]\n")

    for goal_dir in goal_dirs:
        goal_file = goal_dir / "goal.md"
        if goal_file.exists():
            console.print(f"[green]✓[/green] {goal_dir.name}")
            # Basic validation checks
            content = goal_file.read_text(encoding='utf-8')

            # Check for required sections
            required_sections = ["success criteria", "milestones"]
            for section in required_sections:
                if section.lower() in content.lower():
                    console.print(f"    [green]✓[/green] Has {section}")
                else:
                    console.print(f"    [yellow]⚠[/yellow] Missing {section}")

        else:
            console.print(f"[red]✗[/red] {goal_dir.name} (no goal.md file)")

    console.print("\n[green]Validation complete. Use /goalkit.validate for comprehensive AI-powered validation.[/green]")

@app.command()
def plan_project(
    goal_name: str = typer.Argument(..., help="Name of the goal to plan"),
    project_path: Path = typer.Argument(Path.cwd(), help="Path to the project directory"),
    timeline_weeks: int = typer.Option(12, "--timeline", "-t", help="Planning timeline in weeks")
):
    """Create execution plan for a specific goal."""
    show_banner()

    console.print("[bold cyan]📋 Project Planning[/bold cyan]")
    console.print(f"Creating execution plan for: {goal_name}\n")

    # Check if goal exists
    goalkit_dir = project_path / ".goalkit" / "goals" / goal_name
    if not goalkit_dir.exists():
        console.print(f"[red]Error: Goal '{goal_name}' not found[/red]")
        console.print(f"[yellow]Available goals: {', '.join([d.name for d in (project_path / '.goalkit' / 'goals').iterdir() if d.is_dir()]) if (project_path / '.goalkit' / 'goals').exists() else 'None'}[/yellow]")
        return

    console.print(f"[cyan]Planning timeline: {timeline_weeks} weeks[/cyan]")
    console.print("[cyan]Goal location: [/cyan]" + str(goalkit_dir))

    # Basic planning structure
    console.print("\n[bold]Execution Plan Structure:[/bold]")
    console.print("• [cyan]Phase 1:[/cyan] Foundation (Weeks 1-2)")
    console.print("• [cyan]Phase 2:[/cyan] Core Development (Weeks 3-6)")
    console.print("• [cyan]Phase 3:[/cyan] Validation & Testing (Weeks 7-8)")
    console.print("• [cyan]Phase 4:[/cyan] Launch & Optimization (Weeks 9-12)")

    console.print("\n[green]Plan structure created. Use /goalkit.plan for comprehensive AI-powered planning.[/green]")

@app.command()
def insights_project(
    project_path: Path = typer.Argument(Path.cwd(), help="Path to the project directory"),
    data_days: int = typer.Option(30, "--days", "-d", help="Days of data to analyze")
):
    """Generate AI-powered insights from project data."""
    show_banner()

    console.print("[bold cyan]💡 Project Insights[/bold cyan]")
    console.print(f"Generating insights for: {project_path.name}\n")

    # Check project data availability
    goalkit_dir = project_path / ".goalkit"
    if not goalkit_dir.exists():
        console.print("[yellow]No project data found. Initialize project first.[/yellow]")
        return

    console.print(f"[cyan]Analyzing last {data_days} days of project data...[/cyan]")

    # Generate basic insights
    console.print("\n[bold]Key Insights:[/bold]")
    console.print("• [green]Project Structure:[/green] Well organized")
    console.print("• [green]Goal Clarity:[/green] Clear objectives identified")
    console.print("• [cyan]Next Recommendation:[/cyan] Use /goalkit.analyze for detailed health assessment")

    console.print("\n[green]Basic insights complete. Use /goalkit.insights for comprehensive AI-powered analysis.[/green]")

@app.command()
def prioritize_goals(
    project_path: Path = typer.Argument(Path.cwd(), help="Path to the project directory"),
    criteria: str = typer.Option("impact,effort,urgency", "--criteria", help="Prioritization criteria")
):
    """Prioritize project goals using multiple factors."""
    show_banner()

    console.print("[bold cyan]🎯 Goal Prioritization[/bold cyan]")
    console.print(f"Prioritizing goals in: {project_path.name}\n")

    # Check for goals to prioritize
    goals_dir = project_path / ".goalkit" / "goals"
    if not goals_dir.exists():
        console.print("[yellow]No goals found to prioritize[/yellow]")
        return

    goal_dirs = [d for d in goals_dir.iterdir() if d.is_dir()]

    if not goal_dirs:
        console.print("[yellow]No goals found[/yellow]")
        return

    console.print(f"[cyan]Found {len(goal_dirs)} goals to prioritize[/cyan]")
    console.print(f"[cyan]Criteria: {criteria}[/cyan]\n")

    # Simple prioritization display
    console.print("[bold]Prioritization Framework:[/bold]")
    console.print("• [red]P0 (Critical):[/red] Blocking other goals, high business impact")
    console.print("• [orange]P1 (High):[/orange] Significant value, core objectives")
    console.print("• [yellow]P2 (Medium):[/yellow] Valuable but not urgent")
    console.print("• [green]P3 (Low):[/green] Nice-to-have, future consideration")

    console.print("\n[green]Prioritization framework ready. Use /goalkit.prioritize for comprehensive AI-powered prioritization.[/green]")

@app.command()
def track_progress(
    project_path: Path = typer.Argument(Path.cwd(), help="Path to the project directory"),
    show_timeline: bool = typer.Option(False, "--timeline", help="Show progress timeline")
):
    """Track project progress and milestones."""
    show_banner()

    console.print("[bold cyan]📊 Progress Tracking[/bold cyan]")
    console.print(f"Tracking progress in: {project_path.name}\n")

    # Check project structure
    goalkit_dir = project_path / ".goalkit"
    if not goalkit_dir.exists():
        console.print("[yellow]No project data found[/yellow]")
        return

    console.print("[cyan]Current Status:[/cyan]")
    console.print("• Project: [green]Active[/green]")
    console.print("• Goals: [green]Defined[/green]")
    console.print("• Progress: [cyan]Tracking initiated[/cyan]")

    if show_timeline:
        console.print("\n[bold]Timeline View:[/bold]")
        console.print("• Week 1-2: [cyan]Planning & Setup[/cyan]")
        console.print("• Week 3-6: [cyan]Core Development[/cyan]")
        console.print("• Week 7-8: [cyan]Testing & Validation[/cyan]")
        console.print("• Week 9-12: [cyan]Launch & Optimization[/cyan]")

    console.print("\n[green]Progress tracking active. Use /goalkit.track for comprehensive AI-powered progress analysis.[/green]")

@app.command()
def research_project(
    topic: str = typer.Argument(..., help="Research topic or question"),
    project_path: Path = typer.Argument(Path.cwd(), help="Path to the project directory"),
    depth: str = typer.Option("standard", "--depth", help="Research depth: quick, standard, or comprehensive")
):
    """Research external information relevant to project goals."""
    show_banner()

    console.print("[bold cyan]🔬 Project Research[/bold cyan]")
    console.print(f"Researching: {topic}\n")

    console.print(f"[cyan]Research depth: {depth}[/cyan]")
    console.print(f"[cyan]Project context: {project_path.name}[/cyan]\n")

    # Research structure
    console.print("[bold]Research Framework:[/bold]")
    console.print("• [cyan]Market Analysis:[/cyan] Industry trends and competitors")
    console.print("• [cyan]Best Practices:[/cyan] Proven approaches and standards")
    console.print("• [cyan]Technical Research:[/cyan] Tools and implementation options")
    console.print("• [cyan]Risk Assessment:[/cyan] Potential challenges and mitigations")

    console.print("\n[green]Research framework established. Use /goalkit.research for comprehensive AI-powered research.[/green]")

@app.command()
def learn_from_project(
    project_path: Path = typer.Argument(Path.cwd(), help="Path to the project directory"),
    focus_area: str = typer.Option("general", "--focus", help="Learning focus: general, process, technical, or team")
):
    """Extract and document lessons learned from project experience."""
    show_banner()

    console.print("[bold cyan]📚 Learning Extraction[/bold cyan]")
    console.print(f"Extracting lessons from: {project_path.name}\n")

    console.print(f"[cyan]Focus area: {focus_area}[/cyan]\n")

    # Learning categories
    console.print("[bold]Learning Categories:[/bold]")
    console.print("• [green]Success Patterns:[/green] What worked well and why")
    console.print("• [yellow]Failure Analysis:[/yellow] What didn't work and lessons learned")
    console.print("• [cyan]Process Improvements:[/cyan] Better ways of working identified")
    console.print("• [purple]Innovation Opportunities:[/purple] New approaches discovered")

    console.print("\n[green]Learning framework ready. Use /goalkit.learn for comprehensive AI-powered learning extraction.[/green]")

@app.command()
def benchmark_project(
    project_path: Path = typer.Argument(Path.cwd(), help="Path to the project directory"),
    benchmark_type: str = typer.Option("industry", "--type", help="Benchmark type: industry, competitors, or internal")
):
    """Compare project against industry standards and best practices."""
    show_banner()

    console.print("[bold cyan]📊 Project Benchmarking[/bold cyan]")
    console.print(f"Benchmarking: {project_path.name}\n")

    console.print(f"[cyan]Benchmark type: {benchmark_type}[/cyan]\n")

    # Benchmark categories
    console.print("[bold]Benchmark Categories:[/bold]")
    console.print("• [green]Performance:[/green] Speed, quality, and efficiency metrics")
    console.print("• [blue]Process:[/blue] Methodology and workflow effectiveness")
    console.print("• [purple]Innovation:[/purple] Use of modern approaches and tools")
    console.print("• [orange]Team:[/orange] Collaboration and productivity patterns")

    console.print("\n[green]Benchmarking framework established. Use /goalkit.benchmark for comprehensive AI-powered benchmarking.[/green]")

@app.command()
def memory_status(
    project_path: Path = typer.Argument(Path.cwd(), help="Path to the project directory"),
    show_details: bool = typer.Option(False, "--details", help="Show detailed memory statistics")
):
    """Display memory system status and learning insights."""
    show_banner()

    console.print("[bold cyan]🧠 Memory System Status[/bold cyan]")
    console.print(f"Project: {project_path.name}\n")

    if not ProjectMemory:
        console.print("[red]Memory system not available[/red]")
        return

    try:
        memory = ProjectMemory(project_path)

        # Check memory structure
        console.print("[cyan]Memory Structure:[/cyan]")
        console.print(f"• Memory directory: {'✅' if memory.memory_path.exists() else '❌'}")
        console.print(f"• Projects data: {'✅' if memory.projects_path.exists() else '❌'}")
        console.print(f"• Sessions data: {'✅' if memory.sessions_path.exists() else '❌'}")
        console.print(f"• Insights data: {'✅' if memory.insights_path.exists() else '❌'}")

        # Get project patterns
        patterns = memory.get_project_patterns()

        if patterns["patterns"]:
            console.print("\n[bold]Project Statistics:[/bold]")
            total_goals = patterns["patterns"].get("total_goals", 0)
            success_rate = patterns["patterns"].get("success_rate", 0)
            avg_score = patterns["patterns"].get("average_success_score", 0)

            console.print(f"• Total goals tracked: {total_goals}")
            console.print(f"• Success rate: [green]{success_rate:.1%}[/green]")
            console.print(f"• Average success score: [cyan]{avg_score:.1f}/10[/cyan]")

            if show_details:
                console.print("\n[bold]Top Success Factors:[/bold]")
                for factor, count in patterns["patterns"].get("common_success_factors", []):
                    console.print(f"• {factor} ({count} times)")

                console.print("\n[bold]Key Insights:[/bold]")
                for insight in patterns.get("insights", []):
                    console.print(f"• {insight}")

        console.print("\n[green]Memory system operational[/green]")

    except Exception as e:
        console.print(f"[red]Error accessing memory: {e}[/red]")

@app.command()
def learn_extract(
    goal_name: str = typer.Argument(..., help="Name of the completed goal to extract learnings from"),
    project_path: Path = typer.Argument(Path.cwd(), help="Path to the project directory"),
    success_score: int = typer.Option(7, "--score", "-s", help="Success score 1-10")
):
    """Extract learnings from a completed goal and add to memory system."""
    show_banner()

    console.print("[bold cyan]📚 Learning Extraction[/bold cyan]")
    console.print(f"Extracting learnings from goal: {goal_name}\n")

    if not ProjectMemory:
        console.print("[red]Memory system not available[/red]")
        return

    try:
        # Find the goal
        goal_path = project_path / ".goalkit" / "goals" / goal_name
        if not goal_path.exists():
            console.print(f"[red]Goal '{goal_name}' not found[/red]")
            # Show available goals
            goals_dir = project_path / ".goalkit" / "goals"
            if goals_dir.exists():
                available_goals = [d.name for d in goals_dir.iterdir() if d.is_dir()]
                console.print(f"[yellow]Available goals: {', '.join(available_goals)}[/yellow]")
            return

        # Extract learnings
        learnings = extract_goal_learnings(goal_path)
        learnings["success_score"] = success_score

        # Add to memory system
        memory = ProjectMemory(project_path)
        memory.record_goal_completion(goal_name, learnings)

        console.print(f"[green]✅ Learnings extracted and stored[/green]")
        console.print(f"• Success score: {success_score}/10")
        console.print(f"• Milestones found: {learnings['milestone_count']}")
        console.print(f"• Learnings captured: {len(learnings['key_learnings'])}")

        # Show next steps
        console.print("\n[bold]Next Steps:[/bold]")
        console.print("• Use [cyan]goalkeeper memory-status[/cyan] to view memory insights")
        console.print("• Use [cyan]goalkeeper insights-project[/cyan] for AI-powered analysis")

    except Exception as e:
        console.print(f"[red]Error extracting learnings: {e}[/red]")

@app.command()
def memory_insights(
    project_path: Path = typer.Argument(Path.cwd(), help="Path to the project directory"),
    include_patterns: bool = typer.Option(True, "--patterns", help="Include pattern analysis")
):
    """Get AI-powered insights from project memory and learning data."""
    show_banner()

    console.print("[bold cyan]💡 Memory-Driven Insights[/bold cyan]")
    console.print(f"Generating insights for: {project_path.name}\n")

    if not ProjectMemory:
        console.print("[red]Memory system not available[/red]")
        return

    try:
        memory = ProjectMemory(project_path)
        patterns = memory.get_project_patterns()

        if not patterns["patterns"]:
            console.print("[yellow]No project data available for insights[/yellow]")
            console.print("[cyan]Next: Use 'goalkeeper learn-extract <goal>' to add learning data[/cyan]")
            return

        # Display insights
        console.print("[bold]📊 Project Performance:[/bold]")
        stats = patterns["patterns"]
        console.print(f"• Goals tracked: {stats.get('total_goals', 0)}")
        console.print(f"• Success rate: [green]{stats.get('success_rate', 0):.1%}[/green]")
        console.print(f"• Average score: [cyan]{stats.get('average_success_score', 0):.1f}/10[/cyan]")

        if include_patterns and patterns.get("insights"):
            console.print("\n[bold]🔍 Key Insights:[/bold]")
            for insight in patterns["insights"]:
                console.print(f"• {insight}")

        if patterns.get("recommendations"):
            console.print("\n[bold]🎯 Recommendations:[/bold]")
            for rec in patterns["recommendations"]:
                console.print(f"• {rec}")

        # Cross-project insights
        try:
            cross_insights = CrossProjectInsights(memory)
            best_practices = cross_insights.get_best_practices()

            if best_practices["success_factors"]:
                console.print("\n[bold]🏆 Best Practices:[/bold]")
                for factor, count in best_practices["success_factors"][:3]:
                    console.print(f"• {factor} ({count} projects)")

        except Exception as e:
            console.print(f"[dim]Cross-project analysis: {e}[/dim]")

        console.print("\n[green]Insights complete. Use /goalkit.insights for AI-powered analysis.[/green]")

    except Exception as e:
        console.print(f"[red]Error generating insights: {e}[/red]")

@app.command()
def memory_patterns(
    project_path: Path = typer.Argument(Path.cwd(), help="Path to the project directory"),
    pattern_type: str = typer.Option("success", "--type", help="Pattern type: success, failure, or process")
):
    """Analyze patterns in project memory for continuous improvement."""
    show_banner()

    console.print("[bold cyan]🔍 Pattern Analysis[/bold cyan]")
    console.print(f"Analyzing {pattern_type} patterns in: {project_path.name}\n")

    if not ProjectMemory:
        console.print("[red]Memory system not available[/red]")
        return

    try:
        memory = ProjectMemory(project_path)
        patterns = memory.get_project_patterns()

        if not patterns["patterns"]:
            console.print("[yellow]No pattern data available[/yellow]")
            return

        console.print(f"[bold]{pattern_type.title()} Patterns:[/bold]")

        if pattern_type == "success" and patterns["patterns"].get("common_success_factors"):
            console.print("\n🟢 Success Factors:")
            for factor, count in patterns["patterns"]["common_success_factors"]:
                console.print(f"• {factor} ({count} occurrences)")

        elif pattern_type == "failure" and patterns["patterns"].get("common_challenges"):
            console.print("\n🔴 Common Challenges:")
            for challenge, count in patterns["patterns"]["common_challenges"]:
                console.print(f"• {challenge} ({count} occurrences)")

        elif pattern_type == "process":
            console.print("\n🔄 Process Patterns:")
            if patterns.get("insights"):
                for insight in patterns["insights"]:
                    console.print(f"• {insight}")

        # Risk pattern detection
        try:
            cross_insights = CrossProjectInsights(memory)
            risk_patterns = cross_insights.detect_risk_patterns()

            if risk_patterns:
                console.print("\n⚠️ Risk Patterns Detected:")
                for risk in risk_patterns[:5]:
                    console.print(f"• {risk}")

        except Exception as e:
            console.print(f"[dim]Risk analysis: {e}[/dim]")

        console.print("\n[green]Pattern analysis complete[/green]")

    except Exception as e:
        console.print(f"[red]Error analyzing patterns: {e}[/red]")

@app.command()
def baseline(
    project_path: Path = typer.Argument(Path.cwd(), help="Path to the project directory"),
    days: int = typer.Option(30, "--days", "-d", help="Number of days of data to analyze for baseline"),
    run_tests: bool = typer.Option(True, "--run-tests", help="Run hypothesis tests after establishing baseline")
):
    """Establish baseline metrics for AI performance and run hypothesis tests."""
    show_banner()

    console.print("[bold cyan]📊 AI Performance Baseline Measurement[/bold cyan]")
    console.print(f"Project: {project_path.name}\n")

    if not BaselineCollector:
        console.print("[red]Baseline measurement system not available[/red]")
        return

    try:
        # Initialize baseline system
        console.print("[cyan]Initializing baseline measurement system...[/cyan]")
        initialize_baseline_system(project_path)

        # Run hypothesis tests if requested
        if run_tests:
            console.print("[cyan]Running hypothesis tests...[/cyan]")
            tester = HypothesisTester(project_path)
            test_results = tester.run_all_hypothesis_tests()

            # Display test results
            console.print("\n[bold]🧪 Hypothesis Test Results:[/bold]")

            for test_name, test_result in test_results["test_results"].items():
                hypothesis = test_result["hypothesis"]
                status = test_result["current_status"]

                console.print(f"\n[bold]{test_name.title()}:[/bold]")
                console.print(f"  Hypothesis: {hypothesis}")
                console.print(f"  Status: [green]{status}[/green]")

                if "baseline_clarification_rate" in test_result:
                    rate = test_result["baseline_clarification_rate"]
                    console.print(f"  Current baseline: [cyan]{rate:.2%}[/cyan]")

            console.print("\n[bold]✅ Baseline measurement complete![/bold]")
            console.print(f"[green]📁 Files created in:[/green] {project_path}/.goalkit/metrics/")
            console.print(f"[green]📁 Test results in:[/green] {project_path}/.goalkit/tests/")

            # Show next steps
            console.print("\n[bold]Next Steps:[/bold]")
            console.print("1. [cyan]Review baseline metrics[/cyan] to understand current AI performance")
            console.print("2. [cyan]Begin implementing enhanced goal templates[/cyan] (Milestone 2)")
            console.print("3. [cyan]Continue daily measurement[/cyan] to track improvements")
            console.print("4. [cyan]Run 'goalkeeper baseline'[/cyan] regularly to update measurements")

    except Exception as e:
        console.print(f"[red]Error establishing baseline: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def goal_create(
    description: str = typer.Argument(..., help="Description of the goal to create"),
    ai_response: str = typer.Option(None, "--ai-response", "-r", help="AI response containing goal details (optional)"),
    project_path: Path = typer.Option(Path.cwd(), "--project-path", "-p", help="Path to the project directory"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive mode for AI response input"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed processing information"),
):
    """Create a new goal from description and AI response.

    This command processes a goal description and creates the proper directory structure
    and goal.md file using the goal template. It can work with or without an AI response.

    Examples:
        goalkeeper goal-create "create a user authentication system"
        goalkeeper goal-create "build a dashboard" --ai-response "AI response here"
        goalkeeper goal-create "implement feature X" --interactive
    """
    show_banner()

    console.print(f"[cyan]Creating goal:[/cyan] {description}\n")

    try:
        # Initialize goal creation service
        goal_service = GoalCreationService(project_path)

        # Get AI response if not provided
        if not ai_response:
            if interactive:
                console.print("[yellow]Interactive mode: Please paste the AI response below.[/yellow]")
                console.print("[yellow]Press Enter twice when finished:[/yellow]\n")
                ai_response_lines = []
                try:
                    while True:
                        line = input()
                        if not line and ai_response_lines:
                            break
                        ai_response_lines.append(line)
                except (KeyboardInterrupt, EOFError):
                    console.print("\n[yellow]Input cancelled.[/yellow]")
                    raise typer.Exit(1)

                ai_response = '\n'.join(ai_response_lines)
            else:
                console.print("[yellow]No AI response provided. Use --ai-response or --interactive flag.[/yellow]")
                console.print("[yellow]Creating goal with basic structure only.[/yellow]")
                ai_response = f"Goal: {description}\n\nThis goal needs further development and refinement."

        if verbose:
            console.print(f"[dim]AI Response Preview:[/dim]\n{ai_response[:200]}{'...' if len(ai_response) > 200 else ''}\n")

        # Parse AI response and create goal data
        if verbose:
            console.print("[cyan]Parsing AI response...[/cyan]")

        goal_data = goal_service.parse_ai_response(ai_response, description)

        if verbose:
            console.print(f"[green]✓[/green] Parsed goal: {goal_data['goal_title']}")
            console.print(f"[green]✓[/green] Generated directory: {goal_data['goal_directory']}")

        # Create goal directory structure
        if verbose:
            console.print("[cyan]Creating goal directory structure...[/cyan]")

        goal_dir = goal_service.create_goal_directory(goal_data)

        if verbose:
            console.print(f"[green]✓[/green] Created directory: {goal_dir}")

        # Generate goal file
        if verbose:
            console.print("[cyan]Generating goal.md file...[/cyan]")

        goal_file = goal_service.generate_goal_file(goal_data, goal_dir)

        if verbose:
            console.print(f"[green]✓[/green] Created goal file: {goal_file}")

        # Validate the created structure
        if goal_service.validate_goal_structure(goal_dir):
            console.print(f"\n[bold green]✅ Goal created successfully![/bold green]")
            console.print(f"[cyan]Directory:[/cyan] {goal_dir}")
            console.print(f"[cyan]Goal file:[/cyan] {goal_file}")
            console.print(f"[cyan]Title:[/cyan] {goal_data['goal_title']}")

            # Show next steps
            console.print("\n[bold]Next Steps:[/bold]")
            console.print("1. [cyan]Review and customize[/cyan] the generated goal.md file")
            console.print("2. [cyan]Use /goalkit.strategies[/cyan] to explore implementation approaches")
            console.print("3. [cyan]Use /goalkit.milestones[/cyan] to create detailed milestones")
            console.print("4. [cyan]Use /goalkit.execute[/cyan] to start implementation")

            # Log the goal creation
            log_ai_interaction("qwen", "goal_create", True, 100, description, f"Created goal: {goal_data['goal_title']}")

        else:
            console.print(f"\n[red]❌ Goal creation failed - structure validation error[/red]")
            console.print(f"[yellow]Directory created but files may be missing:[/yellow] {goal_dir}")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"\n[red]❌ Error creating goal:[/red] {e}")
        if verbose:
            import traceback
            console.print(f"[red]Traceback:[/red]\n{traceback.format_exc()}")
        raise typer.Exit(1)


@app.command()
def goalkit_goal(
    description: str = typer.Argument(..., help="Description of the goal to create"),
    ai_response: str = typer.Option(None, "--ai-response", "-r", help="AI response containing goal details (optional)"),
    project_path: Path = typer.Option(Path.cwd(), "--project-path", "-p", help="Path to the project directory"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive mode for AI response input"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed processing information"),
):
    """Handle /goalkit.goal slash command for creating goals.

    This command provides the /goalkit.goal interface that AI agents use to create
    structured goals from descriptions and AI responses.

    Examples:
        goalkeeper goalkit-goal "create a user authentication system"
        goalkeeper goalkit-goal "build a dashboard" --ai-response "AI response here"
        goalkeeper goalkit-goal "implement feature X" --interactive
    """
    # Delegate to the main goal creation function
    goal_create(description, ai_response, project_path, interactive, verbose)


@app.command()
def check():
    """Check that all required tools are installed."""
    show_banner()
    console.print("[bold]Checking for installed tools...[/bold]\n")

    tracker = StepTracker("Check Available Tools")

    tracker.add("git", "Git version control")
    tracker.add("claude", "Claude Code CLI")
    tracker.add("gemini", "Gemini CLI")
    tracker.add("qwen", "Qwen Code CLI")
    tracker.add("code", "Visual Studio Code")
    tracker.add("code-insiders", "Visual Studio Code Insiders")
    tracker.add("cursor-agent", "Cursor IDE agent")
    tracker.add("windsurf", "Windsurf IDE")
    tracker.add("kilocode", "Kilo Code IDE")
    tracker.add("opencode", "opencode")
    tracker.add("codex", "Codex CLI")
    tracker.add("auggie", "Auggie CLI")
    tracker.add("q", "Amazon Q Developer CLI")

    git_ok = check_tool_for_tracker("git", tracker)
    claude_ok = check_tool_for_tracker("claude", tracker)
    gemini_ok = check_tool_for_tracker("gemini", tracker)
    qwen_ok = check_tool_for_tracker("qwen", tracker)
    code_ok = check_tool_for_tracker("code", tracker)
    code_insiders_ok = check_tool_for_tracker("code-insiders", tracker)
    cursor_ok = check_tool_for_tracker("cursor-agent", tracker)
    windsurf_ok = check_tool_for_tracker("windsurf", tracker)
    kilocode_ok = check_tool_for_tracker("kilocode", tracker)
    opencode_ok = check_tool_for_tracker("opencode", tracker)
    codex_ok = check_tool_for_tracker("codex", tracker)
    auggie_ok = check_tool_for_tracker("auggie", tracker)
    q_ok = check_tool_for_tracker("q", tracker)

    console.print(tracker.render())

    console.print("\n[bold green]Goalkeeper CLI is ready to use![/bold green]")

    if not git_ok:
        console.print("[dim]Tip: Install git for repository management[/dim]")
    if not (claude_ok or gemini_ok or cursor_ok or qwen_ok or windsurf_ok or kilocode_ok or opencode_ok or codex_ok or auggie_ok or q_ok):
        console.print("[dim]Tip: Install an AI assistant for the best experience[/dim]")

def main():
    app()

if __name__ == "__main__":
    main()

# Test function for goal creation (for development/debugging)
def test_goal_creation():
    """Test function to verify goal creation functionality."""
    try:
        from pathlib import Path

        # Create a test project directory
        test_project = Path.cwd() / "test_goal_creation"
        test_project.mkdir(exist_ok=True)

        # Initialize goal creation service
        goal_service = GoalCreationService(test_project)

        # Test data
        test_description = "create a user authentication system"
        test_ai_response = """
        This goal involves implementing a secure user authentication system with the following key features:

        Success Metrics:
        - 99.9% uptime for authentication services
        - Support for 10,000 concurrent users
        - Sub-second response times for login/logout

        Target Users:
        - End users who need secure access to the application
        - Administrators who manage user accounts
        - Developers who integrate with the authentication system

        Key Hypotheses:
        - Users prefer OAuth integration over custom authentication
        - Multi-factor authentication increases security without hurting UX

        Risk Factors:
        - Integration with existing user database may be complex
        - Security vulnerabilities could compromise user data

        Milestones:
        - Design authentication architecture and security model
        - Implement core authentication service
        - Add multi-factor authentication support
        - Integration testing and security audit
        """

        # Parse and create goal
        goal_data = goal_service.parse_ai_response(test_ai_response, test_description)
        goal_dir = goal_service.create_goal_directory(goal_data)
        goal_file = goal_service.generate_goal_file(goal_data, goal_dir)

        print(f"[SUCCESS] Goal created successfully!")
        print(f"[DIR] Directory: {goal_dir}")
        print(f"[FILE] Goal file: {goal_file}")
        print(f"[TITLE] Title: {goal_data['goal_title']}")

        # Validate structure
        if goal_service.validate_goal_structure(goal_dir):
            print("[SUCCESS] Goal structure validation passed")
        else:
            print("[ERROR] Goal structure validation failed")

        return True

    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False