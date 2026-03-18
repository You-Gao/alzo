import speech_recognition as sr
import os
import time
from dotenv import load_dotenv
import keyboard

import helpers.mistral as mistral
import helpers.win32 as win32
import helpers.spotify as spotify
import helpers.sound as sound
import helpers.agent as agent

from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
load_dotenv()

COMMANDS = {
    # MISC
    ("hate", "game"): lambda command: keyboard.send('alt+f4'),
    ("clip", "that"): lambda command: print("Making a clip..."),
    
    # WINDOWS
    ("lock", "pc"): lambda command: os.system("rundll32.exe user32.dll,LockWorkStation"),
    ("shut", "down", "pc"): lambda command: os.system("shutdown /s /t 1"),
    ("restart", "pc"): lambda command: os.system("shutdown /r /t 1"),
    
    # OPEN/CLOSE COMMANDS
    ("open", "chrome"): lambda command: os.system("start chrome"),
    ("close", "chrome"): lambda command: os.system("taskkill /f /im chrome.exe"),
    ("open", "notepad"): lambda command: os.system("notepad"),
    ("close", "notepad"): lambda command: os.system("taskkill /f /im notepad.exe"),
    ("open", "code"): lambda command: os.system("code"),
    ("close", "code"): lambda command: os.system("taskkill /f /im Code.exe"),
    ("open", "habitica"): lambda command: os.system(r'start "" "https://habitica.com"'),
    ("close", "habitica"): lambda command: print("Habitica is a web app, no process to close."),
    ("open", "spotify"): lambda command: os.system("start spotify"),
    ("close", "spotify"): lambda command: os.system("taskkill /f /im Spotify.exe"),
    ("open", "discord"): lambda command: os.system("start discord"),
    ("close", "discord"): lambda command: os.system("taskkill /f /im Discord.exe"),
    ("open", "steam"): lambda command: os.system("start steam"),
    ("close", "steam"): lambda command: os.system("taskkill /f /im Steam.exe"),
    
    # GOTOs 
    ("go", "to", "chrome"): lambda command: win32.make_window_active("Google Chrome"),
    ("go", "to", "notepad"): lambda command: win32.make_window_active("Notepad"),
    ("go", "to", "code"): lambda command: win32.make_window_active("Visual Studio Code"),
    ("go", "to", "spotify"): lambda command: win32.make_window_active("Spotify"),
    ("go", "to", "discord"): lambda command: win32.make_window_active("Discord"),
    ("go", "to", "steam"): lambda command: win32.make_window_active("Steam"),
    
    # GOOGLE CHROME
    ("google",): lambda command: os.system(rf'start "" "https://www.google.com/search?q={command}"') if not command == "google" and command.startswith("google") else None,

    # SPOTIFY (Requires Premium) 
    # ("play", "music"): lambda command: spotify.play_pause(),
    # ("pause", "music"): lambda command: spotify.play_pause(),
    # ("stop", "music"): lambda command: spotify.play_pause(),
    # ("next", "song"): lambda command: spotify.next_track(),
    # ("skip", "song"): lambda command: spotify.next_track(),
    # ("previous", "song"): lambda command: spotify.previous_track(),
    # ("last", "song"): lambda command: spotify.previous_track(),
    # ("spotify","play", "by"): lambda command: spotify.play_artist_song(command.split("by ")[1].strip(), command.split("play ")[1].split(" by ")[0].strip()),
    # ("spotify","play",): lambda command: spotify.play_artist(command.replace("play ", "")),
    # ("clear", "q"): lambda command: spotify.clear_queue(),
    
    # SOUND
    ("play",): lambda command: sound.play_pause(),
    ("pause",): lambda command: sound.play_pause(),
    ("volume", "up"): lambda command: sound.volume_up(),
    ("volume", "down"): lambda command: sound.volume_down(),
    ("mute", "music"): lambda command: sound.mute(),
    ("mute",): lambda command: sound.mute(),

    # MISTRAL
    # ("question",): lambda command: mistral.call_mistral_with_question(command), 
    ("open", "chat"): lambda command: mistral.call_mistral_with_question(command), 
}

# Tools are just fed in as model input, try removing tools and seeing prompt tokens.
print("Setting Up Agent")
MISTRAL = ChatMistralAI(model="mistral-small-2503", temperature=.7)
SYSTEM_PROMPT = """
If the user is not asking a question or issuing a command, reply with the word Nothing.
Don't use text formatting when responding.
"""
AGENT = create_agent(model = MISTRAL, tools=agent.TOOLS, system_prompt=SYSTEM_PROMPT)
print("Agent Set-up!")

def action(command):
    for keywords, func in COMMANDS.items():
        command_words = command.replace(".","").split()
        contains_all = all((word in command_words for word in keywords))
        if contains_all:
            print(f"Executing command: {keywords}")
            func(command)
            return
    if len(command_words) > 5: # Don't want this running for random pick-ups
        result = AGENT.invoke({"messages": [{"role": "user", "content": f"{command}"}]})
        if result['messages'][-1].content.replace(".","") != "Nothing":
            win32.make_message_box(result['messages'][-1].content)
    return

def callback(recognizer, audio):
    try:
        command = recognizer.recognize_whisper(audio).lower()
        print(command)
        action(command)
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        pass

# INITIALIZE RECOGNITION
r = sr.Recognizer()
m = sr.Microphone()

r.pause_threshold = .75                      # How long to wait before considering speech ended
r.phrase_threshold = .25                   # Minimum audio length to consider as speech
r.non_speaking_duration = .5                # Minimum silence duration to split phrases

print("Adjusted to Ambient Noise")
with m as source: r.adjust_for_ambient_noise(source, duration=5)
r.listen_in_background(m, callback)
print("Set-up Complete!")

while True: time.sleep(2^32-1)