# Install required modules
import os
import sys
import time
os.system('python -m pip install --upgrade -r requirements.txt')

from chat import speech
from multiprocessing import Process, Manager
from user_interface import console


os.chdir(os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':
    with Manager() as manager:

        #shared variables
        list_to_say = manager.list()
        exit_list = manager.list()
        stdin = sys.stdin.fileno()  # get original file descriptor


        speech_process = Process(target=speech.Run, args=(list_to_say,))
        speech_process.daemon = True
        speech_process.start()

        user_interface_process = Process(target=console.display_menu, args=(list_to_say, stdin, exit_list))
        user_interface_process.daemon = True
        user_interface_process.start()

        #exit condition
        while(len(exit_list) == 0):
             time.sleep(1)
