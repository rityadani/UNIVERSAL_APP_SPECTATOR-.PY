import json

class AppActionSpace:
    def __init__(self, app_spec):
        self.app_spec = app_spec
        self.actions = {action['name']: action for action in app_spec['available_actions']}
        self.action_names = list(self.actions.keys())
    
    def get_valid_actions(self, current_state):
        """Get list of valid actions based on current state"""
        valid_actions = []
        
        # Basic safety rules
        for action_name, action in self.actions.items():
            if self._is_action_safe(action, current_state):
                valid_actions.append(action_name)
        
        return valid_actions
    
    def _is_action_safe(self, action, state):
        """Check if action is safe to execute in current state"""
        risk_level = action['risk_level']
        app_status = state.get('status', 'healthy')
        env = state.get('env', 'dev')
        
        # High-risk actions only in dev environment
        if risk_level == 'high' and env != 'dev':
            return False
        
        # Don't restart if already healthy
        if action['name'] == 'restart_service' and app_status == 'healthy':
            return False
        
        return True
    
    def execute_action(self, action_name, dry_run=True):
        """Execute an action (dry_run=True for simulation)"""
        if action_name not in self.actions:
            return {"success": False, "error": f"Unknown action: {action_name}"}
        
        action = self.actions[action_name]
        command = action['command']
        
        if dry_run:
            return {
                "success": True,
                "action": action_name,
                "command": command,
                "risk_level": action['risk_level'],
                "executed": False,
                "message": f"Would execute: {command}"
            }
        else:
            # In real implementation, execute the command
            import subprocess
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                return {
                    "success": result.returncode == 0,
                    "action": action_name,
                    "command": command,
                    "executed": True,
                    "output": result.stdout,
                    "error": result.stderr
                }
            except Exception as e:
                return {
                    "success": False,
                    "action": action_name,
                    "error": str(e)
                }
    
    def get_action_space_size(self):
        """Get the size of action space for RL algorithms"""
        return len(self.action_names)
    
    def action_to_index(self, action_name):
        """Convert action name to index for RL algorithms"""
        return self.action_names.index(action_name)
    
    def index_to_action(self, index):
        """Convert index to action name for RL algorithms"""
        return self.action_names[index]

def create_action_space(app_spec_path):
    """Factory function to create action space from app spec file"""
    with open(app_spec_path, 'r') as f:
        app_spec = json.load(f)
    return AppActionSpace(app_spec)