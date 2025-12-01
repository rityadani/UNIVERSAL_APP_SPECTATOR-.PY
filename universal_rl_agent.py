import json
import random
import numpy as np
from rl.app_state_mapper import AppStateMapper
from rl.app_action_space import AppActionSpace

class UniversalRLAgent:
    def __init__(self, app_spec_path):
        with open(app_spec_path, 'r') as f:
            self.app_spec = json.load(f)
        
        self.state_mapper = AppStateMapper(self.app_spec)
        self.action_space = AppActionSpace(self.app_spec)
        
        # Simple Q-table for demonstration
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1
        
        self.current_state = None
        self.last_action = None
    
    def process_logs(self, log_lines):
        """Process new log lines and update current state"""
        self.current_state = self.state_mapper.extract_state_from_logs(log_lines)
        return self.current_state
    
    def choose_action(self, state=None):
        """Choose action using epsilon-greedy policy"""
        if state is None:
            state = self.current_state
        
        if state is None:
            return None
        
        valid_actions = self.action_space.get_valid_actions(state)
        if not valid_actions:
            return None
        
        state_key = self._state_to_key(state)
        
        # Epsilon-greedy action selection
        if random.random() < self.epsilon or state_key not in self.q_table:
            action = random.choice(valid_actions)
        else:
            # Choose action with highest Q-value
            q_values = self.q_table[state_key]
            valid_q_values = {a: q_values.get(a, 0) for a in valid_actions}
            action = max(valid_q_values, key=valid_q_values.get)
        
        self.last_action = action
        return action
    
    def execute_action(self, action_name, dry_run=True):
        """Execute chosen action"""
        return self.action_space.execute_action(action_name, dry_run)
    
    def update_q_value(self, reward, next_state=None):
        """Update Q-value based on reward"""
        if self.current_state is None or self.last_action is None:
            return
        
        state_key = self._state_to_key(self.current_state)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        
        current_q = self.q_table[state_key].get(self.last_action, 0)
        
        if next_state:
            next_state_key = self._state_to_key(next_state)
            next_max_q = 0
            if next_state_key in self.q_table:
                next_max_q = max(self.q_table[next_state_key].values()) if self.q_table[next_state_key] else 0
        else:
            next_max_q = 0
        
        # Q-learning update
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        self.q_table[state_key][self.last_action] = new_q
    
    def _state_to_key(self, state):
        """Convert state dict to string key for Q-table"""
        return f"{state['status']}_{state['env']}_{state['error_count']}_{state['error_severity']}"
    
    def get_policy_summary(self):
        """Get current policy summary"""
        return {
            "app_name": self.app_spec['name'],
            "q_table_size": len(self.q_table),
            "available_actions": self.action_space.action_names,
            "current_state": self.current_state,
            "epsilon": self.epsilon
        }
    
    def save_policy(self, filepath):
        """Save current policy to file"""
        policy_data = {
            "app_spec": self.app_spec,
            "q_table": self.q_table,
            "hyperparameters": {
                "learning_rate": self.learning_rate,
                "discount_factor": self.discount_factor,
                "epsilon": self.epsilon
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(policy_data, f, indent=2)
    
    def load_policy(self, filepath):
        """Load policy from file"""
        with open(filepath, 'r') as f:
            policy_data = json.load(f)
        
        self.q_table = policy_data.get('q_table', {})
        hyperparams = policy_data.get('hyperparameters', {})
        self.learning_rate = hyperparams.get('learning_rate', 0.1)
        self.discount_factor = hyperparams.get('discount_factor', 0.9)
        self.epsilon = hyperparams.get('epsilon', 0.1)