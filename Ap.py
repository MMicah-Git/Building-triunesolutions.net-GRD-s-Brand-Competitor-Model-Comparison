import streamlit as st
import pandas as pd

# -------------------------------
# Page Config (must be first)
# -------------------------------
st.set_page_config(
    page_title="Triune Solutions – GRD's Competitor Model Comparison",
    page_icon="📊",
    layout="wide"
)

# -------------------------------
# Load Data
# -------------------------------
file_path = "C:/Users/micno/OneDrive/Desktop/triune/Restructured_Competitor_Comparison.xlsx"  # make sure this file is in the same folder
df = pd.read_excel(file_path)

# Ensure consistent column names
df.columns = df.columns.str.strip()

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("🔍 Filter Options")

# Convert all TNB models to string and sort
tnb_models = df["TNB Model"].dropna().unique()
tnb_models = sorted([str(m) for m in tnb_models])  # force all to string

# Searchable dropdown
selected_model = st.sidebar.selectbox("Select a TNB Model:", options=tnb_models)

# -------------------------------
# Main App
# -------------------------------
st.title("📊 Triune Solutions – GRD's Competitor Model Comparison")
st.markdown("""
Easily compare **Tuttle & Bailey (TNB)** models with competitor models across multiple brands.  
Select a model from the sidebar to view competitor equivalents side by side.
""")

# Filter data
filtered_df = df[df["TNB Model"].astype(str) == selected_model]

if not filtered_df.empty:
    st.subheader(f"Results for **TNB Model: {selected_model}**")
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.warning("No competitor data found for the selected model.")
