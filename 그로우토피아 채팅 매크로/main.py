import os
###################
import sys
import time
import winsound
import keyboard
import msvcrt as m

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pynput import keyboard
import pyautogui


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path("test.ui")
form_class = uic.loadUiType(form)[0]
app = QApplication
inputtext = ''


class Worker(QThread):
    finished = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        while True:
            if self.parent.is_playing:
                pyautogui.press('enter')
                pyautogui.write(self.parent.inputtext)
                pyautogui.press('enter')
                time.sleep(float(self.parent.second))
            else:
                return


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
        self.setFixedSize(267, 221)
        self.setWindowTitle("그로우토피아 채팅 매크로")
        self.setupUi(self)
        self.show()

        self.is_playing = False

        # 리스너
        self.worker = MyThread()
        self.worker.finished.connect(self.gotF5)
        self.worker.start()

        # 워커
        self.mainworker = Worker(self)

        # 초 입력
        self.secondEdit.setText("0.1")
        self.secondEdit: QLineEdit

        # 시작 버튼 연결
        self.startBtn.clicked.connect(self.runbuttonClicked)
        self.startBtn: QPushButton

        # 중지 버튼 연결
        self.stopBtn.clicked.connect(self.runbuttonClicked)
        self.stopBtn: QPushButton

        # 텍스트 박스 연결
        self.textEdit: QTextEdit

    def runbuttonClicked(self):
        self.inputtext = self.textEdit.toPlainText()
        self.second = self.secondEdit.text()
        if self.second == '':
            return

        self.is_playing = not self.is_playing

        if self.is_playing:
            self.startBtn.setEnabled(False)
            self.stopBtn.setEnabled(True)
        else:
            self.startBtn.setEnabled(True)
            self.stopBtn.setEnabled(False)

        if self.is_playing:
            self.mainworker.start()
            self.textEdit.setEnabled(False)
            self.secondEdit.setEnabled(False)
        else:
            self.textEdit.setEnabled(True)
            self.secondEdit.setEnabled(True)

    @pyqtSlot()
    def gotF5(self):
        self.worker.start()
        self.runbuttonClicked()


if __name__ == "__main__":
    app = app(sys.argv)
    window = MyWindow()
    app.exec_()
