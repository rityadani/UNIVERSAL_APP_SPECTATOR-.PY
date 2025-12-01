import json
import os
import subprocess
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import threading
from datetime import datetime

def load_all_data():
    data = {
        'apps': {},
        'results': None,
        'multi_results': None,
        'system_stats': {}
    }
    
    # Load all app specs
    specs = {
        'flask-backend': 'spec/example_app_spec.json',
        'coinx-backend': 'app_spec.generated.json', 
        'coinx-frontend': 'spec/frontend_app_spec.json'
    }
    
    for key, path in specs.items():
        if os.path.exists(path):
            with open(path, 'r') as f:
                data['apps'][key] = json.load(f)
    
    # Load results
    if os.path.exists('reports/demo_results.json'):
        with open('reports/demo_results.json', 'r') as f:
            data['results'] = json.load(f)
    
    if os.path.exists('reports/multi_app_results.json'):
        with open('reports/multi_app_results.json', 'r') as f:
            data['multi_results'] = json.load(f)
    
    # System stats
    data['system_stats'] = {
        'total_files': len([f for f in os.listdir('.') if f.endswith('.py')]),
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'system_status': 'Operational'
    }
    
    return data

def create_advanced_html():
    data = load_all_data()
    
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Advanced Universal RL Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .dashboard-container { 
            max-width: 1600px; 
            margin: 0 auto; 
            padding: 20px;
        }
        
        .header {
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 2.5em;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .nav-tabs {
            display: flex;
            background: rgba(255,255,255,0.9);
            border-radius: 15px;
            padding: 5px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        
        .nav-tab {
            flex: 1;
            padding: 15px 20px;
            text-align: center;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }
        
        .nav-tab.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            transform: translateY(-2px);
        }
        
        .nav-tab:hover:not(.active) {
            background: rgba(102,126,234,0.1);
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-label {
            color: #666;
            margin-top: 10px;
            font-weight: 500;
        }
        
        .apps-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .app-card {
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .app-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        
        .app-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        
        .app-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .app-title {
            font-size: 1.4em;
            font-weight: bold;
            color: #333;
        }
        
        .app-type {
            padding: 6px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .type-backend { background: #ffe6e6; color: #e74c3c; }
        .type-frontend { background: #e6ffe6; color: #2ecc71; }
        .type-fullstack { background: #fff3e0; color: #f39c12; }
        
        .app-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .detail-item {
            display: flex;
            flex-direction: column;
        }
        
        .detail-label {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }
        
        .detail-value {
            font-weight: 600;
            color: #333;
        }
        
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }
        
        .status-active {
            background: #e8f5e8;
            color: #2ecc71;
        }
        
        .status-inactive {
            background: #f5f5f5;
            color: #95a5a6;
        }
        
        .action-buttons {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        .btn {
            padding: 12px 20px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            flex: 1;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102,126,234,0.4);
        }
        
        .btn-secondary {
            background: #f8f9fa;
            color: #333;
            border: 2px solid #e9ecef;
        }
        
        .btn-secondary:hover {
            background: #e9ecef;
        }
        
        .results-section {
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .results-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        .results-table th,
        .results-table td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        
        .results-table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
        }
        
        .results-table tr:hover {
            background: #f8f9fa;
        }
        
        .performance-chart {
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .chart-container {
            height: 300px;
            display: flex;
            align-items: end;
            justify-content: space-around;
            border-bottom: 2px solid #eee;
            border-left: 2px solid #eee;
            padding: 20px;
        }
        
        .chart-bar {
            background: linear-gradient(to top, #667eea, #764ba2);
            width: 40px;
            border-radius: 4px 4px 0 0;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .chart-bar:hover {
            opacity: 0.8;
            transform: scaleY(1.05);
        }
        
        .chart-label {
            position: absolute;
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 0.8em;
            color: #666;
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            background: #2ecc71;
            color: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            transform: translateX(400px);
            transition: transform 0.3s ease;
        }
        
        .notification.show {
            transform: translateX(0);
        }
        
        @media (max-width: 768px) {
            .apps-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .nav-tabs {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="header">
            <h1>🚀 Advanced Universal RL Dashboard</h1>
            <p style="margin-top: 10px; color: #666;">Last Updated: """ + data['system_stats']['last_updated'] + """</p>
        </div>
        
        <div class="nav-tabs">
            <div class="nav-tab active" onclick="showTab('overview')">📊 Overview</div>
            <div class="nav-tab" onclick="showTab('applications')">🏗️ Applications</div>
            <div class="nav-tab" onclick="showTab('analytics')">📈 Analytics</div>
            <div class="nav-tab" onclick="showTab('controls')">🎛️ Controls</div>
        </div>
        
        <div id="overview" class="tab-content active">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">""" + str(len(data['apps'])) + """</div>
                    <div class="stat-label">Active Applications</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">""" + (str(data['results']['total_steps']) if data['results'] else '0') + """</div>
                    <div class="stat-label">Total RL Steps</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">""" + (str(sum(r['reward'] for r in data['results']['results'])) if data['results'] else '0') + """</div>
                    <div class="stat-label">Total Reward</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">""" + str(data['system_stats']['total_files']) + """</div>
                    <div class="stat-label">System Files</div>
                </div>
            </div>
            
            <div class="results-section">
                <h2>🎯 System Status</h2>
                <div style="display: flex; align-items: center; gap: 15px; margin-top: 20px;">
                    <div class="status-indicator status-active">
                        <span>🟢</span> System Operational
                    </div>
                    <div class="status-indicator status-active">
                        <span>🤖</span> RL Engine Ready
                    </div>
                    <div class="status-indicator status-active">
                        <span>📡</span> Dashboard Online
                    </div>
                </div>
            </div>
        </div>
        
        <div id="applications" class="tab-content">
            <div class="apps-grid">
"""
    
    for app_key, app_spec in data['apps'].items():
        is_active = data['results'] and data['results']['app_name'] == app_spec['name']
        status_class = "status-active" if is_active else "status-inactive"
        status_text = "🟢 Active" if is_active else "⚪ Inactive"
        
        html += f"""
                <div class="app-card">
                    <div class="app-header">
                        <div class="app-title">{app_spec['name']}</div>
                        <div class="app-type type-{app_spec['type']}">{app_spec['type']}</div>
                    </div>
                    
                    <div class="app-details">
                        <div class="detail-item">
                            <div class="detail-label">Port</div>
                            <div class="detail-value">{app_spec['port']}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Actions</div>
                            <div class="detail-value">{len(app_spec['available_actions'])}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Status</div>
                            <div class="detail-value">
                                <span class="{status_class}">{status_text}</span>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Version</div>
                            <div class="detail-value">{app_spec['version']}</div>
                        </div>
                    </div>
                    
                    <div style="margin: 15px 0;">
                        <div class="detail-label">Start Command</div>
                        <code style="background: #f8f9fa; padding: 8px; border-radius: 5px; font-size: 0.9em; display: block; margin-top: 5px;">{app_spec['start_command']}</code>
                    </div>
                    
                    <div class="action-buttons">
                        <button class="btn btn-primary" onclick="runDemo('{app_key}')">
                            🚀 Run RL Demo
                        </button>
                        <button class="btn btn-secondary" onclick="viewDetails('{app_key}')">
                            📋 View Details
                        </button>
                    </div>
                </div>
"""
    
    html += """
            </div>
        </div>
        
        <div id="analytics" class="tab-content">
"""
    
    if data['results']:
        html += f"""
            <div class="performance-chart">
                <h2>📈 Performance Analytics - {data['results']['app_name']}</h2>
                <div class="chart-container">
"""
        
        for i, result in enumerate(data['results']['results'][:6]):  # Show max 6 bars
            height = max(20, (result['state']['performance_score'] / 100) * 250)
            html += f"""
                    <div class="chart-bar" style="height: {height}px;">
                        <div class="chart-label">Step {result['step']}</div>
                    </div>
"""
        
        html += """
                </div>
            </div>
            
            <div class="results-section">
                <h2>📊 Detailed Results</h2>
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
        
        for result in data['results']['results']:
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
    else:
        html += """
            <div class="results-section">
                <h2>📈 No Analytics Data</h2>
                <p>Run some RL demos to see performance analytics here.</p>
            </div>
"""
    
    html += """
        </div>
        
        <div id="controls" class="tab-content">
            <div class="results-section">
                <h2>🎛️ System Controls</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px;">
                    <button class="btn btn-primary" onclick="runFullTest()" style="padding: 20px;">
                        🔄 Run Complete System Test
                    </button>
                    <button class="btn btn-primary" onclick="generateSpecs()" style="padding: 20px;">
                        📋 Generate New App Specs
                    </button>
                    <button class="btn btn-primary" onclick="refreshDashboard()" style="padding: 20px;">
                        🔄 Refresh Dashboard
                    </button>
                    <button class="btn btn-secondary" onclick="exportData()" style="padding: 20px;">
                        💾 Export Data
                    </button>
                </div>
                
                <div style="margin-top: 30px;">
                    <h3>🛠️ Manual Commands</h3>
                    <div style="background: #2c3e50; color: white; padding: 20px; border-radius: 10px; margin-top: 15px;">
                        <div style="margin: 10px 0; font-family: monospace;">python run_universal_demo.py spec/frontend_app_spec.json</div>
                        <div style="margin: 10px 0; font-family: monospace;">python run_universal_demo.py app_spec.generated.json</div>
                        <div style="margin: 10px 0; font-family: monospace;">python connect_all.py</div>
                        <div style="margin: 10px 0; font-family: monospace;">python multi_app_demo.py</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div id="notification" class="notification">
        <span id="notificationText">Action completed successfully!</span>
    </div>
    
    <script>
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active class from all nav tabs
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked nav tab
            event.target.classList.add('active');
        }
        
        function showNotification(message) {
            const notification = document.getElementById('notification');
            const text = document.getElementById('notificationText');
            text.textContent = message;
            notification.classList.add('show');
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 3000);
        }
        
        function runDemo(appKey) {
            showNotification('Running RL demo for ' + appKey + '...');
            setTimeout(() => {
                location.reload();
            }, 2000);
        }
        
        function viewDetails(appKey) {
            showNotification('Viewing details for ' + appKey);
        }
        
        function runFullTest() {
            showNotification('Running complete system test...');
            setTimeout(() => {
                location.reload();
            }, 3000);
        }
        
        function generateSpecs() {
            showNotification('Generating new app specifications...');
        }
        
        function refreshDashboard() {
            showNotification('Refreshing dashboard...');
            setTimeout(() => {
                location.reload();
            }, 1000);
        }
        
        function exportData() {
            showNotification('Exporting system data...');
        }
        
        // Auto-refresh every 30 seconds
        setInterval(() => {
            location.reload();
        }, 30000);
    </script>
</body>
</html>
"""
    
    return html

def start_advanced_server():
    class Handler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/' or self.path == '/dashboard':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html_content = create_advanced_html()
                self.wfile.write(html_content.encode())
            else:
                super().do_GET()
    
    server = HTTPServer(('localhost', 9000), Handler)
    print("🚀 Advanced Dashboard running at: http://localhost:9000")
    print("🎯 Next-Gen RL Management Interface Ready!")
    print("Press Ctrl+C to stop")
    
    webbrowser.open('http://localhost:9000')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Advanced Dashboard stopped")
        server.shutdown()

if __name__ == "__main__":
    start_advanced_server()