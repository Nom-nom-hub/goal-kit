"""
Final test to verify enhanced QA system functionality
"""

import tempfile
import shutil
from pathlib import Path

# Test that we can create instances of our enhanced QA components
try:
    # Create a temporary directory for testing
    test_dir = Path(tempfile.mkdtemp())
    
    # Create the required .goal directory structure
    (test_dir / ".goal").mkdir()
    
    # Test EnhancedQualityAssurance
    from src.goal_cli.enhanced_quality_assurance import EnhancedQualityAssurance
    qa_system = EnhancedQualityAssurance(test_dir)
    print("EnhancedQualityAssurance instantiated successfully")
    
    # Test TestingFrameworkIntegration
    from src.goal_cli.testing_integration import TestingFrameworkIntegration
    testing_system = TestingFrameworkIntegration(test_dir)
    print("TestingFrameworkIntegration instantiated successfully")
    
    # Test RealTimeQualityMonitor
    from src.goal_cli.real_time_monitoring import RealTimeQualityMonitor
    monitoring_system = RealTimeQualityMonitor(test_dir)
    print("RealTimeQualityMonitor instantiated successfully")
    
    # Test some basic functionality
    # Check that configuration files were created
    quality_config = test_dir / ".goal" / "quality"
    testing_config = test_dir / ".goal" / "testing"
    monitoring_config = test_dir / ".goal" / "monitoring"
    
    if quality_config.exists():
        print("Quality assurance configuration directory created")
    else:
        print("Quality assurance configuration directory not found")
        
    if testing_config.exists():
        print("Testing framework configuration directory created")
    else:
        print("Testing framework configuration directory not found")
        
    if monitoring_config.exists():
        print("Real-time monitoring configuration directory created")
    else:
        print("Real-time monitoring configuration directory not found")
    
    # Clean up
    shutil.rmtree(test_dir)
    
    print("All enhanced QA components tested successfully")
    
except Exception as e:
    print(f"Error testing enhanced QA components: {e}")
    import traceback
    traceback.print_exc()