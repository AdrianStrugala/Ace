import os

try:
  import pyttsx3
except ImportError:
  print ("Trying to Install required module: pyttsx3\n")
  os.system('python -m pip install pyttsx3')

import threading
import communication
import time

class Speech (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global  engine
        self.daemon = True     
        engine = pyttsx3.init()
     

    def say(self, text):
        if(not communication.mute_flag):
            engine.say(text)
            engine.runAndWait()

