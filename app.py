import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os

# Title
st.title("AI Health Bot")

# Input Method Selection
input_method = st.selectbox("Select input method", ["Text", "Voice (Mic)", "Voice (Upload)"])

def recognize_voice_from_mic(language="en-IN"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now.")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language=language)
        return text
    except Exception as e:
        st.error(f"❌ Could not recognize speech: {e}")
        return None

def recognize_voice_from_file(uploaded_file, language="en-IN"):
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp_ogg:
            tmp_ogg.write(uploaded_file.read())
            tmp_ogg_path = tmp_ogg.name

        # Convert OGG to WAV using pydub
        sound = AudioSegment.from_ogg(tmp_ogg_path)
        wav_path = tmp_ogg_path.replace(".ogg", ".wav")
        sound.export(wav_path, format="wav")

        # Recognize using speech_recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language=language)

        # Clean up
        os.remove(tmp_ogg_path)
        os.remove(wav_path)

        return text
    except Exception as e:
        st.error(f"❌ Could not transcribe audio: {e}")
        return None

# Main Logic
if input_method == "Text":
    user_input = st.text_input("Enter your health question here:")
elif input_method == "Voice (Mic)":
    if st.button("Start Recording"):
        user_input = recognize_voice_from_mic()
elif input_method == "Voice (Upload)":
    uploaded_audio = st.file_uploader("Upload an audio file (.ogg)", type=["ogg"])
    if uploaded_audio is not None:
        user_input = recognize_voice_from_file(uploaded_audio)
    else:
        user_input = None
else:
    user_input = None

# Display user input
if user_input:
    st.success(f"Recognized Input: {user_input}")
    # Here, send user_input to your AI model and show response
    st.write("🤖 (Model Response Placeholder)")
