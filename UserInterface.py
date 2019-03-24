# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UserInterface.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_LRP(object):
    def setupUi(self, LRP):
        LRP.setObjectName("LRP")
        LRP.resize(1461, 777)
        self.centralwidget = QtWidgets.QWidget(LRP)
        self.centralwidget.setObjectName("centralwidget")
        self.LoadImg = QtWidgets.QPushButton(self.centralwidget)
        self.LoadImg.setGeometry(QtCore.QRect(1310, 20, 121, 41))
        self.LoadImg.setObjectName("LoadImg")
        self.directReconize = QtWidgets.QPushButton(self.centralwidget)
        self.directReconize.setGeometry(QtCore.QRect(200, 700, 121, 41))
        self.directReconize.setObjectName("directReconize")
        self.nextStep = QtWidgets.QPushButton(self.centralwidget)
        self.nextStep.setGeometry(QtCore.QRect(620, 700, 121, 41))
        self.nextStep.setObjectName("nextStep")
        self.showDetail = QtWidgets.QPushButton(self.centralwidget)
        self.showDetail.setGeometry(QtCore.QRect(800, 700, 121, 41))
        self.showDetail.setObjectName("showDetail")
        self.Path = QtWidgets.QComboBox(self.centralwidget)
        self.Path.setGeometry(QtCore.QRect(20, 20, 1281, 41))
        self.Path.setObjectName("Path")
        self.currentImg = QtWidgets.QGraphicsView(self.centralwidget)
        self.currentImg.setGeometry(QtCore.QRect(550, 100, 501, 581))
        self.currentImg.setObjectName("currentImg")
        self.message = QtWidgets.QTextBrowser(self.centralwidget)
        self.message.setGeometry(QtCore.QRect(1070, 280, 371, 461))
        self.message.setObjectName("message")
        self.originImg = QtWidgets.QGraphicsView(self.centralwidget)
        self.originImg.setGeometry(QtCore.QRect(20, 100, 501, 581))
        self.originImg.setObjectName("originImg")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 70, 111, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(550, 70, 111, 31))
        self.label_2.setObjectName("label_2")
        self.result = QtWidgets.QTextBrowser(self.centralwidget)
        self.result.setGeometry(QtCore.QRect(1070, 100, 371, 131))
        self.result.setObjectName("result")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1070, 70, 81, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(1070, 240, 111, 41))
        self.label_4.setObjectName("label_4")
        self.directReconize.raise_()
        self.nextStep.raise_()
        self.showDetail.raise_()
        self.Path.raise_()
        self.currentImg.raise_()
        self.message.raise_()
        self.originImg.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.result.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.LoadImg.raise_()
        LRP.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LRP)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1461, 18))
        self.menubar.setObjectName("menubar")
        LRP.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LRP)
        self.statusbar.setObjectName("statusbar")
        LRP.setStatusBar(self.statusbar)

        self.retranslateUi(LRP)
        self.LoadImg.clicked.connect(self.myLoadImg)
        self.directReconize.clicked.connect(self.myDirectReconize)
        self.nextStep.clicked.connect(self.myNextStep)
        self.showDetail.clicked.connect(self.myShowDetail)
        QtCore.QMetaObject.connectSlotsByName(LRP)

    def retranslateUi(self, LRP):
        _translate = QtCore.QCoreApplication.translate
        LRP.setWindowTitle(_translate("LRP", "上海市电动车牌识别"))
        self.LoadImg.setText(_translate("LRP", "载入图片"))
        self.directReconize.setText(_translate("LRP", "一键识别"))
        self.nextStep.setText(_translate("LRP", "初步定位"))
        self.showDetail.setText(_translate("LRP", "展示细节"))
        self.label.setText(_translate("LRP", "原始图片"))
        self.label_2.setText(_translate("LRP", "当前图片"))
        self.label_3.setText(_translate("LRP", "识别结果"))
        self.label_4.setText(_translate("LRP", "日志"))
        self.pos = None
        self.devide = None
        self.mp = None