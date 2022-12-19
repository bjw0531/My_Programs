import os
import sys
import time
import winsound
import keyboard
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
thisdirpath = os.path.dirname(os.path.realpath(__file__))

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
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        self.is_idle = False
        # 5초 대기
        for i in range(5, 0, -1):
            self.parent.status.setText(str(i) + '...')
            time.sleep(1)
        self.parent.status.setText('녹화중...')

        # 폴더 없으면 폴더 만들기
        if not os.path.isdir(f'{thisdirpath}/macros'):
            os.mkdir(f'{thisdirpath}/macros')

        # 파일 만들기
        global now
        now = datetime.now()
        filename = f'{thisdirpath}/macros/{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}.txt'
        f = open(
            f'{filename}', 'a')
        f.close()
        global totaltime
        totaltime = 0

        # 함수 선언
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
            global end, start, totaltime
            end = time.time()
            delta = end - start
            totaltime += delta

            with open(f'{filename}', 'a') as f:
                f.write(f'w{delta:.3f}\n')
                f.write(f'r{key}\n')

            start = time.time()

        def onelinewrite(path,text):
            f = open(filename,'a')
            f.write(text)
            f.close()
        
        def hms(s):
            hours = s // 3600
            s = s - hours*3600
            mu = s // 60
            ss = s - mu*60
            return f'{str(hours).zfill(2)}:{str(mu).zfill(2)}:{str(ss).zfill(2)}'

        listener = Listener(on_press=on_press, on_release=on_release)
        listener.start()
        global start
        start = time.time()  # 시작부터 첫키가 눌리기까지 시간

        # recordThreadStopper가 True가 되면 정지
        while True:
            if recordThreadStopper:
                listener.stop()
                onelinewrite(filename,'t'+ hms(round(totaltime))) # 총 소요시간 적기
                break
            time.sleep(0.1)

        listener.join()
        # listener가 끝나면 혹시 모른 상황에 대비해 lock 끄기
        if getLockState(VK_Capital):
            switchLocks(VK_Capital)
        if getLockState(VK_ScrollLock):
            switchLocks(VK_ScrollLock)
        
        self.is_idle = True
        self.parent.status.setText('대기중...')
        return


class locksListener(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        while True:
            if getLockState and self.parent.is_idle:
                pass




class MyThread(QThread):
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

        # locks 끄기
        if getLockState(VK_Capital):
            switchLocks(VK_Capital)
        if getLockState(VK_ScrollLock):
            switchLocks(VK_ScrollLock)

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
        self.is_idle = False

        # AlwaysOnTop
        self.AlwaysOnTop: QCheckBox
        self.AlwaysOnTop.stateChanged.connect(self.AOT)

        # DD 로드하기
        self.DD = windll.LoadLibrary(f"{thisdirpath}/DDHID64.dll")

    def Record(self):
        global recordThreadStopper
        recordThreadStopper = False
        self.recordThread.start()

    def StopSave(self):
        global recordThreadStopper
        recordThreadStopper = True

    def Load(self):
        self.is_idle = False
        self.filepath_str = QFileDialog.getOpenFileName(
            None, '파일을 선택하세요.', os.getenv('HOME'), '텍스트 파일(*.txt)')[0]
        self.filepath.setText(self.filepath_str)
        self.is_idle = True

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
