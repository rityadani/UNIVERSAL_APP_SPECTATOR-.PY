#!/usr/bin/env python3

import sys
import os
import json
import shutil

# Add rl_reality_v1 to path
rl_reality_path = r"c:\Users\RITESH\rl_reality_v1"
sys.path.append(rl_reality_path)

from universal_rl_agent import UniversalRLAgent

class ConnectedUniversalRL:
    def __init__(self, app_spec_path):
        self.universal_agent = UniversalRLAgent(app_spec_path)
        self.rl_reality_path = rl_reality_path
        
    def connect_to_smart_agent(self):
        """Connect to existing smart_agent.py"""
        try:
            from smart_agent import SmartAgent
            print("✅ Connected to rl_reality_v1 SmartAgent")
            return True
        except ImportError:
            print("❌ Could not import SmartAgent from rl_reality_v1")
            return False
    
    def use_advanced_rl(self, state, valid_actions):
        """Use advanced RL from rl_reality_v1 instead of simple Q-learning"""
        try:
            from advanced_rl_agent import AdvancedRLAgent
            
            # Convert universal state to rl_reality format
            rl_state = {
                'deployment_status': state['status'],
                'error_count': state['error_count'],
                'performance_score': state['performance_score']
            }
            
            # Use advanced RL to choose action
            advanced_agent = AdvancedRLAgent()
            action = advanced_agent.choose_action(rl_state, valid_actions)
            return action
            
        except ImportError:
            # Fallback to universal agent's Q-learning
            return self.universal_agent.choose_action(state)
    
    def sync_policies(self):
        """Sync policies between universal and rl_reality systems"""
        # Copy current policy to rl_reality
        universal_policy = self.universal_agent.get_policy_summary()
        
        policy_file = os.path.join(self.rl_reality_path, 'universal_policy.json')
        with open(policy_file, 'w') as f:
            json.dump(universal_policy, f, indent=2)
        
        print(f"✅ Policy synced to {policy_file}")
    
    def run_integrated_demo(self):
        """Run demo using both systems"""
        print("🔗 INTEGRATED RL DEMO - Universal + rl_reality_v1")
        print("=" * 50)
        
        # Check connection
        if self.connect_to_smart_agent():
            print("🚀 Using advanced RL from rl_reality_v1")
        else:
            print("⚠️  Using fallback Q-learning")
        
        # Run demo scenarios
        scenarios = ["normal", "error", "critical"]
        
        for scenario in scenarios:
            print(f"\n--- Testing {scenario} scenario ---")
            
            # Simulate logs
            logs = self._simulate_logs(scenario)
            state = self.universal_agent.process_logs(logs)
            
            print(f"State: {state['status']} (score: {state['performance_score']})")
            
            # Get valid actions
            valid_actions = self.universal_agent.action_space.get_valid_actions(state)
            
            # Choose action using advanced RL if available
            action = self.use_advanced_rl(state, valid_actions)
            
            if action:
                result = self.universal_agent.execute_action(action, dry_run=True)
                print(f"Action: {action} - {result['message']}")
            else:
                print("No action needed")
        
        # Sync policies
        self.sync_policies()
        print("\n✅ Integration demo complete!")
    
    def _simulate_logs(self, scenario):
        """Simulate logs for different scenarios"""
        scenarios = {
            "normal": ["INFO: Application running normally"],
            "error": ["ERROR: 500 Internal Server Error"],
            "critical": ["CRITICAL: System failure detected"]
        }
        return scenarios.get(scenario, ["INFO: Default log"])

def main():
    """Main integration function"""
    print("🔗 CONNECTING UNIVERSAL RL TO RL_REALITY_V1")
    print("=" * 50)
    
    # Check if rl_reality_v1 exists
    if not os.path.exists(rl_reality_path):
        print(f"❌ rl_reality_v1 not found at {rl_reality_path}")
        print("Please update the path in this script")
        return
    
    # Use example app spec
    app_spec = "spec/example_app_spec.json"
    
    # Create integrated system
    integrated_rl = ConnectedUniversalRL(app_spec)
    
    # Run integrated demo
    integrated_rl.run_integrated_demo()
    
    print("\n🎯 INTEGRATION COMPLETE!")
    print("Your Universal RL is now connected to rl_reality_v1")

if __name__ == "__main__":
    main()