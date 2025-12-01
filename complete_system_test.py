#!/usr/bin/env python3

import os
import subprocess
import sys
import json

def test_day_1():
    """Test Day 1 - App Spec Schema"""
    print("DAY 1 - Testing App Spec Schema")
    
    required_files = [
        "spec/app_spec_schema.md",
        "spec/example_app_spec.json"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            return False
    return True

def test_day_2():
    """Test Day 2 - Repo Scanner"""
    print("\nDAY 2 - Testing Repo Scanner")
    
    if not os.path.exists("spec/generate_app_spec.py"):
        print("❌ generate_app_spec.py missing")
        return False
    
    # Test with coinX backend
    result = subprocess.run([
        sys.executable, "spec/generate_app_spec.py", 
        r"c:\Users\RITESH\coinX-hyperlocal\backend"
    ], capture_output=True)
    
    if result.returncode == 0 and os.path.exists("app_spec.generated.json"):
        print("✅ Repo scanner working")
        return True
    else:
        print("❌ Repo scanner failed")
        return False

def test_day_3():
    """Test Day 3 - RL Mapping"""
    print("\nDAY 3 - Testing RL Mapping")
    
    required_files = [
        "rl/app_state_mapper.py",
        "rl/app_action_space.py"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            return False
    return True

def test_day_4():
    """Test Day 4 - Universal RL Agent"""
    print("\nDAY 4 - Testing Universal RL Agent")
    
    if not os.path.exists("universal_rl_agent.py"):
        print("❌ universal_rl_agent.py missing")
        return False
    
    # Test basic demo
    result = subprocess.run([
        sys.executable, "run_universal_demo.py"
    ], capture_output=True)
    
    if result.returncode == 0:
        print("✅ Universal RL Agent working")
        return True
    else:
        print("❌ Universal RL Agent failed")
        return False

def test_day_5():
    """Test Day 5 - Multi-App Demo"""
    print("\nDAY 5 - Testing Multi-App Demo")
    
    # Run multi-app test
    result = subprocess.run([
        sys.executable, "multi_app_demo.py"
    ], capture_output=True)
    
    if result.returncode == 0 and os.path.exists("reports/multi_app_results.json"):
        print("✅ Multi-app demo working")
        return True
    else:
        print("❌ Multi-app demo failed")
        return False

def test_day_6():
    """Test Day 6 - Dashboard"""
    print("\nDAY 6 - Testing Dashboard")
    
    dashboards = ["universal_dashboard.py", "enhanced_dashboard.py"]
    
    for dashboard in dashboards:
        if os.path.exists(dashboard):
            print(f"✅ {dashboard}")
        else:
            print(f"❌ {dashboard}")
            return False
    return True

def test_day_7():
    """Test Day 7 - Integration & Cleanup"""
    print("\nDAY 7 - Testing Integration & Cleanup")
    
    required_files = [
        "UNIVERSAL_SPEC_GUIDE.md",
        "integration_test.py",
        "test_with_vinayak.py",
        "DEPLOYMENT_CHECKLIST.md"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            return False
    return True

def run_complete_test():
    """Run complete 7-day system test"""
    print("UNIVERSAL RL SYSTEM - COMPLETE 7-DAY TEST")
    print("=" * 50)
    
    tests = [
        test_day_1,
        test_day_2, 
        test_day_3,
        test_day_4,
        test_day_5,
        test_day_6,
        test_day_7
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n{'='*50}")
    print(f"FINAL RESULT: {passed}/{len(tests)} days completed successfully")
    
    if passed == len(tests):
        print("🎉 ALL 7 DAYS COMPLETED! Universal RL System is ready!")
    else:
        print("⚠️  Some components need attention")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = run_complete_test()
    sys.exit(0 if success else 1)