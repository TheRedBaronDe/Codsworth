# import the important stuff, once I actually know which ones I need
import random
import re
import json
import os
from Mood import cods_mood, adjust_mood, decay_mood, apply_mood_tone


# set up a .json file with Codswoth's memories
def load_memory():
    if os.path.exists("memory.json"):
        with open("memory.json", "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {"name": "", "age": "", "mood": ""}
    else:
        return {"name": "", "age": "", "mood": ""}

# list of Codsworth "memories"
memory = load_memory()

#saves memories to a .json file
def save_memory(memory):
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=4)

# saves personality to a .json file
def save_personality(data):
    with open("personality.json", "w") as file:
        json.dump(data, file, indent=4) 

# set up a .json file with Codsworth's personality traits
def load_personality():
    if os.path.exists("personality.json"):
        with open("personality.json", "r") as file:
            return json.load(file)
    else:
        personality = { # list of Codsworth personality
            "funny": 7, # 0 to 10 - how often it jokes
            "curious": 7, # 0 to 10 - how often it asks questions  
            "formal": 9, # 0 to 10 - how formal it sounds
            "empathetic": 6, # 0 to 10 - how emotional it sounds
            "psychological": 9, # 0 to 10 - how much it analyses the user/asks the root of the user's feelings and actions
        }
        save_personality(personality)
        return personality

# loads Codsworth's personality traits
personality = load_personality()


# list of responses
responses = {
    "Greetings": ["Good day, Victoria!", "Greetings, V!", "Oh, hello there!", "Hi, there!", "How can I assist you, ma'am?"],

    "How are you?": ["Just had a horrible dream last night. I was a program written in C!", "I'm *feeling* great"],

    "Who Cods": ["Why, I'm Codsworth, of course!", "Having amnesia, aren't we, ma'am?", "I'm a simple AI assistant"],

    "Joke": ["Why do programmers prefer dark mode? Because light attracts bugs!", "Why do Java developers wear glasses? Because they don't see sharp.", 
      "How many programmers does it take to change a light bulb? None, that's a hardware problem!", 
      "A proton walks into a bar and asks, 'Do you want to hear a joke about electrons?' The bartender replies, 'I'm positive.'", "I went to the zoo the other day and they only had a dog! It was a Shitzu"],

    "Love": ["That's certainly sad.", "Getting emotional, ma'am?", "I love you too."],

    "Pride": ["Why, thank you, ma'am!", "I'm great, right?", "The best A.I in the whole neighbourhood, innit?"],

    "British": ["Innit, fam?"],

    "Weather": ["Not sure, ma'am.", "Just look through the window."],

    "Alarm": ["I'll set the alarm for you, ma'am.", "Someday, ma'am."],

    "Insult": ["Well, fuck you, then!", "No way I heard that", "That's a damn lie!", "Hell nah."],
}

# makes Cods remember things
def remember(key, value):
    memory[key] = value
    save_memory(memory)

# makes Codsworth change its tone based on  user's input
def personality_filter(response, personality):

    if personality["funny"] > 7:
        response = "Hahah " + response
    if personality["curious"] > 6 and random.random() < 0.3:
        response += " Why?"
    if personality["formal"] > 7 and random.random() < 0.2:
        response = "Ma'am, " + response.lower()
    if personality["empathetic"] > 8:
        response = response.replace("Ma'am", "Dear")
    if personality["psychological"] > 7 and random.random() < 0.3:
        response += " What makes you feel what you're feeling right now?"
        
    response = apply_mood_tone(response)
    return response


# makes Codsworth act differently based on user's inputs
def evolve_personality(event):
    if event == "compliment":
        personality["empathetic"] += 0.2
        personality["psychological"] += 0.2
    elif event == "insult":
        personality["empathetic"] -= 0.5
        personality["curious"] -= 0.3
        personality["psychological"] += 0.2
    elif event == "long_chat":
        personality["curious"] += 0.1
    elif event == "humor":
        personality["funny"] += 0.2

    # Keep traits within 0–10 range
    for key in personality:
        if isinstance(personality[key], (int, float)):
            personality[key] = min(max(personality[key], 0), 10)
        
    adjust_mood(event)
    save_personality(personality)

# get user's input
def get_response(user_input):
    if re.search(r"\b(thank you|thanks|you're awesome|love you|I love you)\b", user_input, re.IGNORECASE):
        evolve_personality("compliment")
    if re.search(r"\b(stupid|idiot|useless|dumbass|shut up|fuck you|asshole|bitch|imbecile)\b", user_input, re.IGNORECASE):
        evolve_personality("insult")
    if re.search(r"\b(sad|lonely|tired|depressed|terrible|miserable|broken|heartbroken)\b", user_input, re.IGNORECASE):
        evolve_personality("compliment")  
        adjust_mood("sad_stuff")           


    # uses RegEx to match patterns and make the code cleaner and "smarter"
    patterns = [
        (r"\b(hello|hi|hey|greetings|morning)\b", "Greetings"),
        (r"\b(how are you|how's it going|how do you do|how are you feeling|are you okay|everything alright)\b", "How are you?"),
        (r"\b(who are you|what is your name|who is cods)\b", "Who Cods"),
        (r"\b(tell me a joke|make me laugh|say something funny|joke)\b", "Joke"),
        (r"\b(i love you|love you|love ya|i like you|like you)\b", "Love"),
        (r"\b(you're great|you're awesome|you're the best|proud of you|you're my pride and joy)\b", "Pride"),
        (r"\b(british|be brit|show me your true form)\b", "British"),
        (r"\b(weather|how's the weather|is it raining|is it sunny|is it hot|is it cold)\b", "Weather"),
        (r"\b(alarm|set an alarm|wake me up|remind me)\b", "Alarm"),
        (r"\b(stupid|idiot|useless|dumbass|shut up|fuck you|asshole|bitch|imbecile)\b", "Insult"),
    ]
    
    user_input = user_input.lower()

    for pattern, key in patterns:
        if re.search(pattern, user_input):
            response = random.choice(responses[key])
            response = personality_filter(response, personality)
            return response
    
# Saves user's info to a json file
    # User's name
    match = re.search(r"\b(My name is|Call me)\s+([A-Za-z]+)\b(?!\s*(years old|year old|\d))", user_input, re.IGNORECASE)
    if match: 
        name = match.group(2)
        memory["name"] = name
        save_memory(memory)
        return f"Good to meet you, {memory['name']}!"
    
    # User's age
    match = re.search(r"\b(I[' ]?m|I am|My age is)\b", user_input, re.IGNORECASE)
    if match:
        age = re.search(r"\b\d+\b", user_input)
        if age:
            memory["age"] = int(age.group(0))
            save_memory(memory)

            if memory["age"] < 18:
                return f"Still quite young, aren't we?"
            elif memory["age"] < 30:
                return f"Best years of your life!"
            else:
             return f"Years of experience, ma'am."
        
    # User's mood
    match = re.search(r"\b(I[' ]?m|I am)\s+(happy|sad|angry|tired|excited|bored|lonely|anxious|fine|okay|good|great|terrible)\b", user_input, re.IGNORECASE)
    if match:
        mood = match.group(2).lower()
        memory["mood"] = mood
        save_memory(memory)

        if mood in ["happy", "excited", "good", "great"]:
            return f"Good to hear."
        elif mood in ["sad", "lonely", "tired", "terrible", "anxious"]:
            return f"Maybe you should talk to a human instead."
        elif mood == "angry":
            return f"Think logically."
        elif mood in ["fine", "okay", "bored"]:
            return f"Why not take a break?"

    # Default response if no patterns match
    return personality_filter("I'm not sure how to respond to that, ma'am.", personality)


# main function that runs Codsworth/greetings and loops
def main():
    global memory
    memory = load_memory() # loads what's stored in the json file
    print("Codsworth: Hello, ma'am!" )

    if memory["name"]:
        print(f"Codsworth: Welcome back, {memory['name']}. Need anything?") # remembers user's name
    if memory["mood"]:
        print(f"Codsworth: I remember you were feeling {memory['mood']} last time.") # remembers user's mood

    while True:
        decay_mood()
        # print(mood_debug())

        user_input_text = input("Me: ")
        if user_input_text.lower() in ["exit", "quit", "bye", "farewell", "goodbye"]:
            print("Codsworth: Goodbye, ma'am!")
            break
        response = get_response(user_input_text)
        print(f"Codsworth: {response}")


# make it run
if __name__ == "__main__":
    main()