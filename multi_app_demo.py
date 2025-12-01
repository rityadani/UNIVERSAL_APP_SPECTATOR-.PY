import subprocess
import sys
import json

def run_multi_app_demo():
    """Day 5 - Multi-App Demo"""
    print("DAY 5 - MULTI-APP DEMO")
    print("=" * 30)
    
    apps = [
        ("Flask Backend", "spec/example_app_spec.json"),
        ("Node.js Backend", "app_spec.generated.json")
    ]
    
    results = {}
    
    for app_name, spec_file in apps:
        print(f"\nTesting {app_name}...")
        
        result = subprocess.run([
            sys.executable, "run_universal_demo.py", spec_file
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"SUCCESS: {app_name} managed by RL")
            results[app_name] = "PASS"
        else:
            print(f"FAILED: {app_name}")
            results[app_name] = "FAIL"
    
    # Save multi-app results
    with open('reports/multi_app_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nMulti-app demo complete: {results}")

if __name__ == "__main__":
    run_multi_app_demo()