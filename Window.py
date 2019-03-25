# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QGraphicsScene,QScrollArea
from PyQt5.QtWidgets import QWidget,  QFileDialog, QMessageBox,QVBoxLayout,QLabel
from PyQt5.QtGui import QImage, QPixmap
from Divide import MyDivide
from Position import MyPosition
from Recognize import MyPredict
from DataBase import MyDataBase
import cv2
import time
import os
from UserInterface import Ui_LRP

# 显示一个带滚动条Scroll的弹窗
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



class MyWindow(QMainWindow, Ui_LRP):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

    # button-直接识别
    def myDirectReconize(self):
        # 直接识别，不输出中间结果
        if self.pos == None:
            return
        # 定位-倾斜矫正-定位
        self.nextStep.setText('初步定位')
        self.currentImg.close()
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
        if fileName == '':
            return 
        self.Path.addItem(fileName)
        self.Path.setCurrentText(fileName)
        self.showpic(fileName, False)
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
            y = '图片'+self.posImgName+'识别成功，预测结果为'+a+',概率为%0.2f%%\n'%(b*100)
            mydb = MyDataBase()
            y = y+'\n'+time.asctime(time.localtime(time.time()))+'\n' + mydb.myProcess(a,self.originImgName)

        self.message.append('\n' + time.asctime(time.localtime(time.time())) +'\n'+y)
        self.result.setStyleSheet("background-color: white;font-size:30px;color:blue;font:SimHei");
        self.result.clear()
        self.result.setText(x)

