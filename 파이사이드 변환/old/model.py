# -*- coding: UTF-8 -*-#
# ========== 라이브 러리 (모듈 설정) ======================================================

#%%
import os
import sys
from PySide6.QtWidgets import *
import PySide6.QtUiTools
from PySide6.QtCore import QTimer
#from main_window import mae
from datetime import datetime as dt

# # ========== UI 세팅 설정 ================================================================ #
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path("test2.ui")
form_class = PySide6.QtUiTools.loadUiType(form)[0]


# ========== MainWidget ==================================================================== #
class ModelWidget(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # 타이머 설정
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.time_set)            

        self.result_path_btn.clicked.connect(self.file_open_handler1)        
        self.load_btn.clicked.connect(self.file_open_handler2)        

    def time_set(self):
        cur_time = dt.strftime(dt.now(), "%y년 %m월 %d일 %H시 %M분 %S초")
        self.Time.setText(cur_time)

    def file_open_handler1(self):                
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')[0]        
        if not fname:
            return

    def file_open_handler2(self):                
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')[0]        
        if not fname:
            return
if __name__ == "__main__":
    app = QApplication(sys.argv)
    hq = ModelWidget()
    hq.show()
    sys.exit(app.exec_())

# %%
