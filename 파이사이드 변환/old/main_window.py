# -*- coding: UTF-8 -*-
# ========== 라이브 러리 (모듈 설정) =================================================== #
# -*- coding: UTF-8 -*-
#%%
import os
import sys
from datetime import datetime as dt
import numpy as np
import PySide6.QtUiTools
import matplotlib.pyplot as plt
import pandas as pd
# from PyQt5.QtCore import QTimer
# from PyQt5.QtWidgets import *
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from pred_model import * 

# ========== 라이브 러리2 (모듈 설정) ================================================= #
#from model import ModelWidget

# ========== 기본 상태 설정 =========================================================== #
GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True
globalKeepAlive = True


# ========== UI 세팅 설정 ============================================================= #
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path("test.ui") 
print(form)
form_class = PySide6.QtUiTools.loadUiType(form)[0]

form2 = resource_path("test2.ui")
form_class2 = PySide6.QtUiTools.loadUiType(form2)[0]

# ========== 메인 윈도우 생성 ========================================================= #
class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # MainWindow 기본설정
        self.sheet_setup()
        # DataFrame 기본선언
        self.df = pd.DataFrame
        dialog_frm = pd.DataFrame
        # Excel Data import
        self.btn_excelimport.clicked.connect(self.data_get)
        # 타이머 설정
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.time_set)
        # ComboBox 리스트 활성화 작업
        self.heads_list = [
            "★★선택★★",
            "히팅시스템 (Zone#1)",
            "히팅시스템 (Zone#2)",
            "히팅시스템 (Zone#3)",
            "히팅시스템 (Zone#4)",
            "히팅시스템 (Zone#5)",
            "히팅시스템 (Zone#6)",
            "히팅시스템 (Zone#7)",
            "히팅시스템 (Zone#8)",
            "히팅시스템 (Zone#9)",
            "히팅시스템 (Zone#10)",
            "공조팬 (Zone#1)",
            "공조팬 (Zone#2)",
            "공조팬 (Zone#3)",
            "공조팬 (Zone#4)",
            "공조팬 (Zone#5)",
            "공조팬 (Zone#6)",
            "공조팬 (Zone#7)",
            "공조팬 (Zone#8)",
            "공조팬 (Zone#9)",
            "공조팬 (Zone#10)",
            "컨베이어벨트",
        ]
        self.cb_choice.addItems(self.heads_list)
        self.cb_choice.activated.connect(self.send_command)
        # 데이터 실행하기
        self.btn_model.clicked.connect(self.ui_model)

    # ========== 셋업 기본 설정 ====================================================== #
    def sheet_setup(self):
        # 윈도우 타이틀 제목 설정
        self.setWindowTitle("AI 상태진단 플랫폼")
        # 윈도우 창 크기 설정
        self.setGeometry(300, 100, 1600, 1000)
        self.statusBar().showMessage("AI 상태진단 플랫폼 정상 작동중..")

    # ========== dialog 로 데이터받기 ====================================================== #
    def data_get(self):
        global traindata_path
        dialog_frm = QFileDialog.getOpenFileName(self)
        try:
            if dialog_frm[0]:
                traindata_path=dialog_frm[0]
                self.df = pd.read_csv(dialog_frm[0]) #savefile dataframe
                return self.df

        except Exception as e:
            print(e)

    def ui_model(self):
        global model_path, mse, mae, mape
        #file_path = self.file_path
        #_file = file_path.split('/')[-1] # modified 
        #_path = file_path.rstrip(_file) # modified 
        mse, mae, mape, model_path,\
            predict_output, real_predict_array = train11(traindata_path, combo_index) # modified
        self.model = ModelWidget()          
        self.model.metric_table.setItem(1,1,QTableWidgetItem(str(round(mae,2))))
        self.model.metric_table.setItem(2,1,QTableWidgetItem(str(round(mse,2))))
        self.model.metric_table.setItem(3,1,QTableWidgetItem(str(round(mape,2))))

        fig = plt.Figure()
        canvas = FigureCanvas(fig)
        self.model.graph_layout.addWidget(canvas)

        ax = fig.add_subplot(111)
        # ax.set_xlabel("TIME")
        ax.set_ylabel("Num. of data")
        if combo_index == 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9 or 10:
         ax.set_ylabel("Temparature")
        else:
         ax.set_ylabel("Vibration")
        ax.plot(predict_output, label="predict")
        ax.plot(real_predict_array, label="true")
        ax.set_title("Result of Predict")
        ax.legend(loc="upper right")
        canvas.draw()
        self.model.show()


# path = os.path.realpath(model_path)
# os.startfile(path)

    def time_set(self):
        cur_time = dt.strftime(dt.now(), "%y년 %m월 %d일 %H시 %M분 %S초")
        self.lbl_timer.setText(cur_time)

    # ========== combobox index 번호를 누르면 실행하기 ====================================================== #
    def send_command(self):
        global combo_index
        combo_index = self.cb_choice.currentIndex()

        emptydf = self.df
        cal_df = None
        if combo_index == 1:
            list_heating1 = [
                "TIME",
                "ITEM001",
                "ITEM002",
                "ITEM003",
                "ITEM004",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating1 = emptydf[list_heating1]
            cal_df = df_heating1.copy()
            lastr = df_heating1.shape[0]
            lastc = df_heating1.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating1)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating1.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            # x = df_heating1["TIME"]
            # y = df_heating1.drop(["TIME"], axis=1)
            # plt.figure(figsize=(20, 20), fontsize=15)
            # plt.title("Grahp")
            # plt.xlabel("Time")
            # plt.ylabel("Data")
            # self.plot_widget.plot(x, y)
            # self.plot_widget = pg.PlotWidget()
            # self.setCentralWidget(self.plot_widget)
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating1["TIME"]
            y = df_heating1[list_heating1[1]]
            # y = df_heating1.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 2:
            list_heating2 = [
                "TIME",
                "ITEM005",
                "ITEM006",
                "ITEM007",
                "ITEM008",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating2 = emptydf[list_heating2]
            cal_df = df_heating2.copy()
            lastr = df_heating2.shape[0]
            lastc = df_heating2.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating2)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating2.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating2["TIME"]
            y = df_heating2[list_heating2[1]]
            # y = df_heating2.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 3:
            list_heating3 = [
                "TIME",
                "ITEM009",
                "ITEM010",
                "ITEM011",
                "ITEM012",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating3 = emptydf[list_heating3]
            cal_df = df_heating3.copy()
            lastr = df_heating3.shape[0]
            lastc = df_heating3.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating3)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating3.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating3["TIME"]
            y = df_heating3[list_heating3[1]]
            # y = df_heating3.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 4:
            list_heating4 = [
                "TIME",
                "ITEM013",
                "ITEM014",
                "ITEM015",
                "ITEM016",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating4 = emptydf[list_heating4]
            cal_df = df_heating4.copy()
            lastr = df_heating4.shape[0]
            lastc = df_heating4.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating4)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating4.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating4["TIME"]
            y = df_heating4[list_heating4[1]]
            # y = df_heating4.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 5:
            list_heating5 = [
                "TIME",
                "ITEM017",
                "ITEM018",
                "ITEM019",
                "ITEM020",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating5 = emptydf[list_heating5]
            cal_df = df_heating5.copy()
            lastr = df_heating5.shape[0]
            lastc = df_heating5.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating5)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating5.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating5["TIME"]
            y = df_heating5[list_heating5[1]]
            # y = df_heating5.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 6:
            list_heating6 = [
                "TIME",
                "ITEM021",
                "ITEM022",
                "ITEM023",
                "ITEM024",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating6 = emptydf[list_heating6]
            cal_df = df_heating6.copy()
            lastr = df_heating6.shape[0]
            lastc = df_heating6.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating6)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating6.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating6["TIME"]
            y = df_heating6[list_heating6[1]]
            # y = df_heating6.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 7:
            list_heating7 = [
                "TIME",
                "ITEM025",
                "ITEM026",
                "ITEM027",
                "ITEM028",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating7 = emptydf[list_heating7]
            cal_df = df_heating7.copy()
            lastr = df_heating7.shape[0]
            lastc = df_heating7.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating7)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating7.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating7["TIME"]
            y = df_heating7[list_heating7[1]]
            # y = df_heating7.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 8:
            list_heating8 = [
                "TIME",
                "ITEM029",
                "ITEM030",
                "ITEM031",
                "ITEM032",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating8 = emptydf[list_heating8]
            cal_df = df_heating8.copy()
            lastr = df_heating8.shape[0]
            lastc = df_heating8.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating8)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating8.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating8["TIME"]
            y = df_heating8[list_heating8[1]]
            # y = df_heating8.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 9:
            list_heating9 = [
                "TIME",
                "ITEM033",
                "ITEM034",
                "ITEM035",
                "ITEM036",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating9 = emptydf[list_heating9]
            cal_df = df_heating9.copy()
            lastr = df_heating9.shape[0]
            lastc = df_heating9.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating9)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating9.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating9["TIME"]
            y = df_heating9[list_heating9[1]]
            # y = df_heating9.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 10:
            list_heating10 = [
                "TIME",
                "ITEM037",
                "ITEM038",
                "ITEM039",
                "ITEM040",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating10 = emptydf[list_heating10]
            cal_df = df_heating10.copy()
            lastr = df_heating10.shape[0]
            lastc = df_heating10.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating10)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating10.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating10["TIME"]
            y = df_heating10[list_heating10[1]]
            # y = df_heating10.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 11:
            list_heating11 = [
                "TIME",
                "ITEM041",
                "ITEM042",
                "ITEM043",
                "ITEM044",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating11 = emptydf[list_heating11]
            cal_df = df_heating11.copy()
            lastr = df_heating11.shape[0]
            lastc = df_heating11.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating11)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating11.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating11["TIME"]
            y = df_heating11[list_heating11[1]]
            # y = df_heating11.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 12:
            list_heating12 = [
                "TIME",
                "ITEM045",
                "ITEM046",
                "ITEM047",
                "ITEM048",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating12 = emptydf[list_heating12]
            cal_df = df_heating12.copy()
            lastr = df_heating12.shape[0]
            lastc = df_heating12.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating12)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating12.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating12["TIME"]
            y = df_heating12[list_heating12[1]]
            # y = df_heating12.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 13:
            list_heating13 = [
                "TIME",
                "ITEM049",
                "ITEM050",
                "ITEM051",
                "ITEM052",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating13 = emptydf[list_heating13]
            cal_df = df_heating13.copy()
            lastr = df_heating13.shape[0]
            lastc = df_heating13.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating13)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating13.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating13["TIME"]
            y = df_heating13[list_heating13[1]]
            # y = df_heating13.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 14:
            list_heating14 = [
                "TIME",
                "ITEM053",
                "ITEM054",
                "ITEM055",
                "ITEM056",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating14 = emptydf[list_heating14]
            cal_df = df_heating14.copy()
            lastr = df_heating14.shape[0]
            lastc = df_heating14.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating14)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating14.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating14["TIME"]
            y = df_heating14[list_heating14[1]]
            # y = df_heating14.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 15:
            list_heating15 = [
                "TIME",
                "ITEM057",
                "ITEM058",
                "ITEM059",
                "ITEM060",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating15 = emptydf[list_heating15]
            cal_df = df_heating15.copy()
            lastr = df_heating15.shape[0]
            lastc = df_heating15.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating15)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating15.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating15["TIME"]
            y = df_heating15[list_heating15[1]]
            # y = df_heating15.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 16:
            list_heating16 = [
                "TIME",
                "ITEM061",
                "ITEM062",
                "ITEM063",
                "ITEM064",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating16 = emptydf[list_heating16]
            cal_df = df_heating16.copy()
            lastr = df_heating16.shape[0]
            lastc = df_heating16.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating16)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating16.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating16["TIME"]
            y = df_heating16[list_heating16[1]]
            # y = df_heating16.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 17:
            list_heating17 = [
                "TIME",
                "ITEM065",
                "ITEM066",
                "ITEM067",
                "ITEM068",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating17 = emptydf[list_heating17]
            cal_df = df_heating17.copy()
            lastr = df_heating17.shape[0]
            lastc = df_heating17.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating17)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating17.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating17["TIME"]
            y = df_heating17[list_heating17[1]]
            # y = df_heating17.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 18:

            list_heating18 = [
                "TIME",
                "ITEM069",
                "ITEM070",
                "ITEM071",
                "ITEM072",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating18 = emptydf[list_heating18]
            cal_df = df_heating18.copy()
            lastr = df_heating18.shape[0]
            lastc = df_heating18.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating18)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating18.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating18["TIME"]
            y = df_heating18[list_heating18[1]]
            # y = df_heating18.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 19:
            list_heating19 = [
                "TIME",
                "ITEM073",
                "ITEM074",
                "ITEM075",
                "ITEM076",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating19 = emptydf[list_heating19]
            cal_df = df_heating19.copy()
            lastr = df_heating19.shape[0]
            lastc = df_heating19.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating19)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating19.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating19["TIME"]
            y = df_heating19[list_heating19[1]]
            # y = df_heating19.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 20:
            list_heating20 = [
                "TIME",
                "ITEM077",
                "ITEM078",
                "ITEM079",
                "ITEM080",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating20 = emptydf[list_heating20]
            cal_df = df_heating20.copy()
            lastr = df_heating20.shape[0]
            lastc = df_heating20.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating20)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating20.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating20["TIME"]
            y = df_heating20[list_heating20[1]]
            # y = df_heating20.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            # ax.legend()
            self.canvas.draw()

        elif combo_index == 21:
            list_heating21 = [
                "TIME",
                "ITEM081",
                "ITEM082",
                "ITEM083",
                "ITEM084",
                "ITEM093",
                "ITEM094",
                "ITEM095",
                "ITEM096",
                "ITEM097",
                "ITEM098",
                "ITEM099",
                "ITEM100",
            ]
            df_heating21 = emptydf[list_heating21]
            cal_df = df_heating21.copy()
            lastr = df_heating21.shape[0]
            lastc = df_heating21.shape[1]
            self.tb_data.clear()
            self.tb_data.setRowCount(lastr)
            self.tb_data.setColumnCount(lastc)
            self.tb_data.setHorizontalHeaderLabels(list_heating21)
            for i in range(0, lastr):
                for j in range(0, lastc):
                    self.tb_data.setItem(
                        i, j, QTableWidgetItem(str(df_heating21.iloc[i, j]))
                    )
            self.lbl_rowcounter.setText(str(lastr))
            self.fig = plt.Figure()
            self.canvas = FigureCanvas(self.fig)
            self.graph_vbox.addWidget(self.canvas)
            x = df_heating21["TIME"]
            y = df_heating21[list_heating21[1]]
            # y = df_heating21.drop(["TIME"], axis=1)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("TIME")
            ax.set_ylabel("DATA")
            ax.set_title("My graph")
            self.canvas.draw()

        #전력
        x_avg = 0
        x_max = 0
        x_min = 0
                #온도 ,진동
        y_avg1, y_avg2 = 0, 0
        y_max1, y_max2 = 0, 0
        y_min1, y_min2 = 0, 0

        x_avg_format = ""
        x_max_format = ""
        x_min_format = ""
        y_avg_format = ""
        y_max_format = ""
        y_min_format = ""

        x_avg = cal_df.iloc[:, -3].mean()
        x_max = cal_df.iloc[:,-2].max()
        x_min = cal_df.iloc[:,-1].min()            
                
        x_avg_format = str(round(x_avg,2))
        x_max_format = str(round(x_max,2))
        x_min_format = str(round(x_min,2))
        if combo_index >= 1:         
                #진동만
            y_avg2 = cal_df.iloc[:, 1].mean()
            y_max2 = cal_df.iloc[:, 2].max()
            y_min2 = cal_df.iloc[:, 3].min()
            y_avg_format = f"{round(y_avg2,2)}"
            y_max_format = f"{round(y_max2,2)}"
            y_min_format = f"{round(y_min2,2)}"
        
                #독립
        self.label_5.setText(x_avg_format)
        self.label_6.setText(x_max_format)
        self.label_7.setText(x_min_format)
                #종속
        self.label_11.setText(y_avg_format)
        self.label_13.setText(y_max_format)
        self.label_8.setText(y_min_format)                            
        self.Baseline_text.setText("2022-11-08 8:57" + "\n~\n" + "2022-11-14 23:59")

class ModelWidget(QWidget, form_class2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.df = pd.DataFrame
        # 타이머 설정
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.time_set)            

        self.result_path_btn.clicked.connect(self.file_open_handler1)        
        self.load_btn.clicked.connect(self.file_open_handler2)   

        self.metric_table.setSpan(0,0,1,2)
        self.metric_table.setSpan(4,0,1,2)

    def time_set(self):
        cur_time = dt.strftime(dt.now(), "%y년 %m월 %d일 %H시 %M분 %S초")
        self.Time.setText(cur_time)

    def file_open_handler1(self):
        global fname    
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')[0]        
        traindata_path=fname[0]
        #self.df = pd.read_csv(fname[0]) #savefile dataframe  
        
        _file = model_path.split('/')[-1] # modified 
        _path = model_path.rstrip(_file)
        Predict = predict(fname, _path)
        print("최종\n")
        print(Predict)

        self.metric_table.setItem(5,1,QTableWidgetItem(str(round(Predict,2))))

    def file_open_handler2(self):     
        _file = model_path.split('/')[-1] # modified 
        _path = model_path.rstrip(_file)           
        os.startfile(_path)
        


if __name__ == "__main__":
    global model_path
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())

# %%
