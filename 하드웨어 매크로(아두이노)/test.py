import os
import sys
import time
import winsound
import keyboard as kb
import msvcrt as m
import pyautogui
from ctypes import *
from datetime import datetime
from datetime import timedelta
from pynput.keyboard import Key, Listener

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pynput import keyboard
from threading import Thread
from multiprocessing import Process
import multiprocessing
import key
import debugpy

classdd = CDLL(f"./DDHID64.dll")
st = classdd.DD_btn(0)  # DD Initialize

if st == 1:
    print("OK")
    time.sleep(0.2)
    classdd.DD_key(601, 1)
    classdd.DD_key(601, 2)
else:
    print("Error")
    exit(101)
now = datetime.now()

if not os.path.isdir('macros'):
    os.mkdir('macros')

start = 0
end = 0

filepath_str = './macros/2022.12.21.20.59.49.txt'

f = open(filepath_str, 'r')
line = None
while True:
    line = f.readline()
    if line == '':
        break

    value = line[1:-1]
    if line[0] == 'p':
        print(f'press {value}')
        try:
            value = key.keydict[value]

            classdd.DD_key(value, 1)
        except Exception as e:
            print(f'Error : {e}')
            raise

    elif line[0] == 'r':
        print(f'release {value}')
        try:
            value = key.keydict[value]

            classdd.DD_key(value, 2)
        except Exception as e:
            print(f'Error : {e}')
            raise

    elif line[0] == 'w':
        print(f'wait {value}')
        time.sleep(float(value))

f.close()


# listener = Listener(on_press=on_press, on_release=on_release)
# listener.start()
# start = time.time()  # 시작부터 첫키가 눌리기까지 시간
# listener.join()
