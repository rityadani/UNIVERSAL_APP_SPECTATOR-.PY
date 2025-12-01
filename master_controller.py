#!/usr/bin/env python3

import subprocess
import sys
import os
import json

class MasterController:
    """Master controller for the entire Universal RL ecosystem"""
    
    def __init__(self):
        self.base_path = os.getcwd()
        self.rl_reality_path = r"c:\Users\RITESH\rl_reality_v1"
    
    def setup_environment(self):
        """Setup the complete environment"""
        print("🚀 SETTING UP UNIVERSAL RL ECOSYSTEM")
        print("=" * 40)
        
        # Install dependencies
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      capture_output=True)
        
        # Generate app specs for existing projects
        self.generate_all_specs()
        
        print("✅ Environment setup complete!")
    
    def generate_all_specs(self):
        """Generate specs for all available apps"""
        print("\n📋 Generating app specifications...")
        
        apps_to_scan = [
            (r"c:\Users\RITESH\coinX-hyperlocal\backend", "coinx-backend"),
            (r"c:\Users\RITESH\coinX-hyperlocal\frontend", "coinx-frontend")
        ]
        
        for app_path, app_name in apps_to_scan:
            if os.path.exists(app_path):
                print(f"Scanning {app_name}...")
                result = subprocess.run([
                    sys.executable, "spec/generate_app_spec.py", app_path
                ], capture_output=True)
                
                if result.returncode == 0:
                    # Rename generated spec
                    if os.path.exists("app_spec.generated.json"):
                        os.rename("app_spec.generated.json", f"spec/{app_name}_spec.json")
                    print(f"✅ {app_name} spec generated")
                else:
                    print(f"❌ {app_name} spec failed")
    
    def run_complete_demo(self):
        """Run complete system demonstration"""
        print("\n🎬 RUNNING COMPLETE SYSTEM DEMO")
        print("=" * 40)
        
        # 1. Test Universal RL
        print("1. Testing Universal RL Agent...")
        result = subprocess.run([sys.executable, "run_universal_demo.py"], 
                              capture_output=True)
        print("✅ Universal RL" if result.returncode == 0 else "❌ Universal RL")
        
        # 2. Test Multi-App
        print("2. Testing Multi-App Support...")
        result = subprocess.run([sys.executable, "multi_app_demo.py"], 
                              capture_output=True)
        print("✅ Multi-App" if result.returncode == 0 else "❌ Multi-App")
        
        # 3. Test Integration
        print("3. Testing rl_reality_v1 Integration...")
        result = subprocess.run([sys.executable, "connect_to_rl_reality.py"], 
                              capture_output=True)
        print("✅ Integration" if result.returncode == 0 else "❌ Integration")
    
    def start_dashboard(self):
        """Start the monitoring dashboard"""
        print("\n📊 Starting Dashboard...")
        print("Dashboard will open at http://localhost:8501")
        
        try:
            subprocess.run(["streamlit", "run", "universal_dashboard.py"])
        except FileNotFoundError:
            print("❌ Streamlit not installed. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"])
            subprocess.run(["streamlit", "run", "universal_dashboard.py"])
    
    def show_status(self):
        """Show complete system status"""
        print("\n📊 UNIVERSAL RL SYSTEM STATUS")
        print("=" * 40)
        
        # Check files
        required_files = [
            "spec/app_spec_schema.md",
            "spec/example_app_spec.json", 
            "universal_rl_agent.py",
            "run_universal_demo.py",
            "universal_dashboard.py"
        ]
        
        print("Core Files:")
        for file in required_files:
            status = "✅" if os.path.exists(file) else "❌"
            print(f"  {status} {file}")
        
        # Check generated specs
        print("\nGenerated Specs:")
        spec_files = [f for f in os.listdir("spec") if f.endswith("_spec.json")]
        for spec in spec_files:
            print(f"  ✅ spec/{spec}")
        
        # Check results
        print("\nResults:")
        if os.path.exists("reports/demo_results.json"):
            with open("reports/demo_results.json", 'r') as f:
                results = json.load(f)
            print(f"  ✅ Last demo: {results['app_name']} ({results['total_steps']} steps)")
        
        # Integration status
        print("\nIntegration:")
        rl_status = "✅" if os.path.exists(self.rl_reality_path) else "❌"
        print(f"  {rl_status} rl_reality_v1 connection")
    
    def interactive_menu(self):
        """Interactive menu for system control"""
        while True:
            print("\n🎛️  UNIVERSAL RL MASTER CONTROLLER")
            print("=" * 40)
            print("1. Setup Environment")
            print("2. Generate App Specs")
            print("3. Run Complete Demo")
            print("4. Start Dashboard")
            print("5. Show System Status")
            print("6. Connect to rl_reality_v1")
            print("0. Exit")
            
            choice = input("\nEnter choice (0-6): ")
            
            if choice == "1":
                self.setup_environment()
            elif choice == "2":
                self.generate_all_specs()
            elif choice == "3":
                self.run_complete_demo()
            elif choice == "4":
                self.start_dashboard()
            elif choice == "5":
                self.show_status()
            elif choice == "6":
                subprocess.run([sys.executable, "connect_to_rl_reality.py"])
            elif choice == "0":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice")

def main():
    """Main entry point"""
    controller = MasterController()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "setup":
            controller.setup_environment()
        elif command == "demo":
            controller.run_complete_demo()
        elif command == "dashboard":
            controller.start_dashboard()
        elif command == "status":
            controller.show_status()
        else:
            print(f"Unknown command: {command}")
    else:
        controller.interactive_menu()

if __name__ == "__main__":
    main()