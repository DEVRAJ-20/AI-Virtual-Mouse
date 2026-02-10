import eel
import os
import platform
import socket
from queue import Queue
import pyttsx3
import webbrowser

class ChatBot:

    started = False
    userinputQueue = Queue()

    @staticmethod
    def get_free_port():
        """Find a free port automatically"""
        s = socket.socket()
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    @staticmethod
    @eel.expose
    def getUserInput(msg):
        """Called from JS when user sends a message"""
        ChatBot.userinputQueue.put(msg)
        print("User:", msg)

    @staticmethod
    def addAppMsg(msg):
        """Send a message to frontend"""
        try:
            eel.addAppMsg(msg)
        except AttributeError:
            print("APP:", msg)

    @staticmethod
    def start():
        # -------------------------------
        # Set web folder path
        # -------------------------------
        path = os.path.dirname(os.path.abspath(__file__))  # src/
        web_folder = os.path.abspath(os.path.join(path, '..', 'web'))
        print("Eel web folder:", web_folder)
        eel.init(web_folder, allowed_extensions=['.js', '.html'])

        # -------------------------------
        # Pick a free port
        # -------------------------------
        port = ChatBot.get_free_port()
        url = f"http://127.0.0.1:{port}/index.html"

        # -------------------------------
        # Start Eel server
        # -------------------------------
        try:
            # Open in default browser
            webbrowser.open(url)

            # Start Eel (blocking mode)
            eel.start(
                'index.html',
                mode=None,   # default browser
                host='127.0.0.1',
                port=port,
                block=True
            )

        except Exception as e:
            print("Eel error:", e)

        # -------------------------------
        # TTS greeting after Eel starts
        # -------------------------------
        try:
            if platform.system() == "Windows":
                engine = pyttsx3.init("sapi5")
            else:
                engine = pyttsx3.init()  # macOS / Linux auto-select

            greeting = "Hello! I am your AI assistant."
            engine.say(greeting)
            engine.runAndWait()
            ChatBot.addAppMsg(greeting)
        except Exception as e:
            print("TTS error:", e)


if __name__ == "__main__":
    ChatBot.start()
