import streamlit as st
import google.generativeai as genai

st.title("🔑 Gemini API Configuration Check")

try:
    # ✅ Get Gemini API key from Streamlit secrets
    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        st.error("❌ GEMINI_API_KEY not found in Streamlit secrets. Please add it in `.streamlit/secrets.toml`.")
    else:
        # ✅ Configure Gemini client
        genai.configure(api_key=api_key)
        st.success("✅ Gemini API key loaded successfully!")

        # ✅ List available models that can generate content
        st.write("Fetching available models...")
        usable_models = [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]

        if usable_models:
            st.info(f"**Usable Models:** {', '.join(usable_models)}")
        else:
            st.warning("No usable generative models found.")
            
except Exception as e:
    st.error("⚠️ An error occurred while setting up the Gemini API.")
    st.exception(e)
