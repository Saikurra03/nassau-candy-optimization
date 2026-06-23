import streamlit as st
def run():
    st.title("📖 About & User Guide")
    st.markdown("---")
    st.markdown("""
    ### 🎯 Project Goal
    The **Factory Reallocation & Shipping Optimization System** was built to transition Nassau Candy Distributor from static, rule-based logistics to **predictive, model-informed decision-making**. 
    This tool empowers operations managers to visualize the impact of reassigning products to different factories *before* making physical changes to the supply chain.
    """)
    st.markdown("---")
    st.subheader("🧭 How to Use This Application")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **1. 🏭 Simulator**
        *   Select a product from the dropdown.
        *   View its current factory, predicted shipping lead time, and distance.
        *   *Use this to understand the baseline performance.*
        **2. ⚖️ What-If Analysis**
        *   Select a product and choose an alternative factory.
        *   View a side-by-side comparison of Lead Time and Gross Profit.
        *   *Use this to manually test "What if we moved Product X to Factory Y?"*
        """)
    with col2:
        st.markdown("""
        **3. 📈 Recommendations**
        *   Click "Generate Recommendations" to run the simulation engine across multiple products.
        *   View a ranked list of the best factory reassignments based on speed and profit.
        *   *Use this to find quick wins across the catalog.*
        **4. 🛡️ Risk Panel**
        *   Review the recommendations through a risk lens.
        *   Items highlighted in **Red** reduce lead time but destroy profit margins.
        *   Items in **Green** are safe, profitable moves.
        *   *Use this to filter out bad ideas before presenting to leadership.*
        """)
    st.markdown("---")
    st.subheader("💡 Why This Matters (Business Impact)")
    st.markdown("""
    *   **Reduce Lead Times:** Identify geographic inefficiencies and route products from closer facilities.
    *   **Protect Margins:** The Risk panel ensures we never chase speed at the cost of profitability.
    *   **Scale Decisions:** Evaluate thousands of routing scenarios in seconds—a task impossible with manual Excel spreadsheets.
    """)
    st.markdown("---")
    st.subheader("🧠 Under the Hood (Technology)")
    st.info("""
    *   **Models:** Trained using Random Forest & Gradient Boosting Regressors (Scikit-Learn).
    *   **Simulation Engine:** Uses serialized ML models (`.pkl`) to predict outcomes of alternative factory assignments dynamically.
    *   **Distance Calculation:** Utilizes the Haversine formula (Geopy) for accurate geographic distance.
    """)
    st.caption("Developed by Venkata Sai Baba Kurra | Unified Mentor Internship Project")
if __name__ == "__main__":
    run()
