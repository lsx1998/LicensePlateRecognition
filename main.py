from Divide import MyDivide

from Position import MyPosition

import cv2

if __name__=='__main__':
    for i in range(3,4):
        picName = './origin/f%s.jpg'%(i)
        originPath = './origin/'
        picName = picName.split('/')[-1]
        pos = MyPosition(originPath + picName)
        pos.RemoveNoise(pos.img)
        img = pos.getProfile()
        # pos.getDetails()
        # cv2.imshow('img1', img)
        # cv2.waitKey(0)
        img = pos.Rotate()
        pos.RemoveNoise(img)
        img = pos.getProfile()
        # pos.getDetails()
        # cv2.imshow('img2', img)
        # cv2.waitKey(0)
        pos.save()

        picName = picName.split('.')[0]

        divide = MyDivide(picName + '-pos.png')
        divide.Bgr2Gray()
        divide.Gray2Binary()
        divide.Binary2Array()
        divide.lineSeg()
        print(picName, '分割成了', divide.columnSeg(), '张图片')

    # picName = './origin/f10.jpg'
    # originPath = './origin/'
    # picName = picName.split('/')[-1]
    #
    # pos = MyPosition(originPath+picName)
    # pos.RemoveNoise(pos.img)
    # img = pos.getProfile()
    # #pos.getDetails()
    # #cv2.imshow('img1', img)
    # #cv2.waitKey(0)
    # img = pos.Rotate()
    # pos.RemoveNoise(img)
    # img = pos.getProfile()
    # # pos.getDetails()
    # # cv2.imshow('img2', img)
    # # cv2.waitKey(0)
    # pos.save()
    #
    #
    # picName = picName.split('.')[0]
    #
    # divide = MyDivide(picName+'-pos.png')
    # divide.Bgr2Gray()
    # divide.Gray2Binary()
    # divide.Binary2Array()
    # divide.lineSeg()
    # print(picName,'分割成了',divide.columnSeg(),'张图片')



