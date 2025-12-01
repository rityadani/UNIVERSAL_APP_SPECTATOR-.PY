# Universal App Spec Guide

## Overview
This guide shows how to use the Universal RL system to manage any application through standardized specifications.

## Quick Start

### 1. Generate App Spec from Repository
```bash
python spec/generate_app_spec.py /path/to/your/repo
```
This creates `app_spec.generated.json` with auto-detected configuration.

### 2. Run RL Demo
```bash
python run_universal_demo.py app_spec.generated.json
```
This runs a simulation showing how RL manages your app.

### 3. View Dashboard
```bash
streamlit run universal_dashboard.py
```
This opens a web interface to monitor multiple apps.

## Manual App Spec Creation

### Basic Structure
```json
{
  "name": "my-app",
  "type": "backend|frontend|fullstack",
  "version": "1.0.0",
  "build_command": "npm run build",
  "start_command": "npm start",
  "install_command": "npm install",
  "health_endpoint": "http://localhost:3000/health",
  "log_location": "./logs/app.log",
  "port": 3000,
  "envs": [...],
  "error_patterns": [...],
  "available_actions": [...]
}
```

### Required Fields
- `name`: Unique app identifier
- `type`: Application type (backend/frontend/fullstack)
- `build_command`: How to build the app
- `start_command`: How to start the app
- `health_endpoint`: URL to check app health
- `available_actions`: Actions RL can take

### Error Patterns
Define what errors to watch for:
```json
{
  "pattern": "ERROR.*500.*Internal Server Error",
  "severity": "high",
  "description": "Internal server error"
}
```

### Actions
Define what RL can do:
```json
{
  "name": "restart_service",
  "command": "systemctl restart myapp",
  "risk_level": "medium"
}
```

## Integration with Existing RL

### Using with Your Current RL System
```python
from universal_rl_agent import UniversalRLAgent

# Initialize with your app spec
agent = UniversalRLAgent('my_app_spec.json')

# Process logs
state = agent.process_logs(log_lines)

# Choose action
action = agent.choose_action()

# Execute action
result = agent.execute_action(action, dry_run=False)

# Update learning
reward = calculate_reward(old_state, new_state, result)
agent.update_q_value(reward)
```

### Connecting to Real Systems
Replace the demo simulation with real integrations:

1. **Log Processing**: Connect to your actual log sources
2. **Action Execution**: Remove `dry_run=True` for real actions
3. **Reward Calculation**: Use real metrics (uptime, response time, etc.)
4. **State Monitoring**: Connect to your monitoring systems

## File Structure
```
UNIVERSAL_APP.PY/
├── spec/
│   ├── app_spec_schema.md          # Schema documentation
│   ├── example_app_spec.json       # Example specification
│   └── generate_app_spec.py        # Auto-generator
├── rl/
│   ├── app_state_mapper.py         # Log → RL state conversion
│   └── app_action_space.py         # Action management
├── universal_rl_agent.py           # Main RL agent
├── run_universal_demo.py           # Demo runner
├── universal_dashboard.py          # Web dashboard
└── reports/
    └── demo_results.json           # Demo outputs
```

## Best Practices

### 1. Start Simple
- Begin with basic error patterns
- Use safe actions first (clear cache, restart)
- Test in dev environment

### 2. Gradual Expansion
- Add more sophisticated error detection
- Include performance metrics
- Add production-safe actions

### 3. Safety First
- Always test actions in dev first
- Use risk levels appropriately
- Implement rollback mechanisms

### 4. Monitoring
- Track RL performance over time
- Monitor false positives/negatives
- Adjust reward functions based on results

## Troubleshooting

### Common Issues
1. **Unicode errors**: Remove emojis from output
2. **Missing dependencies**: Install required packages
3. **Permission errors**: Ensure proper file permissions
4. **Action failures**: Check command syntax and permissions

### Debug Mode
Add debug logging to see what's happening:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Next Steps
1. Connect to your existing RL system in `rl_reality_v1`
2. Replace simulation with real log sources
3. Add more sophisticated reward functions
4. Implement safety mechanisms for production use