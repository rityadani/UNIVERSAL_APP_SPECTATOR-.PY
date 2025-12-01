import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px

def load_all_results():
    results = {}
    if os.path.exists('reports/demo_results.json'):
        with open('reports/demo_results.json', 'r') as f:
            results['latest'] = json.load(f)
    if os.path.exists('reports/multi_app_results.json'):
        with open('reports/multi_app_results.json', 'r') as f:
            results['multi_app'] = json.load(f)
    return results

def main():
    st.set_page_config(page_title="Universal RL Dashboard", layout="wide")
    st.title("Universal RL Management Dashboard")
    
    # Load data
    results = load_all_results()
    
    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Choose Page", ["Overview", "App Details", "Performance"])
    
    if page == "Overview":
        st.header("System Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Active Apps", len(results))
        
        with col2:
            if 'latest' in results:
                st.metric("Total Steps", results['latest']['total_steps'])
        
        with col3:
            if 'multi_app' in results:
                passed = sum(1 for v in results['multi_app'].values() if v == "PASS")
                st.metric("Apps Passing", f"{passed}/{len(results['multi_app'])}")
        
        # Multi-app status
        if 'multi_app' in results:
            st.subheader("Multi-App Test Results")
            for app, status in results['multi_app'].items():
                color = "🟢" if status == "PASS" else "🔴"
                st.write(f"{color} {app}: {status}")
    
    elif page == "Performance":
        if 'latest' in results:
            st.header("Performance Analysis")
            
            # Create performance chart
            chart_data = []
            for result in results['latest']['results']:
                chart_data.append({
                    'Step': result['step'],
                    'Performance': result['state']['performance_score'],
                    'Reward': result['reward']
                })
            
            df = pd.DataFrame(chart_data)
            
            # Performance line chart
            fig = px.line(df, x='Step', y='Performance', title='Performance Over Time')
            st.plotly_chart(fig)
            
            # Rewards bar chart
            fig2 = px.bar(df, x='Step', y='Reward', title='Rewards by Step')
            st.plotly_chart(fig2)

if __name__ == "__main__":
    main()