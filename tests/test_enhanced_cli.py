#!/usr/bin/env python3
"""
Test script for the enhanced goal-dev-spec CLI
"""

import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_enhanced_cli():
    """Test the enhanced CLI functionality"""
    print("Testing enhanced goal-dev-spec CLI...")
    
    # Test imports
    try:
        from goal_cli import EnhancedStepTracker, PredictiveAnalyticsEngine
        print("[PASS] EnhancedStepTracker imported successfully")
        print("[PASS] PredictiveAnalyticsEngine imported successfully")
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        return False
    
    # Test EnhancedStepTracker
    try:
        tracker = EnhancedStepTracker("Test Process", total_steps=3)
        tracker.add("step1", "First step")
        tracker.add("step2", "Second step")
        tracker.add("step3", "Third step")
        
        tracker.start("step1", "Processing...")
        tracker.complete("step1", "Done")
        
        tracker.start("step2", "Processing...")
        tracker.complete("step2", "Done")
        
        progress = tracker.get_progress_percentage()
        print(f"[PASS] EnhancedStepTracker progress: {progress:.1f}%")
    except Exception as e:
        print(f"[FAIL] EnhancedStepTracker error: {e}")
        return False
    
    # Test PredictiveAnalyticsEngine
    try:
        # Create a temporary project path for testing
        test_path = Path(__file__).parent
        # Create the analytics directory if it doesn't exist
        analytics_path = test_path / ".goal" / "analytics"
        analytics_path.mkdir(parents=True, exist_ok=True)
        
        engine = PredictiveAnalyticsEngine(test_path)
        
        # Test with sample goal data
        goal_data = {
            "title": "Test Goal",
            "description": "A test goal for authentication system",
            "objectives": ["Implement login", "Implement registration"],
            "success_criteria": ["99.9% uptime", "Password strength validation"],
            "dependencies": ["database-setup"]
        }
        
        complexity = engine.analyze_goal_complexity(goal_data)
        print(f"[PASS] PredictiveAnalyticsEngine complexity analysis: {complexity['total_score']}/10")
        
        estimated_time = engine.estimate_completion_time(goal_data)
        print(f"[PASS] PredictiveAnalyticsEngine time estimation: {estimated_time} days")
        
        risks = engine.identify_risk_factors(goal_data)
        print(f"[PASS] PredictiveAnalyticsEngine risk factors: {risks}")
        
    except Exception as e:
        print(f"[FAIL] PredictiveAnalyticsEngine error: {e}")
        return False
    
    print("All tests passed!")
    return True

if __name__ == "__main__":
    success = test_enhanced_cli()
    sys.exit(0 if success else 1)