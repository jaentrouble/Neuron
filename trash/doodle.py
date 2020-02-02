from multiprocessing import Process, Queue, freeze_support
import time

class sample () :
    def __init__(self, a) :
        self.a = a

def creator(q) :
    for _ in range(5) :
        time.sleep(1)
        print('putting')
        t = sample([1,1])
        q.put(t)
    q.put(-1)

def consumer(q) :
    while True :
        data = q.get()
        if data == -1 :
            break
        print(data.a)

if __name__ == '__main__':
    freeze_support()
    q = Queue()

    proc1 = Process(target = creator, args = (q,))
    proc2 = Process(target = consumer, args = (q,))
    proc1.start()
    proc2.start()
    proc1.join()
    proc2.join()