# Universal App-Spec Interpreter for RL

A universal system that allows RL agents to manage any application through standardized specifications.

## What This Does

This system creates a "universal language" between arbitrary codebases and RL engines. Instead of hardcoding RL logic for each app, you define a simple JSON spec that describes:

- How to build/start the app
- What errors to watch for  
- What actions the RL agent can take
- How to monitor app health

The RL agent then uses this spec to automatically manage any application.

## Quick Demo

```bash
# 1. Generate spec for any repo
python spec/generate_app_spec.py /path/to/your/repo

# 2. Run RL simulation
python run_universal_demo.py app_spec.generated.json

# 3. View results dashboard
streamlit run universal_dashboard.py
```

## Key Components

- **App Spec Schema**: Standard format for describing any app
- **Repo Scanner**: Auto-generates specs from codebases
- **State Mapper**: Converts logs → RL states
- **Action Space**: Defines what RL can do
- **Universal Agent**: RL brain that works with any spec

## Example App Spec

```json
{
  "name": "my-api",
  "type": "backend",
  "start_command": "python app.py",
  "health_endpoint": "http://localhost:5000/health",
  "error_patterns": [
    {
      "pattern": "ERROR.*500",
      "severity": "high",
      "description": "Server error"
    }
  ],
  "available_actions": [
    {
      "name": "restart_service",
      "command": "systemctl restart myapp",
      "risk_level": "medium"
    }
  ]
}
```

## Integration with Existing RL

This builds on top of your existing RL work in `rl_reality_v1`. The universal layer:

1. **Standardizes Input**: Any app → standard state format
2. **Standardizes Actions**: Any app → standard action interface  
3. **Enables Reuse**: Same RL brain works across all apps

## Files

- `spec/` - App specification tools
- `rl/` - State/action mapping components
- `universal_rl_agent.py` - Main RL agent
- `run_universal_demo.py` - Demo runner
- `universal_dashboard.py` - Web dashboard

## Next Steps

1. Connect to your production RL system
2. Add real log sources (replace simulation)
3. Implement safety mechanisms
4. Scale to multiple apps

See `UNIVERSAL_SPEC_GUIDE.md` for detailed usage instructions.