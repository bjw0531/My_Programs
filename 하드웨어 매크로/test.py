from pynput.keyboard import Key, Listener
from datetime import datetime
import os
import time

now = datetime.now()

if not os.path.isdir('macros'):
    os.mkdir('macros')

f = open(
    f'./macros/{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}.txt', 'a')
f.close()


start = 0
end = 0


def on_press(key):
    global end, start
    end = time.time()
    timedelta = end - start

    with open(f'./macros/{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}.txt', 'a') as f:
        f.write(f'w{timedelta:.3f}\n')
        f.write(f'p{key}\n')

    print(f'{key} pressed')
    start = time.time()


def on_release(key):
    global end, start
    end = time.time()
    timedelta = end - start

    with open(f'./macros/{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}.txt', 'a') as f:
        f.write(f'w{timedelta:.3f}\n')
        f.write(f'r{key}\n')

    print(f'{key} release')
    if key == Key.esc:
        # Stop listener
        return False
    start = time.time()


listener = Listener(on_press=on_press, on_release=on_release)
listener.start()
start = time.time()  # 시작부터 첫키가 눌리기까지 시간
listener.join()
