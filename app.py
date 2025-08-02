import streamlit as st
from utils.db import init_db, insert_tip, get_all_tips, upvote_tip
from utils.translator import translate_text
from utils.voice import recognize_voice

st.set_page_config(page_title="Health Tips App", layout="centered")

# Initialize the database
init_db()

# Initialize session state for voice transcription if not already present
if "tip" not in st.session_state:
    st.session_state["tip"] = ""

# Supported voice input languages
voice_lang = st.selectbox("🎙️ Select Voice Language", [
    ("Telugu", "te-IN"),
    ("Hindi", "hi-IN"),
    ("English", "en-GB"),
    ("Kannada", "kn-IN"),
    ("Tamil", "ta-IN"),
], format_func=lambda x: x[0])

st.title("🩺 Lets share Health Tips")

# Tip submission section
st.header("📝 Share Your Health Tip")
input_method = st.radio("Choose input method:", ("Text", "Voice"))

tip = ""

if input_method == "Text":
    st.session_state["tip"] = st.text_area("Enter your health tip (in any language)", height=100)
    tip = st.session_state["tip"]

elif input_method == "Voice":
    if st.button("🎙️ Record Voice"):
        with st.spinner("Recording... Speak now!"):
            text = recognize_voice(language=voice_lang[1])
        st.session_state["tip"] = text or ""
    st.text_area("🎧 Transcribed Voice Tip:", value=st.session_state["tip"], height=100)
    tip = st.session_state["tip"]

# Submit the tip
if st.button("✅ Submit Tip"):
    if st.session_state["tip"].strip():
        insert_tip(st.session_state["tip"].strip())
        st.success("✅ Health tip submitted successfully!")
        st.session_state["tip"] = ""  # clear input after submit
    else:
        st.warning("⚠️ Please enter or record a tip before submitting.")

# Display all community tips
st.header("📚 Community Tips")
all_tips = get_all_tips()

# Language code mapping for translation
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
