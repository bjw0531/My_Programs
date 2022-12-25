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
import key
import debugpy


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
keydict = {
    "'!'": "'1'",
    "'@'": "'2'",
    "'#'": "'3'",
    "'$'": "'4'",
    "'%'": "'5'",
    "'^'": "'6'",
    "'&'": "'7'",
    "'*'": "'8'",
    "'('": "'9'",
    "')'": "'0'",
    "'_'": "'-'",
    "'+'": "'='",
    "'|'": "'\\'",
    '{': "'['",
    '}': "']'",
    ':': "';'",
    '\'"\'': "\"'\"",
    "'<'": "','",
    "'>'": "'.'",
    "'?'": "'/'"
}

# User32 불러오기
hllDll = WinDLL("User32.dll")

# 함수 선언
VK_Capital = 0x14
VK_ScrollLock = 0x91
start = 0
end = 0
onoff = {65409: True,
         65408: False,
         1: True,
         0: False}
donerun = False

classdd = ''


def LoadDD():
    global classdd
    classdd = windll.LoadLibrary(f"{thisdirpath}/DDHID64.dll")
    st = classdd.DD_btn(0)  # DD Initialize

    if st == 1:
        print("OK")
    else:
        print("Error")
        sys.exit(101)


def getLockState(Key):
    """
    Key:
    VK_Capital
    VK_ScrollLock
    """
    return onoff[hllDll.GetKeyState(Key)]


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

        def onelinewrite(path, text):
            f = open(filename, 'a')
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
                onelinewrite(filename, 't' +
                             hms(round(totaltime)))  # 총 소요시간 적기
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


class capslockListener(QThread):
    capsdetected = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        def on_release(key):
            if key == Key.caps_lock:
                print(getLockState(VK_Capital))
                self.capsdetected.emit(getLockState(VK_Capital))

        self.listener = Listener(on_release=on_release)
        self.listener.daemon = True
        self.listener.start()
        self.running = True

    def quit(self):
        self.running = False
        self.listener.stop()


class scrlockListener(QThread):
    scrldetected = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        def on_release(key):
            if key == Key.scroll_lock:
                print(getLockState(VK_ScrollLock))
                self.scrldetected.emit(getLockState(VK_ScrollLock))

        listener = Listener(on_release=on_release)
        listener.daemon = True
        listener.start()
        self.running = True

    def quit(self):
        self.running = False
        self.listener.stop()


class runThread(QThread):
    # debugpy.debug_this_thread()
    done = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        self.set = set()
        self.parent.status.setText('실행중...')
        self.parent.is_idle = False

        self.f = open(self.parent.filepath_str, 'r')
        self.line = None
        while True:
            self.line = self.f.readline()
            if self.line == '':
                break

            self.value = self.line[1:-1]

            if self.line[0] == 'p':
                try:
                    self.tmp = key.keydict[self.value]
                    if self.tmp not in self.set:
                        self.set.add(self.tmp)
                        print(f'press {self.set}')
                        classdd.DD_key(self.tmp, 1)

                except Exception as e:
                    print(f'Error : {e}')
                    raise

            elif self.line[0] == 'r':
                try:
                    self.tmp = key.keydict[self.value]
                    if self.tmp in self.set:
                        self.set.remove(self.tmp)
                    print(f'release {self.tmp}')
                    classdd.DD_key(self.tmp, 2)
                    if not getLockState(VK_Capital):
                        for i in self.set:
                            classdd.DD_key(i, 2)
                        break
                    if getLockState(VK_ScrollLock):
                        self.parent.status.setText('일시정지...')

                        for i in self.set:
                            classdd.DD_key(i, 2)

                        while True:
                            if not getLockState(VK_ScrollLock):
                                self.parent.status.setText('실행중...')
                                break
                            time.sleep(0.1)

                except Exception as e:
                    print(f'Error : {e}')
                    raise

            elif self.line[0] == 'w':
                print(f'wait {self.value}')
                time.sleep(float(self.value))

        self.f.close()

        self.parent.status.setText('대기중...')
        self.parent.is_idle = True

        if getLockState(VK_Capital):
            switchLocks(VK_Capital)

        self.done.emit(True)


class errorThread(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        self.parent.is_idle = False
        self.parent.status.setText('오류!')
        time.sleep(1)
        self.parent.status.setText('대기중...')
        self.parent.is_idle = True


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

        # 소요시간 라벨
        self.timeLabel: QLabel
        self.timeLabel.setText("00시간 00분 00초")
        self.filetime = ''

        # 상태 라벨
        self.status: QLabel
        self.is_idle = True

        # AlwaysOnTop
        self.AlwaysOnTop: QCheckBox
        self.AlwaysOnTop.stateChanged.connect(self.AOT)

        # DD 로드하기
        LoadDD()
        time.sleep(0.2)
        classdd.DD_key(605, 1)
        classdd.DD_key(605, 2)

        # lock listener 쓰기
        self.capslocklistener = capslockListener(self)
        self.capslocklistener.start()
        self.capslocklistener.capsdetected.connect(self.capsDetected)

        self.scrlocklistener = scrlockListener(self)
        self.scrlocklistener.start()

        self.runthread = runThread(self)
        self.runthread.done.connect(self.donerunning)

        self.error = errorThread(self)
        # 파일 불러오기
        try:
            with open('config', 'r', encoding='EUC-KR') as f:
                line = f.readline()
                if 'txt' in line:
                    self.filepath_str = line
                    self.filepath.setText(self.filepath_str)

                with open(self.filepath_str, 'rb') as f:
                    try:
                        f.seek(-2, os.SEEK_END)
                        while f.read(1) != b'\n':
                            f.seek(-2, os.SEEK_CUR)
                    except OSError:
                        f.seek(0)
                    self.filetime = f.readline().decode()[1:]

                try:
                    h, m, s = self.filetime.split(':')
                    self.timeLabel.setText(f'{h}시간 {m}분 {s}초')
                except:
                    self.error.start()
        except:
            pass

    def Record(self):
        if not self.is_idle:
            return

        global recordThreadStopper
        recordThreadStopper = False
        self.recordThread.start()
        self.capslocklistener.quit()

    def StopSave(self):
        global recordThreadStopper
        recordThreadStopper = True
        if not self.capslocklistener.running:
            self.capslocklistener.start()

    def Load(self):
        self.is_idle = False
        self.status.setText('로딩중...')
        try:
            self.filepath_str = QFileDialog.getOpenFileName(
                None, '파일을 선택하세요.', os.getenv('HOME'), '텍스트 파일(*.txt)')[0]
        except:
            self.error.start()
            pass

        # 파일이 정상적으로 불러와지지 않았으면 return
        if self.filepath_str == '':
            self.error.start()
            return

        self.filepath.setText(self.filepath_str)

        # 파일 맨 마지막줄 구하기
        with open(self.filepath_str, 'rb') as f:
            try:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            self.filetime = f.readline().decode()[1:]

        try:
            h, m, s = self.filetime.split(':')
            self.timeLabel.setText(f'{h}시간 {m}분 {s}초')
        except:
            self.error.start()

        # config에 쓰기
        with open('config', 'w', encoding="EUC-KR") as f:
            f.write(self.filepath_str)

        self.is_idle = True
        self.status.setText('대기중...')

    def Delete(self):
        with open('config', 'w', encoding="EUC-KR") as f:
            pass

        self.filepath.setText('')
        self.filepath_str = None
        self.timeLabel.setText("00시간 00분 00초")
        time.sleep(1)
        classdd.DD_key(401, 1)
        classdd.DD_key(401, 2)

    def AOT(self):
        if self.AlwaysOnTop.isChecked():
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.show()
        else:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            self.show()

    @ pyqtSlot(bool)
    def capsDetected(self, value):
        if not self.filepath_str:
            return

        if self.is_idle and value:
            self.runthread.start()

    @ pyqtSlot(bool)
    def donerunning(self, value):
        if not self.capslocklistener.running:
            self.capslocklistener.start()


if __name__ == "__main__":
    app = app(sys.argv)
    global window
    window = MyWindow()
    app.exec_()
