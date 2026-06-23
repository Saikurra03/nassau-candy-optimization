import streamlit as st
import pandas as pd
import numpy as np
import joblib
import sys, os
sys.path.insert(0, os.path.abspath('.'))
from utils.factory_config import FACTORIES, PRODUCT_FACTORY_MAP
from utils.data_prep import prepare_data
from modules import page_0_about
st.set_page_config(page_title="Nassau Candy Optimizer", layout="wide")
@st.cache_resource
def load_model():
    return joblib.load("models/lead_time_model.pkl"), joblib.load("models/features.pkl")
@st.cache_data
def load_data():
    return prepare_data("data/Nassau Candy Distributor.csv")
model, features = load_model()
df = load_data()
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "📖 About & User Guide",
    "Factory Optimization Simulator", 
    "What-If Scenario Analysis", 
    "Recommendation Dashboard", 
    "Risk & Impact Panel"
])
st.title("Factory Reallocation & Shipping Optimization")
st.caption("Nassau Candy Distributor - Decision Intelligence System")
if page == "📖 About & User Guide":
    page_0_about.run()
elif page == "Factory Optimization Simulator":
    from modules import page_1_simulator
    page_1_simulator.show(df, model, features)
elif page == "What-If Scenario Analysis":
    from modules import page_2_whatif
    page_2_whatif.show(df, model, features)
elif page == "Recommendation Dashboard":
    from modules import page_3_recommendations
    page_3_recommendations.show(df, model, features)
elif page == "Risk & Impact Panel":
    from modules import page_4_risk
    page_4_risk.show(df, model, features)
