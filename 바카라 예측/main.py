import os
###################
import sys
import time
import winsound
import keyboard
import msvcrt as m
import random

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pynput import keyboard
import resource_rc


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path("test.ui")
form_class = uic.loadUiType(form)[0]
app = QApplication
imgB = '<html><head/><body><p><img src=":/newPrefix/B.png"/></p></body></html>'
imgP = '<html><head/><body><p><img src=":/newPrefix/P.png"/></p></body></html>'


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setFixedSize(460, 430)
        self.setWindowTitle("Baccarat")
        self.setupUi(self)
        self.labellist = []

        for i in range(100):
            self.label = QLabel(imgB, self)
            self.label.setPixmap(QPixmap('P.png'))
            self.labellist.append(self.label)

        self.label_2: QLabel

        self.addB: QPushButton
        self.addB.clicked.connect(self.Bclick)

        self.addP: QPushButton
        self.addP.clicked.connect(self.Pclick)

        self.widget = QWidget()

        self.scrollArea: QScrollArea
        self.scrollArea.setWidget(self.widget)

        self.show()

    def Bclick(self):
        object = QLabel(imgB, self)
        object.setPixmap(QPixmap('P.png'))
        self.labellist.append(object)
        i = random.randint(0, 99)
        self.labellist[i].move(i, i)

    def Pclick(self):
        self.label_2.setText(
            '<html><head/><body><p><img src=":/newPrefix/P.png"/></p></body></html>')


if __name__ == "__main__":
    app = app(sys.argv)
    window = MyWindow()
    app.exec_()
