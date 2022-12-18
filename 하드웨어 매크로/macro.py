import os
import sys
import time
import winsound
import keyboard
import msvcrt as m
import pyautogui
from ctypes import *
from datetime import datetime
from pynput.keyboard import Key, Listener

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pynput import keyboard
from threading import Thread
from multiprocessing import Process
import multiprocessing


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# 변수 선언
form = resource_path("main.ui")
form_class = uic.loadUiType(form)[0]
app = QApplication
recordThreadStopper = False

# User32 불러오기
hllDll = WinDLL("User32.dll")

# 함수 선언
VK_Capital = 0x14
VK_ScrollLock = 0x91
start = 0
end = 0


def getLockState(Key):
    """
    Key:
    VK_Capital
    VK_ScrollLock
    """
    return hllDll.GetKeyState(Key)


def switchLocks(Key):
    """
    Key:
    VK_Capital
    VK_ScrollLock
    """
    hllDll.keybd_event(Key, 0X3a, 0X1, 0)
    hllDll.keybd_event(Key, 0X3a, 0X3, 0)


# qt
class recordThread(QThread):
    finished = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        # 5초 대기
        for i in range(5, 0, -1):
            self.parent.status.setText(str(i) + '...')
            time.sleep(1)
        self.parent.status.setText('녹화중...')

        # 폴더 없으면 폴더 만들기
        if not os.path.isdir('macros'):
            os.mkdir('macros')

        # 파일 만들기
        global now
        now = datetime.now()
        filename = f'./macros/{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}.txt'
        f = open(
            f'{filename}', 'a')
        f.close()

        # 함수 선언
        def on_press(key):
            global end, start
            end = time.time()
            timedelta = end - start

            with open(f'{filename}', 'a') as f:
                f.write(f'w{timedelta:.3f}\n')
                f.write(f'p{key}\n')

            start = time.time()

        def on_release(key):
            global end, start
            end = time.time()
            timedelta = end - start

            with open(f'{filename}', 'a') as f:
                f.write(f'w{timedelta:.3f}\n')
                f.write(f'r{key}\n')

            start = time.time()

        listener = Listener(on_press=on_press, on_release=on_release)
        listener.start()
        global start
        start = time.time()  # 시작부터 첫키가 눌리기까지 시간

        # recordThreadStopper가 True가 되면 정지
        while True:
            if recordThreadStopper:
                listener.stop()
                break
            time.sleep(0.1)

        listener.join()
        # listener가 끝나면
        self.parent.status.setText('대기중...')
        return


# class locksListener(QThread):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent

#     def run(self):


class MyThread(QThread):
    cnt = 0
    running = False
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def on_press(self, key):
        if key == keyboard.Key.f5:
            self.finished.emit()

    def run(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 500)
        self.setupUi(self)
        self.show()
        self.raise_()

        # 녹화버튼
        self.recordBtn: QPushButton
        self.recordBtn.clicked.connect(self.Record)
        self.recordThread = recordThread(self)

        # 중단/저장버튼
        self.stopsaveBtn: QPushButton
        self.stopsaveBtn.clicked.connect(self.StopSave)

        # 불러오기버튼
        self.loadBtn: QPushButton
        self.loadBtn.clicked.connect(self.Load)

        # 삭제버튼
        self.deleteBtn: QPushButton
        self.deleteBtn.clicked.connect(self.Delete)

        # 파일경로 라인에딧
        self.filepath: QLineEdit
        self.filepath_str = ''

        # 상태 라벨
        self.status: QLabel

        # AlwaysOnTop
        self.AlwaysOnTop: QCheckBox
        self.AlwaysOnTop.stateChanged.connect(self.AOT)

        # DD 로드하기
        self.DD = windll.LoadLibrary('./DDHID64.dll')

    def Record(self):
        global recordThreadStopper
        recordThreadStopper = False
        self.recordThread.start()

    def StopSave(self):
        global recordThreadStopper
        recordThreadStopper = True

    def Load(self):
        self.filepath_str = QFileDialog.getOpenFileName(
            None, '파일을 선택하세요.', os.getenv('HOME'), '텍스트 파일(*.txt)')[0]

        self.filepath.setText(self.filepath_str)

    def Delete(self):
        self.filepath.setText('')
        self.filepath_str = None

    def AOT(self):
        if self.AlwaysOnTop.isChecked():
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.show()
        else:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            self.show()


if __name__ == "__main__":
    app = app(sys.argv)
    global window
    window = MyWindow()
    app.exec_()
