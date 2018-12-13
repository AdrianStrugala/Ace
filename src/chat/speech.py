import pyttsx3
import threading
import time

interval = 0.5

list_to_say = []

engine = pyttsx3.init()


def Run(list_to_say, fn):
	while True:
		if (len(list_to_say) > 0):
			engine.say(list_to_say.pop(0))
			engine.runAndWait()

		time.sleep(interval)
