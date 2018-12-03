import pyttsx3
import threading
import time

engine = pyttsx3.init()   
        
     
def Say(text):
	engine.say(text)
	engine.runAndWait()

