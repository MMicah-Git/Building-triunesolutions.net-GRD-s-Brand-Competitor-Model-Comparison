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
        github_url = "https://raw.githubusercontent.com/<your-username>/<your-repo>/main/data/Restructured_Data_With_Titus.xlsx"
        
        df = pd.read_excel(github_url)
        st.success("✅ Loaded dataset from GitHub.")
    except Exception:
        st.warning("⚠️ Could not load from GitHub. Please upload the file manually.")
        uploaded_file = st.sidebar.file_uploader("📂 Upload Excel File", type=["xlsx"])
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)
            st.success("✅ Loaded dataset from uploaded file.")
        else:
            return None

    # 🔑 Clean up blanks
    df.columns = df.columns.str.strip()
    df = df.dropna(how="all")
    if "TNB Model" in df.columns:
        df = df[df["TNB Model"].notna()]
    return df

df = load_data()

if df is None:
    st.error("❌ No data available. Please upload an Excel file.")
    st.stop()

# -------------------------------
# Brand Setup
# -------------------------------
brand_columns = ["TNB Model", "Anemostat", "Carnes", "EH Price",
                 "Krueger", "MetalAire", "Nailor", "Titus"]

brand_display_names = {
    "TNB Model": "GRD's",
    "Anemostat": "Anemostat",
    "Carnes": "Carnes",
    "EH Price": "EH Price",
    "Krueger": "Krueger",
    "MetalAire": "MetalAire",
    "Nailor": "Nailor",
    "Titus": "Titus"
}

# -------------------------------
# Tabs
# -------------------------------
tab1, tab2 = st.tabs(["🔍 Model Comparison", "💬 GRD's Chatbot"])

# -------------------------------
# TAB 1: Model Comparison
# -------------------------------
with tab1:
    st.title("📊 Triune Solutions – GRD's Competitor Model Comparison")
    st.markdown(
        """
        Welcome to **Triune Solutions' GRD's Competitor Model Comparison Tool** 🎯  
        Easily compare **GRD's** models against competitor brands with just a few clicks.  
        Use the filters in the sidebar to explore multiple models and export results.
        """
    )

    # Sidebar
    st.sidebar.header("🔍 Filter Options")

    BASE_BRAND = st.sidebar.selectbox("📌 Select a Base Brand:", options=brand_columns)
    BASE_BRAND_LABEL = brand_display_names.get(BASE_BRAND, BASE_BRAND)

    # Search box for models
    search_query = st.sidebar.text_input(f"🔎 Search {BASE_BRAND_LABEL} models:")

    base_models = df[BASE_BRAND].dropna().unique()
    base_models = sorted([str(m) for m in base_models])

    # Filter models based on search query
    if search_query:
        base_models = [m for m in base_models if search_query.lower() in m.lower()]

    selected_models = st.sidebar.multiselect(f"📋 Select {BASE_BRAND_LABEL} models:", options=base_models)

    selected_brands = st.sidebar.multiselect(
        "🏷️ Select Competitor Brands:",
        options=[b for b in brand_columns if b != BASE_BRAND],
        default=[b for b in brand_columns if b != BASE_BRAND]
    )

    if selected_models:
        filtered_df = df[df[BASE_BRAND].astype(str).isin(selected_models)]

        if not filtered_df.empty:
            st.success(f"✅ Showing results for {len(selected_models)} {BASE_BRAND_LABEL} model(s).")

            for model in selected_models:
                sub_df = filtered_df[filtered_df[BASE_BRAND].astype(str) == model]
                comparison_df = sub_df[[BASE_BRAND] + selected_brands].fillna("")

                # 🔑 Drop rows where all competitor columns are blank
                comparison_df = comparison_df.loc[~(comparison_df[selected_brands] == "").all(axis=1)]

                with st.expander(f"🔎 Results for {BASE_BRAND_LABEL}: **{model}**", expanded=False):
                    st.dataframe(
                        comparison_df,
                        use_container_width=True,
                        height=200
                    )

            # Export option
            export_df = filtered_df[[BASE_BRAND] + selected_brands].fillna("")
            export_df = export_df.loc[~(export_df[selected_brands] == "").all(axis=1)]

            st.download_button(
                label="⬇️ Download results as CSV",
                data=export_df.to_csv(index=False).encode("utf-8"),
                file_name="comparison_results.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ No competitor data found for selected models.")
    else:
        st.info(f"👈 Select at least one {BASE_BRAND_LABEL} model to compare.")

# -------------------------------
# TAB 2: Chatbot
# -------------------------------
with tab2:
    st.title("💬 GRD's Interactive Chatbot")
    st.markdown(
        """
        Ask any question about **GRD's models** and their competitor equivalents.  
        Example questions:  
        - *What is the competitor model for GRD's X123?*  
        - *Does Krueger have an alternative for GRD's Y456?*  
        - *Show all equivalents for Anemostat model Z789.*  
        """
    )

    if "OPENAI_API_KEY" not in st.secrets:
        st.error("⚠️ No OpenAI API key found. Please add it to `.streamlit/secrets.toml` or Streamlit Cloud Secrets Manager.")
    else:
        openai.api_key = st.secrets["OPENAI_API_KEY"]

        user_question = st.chat_input("💡 Ask me about GRD's or competitor models...")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if user_question:
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.write(user_question)

            # Context (first 50 rows for efficiency)
            context = df[brand_columns].fillna("").head(50).to_string(index=False)

            prompt = f"""
            You are an expert assistant for HVAC model comparison.
            Here is the dataset of GRD's and competitor models:\n{context}\n
            Question: {user_question}\n
            Answer clearly and cite the model/brand names from the dataset.
            """

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful HVAC model comparison assistant."},
                        *st.session_state.chat_history,
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2
                )
                answer = response.choices[0].message["content"]

                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                with st.chat_message("assistant"):
                    st.write(answer)

            except Exception as e:
                st.error(f"❌ Chatbot Error: {e}")
