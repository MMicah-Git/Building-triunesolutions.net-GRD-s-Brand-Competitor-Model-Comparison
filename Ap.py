# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    try:
        # 🔗 Direct link to raw GitHub file (replace with your repo & branch)
        github_url = "Restructured_Data_With_Titus.xlsx"
        
        df = pd.read_excel(github_url)
        st.success("✅ Loaded dataset from GitHub.")
    except Exception as e:
        st.warning("⚠️ Could not load from GitHub. Please upload the file manually.")
        uploaded_file = st.sidebar.file_uploader("📂 Upload Excel File", type=["xlsx"])
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)
            st.success("✅ Loaded dataset from uploaded file.")
        else:
            return None

    # 🔑 Clean up
    df.columns = df.columns.str.strip()
    df = df.dropna(how="all")
    if "TNB Model" in df.columns:
        df = df[df["TNB Model"].notna()]
    return df

df = load_data()

if df is None:
    st.error("❌ No data available. Please upload an Excel file.")
    st.stop()
