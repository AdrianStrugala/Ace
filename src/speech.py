import pyttsx3
import threading
import time

class Speech (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global  engine
        engine = pyttsx3.init()
     

    def say(self, text, muteFlag):
        if(not muteFlag):
            engine.say(text)
            engine.runAndWait()

