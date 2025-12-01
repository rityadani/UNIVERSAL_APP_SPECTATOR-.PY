#!/usr/bin/env python3

import subprocess
import sys
import json
import os

def run_all_apps_demo():
    """Demo all supported app types"""
    print("UNIVERSAL RL - ALL APPS DEMO")
    print("=" * 40)
    
    # All available app specs
    apps = {
        "Flask Backend": "spec/example_app_spec.json",
        "Django Backend": "spec/django_app_spec.json", 
        "FastAPI Backend": "spec/fastapi_app_spec.json",
        "Spring Boot Backend": "spec/springboot_app_spec.json",
        "React Frontend": "spec/frontend_app_spec.json",
        "Next.js Frontend": "spec/nextjs_app_spec.json",
        "Node.js Backend": "app_spec.generated.json",
        "Docker Container": "spec/docker_app_spec.json"
    }
    
    results = {}
    
    print(f"Testing {len(apps)} different app types...")
    print()
    
    for app_name, spec_file in apps.items():
        if os.path.exists(spec_file):
            print(f"Testing {app_name}...")
            
            # Run RL demo for this app
            result = subprocess.run([
                sys.executable, "run_universal_demo.py", spec_file
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {app_name}: SUCCESS")
                results[app_name] = "PASS"
            else:
                print(f"❌ {app_name}: FAILED")
                results[app_name] = "FAIL"
        else:
            print(f"⏭️  {app_name}: SPEC NOT FOUND")
            results[app_name] = "SKIP"
        
        print()
    
    # Save comprehensive results
    with open('reports/all_apps_results.json', 'w') as f:
        json.dump({
            "total_apps": len(apps),
            "tested_apps": len([r for r in results.values() if r != "SKIP"]),
            "passed_apps": len([r for r in results.values() if r == "PASS"]),
            "results": results,
            "summary": "Universal RL tested across multiple app types"
        }, f, indent=2)
    
    # Final summary
    print("=" * 40)
    print("FINAL RESULTS:")
    print("=" * 40)
    
    passed = sum(1 for r in results.values() if r == "PASS")
    total_tested = sum(1 for r in results.values() if r != "SKIP")
    
    for app_name, status in results.items():
        status_icon = {"PASS": "✅", "FAIL": "❌", "SKIP": "⏭️"}[status]
        print(f"{status_icon} {app_name}: {status}")
    
    print()
    print(f"SUCCESS RATE: {passed}/{total_tested} apps passed")
    print(f"UNIVERSAL RL WORKS WITH {passed} DIFFERENT APP TYPES!")
    
    if passed >= 5:
        print("🎉 EXCELLENT! Universal system is truly universal!")
    elif passed >= 3:
        print("🚀 GOOD! System works across multiple app types!")
    else:
        print("⚠️  NEEDS WORK: Some apps need attention")
    
    return results

if __name__ == "__main__":
    results = run_all_apps_demo()
    print(f"\nDetailed results saved to: reports/all_apps_results.json")