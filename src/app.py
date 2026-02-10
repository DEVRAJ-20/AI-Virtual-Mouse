import eel
import os
import platform
from queue import Queue
import pyttsx3

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
        exit()

    @staticmethod
    @eel.expose
    def getUserInput(msg):
        ChatBot.userinputQueue.put(msg)
        print("User:", msg)

    @staticmethod
    def close():
        ChatBot.started = False

    @staticmethod
    def addUserMsg(msg):
        try:
            eel.addUserMsg(msg)
        except AttributeError:
            print("USER:", msg)

    @staticmethod
    def addAppMsg(msg):
        try:
            eel.addAppMsg(msg)
        except AttributeError:
            print("APP:", msg)

    @staticmethod
    def start():
        path = os.path.dirname(os.path.abspath(__file__))
        # Cross-platform path to web folder
        eel.init(os.path.join(path, 'web'), allowed_extensions=['.js', '.html'])

        try:
            eel.start(
                'index.html',
                mode='chrome',
                host='localhost',
                port=27005,
                block=False,
                size=(350, 480),
                position=(10,100),
                disable_cache=True,
                close_callback=ChatBot.close_callback
            )
            ChatBot.started = True

            # Example TTS engine (cross-platform)
            if platform.system() == "Windows":
                engine = pyttsx3.init("sapi5")
            else:
                engine = pyttsx3.init()  # macOS / Linux auto-select

            # Example greeting
            engine.say("Hello! I am your AI assistant.")
            engine.runAndWait()
            ChatBot.addAppMsg("Hello! I am your AI assistant.")

            # Keep the Eel loop alive
            while ChatBot.started:
                eel.sleep(10.0)

        except Exception as e:
            print("Eel error:", e)


if __name__ == "__main__":
    ChatBot.start()
