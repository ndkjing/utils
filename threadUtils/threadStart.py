# Code to execute in an independent thread
import time


def countdown(n):
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(1)


# Create and launch a thread
from threading import Thread

t = Thread(target=countdown, args=(10,))
t.start()
# t.join()

# while 1:
#     if t.is_alive():
#         time.sleep(1)
#     else:
#         print('t.is_alive()', t.is_alive())
#         break
