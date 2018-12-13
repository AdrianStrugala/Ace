import time
from multiprocessing import Process, Manager


sth = 1

def dupa(L):
    while True:
        print('dupa')
        L.append(7)
        time.sleep(1.75)

def liczba(L):
    i = 0
    while True:
        print(i)
        i+=1
        print(L)
        time.sleep(1)


def runInParallel(*fns):
    with Manager() as manager:
        L = manager.list()

        processes = []
        for fn in fns:
            p = Process(target=fn, args=(L,))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()




if __name__ == '__main__':

    runInParallel(dupa, liczba)
