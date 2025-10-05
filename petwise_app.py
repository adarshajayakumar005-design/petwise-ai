import streamlit as st
import time
import requests

# --- Helper function to safely get the Groq API key ---
def get_groq_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except KeyError:
        st.error(
            "Groq API key not found! "
            "Please add your `GROQ_API_KEY` in Streamlit app secrets."
        )
        st.stop()  # Stop execution until the secret is provided

# --- Get API key safely ---
groq_api_key = get_groq_api_key()

# --- Streamlit App UI ---
st.title("🐕 Petwise AI - Pet Symptom Checker")

pet_type = st.selectbox("Select your pet type:", ["Dog", "Cat", "Other"])
symptoms = st.text_area("Enter symptoms your pet is showing:")

if st.button("Analyze Symptoms"):
    start_time = time.time()
    st.info("Analyzing symptoms...")
    
    # --- Example: Call Groq API (replace with your actual API call) ---
    try:
        headers = {"Authorization": f"Bearer {groq_api_key}"}
        payload = {"prompt": f"{pet_type}: {symptoms}", "max_tokens": 200}

        # Replace URL with your Groq endpoint
        response = requests.post("https://api.groq.ai/v1/generate", headers=headers, json=payload)
        response.raise_for_status()  # Raises exception for HTTP errors
        result = response.json().get("text", "No response text received.")

        analysis_time = time.time() - start_time
        st.success("✅ Analysis Complete!")
        st.markdown(f"**AI Analysis:**\n{result}")
        st.markdown(f"⏱️ Analysis Time: {int(analysis_time//60):02}:{int(analysis_time%60):02} (mm:ss)")

    except Exception as e:
        st.error(f"⚠️ Error connecting to Groq: {e}")

# --- Vet urgency placeholder ---
urgency = st.slider("Estimate Vet Urgency (0 = Low, 100 = High):", 0, 100)
st.markdown(f"🚑 Estimated Vet Urgency: **{urgency}**")

# --- Optional: session history ---
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Save to History"):
    st.session_state.history.append({
        "pet": pet_type,
        "symptoms": symptoms,
        "urgency": urgency,
        "response": result if 'result' in locals() else ""
    })
    st.success("Saved to session history!")
