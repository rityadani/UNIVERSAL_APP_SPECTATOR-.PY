import os

def test_all_files():
    print("UNIVERSAL RL SYSTEM - FILE CHECK")
    print("=" * 40)
    
    required_files = [
        # Day 1
        "spec/app_spec_schema.md",
        "spec/example_app_spec.json",
        
        # Day 2  
        "spec/generate_app_spec.py",
        
        # Day 3
        "rl/app_state_mapper.py", 
        "rl/app_action_space.py",
        
        # Day 4
        "universal_rl_agent.py",
        "run_universal_demo.py",
        
        # Day 5
        "multi_app_demo.py",
        
        # Day 6
        "universal_dashboard.py",
        
        # Day 7
        "integration_test.py",
        "UNIVERSAL_SPEC_GUIDE.md",
        "FINAL_SUMMARY.md"
    ]
    
    present = 0
    for file in required_files:
        if os.path.exists(file):
            print(f"PASS: {file}")
            present += 1
        else:
            print(f"MISSING: {file}")
    
    print(f"\nRESULT: {present}/{len(required_files)} files present")
    
    if present == len(required_files):
        print("SUCCESS: All 7 days completed!")
    else:
        print("INCOMPLETE: Some files missing")

if __name__ == "__main__":
    test_all_files()