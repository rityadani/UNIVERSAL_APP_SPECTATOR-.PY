#!/usr/bin/env python3

import json
import time
from universal_rl_agent import UniversalRLAgent

def simulate_app_logs(scenario="normal"):
    """Generate simulated log lines for different scenarios"""
    if scenario == "normal":
        return [
            "INFO: Application started successfully",
            "INFO: Processing request /api/users",
            "INFO: Database connection established"
        ]
    elif scenario == "error":
        return [
            "ERROR: 500 Internal Server Error in /api/orders",
            "ERROR: Database connection timeout",
            "WARNING: High memory usage detected"
        ]
    elif scenario == "critical":
        return [
            "CRITICAL: Database connection failed",
            "ERROR: Multiple service failures detected",
            "FATAL: Application crash imminent"
        ]

def calculate_reward(old_state, new_state, action_result):
    """Calculate reward based on state transition"""
    if not action_result.get('success', False):
        return -10  # Failed action
    
    old_score = old_state.get('performance_score', 50) if old_state else 50
    new_score = new_state.get('performance_score', 50)
    
    # Reward improvement
    improvement = new_score - old_score
    
    # Bonus for fixing critical issues
    if old_state and old_state.get('status') == 'critical' and new_state.get('status') != 'critical':
        improvement += 20
    
    return improvement

def run_demo(app_spec_path):
    """Run a complete demo of the universal RL system"""
    print(f"Starting Universal RL Demo")
    print(f"Loading app spec: {app_spec_path}")
    
    # Initialize agent
    agent = UniversalRLAgent(app_spec_path)
    
    print(f"Agent initialized for app: {agent.app_spec['name']}")
    print(f"Available actions: {agent.action_space.action_names}")
    
    # Simulation scenarios
    scenarios = [
        ("normal", "Normal operation"),
        ("error", "Error detected"),
        ("critical", "Critical failure"),
        ("normal", "Recovery check")
    ]
    
    results = []
    
    for i, (scenario, description) in enumerate(scenarios):
        print(f"\n--- Step {i+1}: {description} ---")
        
        # Generate logs for scenario
        logs = simulate_app_logs(scenario)
        print(f"Logs: {logs[0][:50]}...")
        
        # Process logs and get state
        old_state = agent.current_state
        current_state = agent.process_logs(logs)
        print(f"State: {current_state['status']} (score: {current_state['performance_score']})")
        
        # Choose and execute action
        action = agent.choose_action()
        if action:
            print(f"Chosen action: {action}")
            action_result = agent.execute_action(action, dry_run=True)
            print(f"Action result: {action_result['message']}")
            
            # Calculate reward and update
            reward = calculate_reward(old_state, current_state, action_result)
            agent.update_q_value(reward)
            print(f"Reward: {reward}")
            
            results.append({
                "step": i+1,
                "scenario": scenario,
                "state": current_state,
                "action": action,
                "reward": reward,
                "action_success": action_result['success']
            })
        else:
            print("No action needed")
            results.append({
                "step": i+1,
                "scenario": scenario,
                "state": current_state,
                "action": None,
                "reward": 0,
                "action_success": True
            })
        
        time.sleep(1)  # Simulate time passing
    
    # Save results
    with open('reports/demo_results.json', 'w') as f:
        json.dump({
            "app_name": agent.app_spec['name'],
            "total_steps": len(results),
            "results": results,
            "final_policy": agent.get_policy_summary()
        }, f, indent=2)
    
    # Summary
    print(f"\nDemo Complete!")
    print(f"Total steps: {len(results)}")
    print(f"Q-table entries: {len(agent.q_table)}")
    
    total_reward = sum(r['reward'] for r in results)
    print(f"Total reward: {total_reward}")
    
    successful_actions = sum(1 for r in results if r['action'] and r['action_success'])
    print(f"Successful actions: {successful_actions}/{len([r for r in results if r['action']])}")
    
    return results

if __name__ == "__main__":
    import sys
    
    # Use example spec if no path provided
    spec_path = sys.argv[1] if len(sys.argv) > 1 else "spec/example_app_spec.json"
    
    try:
        results = run_demo(spec_path)
        print(f"\nResults saved to reports/demo_results.json")
    except Exception as e:
        print(f"Demo failed: {e}")
        sys.exit(1)