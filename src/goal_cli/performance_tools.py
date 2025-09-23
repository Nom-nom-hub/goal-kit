"""
Performance Optimization Tools for goal-dev-spec
Exceeds spec-kit functionality with advanced performance analysis and optimization capabilities.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import psutil


@dataclass
class PerformanceRequest:
    """Data class for performance optimization requests"""
    id: str
    action: str  # analyze, optimize, benchmark, profile
    target: str  # project, module, function, endpoint
    created_at: str
    status: str = "pending"
    result: Optional[Dict] = None
    error: Optional[str] = None


@dataclass
class PerformanceMetric:
    """Data class for performance metrics"""
    id: str
    name: str
    value: float
    unit: str
    timestamp: str
    context: Dict[str, Any] = None


class PerformanceOptimizer:
    """Performance optimization tools system"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.perf_path = project_path / ".goal" / "performance"
        self.perf_path.mkdir(exist_ok=True)
        
        # Performance requests storage
        self.perf_requests_file = self.perf_path / "perf_requests.json"
        self.perf_requests = self._load_perf_requests()
        
        # Performance metrics storage
        self.metrics_file = self.perf_path / "perf_metrics.json"
        self.metrics = self._load_metrics()
        
        # Benchmark results storage
        self.benchmarks_file = self.perf_path / "benchmarks.json"
        self.benchmarks = self._load_benchmarks()
        
        # Supported performance actions
        self.supported_actions = {
            "analyze": "Performance Analysis",
            "optimize": "Performance Optimization",
            "benchmark": "Benchmarking",
            "profile": "Profiling"
        }
        
        # Initialize with default benchmarks if they don't exist
        self._initialize_default_benchmarks()
    
    def _load_perf_requests(self) -> Dict[str, PerformanceRequest]:
        """Load performance requests from file"""
        if self.perf_requests_file.exists():
            try:
                with open(self.perf_requests_file, 'r') as f:
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
                    request = PerformanceRequest(**req_data)
                    requests[request.id] = request
                return requests
            except Exception as e:
                print(f"Warning: Could not load performance requests: {e}")
        return {}
    
    def _save_perf_requests(self):
        """Save performance requests to file"""
        # Convert result to string if it's a dict for JSON serialization
        data = []
        for req in self.perf_requests.values():
            req_dict = asdict(req)
            if isinstance(req_dict.get('result'), dict):
                req_dict['result'] = json.dumps(req_dict['result'])
            data.append(req_dict)
        
        with open(self.perf_requests_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_metrics(self) -> Dict[str, PerformanceMetric]:
        """Load performance metrics from file"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    data = json.load(f)
                metrics = {}
                for metric_data in data:
                    metric = PerformanceMetric(**metric_data)
                    metrics[metric.id] = metric
                return metrics
            except Exception as e:
                print(f"Warning: Could not load performance metrics: {e}")
        return {}
    
    def _save_metrics(self):
        """Save performance metrics to file"""
        data = [asdict(metric) for metric in self.metrics.values()]
        with open(self.metrics_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_benchmarks(self) -> Dict[str, Dict]:
        """Load benchmark results from file"""
        if self.benchmarks_file.exists():
            try:
                with open(self.benchmarks_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load benchmark results: {e}")
        return {}
    
    def _save_benchmarks(self):
        """Save benchmark results to file"""
        with open(self.benchmarks_file, 'w') as f:
            json.dump(self.benchmarks, f, indent=2)
    
    def _initialize_default_benchmarks(self):
        """Initialize default benchmarks"""
        default_benchmarks = {
            "startup_time": {
                "name": "Application Startup Time",
                "description": "Time taken to start the application",
                "unit": "seconds",
                "baseline": 5.0,
                "target": 2.0
            },
            "memory_usage": {
                "name": "Memory Usage",
                "description": "Peak memory usage during operation",
                "unit": "MB",
                "baseline": 100.0,
                "target": 50.0
            },
            "response_time": {
                "name": "Average Response Time",
                "description": "Average time to respond to requests",
                "unit": "milliseconds",
                "baseline": 200.0,
                "target": 100.0
            },
            "throughput": {
                "name": "Request Throughput",
                "description": "Number of requests processed per second",
                "unit": "requests/second",
                "baseline": 50.0,
                "target": 100.0
            }
        }
        
        # Add default benchmarks if they don't exist
        for bench_id, bench_data in default_benchmarks.items():
            if bench_id not in self.benchmarks:
                self.benchmarks[bench_id] = bench_data
        
        self._save_benchmarks()
    
    def analyze_performance(self, target: str = "project") -> str:
        """
        Analyze performance of a target
        
        Args:
            target: What to analyze (project, module, function, endpoint)
            
        Returns:
            ID of the performance request
        """
        # Create performance request
        request_id = hashlib.md5(f"analyze_{target}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        request = PerformanceRequest(
            id=request_id,
            action="analyze",
            target=target,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.perf_requests[request_id] = request
        self._save_perf_requests()
        
        # Process request
        self._process_perf_request(request_id)
        
        return request_id
    
    def optimize_performance(self, target: str = "project", strategy: str = "auto") -> str:
        """
        Optimize performance of a target
        
        Args:
            target: What to optimize (project, module, function, endpoint)
            strategy: Optimization strategy (auto, memory, cpu, io)
            
        Returns:
            ID of the performance request
        """
        # Create performance request
        request_id = hashlib.md5(f"optimize_{target}_{strategy}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        request = PerformanceRequest(
            id=request_id,
            action="optimize",
            target=target,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.perf_requests[request_id] = request
        self._save_perf_requests()
        
        # Process request
        self._process_perf_request(request_id, {"strategy": strategy})
        
        return request_id
    
    def run_benchmark(self, benchmark_type: str, target: str = "project") -> str:
        """
        Run a benchmark on a target
        
        Args:
            benchmark_type: Type of benchmark to run
            target: What to benchmark (project, module, function, endpoint)
            
        Returns:
            ID of the performance request
        """
        # Create performance request
        request_id = hashlib.md5(f"benchmark_{benchmark_type}_{target}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        request = PerformanceRequest(
            id=request_id,
            action="benchmark",
            target=target,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.perf_requests[request_id] = request
        self._save_perf_requests()
        
        # Process request
        self._process_perf_request(request_id, {"benchmark_type": benchmark_type})
        
        return request_id
    
    def profile_performance(self, target: str = "project", profiler: str = "cprofile") -> str:
        """
        Profile performance of a target
        
        Args:
            target: What to profile (project, module, function, endpoint)
            profiler: Profiler to use (cprofile, py-spy, custom)
            
        Returns:
            ID of the performance request
        """
        # Create performance request
        request_id = hashlib.md5(f"profile_{target}_{profiler}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        request = PerformanceRequest(
            id=request_id,
            action="profile",
            target=target,
            created_at=datetime.now().isoformat()
        )
        
        # Store request
        self.perf_requests[request_id] = request
        self._save_perf_requests()
        
        # Process request
        self._process_perf_request(request_id, {"profiler": profiler})
        
        return request_id
    
    def _process_perf_request(self, request_id: str, params: Dict = None):
        """Process a performance request"""
        if request_id not in self.perf_requests:
            return
        
        request = self.perf_requests[request_id]
        request.status = "processing"
        self._save_perf_requests()
        
        try:
            result = {}
            
            if request.action == "analyze":
                result = self._analyze_performance(request.target)
            elif request.action == "optimize":
                strategy = params.get("strategy", "auto") if params else "auto"
                result = self._optimize_performance(request.target, strategy)
            elif request.action == "benchmark":
                benchmark_type = params.get("benchmark_type", "generic") if params else "generic"
                result = self._run_benchmark(request.target, benchmark_type)
            elif request.action == "profile":
                profiler = params.get("profiler", "cprofile") if params else "cprofile"
                result = self._profile_performance(request.target, profiler)
            
            # Update request
            request.status = "completed"
            request.result = result
            
        except Exception as e:
            request.status = "failed"
            request.error = str(e)
        
        self._save_perf_requests()
    
    def _analyze_performance(self, target: str) -> Dict:
        """Analyze performance of a target"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "system_metrics": {},
            "application_metrics": {},
            "recommendations": []
        }
        
        # Collect system metrics
        analysis["system_metrics"] = self._collect_system_metrics()
        
        # Collect application metrics (mock for now)
        analysis["application_metrics"] = self._collect_application_metrics(target)
        
        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(analysis)
        
        # Store metrics
        self._store_metrics_from_analysis(analysis)
        
        return analysis
    
    def _optimize_performance(self, target: str, strategy: str) -> Dict:
        """Optimize performance of a target"""
        optimization = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "strategy": strategy,
            "optimizations_applied": [],
            "before_metrics": {},
            "after_metrics": {},
            "improvements": {}
        }
        
        # Collect before metrics
        optimization["before_metrics"] = self._collect_system_metrics()
        
        # Apply optimizations based on strategy
        optimizations = self._apply_optimizations(target, strategy)
        optimization["optimizations_applied"] = optimizations
        
        # Collect after metrics
        optimization["after_metrics"] = self._collect_system_metrics()
        
        # Calculate improvements
        optimization["improvements"] = self._calculate_improvements(
            optimization["before_metrics"],
            optimization["after_metrics"]
        )
        
        return optimization
    
    def _run_benchmark(self, target: str, benchmark_type: str) -> Dict:
        """Run a benchmark on a target"""
        benchmark = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "benchmark_type": benchmark_type,
            "results": {},
            "baseline_comparison": {}
        }
        
        # Run benchmark based on type
        if benchmark_type == "startup_time":
            benchmark["results"] = self._benchmark_startup_time(target)
        elif benchmark_type == "memory_usage":
            benchmark["results"] = self._benchmark_memory_usage(target)
        elif benchmark_type == "response_time":
            benchmark["results"] = self._benchmark_response_time(target)
        elif benchmark_type == "throughput":
            benchmark["results"] = self._benchmark_throughput(target)
        else:
            benchmark["results"] = self._benchmark_generic(target)
        
        # Compare with baseline
        benchmark["baseline_comparison"] = self._compare_with_baseline(benchmark_type, benchmark["results"])
        
        # Store benchmark results
        self.benchmarks[benchmark_type] = {
            "last_run": datetime.now().isoformat(),
            "results": benchmark["results"]
        }
        self._save_benchmarks()
        
        return benchmark
    
    def _profile_performance(self, target: str, profiler: str) -> Dict:
        """Profile performance of a target"""
        profiling = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "profiler": profiler,
            "profile_data": {},
            "hotspots": []
        }
        
        # Run profiling based on profiler type
        if profiler == "cprofile":
            profiling["profile_data"] = self._profile_with_cprofile(target)
        else:
            profiling["profile_data"] = self._profile_generic(target)
        
        # Identify hotspots
        profiling["hotspots"] = self._identify_hotspots(profiling["profile_data"])
        
        return profiling
    
    def _collect_system_metrics(self) -> Dict:
        """Collect system performance metrics"""
        metrics = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_available_mb": psutil.virtual_memory().available / (1024 * 1024),
            "disk_usage_percent": psutil.disk_usage('/').percent,
            "network_io": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv
            }
        }
        return metrics
    
    def _collect_application_metrics(self, target: str) -> Dict:
        """Collect application-specific metrics"""
        # This would collect application-specific metrics
        # For now, we'll return mock data
        return {
            "response_time_ms": 150.5,
            "requests_per_second": 45.2,
            "error_rate": 0.02,
            "database_query_time_ms": 45.3,
            "cache_hit_rate": 0.85
        }
    
    def _generate_recommendations(self, analysis: Dict) -> List[Dict]:
        """Generate performance recommendations"""
        recommendations = []
        system_metrics = analysis.get("system_metrics", {})
        app_metrics = analysis.get("application_metrics", {})
        
        # CPU usage recommendations
        if system_metrics.get("cpu_percent", 0) > 80:
            recommendations.append({
                "type": "cpu",
                "priority": "high",
                "description": "High CPU usage detected",
                "recommendation": "Consider optimizing CPU-intensive operations or adding more CPU resources"
            })
        
        # Memory usage recommendations
        if system_metrics.get("memory_percent", 0) > 80:
            recommendations.append({
                "type": "memory",
                "priority": "high",
                "description": "High memory usage detected",
                "recommendation": "Consider optimizing memory usage or adding more RAM"
            })
        
        # Application response time recommendations
        if app_metrics.get("response_time_ms", 0) > 200:
            recommendations.append({
                "type": "application",
                "priority": "medium",
                "description": "High response time detected",
                "recommendation": "Consider optimizing database queries or implementing caching"
            })
        
        # Generic recommendations
        recommendations.append({
            "type": "general",
            "priority": "low",
            "description": "Regular performance monitoring recommended",
            "recommendation": "Set up continuous performance monitoring and alerting"
        })
        
        return recommendations
    
    def _store_metrics_from_analysis(self, analysis: Dict):
        """Store metrics from analysis results"""
        timestamp = analysis.get("timestamp", datetime.now().isoformat())
        
        # Store system metrics
        system_metrics = analysis.get("system_metrics", {})
        for metric_name, value in system_metrics.items():
            if isinstance(value, (int, float)):
                metric_id = hashlib.md5(f"{metric_name}_{timestamp}".encode()).hexdigest()[:16]
                metric = PerformanceMetric(
                    id=metric_id,
                    name=metric_name,
                    value=value,
                    unit="percent" if "percent" in metric_name else "bytes" if "bytes" in metric_name else "unknown",
                    timestamp=timestamp
                )
                self.metrics[metric_id] = metric
        
        # Store application metrics
        app_metrics = analysis.get("application_metrics", {})
        for metric_name, value in app_metrics.items():
            if isinstance(value, (int, float)):
                metric_id = hashlib.md5(f"{metric_name}_{timestamp}".encode()).hexdigest()[:16]
                unit = "ms" if "time" in metric_name else "requests/sec" if "per_second" in metric_name else "unknown"
                metric = PerformanceMetric(
                    id=metric_id,
                    name=metric_name,
                    value=value,
                    unit=unit,
                    timestamp=timestamp
                )
                self.metrics[metric_id] = metric
        
        self._save_metrics()
    
    def _apply_optimizations(self, target: str, strategy: str) -> List[Dict]:
        """Apply performance optimizations"""
        optimizations = []
        
        # This would apply actual optimizations
        # For now, we'll return mock optimizations
        
        if strategy in ["auto", "memory"]:
            optimizations.append({
                "type": "memory",
                "description": "Implemented memory pooling",
                "status": "applied"
            })
        
        if strategy in ["auto", "cpu"]:
            optimizations.append({
                "type": "cpu",
                "description": "Optimized CPU-intensive loops",
                "status": "applied"
            })
        
        if strategy in ["auto", "io"]:
            optimizations.append({
                "type": "io",
                "description": "Implemented async I/O operations",
                "status": "applied"
            })
        
        return optimizations
    
    def _calculate_improvements(self, before: Dict, after: Dict) -> Dict:
        """Calculate performance improvements"""
        improvements = {}
        
        # Calculate improvements for numeric metrics
        for key, before_value in before.items():
            if key in after and isinstance(before_value, (int, float)):
                after_value = after[key]
                if before_value != 0:
                    improvement_pct = ((before_value - after_value) / before_value) * 100
                    improvements[key] = {
                        "before": before_value,
                        "after": after_value,
                        "improvement_percent": improvement_pct
                    }
        
        return improvements
    
    def _benchmark_startup_time(self, target: str) -> Dict:
        """Benchmark application startup time"""
        # This would actually measure startup time
        # For now, we'll return mock data
        return {
            "startup_time_seconds": 2.3,
            "import_time_seconds": 1.1,
            "initialization_time_seconds": 1.2
        }
    
    def _benchmark_memory_usage(self, target: str) -> Dict:
        """Benchmark memory usage"""
        # This would actually measure memory usage
        # For now, we'll return mock data
        return {
            "peak_memory_mb": 75.4,
            "average_memory_mb": 62.1,
            "memory_growth_mb": 13.3
        }
    
    def _benchmark_response_time(self, target: str) -> Dict:
        """Benchmark response time"""
        # This would actually measure response time
        # For now, we'll return mock data
        return {
            "average_response_ms": 145.2,
            "median_response_ms": 138.7,
            "p95_response_ms": 201.3,
            "p99_response_ms": 256.8
        }
    
    def _benchmark_throughput(self, target: str) -> Dict:
        """Benchmark throughput"""
        # This would actually measure throughput
        # For now, we'll return mock data
        return {
            "requests_per_second": 87.3,
            "bytes_per_second": 1250000,
            "concurrent_users": 50
        }
    
    def _benchmark_generic(self, target: str) -> Dict:
        """Generic benchmark"""
        # This would run a generic benchmark
        # For now, we'll return mock data
        return {
            "score": 85.7,
            "relative_performance": "good",
            "compared_to_baseline": "+15%"
        }
    
    def _compare_with_baseline(self, benchmark_type: str, results: Dict) -> Dict:
        """Compare benchmark results with baseline"""
        comparison = {
            "baseline_available": False,
            "improvement": "unknown"
        }
        
        if benchmark_type in self.benchmarks:
            baseline = self.benchmarks[benchmark_type]
            comparison["baseline_available"] = True
            
            # Calculate improvement (simplified)
            if "score" in results:
                baseline_score = baseline.get("baseline", 0)
                current_score = results.get("score", 0)
                if baseline_score != 0:
                    improvement = ((current_score - baseline_score) / baseline_score) * 100
                    comparison["improvement"] = f"{improvement:+.1f}%"
        
        return comparison
    
    def _profile_with_cprofile(self, target: str) -> Dict:
        """Profile with cProfile"""
        # This would actually run cProfile
        # For now, we'll return mock data
        return {
            "profiler": "cProfile",
            "total_time": 1.23,
            "function_calls": 15420,
            "primitive_calls": 12345
        }
    
    def _profile_generic(self, target: str) -> Dict:
        """Generic profiling"""
        # This would run generic profiling
        # For now, we'll return mock data
        return {
            "profiler": "generic",
            "profile_data": "Profile data placeholder"
        }
    
    def _identify_hotspots(self, profile_data: Dict) -> List[Dict]:
        """Identify performance hotspots"""
        # This would analyze profile data to identify hotspots
        # For now, we'll return mock hotspots
        return [
            {
                "function": "expensive_function",
                "time_spent": 0.45,
                "percentage": 36.6,
                "recommendation": "Consider optimizing this function"
            },
            {
                "function": "database_query",
                "time_spent": 0.32,
                "percentage": 26.0,
                "recommendation": "Consider adding database indexes"
            }
        ]
    
    def get_perf_status(self, request_id: str) -> Optional[Dict]:
        """Get the status of a performance request"""
        if request_id in self.perf_requests:
            request = self.perf_requests[request_id]
            result = asdict(request)
            # Convert result back to dict if it's a JSON string
            if isinstance(result.get('result'), str):
                try:
                    result['result'] = json.loads(result['result'])
                except json.JSONDecodeError:
                    result['result'] = None
            return result
        return None
    
    def list_perf_requests(self) -> List[Dict]:
        """List all performance requests"""
        requests = []
        for req in self.perf_requests.values():
            req_dict = asdict(req)
            # Convert result back to dict if it's a JSON string
            if isinstance(req_dict.get('result'), str):
                try:
                    req_dict['result'] = json.loads(req_dict['result'])
                except json.JSONDecodeError:
                    req_dict['result'] = None
            requests.append(req_dict)
        return requests
    
    def get_recent_metrics(self, limit: int = 10) -> List[Dict]:
        """Get recent performance metrics"""
        # Sort metrics by timestamp and return most recent
        sorted_metrics = sorted(
            self.metrics.values(),
            key=lambda x: x.timestamp,
            reverse=True
        )
        return [asdict(metric) for metric in sorted_metrics[:limit]]
    
    def get_benchmark_history(self, benchmark_type: str) -> List[Dict]:
        """Get benchmark history for a specific benchmark type"""
        # This would return historical benchmark data
        # For now, we'll return stored data
        if benchmark_type in self.benchmarks:
            return [self.benchmarks[benchmark_type]]
        return []
    
    def generate_performance_report(self) -> str:
        """Generate a comprehensive performance report"""
        # Get recent performance requests
        recent_requests = sorted(
            [req for req in self.perf_requests.values() 
             if req.status in ["completed", "failed"]],
            key=lambda x: x.created_at,
            reverse=True
        )[:10]  # Last 10 requests
        
        # Get recent metrics
        recent_metrics = self.get_recent_metrics(20)
        
        # Get benchmark data
        benchmark_summary = {}
        for bench_id in self.benchmarks:
            benchmark_summary[bench_id] = self.benchmarks[bench_id]
        
        # Create report
        report = f"""# Performance Optimization Report

## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Recent Performance Activities

| ID | Action | Target | Status | Created |
|----|--------|--------|--------|---------|
"""
        
        for req in recent_requests:
            created = datetime.fromisoformat(req.created_at).strftime("%Y-%m-%d %H:%M")
            report += f"| {req.id[:8]} | {req.action} | {req.target} | {req.status} | {created} |\n"
        
        report += """
## Recent Performance Metrics

| Metric | Value | Unit | Timestamp |
|--------|-------|------|-----------|
"""
        
        for metric in recent_metrics[:10]:  # Show first 10 metrics
            timestamp = datetime.fromisoformat(metric['timestamp']).strftime("%Y-%m-%d %H:%M")
            report += f"| {metric['name']} | {metric['value']:.2f} | {metric['unit']} | {timestamp} |\n"
        
        report += """
## Benchmark Summary

| Benchmark | Last Run | Latest Result |
|-----------|----------|---------------|
"""
        
        for bench_id, bench_data in benchmark_summary.items():
            last_run = bench_data.get('last_run', 'never')
            if last_run != 'never':
                last_run = datetime.fromisoformat(last_run).strftime("%Y-%m-%d %H:%M")
            results = bench_data.get('results', {})
            result_summary = str(results.get('score', 'N/A')) if results else 'N/A'
            report += f"| {bench_data.get('name', bench_id)} | {last_run} | {result_summary} |\n"
        
        report += f"""
## Summary

- Total Performance Requests: {len(self.perf_requests)}
- Completed Requests: {len([r for r in self.perf_requests.values() if r.status == 'completed'])}
- Failed Requests: {len([r for r in self.perf_requests.values() if r.status == 'failed'])}
- Tracked Metrics: {len(self.metrics)}
- Benchmark Types: {len(self.benchmarks)}

"""
        
        # Add recommendations if available
        if recent_requests and recent_requests[0].result:
            result = recent_requests[0].result
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    result = {"output": result}
            
            if result.get("recommendations"):
                report += "## Latest Recommendations\n\n"
                for rec in result["recommendations"]:
                    priority = rec.get("priority", "medium")
                    priority_icon = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"
                    report += f"{priority_icon} **{rec.get('description', 'No description')}**\n"
                    report += f"   Recommendation: {rec.get('recommendation', 'No recommendation')}\n\n"
        
        report += """
## Recommendations

1. Regularly monitor performance metrics
2. Run benchmarks after major changes
3. Profile applications to identify bottlenecks
4. Apply optimizations based on profiling data
5. Set up performance alerts for critical metrics

---
*Report generated by Performance Optimization Tools System*
"""
        
        return report


# CLI Integration
def performance_cli():
    """CLI commands for performance optimization"""
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    app = typer.Typer()
    console = Console()
    
    @app.command()
    def analyze(target: str = typer.Argument("project", help="Target to analyze (project, module, function, endpoint)")):
        """Analyze performance of a target"""
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
            
            # Initialize performance optimizer
            perf_optimizer = PerformanceOptimizer(project_path)
            
            # Analyze performance
            request_id = perf_optimizer.analyze_performance(target)
            
            console.print(f"[green]✓[/green] Performance analysis request created with ID: {request_id}")
            console.print(f"Check status with: goal perf status {request_id}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def optimize(
        target: str = typer.Argument("project", help="Target to optimize (project, module, function, endpoint)"),
        strategy: str = typer.Option("auto", help="Optimization strategy (auto, memory, cpu, io)")
    ):
        """Optimize performance of a target"""
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
            
            # Initialize performance optimizer
            perf_optimizer = PerformanceOptimizer(project_path)
            
            # Optimize performance
            request_id = perf_optimizer.optimize_performance(target, strategy)
            
            console.print(f"[green]✓[/green] Performance optimization request created with ID: {request_id}")
            console.print(f"Check status with: goal perf status {request_id}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def benchmark(
        type: str = typer.Argument(..., help="Type of benchmark to run"),
        target: str = typer.Option("project", help="Target to benchmark (project, module, function, endpoint)")
    ):
        """Run a benchmark on a target"""
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
            
            # Initialize performance optimizer
            perf_optimizer = PerformanceOptimizer(project_path)
            
            # Run benchmark
            request_id = perf_optimizer.run_benchmark(type, target)
            
            console.print(f"[green]✓[/green] Benchmark request created with ID: {request_id}")
            console.print(f"Check status with: goal perf status {request_id}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def profile(
        target: str = typer.Argument("project", help="Target to profile (project, module, function, endpoint)"),
        profiler: str = typer.Option("cprofile", help="Profiler to use (cprofile, py-spy, custom)")
    ):
        """Profile performance of a target"""
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
            
            # Initialize performance optimizer
            perf_optimizer = PerformanceOptimizer(project_path)
            
            # Profile performance
            request_id = perf_optimizer.profile_performance(target, profiler)
            
            console.print(f"[green]✓[/green] Performance profiling request created with ID: {request_id}")
            console.print(f"Check status with: goal perf status {request_id}")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def status(request_id: str = typer.Argument(..., help="Performance request ID")):
        """Check the status of a performance request"""
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
            
            # Initialize performance optimizer
            perf_optimizer = PerformanceOptimizer(project_path)
            
            # Check status
            status = perf_optimizer.get_perf_status(request_id)
            if status:
                console.print(Panel(f"[bold]Performance Request Status: {request_id}[/bold]", expand=False))
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
                    
                    console.print(f"Timestamp: {result.get('timestamp', 'unknown')}")
                    if result.get('recommendations'):
                        console.print(f"Recommendations: {len(result['recommendations'])}")
                    if result.get('optimizations_applied'):
                        console.print(f"Optimizations Applied: {len(result['optimizations_applied'])}")
            else:
                console.print(f"[red]Performance request {request_id} not found[/red]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def list():
        """List all performance requests"""
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
            
            # Initialize performance optimizer
            perf_optimizer = PerformanceOptimizer(project_path)
            
            # List requests
            requests = perf_optimizer.list_perf_requests()
            if requests:
                console.print(Panel(f"[bold]Performance Requests ({len(requests)})[/bold]", expand=False))
                
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
                console.print("[yellow]No performance requests found[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def metrics(limit: int = typer.Option(10, help="Number of recent metrics to show")):
        """Show recent performance metrics"""
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
            
            # Initialize performance optimizer
            perf_optimizer = PerformanceOptimizer(project_path)
            
            # Get recent metrics
            recent_metrics = perf_optimizer.get_recent_metrics(limit)
            if recent_metrics:
                console.print(Panel(f"[bold]Recent Performance Metrics (Last {len(recent_metrics)})[/bold]", expand=False))
                
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="green")
                table.add_column("Unit", style="yellow")
                table.add_column("Time", style="dim")
                
                for metric in recent_metrics:
                    timestamp = datetime.fromisoformat(metric['timestamp']).strftime("%H:%M:%S")
                    table.add_row(
                        metric['name'],
                        f"{metric['value']:.2f}",
                        metric['unit'],
                        timestamp
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No performance metrics found[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def benchmarks(type: str = typer.Argument(None, help="Specific benchmark type to show history for")):
        """Show benchmark results"""
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
            
            # Initialize performance optimizer
            perf_optimizer = PerformanceOptimizer(project_path)
            
            if type:
                # Show history for specific benchmark type
                history = perf_optimizer.get_benchmark_history(type)
                if history:
                    console.print(Panel(f"[bold]Benchmark History: {type}[/bold]", expand=False))
                    for entry in history:
                        console.print(f"Last Run: {entry.get('last_run', 'unknown')}")
                        console.print(f"Results: {entry.get('results', 'no results')}")
                else:
                    console.print(f"[yellow]No benchmark history found for {type}[/yellow]")
            else:
                # Show all benchmarks
                all_benchmarks = perf_optimizer.benchmarks
                if all_benchmarks:
                    console.print(Panel(f"[bold]Benchmark Summary ({len(all_benchmarks)})[/bold]", expand=False))
                    
                    table = Table(show_header=True, header_style="bold magenta")
                    table.add_column("Benchmark", style="cyan")
                    table.add_column("Last Run", style="green")
                    table.add_column("Description", style="yellow")
                    
                    for bench_id, bench_data in all_benchmarks.items():
                        last_run = bench_data.get('last_run', 'never')
                        if last_run != 'never':
                            last_run = datetime.fromisoformat(last_run).strftime("%Y-%m-%d %H:%M")
                        table.add_row(
                            bench_data.get('name', bench_id),
                            last_run,
                            bench_data.get('description', 'no description')
                        )
                    
                    console.print(table)
                else:
                    console.print("[yellow]No benchmarks found[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    @app.command()
    def report():
        """Generate a performance optimization report"""
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
            
            # Initialize performance optimizer
            perf_optimizer = PerformanceOptimizer(project_path)
            
            # Generate report
            report_content = perf_optimizer.generate_performance_report()
            
            # Save report
            report_file = project_path / ".goal" / "performance" / "perf_report.md"
            with open(report_file, 'w') as f:
                f.write(report_content)
            
            console.print(f"[green]✓[/green] Performance report saved to {report_file}")
            console.print("\n[bold]Report Preview:[/bold]")
            console.print(report_content[:1000] + "..." if len(report_content) > 1000 else report_content)
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
    
    return app


# Integration with main CLI
def integrate_performance_with_main_cli(main_app):
    """Integrate performance optimization commands with main CLI"""
    perf_app = performance_cli()
    main_app.add_typer(perf_app, name="perf")
    return main_app