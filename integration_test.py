import os
import subprocess
import sys

def run_integration_test():
    print("UNIVERSAL RL SYSTEM - INTEGRATION TEST")
    print("=" * 40)
    
    # Test 1: Repo scanner
    print("1. Testing repo scanner...")
    result = subprocess.run([sys.executable, "spec/generate_app_spec.py", r"c:\Users\RITESH\coinX-hyperlocal\backend"], capture_output=True)
    print("PASS" if result.returncode == 0 else "FAIL")
    
    # Test 2: Universal agent
    print("2. Testing universal agent...")
    result = subprocess.run([sys.executable, "run_universal_demo.py"], capture_output=True)
    print("PASS" if result.returncode == 0 else "FAIL")
    
    # Test 3: Multi-app
    print("3. Testing multi-app...")
    if os.path.exists("app_spec.generated.json"):
        result = subprocess.run([sys.executable, "run_universal_demo.py", "app_spec.generated.json"], capture_output=True)
        print("PASS" if result.returncode == 0 else "FAIL")
    else:
        print("SKIP")
    
    print("Integration test complete!")

if __name__ == "__main__":
    run_integration_test()