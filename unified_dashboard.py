import json
import os
import subprocess
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import threading

def load_all_apps():
    apps = {}
    
    # Backend specs
    if os.path.exists('spec/example_app_spec.json'):
        with open('spec/example_app_spec.json', 'r') as f:
            apps['flask-backend'] = json.load(f)
    
    if os.path.exists('app_spec.generated.json'):
        with open('app_spec.generated.json', 'r') as f:
            apps['coinx-backend'] = json.load(f)
    
    # Frontend specs
    if os.path.exists('spec/frontend_app_spec.json'):
        with open('spec/frontend_app_spec.json', 'r') as f:
            apps['coinx-frontend'] = json.load(f)
    
    return apps

def load_results():
    if os.path.exists('reports/demo_results.json'):
        with open('reports/demo_results.json', 'r') as f:
            return json.load(f)
    return None

def run_demo_for_app(app_key, apps):
    """Run demo for specific app"""
    spec_files = {
        'flask-backend': 'spec/example_app_spec.json',
        'coinx-backend': 'app_spec.generated.json',
        'coinx-frontend': 'spec/frontend_app_spec.json'
    }
    
    spec_file = spec_files.get(app_key)
    if spec_file and os.path.exists(spec_file):
        result = subprocess.run([sys.executable, "run_universal_demo.py", spec_file], 
                              capture_output=True)
        return result.returncode == 0
    return False

def create_unified_html():
    apps = load_all_apps()
    results = load_results()
    
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Universal RL Dashboard - Frontend & Backend</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; text-align: center; }
        .section { background: white; padding: 25px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .app-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .app-card { background: white; border: 2px solid #e1e8ed; border-radius: 12px; padding: 20px; transition: all 0.3s ease; }
        .app-card:hover { border-color: #3498db; transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.15); }
        .app-card.backend { border-left: 5px solid #e74c3c; }
        .app-card.frontend { border-left: 5px solid #2ecc71; }
        .app-title { font-size: 20px; font-weight: bold; margin-bottom: 10px; }
        .app-type { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; text-transform: uppercase; }
        .type-backend { background: #ffe6e6; color: #e74c3c; }
        .type-frontend { background: #e6ffe6; color: #2ecc71; }
        .status-active { color: #27ae60; font-weight: bold; }
        .status-inactive { color: #95a5a6; }
        .run-btn { background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; margin: 5px; }
        .run-btn:hover { background: #2980b9; }
        .run-btn.backend-btn { background: #e74c3c; }
        .run-btn.backend-btn:hover { background: #c0392b; }
        .run-btn.frontend-btn { background: #2ecc71; }
        .run-btn.frontend-btn:hover { background: #27ae60; }
        .metrics { display: flex; gap: 30px; margin: 20px 0; }
        .metric { text-align: center; }
        .metric-value { font-size: 28px; font-weight: bold; color: #3498db; }
        .metric-label { font-size: 14px; color: #7f8c8d; margin-top: 5px; }
        .results-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        .results-table th, .results-table td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        .results-table th { background: #f8f9fa; font-weight: bold; }
        .command-section { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-top: 20px; }
        .command { background: #34495e; padding: 10px; border-radius: 4px; font-family: monospace; margin: 5px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Universal RL Management Dashboard</h1>
            <p>Manage Frontend & Backend Applications with Reinforcement Learning</p>
        </div>
        
        <div class="section">
            <h2>🎯 Quick Actions</h2>
            <div style="text-align: center; margin: 20px 0;">
                <button class="run-btn backend-btn" onclick="runDemo('coinx-backend')">🔧 Test Backend RL</button>
                <button class="run-btn frontend-btn" onclick="runDemo('coinx-frontend')">🎨 Test Frontend RL</button>
                <button class="run-btn" onclick="runDemo('flask-backend')">⚡ Test Flask Demo</button>
                <button class="run-btn" onclick="location.reload()">🔄 Refresh Dashboard</button>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 System Overview</h2>
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">""" + str(len(apps)) + """</div>
                    <div class="metric-label">Total Apps</div>
                </div>
"""
    
    if results:
        html += f"""
                <div class="metric">
                    <div class="metric-value">{results["total_steps"]}</div>
                    <div class="metric-label">Last Demo Steps</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{sum(r['reward'] for r in results["results"])}</div>
                    <div class="metric-label">Total Reward</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{results["app_name"]}</div>
                    <div class="metric-label">Active App</div>
                </div>
"""
    
    html += """
            </div>
        </div>
        
        <div class="section">
            <h2>🏗️ Applications</h2>
            <div class="app-grid">
"""
    
    for app_key, app_spec in apps.items():
        app_type = app_spec['type']
        is_active = results and results['app_name'] == app_spec['name']
        status_class = "status-active" if is_active else "status-inactive"
        status_text = "🟢 Active" if is_active else "⚪ Inactive"
        
        html += f"""
                <div class="app-card {app_type}">
                    <div class="app-title">{app_spec['name']}</div>
                    <span class="app-type type-{app_type}">{app_type}</span>
                    <div style="margin: 15px 0;">
                        <strong>Port:</strong> {app_spec['port']}<br>
                        <strong>Actions:</strong> {len(app_spec['available_actions'])}<br>
                        <strong>Status:</strong> <span class="{status_class}">{status_text}</span>
                    </div>
                    <div>
                        <strong>Start Command:</strong><br>
                        <code style="background: #f8f9fa; padding: 5px; border-radius: 3px; font-size: 12px;">{app_spec['start_command']}</code>
                    </div>
                </div>
"""
    
    html += """
            </div>
        </div>
"""
    
    if results:
        html += f"""
        <div class="section">
            <h2>📈 Latest Results - {results['app_name']}</h2>
            <table class="results-table">
                <tr>
                    <th>Step</th>
                    <th>Scenario</th>
                    <th>Status</th>
                    <th>Action</th>
                    <th>Reward</th>
                    <th>Performance</th>
                </tr>
"""
        
        for result in results['results']:
            action = result['action'] if result['action'] else 'None'
            html += f"""
                <tr>
                    <td>{result['step']}</td>
                    <td>{result['scenario']}</td>
                    <td>{result['state']['status']}</td>
                    <td>{action}</td>
                    <td>{result['reward']}</td>
                    <td>{result['state']['performance_score']}%</td>
                </tr>
"""
        
        html += """
            </table>
        </div>
"""
    
    html += """
        <div class="command-section">
            <h3>🛠️ Manual Commands</h3>
            <div class="command">python run_universal_demo.py spec/frontend_app_spec.json  # Frontend RL</div>
            <div class="command">python run_universal_demo.py app_spec.generated.json     # Backend RL</div>
            <div class="command">python connect_all.py                                    # Full System Test</div>
        </div>
    </div>
    
    <script>
        function runDemo(appType) {
            alert('Running RL demo for ' + appType + '... Check console for progress!');
            // In a real implementation, this would trigger the Python script
            setTimeout(() => {
                location.reload();
            }, 3000);
        }
    </script>
</body>
</html>
"""
    
    return html

def start_unified_server():
    class Handler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/' or self.path == '/dashboard':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html_content = create_unified_html()
                self.wfile.write(html_content.encode())
            else:
                super().do_GET()
    
    server = HTTPServer(('localhost', 8080), Handler)
    print("🚀 Unified Dashboard running at: http://localhost:8080")
    print("📊 Frontend & Backend RL Management Ready!")
    print("Press Ctrl+C to stop")
    
    webbrowser.open('http://localhost:8080')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped")
        server.shutdown()

if __name__ == "__main__":
    start_unified_server()