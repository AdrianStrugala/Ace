# Install required modules
import os

os.system('python -m pip install --upgrade -r requirements.txt')
from chat import create_database
from chat import create_training_data
from web_controller import open_website
from web_controller import google_phrase
from chat import speech
from programs import create_database as create_programs_database
from programs import clear_database as clear_programs_database
from programs import open_program
from programs import close_program
from programs import add_program_manually
# from chat.AI_nmt.setup import prepare_data as nmt_prepare_data
# from chat.AI_nmt import train
# from chat.AI_nmt.inference import inference
import subprocess
import colorama
from multiprocessing import Pool
from contextlib import contextmanager
import threading
import time
from multiprocessing import Process, Manager


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def sendMessage(text):
    print(f'{colorama.Fore.LIGHTRED_EX}{text}{colorama.Fore.RESET}')


# speech.Say(text)


def print_user_options():
    print("1 - Create Database")
    print("2 - Open Program")
    print("3 - Close Program")
    print("4 - Open Website")
    print("5 - Search in Google")
    print("6 - Clear Database")
    print("7 - Manually add program to the Database")
    print("8 - Teach me how to speak")
    print("")
    print("0 - Exit")


class switch(object):
    value = None

    def __new__(class_, value):
        class_.value = value
        return True


def case(*args):
    return any((arg == switch.value for arg in args))


def display_menu(list_to_say):
    os.chdir(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    sendMessage("Hello. My name is Ace!")
    list_to_say.append("Hello. My name is Ace!")

    user_choice = -1

    while user_choice != 0:
        sendMessage("")
        sendMessage("Make your choice")
        list_to_say.append("Make your choice")

        print_user_options()

        user_choice = int(input('Choice: '))

        while switch(user_choice):
            if case(1):
                sendMessage("Creating Database...")
                try:
                    create_programs_database.Execute()
                except Exception as e:
                    sendMessage("Cannot create database")
                    print(e)
                break

            if case(2):
                program_to_open = input('Type name of the program: ')
                sendMessage("Opening Program... " + program_to_open)
                try:
                    open_program.Execute(program_to_open)
                except Exception as e:
                    sendMessage("Cannot open " + program_to_open)
                    print(e)
                break

            if case(3):
                program_to_close = input('Type name of the program: ')
                sendMessage("Closing Program... " + program_to_close)
                try:
                    close_program.Execute(program_to_close)
                except Exception as e:
                    sendMessage("Cannot close" + program_to_close)
                    print(e)
                break

            if case(4):
                url_to_open = input('Write the url: ')
                sendMessage("Opening website... " + url_to_open)
                try:
                    open_website.Execute(url_to_open)
                except Exception as e:
                    sendMessage("Cannot navigate to" + url_to_open)
                    print(e)
                break

            if case(5):
                phrase_to_search = input('What are you looking for: ')
                sendMessage("Searching in Google for... " + phrase_to_search)
                try:
                    google_phrase.Execute(phrase_to_search)
                except Exception as e:
                    sendMessage("Cannot find " + phrase_to_search + " in Google")
                    print(e)
                break

            if case(6):
                sendMessage("Clearing database...")
                try:
                    clear_programs_database.Execute()
                except Exception as e:
                    sendMessage("Cannot clear database")
                    print(e)
                break

            if case(7):
                sendMessage("Adding program...")
                try:
                    add_program_manually.Execute()
                except Exception as e:
                    sendMessage("Cannot add program")
                    print(e)
                break

            if case(8):
                sendMessage("Learning how to speak...")
                try:
                    sendMessage("Gathering vocabulary")
                    #   create_database.Execute()
                    #  create_training_data.Execute()
                    with cd(os.getcwd() + "\AI_nmt\setup"):
                        sendMessage("Preparing data for train")
                    #	subprocess.call("py .\prepare_data.py")

                    # outside the context manager we are back wherever we started.
                    with cd(os.getcwd() + "\AI_nmt"):
                        sendMessage("The training begins now!")
                        print(os.getcwd())
                        subprocess.call("python -c \"from train import Execute; Execute()\"")

                except Exception as e:
                    sendMessage("I still cannot speak :(")
                    print(e)
                break

            if case(0):
                sendMessage("Exiting")
                break

            # print(inference(user_choice))
            break


def runInParallel(*fns):
    with Manager() as manager:
        list_to_say = manager.list()

        processes = []
        for fn in fns:
            p = Process(target=fn, args=(list_to_say,))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()


if __name__ == '__main__':
    runInParallel(speech.Run, display_menu)
