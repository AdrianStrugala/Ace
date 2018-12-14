# Install required modules
import os
import sys
os.system('python -m pip install --upgrade -r requirements.txt')

from chat import speech
from multiprocessing import Process, Manager
from user_interface import console

import time



if __name__ == '__main__':
    with Manager() as manager:
        list_to_say = manager.list()
        stdin = sys.stdin.fileno()  # get original file descriptor
        processes = []

        p = Process(target=speech.Run, args=(list_to_say,))
        p.daemon = True
        p.start()
        processes.append(p)

        p2 = Process(target=console.display_menu, args=(list_to_say, stdin))
        p2.daemon = True
        p2.start()
        processes.append(p2)

       # p.join()

        while(True):
           # print(2)
            time.sleep(1)
            print ("Child process state: %d" % p.is_alive())

        # for p in processes:
        #     p.join()
