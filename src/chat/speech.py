import pyttsx3
import threading
import time

interval = 0.5

list_to_say = []

engine = pyttsx3.init()


def Run():
	while True:
		if (len(list_to_say) > 0):
			engine.say(list_to_say[0])
			engine.runAndWait()

		time.sleep(interval)


def Say(text):
	list_to_say.append(text)
