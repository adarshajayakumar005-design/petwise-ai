import streamlit as st
import time
from transformers import pipeline

# --- Load AI model ---
@st.cache_resource(show_spinner=False)
def load_model():
    return pipeline("text-generation", model="google/flan-t5-small")  # small free model

model = load_model()

# --- Streamlit App UI ---
st.title("🐕 Petwise AI - Pet Symptom Checker")

pet_type = st.selectbox("Select your pet type:", ["Dog", "Cat", "Other"])
symptoms = st.text_area("Enter symptoms your pet is showing:")

result = ""  # initialize result variable

if st.button("Analyze Symptoms"):
    start_time = time.time()
    st.info("Analyzing symptoms...")

    try:
        prompt = f"Pet type: {pet_type}\nSymptoms: {symptoms}\nProvide a helpful AI analysis:"
        output = model(prompt, max_length=200, do_sample=True)
        result = output[0]['generated_text']

        analysis_time = time.time() - start_time
        st.success("✅ Analysis Complete!")
        st.markdown(f"**AI Analysis:**\n{result}")
        st.markdown(f"⏱️ Analysis Time: {int(analysis_time//60):02}:{int(analysis_time%60):02} (mm:ss)")

    except Exception as e:
        st.error(f"⚠️ Error generating AI analysis: {e}")

# --- Vet urgency slider ---
urgency = st.slider("Estimate Vet Urgency (0 = Low, 100 = High):", 0, 100)
st.markdown(f"🚑 Estimated Vet Urgency: **{urgency}**")

# --- Session history ---
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Save to History"):
    st.session_state.history.append({
        "pet": pet_type,
        "symptoms": symptoms,
        "urgency": urgency,
        "response": result
    })
    st.success("Saved to session history!")
