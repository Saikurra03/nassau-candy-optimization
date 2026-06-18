import streamlit as st
import pandas as pd
import numpy as np
from utils.factory_config import FACTORIES, PRODUCT_FACTORY_MAP
def simulate_factory(product_df, target_factory_name, model, features):
    avg_features = product_df[features].mean().to_frame().T
    safe_target = target_factory_name.replace(" ", "_").replace("'", "")
    for f_name in FACTORIES.keys():
        safe_name = f_name.replace(" ", "_").replace("'", "")
        if f_name == target_factory_name:
            avg_features["Dist_" + safe_name] = product_df["Dist_" + safe_name].mean()
        else:
            avg_features["Dist_" + safe_name] = 99999
    return model.predict(avg_features[features])[0]
def show(df, model, features):
    st.header("Risk & Impact Panel")
    st.write("Evaluate the financial safety and potential risks before executing factory reassignments.")
    selected_product = st.selectbox("Select Product to Analyze", list(PRODUCT_FACTORY_MAP.keys()), key="risk_product")
    product_df = df[df['Product Name'] == selected_product]
    if product_df.empty:
        st.warning("No data available for this product.")
        return
    current_fact = PRODUCT_FACTORY_MAP[selected_product]
    # Financial metrics
    avg_profit = product_df['Gross Profit'].mean()
    total_sales = product_df['Sales'].sum()
    col1, col2 = st.columns(2)
    col1.metric("Historical Avg Profit/Order", f"")
    col2.metric("Total Historical Sales", f"")
    st.subheader("Reassignment Risk Assessment")
    risks = []
    for f_name in FACTORIES.keys():
        if f_name == current_fact: continue
        pred_lt = simulate_factory(product_df, f_name, model, features)
        current_pred_lt = simulate_factory(product_df, current_fact, model, features)
        lt_diff = pred_lt - current_pred_lt
        # Risk rules
        risk_level = "Low"
        risk_color = "green"
        if lt_diff > 50:
            risk_level = "High"
            risk_color = "red"
        elif lt_diff > 20:
            risk_level = "Medium"
            risk_color = "orange"
        # Check if profit margin is historically thin (less than )
        if avg_profit < 2.00:
            risk_level = "High"
            risk_color = "red"
        risks.append({
            "Alternative Factory": f_name,
            "Predicted Lead Time Change": f"{lt_diff:+.1f} days",
            "Risk Level": risk_level,
            "Profit Status": "Stable" if avg_profit >= 2.00 else "Low Margin Alert"
        })
    risk_df = pd.DataFrame(risks)
    for _, row in risk_df.iterrows():
        if row["Risk Level"] == "High":
            st.error(f"⚠️ **High Risk:** Moving to {row['Alternative Factory']} (Lead Time: {row['Predicted Lead Time Change']}, {row['Profit Status']})")
        elif row["Risk Level"] == "Medium":
            st.warning(f"⚡ **Medium Risk:** Moving to {row['Alternative Factory']} (Lead Time: {row['Predicted Lead Time Change']})")
        else:
            st.success(f"✅ **Low Risk:** Moving to {row['Alternative Factory']} (Lead Time: {row['Predicted Lead Time Change']})")
    st.subheader("Detailed Risk Table")
    st.dataframe(risk_df, use_container_width=True, hide_index=True)
