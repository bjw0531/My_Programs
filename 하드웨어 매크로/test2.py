from multiprocessing import Process, Value, Array
from pynput.keyboard import Key, Listener
from threading import Thread
import time
from datetime import datetime

now = datetime.now()
filename = f"{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}.txt"

global key


def f():
    listener = Listener()
    listener.daemon = True
    listener.start()
    if key == True:


def on_press(key):
    global end, start
    end = time.time()
    timedelta = end - start

    with open(f'./macros/{filename}', 'a') as f:
        f.write(f'w{timedelta:.3f}\n')
        f.write(f'p{key}\n')

    print(f'{key} pressed')
    start = time.time()


def on_release(key):
    global end, start
    end = time.time()
    timedelta = end - start

    with open(f'./macros/{filename}', 'a') as f:
        f.write(f'w{timedelta:.3f}\n')
        f.write(f'r{key}\n')

    print(f'{key} release')
    start = time.time()


T = Thread(target=f)
T.start()
with Thread(target=f) as T:
    listener = Listener()
    listener.daemon = True
    listener.start()
    T.join()
