# Install required modules
import os
import sys
os.system('python -m pip install --upgrade -r requirements.txt')

from chat import speech
from multiprocessing import Process, Manager
from graphical_user_interface import GUI





def runInParallel(*fns):
    with Manager() as manager:
        list_to_say = manager.list()
        xd = sys.stdin.fileno()  # get original file descriptor
        processes = []
        for fn in fns:
            p = Process(target=fn, args=(list_to_say,xd,))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()


if __name__ == '__main__':
    runInParallel(speech.Run, GUI.display_menu)
