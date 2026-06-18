import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.factory_config import FACTORIES, PRODUCT_FACTORY_MAP
def show(df, model, features):
    st.header("Factory Optimization Simulator")
    st.write("Select a product to simulate how shipping lead times would change if it were assigned to different factories.")
    product_list = df['Product Name'].unique()
    selected_product = st.selectbox("Choose a Product", product_list)
    current_factory = PRODUCT_FACTORY_MAP.get(selected_product, "Unknown")
    st.info(f"**Current Factory Assignment:** {current_factory}")
    product_df = df[df['Product Name'] == selected_product]
    if st.button("Run Simulation", type="primary"):
        with st.spinner("Simulating across all factories..."):
            # Get average features for the selected product
            avg_features = product_df[features].mean().to_frame().T
            results = []
            for f_name, f_coords in FACTORIES.items():
                test_row = avg_features.copy()
                # Set the distance for the factory we are testing
                safe_name = f_name.replace(" ", "_").replace("'", "")
                test_row["Dist_" + safe_name] = product_df["Dist_" + safe_name].mean()
                # Set distances for all OTHER factories to a very high number
                # This isolates the effect of the tested factory
                for other_name in FACTORIES.keys():
                    if other_name != f_name:
                        other_safe = other_name.replace(" ", "_").replace("'", "")
                        test_row["Dist_" + other_safe] = 99999
                # Predict lead time
                pred_lead_time = model.predict(test_row[features])[0]
                results.append({
                    "Factory": f_name,
                    "Predicted Lead Time (Days)": round(pred_lead_time, 2),
                    "Status": "Current" if f_name == current_factory else "Alternative"
                })
            res_df = pd.DataFrame(results).sort_values("Predicted Lead Time (Days)")
            # Display results table
            st.subheader("Simulation Results")
            st.dataframe(res_df, use_container_width=True, hide_index=True)
            # Display chart
            fig = px.bar(res_df, x="Factory", y="Predicted Lead Time (Days)", 
                         color="Status", title=f"Predicted Lead Time: {selected_product}",
                         color_discrete_map={"Current": "red", "Alternative": "blue"})
            st.plotly_chart(fig, use_container_width=True)
            # Find best alternative
            best_row = res_df[res_df["Status"] == "Alternative"].iloc[0]
            current_row = res_df[res_df["Status"] == "Current"].iloc[0]
            reduction = current_row["Predicted Lead Time (Days)"] - best_row["Predicted Lead Time (Days)"]
            if reduction > 0:
                st.success(f"**Recommendation:** Reassigning to **{best_row['Factory']}** could reduce lead time by ~{reduction:.2f} days on average.")
            else:
                st.warning("Current factory assignment appears optimal based on distance.")
