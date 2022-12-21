from pynput.keyboard import Key, Listener
from pynput.keyboard._win32 import KeyCode
from datetime import datetime
import os
import time

thisdirpath = os.path.dirname(os.path.realpath(__file__))

global now
now = datetime.now()
filename = f'{thisdirpath}/macros/{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}.txt'
f = open(
    f'{filename}', 'a')
f.close()
global totaltime
totaltime = 0


def on_press(key):
    global end, start, totaltime
    end = time.time()
    delta = end - start
    totaltime += delta

    with open(f'{filename}', 'a') as f:
        f.write(f'w{delta:.3f}\n')
        f.write(f'p{key}\n')

    start = time.time()


def on_release(key):
    print(str(type(key)))
    with open(f'{filename}', 'a') as f:
        f.write(f'r{key}\n')


KeyCode.
listener = Listener(on_release=on_release)
listener.start()
time.sleep(1000)
