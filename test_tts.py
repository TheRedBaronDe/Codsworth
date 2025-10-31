import pyttsx3
engine = pyttsx3.init()

for v in engine.getProperty('voices'):
    if "hazel" in v.name.lower():
        engine.setProperty('voice', v.id)
        break

engine.setProperty('rate', 175)
engine.setProperty('volume', 0.9)

lines = [
    "Hello, ma'am.",
    "Testing second sentence.",
    "And this is the third sentence."
]

for line in lines:
    print("Codsworth:", line)
    engine.say(line)
    engine.runAndWait()