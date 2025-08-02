from pydub import AudioSegment
import tempfile
import os

elif input_method == "Voice (Upload)":
    audio_file = st.file_uploader("Upload a voice file (WAV/MP3/OGG)", type=["wav", "mp3", "ogg"])
    if audio_file:
        recognizer = sr.Recognizer()
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
                if audio_file.type == "audio/ogg":
                    # Convert OGG to WAV using pydub
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp_ogg:
                        tmp_ogg.write(audio_file.read())
                        tmp_ogg.flush()
                        audio = AudioSegment.from_ogg(tmp_ogg.name)
                        audio.export(tmp_wav.name, format="wav")
                else:
                    tmp_wav.write(audio_file.read())
                    tmp_wav.flush()

                with sr.AudioFile(tmp_wav.name) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language=voice_lang[1])
                    st.session_state["tip"] = text
                    st.success("🎉 Transcription successful!")
        except Exception as e:
            st.error(f"❌ Could not transcribe audio: {e}")
        finally:
            if os.path.exists(tmp_wav.name):
                os.remove(tmp_wav.name)
            if audio_file.type == "audio/ogg" and os.path.exists(tmp_ogg.name):
                os.remove(tmp_ogg.name)

    st.text_area("🎧 Transcribed Voice Tip:", value=st.session_state["tip"], height=100)
    tip = st.session_state["tip"]
