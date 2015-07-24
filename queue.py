from Queue import Queue

q = Queue(maxsize=0)

def add(q):
    while True:
        q.put(2)
        time.sleep(0.5)

def read(q):
    while True:
        while not q.empty():
            print q.get()
            q.task_done()
        time.sleep(5)
        print "----"

start_new_thread(add,(q,))
start_new_thread(read,(q,))
