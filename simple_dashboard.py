import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import threading

def load_data():
    data = {"apps": [], "results": None}
    
    # Load app specs
    if os.path.exists('spec/example_app_spec.json'):
        with open('spec/example_app_spec.json', 'r') as f:
            data["apps"].append({"name": "Flask Example", "spec": json.load(f)})
    
    if os.path.exists('app_spec.generated.json'):
        with open('app_spec.generated.json', 'r') as f:
            spec = json.load(f)
            data["apps"].append({"name": spec["name"], "spec": spec})
    
    # Load results
    if os.path.exists('reports/demo_results.json'):
        with open('reports/demo_results.json', 'r') as f:
            data["results"] = json.load(f)
    
    return data

def create_html():
    data = load_data()
    
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Universal RL Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .card { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .status-good { color: #27ae60; font-weight: bold; }
        .status-bad { color: #e74c3c; font-weight: bold; }
        .metric { display: inline-block; margin: 10px 20px 10px 0; }
        .metric-value { font-size: 24px; font-weight: bold; color: #3498db; }
        .metric-label { font-size: 14px; color: #7f8c8d; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #ecf0f1; }
        .refresh-btn { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .refresh-btn:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Universal RL Management Dashboard</h1>
            <p>Monitor and manage RL policies across different applications</p>
        </div>
        
        <div class="card">
            <h2>System Overview</h2>
            <div class="metric">
                <div class="metric-value">""" + str(len(data["apps"])) + """</div>
                <div class="metric-label">Active Apps</div>
            </div>
"""
    
    if data["results"]:
        html += f"""
            <div class="metric">
                <div class="metric-value">{data["results"]["total_steps"]}</div>
                <div class="metric-label">Total Steps</div>
            </div>
            <div class="metric">
                <div class="metric-value">{sum(r['reward'] for r in data["results"]["results"])}</div>
                <div class="metric-label">Total Reward</div>
            </div>
"""
    
    html += """
        </div>
        
        <div class="card">
            <h2>Applications</h2>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Port</th>
                    <th>Actions</th>
                    <th>Status</th>
                </tr>
"""
    
    for app in data["apps"]:
        spec = app["spec"]
        status = "Active" if data["results"] and data["results"]["app_name"] == spec["name"] else "Inactive"
        status_class = "status-good" if status == "Active" else "status-bad"
        
        html += f"""
                <tr>
                    <td>{spec["name"]}</td>
                    <td>{spec["type"]}</td>
                    <td>{spec["port"]}</td>
                    <td>{len(spec["available_actions"])}</td>
                    <td class="{status_class}">{status}</td>
                </tr>
"""
    
    html += """
            </table>
        </div>
"""
    
    if data["results"]:
        html += f"""
        <div class="card">
            <h2>Latest Results - {data["results"]["app_name"]}</h2>
            <table>
                <tr>
                    <th>Step</th>
                    <th>Scenario</th>
                    <th>Status</th>
                    <th>Action</th>
                    <th>Reward</th>
                </tr>
"""
        
        for result in data["results"]["results"]:
            action = result["action"] if result["action"] else "None"
            html += f"""
                <tr>
                    <td>{result["step"]}</td>
                    <td>{result["scenario"]}</td>
                    <td>{result["state"]["status"]}</td>
                    <td>{action}</td>
                    <td>{result["reward"]}</td>
                </tr>
"""
        
        html += """
            </table>
        </div>
"""
    
    html += """
        <div class="card">
            <button class="refresh-btn" onclick="location.reload()">Refresh Dashboard</button>
            <p><strong>Commands:</strong></p>
            <ul>
                <li><code>python run_universal_demo.py</code> - Run RL demo</li>
                <li><code>python connect_all.py</code> - Connect all systems</li>
                <li><code>python master_controller.py</code> - Interactive control</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""
    
    return html

def start_server():
    # Create HTML file
    html_content = create_html()
    with open('dashboard.html', 'w') as f:
        f.write(html_content)
    
    # Start server
    class Handler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/' or self.path == '/dashboard':
                self.path = '/dashboard.html'
                # Regenerate HTML on each request
                html_content = create_html()
                with open('dashboard.html', 'w') as f:
                    f.write(html_content)
            return SimpleHTTPRequestHandler.do_GET(self)
    
    server = HTTPServer(('localhost', 8080), Handler)
    print("Dashboard running at: http://localhost:8080")
    print("Press Ctrl+C to stop")
    
    # Open browser
    webbrowser.open('http://localhost:8080')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped")
        server.shutdown()

if __name__ == "__main__":
    start_server()