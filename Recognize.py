# # -*- coding: utf-8 -*-
import sys
import os
import time
import random
import numpy as np
import tensorflow as tf
from PIL import Image

IMGSIZE = 1280
WIDTH = 16
HEIGHT =16

NUMBERLIST = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")

NUMBER = 10

IMG_DIR = './digit_images/'
VAL_DIR = './digit_validation/'

SAV_DIR = './digit_save/'


class Mytf():
    # 定义图片数据的输入格式和标签的输入格式
    time_begin = 0
    img_input = tf.placeholder(tf.float32, shape = [None,IMGSIZE])
    lab_input = tf.placeholder(tf.float32, shape=[None, 10])
    
    # 将img_input修改为指定的形式
    sized_img = tf.reshape(img_input, [-1, WIDTH, HEIGHT, 1])

    keep_prob = tf.placeholder(tf.float32)
    # 卷积函数
    '''
    参数说明：
    inputs:输入图像
    w:过滤器，用于和原始图片卷积计算
    b:偏置项,与w组成g(x) = wx+b
    conv_strides: 步长
    kernel_size:池化窗口大小[1,height,width,1]
    pool_strides:池化层填充
    conv_padding:卷积层填充
    '''
    def convLayer(self, inputs, w, b, conv_strides, kernel_size, pool_strides, conv_padding):
        conv_output = tf.nn.conv2d(inputs, w, strides=conv_strides, padding=conv_padding)
        relu_output = tf.nn.relu(conv_output + b)
        pool_output = tf.nn.max_pool(relu_output, ksize=kernel_size, strides=pool_strides, padding='SAME')
        return pool_output
    
    # 全连接层
    '''
    参数说明：
    inputs:输入图像
    w:用于和输入图像进行矩阵乘法运算
    b:偏置项，g(x)=wx+b
    '''
    def fullConnectLayer(self, inputs, w, b):
        return tf.nn.relu(tf.matmul(inputs, w) + b)

    # 两层卷积运算
    def convOperate(self, w_conv1, b_conv1, w_conv2, b_conv2):
        # 第一层
        conv_strides = [1, 1, 1, 1]
        kernel_size = [1, 2, 2, 1]
        pool_strides = [1, 2, 2, 1]
        L1_pool = self.convLayer(self.sized_img, w_conv1, b_conv1, conv_strides, kernel_size, pool_strides, conv_padding='SAME')
        # 第二层
        kernel_size = [1, 1, 1, 1]
        pool_strides = [1, 1, 1, 1]
        return self.convLayer(L1_pool, w_conv2, b_conv2, conv_strides, kernel_size, pool_strides, conv_padding='SAME')
    
    # 全连接层运算
    def fullConnectOperate(self, L2_pool, w_fc1, b_fc1):
        h_pool2_flat = tf.reshape(L2_pool, [-1, 16 * 20 * 32])
        return self.fullConnectLayer(h_pool2_flat, w_fc1, b_fc1)
    
    # dropout层
    def dropOutLayer(self, h_fc1):
        return tf.nn.dropout(h_fc1, self.keep_prob)
        
    # 图像处理，使数字变细，作用类似于opencv中的
    # cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV)
    def imgHandle(self, old_img,new_img,val):
        width = old_img.size[0]
        height = old_img.size[1]
        for h in range(0, height):
            for w in range(0, width):
                if old_img.getpixel((w, h)) > val:
                    new_img[w + h * width] = 0
                else:
                    new_img[w + h * width] = 1

class MyTrain(Mytf):
    img_dir = IMG_DIR
    val_dir = VAL_DIR
    sav_dir = SAV_DIR

    input_count = 0
    val_count = 0

    input_images = [] #输入的图片数据
    input_labels = [] #输入的图片标签
    val_images = []   #检验的图片数据
    val_labels = []  #检验的图片标签
    
    # 获取指定文件夹下的图片数量
    def getNum(self, dir):
        count = 0
        for i in range(0, NUMBER):
            dir1 = dir + '%s/' % i
            for _, __, files in os.walk(dir1):
                for filename in files:
                    count += 1
        return count
    
    # 获取指定文件夹下的图片数据
    def getImg(self, dir,imgdata,labeldata):
        index = 0
        for i in range(0, NUMBER):
            dir1 = dir + '%s/' % i
            for _, __, files in os.walk(dir1):
                for filename in files:
                    filename = dir1 + filename
                    img = Image.open(filename)
                    Mytf.imgHandle(self,img,imgdata[index],230)
                    labeldata[index][i] = 1
                    index += 1

    # 获取图片用于训练        
    def getTrainData(self):
        Mytf.time_begin = time.time()
        count = self.getNum(self.img_dir)
        self.input_count = count
        self.input_images = np.array([[0] * IMGSIZE for i in range(count)])
        self.input_labels = np.array([[0] * NUMBER for i in range(count)])
        self.getImg(self.img_dir, self.input_images, self.input_labels)
        
    # 获取图片用于检验训练效果
    def getValData(self):
        count = self.getNum(self.val_dir)
        self.val_count = count
        self.val_images = np.array([[0] * IMGSIZE for i in range(count)])
        self.val_labels = np.array([[0] * NUMBER for i in range(count)])
        self.getImg(self.val_dir, self.val_images, self.val_labels)

    #训练数据
    def train(self,sess,train_step, accuracy):
        group_size = 60
        group_count = int(self.input_count / group_size)
        remaind = self.input_count % group_size
        print("训练数据分为%s组，每组%s个数据，最后一组%s个数据，即将开始训练" % (group_count + 1, group_size, remaind))

        for i in range(1000):
            for n in range(group_count):
                train_step.run(feed_dict={Mytf.img_input: self.input_images[n * group_size:(n + 1) * group_size], Mytf.lab_input: self.input_labels[n * group_size:(n + 1) * group_size], Mytf.keep_prob: 0.5})
            if remaind > 0:
                train_step.run(feed_dict={Mytf.img_input: self.input_images[group_count * group_size:self.input_count-1], Mytf.lab_input: self.input_labels[group_count * group_size:self.input_count-1], Mytf.keep_prob: 0.5})
            if i % 5 == 0:
                ac = accuracy.eval(feed_dict={Mytf.img_input: self.val_images, Mytf.lab_input: self.val_labels, Mytf.keep_prob: 1.0})
                print('第 %d 次训练迭代: 准确率 %0.5f%%' % (i, ac * 100))
                if ac > 0.9999:
                    break
        time_cost = time.time()-Mytf.time_begin
        print('完成训练,花费时间%d秒' % time_cost)
        if not os.path.exists(self.sav_dir):
            os.makedirs(self.sav_dir)
        saver = tf.train.Saver()
        saver_path = saver.save(sess,'%smodel.ckpt'%(self.sav_dir))


    # 设置相关
    def operations(self):
        with tf.Session() as sess:
            w_conv1 = tf.Variable(tf.truncated_normal([8, 8, 1, 16], stddev=0.1), name="w_conv1")
            b_conv1 = tf.Variable(tf.constant(0.1, shape=[16]), name="b_conv1")
            w_conv2 = tf.Variable(tf.truncated_normal([5, 5, 16, 32], stddev=0.1), name="w_conv2")
            b_conv2 = tf.Variable(tf.constant(0.1, shape=[32]), name="b_conv2")

            # 返回两层卷积的结果
            L2_pool = Mytf.convOperate(self,w_conv1, b_conv1, w_conv2, b_conv2)

            w_fc1 = tf.Variable(tf.truncated_normal([16 * 20 * 32, 512], stddev=0.1), name="w_fc1")
            b_fc1 = tf.Variable(tf.constant(0.1, shape=[512]), name="b_fc1")

            # 返回全连接层的结果
            h_fc1 = Mytf.fullConnectOperate(self,L2_pool, w_fc1, b_fc1)
            h_fc1_drop = Mytf.dropOutLayer(self,h_fc1)

            w_fc2 = tf.Variable(tf.truncated_normal([512, NUMBER], stddev=0.1), name="w_fc2")
            b_fc2 = tf.Variable(tf.constant(0.1, shape=[NUMBER]), name="b_fc2")

            # 定义优化器
            val_conv = tf.matmul(h_fc1_drop, w_fc2) + b_fc2
            cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Mytf.lab_input, logits=val_conv))
            train_step = tf.train.AdamOptimizer((1e-4)).minimize(cross_entropy)
            correct_prediction=tf.equal(tf.argmax(val_conv, 1), tf.argmax(Mytf.lab_input, 1))
            accuracy=tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
            sess.run(tf.global_variables_initializer())
            time_cost=time.time() - Mytf.time_begin
            print("一共读取了%s个训练图像(标签)和%s检验图像(标签)，花费时间%d秒" % (self.input_count, self.val_count, time_cost))
            self.train(sess,train_step,accuracy)


                
class MyPredict(Mytf):
    imgPath = ''
    imgName = ''
    License = ''
    predict_list = []
    count = 0

    def __init__(self, path):
        self.imgPath = path
        self.imgName = path.split('/', 1)[-1]


    def predict(self, sess,conv):
        self.count = 0
        for _, __, files in os.walk(self.imgPath):
            for filename in files:
                self.count += 1
        if (self.count < 7):
            print('数量过少，识别失败', self.count)
            
        for j in range(self.count):
            img = Image.open(self.imgPath + '%s.png'%j)
            img_data = [[0] * IMGSIZE for i in range(1)]
            Mytf.imgHandle(self, img, img_data[0],190)
            result = sess.run(conv, feed_dict={Mytf.img_input: np.array(img_data), Mytf.keep_prob: 1.0})
            max1,max2,max3 = 0,0,0
            max1_index,max2_index,max3_index = 0,0,0
            for i in range(NUMBER):
                if result[0][i] > max1:
                    max1 = result[0][i]
                    max1_index = i
            for i in range(NUMBER):
                if (result[0][i] > max2) and (result[0][i] < max1):
                    max2 = result[0][i]
                    max2_index = i
            for i in range(NUMBER):
                if (result[0][i] > max3) and (result[0][i] < max2):
                    max3 = result[0][i]
                    max3_index = i


                    
            self.predict_list.append([max1_index,max1])

            print('图片%s.png的识别结果是：%s: %0.2f%%, %s: %0.2f%%, %s:%0.2f%%, sum = %0.2f' % (j, max1_index, max1 * 100, max2_index, max2 * 100, max3_index, max3 * 100,result[0].sum()))


    def operations(self):
        with tf.Session() as sess:
            saver = tf.train.import_meta_graph("%smodel.ckpt.meta"%(SAV_DIR))
            model_file = tf.train.latest_checkpoint(SAV_DIR)
            saver.restore(sess, model_file)
            w_conv1 = sess.graph.get_tensor_by_name("w_conv1:0")
            b_conv1 = sess.graph.get_tensor_by_name("b_conv1:0")
            w_conv2 = sess.graph.get_tensor_by_name("w_conv2:0")
            b_conv2 = sess.graph.get_tensor_by_name("b_conv2:0")
            L2_pool = Mytf.convOperate(self, w_conv1, b_conv1, w_conv2, b_conv2)
            w_fc1 = sess.graph.get_tensor_by_name("w_fc1:0")
            b_fc1 = sess.graph.get_tensor_by_name("b_fc1:0")
            h_fc1 = Mytf.fullConnectOperate(self,L2_pool, w_fc1, b_fc1)
            h_fc1_drop = Mytf.dropOutLayer(self,h_fc1)
            w_fc2 = sess.graph.get_tensor_by_name("w_fc2:0")
            b_fc2 = sess.graph.get_tensor_by_name("b_fc2:0")
            conv = tf.nn.softmax(tf.matmul(h_fc1_drop, w_fc2) + b_fc2)
            self.predict(sess,conv)


    def getLicense(self):
        # 查找概率最大的连续的7个数
        p =1.0
        if self.count > 7:
            cur = 0
            for i in range(7):
                cur += self.predict_list[i][1]
            max1 = cur
            max1_index = 0
            for i in range(1, self.count - 6):
                cur -= self.predict_list[i - 1][1]
                cur += self.predict_list[i + 6][1]
                if cur > max1:
                    max1 = cur
                    max1_index = i
            for i in range(max1_index,max1_index+7):
                self.License += NUMBERLIST[self.predict_list[i][0]]
                p = p*self.predict_list[i][1]
        else:
            for i in range(self.count):
                self.License += NUMBERLIST[self.predict_list[i][0]]
        print('识别结果为%s, 概率为%0.2f%%'%(self.License,p*100))



        



if __name__ == "__main__":
    mt = MyTrain()
    mt.getTrainData()
    mt.getValData()
    mt.operations()

    # mp = MyPredict('./Divide/f3/')
    # mp.operations()
    # mp.getLicense()

    # for i in range(0, NUMBER):
    #     dir1 = IMG_DIR + '%s/' % i
    #     dir2 = VAL_DIR + '%s/' % i
    #     for _, __, files in os.walk(dir2):
    #         for filename in files:
    #             if os.path.exists(dir1 + filename):
    #                 os.remove(dir1 + filename)
    #                 print('删除文件',dir1+filename)




