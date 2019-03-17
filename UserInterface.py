# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UserInterface.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QGraphicsScene,QScrollArea
from PyQt5.QtWidgets import QWidget,  QFileDialog, QMessageBox,QVBoxLayout,QLabel
from PyQt5.QtGui import QImage, QPixmap
from Divide import MyDivide
from Position import MyPosition
from Recognize import MyPredict
import cv2
import time
import os


class ScrollMessageBox(QMessageBox):
   def __init__(self, l, *args, **kwargs):
      QMessageBox.__init__(self, *args, **kwargs)
      scroll = QScrollArea(self)
      scroll.setWidgetResizable(True)
      self.content = QWidget()
      scroll.setWidget(self.content)
      lay = QVBoxLayout(self.content)
      for item in l:
         lay.addWidget(QLabel(item, self))
      self.layout().addWidget(scroll, 0, 0, 20, self.layout().columnCount())
      self.setStyleSheet("QScrollArea{min-width:600 px; min-height: 400px}")


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

    # button-直接识别
    def myDirectReconize(self):
        # 直接识别，不输出中间结果
        if self.pos == None:
            return
        # 定位-倾斜矫正-定位
        self.message.append('\n'+time.asctime(time.localtime(time.time())) +'\n选择了“直接识别”，将不输出中间处理结果')
        self.doPosition1()
        self.doRotate()
        self.doPosition2()
        # 划分
        self.doDivide()
        # 识别
        self.doPredict()

    # button-下一步
    def myNextStep(self):
        if self.pos == None:
            return

        if self.nextStep.text() == '初步定位':
            self.doPosition1()
            cv2.imwrite('./tmp/tmp.png',self.pos.result)
            self.showpic('./tmp/tmp.png', True)
            self.nextStep.setText('倾斜校正')
            self.message.append('\n' + time.asctime(time.localtime(time.time())) + '\n初步定位完成')
            return

        if self.nextStep.text() == '倾斜校正':
            img = self.pos.Rotate()
            cv2.imwrite('./tmp/tmp.png',img)
            self.showpic('./tmp/tmp.png', True)
            self.nextStep.setText('再次定位')
            self.message.append('\n' + time.asctime(time.localtime(time.time())) + '\n倾斜校正完成')
            return

        if self.nextStep.text() == '再次定位':
            self.doPosition2()
            cv2.imwrite('./tmp/tmp.png', self.pos.result)
            self.showpic('./tmp/tmp.png',True)
            self.nextStep.setText('字符分割')
            self.message.append('\n' + time.asctime(time.localtime(time.time())) + '\n再次定位完成')
            return

        if self.nextStep.text() == '字符分割':
            self.doDivide()
            self.nextStep.setText('字符识别')
            self.message.append('\n' + time.asctime(time.localtime(time.time())) + '\n字符分割完成')
            return

        if self.nextStep.text() == '字符识别':
            self.doPredict()
            self.nextStep.setText('初步定位')
            self.message.append('\n' + time.asctime(time.localtime(time.time())) + '\n字符识别完成')
            return

    # button-展示细节
    def myShowDetail(self):
        if self.pos == None:
            return

        if self.nextStep.text() == '初步定位':
            if self.mp.msg == None:
                return
            result = ScrollMessageBox(self.mp.msg, None)
            result.exec_()


        if self.nextStep.text() == '倾斜校正':
            self.pos.getDetails()
            return

        if self.nextStep.text() == '再次定位':
            return

        if self.nextStep.text() == '字符分割':
            self.pos.getDetails()
            return

        if self.nextStep.text() == '字符识别':
            path = '\divide\\'+self.posImgName
            current_path = os.path.abspath(__file__)
            father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep)
            print(father_path+path)
            os.system('explorer.exe "%s"'%(father_path+path))
            return

    # 显示一张图片
    def showpic(self,fileName,isCurrent):
        img=QImage()
        QImage.load(img,fileName)
        if img.width() > self.originImg.width():
            img = img.scaled(self.originImg.width(), img.height()*self.originImg.width()/img.width())
        if img.height() > self.originImg.height():
            img = img.scaled(img.width() * self.originImg.height() / img.height(),self.originImg.height())
        scene = QGraphicsScene()  # 创建场景
        scene.addPixmap(QPixmap.fromImage(img))
        if isCurrent == True:
            self.currentImg.setScene(scene)  # 将场景添加至视图
            self.currentImg.show()
        else:
            self.originImg.setScene(scene)  # 将场景添加至视图
            self.originImg.show()

    # 载入图片
    def myLoadImg(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "选择文件", "./origin/", "picture (*.jpg)")
        self.Path.addItem(fileName)
        self.Path.setCurrentText(fileName)
        self.showpic(fileName,False)
        self.nextStep.setText('初步定位')
        self.imgInit(fileName)

    # 初始化定位、分割、识别对象
    def imgInit(self,fileName):
        # originImgName 为原始图片名
        self.originImgName = fileName
        # 此处获取定位后图片名，如 ./origin/f1.jpg -> f1
        self.posImgName = fileName.split('/')[-1]
        self.posImgName = self.posImgName.split('.')[0]
        # 定义 MyPosition 对象
        self.pos = MyPosition(fileName)
        self.message.setText(time.asctime(time.localtime(time.time())) + '\n载入图片' + fileName)

    # 定位1
    def doPosition1(self):
        self.pos.RemoveNoise(self.pos.img)
        self.pos.getProfile()

    # 定位2
    def doPosition2(self):
        self.pos.RemoveNoise(self.pos.img)
        self.pos.getProfile()
        self.pos.save()
        self.message.append('\n' + time.asctime(time.localtime(time.time())) +
                            '\n保存定位图片./position/' + self.posImgName + '-pos.png')

    # 倾斜矫正
    def doRotate(self):
        self.pos.Rotate()

    # 划分
    def doDivide(self):
        self.divide = MyDivide(self.posImgName + '-pos.png')
        self.divide.Bgr2Gray()
        self.divide.Gray2Binary()
        self.divide.Binary2Array()
        self.divide.lineSeg()
        x = self.divide.columnSeg()
        self.message.append('\n' + time.asctime(time.localtime(time.time())) +
                    '\n图片./position/'+self.posImgName+'-pos.png划分成了%d张图片，大小16*16，保存位置./Divide/'%x+self.posImgName)

     # 识别
    def doPredict(self):
        self.mp = MyPredict('./Divide/' + self.posImgName + '/')
        self.mp.operations()
        (a,b) = self.mp.getLicense()
        if len(a) < 7 :
            x = '识别失败,切分数量过少'
            y = '图片'+self.posImgName+'识别失败，切分数量过少，预测结果'+a+',概率为%0.2f%%'%(b*100)
        elif b < 0.65:
            x = a+'\n识别失败\n概率过低:%0.2f%%'%(b*100)
            y = '图片'+self.posImgName+'识别失败，概率过低，预测结果'+a+',概率为%0.2f%%'%(b*100)
        else:
            x = a+'\n识别成功\n概率:%0.2f%%'%(b*100)
            y = '图片'+self.posImgName+'识别成功，预测结果为'+a+',概率为%0.2f%%'%(b*100)

        self.message.append('\n' + time.asctime(time.localtime(time.time())) +'\n'+y)
        self.result.setStyleSheet("background-color: white;font-size:30px;color:blue;font:SimHei");
        self.result.clear()
        self.result.setText(x)
