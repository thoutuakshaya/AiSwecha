import streamlit as st
from utils.db import init_db, insert_tip, get_all_tips, upvote_tip
from utils.translator import translate_text
from utils.voice import recognize_voice, speak_text
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os

st.set_page_config(page_title="Health Tips App", layout="centered")

# Initialize the database
init_db()

# Initialize session state
if "tip" not in st.session_state:
    st.session_state["tip"] = ""

voice_lang = st.selectbox("🎙️ Select Voice Language", [
    ("Telugu", "te-IN"),
    ("Hindi", "hi-IN"),
    ("English", "en-GB"),
    ("Kannada", "kn-IN"),
    ("Tamil", "ta-IN"),
], format_func=lambda x: x[0])

st.title("🩺 Let's Share Health Tips")

# Tip submission
st.header("📝 Share Your Health Tip")
input_method = st.radio("Choose input method:", ("Text", "Voice (Record)", "Voice (Upload)"))

tip = ""

if input_method == "Text":
    st.session_state["tip"] = st.text_area("Enter your health tip (in any language)", height=100)
    tip = st.session_state["tip"]

elif input_method == "Voice (Record)":
    st.warning("⚠️ Live voice input is not supported on this platform. Please upload a file instead.")
    st.text_area("🎧 Transcribed Voice Tip:", value=st.session_state["tip"], height=100)
    tip = st.session_state["tip"]

elif input_method == "Voice (Upload)":
    audio_file = st.file_uploader("📁 Upload voice file (.wav/.mp3/.ogg)", type=["wav", "mp3", "ogg"])
    if audio_file:
        try:
            # Save uploaded audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp_ogg:
                tmp_ogg.write(audio_file.read())
                ogg_path = tmp_ogg.name

            # Convert OGG to WAV
            wav_path = ogg_path.replace(".ogg", ".wav")
            audio = AudioSegment.from_file(ogg_path)
            audio.export(wav_path, format="wav")

            # Transcribe WAV using speech_recognition
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language=voice_lang[1])
                st.session_state["tip"] = text
                st.success("🎉 Transcription successful!")

            os.remove(ogg_path)
            os.remove(wav_path)

        except Exception as e:
            st.error(f"❌ Could not transcribe audio: {e}")

    st.text_area("🎧 Transcribed Voice Tip:", value=st.session_state["tip"], height=100)
    tip = st.session_state["tip"]

# Submit the tip
if st.button("✅ Submit Tip"):
    if st.session_state["tip"].strip():
        insert_tip(st.session_state["tip"].strip())
        st.success("✅ Health tip submitted successfully!")
        st.session_state["tip"] = ""
    else:
        st.warning("⚠️ Please enter or record a tip before submitting.")

# Show tips
st.header("📚 Community Tips")
all_tips = get_all_tips()

lang_code_map = {
    "Telugu": "te-IN",
    "Hindi": "hi-IN",
    "English": "en-GB",
    "Kannada": "kn-IN",
    "Tamil": "ta-IN",
}

for idx, (tip_id, user_input, bot_response, timestamp, upvotes) in enumerate(all_tips):
    with st.expander(f"💡 Tip #{idx + 1} (👍 {upvotes} votes)"):
        st.write(f"🗒️ Original Tip:\n\n{user_input}")

        col1, col2 = st.columns([3, 1])
        with col1:
            lang = st.selectbox(
                "🌐 Translate to:",
                ["Telugu", "Hindi", "English", "Kannada", "Tamil"],
                key=f"lang_{idx}"
            )
            if st.button("🌐 Translate", key=f"translate_{idx}"):
                translated = translate_text(user_input, lang)
                st.markdown(f"🔤 **Translated Tip:**\n\n{translated}")

        with col2:
            if st.button("👍 Upvote", key=f"upvote_{tip_id}"):
                upvote_tip(tip_id)
                st.success("🙏 You supported this tip!")
                st.rerun()





# import streamlit as st
# from utils.db import init_db, insert_tip, get_all_tips, upvote_tip
# from utils.translator import translate_text
# from utils.voice import recognize_voice
# import speech_recognition as sr

# st.set_page_config(page_title="Health Tips App", layout="centered")

# # Initialize the database
# init_db()

# # Initialize session state
# if "tip" not in st.session_state:
#     st.session_state["tip"] = ""

# voice_lang = st.selectbox("🎙️ Select Voice Language", [
#     ("Telugu", "te-IN"),
#     ("Hindi", "hi-IN"),
#     ("English", "en-GB"),
#     ("Kannada", "kn-IN"),
#     ("Tamil", "ta-IN"),
# ], format_func=lambda x: x[0])

# st.title("🩺 Let's Share Health Tips")

# # Tip submission
# st.header("📝 Share Your Health Tip")
# input_method = st.radio("Choose input method:", ("Text", "Voice (Record)", "Voice (Upload)"))

# tip = ""

# if input_method == "Text":
#     st.session_state["tip"] = st.text_area("Enter your health tip (in any language)", height=100)
#     tip = st.session_state["tip"]

# elif input_method == "Voice (Record)":
#     st.warning("⚠️ Live voice input is not supported on this platform. Please upload a file instead.")
#     # Optionally disable or fallback if deployed
#     # Uncomment below if running locally only
#     # if st.button("🎙️ Record Voice"):
#     #     with st.spinner("Recording... Speak now!"):
#     #         try:
#     #             text = recognize_voice(language=voice_lang[1])
#     #             st.session_state["tip"] = text or ""
#     #         except Exception as e:
#     #             st.error(f"Error: {e}")
#     st.text_area("🎧 Transcribed Voice Tip:", value=st.session_state["tip"], height=100)
#     tip = st.session_state["tip"]

# elif input_method == "Voice (Upload)":
#     audio_file = st.file_uploader("Upload a voice file (WAV/MP3)", type=["wav", "mp3", "ogg"])
#     if audio_file:
#         recognizer = sr.Recognizer()
#         try:
#             with sr.AudioFile(audio_file) as source:
#                 audio_data = recognizer.record(source)
#                 text = recognizer.recognize_google(audio_data, language=voice_lang[1])
#                 st.session_state["tip"] = text
#                 st.success("🎉 Transcription successful!")
#         except Exception as e:
#             st.error(f"❌ Could not transcribe audio: {e}")
#     st.text_area("🎧 Transcribed Voice Tip:", value=st.session_state["tip"], height=100)
#     tip = st.session_state["tip"]

# # Submit the tip
# if st.button("✅ Submit Tip"):
#     if st.session_state["tip"].strip():
#         insert_tip(st.session_state["tip"].strip())
#         st.success("✅ Health tip submitted successfully!")
#         st.session_state["tip"] = ""
#     else:
#         st.warning("⚠️ Please enter or record a tip before submitting.")

# # Show tips
# st.header("📚 Community Tips")
# all_tips = get_all_tips()

# lang_code_map = {
#     "Telugu": "te-IN",
#     "Hindi": "hi-IN",
#     "English": "en-GB",
#     "Kannada": "kn-IN",
#     "Tamil": "ta-IN",
# }

# for idx, (tip_id, user_input, bot_response, timestamp, upvotes) in enumerate(all_tips):
#     with st.expander(f"💡 Tip #{idx + 1} (👍 {upvotes} votes)"):
#         st.write(f"🗒️ Original Tip:\n\n{user_input}")

#         col1, col2 = st.columns([3, 1])
#         with col1:
#             lang = st.selectbox(
#                 "🌐 Translate to:",
#                 ["Telugu", "Hindi", "English", "Kannada", "Tamil"],
#                 key=f"lang_{idx}"
#             )
#             if st.button("🌐 Translate", key=f"translate_{idx}"):
#                 translated = translate_text(user_input, lang)
#                 st.markdown(f"🔤 **Translated Tip:**\n\n{translated}")

#         with col2:
#             if st.button("👍 Upvote", key=f"upvote_{tip_id}"):
#                 upvote_tip(tip_id)
#                 st.success("🙏 You supported this tip!")
#                 st.rerun() 





