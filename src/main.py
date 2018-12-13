# Install required modules
import os
import sys
os.system('python -m pip install --upgrade -r requirements.txt')

from chat import speech
from multiprocessing import Process, Manager
from user_interface import console



if __name__ == '__main__':
    with Manager() as manager:
        list_to_say = manager.list()
        stdin = sys.stdin.fileno()  # get original file descriptor
        processes = []

        p = Process(target=speech.Run, args=(list_to_say,))
        p.start()
        processes.append(p)

        p2 = Process(target=console.display_menu, args=(list_to_say, stdin))
        p2.start()
        processes.append(p2)

        for p in processes:
            p.join()
