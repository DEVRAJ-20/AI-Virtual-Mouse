import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
import platform
import subprocess
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import Gesture_Controller
import app
from threading import Thread
today = date.today()
r = sr.Recognizer()
keyboard = Controller()

# TTS setup — use macOS native 'say' command to avoid pyttsx3 hanging
IS_MAC = platform.system() == 'Darwin'
if not IS_MAC:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

file_exp_status = False
files =[]
path = ''
is_awake = True  
def reply(audio):
    app.ChatBot.addAppMsg(audio)
    print(audio)
    try:
        if IS_MAC:
            # Use macOS native 'say' — non-blocking, no hang
            subprocess.Popen(['say', audio])
        else:
            engine.say(audio)
            engine.runAndWait()
    except Exception as e:
        print(f"TTS error: {e}")


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        reply("Good Morning!")
    elif hour>=12 and hour<18:
        reply("Good Afternoon!")   
    else:
        reply("Good Evening!")  
        
    reply("I am Proton, how may I help you?")

r.energy_threshold = 500
r.dynamic_energy_threshold = False

mic_available = True

def record_audio():
    global mic_available
    if not mic_available:
        return None  # Signal to wait for text input
    try:
        with sr.Microphone() as source:
            r.pause_threshold = 0.8
            voice_data = ''
            audio = r.listen(source, phrase_time_limit=5)

            try:
                voice_data = r.recognize_google(audio)
            except sr.RequestError:
                reply('Sorry my Service is down. Plz check your Internet connection')
            except sr.UnknownValueError:
                pass
            return voice_data.lower()
    except (AttributeError, OSError) as e:
        print(f"Microphone not available: {e}")
        print("Switching to text-only mode. Use the chat window.")
        mic_available = False
        return None

def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(voice_data)
    voice_data = voice_data.replace('proton','').strip()

    if is_awake==False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()
    elif 'hello' in voice_data or 'hi' in voice_data:
        wish()

    elif 'what is your name' in voice_data:
        reply('My name is Proton!')

    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'search' in voice_data:
        reply('Searching for ' + voice_data.split('search')[1])
        url = 'https://google.com/search?q=' + voice_data.split('search')[1]
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    elif 'location' in voice_data or 'find' in voice_data:
        # Extract location from the command text
        location = voice_data
        for word in ['location', 'find', 'a', 'the']:
            location = location.replace(word, '')
        location = location.strip()
        if location:
            reply(f'Locating {location}...')
            url = 'https://google.com/maps/place/' + location
            try:
                webbrowser.get().open(url)
                reply('This is what I found Sir')
            except:
                reply('Please check your Internet')
        else:
            reply('Please specify a location, e.g.: proton find location Mumbai')

    elif ('bye' in voice_data) or ('by' in voice_data):
        reply("Good bye Sir! Have a nice day.")
        is_awake = False

    elif ('exit' in voice_data) or ('terminate' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
    
        sys.exit()
    
    elif 'launch gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            reply('Gesture recognition is already active')
        else:
            gc = Gesture_Controller.GestureController()
            t = Thread(target = gc.start)
            t.start()
            reply('Launched Successfully')

    elif ('stop gesture recognition' in voice_data) or ('top gesture recognition' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
            reply('Gesture recognition stopped')
        else:
            reply('Gesture recognition is already inactive')
        
    elif 'copy' in voice_data:
        _mod_key = Key.cmd if platform.system() == 'Darwin' else Key.ctrl
        with keyboard.pressed(_mod_key):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')
          
    elif 'page' in voice_data or 'pest'  in voice_data or 'paste' in voice_data:
        _mod_key = Key.cmd if platform.system() == 'Darwin' else Key.ctrl
        with keyboard.pressed(_mod_key):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')
        
    elif 'list' in voice_data:
        counter = 0
        path = os.path.expanduser('~')
        files = listdir(path)
        filestr = ""
        for f in files:
            counter+=1
            print(str(counter) + ':  ' + f)
            filestr += str(counter) + ':  ' + f + '<br>'
        file_exp_status = True
        reply('These are the files in your root directory')
        app.ChatBot.addAppMsg(filestr)
        
    elif file_exp_status == True:
        counter = 0   
        if 'open' in voice_data:
            if isfile(join(path,files[int(voice_data.split(' ')[-1])-1])):
                filepath = os.path.join(path, files[int(voice_data.split(' ')[-1])-1])
                if platform.system() == 'Darwin':
                    subprocess.Popen(['open', filepath])
                elif platform.system() == 'Windows':
                    os.startfile(filepath)
                else:
                    subprocess.Popen(['xdg-open', filepath])
                file_exp_status = False
            else:
                try:
                    path = path + files[int(voice_data.split(' ')[-1])-1] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter+=1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    reply('Opened Successfully')
                    app.ChatBot.addAppMsg(filestr)
                    
                except:
                    reply('You do not have permission to access this folder')
                                    
        if 'back' in voice_data:
            filestr = ""
            home = os.path.expanduser('~')
            if path == home or path == home + os.sep:
                reply('Sorry, this is the root directory')
            else:
                path = os.path.dirname(os.path.normpath(path)) + os.sep
                files = listdir(path)
                for f in files:
                    counter+=1
                    filestr += str(counter) + ':  ' + f + '<br>'
                    print(str(counter) + ':  ' + f)
                reply('ok')
                app.ChatBot.addAppMsg(filestr)
                   
    else: 
        reply('I am not functioned to do this !')

t1 = Thread(target = app.ChatBot.start)
t1.start()

while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None
while True:
    if app.ChatBot.isUserInput():
        voice_data = app.ChatBot.popUserInput()
    else:
        voice_data = record_audio()
        if voice_data is None:
            # Mic unavailable — wait for text input
            time.sleep(0.5)
            continue

    if voice_data and 'proton' in voice_data:
        try:
            respond(voice_data)
        except SystemExit:
            reply("Exit Successful")
            break
        except Exception as e:
            print(f"Error: {e}")
            break
