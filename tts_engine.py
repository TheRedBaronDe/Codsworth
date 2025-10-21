import pyttsx3

engine = None  

def setup_engine(shared_engine):
    global engine
    engine = shared_engine

def speak(text: str):
    if not text or engine is None:
        print("[TTS Warning] Engine not initialized or empty text.")
        return
    engine.say(text)
    engine.runAndWait()