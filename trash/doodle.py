from multiprocessing import Process, Queue, freeze_support
import time


def creator(q) :
    for _ in range(5) :
        time.sleep(1)
        print('putting')
        q.put('a')
    q.put(-1)

def consumer(q) :
    while True :
        data = q.get()
        print(data)
        print(1)
        if data == -1 :
            break

if __name__ == '__main__':
    freeze_support()
    q = Queue()

    proc1 = Process(target = creator, args = (q,))
    proc2 = Process(target = consumer, args = (q,))
    proc1.start()
    proc2.start()
    proc1.join()
    proc2.join()