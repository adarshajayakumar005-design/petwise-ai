import streamlit as st
import time
import requests

# ----------------------------
# Helper function to call Ollama
# ----------------------------
def get_ollama_response(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt},
            stream=False,
            timeout=300
        )
        if response.status_code == 200:
            result = response.json()
            if "response" in result:
                return result["response"]
            else:
                return result.get("output", "⚠️ Unable to parse AI response.")
        else:
            return f"⚠️ Ollama error: {response.status_code}"
    except Exception as e:
        return f"⚠️ Error connecting to Ollama: {e}"

# ----------------------------
# Streamlit Page Setup
# ----------------------------
st.set_page_config(page_title="🐾 Petwise AI", page_icon="🐶", layout="centered")

# ----------------------------
# Custom CSS for Styling
# ----------------------------
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
    }
    .main {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0px 0px 15px rgba(0,0,0,0.1);
    }
    .title {
        text-align: center;
        font-size: 2.2em;
        color: #2c3e50;
        font-weight: 700;
        margin-bottom: 0.5em;
    }
    .subtitle {
        text-align: center;
        font-size: 1.1em;
        color: #16a085;
        margin-bottom: 1.5em;
    }
    .section {
        background-color: #eafaf1;
        border-radius: 12px;
        padding: 1.2em;
        margin-bottom: 1.2em;
    }
    .footer {
        text-align: center;
        font-size: 0.9em;
        color: #7f8c8d;
        margin-top: 1.5em;
    }
    .highlight {
        color: #27ae60;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# App Header
# ----------------------------
st.markdown("<div class='title'>🐾 Petwise AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your friendly AI Pet Symptom Checker 🐶🐱🐰</div>", unsafe_allow_html=True)

# ----------------------------
# Input Section
# ----------------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)

pet_type = st.selectbox("🐕 What kind of pet is this?", ["Dog", "Cat", "Rabbit"])
symptoms = st.text_area("💬 Describe the symptoms in detail:")

pet_emojis = {"Dog": "🐶", "Cat": "🐱", "Rabbit": "🐰"}
st.markdown(f"**Selected pet:** {pet_type} {pet_emojis.get(pet_type, '')}")

st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# Button - Run AI
# ----------------------------
if st.button("🔍 Analyze Symptoms"):
    if not symptoms.strip():
        st.warning("⚠️ Please enter symptoms before checking.")
    else:
        prompt = f"""
        Pet: {pet_type}
        Symptoms: {symptoms}

        Provide:
        1. Possible causes
        2. Home care advice
        3. When to see a vet
        Format it in friendly, structured text with emojis.
        """

        # Spinner while analyzing
        with st.spinner("🤖 Analyzing your pet's symptoms... please wait."):
            start_time = time.time()
            response = get_ollama_response(prompt)
            end_time = time.time()

        # Calculate runtime
        elapsed_time = end_time - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        runtime_str = f"{minutes:02d}:{seconds:02d}"

        # ----------------------------
        # Output Section
        # ----------------------------
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown("### 🐕 AI Analysis")
        st.markdown(response)
        st.markdown(f"⏱️ **Analysis Time:** `{runtime_str}` (mm:ss)")
        st.markdown("</div>", unsafe_allow_html=True)

        # ----------------------------
        # Urgency Slider After Result
        # ----------------------------
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        urgency = st.slider("🚑 Estimate Vet Urgency (0 = Low, 100 = High)", 0, 100, 50)
        st.progress(urgency / 100)
        st.markdown("</div>", unsafe_allow_html=True)

        # ----------------------------
        # Chat history (disabled for now)
        # ----------------------------
        """
        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append({
            "pet": pet_type,
            "symptoms": symptoms,
            "urgency": urgency,
            "response": response
        })
        """

# ----------------------------
# Footer
# ----------------------------
st.markdown("""
<hr style="border: 1px solid #ddd;">
<div class='footer'>
⚠️ <strong>Disclaimer:</strong> All AI guidance is for educational purposes only.<br>
Always consult a licensed veterinarian for serious symptoms.
</div>
""", unsafe_allow_html=True)
