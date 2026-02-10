import eel
import os
import platform
from queue import Queue
import pyttsx3
import webbrowser

class ChatBot:

    started = False
    userinputQueue = Queue()

    @staticmethod
    def isUserInput():
        return not ChatBot.userinputQueue.empty()

    @staticmethod
    def popUserInput():
        return ChatBot.userinputQueue.get()

    @staticmethod
    def close_callback(route, websockets):
        """Called when user closes the Eel window"""
        ChatBot.started = False
        exit()

    @staticmethod
    @eel.expose
    def getUserInput(msg):
        """Called from JS when user sends a message"""
        ChatBot.userinputQueue.put(msg)
        print("User:", msg)

    @staticmethod
    def addUserMsg(msg):
        """Send a message to the frontend chat from user"""
        try:
            eel.addUserMsg(msg)
        except AttributeError:
            print("USER:", msg)

    @staticmethod
    def addAppMsg(msg):
        """Send a message to the frontend chat from app"""
        try:
            eel.addAppMsg(msg)
        except AttributeError:
            print("APP:", msg)

    @staticmethod
    def start():
        # -------------------------------
        # Determine web folder path
        # -------------------------------
        path = os.path.dirname(os.path.abspath(__file__))  # src/
        web_folder = os.path.abspath(os.path.join(path, '..', 'web'))  # project_root/web
        print("Eel web folder:", web_folder)  # debug
        eel.init(web_folder, allowed_extensions=['.js', '.html'])

        # -------------------------------
        # Start Eel
        # -------------------------------
        try:
            # Open in default browser (optional)
            url = f"http://127.0.0.1:27005/index.html"
            webbrowser.open(url)

            eel.start(
                'index.html',
                mode=None,  # Use default browser
                host='127.0.0.1',
                port=27006,
                block=False,
                size=(350, 480),
                position=(10,100),
                disable_cache=True,
                close_callback=ChatBot.close_callback
            )
            ChatBot.started = True

            # -------------------------------
            # Initialize TTS engine
            # -------------------------------
            if platform.system() == "Windows":
                engine = pyttsx3.init("sapi5")
            else:
                engine = pyttsx3.init()  # macOS / Linux auto-select

            # Example greeting
            greeting = "Hello! I am your AI assistant."
            engine.say(greeting)
            engine.runAndWait()
            ChatBot.addAppMsg(greeting)

            # -------------------------------
            # Keep the Eel loop alive
            # -------------------------------
            while ChatBot.started:
                eel.sleep(10.0)

        except Exception as e:
            print("Eel error:", e)


if __name__ == "__main__":
    ChatBot.start()
