import speech_recognition as sr

print (sr.__version__)


mic = sr.Microphone()
r = sr.Recognizer()

with mic as source:
    print("Say something!")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)


# recognize speech using Google Speech Recognition
try:
    print("Karolina: " + r.recognize_google(audio, language="pl_PL"))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

# # recognize speech using Sphinx
# try:
#     print("Sphinx thinks you said: " + r.recognize_sphinx(audio))
# except sr.UnknownValueError:
#     print("Sphinx could not understand audio")
# except sr.RequestError as e:
#     print("Sphinx error; {0}".format(e))