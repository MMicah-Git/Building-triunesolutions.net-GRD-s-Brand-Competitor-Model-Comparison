import streamlit as st
import pandas as pd
import openai

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Triune Solutions – GRD's Competitor Model Comparison",
    page_icon="📊",
    layout="wide"
)

# -------------------------------
# Cache Decorator (compatible with all Streamlit versions)
# -------------------------------
if hasattr(st, "cache_data"):
    cache_func = st.cache_data
else:
    cache_func = st.cache  # fallback for older versions

# -------------------------------
# Load Data
# -------------------------------
@cache_func
def load_data():
    try:
        # 🔗 Direct link to raw GitHub file (replace with your repo & branch!)
        github_url = "https://raw.githubusercontent.com/MMicah-Git/Building-triunesolutions.net-GRD-s-Brand-Competitor-Model-Comparison/main/data/Restructured_Data_With_Titus.xlsx"
        
        df = pd.read_excel(github_url)
        st.success("✅ Loaded dataset from GitHub.")
    except Exception:
        st.warning("⚠️ Could not load from GitHub. Please upload the file manually.")
        uploaded_file = st.sidebar.file_uploader("📂 Upload Excel File", type=["xlsx"])
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)
            st.success("✅ Loaded dataset from uploaded fil
