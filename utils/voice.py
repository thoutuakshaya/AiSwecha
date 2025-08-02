import speech_recognition as sr

# Language-specific translations for fallback messages
ERROR_MESSAGES = {
    "en": {
        "unknown": "Sorry, could not understand the audio.",
        "request": "Sorry, speech service is not available.",
    },
    "te": {
        "unknown": "క్షమించండి, మీ స్వరం అర్థం కాలేదు.",
        "request": "క్షమించండి, స్పీచ్ సేవ అందుబాటులో లేదు.",
    },
    "hi": {
        "unknown": "माफ़ कीजिए, मैं आपकी आवाज़ समझ नहीं पाया।",
        "request": "माफ़ कीजिए, स्पीच सेवा उपलब्ध नहीं है।",
    },
    "ta": {
        "unknown": "மன்னிக்கவும், உங்கள் குரலை புரிந்து கொள்ள முடியவில்லை.",
        "request": "மன்னிக்கவும், பேச்சு சேவை கிடைக்கவில்லை.",
    },
    "kn": {
        "unknown": "ಕ್ಷಮಿಸಿ, ನಿನ್ಗೆ ಧ್ವನಿಯನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲಾಗಲಿಲ್ಲ.",
        "request": "ಕ್ಷಮಿಸಿ, ಸ್ಪೀಚ್ ಸೇವೆ ಲಭ್ಯವಿಲ್ಲ.",
    }
}

def recognize_voice(language="te-IN"):
    recognizer = sr.Recognizer()
    lang_code = language.split("-")[0]  # e.g., "te" from "te-IN"

    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = recognizer.listen(source, phrase_time_limit=5)

    try:
        text = recognizer.recognize_google(audio, language=language)
        
        return text
    except sr.UnknownValueError:
        english_msg = ERROR_MESSAGES["en"]["unknown"]
        native_msg = ERROR_MESSAGES.get(lang_code, {}).get("unknown", "")
        return f"{english_msg}\n{native_msg}"
    except sr.RequestError:
        english_msg = ERROR_MESSAGES["en"]["request"]
        native_msg = ERROR_MESSAGES.get(lang_code, {}).get("request", "")
        return f"{english_msg}\n{native_msg}"
