#!/usr/bin/env python3

import subprocess
import sys
import time

def run_everything():
    """Run the complete Universal RL system end-to-end"""
    
    print("🚀 UNIVERSAL RL SYSTEM - COMPLETE EXECUTION")
    print("=" * 50)
    
    steps = [
        ("📋 Generating app specs", "python spec/generate_app_spec.py \"c:\\Users\\RITESH\\coinX-hyperlocal\\backend\""),
        ("🤖 Running Universal RL demo", "python run_universal_demo.py"),
        ("🔄 Testing multi-app support", "python multi_app_demo.py"),
        ("🔗 Connecting to rl_reality_v1", "python connect_to_rl_reality.py"),
        ("✅ Running system validation", "python simple_test.py")
    ]
    
    results = []
    
    for step_name, command in steps:
        print(f"\n{step_name}...")
        
        try:
            result = subprocess.run(command.split(), 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=30)
            
            if result.returncode == 0:
                print(f"✅ SUCCESS")
                results.append((step_name, "PASS"))
            else:
                print(f"❌ FAILED: {result.stderr[:100]}")
                results.append((step_name, "FAIL"))
                
        except subprocess.TimeoutExpired:
            print(f"⏰ TIMEOUT")
            results.append((step_name, "TIMEOUT"))
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            results.append((step_name, "ERROR"))
        
        time.sleep(1)
    
    # Summary
    print(f"\n{'='*50}")
    print("EXECUTION SUMMARY:")
    print("=" * 50)
    
    passed = 0
    for step_name, status in results:
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{status_icon} {step_name}: {status}")
        if status == "PASS":
            passed += 1
    
    print(f"\nRESULT: {passed}/{len(results)} steps completed successfully")
    
    if passed == len(results):
        print("\n🎉 COMPLETE SUCCESS! Universal RL System is fully operational!")
        print("\nNext steps:")
        print("- Run 'streamlit run universal_dashboard.py' to see dashboard")
        print("- Use 'python master_controller.py' for interactive control")
    else:
        print("\n⚠️  Some steps failed. Check error messages above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = run_everything()
    
    if success:
        print("\n🎯 SYSTEM READY! Your Universal RL is connected and operational!")
    else:
        print("\n🔧 SYSTEM NEEDS ATTENTION! Check failed components.")
    
    sys.exit(0 if success else 1)