#!/usr/bin/env python3
"""Quick test runner to avoid hanging."""
import subprocess
import sys

tests = [
    ("Metrics", ["tests/test_metrics.py"]),
    ("Metrics Command", ["tests/test_metrics_command.py"]),
    ("Status", ["tests/test_status.py"]),
    ("Milestones", ["tests/test_milestones.py"]),
    ("Execution", ["tests/test_execution.py"]),
    ("Analyzer", ["tests/test_analyzer.py"]),
]

total_passed = 0
total_failed = 0

for name, files in tests:
    print(f"\n{'='*60}")
    print(f"Running {name} tests...")
    print('='*60)
    
    cmd = ["python", "-m", "pytest"] + files + ["-v", "--tb=no", "-q"]
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode == 0:
        print(f"OK: {name} tests passed")
    else:
        print(f"FAIL: {name} tests failed")

print("\n" + "="*60)
print("Test run complete")
print("="*60)
