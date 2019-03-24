# -*- coding: utf-8 -*-

import cv2

import numpy as np

import os

import shutil


class MyDivide:
    imgName = ''
    imgPath = './position/'
    dividePath = './divide/'

    img = []       #读入的图片
    gray = []      #灰度图
    binary = []    #二值图
    data = []      #图片转换成array
    len_x = 0      #data的高度
    len_y = 0      #data的宽度
    rowPairs = []  #行分割后的结果

    min_val = 10  #最小字符高度，防止切分噪音
    dsize_x = 16  #分割后的图像高度
    dsize_y = 16  #分割后图像宽度

    def __init__(self, name):
        self.imgName = name
        self.dividePath = self.dividePath+name.split('-', 1)[0]+'/'
        self.img = cv2.imread(self.imgPath + self.imgName)

        x = self.img.shape[0]
        y = self.img.shape[1]
        rowPairs = []
        # 对于太小的图片进行放大
        if x < 360:
            self.img = cv2.resize(self.img, (360,360*x//y))
        elif y < 360:
            self.img = cv2.resize(self.img, (360*y//x,360))

    def Bgr2Gray(self):
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        return self.gray

    def Gray2Binary(self):
        GrayImageF1, self.binary = cv2.threshold(self.gray, 127, 255, cv2.THRESH_BINARY_INV)
        return self.binary

    def Binary2Array(self):
        self.data = np.array(self.binary)
        self.len_x = self.data.shape[0]
        self.len_y = self.data.shape[1]
    
    def lineSeg(self):
        start_i = -1
        end_i = -1
        def Judge(linedata, length):
            x = (linedata.sum() / 255) / length
            return x < 0.8 and x > 0.2
        
        for i in range(self.len_x):
            if (Judge(self.data[i], self.len_y) and start_i < 0):
                start_i = i
            elif (Judge(self.data[i], self.len_y)):
                end_i = i
            elif (not Judge(self.data[i], self.len_y) and start_i >= 0):
                if (end_i - start_i >= self.min_val):
                    self.rowPairs.append((start_i, end_i))
                start_i = -1
                end_i = -1
    
    def columnSeg(self):
        if os.path.exists(self.dividePath):
            shutil.rmtree(self.dividePath)
        os.mkdir(self.dividePath)
        start_j = -1
        end_j = -1
        min_val = 5
        num = 0
        for start, end in self.rowPairs:
            for j in range(self.len_y):
                if (not self.data[start:end, j].all() and start_j < 0):
                    start_j = j
                elif (not self.data[start:end, j].all()):
                    end_j = j
                elif (self.data[start:end, j].all() and start_j >= 0):
                    if (end_j - start_j >= min_val):
                        tmp = self.data[start:end, start_j:end_j]
                        tmp = cv2.copyMakeBorder(tmp, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255,255,255])
                        tmp = cv2.resize(tmp, (self.dsize_x, self.dsize_y))
                        cv2.imwrite(self.dividePath + '%d.png' % num, tmp)
                        num += 1
                    start_j = -1
                    end_j = -1
        return num
                        
        
if __name__ == '__main__':
    divide = MyDivide('f4-pos.png')
    divide.Bgr2Gray()
    divide.Gray2Binary()
    divide.Binary2Array()
    divide.lineSeg()
    print(divide.rowPairs)
    print('分割成了',divide.columnSeg(),'张图片')
    cv2.imshow('g',divide.binary)
    cv2.waitKey(0)




