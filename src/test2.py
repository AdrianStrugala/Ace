import speech_recognition as sr

print (sr.__version__)

mic = sr.Microphone()
r = sr.Recognizer()

with mic as source:
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)