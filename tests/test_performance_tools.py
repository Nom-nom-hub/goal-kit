#!/usr/bin/env python3
"""
Test file for the performance optimization tools
"""

import json
import os
import shutil
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from goal_cli.performance_tools import PerformanceOptimizer


def test_performance_optimization():
    """Test the performance optimization tools"""
    print("Testing Performance Optimization Tools...")
    
    # Create a temporary project directory for testing
    test_project = Path(__file__).parent / "test_project"
    test_project.mkdir(exist_ok=True)
    
    # Create required .goal directory structure
    goal_dir = test_project / ".goal"
    goal_dir.mkdir(exist_ok=True)
    
    # Create a basic goal.yaml file
    goal_yaml = goal_dir / "goal.yaml"
    with open(goal_yaml, 'w') as f:
        f.write("project:\n  name: test-project\n  version: 0.1.0\n  description: A test project for performance optimization\n")
    
    # Initialize performance optimizer
    perf_optimizer = PerformanceOptimizer(test_project)
    
    # Test 1: List available benchmarks
    print("\n1. Listing available benchmarks...")
    benchmarks = perf_optimizer.benchmarks
    print(f"Found {len(benchmarks)} benchmarks")
    for bench_id, bench_data in list(benchmarks.items())[:3]:  # Show first 3
        print(f"  - {bench_id}: {bench_data.get('name', 'unnamed')}")
    
    # Test 2: Analyze performance
    print("\n2. Analyzing performance...")
    analyze_id = perf_optimizer.analyze_performance("project")
    print(f"Created analysis request: {analyze_id}")
    
    # Check status
    analyze_status = perf_optimizer.get_perf_status(analyze_id)
    print(f"Analysis Status: {analyze_status['status']}")
    
    # Test 3: Run a benchmark
    print("\n3. Running a benchmark...")
    benchmark_id = perf_optimizer.run_benchmark("startup_time", "project")
    print(f"Created benchmark request: {benchmark_id}")
    
    # Check status
    benchmark_status = perf_optimizer.get_perf_status(benchmark_id)
    print(f"Benchmark Status: {benchmark_status['status']}")
    
    # Test 4: Optimize performance
    print("\n4. Optimizing performance...")
    optimize_id = perf_optimizer.optimize_performance("project", "auto")
    print(f"Created optimization request: {optimize_id}")
    
    # Check status
    optimize_status = perf_optimizer.get_perf_status(optimize_id)
    print(f"Optimization Status: {optimize_status['status']}")
    
    # Test 5: Profile performance
    print("\n5. Profiling performance...")
    profile_id = perf_optimizer.profile_performance("project", "cprofile")
    print(f"Created profiling request: {profile_id}")
    
    # Check status
    profile_status = perf_optimizer.get_perf_status(profile_id)
    print(f"Profiling Status: {profile_status['status']}")
    
    # Test 6: List all requests
    print("\n6. Listing all performance requests...")
    requests = perf_optimizer.list_perf_requests()
    print(f"Found {len(requests)} performance requests")
    
    # Test 7: Show recent metrics
    print("\n7. Showing recent metrics...")
    recent_metrics = perf_optimizer.get_recent_metrics(5)
    print(f"Found {len(recent_metrics)} recent metrics")
    for metric in recent_metrics:
        print(f"  - {metric['name']}: {metric['value']:.2f} {metric['unit']}")
    
    # Test 8: Show benchmark history
    print("\n8. Showing benchmark history...")
    bench_history = perf_optimizer.get_benchmark_history("startup_time")
    print(f"Found {len(bench_history)} benchmark history entries")
    
    # Test 9: Generate performance report
    print("\n9. Generating performance report...")
    report_content = perf_optimizer.generate_performance_report()
    print(f"Generated report with {len(report_content)} characters")
    
    # Test 10: Check final statuses
    print("\n10. Checking final statuses...")
    all_request_ids = [analyze_id, benchmark_id, optimize_id, profile_id]
    for req_id in all_request_ids:
        status = perf_optimizer.get_perf_status(req_id)
        if status:
            print(f"  - {req_id[:8]}: {status['status']}")
            if status.get('result'):
                result = status['result']
                if isinstance(result, str):
                    try:
                        result = json.loads(result)
                    except:
                        result = {"output": result}
                if result.get('recommendations'):
                    print(f"    Recommendations: {len(result['recommendations'])}")
                if result.get('optimizations_applied'):
                    print(f"    Optimizations: {len(result['optimizations_applied'])}")
    
    # Clean up test project and generated files
    import shutil
    shutil.rmtree(test_project, ignore_errors=True)
    
    # Clean up any generated automation files
    automation_files = list(Path(__file__).parent.glob("test_project_*"))
    for f in automation_files:
        if f.is_dir():
            shutil.rmtree(f, ignore_errors=True)
    
    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    test_performance_optimization()