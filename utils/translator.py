from deep_translator import MyMemoryTranslator, GoogleTranslator

def translate_text(text, target_lang):
    lang_codes = {
        "Telugu": "te",
        "Hindi": "hi",
        "English": "en",
        "Kannada": "kn",
        "Tamil": "ta",
    }
    try:
        dest_lang = lang_codes.get(target_lang, "en")
        # Try MyMemory first
        return MyMemoryTranslator(source='en', target=dest_lang).translate(text)
    except Exception as e:
        try:
            # Fallback to GoogleTranslator
            return GoogleTranslator(source='en', target=dest_lang).translate(text)
        except Exception as e2:
            return f"❌ Translation failed: {str(e2)}"
