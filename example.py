import threading
import time

def thread1(num):
    while True:
        print(num)
        time.sleep(2)


def thread2(num):
    while True:
        print(num)
        time.sleep(2)

t1 = threading.Thread(target=thread1, args=(1,))
t2 = threading.Thread(target=thread2, args=(2,))
t1.start
t2.start