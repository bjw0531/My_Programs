
# -*- coding: utf-8 -*-
################################################################################
# Form generated from reading UI file 'test.ui', 'test2.ui'
##
# Created by: Qt User Interface Compiler version 6.4.0
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

# %%
import csv
import os
from datetime import datetime as dt
import pandas as pd
import numpy as np
import PyInstaller
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


from pred import *
# %%


class Ui_MainWindow1(object):
    def setupUi(self, MainWindow1):
        MainWindow1.setObjectName("MainWindow1")
        MainWindow1.resize(1293, 1000)
        self.centralwidget = QWidget(MainWindow1)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.frame = QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")

        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.Total_layout = QHBoxLayout()
        self.Total_layout.setSizeConstraint(
            QLayout.SetDefaultConstraint)
        self.Total_layout.setObjectName("Total_layout")
        spacerItem = QSpacerItem(
            50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.Total_layout.addItem(spacerItem)
        self.Semitotal_layout = QVBoxLayout()
        self.Semitotal_layout.setSpacing(0)
        self.Semitotal_layout.setObjectName("Semitotal_layout")
        spacerItem1 = QSpacerItem(
            20, 16, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Semitotal_layout.addItem(spacerItem1)
        self.Title_layout = QHBoxLayout()
        self.Title_layout.setSpacing(0)
        self.Title_layout.setObjectName("Title_layout")
        self.Title = QLabel(self.frame)
        self.Title.setStyleSheet("background-color: rgb(200, 206, 206);\n"
                                 "font: 75 18pt \"에스코어 드림 6 Bold\";\n"
                                 "border-radius: 10px;\n"
                                 "border-width: 1px;\n"
                                 "border-color: rgb(0, 0, 0);\n"
                                 "border-style: solid;\n"
                                 "")
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.Title_layout.addWidget(self.Title)
        spacerItem2 = QSpacerItem(
            30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.Title_layout.addItem(spacerItem2)
        self.Time = QLabel(self.frame)
        self.Time.setStyleSheet("background-color: rgb(200, 206, 206);\n"
                                "font: 75 18pt \"에스코어 드림 6 Bold\";\n"
                                "border-radius: 10px;\n"
                                "border-width: 1px;\n"
                                "border-color: rgb(0, 0, 0);\n"
                                "border-style: solid;\n"
                                "")
        self.Time.setAlignment(QtCore.Qt.AlignCenter)
        self.Time.setObjectName("Time")
        self.Title_layout.addWidget(self.Time)
        self.Title_layout.setStretch(0, 710)
        self.Title_layout.setStretch(1, 50)
        self.Title_layout.setStretch(2, 410)
        self.Semitotal_layout.addLayout(self.Title_layout)
        spacerItem3 = QSpacerItem(
            20, 16, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Semitotal_layout.addItem(spacerItem3)
        self.Menu_layout = QHBoxLayout()
        self.Menu_layout.setSpacing(30)
        self.Menu_layout.setObjectName("Menu_layout")

        self.Excel_import = QPushButton(self.frame)
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Excel_import.sizePolicy().hasHeightForWidth())
        self.Excel_import.setSizePolicy(sizePolicy)
        self.Excel_import.setStyleSheet("background-color: rgb(238, 238, 238);\n"
                                        "font: 75 9pt \"에스코어 드림 6 Bold\";\n"
                                        "")
        self.Excel_import.setObjectName("Excel_import")
        self.Menu_layout.addWidget(self.Excel_import)
        spacerItem4 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.Menu_layout.addItem(spacerItem4)

        self.Baseline_text = QLabel(self.frame)
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Baseline_text.sizePolicy().hasHeightForWidth())
        self.Baseline_text.setSizePolicy(sizePolicy)

        #self.Baseline_text.setMinimumSize(QtCore.QSize(0, 60))
        self.Baseline_text.setStyleSheet("background-color: rgb(200, 206, 206);\n"
                                         "font: 75 9pt \"에스코어 드림 6 Bold\";\n"
                                         "border-radius: 10px;\n"
                                         "border-width:1px;\n"
                                         "border-style:solid;\n"
                                         "border-color: rgb(0, 0, 0);")
        self.Baseline_text.setWordWrap(True)
        self.Baseline_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Menu_layout.addWidget(self.Baseline_text)

        spacerItem_5 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.Menu_layout.addItem(spacerItem_5)

        self.Baseline_text2 = QLabel(self.frame)
        self.Baseline_text2.setMinimumSize(QtCore.QSize(0, 60))
        self.Baseline_text2.setStyleSheet("background-color: rgb(200, 206, 206);\n"
                                          "font: 75 9pt \"에스코어 드림 6 Bold\";\n"
                                          "border-radius: 10px;\n"
                                          "border-width:1px;\n"
                                          "border-style:solid;\n"
                                          "border-color: rgb(0, 0, 0);")
        self.Baseline_text2.setWordWrap(True)
        self.Baseline_text2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Menu_layout.addWidget(self.Baseline_text2)

        spacerItem5 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.Menu_layout.addItem(spacerItem5)
        self.variable_num = QLabel(self.frame)
        self.variable_num.setBaseSize(300, 80)
        self.variable_num.setStyleSheet("background-color: rgb(200, 206, 206);\n"
                                        "font: 75 9pt \"에스코어 드림 6 Bold\";\n"
                                        "border-radius: 10px;\n"
                                        "border-width:1px;\n"
                                        "border-style:solid;\n"
                                        "border-color: rgb(0, 0, 0);")
        self.variable_num.setAlignment(QtCore.Qt.AlignCenter)
        self.variable_num.setWordWrap(True)
        self.variable_num.setObjectName("variable_num")
        self.Menu_layout.addWidget(self.variable_num)

        spacerItem6 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.Menu_layout.addItem(spacerItem6)
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        spacerItem7 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.Menu_layout.addItem(spacerItem7)

        self.model_product = QPushButton(self.frame)
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.model_product.sizePolicy().hasHeightForWidth())
        self.model_product.setSizePolicy(sizePolicy)
        self.model_product.setStyleSheet("background-color: rgb(238, 238, 238);\n"
                                         "font: 75 9pt \"에스코어 드림 6 Bold\";\n"
                                         "")
        self.model_product.setObjectName("model_product")
        self.Menu_layout.addWidget(self.model_product)
        self.Menu_layout.setStretch(0, 300)
        self.Menu_layout.setStretch(1, 100)
        self.Menu_layout.setStretch(2, 300)
        self.Menu_layout.setStretch(3, 100)
        self.Menu_layout.setStretch(4, 300)
        self.Menu_layout.setStretch(5, 100)
        self.Menu_layout.setStretch(6, 300)
        self.Menu_layout.setStretch(7, 0)
        self.Menu_layout.setStretch(8, 0)
        self.Menu_layout.setStretch(9, 300)
        self.Semitotal_layout.addLayout(self.Menu_layout)
        spacerItem8 = QSpacerItem(
            20, 16, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Semitotal_layout.addItem(spacerItem8)
        self.Table = QTableWidget(self.frame)
        font = QtGui.QFont()
        font.setFamily("에스코어 드림 6 Bold")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(QtGui.QFont.ExtraLight)

        self.inner_hbox = QHBoxLayout()  # modified
        self.inner_hbox.setSpacing(0)  # modified

        self.inner_vbox = QVBoxLayout()
        self.inner_vbox.setSpacing(0)

        self.Table.setFont(font)
        self.Table.setStyleSheet("background-color: rgb(200, 206, 206);\n"
                                 "font: 75 12pt \"에스코어 드림 6 Bold\";")
        self.Table.setAlternatingRowColors(False)
        self.Table.setRowCount(0)
        self.Table.setObjectName("Table")
        self.Table.setColumnCount(0)
        self.Table.horizontalHeader().setVisible(True)
        self.Table.horizontalHeader().setCascadingSectionResizes(False)
        self.Table.horizontalHeader().setHighlightSections(True)
        self.Table.horizontalHeader().setStretchLastSection(False)
        self.Table.setFixedWidth(600)  # modified
        self.Table.setContentsMargins(0, 10, 0, 0)

        self.inner_hbox.addWidget(self.Table)  # modified

        self.inner_hbox.addLayout(self.inner_vbox)

        #############
        # modified
        self.lbl_picture_O = QLabel(self.frame)
        self.lbl_picture_O.setFixedHeight(400)
        self.lbl_picture_O.setFixedWidth(600)
        self.lbl_picture_O.setScaledContents(True)

        self.lbl_picture_V = QLabel(self.frame)
        self.lbl_picture_V.setFixedHeight(400)
        self.lbl_picture_V.setFixedWidth(600)
        self.lbl_picture_V.setScaledContents(True)

        self.Semitotal_layout.addLayout(self.inner_hbox)  # modified

        self.inner_vbox.addWidget(self.lbl_picture_O)  # modified
        self.inner_vbox.addWidget(self.lbl_picture_V)  # modified

        #############
        spacerItem9 = QSpacerItem(
            20, 16, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Semitotal_layout.addItem(spacerItem9)
        '''
        self.coefficient_table = QTableWidget(self.frame)
        self.coefficient_table.setStyleSheet("background-color: rgb(200, 206, 206);\n"
"font: 75 12pt \"에스코어 드림 6 Bold\";")
        self.coefficient_table.setRowCount(0)
        self.coefficient_table.setObjectName("coefficient_table")
        self.coefficient_table.setColumnCount(0)
        self.Semitotal_layout.addWidget(self.coefficient_table)
        
        spacerItem10 = QSpacerItem(20, 16, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Semitotal_layout.addItem(spacerItem10)
        '''
        self.Semitotal_layout.setStretch(0, 16)
        self.Semitotal_layout.setStretch(1, 60)
        self.Semitotal_layout.setStretch(2, 16)
        self.Semitotal_layout.setStretch(3, 61)
        self.Semitotal_layout.setStretch(4, 16)
        self.Semitotal_layout.setStretch(5, 500)
        self.Semitotal_layout.setStretch(6, 16)
        self.Semitotal_layout.setStretch(7, 100)
        self.Semitotal_layout.setStretch(8, 16)
        self.Total_layout.addLayout(self.Semitotal_layout)
        spacerItem11 = QSpacerItem(
            50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.Total_layout.addItem(spacerItem11)
        self.Total_layout.setStretch(0, 25)
        self.Total_layout.setStretch(1, 1230)
        self.Total_layout.setStretch(2, 25)
        self.gridLayout.addLayout(self.Total_layout, 0, 0, 1, 1)
        self.horizontalLayout_4.addWidget(self.frame)
        MainWindow1.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow1)

        self.file_path = None  # modified

    # 기능

    def retranslateUi(self, MainWindow1):
        _translate = QtCore.QCoreApplication.translate
        MainWindow1.setWindowTitle(_translate("MainWindow1", "MainWindow"))
        self.Title.setText(_translate("MainWindow1", "MCT 고장예측 플랫폼"))
        self.Time.setText(_translate("MainWindow1", "날짜, 현재시간"))
        self.Excel_import.setText(_translate("MainWindow1", "학습 데이터 입력"))
        self.Baseline_text.setText(_translate("MainWindow1", "베이스라인 기간"))
        self.Baseline_text2.setText(_translate("MainWindow1", "베이스라인 기간"))
        self.variable_num.setText(_translate("MainWindow1", "데이터 개수(#row) 표출"))
        self.model_product.setText(_translate("MainWindow1", "모델생성"))

        self.Excel_import.clicked.connect(self.handleOpen)
        self.model_product.clicked.connect(self.newWindow)

    def makeClock(self):
        cur_time = dt.strftime(dt.now(), "%y년 %m월 %d일 %H시 %M분 %S초")
        self.Time.setText(cur_time)

    def newWindow(self):
        global model_path, mse, mae, mape
        print(self.file_path)
        file_path = self.file_path
        _file = file_path.split('/')[-1]  # modified
        _path = file_path.rstrip(_file)  # modified

        mse, mae, mape, model_path = train(_path, _file)  # modified
        print(mse, mae, mape)

        MainWindow1.setVisible(False)  # modified

        MainWindow2.show()

    # modifield
    def loadImageFromFile(self):
        # QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        # _O = Output // _V = Vibration
        self.qPixmapFileVar_O = QtGui.QPixmap()
        self.qPixmapFileVar_O.load("raw_plot_O.jpg")
        self.qPixmapFileVar_O = self.qPixmapFileVar_O.scaledToWidth(200)
        self.qPixmapFileVar_V = QtGui.QPixmap()
        self.qPixmapFileVar_V.load("raw_plot_V.jpg")
        self.qPixmapFileVar_V = self.qPixmapFileVar_O.scaledToWidth(200)
        self.lbl_picture_O = QLabel(self.frame)
        self.lbl_picture_O.setPixmap(self.qPixmapFileVar_O)
        self.lbl_picture_O.resize(20, 20)
        self.lbl_picture_V = QLabel(self.frame)
        self.lbl_picture_V.setPixmap(self.qPixmapFileVar_V)
        self.lbl_picture_V.resize(20, 20)

        # self.qPixmapFileVar = QtGui.QPixmap()
        # self.qPixmapFileVar.load("raw_plot1.jpg")
        # self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(200)
        # self.lbl_picture = QLabel(self.frame)
        # self.lbl_picture.setPixmap(self.qPixmapFileVar)
        # self.lbl_picture.resize(20, 20)

    def handleOpen(self):
        filepath, ok = QFileDialog.getOpenFileName(
            None, 'CSV 데이터 파일을 선택하세요.', os.getenv('HOME'), 'CSV(*.csv)')
        self.file_path = filepath
        df = pd.read_csv(filepath)
        df_output = df[['TIME', 'Output']]
        df_vib = df[['TIME', 'Vibration']]

        fig_out = df_output.plot(xlabel="Num Of Data",
                                 ylabel="Remaining useful life").get_figure()
        fig_vib = df_vib.plot(xlabel="Num Of Data",
                              ylabel="Remaining useful life").get_figure()

        fig_out.savefig('raw_plot_O.jpg')
        fig_vib.savefig('raw_plot_V.jpg')

        countVal = 0
        countHead = 0
        startval = ''
        endval = ''
        if ok:
            self.Table.clear()
            with open(filepath) as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)
                hlist = list(header)
                countHead = len(header)
                self.Table.setColumnCount(len(header))
                self.Table.setHorizontalHeaderLabels(header)
                for row, values in enumerate(reader):
                    self.Table.insertRow(row)
                    countVal += 1
                    for column, value in enumerate(values):
                        try:
                            if column == 0 and row == 0:  # modified
                                startval = value

                            elif column == 0:  # modified
                                endval = value

                        except:
                            continue
                        self.Table.setItem(
                            row, column, QTableWidgetItem(value))

            qPixmapFileVar_O = QtGui.QPixmap()
            qPixmapFileVar_O.load("raw_plot_O.jpg")
            qPixmapFileVar_V = QtGui.QPixmap()
            qPixmapFileVar_V.load("raw_plot_V.jpg")
            '''
            lbl_picture = QLabel(self.frame)
            lbl_picture.setFixedHeight(32)
            lbl_picture.setFixedWidth(48)
            lbl_picture.setScaledContents(True)
            lbl_picture.setPixmap(qPixmapFileVar)
            '''
            self.lbl_picture_O.setPixmap(qPixmapFileVar_O)
            self.lbl_picture_V.setPixmap(qPixmapFileVar_V)

        # 전체 헤더 갯수에서 [기간] 빼기

        self.variable_num.setText(str(countVal))  # modified
        self.Baseline_text.setText(startval)
        self.Baseline_text2.setText(endval)
        # modified


class Ui_MainWindow2(object):

    def setupUi(self, MainWindow2):
        MainWindow2.setObjectName("MainWindow2")
        MainWindow2.resize(1293, 862)
        self.centralwidget = QWidget(MainWindow2)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: rgb(255,255,255);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.Total_Layout = QHBoxLayout()
        self.Total_Layout.setSpacing(0)
        self.Total_Layout.setObjectName("Total_Layout")
        spacerItem = QSpacerItem(
            50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.Total_Layout.addItem(spacerItem)
        self.Semitotal_Layout = QVBoxLayout()
        self.Semitotal_Layout.setSpacing(0)
        self.Semitotal_Layout.setObjectName("Semitotal_Layout")
        spacerItem1 = QSpacerItem(
            754, 13, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Semitotal_Layout.addItem(spacerItem1)
        self.Title_layout = QHBoxLayout()
        self.Title_layout.setSpacing(0)
        self.Title_layout.setObjectName("Title_layout")
        self.Title = QLabel(self.frame)
        self.Title.setStyleSheet("background-color: rgb(200, 206, 206);\n"
                                 "font: 75 18pt \"에스코어 드림 6 Bold\";\n"
                                 "border-radius: 10px;\n"
                                 "border-width: 1px;\n"
                                 "border-color: rgb(0, 0, 0);\n"
                                 "border-style: solid;\n"
                                 "")

        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.Title_layout.addWidget(self.Title)
        spacerItem2 = QSpacerItem(
            30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.Title_layout.addItem(spacerItem2)
        self.Time = QLabel(self.frame)
        self.Time.setStyleSheet("background-color: rgb(200, 206, 206);\n"
                                "font: 75 18pt \"에스코어 드림 6 Bold\";\n"
                                "border-radius: 10px;\n"
                                "border-width: 1px;\n"
                                "border-color: rgb(0, 0, 0);\n"
                                "border-style: solid;\n"
                                "")
        self.Time.setAlignment(QtCore.Qt.AlignCenter)
        self.Time.setObjectName("Time")
        self.Title_layout.addWidget(self.Time)
        self.Title_layout.setStretch(0, 710)
        self.Title_layout.setStretch(1, 50)
        self.Title_layout.setStretch(2, 410)
        self.Semitotal_Layout.addLayout(self.Title_layout)
        spacerItem3 = QSpacerItem(
            20, 16, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Semitotal_Layout.addItem(spacerItem3)
        spacerItem4 = QSpacerItem(
            754, 13, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Semitotal_Layout.addItem(spacerItem4)
        '''
        self.Graph = QWidget(self.frame)
        self.Graph.setMinimumSize(QtCore.QSize(0, 192))
        self.Graph.setStyleSheet("background-color: rgb(200, 206, 206);")
        self.Graph.setObjectName("Graph")
        '''
        # modifield
        self.Graph = QLabel(self.frame)
        self.Graph.setFixedHeight(500)
        self.Graph.setFixedWidth(1250)
        self.Graph.setScaledContents(True)

        self.Semitotal_Layout.addWidget(self.Graph)
        spacerItem5 = QSpacerItem(
            754, 13, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Semitotal_Layout.addItem(spacerItem5)
        self.Result_Layout = QHBoxLayout()
        self.Result_Layout.setSpacing(0)
        self.Result_Layout.setObjectName("Result_Layout")
        self.metric_table = QTableWidget(self.frame)
        self.metric_table.setStyleSheet(
            "background-color: rgb(200, 206, 206);")
        self.metric_table.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustIgnored)
        self.metric_table.setAutoScrollMargin(16)
        self.metric_table.setRowCount(6)
        self.metric_table.setColumnCount(2)
        self.metric_table.setObjectName("metric_table")
        item = QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.metric_table.setItem(0, 0, item)
        item = QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.metric_table.setItem(0, 1, item)
        item = QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.metric_table.setItem(1, 0, item)
        item = QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.metric_table.setItem(2, 0, item)
        item = QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.metric_table.setItem(3, 0, item)
        # modifield
        item = QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.metric_table.setItem(1, 1, item)
        item = QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.metric_table.setItem(2, 1, item)
        item = QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.metric_table.setItem(3, 1, item)

        item = QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.metric_table.setItem(4, 0, item)
        item = QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.metric_table.setItem(4, 1, item)  # modified

        item = QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.metric_table.setItem(5, 1, item)

        item = QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.metric_table.setItem(5, 0, item)
        self.metric_table.horizontalHeader().setVisible(False)
        self.metric_table.horizontalHeader().setCascadingSectionResizes(False)
        self.metric_table.horizontalHeader().setStretchLastSection(True)
        self.metric_table.verticalHeader().setVisible(False)
        self.metric_table.verticalHeader().setCascadingSectionResizes(False)
        self.metric_table.verticalHeader().setDefaultSectionSize(43)
        self.metric_table.verticalHeader().setSortIndicatorShown(False)
        self.metric_table.verticalHeader().setStretchLastSection(True)

        self.metric_table.setSpan(0, 0, 1, 2)
        self.metric_table.setSpan(4, 0, 1, 2)

        self.Result_Layout.addWidget(self.metric_table)
        spacerItem6 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.Result_Layout.addItem(spacerItem6)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.faule_result_btn = QPushButton(self.frame)  # modified

        font = QtGui.QFont()
        font.setFamily("에스코어 드림 6 Bold")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(QtGui.QFont.ExtraLight)
        self.faule_result_btn.setFont(font)
        self.faule_result_btn.setMinimumHeight(100)  # modified
        self.faule_result_btn.setStyleSheet("background-color: rgb(200, 206, 206);\n"
                                            "font: 75 18pt \"에스코어 드림 6 Bold\";\n"
                                            "border-radius: 10px;\n"
                                            "border-width: 1px;\n"
                                            "border-color: rgb(0, 0, 0);\n"
                                            "border-style: solid;\n"
                                            "")
        self.faule_result_btn.setObjectName("faule_result_btn")
        self.verticalLayout_2.addWidget(self.faule_result_btn)

        self.life_predict_btn = QPushButton(self.frame)  # modified
        self.life_predict_btn.setMinimumHeight(100)  # modified
        font = QtGui.QFont()
        font.setFamily("에스코어 드림 6 Bold")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(QtGui.QFont.ExtraLight)
        self.life_predict_btn.setFont(font)
        self.life_predict_btn.setStyleSheet("background-color: rgb(200, 206, 206);\n"
                                            "font: 75 18pt \"에스코어 드림 6 Bold\";\n"
                                            "border-radius: 10px;\n"
                                            "border-width: 1px;\n"
                                            "border-color: rgb(0, 0, 0);\n"
                                            "border-style: solid;\n"
                                            "")
        self.life_predict_btn.setObjectName("life_predict_btn")
        self.verticalLayout_2.addWidget(self.life_predict_btn)
        self.verticalLayout_2.setStretch(0, 50)
        self.verticalLayout_2.setStretch(1, 10)
        self.verticalLayout_2.setStretch(2, 50)
        self.Result_Layout.addLayout(self.verticalLayout_2)
        self.Result_Layout.setStretch(0, 140)
        self.Result_Layout.setStretch(1, 10)
        self.Result_Layout.setStretch(2, 50)
        self.Semitotal_Layout.addLayout(self.Result_Layout)
        spacerItem8 = QSpacerItem(
            754, 13, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Semitotal_Layout.addItem(spacerItem8)
        self.Semitotal_Layout.setStretch(0, 16)
        self.Semitotal_Layout.setStretch(1, 60)
        self.Semitotal_Layout.setStretch(2, 16)
        self.Semitotal_Layout.setStretch(3, 16)
        self.Semitotal_Layout.setStretch(4, 350)
        self.Semitotal_Layout.setStretch(5, 16)
        self.Semitotal_Layout.setStretch(6, 250)
        self.Semitotal_Layout.setStretch(7, 16)
        self.Total_Layout.addLayout(self.Semitotal_Layout)
        spacerItem9 = QSpacerItem(
            50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.Total_Layout.addItem(spacerItem9)
        self.Total_Layout.setStretch(0, 25)
        self.Total_Layout.setStretch(1, 1230)
        self.Total_Layout.setStretch(2, 25)
        self.gridLayout.addLayout(self.Total_Layout, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        MainWindow2.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow2)

        self.faule_result_btn.clicked.connect(self.getSavePath)  # modified
        self.life_predict_btn.clicked.connect(self.predDataLoad)  # modified

    # 수명예측?이 뭔지에 따라 추가 구현 필요
    # modified

    def predDataLoad(self):
        filepath = QFileDialog.getOpenFileName(
            None, 'CSV 데이터 파일을 선택하세요.', os.getenv('HOME'), 'CSV(*.csv)')
        print(filepath)

        global Pred
        Pred = predict(filepath[0], model_path)
        _translate = QtCore.QCoreApplication.translate
        item = self.metric_table.item(5, 1)
        item.setText(_translate("MainWindow2", str(round(Pred, 2))))
        print('PRED/n')
        print(Pred)
    # modified

    def getSavePath(self):
        global model_path, mse, mae, mape
        print(model_path)

        # 성능 metric 표시
        _translate = QtCore.QCoreApplication.translate
        item = self.metric_table.item(1, 1)
        item.setText(_translate("MainWindow2", str(round(mae, 2))))
        item = self.metric_table.item(2, 1)
        item.setText(_translate("MainWindow2", str(round(mse, 2))))
        item = self.metric_table.item(3, 1)
        item.setText(_translate("MainWindow2", str(round(mape, 2))))

        # 그래프 플롯
        qPixmapFileVar = QtGui.QPixmap()
        qPixmapFileVar.load(model_path + "예측결과plot")
        self.Graph.setPixmap(qPixmapFileVar)

        # 학습모델 저장 경로 오픈
        path = os.path.realpath(model_path)
        os.startfile(path)

    def retranslateUi(self, MainWindow2):

        _translate = QtCore.QCoreApplication.translate
        MainWindow2.setWindowTitle(_translate("MainWindow2", "MainWindow"))
        self.Title.setText(_translate("MainWindow2", "MCT 고장예측 플랫폼"))
        self.Time.setText(_translate("MainWindow2", "날짜, 현재시간"))
        __sortingEnabled = self.metric_table.isSortingEnabled()
        self.metric_table.setSortingEnabled(False)
        item = self.metric_table.item(0, 0)
        item.setText(_translate("MainWindow2", "예측 모델의 학습 정확도"))
        item = self.metric_table.item(1, 0)
        item.setText(_translate("MainWindow2", "MAE"))
        item = self.metric_table.item(2, 0)
        item.setText(_translate("MainWindow2", "MSE"))
        item = self.metric_table.item(3, 0)
        item.setText(_translate("MainWindow2", "MAPE"))
        item = self.metric_table.item(4, 0)
        item.setText(_translate("MainWindow2", "수명 예측 결과"))
        item = self.metric_table.item(5, 0)
        item.setText(_translate("MainWindow2", "남은 수명"))
        self.metric_table.setSortingEnabled(__sortingEnabled)
        self.faule_result_btn.setText(
            _translate("MainWindow2", "결과 보기"))  # modified
        self.life_predict_btn.setText(
            _translate("MainWindow2", "수명예측 데이터 Load"))

    def makeClock(self):
        cur_time = dt.strftime(dt.now(), "%y년 %m월 %d일 %H시 %M분 %S초")
        self.Time.setText(cur_time)


if __name__ == "__main__":
    import sys
    global model_path, mse, mae, mape
    model_path, mse, mae, mape = None, None,  None,  None

    app = QApplication(sys.argv)
    MainWindow1 = QMainWindow()
    MainWindow2 = QMainWindow()
    ui = Ui_MainWindow1()
    ui.setupUi(MainWindow1)
    ui2 = Ui_MainWindow2()
    ui2.setupUi(MainWindow2)

    timer = QtCore.QTimer()
    timer.timeout.connect(ui.makeClock)
    timer.timeout.connect(ui2.makeClock)
    timer.start(1000)
    MainWindow1.show()
    sys.exit(app.exec())


# %%
