import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import datetime


#Created on Apr 08 2025
#last modified on Feb 05 2026

#@author: BSbarro


# --- Configuration ---
st.set_page_config(
    page_title="City.ble - CivicPulse Dashboard",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Helper Functions & Mock Data Generation ---

# Simulate data generation 
# note: to be replaced with real data sources in a production environment

def generate_time_series_data(days=30):
    """Generates mock time series data for charts."""
    dates = pd.date_range(end=datetime.datetime.now(), periods=days, freq='D')
    data = np.random.rand(days) * 100
    return pd.DataFrame({'Date': dates, 'Value': data}).set_index('Date')

def generate_aqi_data(num_locations=5):
    """Generates mock AQI data for different locations."""
    locations = [f"Zone {chr(65+i)}" for i in range(num_locations)]
    aqi_values = np.random.randint(10, 150, num_locations)
    lat = np.random.uniform(41.8, 42.0, num_locations) # Example coordinates around Rome
    lon = np.random.uniform(12.4, 12.6, num_locations)
    return pd.DataFrame({
        'Location': locations,
        'AQI': aqi_values,
        'lat': lat,
        'lon': lon
    })

def generate_citizen_data():
    """Generates mock data related to citizen engagement."""
    participation_rate = np.random.uniform(5, 25) # Percentage
    well_being_index = np.random.uniform(50, 85) # Score out of 100
    empowerment_score = np.random.uniform(40, 75) # Score out of 100
    # Inclusivity: Mock demographic breakdown
    demographics = pd.DataFrame({
        'Group': ['Gender: Female', 'Gender: Male', 'Age: 18-30', 'Age: 31-50', 'Age: 51+', 'Income: Low', 'Income: Mid', 'Income: High'],
        'Participation (%)': np.random.uniform(5, 30, 8)
    })
    return participation_rate, well_being_index, empowerment_score, demographics

def generate_policy_data():
    """Generates mock policy uptake data."""
    policies = [
        {'Policy Area': 'Air Quality Improvement Plan', 'Status': np.random.choice(['Adopted', 'Implemented', 'Under Review']), 'Data Source': 'CivicPulse AQI Trends'},
        {'Policy Area': 'Green Space Expansion', 'Status': np.random.choice(['Adopted', 'Implemented', 'Proposed']), 'Data Source': 'Citizen Reports & Biodiversity Index'},
        {'Policy Area': 'Public Transport Incentives', 'Status': np.random.choice(['Implemented', 'Under Review', 'Proposed']), 'Data Source': 'Mobility Data & Behavior Change KPI'},
        {'Policy Area': 'Open Data Mandate', 'Status': np.random.choice(['Adopted', 'Implemented']), 'Data Source': 'Innovation & Data Metrics'}
    ]
    return pd.DataFrame(policies)

def create_gauge_chart(value, title, max_value=100, suffix=""):
    """Creates a Plotly gauge chart."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title, 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [0, max_value], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, max_value * 0.5], 'color': 'lightgray'},
                {'range': [max_value * 0.5, max_value * 0.8], 'color': 'gray'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9 # Example threshold
                }
            },
        number={'suffix': suffix, 'font': {'size': 24}}
        ))
    fig.update_layout(height=250, margin={'t':50, 'b':50, 'l':50, 'r':50})
    return fig

# --- Sidebar ---
st.sidebar.title("🏙️ CivicPulse Dashboard")
st.sidebar.write("City.ble - Integrated Smart City Monitoring") # Replace [City Name]
st.sidebar.markdown("---")
st.sidebar.info("This dashboard leverages technology and citizen science to provide holistic insights into city performance and SDG progress.")
st.sidebar.markdown("---")
# Add filtering options later if needed (e.g., date range, specific zone)
# selected_zone = st.sidebar.selectbox("Select Zone (Optional)", ["All Zones"] + [f"Zone {chr(65+i)}" for i in range(5)])
# date_range = st.sidebar.date_input("Select Date Range (Optional)", [])

# --- Main Dashboard Area ---
st.title("CivicPulse: Integrated Dashboard")
st.caption(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- Data Loading / Generation ---
# (In a real app, load data here)
aqi_data = generate_aqi_data()
participation_rate, well_being_index, empowerment_score, demographics_data = generate_citizen_data()
policy_data = generate_policy_data()
energy_consumption_data = generate_time_series_data()
traffic_congestion_data = generate_time_series_data()
waste_recycling_data = generate_time_series_data()
behavior_change_data = generate_time_series_data(days=90) # Longer term for behavior

# --- Dashboard Tabs ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview & SDG Pulse",
    "🌳 Environment",
    "🚗 Infrastructure & Mobility",
    "👥 Citizen Engagement & Well-being",
    "💡 Innovation & Data",
    "📜 Policy & Action"
])

# --- Tab 1: Overview & SDG Pulse ---
with tab1:
    st.header("City Overview & SDG Pulse")
    st.markdown("High-level snapshot of key city metrics and progress towards Sustainable Development Goals.")
    st.markdown("*(Reflects Findings 2, 5, 6)*")

    col1, col2, col3, col4 = st.columns(4)
    # Headline KPIs
    avg_aqi = int(aqi_data['AQI'].mean())
    col1.metric("Avg. Air Quality Index (AQI)", f"{avg_aqi}", delta=f"{np.random.randint(-5, 5)} today",
                help="Lower is better. Based on city-wide sensor network.")
    col2.metric("Citizen Engagement Rate", f"{participation_rate:.1f}%", delta=f"{np.random.uniform(-0.5, 0.5):.1f}% this month",
                help="Percentage of target population actively participating in citizen science/civic projects.")
    col3.metric("Community Well-being", f"{well_being_index:.1f}/100", delta=f"{np.random.uniform(-1, 1):.1f} this quarter",
                help="Composite index based on citizen surveys (mental health, social capital).")
    # Simulate CO2 Clock (using a metric with high value and delta)
    co2_level = 415 + np.random.rand() # Mock CO2 level in ppm
    co2_change = np.random.uniform(-0.1, 0.2) # Mock change
    col4.metric("Est. City CO₂ Level (ppm)", f"{co2_level:.1f}", delta=f"{co2_change:.2f} vs yesterday", delta_color="inverse",
                help="Estimated atmospheric CO2 concentration trend within the city.")

    st.markdown("---")
    st.subheader("SDG Progress Snapshot")
    # Mock SDG progress - Map KPIs to SDGs
    sdg_progress = {
        'SDG 3 (Health)': np.mean([well_being_index, (150 - avg_aqi) / 1.5]), # Combine well-being and inverse AQI
        'SDG 7 (Energy)': np.random.uniform(40, 70), # Mock energy efficiency progress
        'SDG 9 (Infrastructure)': np.random.uniform(50, 80), # Mock infrastructure reliability
        'SDG 10 (Inequality)': (100 - demographics_data['Participation (%)'].std() * 2), # Lower std dev = more equal participation
        'SDG 11 (Cities)': np.mean([(150 - avg_aqi) / 1.5, participation_rate * 2, empowerment_score]), # Combine AQI, participation, empowerment
        'SDG 13 (Climate)': (100 - (co2_level - 400)*5), # Progress based on CO2 level vs baseline
        'SDG 15 (Life on Land)': np.random.uniform(30, 60), # Mock biodiversity index
        'SDG 16 (Institutions)': empowerment_score * 0.8 + policy_data['Status'].apply(lambda x: 1 if x=='Implemented' else 0.5 if x=='Adopted' else 0).mean()*20, # Empowerment + Policy
    }

    cols = st.columns(4)
    i = 0
    for sdg, progress in sdg_progress.items():
        col = cols[i % 4]
        col.write(f"**{sdg}**")
        col.progress(int(progress))
        i += 1
    st.caption("Progress bars indicate estimated alignment (0-100) based on relevant KPIs.")

# --- Tab 2: Environment ---
with tab2:
    st.header("🌳 Environmental Monitoring")
    st.markdown("Real-time and trend data on key environmental indicators.")
    st.markdown("*(Reflects Findings 1, 2, 5)*")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Air Quality Index (AQI)")
        st.map(aqi_data, latitude='lat', longitude='lon', size='AQI', color=(255, 0, 0, 150)) # Red color, semi-transparent
        st.dataframe(aqi_data[['Location', 'AQI']].style.highlight_max(axis=0, color='lightcoral').format({'AQI': '{:.0f}'}))
        st.caption("Live AQI data from sensor network. Larger circles indicate higher (worse) AQI.")

    with col2:
        st.subheader("Energy Consumption Trend")
        st.line_chart(energy_consumption_data['Value'])
        st.metric("Current Consumption (MWh)", f"{energy_consumption_data['Value'].iloc[-1]:.1f}",
                  delta=f"{energy_consumption_data['Value'].iloc[-1] - energy_consumption_data['Value'].iloc[-2]:.1f} vs previous day")
        st.caption("City-wide energy usage trend (mock data).")

        st.subheader("Waste & Recycling Trend")
        st.line_chart(waste_recycling_data['Value'])
        st.metric("Recycling Rate (%)", f"{waste_recycling_data['Value'].iloc[-1]:.1f}",
                  delta=f"{waste_recycling_data['Value'].iloc[-1] - waste_recycling_data['Value'].iloc[-2]:.1f}% vs previous day")
        st.caption("Percentage of waste being recycled (mock data).")

    # Placeholder for Biodiversity Index
    st.subheader("Biodiversity Index (Mock)")
    biodiversity_score = np.random.uniform(40, 75)
    st.plotly_chart(create_gauge_chart(biodiversity_score, "Biodiversity Health Score", 100), use_container_width=True)
    st.caption("Index based on sensor data (e.g., acoustic monitoring) and citizen science observations (e.g., species sightings). Higher is better.")


# --- Tab 3: Infrastructure & Mobility ---
with tab3:
    st.header("🚗 Infrastructure & Mobility")
    st.markdown("Monitoring city infrastructure health and transportation efficiency.")
    st.markdown("*(Reflects Finding 1)*")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Traffic Congestion Trend")
        st.line_chart(traffic_congestion_data['Value'])
        st.metric("Current Congestion Index", f"{traffic_congestion_data['Value'].iloc[-1]:.1f}",
                  delta=f"{traffic_congestion_data['Value'].iloc[-1] - traffic_congestion_data['Value'].iloc[-2]:.1f} vs previous day",
                  delta_color="inverse") # Higher is worse
        st.caption("Index representing city-wide traffic congestion levels (mock data).")

        st.subheader("Public Transport Performance")
        on_time_perf = np.random.uniform(80, 98)
        satisfaction = np.random.uniform(65, 90)
        st.metric("On-Time Performance", f"{on_time_perf:.1f}%")
        st.metric("Citizen Satisfaction", f"{satisfaction:.1f}%")
        st.caption("Based on real-time tracking and citizen feedback (mock data).")

    with col2:
        st.subheader("Infrastructure Issues Reported")
        # Mock data for reported issues
        issues = pd.DataFrame({
            'Type': ['Pothole', 'Streetlight Outage', 'Damaged Sign', 'Water Leak', 'Broken Bench'],
            'Reports (Last 7 Days)': np.random.randint(5, 50, 5),
            'Status': np.random.choice(['Open', 'In Progress', 'Resolved'], 5, p=[0.4, 0.3, 0.3])
        })
        st.dataframe(issues)
        st.caption("Aggregated from citizen reporting apps and sensor alerts (mock data).")

        st.subheader("Digital Connectivity")
        wifi_coverage = np.random.uniform(70, 95)
        broadband_access = np.random.uniform(85, 99)
        st.metric("Public Wi-Fi Coverage", f"{wifi_coverage:.1f}%")
        st.metric("Household Broadband Access", f"{broadband_access:.1f}%")
        st.caption("Estimated city-wide digital access (mock data).")


# --- Tab 4: Citizen Engagement & Well-being ---
with tab4:
    st.header("👥 Citizen Engagement & Social Well-being")
    st.markdown("Measuring participation, well-being, equity, and empowerment.")
    st.markdown("*(Reflects Finding 5 & New KPIs)*")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Citizen Science Hub")
        st.metric("Active Participants (Monthly)", f"{np.random.randint(500, 5000)}")
        st.metric("Data Contributions (Monthly)", f"{np.random.randint(10000, 100000)}")
        st.metric("Participation Rate", f"{participation_rate:.1f}%")

        st.subheader("Community Well-being Index")
        st.plotly_chart(create_gauge_chart(well_being_index, "Well-being Score", 100), use_container_width=True)

        st.subheader("Empowerment Score")
        st.plotly_chart(create_gauge_chart(empowerment_score, "Empowerment Score", 100), use_container_width=True)
        st.caption("Reflects citizens' perceived ability to influence local issues.")

    with col2:
        st.subheader("Inclusivity & Equity Metrics")
        st.bar_chart(demographics_data.set_index('Group'))
        st.caption("Participation breakdown by demographic groups. Aim for equitable distribution.")

        st.subheader("Behavior Change KPI (Example: Sustainable Transport Use)")
        st.line_chart(behavior_change_data['Value'])
        st.metric("Sustainable Transport Use Index", f"{behavior_change_data['Value'].iloc[-1]:.1f}",
                  delta=f"{behavior_change_data['Value'].iloc[-1] - behavior_change_data['Value'].iloc[-30]:.1f} vs last month")
        st.caption("Index tracking adoption of sustainable practices like public transit, cycling (mock data).")


# --- Tab 5: Innovation & Data ---
with tab5:
    st.header("💡 Innovation & Data Ecosystem")
    st.markdown("Tracking open data usage and responsible AI implementation.")
    st.markdown("*(Reflects Findings 1, 3, 4)*")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Open Data Portal Monitor")
        st.metric("Available Datasets", f"{np.random.randint(100, 500)}")
        st.metric("API Calls (Last 30 Days)", f"{np.random.randint(5000, 50000)}")
        st.metric("Dataset Downloads (Last 30 Days)", f"{np.random.randint(1000, 10000)}")
        st.caption("Usage statistics for the city's open data platform.")

    with col2:
        st.subheader("AI Governance & Ethics (Placeholder)")
        ai_systems = pd.DataFrame({
            'AI System': ['Traffic Prediction', 'Resource Allocation', 'Public Safety Analysis'],
            'Status': ['Active', 'Active', 'Pilot'],
            'Last Ethical Review': pd.to_datetime(['2024-10-01', '2025-01-15', '2024-11-30']),
            'Transparency Level': ['High', 'Medium', 'Medium']
        })
        st.dataframe(ai_systems)
        st.caption("Registry and status of AI systems used in city management.")

    st.subheader("Project Synergy Tracker (Conceptual)")
    # In a real dashboard, this could be a network graph showing connections
    st.write("Visualizing connections between different smart city projects to highlight integration.")
    st.image("https://placehold.co/600x200/e2e8f0/475569?text=Network+Graph+Showing+Project+Connections",
             caption="Conceptual representation of project integration.")


# --- Tab 6: Policy & Action ---
with tab6:
    st.header("📜 Policy & Action Hub")
    st.markdown("Connecting dashboard insights to policy-making and tracking implementation.")
    st.markdown("*(Reflects Finding 5 & New KPIs)*")

    st.subheader("Policy Uptake KPI Tracker")
    st.dataframe(policy_data)
    st.caption("Status of policy recommendations derived from or supported by CivicPulse data.")

    # Calculate Policy Implementation Rate
    implemented_count = policy_data[policy_data['Status'] == 'Implemented'].shape[0]
    total_policies = policy_data.shape[0]
    implementation_rate = (implemented_count / total_policies) * 100 if total_policies > 0 else 0

    st.metric("Policy Implementation Rate", f"{implementation_rate:.1f}%",
              help="Percentage of tracked policies that have been fully implemented.")

    st.subheader("Impact Evaluation (Conceptual)")
    st.write("This section would link to reports evaluating the effectiveness of implemented policies based on ongoing KPI monitoring.")
    # Example Link (Placeholder)
    st.link_button("View Example Impact Report (PDF)", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf")

# --- Footer ---
st.markdown("---")
st.caption("CivicPulse Dashboard Concept - (c) Bernardo Sbarro @ City.ble Project - Mock Data")

