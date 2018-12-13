import time
from multiprocessing import Process


def dupa():
    while True:
        print('dupa')

        time.sleep(1.75)

def liczba():
    i = 0
    while True:
        print(i)
        i+=1

        time.sleep(1)


def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()




if __name__ == '__main__':
	#pool = Pool(processes=2)

    runInParallel(dupa, liczba)
	#pool.apply_async(display_menu())
	#pool.apply_async(speech.Run())

#	main_thread = Process(target=dupa())
#	speech_thread = Process(target=liczba())
#	main_thread.daemon = True  # Daemonize thread
 #   main_thread.



#	main_thread.start()
#	speech_thread.start()

#	main_thread.join()
#	speech_thread.join()