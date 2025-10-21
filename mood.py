# Codsworth mood
import random

# Codsworth's current emotion
cods_mood = {
    "state": "neutral",   
    "intensity": 5.0      # 0.0 (calm) to 10.0 (extreme)
}


# Mood adjustment
def adjust_mood(event):
    """Adjust Codsworth's temporary mood based on user interaction events."""
    global cods_mood

    changes = {
        "compliment": ("happy", 2.0),
        "insult": ("annoyed", 3.0),
        "long_chat": ("curious", 1.0),
        "humor": ("proud", 1.5),
        "ignored": ("tired", 1.0),
        "sad_stuff": ("sad", 2.5),
    }

    if event not in changes:
        return

    new_state, delta = changes[event]

    if cods_mood["state"] == new_state:
        cods_mood["intensity"] = min(10.0, cods_mood["intensity"] + delta)
    else:
        # Blends moods
        cods_mood["state"] = new_state
        cods_mood["intensity"] = min(10.0, cods_mood["intensity"] * 0.6 + delta)


# Mood decay over time
def decay_mood():
    """Gradually move Codsworth's mood intensity toward a neutral baseline (5.0)."""
    if cods_mood["intensity"] > 5.0:
        cods_mood["intensity"] -= 0.1
    elif cods_mood["intensity"] < 5.0:
        cods_mood["intensity"] += 0.1

    # Prevents precision issues
    cods_mood["intensity"] = round(cods_mood["intensity"], 2)


# Codsworth's verbal tone
def apply_mood_tone(response):
    """Modify Codsworth's verbal tone based on current mood."""
    mood = cods_mood["state"]
    intensity = cods_mood["intensity"]

    # Adjust speech
    if mood == "happy" and intensity > 6:
        response = response.replace("ma'am", "my dear").replace("Ma'am", "My dear")
        response += " Are you as happy as me?"

    elif mood == "annoyed":
        if intensity > 6:
            response = f"({random.choice(['Sigh...', 'Oh, please...'])}) " + response
        else:
            response = response.replace("ma'am", "ma’am...").replace("Ma'am", "Ma’am...")

    elif mood == "sad" and intensity > 5:
        response = "I feel like I'm on a Radiohead song right now... " + response

    elif mood == "proud":
        response = "With pride, " + response

    elif mood == "curious" and intensity > 5:
        response += " Fascinating, truly."

    return response


# Debug
def mood_debug():
    """Optional helper for live monitoring."""
    return f"[Mood: {cods_mood['state']} | Intensity: {cods_mood['intensity']}]"