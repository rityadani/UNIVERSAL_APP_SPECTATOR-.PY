#!/usr/bin/env python3

import subprocess
import sys
import os

def connect_everything():
    print("UNIVERSAL RL SYSTEM - COMPLETE CONNECTION")
    print("=" * 50)
    
    # Step 1: Generate specs
    print("\n1. Generating app specifications...")
    result1 = subprocess.run([
        sys.executable, "spec/generate_app_spec.py", 
        r"c:\Users\RITESH\coinX-hyperlocal\backend"
    ], capture_output=True)
    print("PASS" if result1.returncode == 0 else "FAIL")
    
    # Step 2: Run universal demo
    print("\n2. Running Universal RL demo...")
    result2 = subprocess.run([
        sys.executable, "run_universal_demo.py"
    ], capture_output=True)
    print("PASS" if result2.returncode == 0 else "FAIL")
    
    # Step 3: Test multi-app
    print("\n3. Testing multi-app support...")
    result3 = subprocess.run([
        sys.executable, "multi_app_demo.py"
    ], capture_output=True)
    print("PASS" if result3.returncode == 0 else "FAIL")
    
    # Step 4: Validate system
    print("\n4. Validating complete system...")
    result4 = subprocess.run([
        sys.executable, "simple_test.py"
    ], capture_output=True)
    print("PASS" if result4.returncode == 0 else "FAIL")
    
    # Summary
    results = [result1, result2, result3, result4]
    passed = sum(1 for r in results if r.returncode == 0)
    
    print(f"\nFINAL RESULT: {passed}/4 components working")
    
    if passed == 4:
        print("\nSUCCESS! Universal RL System fully connected!")
        print("\nYour system can now:")
        print("- Manage any app through specs")
        print("- Use same RL brain for all apps") 
        print("- Auto-generate configurations")
        print("- Monitor through dashboard")
        
        print("\nNext commands:")
        print("- streamlit run universal_dashboard.py (dashboard)")
        print("- python master_controller.py (interactive control)")
        
    else:
        print("\nSome components need attention. Check individual results.")
    
    return passed == 4

if __name__ == "__main__":
    success = connect_everything()
    
    if success:
        print("\nYour Universal RL ecosystem is ready!")
    else:
        print("\nSome setup needed. Check error messages.")
    
    sys.exit(0 if success else 1)