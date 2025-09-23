"""
Performance monitoring module for the goal-dev-spec system.
Provides performance standards, monitoring, and optimization recommendations.
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from collections import defaultdict

class PerformanceMonitor:
    """Monitors performance metrics and provides optimization recommendations."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.performance_path = project_path / ".goal" / "performance"
        self.performance_path.mkdir(exist_ok=True)
        
        # Load performance standards
        self.standards = self._load_performance_standards()
        
        # Load metrics history
        self.metrics_history = self._load_metrics_history()
    
    def _load_performance_standards(self) -> Dict:
        """Load performance standards."""
        return {
            "goal_completion": {
                "name": "Goal Completion Time",
                "target": 14,  # days
                "unit": "days",
                "threshold": 21,  # days - beyond this is considered slow
                "optimization_tips": [
                    "Break down complex goals into smaller, manageable tasks",
                    "Ensure clear success criteria to avoid rework",
                    "Use templates to speed up specification creation"
                ]
            },
            "specification_quality": {
                "name": "Specification Quality Score",
                "target": 0.85,  # 85% quality
                "unit": "score",
                "threshold": 0.70,  # below this is considered low quality
                "optimization_tips": [
                    "Include more detailed acceptance criteria",
                    "Use examples to clarify ambiguous requirements",
                    "Review specifications with stakeholders before finalizing"
                ]
            },
            "review_cycle_time": {
                "name": "Review Cycle Time",
                "target": 2,  # days
                "unit": "days",
                "threshold": 5,  # days - beyond this is considered slow
                "optimization_tips": [
                    "Set clear review deadlines",
                    "Use automated review tools where possible",
                    "Ensure reviewers have all necessary context"
                ]
            },
            "deployment_frequency": {
                "name": "Deployment Frequency",
                "target": 1,  # per week
                "unit": "deployments/week",
                "threshold": 0.2,  # per week - below this is considered infrequent
                "optimization_tips": [
                    "Implement continuous integration/deployment",
                    "Break features into smaller deployable units",
                    "Automate testing to enable faster deployments"
                ]
            }
        }
    
    def _load_metrics_history(self) -> Dict:
        """Load historical metrics data."""
        metrics_file = self.performance_path / "metrics_history.json"
        if metrics_file.exists():
            try:
                with open(metrics_file, 'r') as f:
                    return json.load(f)
            except:
                return defaultdict(list)
        return defaultdict(list)
    
    def record_metric(self, metric_name: str, value: float, context: Dict = None):
        """Record a performance metric."""
        if metric_name not in self.standards:
            raise ValueError(f"Unknown metric: {metric_name}")
        
        metric_record = {
            "timestamp": datetime.now().isoformat(),
            "value": value,
            "context": context or {}
        }
        
        self.metrics_history[metric_name].append(metric_record)
        
        # Save to file
        metrics_file = self.performance_path / "metrics_history.json"
        with open(metrics_file, 'w') as f:
            json.dump(dict(self.metrics_history), f, indent=2)
    
    def get_metric_stats(self, metric_name: str) -> Dict:
        """Get statistics for a specific metric."""
        if metric_name not in self.metrics_history:
            return {"error": f"No data for metric: {metric_name}"}
        
        values = [record["value"] for record in self.metrics_history[metric_name]]
        if not values:
            return {"error": f"No values for metric: {metric_name}"}
        
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "average": sum(values) / len(values),
            "latest": values[-1] if values else None
        }
    
    def assess_performance(self, metric_name: str, value: float) -> Dict:
        """Assess performance against standards."""
        if metric_name not in self.standards:
            return {"error": f"Unknown metric: {metric_name}"}
        
        standard = self.standards[metric_name]
        target = standard["target"]
        threshold = standard["threshold"]
        
        assessment = {
            "metric": metric_name,
            "name": standard["name"],
            "value": value,
            "target": target,
            "threshold": threshold,
            "unit": standard["unit"],
            "status": "unknown"
        }
        
        # Determine status based on the metric type (higher is better vs lower is better)
        if metric_name in ["specification_quality"]:  # Higher is better
            if value >= target:
                assessment["status"] = "excellent"
            elif value >= threshold:
                assessment["status"] = "acceptable"
            else:
                assessment["status"] = "poor"
        else:  # Lower is better (time-based metrics)
            if value <= target:
                assessment["status"] = "excellent"
            elif value <= threshold:
                assessment["status"] = "acceptable"
            else:
                assessment["status"] = "poor"
        
        return assessment
    
    def get_performance_recommendations(self, metric_name: str, value: float) -> List[str]:
        """Get optimization recommendations for a metric."""
        if metric_name not in self.standards:
            return [f"Unknown metric: {metric_name}"]
        
        standard = self.standards[metric_name]
        target = standard["target"]
        threshold = standard["threshold"]
        
        # Only provide recommendations if performance is below target
        if metric_name in ["specification_quality"]:  # Higher is better
            if value >= target:
                return ["Performance is excellent - no recommendations needed"]
        else:  # Lower is better
            if value <= target:
                return ["Performance is excellent - no recommendations needed"]
        
        return standard.get("optimization_tips", ["No specific recommendations available"])
    
    def generate_performance_report(self) -> str:
        """Generate a performance report in markdown format."""
        report = f"# Performance Report\n\n"
        report += f"Generated: {datetime.now().isoformat()}\n\n"
        report += f"Project: {self.project_path}\n\n"
        
        # Overall performance summary
        report += "## Performance Summary\n\n"
        
        for metric_name in self.standards:
            standard = self.standards[metric_name]
            stats = self.get_metric_stats(metric_name)
            
            if "error" in stats:
                report += f"### {standard['name']}\n\n"
                report += f"Status: ⚠️ No data available\n\n"
                continue
            
            latest_value = stats["latest"]
            assessment = self.assess_performance(metric_name, latest_value)
            
            report += f"### {standard['name']}\n\n"
            report += f"Latest Value: {latest_value:.2f} {standard['unit']}\n"
            report += f"Target: {target} {standard['unit']}\n"
            report += f"Threshold: {threshold} {standard['unit']}\n\n"
            
            if assessment["status"] == "excellent":
                report += f"Status: ✅ EXCELLENT\n\n"
            elif assessment["status"] == "acceptable":
                report += f"Status: ⚠️ ACCEPTABLE\n\n"
            else:
                report += f"Status: ❌ POOR\n\n"
            
            # Add recommendations if performance is not excellent
            if assessment["status"] != "excellent":
                recommendations = self.get_performance_recommendations(metric_name, latest_value)
                report += "Recommendations:\n"
                for rec in recommendations:
                    report += f"- {rec}\n"
                report += "\n"
            
            # Add historical trend
            if stats["count"] > 1:
                report += f"Historical Data:\n"
                report += f"- Average: {stats['average']:.2f} {standard['unit']}\n"
                report += f"- Min: {stats['min']:.2f} {standard['unit']}\n"
                report += f"- Max: {stats['max']:.2f} {standard['unit']}\n"
                report += f"- Count: {stats['count']} measurements\n\n"
        
        return report
    
    def get_velocity_metrics(self, project_data: Dict) -> Dict:
        """Calculate velocity metrics for the project."""
        metrics = {
            "goals_completed": 0,
            "goals_in_progress": 0,
            "avg_completion_time": 0,
            "completion_rate": 0
        }
        
        # Calculate completion rate and velocity
        if "goals" in project_data:
            completed_goals = []
            in_progress_goals = []
            
            for goal in project_data["goals"]:
                if goal.get("status") == "completed":
                    completed_goals.append(goal)
                elif goal.get("status") == "in_progress":
                    in_progress_goals.append(goal)
            
            metrics["goals_completed"] = len(completed_goals)
            metrics["goals_in_progress"] = len(in_progress_goals)
            
            # Calculate average completion time
            completion_times = []
            for goal in completed_goals:
                if "created_at" in goal and "updated_at" in goal:
                    try:
                        from datetime import datetime
                        created = datetime.fromisoformat(goal["created_at"])
                        completed = datetime.fromisoformat(goal["updated_at"])
                        completion_times.append((completed - created).days)
                    except:
                        pass
            
            if completion_times:
                metrics["avg_completion_time"] = sum(completion_times) / len(completion_times)
            
            # Calculate completion rate (goals per week)
            if completion_times:
                # Simplified calculation - in reality, we would consider the time period
                metrics["completion_rate"] = len(completed_goals) / 4  # Assuming 4 weeks of data
        
        return metrics

# Example usage
if __name__ == "__main__":
    # This is just for testing purposes
    monitor = PerformanceMonitor(Path("."))
    print("PerformanceMonitor initialized")