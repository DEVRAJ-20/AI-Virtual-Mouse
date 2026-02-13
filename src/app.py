import eel
import os
import sys
from queue import Queue

class ChatBot:

    started = False
    userinputQueue = Queue()

    @staticmethod
    @eel.expose
    def getUserInput(msg):
        """Called from JS when user sends a message"""
        ChatBot.userinputQueue.put(msg)
        print("User:", msg)

    @staticmethod
    def isUserInput():
        """Check if there is user input waiting in the queue"""
        return not ChatBot.userinputQueue.empty()

    @staticmethod
    def popUserInput():
        """Pop the next user input from the queue"""
        return ChatBot.userinputQueue.get()

    @staticmethod
    def addAppMsg(msg):
        """Send a message to frontend"""
        try:
            eel.addAppMsg(msg)
        except Exception:
            print("APP:", msg)

    @staticmethod
    def close():
        """Gracefully shut down the Eel app"""
        try:
            sys.exit(0)
        except SystemExit:
            pass

    @staticmethod
    def start():
        path = os.path.dirname(os.path.abspath(__file__))  # src/
        web_folder = os.path.abspath(os.path.join(path, '..', 'web'))
        print("Eel web folder:", web_folder)
        eel.init(web_folder, allowed_extensions=['.js', '.html'])

        # Mark as started BEFORE blocking call (this runs in a thread)
        ChatBot.started = True

        try:
            # mode='default' lets Eel open the default browser
            # block=True keeps this thread alive to serve requests
            eel.start(
                'index.html',
                mode='default',
                host='127.0.0.1',
                port=8000,
                block=True
            )
        except Exception as e:
            print("Eel error:", e)


if __name__ == "__main__":
    ChatBot.start()
