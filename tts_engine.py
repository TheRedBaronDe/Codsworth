from gtts import gTTS
from playsound import playsound
import os
import tempfile
import threading

def speak(text):
    if not text:
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name

    try:
        tts = gTTS(text=text, lang='en', tld='co.uk')
        tts.save(temp_path)

        # Play sound
        playsound(temp_path)

    except Exception as e:
        print(f"[TTS Error] {e}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def speak_async(text):
    threading.Thread(target=speak, args=(text,)).start()