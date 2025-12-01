import streamlit as st
import json
import os
import pandas as pd

def load_app_specs():
    specs = {}
    if os.path.exists('spec/example_app_spec.json'):
        with open('spec/example_app_spec.json', 'r') as f:
            specs['example-flask-api'] = json.load(f)
    if os.path.exists('app_spec.generated.json'):
        with open('app_spec.generated.json', 'r') as f:
            specs['generated-backend'] = json.load(f)
    return specs

def load_demo_results():
    if os.path.exists('reports/demo_results.json'):
        with open('reports/demo_results.json', 'r') as f:
            return json.load(f)
    return None

def main():
    st.set_page_config(page_title="Universal RL Dashboard", layout="wide")
    st.title("Universal RL Management Dashboard")
    st.markdown("Monitor and manage RL policies across different applications")
    
    st.sidebar.header("App Selection")
    
    app_specs = load_app_specs()
    if not app_specs:
        st.error("No app specifications found. Please generate some app specs first.")
        return
    
    selected_app = st.sidebar.selectbox("Choose Application", list(app_specs.keys()))
    
    if selected_app:
        app_spec = app_specs[selected_app]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header(f"App: {app_spec['name']}")
            
            st.subheader("Application Details")
            details_df = pd.DataFrame([
                ["Type", app_spec['type']],
                ["Version", app_spec['version']],
                ["Port", app_spec['port']],
                ["Start Command", app_spec['start_command']],
                ["Build Command", app_spec['build_command']]
            ], columns=["Property", "Value"])
            st.table(details_df)
            
            st.subheader("Available Actions")
            actions_data = []
            for action in app_spec['available_actions']:
                actions_data.append([
                    action['name'],
                    action['risk_level'],
                    action['command'][:50] + "..." if len(action['command']) > 50 else action['command']
                ])
            
            if actions_data:
                actions_df = pd.DataFrame(actions_data, columns=["Action", "Risk Level", "Command"])
                st.table(actions_df)
        
        with col2:
            st.subheader("RL Policy Status")
            
            demo_results = load_demo_results()
            if demo_results and demo_results['app_name'] == app_spec['name']:
                st.success("Policy Active")
                st.metric("Q-table Size", demo_results['final_policy']['q_table_size'])
                st.metric("Total Steps", demo_results['total_steps'])
                
                total_reward = sum(r['reward'] for r in demo_results['results'])
                st.metric("Total Reward", total_reward)
            else:
                st.warning("No active policy")

if __name__ == "__main__":
    main()