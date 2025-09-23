"""
Predictive analytics engine for goal-dev-spec
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import random
import time

@dataclass
class HistoricalProject:
    project_id: str
    completion_time: int  # in days
    complexity_score: float
    revision_count: int
    keywords: List[str]

class PredictiveAnalyticsEngine:
    """Engine for predictive analytics in goal-dev-spec"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.analytics_path = project_path / ".goal" / "analytics"
        self.analytics_path.mkdir(exist_ok=True)
        self.historical_data_file = self.analytics_path / "historical_data.json"
        self.model_file = self.analytics_path / "forecasting_model.json"
        
        # Load historical data
        self.historical_projects = self._load_historical_data()
        
        # Initialize models (simplified for prototype)
        self._train_models()
    
    def _load_historical_data(self) -> List[HistoricalProject]:
        """Load historical project data"""
        if not self.historical_data_file.exists():
            # Create sample data for demonstration
            sample_data = [
                {
                    "project_id": "auth-impl-001",
                    "completion_time": 14,
                    "complexity_score": 7.2,
                    "revision_count": 3,
                    "keywords": ["authentication", "security", "login"]
                },
                {
                    "project_id": "auth-impl-002",
                    "completion_time": 18,
                    "complexity_score": 8.1,
                    "revision_count": 5,
                    "keywords": ["authentication", "security", "oauth", "compliance"]
                },
                {
                    "project_id": "payment-impl-001",
                    "completion_time": 22,
                    "complexity_score": 9.3,
                    "revision_count": 4,
                    "keywords": ["payment", "security", "pci", "integration"]
                }
            ]
            with open(self.historical_data_file, 'w') as f:
                json.dump(sample_data, f)
            return [HistoricalProject(**item) for item in sample_data]
        
        with open(self.historical_data_file, 'r') as f:
            data = json.load(f)
        return [HistoricalProject(**item) for item in data]
    
    def _train_models(self):
        """Train predictive models (simplified for prototype)"""
        # In a real implementation, this would train ML models
        # For now, we'll just use the historical data directly
        pass
    
    def analyze_goal_complexity(self, goal_data: Dict) -> Dict:
        """Analyze the complexity of a goal"""
        description = goal_data.get('description', '')
        objectives = goal_data.get('objectives', [])
        success_criteria = goal_data.get('success_criteria', [])
        dependencies = goal_data.get('dependencies', [])
        
        # Simple keyword-based complexity analysis
        security_keywords = ['security', 'authentication', 'authorization', 'encryption', 'compliance']
        integration_keywords = ['integration', 'api', 'third-party', 'external']
        complexity_keywords = ['real-time', 'scalable', 'performance', 'concurrent']
        
        # Count keywords
        text_to_analyze = f"{description} {' '.join(objectives)} {' '.join(success_criteria)}"
        security_score = sum(1 for keyword in security_keywords if keyword in text_to_analyze.lower())
        integration_score = sum(1 for keyword in integration_keywords if keyword in text_to_analyze.lower())
        complexity_score = sum(1 for keyword in complexity_keywords if keyword in text_to_analyze.lower())
        
        # Dependency complexity
        dependency_score = len(dependencies) * 0.5
        
        # Total complexity score (0-10)
        total_score = min(10.0, (security_score + integration_score + complexity_score + dependency_score) * 1.5)
        
        return {
            'security_factors': security_score,
            'integration_factors': integration_score,
            'complexity_factors': complexity_score,
            'dependency_factors': dependency_score,
            'total_score': round(total_score, 2)
        }
    
    def estimate_completion_time(self, goal_data: Dict) -> int:
        """Estimate completion time for a goal"""
        if not self.historical_projects:
            return 15  # Default estimate
        
        # Simple approach: find similar projects and average their completion times
        complexity = self.analyze_goal_complexity(goal_data)
        goal_complexity = complexity['total_score']
        
        # Find projects with similar complexity (within 2 points)
        similar_projects = [
            p for p in self.historical_projects 
            if abs(p.complexity_score - goal_complexity) <= 2.0
        ]
        
        if similar_projects:
            # Average completion time of similar projects
            avg_time = sum(p.completion_time for p in similar_projects) / len(similar_projects)
            return max(1, int(round(avg_time)))
        else:
            # Fallback to overall average
            avg_time = sum(p.completion_time for p in self.historical_projects) / len(self.historical_projects)
            return max(1, int(round(avg_time)))
    
    def identify_risk_factors(self, goal_data: Dict) -> List[str]:
        """Identify potential risk factors for a goal"""
        risks = []
        description = goal_data.get('description', '').lower()
        dependencies = goal_data.get('dependencies', [])
        
        # Security-related risks
        if any(keyword in description for keyword in ['security', 'authentication', 'authorization']):
            risks.append("security_compliance")
        
        # Integration risks
        if any(keyword in description for keyword in ['integration', 'api', 'third-party']):
            risks.append("integration_complexity")
        
        # Dependency risks
        if dependencies:
            risks.append("dependency_management")
        
        # Performance risks
        if any(keyword in description for keyword in ['performance', 'scalable', 'real-time']):
            risks.append("performance_optimization")
        
        # Compliance risks
        if any(keyword in description for keyword in ['compliance', 'regulation', 'gdpr', 'hippa']):
            risks.append("regulatory_compliance")
        
        return risks
    
    def recommend_resources(self, goal_data: Dict) -> List[Dict]:
        """Recommend resources for a goal"""
        complexity = self.analyze_goal_complexity(goal_data)
        total_score = complexity['total_score']
        
        recommendations = []
        
        # Backend developers
        if total_score > 5:
            recommendations.append({
                'role': 'senior_backend_developer',
                'count': 2,
                'reason': 'High complexity project requires experienced developers'
            })
        else:
            recommendations.append({
                'role': 'backend_developer',
                'count': 1,
                'reason': 'Standard complexity project'
            })
        
        # Security specialist for security-related projects
        if complexity['security_factors'] > 0:
            recommendations.append({
                'role': 'security_specialist',
                'count': 1,
                'reason': 'Security factors identified in project scope'
            })
        
        # QA engineer for complex projects
        if total_score > 7:
            recommendations.append({
                'role': 'qa_engineer',
                'count': 1,
                'reason': 'High complexity requires dedicated testing'
            })
        
        return recommendations
    
    def enhance_goal_with_analytics(self, goal_data: Dict) -> Dict:
        """Enhance goal data with predictive analytics"""
        enhanced_goal = goal_data.copy()
        
        # Add analytics data
        enhanced_goal['metadata'] = enhanced_goal.get('metadata', {})
        enhanced_goal['metadata']['predictive_analytics'] = {
            'complexity_analysis': self.analyze_goal_complexity(goal_data),
            'estimated_completion_days': self.estimate_completion_time(goal_data),
            'risk_factors': self.identify_risk_factors(goal_data),
            'resource_recommendations': self.recommend_resources(goal_data),
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return enhanced_goal

# Progress tracking with analytics
class ProgressTracker:
    """Enhanced progress tracker with predictive analytics"""
    
    def __init__(self, title: str, total_steps: int = 0):
        self.title = title
        self.total_steps = total_steps
        self.current_step = 0
        self.start_time = time.time()
        self.step_times = []  # Track time for each step
        self.estimated_completion_time = None
        self.notifications = []
        
    def start_step(self, step_name: str):
        """Start a new step"""
        self.current_step_name = step_name
        self.step_start_time = time.time()
        
    def complete_step(self):
        """Complete the current step"""
        if hasattr(self, 'step_start_time'):
            step_duration = time.time() - self.step_start_time
            self.step_times.append(step_duration)
            
        self.current_step += 1
        
        # Update estimated completion time
        if self.step_times and self.total_steps > 0:
            avg_time_per_step = sum(self.step_times) / len(self.step_times)
            remaining_steps = self.total_steps - self.current_step
            self.estimated_completion_time = avg_time_per_step * remaining_steps
    
    def get_progress_percentage(self) -> float:
        """Get progress percentage"""
        if self.total_steps <= 0:
            return 0.0
        return min(100.0, (self.current_step / self.total_steps) * 100.0)
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time in seconds"""
        return time.time() - self.start_time
    
    def get_estimated_remaining_time(self) -> Optional[float]:
        """Get estimated remaining time in seconds"""
        return self.estimated_completion_time
    
    def get_eta(self) -> Optional[datetime]:
        """Get estimated time of arrival"""
        if self.estimated_completion_time is not None:
            return datetime.now() + timedelta(seconds=self.estimated_completion_time)
        return None
    
    def add_notification(self, message: str, level: str = "info"):
        """Add a notification"""
        self.notifications.append({
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'level': level
        })
    
    def get_notifications(self) -> List[Dict]:
        """Get all notifications"""
        return self.notifications

# CLI Commands for Analytics
import typer
from rich.console import Console
from rich.table import Table

console = Console()

def analytics_cli():
    """CLI commands for predictive analytics"""
    app = typer.Typer()
    
    @app.command()
    def analyze_goal(goal_id: str):
        """Analyze a goal with predictive analytics"""
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
            
            # Load goal
            goal_file = project_path / ".goal" / "goals" / goal_id / "goal.yaml"
            if not goal_file.exists():
                console.print(f"[red]Error:[/red] Goal {goal_id} not found")
                return
            
            with open(goal_file, 'r') as f:
                goal_data = yaml.safe_load(f)
            
            # Analyze with engine
            engine = PredictiveAnalyticsEngine(project_path)
            enhanced_goal = engine.enhance_goal_with_analytics(goal_data)
            
            # Display results
            analytics = enhanced_goal['metadata']['predictive_analytics']
            
            console.print(f"[bold]Predictive Analytics for Goal: {goal_data['title']}[/bold]\n")
            
            # Complexity Analysis
            console.print("[cyan]Complexity Analysis:[/cyan]")
            complexity = analytics['complexity_analysis']
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Factor", style="dim")
            table.add_column("Score", justify="right")
            table.add_row("Security Factors", str(complexity['security_factors']))
            table.add_row("Integration Factors", str(complexity['integration_factors']))
            table.add_row("Complexity Factors", str(complexity['complexity_factors']))
            table.add_row("Dependency Factors", str(complexity['dependency_factors']))
            table.add_row("Total Score", f"{complexity['total_score']}/10")
            console.print(table)
            
            # Time Estimation
            console.print(f"\n[cyan]Estimated Completion:[/cyan] {analytics['estimated_completion_days']} days")
            
            # Risk Factors
            if analytics['risk_factors']:
                console.print("\n[cyan]Identified Risk Factors:[/cyan]")
                for risk in analytics['risk_factors']:
                    console.print(f"  • {risk}")
            else:
                console.print("\n[cyan]Risk Factors:[/cyan] None identified")
            
            # Resource Recommendations
            console.print("\n[cyan]Resource Recommendations:[/cyan]")
            for rec in analytics['resource_recommendations']:
                console.print(f"  • {rec['count']}x {rec['role']}: {rec['reason']}")
                
            # Update goal file with analytics
            with open(goal_file, 'w') as f:
                yaml.dump(enhanced_goal, f, default_flow_style=False, sort_keys=False)
            
            console.print("\n[green]✓[/green] Goal enhanced with predictive analytics")
                
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    return app

# Integration with main CLI
def integrate_analytics_with_main_cli(main_app):
    """Integrate analytics commands with main CLI"""
    analytics_app = analytics_cli()
    main_app.add_typer(analytics_app, name="analytics")
    return main_app