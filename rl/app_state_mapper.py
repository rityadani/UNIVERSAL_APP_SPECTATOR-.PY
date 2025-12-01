import json
import re
from datetime import datetime

class AppStateMapper:
    def __init__(self, app_spec):
        self.app_spec = app_spec
        self.app_name = app_spec['name']
        self.error_patterns = {p['pattern']: p['severity'] for p in app_spec['error_patterns']}
    
    def extract_state_from_logs(self, log_lines):
        """Convert log lines to RL state representation"""
        state = {
            "app": self.app_name,
            "env": "dev",  # default
            "status": "healthy",
            "error_count": 0,
            "error_severity": "none",
            "timestamp": datetime.now().isoformat(),
            "performance_score": 100
        }
        
        error_count = 0
        max_severity = "none"
        
        for line in log_lines:
            # Check for error patterns
            for pattern, severity in self.error_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    error_count += 1
                    if self._severity_level(severity) > self._severity_level(max_severity):
                        max_severity = severity
            
            # Extract environment if mentioned
            env_match = re.search(r'env[ironment]*[:\s]*(\w+)', line, re.IGNORECASE)
            if env_match:
                state["env"] = env_match.group(1).lower()
        
        # Determine overall status
        if error_count == 0:
            state["status"] = "healthy"
        elif error_count < 5:
            state["status"] = "degraded"
        else:
            state["status"] = "critical"
        
        state["error_count"] = error_count
        state["error_severity"] = max_severity
        state["performance_score"] = max(0, 100 - (error_count * 10))
        
        return state
    
    def _severity_level(self, severity):
        """Convert severity to numeric level"""
        levels = {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
        return levels.get(severity, 0)
    
    def state_to_vector(self, state):
        """Convert state dict to numeric vector for RL"""
        # Simple encoding for RL algorithms
        status_encoding = {"healthy": 0, "degraded": 1, "critical": 2}
        env_encoding = {"dev": 0, "stage": 1, "prod": 2}
        severity_encoding = {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
        
        vector = [
            status_encoding.get(state["status"], 0),
            env_encoding.get(state["env"], 0),
            min(state["error_count"], 10),  # cap at 10
            severity_encoding.get(state["error_severity"], 0),
            state["performance_score"] / 100.0  # normalize to 0-1
        ]
        
        return vector

def create_state_mapper(app_spec_path):
    """Factory function to create state mapper from app spec file"""
    with open(app_spec_path, 'r') as f:
        app_spec = json.load(f)
    return AppStateMapper(app_spec)