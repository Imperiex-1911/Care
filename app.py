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
        st.warning("Please describe your symptoms first!")

import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Auth UI
st.sidebar.title("Login/Signup")
email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    try:
        user = auth.get_user_by_email(email)
        st.sidebar.success(f"Welcome {user.uid[:5]}...")
    except:
        st.sidebar.error("Login failed")

if st.sidebar.button("Create Account"):
    try:
        user = auth.create_user(email=email, password=password)
        st.sidebar.success("Account created!")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")
# Patient Profile Section
st.header("Your Profile")
name = st.text_input("Full Name")
age = st.number_input("Age", min_value=0, max_value=120)

if st.button("Save Profile"):
    patient_data = {
        "name": name,
        "age": age,
        "last_updated": firestore.SERVER_TIMESTAMP
    }
    db.collection("patients").document(email).set(patient_data)
    st.success("Profile saved!")

import whisper
import tempfile

# Load Whisper model (cache it)
@st.cache_resource
def load_whisper():
    return whisper.load_model("tiny")  # Smallest model for CPU

# Voice Input Section
st.header("Voice Symptom Input")
audio_file = st.file_uploader("Record/upload symptoms (MP3/WAV)", type=["wav", "mp3"])

if audio_file:
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name
    
    # Transcribe
    model = load_whisper()
    result = model.transcribe(tmp_path)
    symptoms = result["text"]
    st.text_area("Transcribed Symptoms", symptoms, height=100)
# Severity Analysis (after symptom input)
if symptoms:
    severity_prompt = f"""
    Analyze these symptoms: {symptoms}
    Rate severity (1-5) and suggest action:
    1 - Mild (self-care)
    3 - Moderate (see doctor soon)
    5 - Emergency (seek help now)
    Format as: "Severity: X/5. Recommendation: [text]"
    """
    
    severity = model(severity_prompt, max_length=150)[0]["generated_text"]
    st.warning(f"🔍 Triage: {severity}")
# Patient Insights (from Firestore)
st.header("Your Health Insights")
if email:
    try:
        docs = db.collection("patients").document(email).collection("symptoms").stream()
        symptom_history = [doc.to_dict() for doc in docs]
        
        if symptom_history:
            # Show trends
            st.line_chart(
                pd.DataFrame(symptom_history)
                .set_index("timestamp")["severity"]
            )
        else:
            st.info("No history yet. Record symptoms to see insights.")
    except:
        st.error("Error loading history")
from translate import Translator

LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "Hindi": "hi",
    "Arabic": "ar"
}

lang = st.sidebar.selectbox("🌐 Language", list(LANGUAGES.keys()))
translator = Translator(to_lang=LANGUAGES[lang])

# Modify your existing AI response code:
ai_response = model(symptom_prompt)[0]["generated_text"]
translated_response = translator.translate(ai_response)
st.success(f"💬 {translated_response}")

emergency_tab, contacts_tab = st.tabs(["🚨 Emergency", "📞 Contacts"])

with contacts_tab:
    st.header("Your Emergency Contacts")
    col1, col2 = st.columns(2)
    with col1:
        contact_name = st.text_input("Contact Name")
    with col2:
        contact_phone = st.text_input("Phone Number")
    
    if st.button("Save Contact"):
        db.collection("patients").document(email).collection("contacts").add({
            "name": contact_name,
            "phone": contact_phone,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
with emergency_tab:
    st.header("Emergency Assistance")
    if st.button("🚑 ACTIVATE EMERGENCY PROTOCOL", type="primary", use_container_width=True):
        # Get all contacts
        contacts = db.collection("patients").document(email).collection("contacts").stream()
        
        # Simulate alerts (real implementation would use Twilio)
        for contact in contacts:
            contact = contact.to_dict()
            st.error(f"ALERT SENT to {contact['name']} at {contact['phone']}")
        
        # Save emergency event
        db.collection("emergencies").add({
            "patient": email,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "status": "activated"
        })
st.set_page_config(
    page_title="CareBridge",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="auto"
)

# Mobile-friendly CSS
st.markdown("""
<style>
    @media (max-width: 600px) {
        .stTextInput>div>div>input {
            font-size: 16px !important;
        }
        .stButton>button {
            width: 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)