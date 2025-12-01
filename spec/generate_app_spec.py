import os
import json
import re

def detect_app_type(repo_path):
    """Detect if app is frontend, backend, or fullstack"""
    files = os.listdir(repo_path)
    
    has_frontend = any(f in files for f in ['package.json', 'index.html', 'src'])
    has_backend = any(f in files for f in ['requirements.txt', 'app.py', 'server.js', 'main.py'])
    
    if has_frontend and has_backend:
        return "fullstack"
    elif has_frontend:
        return "frontend"
    elif has_backend:
        return "backend"
    else:
        return "unknown"

def extract_commands(repo_path, app_type):
    """Extract build/start commands based on detected files"""
    commands = {
        "build_command": "",
        "start_command": "",
        "install_command": ""
    }
    
    # Check for package.json (Node.js)
    package_json_path = os.path.join(repo_path, 'package.json')
    if os.path.exists(package_json_path):
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
            scripts = package_data.get('scripts', {})
            commands["build_command"] = scripts.get('build', 'npm run build')
            commands["start_command"] = scripts.get('start', 'npm start')
            commands["install_command"] = "npm install"
    
    # Check for requirements.txt (Python)
    elif os.path.exists(os.path.join(repo_path, 'requirements.txt')):
        commands["install_command"] = "pip install -r requirements.txt"
        
        # Look for main Python file
        python_files = [f for f in os.listdir(repo_path) if f.endswith('.py')]
        main_file = next((f for f in python_files if 'app' in f or 'main' in f), python_files[0] if python_files else 'app.py')
        commands["start_command"] = f"python {main_file}"
        commands["build_command"] = "pip install -r requirements.txt"
    
    # Check for Dockerfile
    elif os.path.exists(os.path.join(repo_path, 'Dockerfile')):
        commands["build_command"] = "docker build -t app ."
        commands["start_command"] = "docker run -p 8000:8000 app"
        commands["install_command"] = "docker build -t app ."
    
    return commands

def detect_port(repo_path):
    """Try to detect default port from common files"""
    port = 8000  # default
    
    # Check package.json
    package_json_path = os.path.join(repo_path, 'package.json')
    if os.path.exists(package_json_path):
        with open(package_json_path, 'r') as f:
            content = f.read()
            port_match = re.search(r'port.*?(\d{4})', content)
            if port_match:
                port = int(port_match.group(1))
    
    # Check Python files for Flask/FastAPI
    for file in os.listdir(repo_path):
        if file.endswith('.py'):
            try:
                with open(os.path.join(repo_path, file), 'r') as f:
                    content = f.read()
                    port_match = re.search(r'port=(\d{4})', content)
                    if port_match:
                        port = int(port_match.group(1))
                        break
            except:
                continue
    
    return port

def generate_app_spec(repo_path):
    """Generate app spec from repository analysis"""
    repo_name = os.path.basename(repo_path)
    app_type = detect_app_type(repo_path)
    commands = extract_commands(repo_path, app_type)
    port = detect_port(repo_path)
    
    spec = {
        "name": repo_name,
        "type": app_type,
        "version": "1.0.0",
        "build_command": commands["build_command"],
        "start_command": commands["start_command"],
        "install_command": commands["install_command"],
        "health_endpoint": f"http://localhost:{port}/health",
        "log_location": "./logs/app.log",
        "port": port,
        "envs": [
            {
                "name": "dev",
                "url": f"http://localhost:{port}",
                "config_file": ".env"
            }
        ],
        "error_patterns": [
            {
                "pattern": "ERROR",
                "severity": "high",
                "description": "General error pattern"
            },
            {
                "pattern": "CRITICAL|FATAL",
                "severity": "critical",
                "description": "Critical system error"
            }
        ],
        "available_actions": [
            {
                "name": "restart_service",
                "command": f"pkill -f {repo_name} && {commands['start_command']} &",
                "risk_level": "medium"
            }
        ]
    }
    
    return spec

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python generate_app_spec.py <repo_path>")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    
    if not os.path.exists(repo_path):
        print(f"Error: Path {repo_path} does not exist")
        sys.exit(1)
    
    spec = generate_app_spec(repo_path)
    
    output_file = "app_spec.generated.json"
    with open(output_file, 'w') as f:
        json.dump(spec, f, indent=2)
    
    print(f"Generated app spec saved to {output_file}")
    print(f"Detected app type: {spec['type']}")