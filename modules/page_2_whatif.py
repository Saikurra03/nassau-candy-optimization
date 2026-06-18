import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.factory_config import FACTORIES, PRODUCT_FACTORY_MAP
def show(df, model, features):
    st.header("What-If Scenario Analysis")
    st.write("Compare current shipping performance against a simulated alternative factory assignment for a specific region and ship mode.")
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_product = st.selectbox("Product", df['Product Name'].unique(), key="wi_product")
    with col2:
        selected_region = st.selectbox("Region", df['Region'].unique(), key="wi_region")
    with col3:
        selected_ship_mode = st.selectbox("Ship Mode", df['Ship Mode'].unique(), key="wi_ship")
    current_factory = PRODUCT_FACTORY_MAP.get(selected_product, "Unknown")
    # Filter dataset for the specific scenario
    scenario_df = df[
        (df['Product Name'] == selected_product) & 
        (df['Region'] == selected_region) & 
        (df['Ship Mode'] == selected_ship_mode)
    ]
    if len(scenario_df) == 0:
        st.warning("No data found for this specific combination. Try different filters.")
        return
    # 1. Calculate CURRENT actual average lead time
    current_avg_lead_time = scenario_df['Lead Time'].mean()
    # 2. Find the BEST alternative factory (based on shortest average distance)
    dist_cols = [c for c in scenario_df.columns if c.startswith('Dist_')]
    avg_distances = scenario_df[dist_cols].mean()
    safe_current = current_factory.replace(" ", "_").replace("'", "")
    if safe_current in avg_distances.index:
        avg_distances = avg_distances.drop(safe_current)
    best_factory_col = avg_distances.idxmin()
    best_factory_name = best_factory_col.replace("Dist_", "").replace("_", " ")
    # Map back to exact factory name
    for f_name in FACTORIES:
        if f_name.replace(" ", "_").replace("'", "") == best_factory_col:
            best_factory_name = f_name
            break
    # 3. Simulate PREDICTED lead time from the best alternative factory
    sim_features = scenario_df[features].copy()
    for col in dist_cols:
        sim_features[col] = 99999 # Set all distances to max
    sim_features[best_factory_col] = scenario_df[best_factory_col] # Set only the best factory distance
    predicted_lead_times = model.predict(sim_features)
    recommended_avg_lead_time = predicted_lead_times.mean()
    # 4. Display Comparison
    st.subheader("Scenario Comparison")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Current Factory", current_factory)
        st.metric("Actual Avg Lead Time", f"{current_avg_lead_time:.1f} days")
    with col_b:
        st.metric("Recommended Factory", best_factory_name)
        st.metric("Predicted Avg Lead Time", f"{recommended_avg_lead_time:.1f} days")
    with col_c:
        improvement = current_avg_lead_time - recommended_avg_lead_time
        st.metric("Estimated Improvement", f"{improvement:.1f} days", delta=f"{improvement:.1f}")
    # 5. Visualization
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Current Assignment', 'Simulated Reassignment'],
        y=[current_avg_lead_time, recommended_avg_lead_time],
        marker_color=['#FF4B4B', '#19C37D'],
        text=[f"{current_avg_lead_time:.1f} days", f"{recommended_avg_lead_time:.1f} days"],
        textposition='auto'
    ))
    fig.update_layout(yaxis_title="Lead Time (Days)", title="Lead Time Comparison", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
