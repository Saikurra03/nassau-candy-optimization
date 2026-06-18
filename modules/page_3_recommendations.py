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
    st.header("Recommendation Dashboard")
    st.write("System-generated, ranked factory reassignment suggestions for all products based on maximum efficiency gain.")
    recommendations = []
    for product, current_fact in PRODUCT_FACTORY_MAP.items():
        product_df = df[df['Product Name'] == product]
        if product_df.empty: continue
        # Current performance
        current_pred = simulate_factory(product_df, current_fact, model, features)
        # Find best alternative
        best_alt_fact = None
        best_alt_pred = current_pred
        for f_name in FACTORIES.keys():
            if f_name == current_fact: continue
            alt_pred = simulate_factory(product_df, f_name, model, features)
            if alt_pred < best_alt_pred:
                best_alt_pred = alt_pred
                best_alt_fact = f_name
        reduction = current_pred - best_alt_pred
        reduction_pct = (reduction / current_pred) * 100 if current_pred > 0 else 0
        confidence = min(100, len(product_df) * 2) # Simple confidence based on sample size
        if reduction > 0 and best_alt_fact is not None:
            recommendations.append({
                "Product": product,
                "Current Factory": current_fact,
                "Recommended Factory": best_alt_fact,
                "Current Pred. Lead Time": round(current_pred, 1),
                "New Pred. Lead Time": round(best_alt_pred, 1),
                "Lead Time Reduction (%)": round(reduction_pct, 2),
                "Confidence Score": confidence
            })
    if not recommendations:
        st.info("No better alternatives found for current product-factory assignments.")
        return
    rec_df = pd.DataFrame(recommendations).sort_values("Lead Time Reduction (%)", ascending=False)
    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Recommendations", len(rec_df))
    col2.metric("Avg Lead Time Reduction", f"{rec_df['Lead Time Reduction (%)'].mean():.2f}%")
    col3.metric("Recommendation Coverage", f"{(len(rec_df) / len(PRODUCT_FACTORY_MAP)) * 100:.0f}%")
    st.subheader("Ranked Reassignment Suggestions")
    st.dataframe(rec_df, use_container_width=True, hide_index=True)
