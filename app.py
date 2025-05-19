<<<<<<< HEAD
import streamlit as st
from transformers import pipeline

# Set up the page
st.set_page_config(page_title="CareBridge", page_icon="🏥")
st.title("CareBridge: AI Symptom Checker 🏥")

# Load BioGPT (free medical AI from Hugging Face)
@st.cache_resource  # Cache the model to avoid reloading
def load_model():
    return pipeline("text-generation", model="microsoft/BioGPT-Large")

model = load_model()

# User input
symptoms = st.text_input("Describe your symptoms (e.g., 'headache and fever'):")

if st.button("Analyze Symptoms"):
    if symptoms:
        # Generate AI response
        response = model(
            f"Explain in simple terms what might cause {symptoms}. Max 50 words.",
            max_length=100,
        )
        st.write("### 🤖 AI Doctor's Response:")
        st.success(response[0]["generated_text"])
    else:
=======
import streamlit as st
from transformers import pipeline

# Set up the page
st.set_page_config(page_title="CareBridge", page_icon="🏥")
st.title("CareBridge: AI Symptom Checker 🏥")

# Load BioGPT (free medical AI from Hugging Face)
@st.cache_resource  # Cache the model to avoid reloading
def load_model():
    return pipeline("text-generation", model="microsoft/BioGPT-Large")

model = load_model()

# User input
symptoms = st.text_input("Describe your symptoms (e.g., 'headache and fever'):")

if st.button("Analyze Symptoms"):
    if symptoms:
        # Generate AI response
        response = model(
            f"Explain in simple terms what might cause {symptoms}. Max 50 words.",
            max_length=100,
        )
        st.write("### 🤖 AI Doctor's Response:")
        st.success(response[0]["generated_text"])
    else:
>>>>>>> a52e1eb1ec9525714ce1b439e79f08d0e2e955e3
        st.warning("Please describe your symptoms first!")