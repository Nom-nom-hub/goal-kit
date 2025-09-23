"""
Real-time Quality Monitoring for goal-dev-spec
Provides continuous monitoring of quality metrics and immediate feedback.
"""

import json
from pathlib import Path
from typing import Dict, List, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import threading
import time
from collections import defaultdict, deque
import hashlib

# Import our enhanced quality assurance module
from .enhanced_quality_assurance import EnhancedQualityAssurance, QualityMetrics


@dataclass
class MonitoringEvent:
    """Data class for monitoring events"""
    id: str
    timestamp: str
    event_type: str  # quality_change, threshold_breach, artifact_update, etc.
    severity: int  # 1-5, 5 being critical
    description: str
    details: Dict
    related_artifacts: List[str]


@dataclass
class ThresholdRule:
    """Data class for threshold rules"""
    metric: str
    operator: str  # gt, lt, eq, gte, lte
    threshold: float
    severity: int
    action: str  # alert, notify, block, etc.
    enabled: bool = True


class RealTimeQualityMonitor:
    """Real-time quality monitoring system"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.monitoring_path = project_path / ".goal" / "monitoring"
        self.monitoring_path.mkdir(exist_ok=True)
        
        # Initialize enhanced quality assurance system
        self.qa_system = EnhancedQualityAssurance(project_path)
        
        # Load monitoring configuration
        self.config = self._load_monitoring_config()
        
        # Initialize thresholds
        self.thresholds = self._load_thresholds()
        
        # Event history
        self.event_history = deque(maxlen=1000)  # Keep last 1000 events
        
        # Monitoring state
        self.is_monitoring = False
        self.monitoring_thread = None
        self.last_metrics = None
        
        # Callbacks for events
        self.event_callbacks = []
        
        # Artifact tracking
        self.artifact_hashes = self._load_artifact_hashes()
    
    def _load_monitoring_config(self) -> Dict:
        """Load monitoring configuration"""
        config_file = self.monitoring_path / "monitoring_config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        
        # Default configuration
        default_config = {
            "enabled": True,
            "check_interval_seconds": 300,  # 5 minutes
            "artifact_scan_interval_seconds": 60,  # 1 minute
            "metrics_to_monitor": [
                "overall_score",
                "clarity_score",
                "completeness_score",
                "consistency_score",
                "testability_score",
                "maintainability_score",
                "security_score"
            ],
            "enable_file_watching": True,
            "enable_performance_monitoring": True,
            "enable_security_scanning": True
        }
        
        # Save default configuration
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    def _load_thresholds(self) -> List[ThresholdRule]:
        """Load threshold rules"""
        thresholds_file = self.monitoring_path / "thresholds.json"
        if thresholds_file.exists():
            try:
                with open(thresholds_file, 'r') as f:
                    thresholds_data = json.load(f)
                return [ThresholdRule(**rule) for rule in thresholds_data]
            except json.JSONDecodeError:
                pass
        
        # Default thresholds
        default_thresholds = [
            ThresholdRule("overall_score", "lt", 0.6, 4, "alert"),
            ThresholdRule("clarity_score", "lt", 0.5, 5, "alert"),
            ThresholdRule("consistency_score", "lt", 0.5, 5, "alert"),
            ThresholdRule("security_score", "lt", 0.7, 3, "alert"),
            ThresholdRule("testability_score", "lt", 0.6, 2, "notify")
        ]
        
        # Save default thresholds
        with open(thresholds_file, 'w') as f:
            json.dump([asdict(rule) for rule in default_thresholds], f, indent=2)
        
        return default_thresholds
    
    def _load_artifact_hashes(self) -> Dict:
        """Load artifact hashes for change detection"""
        hashes_file = self.monitoring_path / "artifact_hashes.json"
        if hashes_file.exists():
            try:
                with open(hashes_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def _save_artifact_hashes(self):
        """Save artifact hashes"""
        hashes_file = self.monitoring_path / "artifact_hashes.json"
        with open(hashes_file, 'w') as f:
            json.dump(self.artifact_hashes, f, indent=2)
    
    def start_monitoring(self):
        """Start real-time monitoring"""
        if self.is_monitoring:
            return {"status": "already_running", "message": "Monitoring is already running"}
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        return {"status": "started", "message": "Real-time monitoring started"}
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        if not self.is_monitoring:
            return {"status": "not_running", "message": "Monitoring is not running"}
        
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)  # Wait up to 5 seconds
        
        return {"status": "stopped", "message": "Real-time monitoring stopped"}
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        last_artifact_scan = time.time()
        artifact_scan_interval = self.config.get("artifact_scan_interval_seconds", 60)
        
        while self.is_monitoring:
            try:
                current_time = time.time()
                
                # Check for artifact changes
                if current_time - last_artifact_scan >= artifact_scan_interval:
                    self._scan_for_artifact_changes()
                    last_artifact_scan = current_time
                
                # Perform quality assessment
                self._perform_quality_assessment()
                
                # Wait for next check
                check_interval = self.config.get("check_interval_seconds", 300)
                time.sleep(min(check_interval, 60))  # Check at least every minute
                
            except Exception as e:
                # Log error but continue monitoring
                self._record_event(
                    event_type="monitoring_error",
                    severity=3,
                    description=f"Error in monitoring loop: {str(e)}",
                    details={"error": str(e)}
                )
                time.sleep(60)  # Wait before retrying
    
    def _scan_for_artifact_changes(self):
        """Scan for changes in artifacts"""
        # Find all goal, spec, plan, and task files
        artifact_patterns = [
            ".goal/goals/**/*.yaml",
            ".goal/specs/**/*.yaml",
            ".goal/plans/**/*.yaml",
            ".goal/tasks/**/*.yaml"
        ]
        
        changed_artifacts = []
        
        for pattern in artifact_patterns:
            for file_path in self.project_path.glob(pattern):
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        file_hash = hashlib.md5(content).hexdigest()
                    
                    relative_path = str(file_path.relative_to(self.project_path))
                    
                    if relative_path not in self.artifact_hashes:
                        # New artifact
                        self.artifact_hashes[relative_path] = file_hash
                        changed_artifacts.append({
                            "path": relative_path,
                            "type": "new",
                            "hash": file_hash
                        })
                    elif self.artifact_hashes[relative_path] != file_hash:
                        # Changed artifact
                        old_hash = self.artifact_hashes[relative_path]
                        self.artifact_hashes[relative_path] = file_hash
                        changed_artifacts.append({
                            "path": relative_path,
                            "type": "modified",
                            "old_hash": old_hash,
                            "new_hash": file_hash
                        })
                except Exception as e:
                    self._record_event(
                        event_type="artifact_scan_error",
                        severity=2,
                        description=f"Error scanning artifact {file_path}: {str(e)}",
                        details={"error": str(e), "path": str(file_path)}
                    )
        
        # Save updated hashes
        self._save_artifact_hashes()
        
        # Record events for changed artifacts
        for artifact in changed_artifacts:
            self._record_event(
                event_type="artifact_update",
                severity=1 if artifact["type"] == "new" else 2,
                description=f"Artifact {artifact['type']}: {artifact['path']}",
                details=artifact,
                related_artifacts=[artifact["path"]]
            )
    
    def _perform_quality_assessment(self):
        """Perform quality assessment of the project"""
        try:
            # Load current project data (simplified)
            project_data = self._load_project_data()
            
            # Calculate current metrics
            current_metrics = self.qa_system.calculate_comprehensive_quality_score(project_data)
            
            # Check for significant changes
            if self.last_metrics:
                self._check_for_metric_changes(current_metrics)
            
            # Check thresholds
            self._check_thresholds(current_metrics)
            
            # Update last metrics
            self.last_metrics = current_metrics
            
            # Record successful assessment
            self._record_event(
                event_type="quality_assessment",
                severity=1,
                description="Quality assessment completed successfully",
                details={"metrics": current_metrics}
            )
            
        except Exception as e:
            self._record_event(
                event_type="quality_assessment_error",
                severity=4,
                description=f"Error performing quality assessment: {str(e)}",
                details={"error": str(e)}
            )
    
    def _load_project_data(self) -> Dict:
        """Load current project data"""
        # This would load actual project data
        # For now, we'll return a simplified structure
        return {
            "goals": [],
            "specs": [],
            "plans": [],
            "tasks": []
        }
    
    def _check_for_metric_changes(self, current_metrics: QualityMetrics):
        """Check for significant changes in metrics"""
        if not self.last_metrics:
            return
        
        # Check each metric for significant changes (more than 10% change)
        metrics_to_check = [
            "clarity_score", "completeness_score", "consistency_score",
            "testability_score", "maintainability_score", "security_score", "overall_score"
        ]
        
        for metric in metrics_to_check:
            current_value = getattr(current_metrics, metric, 0)
            last_value = getattr(self.last_metrics, metric, 0)
            
            if last_value != 0:
                change_percent = abs(current_value - last_value) / last_value
                if change_percent > 0.1:  # 10% change
                    self._record_event(
                        event_type="quality_change",
                        severity=2 if change_percent > 0.2 else 1,  # Higher severity for >20% change
                        description=f"Significant change in {metric}: {last_value:.2f} → {current_value:.2f} ({change_percent:.1%})",
                        details={
                            "metric": metric,
                            "previous_value": last_value,
                            "current_value": current_value,
                            "change_percent": change_percent
                        }
                    )
    
    def _check_thresholds(self, current_metrics: QualityMetrics):
        """Check current metrics against thresholds"""
        metrics_dict = asdict(current_metrics)
        
        for threshold in self.thresholds:
            if not threshold.enabled:
                continue
            
            metric_value = metrics_dict.get(threshold.metric)
            if metric_value is None:
                continue
            
            # Evaluate threshold condition
            condition_met = False
            if threshold.operator == "gt" and metric_value > threshold.threshold:
                condition_met = True
            elif threshold.operator == "lt" and metric_value < threshold.threshold:
                condition_met = True
            elif threshold.operator == "eq" and metric_value == threshold.threshold:
                condition_met = True
            elif threshold.operator == "gte" and metric_value >= threshold.threshold:
                condition_met = True
            elif threshold.operator == "lte" and metric_value <= threshold.threshold:
                condition_met = True
            
            if condition_met:
                self._record_event(
                    event_type="threshold_breach",
                    severity=threshold.severity,
                    description=f"Threshold breached: {threshold.metric} {threshold.operator} {threshold.threshold} (current: {metric_value:.2f})",
                    details={
                        "metric": threshold.metric,
                        "operator": threshold.operator,
                        "threshold": threshold.threshold,
                        "current_value": metric_value,
                        "severity": threshold.severity,
                        "action": threshold.action
                    }
                )
                
                # Execute threshold action
                self._execute_threshold_action(threshold, metric_value)
    
    def _execute_threshold_action(self, threshold: ThresholdRule, metric_value: float):
        """Execute action for threshold breach"""
        if threshold.action == "alert":
            # Alert is already recorded as an event
            pass
        elif threshold.action == "notify":
            # Could send notifications via email, Slack, etc.
            pass
        elif threshold.action == "block":
            # Could block certain operations
            pass
    
    def _record_event(self, event_type: str, severity: int, description: str, details: Dict, related_artifacts: List[str] = None):
        """Record a monitoring event"""
        event = MonitoringEvent(
            id=hashlib.md5(f"{event_type}_{datetime.now().isoformat()}".encode()).hexdigest()[:16],
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            severity=severity,
            description=description,
            details=details,
            related_artifacts=related_artifacts or []
        )
        
        self.event_history.append(asdict(event))
        
        # Trigger callbacks
        for callback in self.event_callbacks:
            try:
                callback(event)
            except Exception:
                # Don't let callback errors stop monitoring
                pass
        
        # Save events periodically
        if len(self.event_history) % 10 == 0:
            self._save_events()
    
    def _save_events(self):
        """Save events to file"""
        events_file = self.monitoring_path / "events.json"
        try:
            with open(events_file, 'w') as f:
                json.dump(list(self.event_history), f, indent=2)
        except Exception:
            # Don't let save errors stop monitoring
            pass
    
    def add_event_callback(self, callback: Callable[[MonitoringEvent], None]):
        """Add a callback function for events"""
        self.event_callbacks.append(callback)
    
    def remove_event_callback(self, callback: Callable[[MonitoringEvent], None]):
        """Remove a callback function for events"""
        if callback in self.event_callbacks:
            self.event_callbacks.remove(callback)
    
    def get_recent_events(self, limit: int = 50, event_type: str = None, min_severity: int = 1) -> List[Dict]:
        """Get recent monitoring events"""
        events = list(self.event_history)
        
        # Filter by event type if specified
        if event_type:
            events = [e for e in events if e["event_type"] == event_type]
        
        # Filter by minimum severity
        events = [e for e in events if e["severity"] >= min_severity]
        
        # Return most recent events
        return events[-limit:] if len(events) > limit else events
    
    def get_current_status(self) -> Dict:
        """Get current monitoring status"""
        return {
            "is_monitoring": self.is_monitoring,
            "config": self.config,
            "last_metrics": asdict(self.last_metrics) if self.last_metrics else None,
            "events_count": len(self.event_history),
            "thresholds": [asdict(t) for t in self.thresholds],
            "artifact_count": len(self.artifact_hashes)
        }
    
    def get_quality_trends(self, hours: int = 24) -> Dict:
        """Get quality trends over time"""
        # Filter events to quality assessments within the time window
        cutoff_time = datetime.now() - timedelta(hours=hours)
        quality_events = [
            e for e in self.event_history
            if e["event_type"] == "quality_assessment" 
            and datetime.fromisoformat(e["timestamp"]) >= cutoff_time
        ]
        
        # Extract metrics over time
        trends = {
            "timestamps": [],
            "metrics": defaultdict(list)
        }
        
        for event in quality_events:
            timestamp = event["timestamp"]
            trends["timestamps"].append(timestamp)
            
            metrics = event["details"].get("metrics", {})
            for metric, value in metrics.items():
                trends["metrics"][metric].append(value)
        
        return trends
    
    def get_artifact_change_history(self, limit: int = 50) -> List[Dict]:
        """Get history of artifact changes"""
        artifact_events = [
            e for e in self.event_history
            if e["event_type"] == "artifact_update"
        ]
        
        return artifact_events[-limit:] if len(artifact_events) > limit else artifact_events
    
    def generate_monitoring_report(self) -> str:
        """Generate a monitoring report in markdown format"""
        status = self.get_current_status()
        recent_events = self.get_recent_events(20)
        
        report = f"""# Real-time Quality Monitoring Report

## Current Status

**Monitoring Active:** {"Yes" if status["is_monitoring"] else "No"}
**Last Update:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Artifacts Tracked:** {status["artifact_count"]}
**Events Recorded:** {status["events_count"]}

## Current Quality Metrics

"""
        
        if status["last_metrics"]:
            metrics = status["last_metrics"]
            report += "| Metric | Score | Status |\n"
            report += "|--------|-------|--------|\n"
            
            metric_names = [
                ("Overall Quality", "overall_score"),
                ("Clarity", "clarity_score"),
                ("Completeness", "completeness_score"),
                ("Consistency", "consistency_score"),
                ("Testability", "testability_score"),
                ("Maintainability", "maintainability_score"),
                ("Security", "security_score")
            ]
            
            for name, key in metric_names:
                score = metrics.get(key, 0)
                status_symbol = "✅" if score >= 0.9 else "⚠️" if score >= 0.7 else "❌"
                report += f"| {name} | {score:.2f} | {status_symbol} |\n"
        
        report += """

## Recent Events

"""
        
        if recent_events:
            report += "| Time | Type | Severity | Description |\n"
            report += "|------|------|----------|-------------|\n"
            
            for event in recent_events:
                timestamp = datetime.fromisoformat(event["timestamp"]).strftime("%H:%M:%S")
                severity = "🔴" * event["severity"]  # Visual severity indicator
                description = event["description"][:50] + "..." if len(event["description"]) > 50 else event["description"]
                report += f"| {timestamp} | {event['event_type']} | {severity} | {description} |\n"
        else:
            report += "No recent events recorded.\n"
        
        report += f"""

## Threshold Rules

Total thresholds: {len(status['thresholds'])}

"""
        
        for threshold in status["thresholds"]:
            status_text = "Enabled" if threshold["enabled"] else "Disabled"
            report += f"- {threshold['metric']} {threshold['operator']} {threshold['threshold']} (Severity: {threshold['severity']}, Action: {threshold['action']}) - {status_text}\n"
        
        report += """

---
*Report generated by Real-time Quality Monitoring System*
"""
        
        return report


# CLI Integration
def monitoring_cli():
    """CLI commands for real-time monitoring"""
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    app = typer.Typer()
    console = Console()
    
    @app.command()
    def start():
        """Start real-time monitoring"""
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
            
            # Initialize monitoring system
            monitor = RealTimeQualityMonitor(project_path)
            
            # Start monitoring
            result = monitor.start_monitoring()
            
            if result["status"] == "started":
                console.print("[green]✓[/green] Real-time monitoring started successfully")
                console.print("Monitoring will continue in the background.")
                console.print("Use 'goal monitor status' to check the current status.")
            else:
                console.print(f"[yellow]⚠[/yellow] {result['message']}")
                
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def stop():
        """Stop real-time monitoring"""
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
            
            # Initialize monitoring system
            monitor = RealTimeQualityMonitor(project_path)
            
            # Stop monitoring
            result = monitor.stop_monitoring()
            
            if result["status"] == "stopped":
                console.print("[green]✓[/green] Real-time monitoring stopped successfully")
            else:
                console.print(f"[yellow]⚠[/yellow] {result['message']}")
                
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def status():
        """Show current monitoring status"""
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
            
            # Initialize monitoring system
            monitor = RealTimeQualityMonitor(project_path)
            
            # Get status
            status_info = monitor.get_current_status()
            
            # Display status
            console.print(Panel("[bold]Real-time Quality Monitoring Status[/bold]", expand=False))
            
            console.print(f"Monitoring Active: {'[green]Yes[/green]' if status_info['is_monitoring'] else '[red]No[/red]'}")
            console.print(f"Artifacts Tracked: {status_info['artifact_count']}")
            console.print(f"Events Recorded: {status_info['events_count']}")
            
            if status_info['last_metrics']:
                console.print("\n[bold]Current Quality Metrics:[/bold]")
                metrics = status_info['last_metrics']
                
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Metric", style="dim")
                table.add_column("Score", justify="right")
                table.add_column("Status", justify="center")
                
                metric_data = [
                    ("Overall Quality", metrics['overall_score']),
                    ("Clarity", metrics['clarity_score']),
                    ("Completeness", metrics['completeness_score']),
                    ("Consistency", metrics['consistency_score']),
                    ("Testability", metrics['testability_score']),
                    ("Maintainability", metrics['maintainability_score']),
                    ("Security", metrics['security_score'])
                ]
                
                for name, score in metric_data:
                    status_symbol = "✅" if score >= 0.9 else "⚠️" if score >= 0.7 else "❌"
                    table.add_row(name, f"{score:.2f}", status_symbol)
                
                console.print(table)
            
            console.print(f"\n[bold]Threshold Rules:[/bold] {len(status_info['thresholds'])} active")
                
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def events(
        limit: int = typer.Option(20, help="Number of events to show"),
        event_type: str = typer.Option(None, help="Filter by event type"),
        min_severity: int = typer.Option(1, help="Minimum severity level (1-5)")
    ):
        """Show recent monitoring events"""
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
            
            # Initialize monitoring system
            monitor = RealTimeQualityMonitor(project_path)
            
            # Get events
            events = monitor.get_recent_events(limit=limit, event_type=event_type, min_severity=min_severity)
            
            # Display events
            console.print(Panel(f"[bold]Recent Monitoring Events[/bold] (Last {limit})", expand=False))
            
            if events:
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Time", style="dim")
                table.add_column("Type")
                table.add_column("Severity")
                table.add_column("Description")
                
                for event in events:
                    timestamp = datetime.fromisoformat(event["timestamp"]).strftime("%H:%M:%S")
                    severity = "🔴" * event["severity"]
                    description = event["description"][:60] + "..." if len(event["description"]) > 60 else event["description"]
                    table.add_row(timestamp, event["event_type"], severity, description)
                
                console.print(table)
            else:
                console.print("No events found matching the criteria.")
                
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def report():
        """Generate monitoring report"""
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
            
            # Initialize monitoring system
            monitor = RealTimeQualityMonitor(project_path)
            
            # Generate report
            report_content = monitor.generate_monitoring_report()
            
            # Save report
            report_file = project_path / ".goal" / "monitoring" / "latest_report.md"
            with open(report_file, 'w') as f:
                f.write(report_content)
            
            console.print(f"[green]✓[/green] Monitoring report saved to {report_file}")
            console.print("\n[bold]Report Preview:[/bold]")
            console.print(report_content[:1000] + "..." if len(report_content) > 1000 else report_content)
                
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    return app


# Integration with main CLI
def integrate_monitoring_with_main_cli(main_app):
    """Integrate monitoring commands with main CLI"""
    monitoring_app = monitoring_cli()
    main_app.add_typer(monitoring_app, name="monitor")
    return main_app