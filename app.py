import speech_recognition as sr
import os
import webbrowser
import datetime
import pygame
import configparser
from gtts import gTTS
import requests
from bs4 import BeautifulSoup
import re
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import os.path

def get_name():
    if os.path.isfile("name.txt"):
        with open("name.txt", "r") as f:
            if not ("sorry" in f.read()):
                name = f.read()

    else:
        say("Please say your name sir")
        name = takeCommand()
        if "sorry" in name:
            while "sorry" in name:
                say("I couldnt get your name please repeat")
                name = takeCommand()
        else:
            with open("name.txt", "w") as f:
                f.write(name)
    return name

def get_google_description(query):
    search_url = f"https://www.google.com/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    description_header = soup.find('h3', class_='bNg8Rb OhScic zsYMMe BBwThe', string='Description')
    if description_header:

        description_span = description_header.find_next('span')

        if description_span:
            return description_span.get_text()

    return "Description not found."


def get_query(query, excluded_words):
    words = query.split(' ')
    pattern = re.compile(r'\b(?:' + '|'.join(excluded_words) + r')\b', re.IGNORECASE)
    words = [word for word in words if not pattern.search(word)]
    query = ' '.join(words)

    return query


def get_google_query(query):
    exclude_words = ["google", "search", "on", "in", "about"]
    words = query.split(' ')
    pattern = re.compile(r'\b(?:' + '|'.join(exclude_words) + r')\b', re.IGNORECASE)
    words = [word for word in words if not pattern.search(word)]
    query = ' '.join(words)
    return query

def say(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    filename = "temp_audio.mp3"
    tts.save(filename)

    pygame.mixer.init()

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    os.remove(filename)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        # print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-IN")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return "Sorry, I did not understand that."
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "Sorry, there was an issue with the speech recognition service."


def my_assist():
    name = get_name()
    print('Welcome to MY ASSIST A.I')
    say(f" hi {name} how are you i am MY ASSIST A.I")
    musicpath = "C:/Users/path_to_music"
    while True:
        print("Listening...")
        query = takeCommand()

        if "the time" in query.lower():
            now = datetime.datetime.now()
            time = now.strftime("%I:%M %p")
            say(f"{name}, the time is {time}")
        elif "date" in query.lower():
            date = datetime.date.today().strftime("%B %d, %Y")
            say(f"{name}, today's date is {date}")

        elif "quit".lower() in query.lower():
            say(f"Goodbye, {name}")
            exit()

        elif "google".lower() in query.lower():
            search_query = get_google_query(query)
            say(f"Googling about {search_query}")
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(url)
            say(get_google_description(search_query))

        elif "unmute".lower() in query.lower() or "un mute".lower() in query.lower():
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(0, None)
            say(f"UnMuted volume {name}")

 
        elif "mute".lower() in query.lower():
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(1, None)

        elif "who your master".lower() in query.lower():
            say("Its Veera babu")
        elif "stop listening".lower() in query.lower():
            say(f"Okay {name}, waiting for your command.")
            while True:
                print("Waiting ...")
                query = takeCommand()
                print(f"Received query during while waiting")
                if "start".lower() in query.lower():
                    say(f"Starting, {name}.")
                    break
        elif "help".lower() in query.lower():
            say(" To search on google")
            say("Say google about search query")
            say("To quit say MY ASSIST quit")
            say("To Mute the volume say mute the volume")
            say("To unmute the volume say unmute the volume")

        else:
            say("I'm not sure what you mean. Please try again.")

my_assist()