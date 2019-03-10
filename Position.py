# encoding:utf-8

import cv2

import math

import numpy as np

from scipy import misc, ndimage

import matplotlib.pyplot as plt

class MyPosition:
    imgName = ''
    positionPath = './position/'
    positionName = ''

    img = []  #
    gray = []  #
    gaussian = []
    median = []
    sobel = []
    binary = []
    dilation = []
    dilation2 = []
    erosion = []
    closed = []
    result = []

    len_x = 0 #
    len_y = 0 #

    def __init__(self,name):
        self.img = cv2.imread(name)
        self.positionName = (name.split('.')[-2]).split('/')[-1] + '-pos.png'
        self.len_x = self.img.shape[0]
        self.len_y = self.img.shape[1]

    def RemoveNoise(self, img):
        self.img = img
        # 灰度化处理
        self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 高斯平滑 去噪声
        self.gaussian = cv2.GaussianBlur(self.gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
        # 中值滤波
        self.median = cv2.medianBlur(self.gaussian, 5)
        # Sobel算子 XY方向求梯度
        x = cv2.Sobel(self.median, cv2.CV_32F, 1, 0, ksize = 3)  # X方向
        y = cv2.Sobel(self.median, cv2.CV_32F, 0, 1, ksize = 3)  # Y方向
        gradient = cv2.subtract(x, y)
        self.sobel = cv2.convertScaleAbs(gradient)
        # 二值化
        blurred = cv2.GaussianBlur(self.sobel, (9, 9), 0)  # 再进行一次高斯去噪
        ret, self.binary = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
        # 膨胀和腐蚀操作的核函数
        element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
        element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))
        # 第一次膨胀
        self.dilation = cv2.dilate(self.binary, element2, iterations = 1)
        # 腐蚀
        self.erosion = cv2.erode(self.dilation, element1, iterations = 1)
        # 第二次膨胀
        self.dilation2 = cv2.dilate(self.erosion, element2, iterations=3)
        # 建立一个椭圆核函数
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
        # 执行图像形态学, 细节直接查文档，很简单
        self.closed = cv2.morphologyEx(self.binary, cv2.MORPH_CLOSE, kernel)
        self.closed = cv2.erode(self.closed, None, iterations=4)
        self.closed = cv2.dilate(self.closed, None, iterations=4)

    def getDetails(self):
        if self.closed.shape[:2] != self.img.shape[:2]:
            print("没有处理完成",self.closed.shape,self.img.shape)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        titles = [u"原图(BGR格式)", '灰度图', '高斯降噪',
                '中值滤波','边缘检测', '二值化',
                '第一次膨胀','腐蚀', '第二次膨胀']
        images = [self.img, self.gray, self.gaussian,
                self.median, self.sobel, self.binary,
                self.dilation, self.erosion, self.closed]
        for i in range(9):
            plt.subplot(3 ,3 , i +1) ,plt.imshow(images[i] ,'gray')
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])
        plt.show()


    def getProfile(self):
        (cnts, _) = cv2.findContours(self.closed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        rect = cv2.minAreaRect(c)
        Box = np.int0(cv2.boxPoints(rect))
        Final_img = cv2.drawContours(self.img.copy(), [Box], -1, (0, 0, 255), 3)
        # cv2.imshow('f',Final_img)
        up = max(min(Box[i][1] for i in range(4)),0)
        down = min(max(Box[i][1] for i in range(4)),self.len_x)
        left = max(min(Box[i][0] for i in range(4)),0)
        right = min(max(Box[i][0] for i in range(4)),self.len_y)
        myimg = self.img[up:down,left:right]
        self.result = myimg
        return myimg

    def Rotate(self):
        gray = cv2.cvtColor(self.result, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        # 霍夫变换
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 0)
        rotate_angle = 0
        for rho, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            if x1 == x2 or y1 == y2:
                continue
            t = float(y2 - y1) / (x2 - x1)
            rotate_angle = math.degrees(math.atan(t))
            if rotate_angle > 45:
                rotate_angle = -90 + rotate_angle
            elif rotate_angle < -45:
                rotate_angle = 90 + rotate_angle
        # rotate_img = ndimage.rotate(self.result, rotate_angle,mode='constant',cval = 255.0)
        rotate_img = ndimage.rotate(self.result, rotate_angle, mode='nearest')
        self.img = rotate_img
        return rotate_img

    def save(self):
        cv2.imwrite(self.positionPath+self.positionName,self.img)

if __name__ == '__main__':
    pos = MyPosition('./origin/d1.jpg')
    pos.RemoveNoise(pos.img)
    img = pos.getProfile()
    pos.getDetails()
    cv2.imshow('img1', img)
    cv2.waitKey(0)
    img = pos.Rotate()
    pos.RemoveNoise(img)
    img = pos.getProfile()
    pos.getDetails()
    cv2.imshow('img2', img)
    pos.save()
    cv2.waitKey(0)
        



    