"""
Enhanced UI components for the goal-dev-spec CLI with advanced progress tracking
"""

import time
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from rich.console import Console
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.live import Live

console = Console()

class EnhancedStepTracker:
    """Enhanced step tracker with real-time progress updates and predictive analytics"""
    
    def __init__(self, title: str, total_steps: int = 0):
        self.title = title
        self.total_steps = total_steps
        self.current_step = 0
        self.steps: List[Dict[str, Any]] = []  # list of dicts: {key, label, status, detail, start_time, end_time}
        self.start_time = time.time()
        self.step_times: List[float] = []  # Track time for each step
        self.estimated_completion_time = None
        self.notifications: List[Dict[str, Any]] = []
        self._refresh_cb = None
        self.status_order = {"pending": 0, "running": 1, "done": 2, "error": 3, "skipped": 4}
        self.live_display = None
        self.live_thread = None
        self.should_stop = False
        
    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if not key or not label:
            return  # Skip invalid inputs
        if key not in [s["key"] for s in self.steps]:
            self.steps.append({
                "key": key, 
                "label": label, 
                "status": "pending", 
                "detail": "",
                "start_time": None,
                "end_time": None
            })
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        # Update step status
        for s in self.steps:
            if s["key"] == key:
                s["status"] = "running"
                s["detail"] = detail
                s["start_time"] = time.time()
                break
        else:
            # If not present, add it
            self.steps.append({
                "key": key, 
                "label": key, 
                "status": "running", 
                "detail": detail,
                "start_time": time.time(),
                "end_time": None
            })
        
        self.current_step += 1
        self._maybe_refresh()

    def complete(self, key: str, detail: str = ""):
        # Update step status
        for s in self.steps:
            if s["key"] == key:
                s["status"] = "done"
                if detail:
                    s["detail"] = detail
                s["end_time"] = time.time()
                break
        
        # Update timing information
        if self.steps:
            completed_steps = [s for s in self.steps if s["status"] == "done"]
            if completed_steps:
                # Calculate average time per step
                total_time = sum(
                    (s["end_time"] - s["start_time"]) 
                    for s in completed_steps 
                    if s["start_time"] and s["end_time"]
                )
                avg_time_per_step = total_time / len(completed_steps)
                
                # Estimate remaining time
                remaining_steps = len([s for s in self.steps if s["status"] in ["pending", "running"]])
                self.estimated_completion_time = avg_time_per_step * remaining_steps
        
        self._maybe_refresh()

    def error(self, key: str, detail: str = ""):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = "error"
                if detail:
                    s["detail"] = detail
                s["end_time"] = time.time()
                break
        self._maybe_refresh()

    def skip(self, key: str, detail: str = ""):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = "skipped"
                if detail:
                    s["detail"] = detail
                s["end_time"] = time.time()
                break
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass  # Silently ignore refresh errors

    def get_progress_percentage(self) -> float:
        """Get progress percentage"""
        if self.total_steps <= 0:
            # Estimate based on completed steps
            if not self.steps:
                return 0.0
            completed = len([s for s in self.steps if s["status"] == "done"])
            return min(100.0, (completed / len(self.steps)) * 100.0)
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
        self._maybe_refresh()

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        
        # Add progress information
        elapsed = self.get_elapsed_time()
        eta = self.get_eta()
        
        progress_info = f"[bright_black]Elapsed: {self._format_time(elapsed)}[/bright_black]"
        if eta:
            progress_info += f" [bright_black]| ETA: {eta.strftime('%H:%M:%S')}[/bright_black]"
        
        if self.total_steps > 0:
            progress_info += f" [bright_black]| {self.current_step}/{self.total_steps} steps[/bright_black]"
        else:
            completed_steps = len([s for s in self.steps if s["status"] == "done"])
            progress_info += f" [bright_black]| {completed_steps}/{len(self.steps)} steps[/bright_black]"
        
        tree.add(progress_info)
        
        # Add steps
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            # Status symbols with colors
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
        
        # Add notifications if any
        if self.notifications:
            notification_tree = tree.add("[bold yellow]Notifications:[/bold yellow]")
            for notification in self.notifications[-3:]:  # Show last 3 notifications
                level_color = {
                    "info": "blue",
                    "warning": "yellow",
                    "error": "red",
                    "success": "green"
                }.get(notification["level"], "white")
                
                message = f"[{level_color}]{notification['message']}[/{level_color}]"
                notification_tree.add(message)
        
        return tree
    
    def _format_time(self, seconds: float) -> str:
        """Format time in a human-readable way"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"

class ProgressDisplayManager:
    """Manages the live display of progress information"""
    
    def __init__(self, tracker: EnhancedStepTracker):
        self.tracker = tracker
        self.live = None
        self.is_running = False
        
    def start(self):
        """Start the live display"""
        if not self.is_running:
            self.is_running = True
            self.live = Live(
                self.tracker.render(), 
                console=console, 
                refresh_per_second=4,
                transient=False
            )
            self.live.start()
            self.tracker.attach_refresh(self._update_display)
    
    def stop(self):
        """Stop the live display"""
        if self.is_running and self.live:
            self.is_running = False
            self.live.stop()
            # Show final state
            console.print(self.tracker.render())
    
    def _update_display(self):
        """Update the live display"""
        if self.is_running and self.live:
            self.live.update(self.tracker.render())

# Enhanced progress bar with analytics
class EnhancedProgressBar:
    """Enhanced progress bar with predictive analytics integration"""
    
    def __init__(self, title: str, total: int):
        self.title = title
        self.total = total
        self.current = 0
        self.start_time = time.time()
        self.step_times: List[float] = []
        self.estimated_completion_time: Optional[float] = None
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console
        )
        self.task = self.progress.add_task(title, total=total)
        
    def start(self):
        """Start the progress bar"""
        self.progress.start()
        
    def advance(self, steps: int = 1, description: str = ""):
        """Advance the progress bar"""
        self.current += steps
        self.step_times.append(time.time())
        
        # Update estimated completion time
        if len(self.step_times) > 1:
            avg_time_per_step = (self.step_times[-1] - self.step_times[0]) / len(self.step_times)
            remaining_steps = self.total - self.current
            self.estimated_completion_time = avg_time_per_step * remaining_steps
            
        self.progress.update(self.task, advance=steps, description=description)
        
    def stop(self):
        """Stop the progress bar"""
        self.progress.stop()
        
    def get_eta(self) -> Optional[datetime]:
        """Get estimated time of arrival"""
        if self.estimated_completion_time is not None:
            return datetime.now() + timedelta(seconds=self.estimated_completion_time)
        return None

# Notification system
class NotificationManager:
    """Manages notifications and alerts"""
    
    def __init__(self):
        self.notifications = []
        
    def notify(self, message: str, level: str = "info"):
        """Add a notification"""
        notification = {
            'timestamp': datetime.now(),
            'message': message,
            'level': level
        }
        self.notifications.append(notification)
        
        # Display notification based on level
        level_colors = {
            "info": "blue",
            "warning": "yellow",
            "error": "red",
            "success": "green"
        }
        
        color = level_colors.get(level, "white")
        icon = {
            "info": "ℹ",
            "warning": "⚠",
            "error": "❌",
            "success": "✅"
        }.get(level, "•")
        
        console.print(f"[{color}]{icon} {message}[/{color}]")
        
    def get_notifications(self, level: Optional[str] = None) -> List[Dict]:
        """Get notifications, optionally filtered by level"""
        if level:
            return [n for n in self.notifications if n['level'] == level]
        return self.notifications

# Error handling with recovery mechanisms
class ErrorHandler:
    """Handles errors with recovery mechanisms"""
    
    def __init__(self, tracker: Optional[EnhancedStepTracker] = None):
        self.tracker = tracker
        self.error_count = 0
        self.max_retries = 3
        
    def handle_error(self, error: Exception, step_key: Optional[str] = None, retry_count: int = 0):
        """Handle an error with potential recovery"""
        self.error_count += 1
        
        # Log the error
        error_msg = f"Error occurred: {str(error)}"
        if self.tracker:
            self.tracker.add_notification(error_msg, "error")
            if step_key:
                self.tracker.error(step_key, str(error)[:50] + "..." if len(str(error)) > 50 else str(error))
        
        # Try to recover if retry count is less than max
        if retry_count < self.max_retries:
            recovery_msg = f"Attempting recovery (attempt {retry_count + 1}/{self.max_retries})"
            if self.tracker:
                self.tracker.add_notification(recovery_msg, "warning")
            
            # Wait before retry (exponential backoff)
            time.sleep(2 ** retry_count)
            return True  # Indicate that recovery should be attempted
        
        # If we've exhausted retries, mark as failed
        if self.tracker and step_key:
            self.tracker.error(step_key, f"Failed after {self.max_retries} attempts")
        
        return False  # Indicate that recovery failed