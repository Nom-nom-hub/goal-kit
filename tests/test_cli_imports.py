"""
Test file to verify CLI integration
"""

# Test that we can import all the necessary modules
try:
    from src.goal_cli.enhanced_quality_assurance import EnhancedQualityAssurance
    print("EnhancedQualityAssurance imported successfully")
except Exception as e:
    print(f"Error importing EnhancedQualityAssurance: {e}")

try:
    from src.goal_cli.testing_integration import TestingFrameworkIntegration
    print("TestingFrameworkIntegration imported successfully")
except Exception as e:
    print(f"Error importing TestingFrameworkIntegration: {e}")

try:
    from src.goal_cli.real_time_monitoring import RealTimeQualityMonitor
    print("RealTimeQualityMonitor imported successfully")
except Exception as e:
    print(f"Error importing RealTimeQualityMonitor: {e}")

try:
    from src.goal_cli.__init__ import app
    print("CLI app imported successfully")
except Exception as e:
    print(f"Error importing CLI app: {e}")

print("All imports completed")