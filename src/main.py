import repository
import speech
import controller
import communication
import glob
import os
import win32com

def sendMessage(text):
    controller.write(text)
    #communication.to_say = text
    speech.say(text)


def print_user_options():
    print("1 - Create Database")
    print("2 - Open Program")
    print("3 - Close Program")
    print("4 - Open Website")
    print("5 - Search in Google")
    
    print("0 - Exit")

class switch(object):
    value = None

    def __new__(class_, value):
        class_.value = value
        return True


def case(*args):
    return any((arg == switch.value for arg in args))


if __name__ == '__main__':

    global muteFlag
    muteFlag = False

    speech = speech.Speech()
    controller = controller.Controller()

    sendMessage("Hello. My name is Ace!")

    user_choice = -1

    while user_choice != 0:
        print("")
        sendMessage("Make your choice")
        print_user_options()
        
        try:
            user_choice = int(input('Choice: '))
        except ValueError:
            sendMessage("Not a number")

        while switch(user_choice):
            if case(1):
                sendMessage("Creating Database...")
                try:
                    controller.create_database()
                except:
                    sendMessage("Cannot create database")
                break

            if case(2):
                program_to_open = input('Type name of the program: ')
                sendMessage("Opening Program..." + program_to_open)
                try:
                    controller.open_program(program_to_open)
                except:
                    sendMessage("Cannot open " + program_to_open)
                break

            if case(3):
                program_to_close = input('Type name of the program: ')
                sendMessage("Closing Program..." + program_to_close)
                try:
                    controller.close_program(program_to_close)
                except:
                    sendMessage("Cannot close" + program_to_close)
                break

            if case(4):
                url_to_open = input('Write the url: ')
                sendMessage("Opening website..." + url_to_open)
                try:
                    controller.open_website(url_to_open)
                except:
                    sendMessage("Cannot navigate to" + url_to_open)
                break

            if case(5):
                phrase_to_search = input('What are you looking for: ')
                sendMessage("Searching in Google for ..." + phrase_to_search)
                try:
                    controller.search_in_google(phrase_to_search)
                except:
                    sendMessage("Cannot find " + phrase_to_search + " in google")
                break

            if case(0):
                sendMessage("Exiting")
                break

            sendMessage("Unrecognized option.")
            break
