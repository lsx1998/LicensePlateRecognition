# -*- coding: utf-8 -*-

import pymysql

# 数据库类，使用前要先建立database：LPRDB 和用户LPRadmin，密码123456，拥有LPRDB中所有权限
'''
第一次使用前建议先在数据库端root权限下输入以下语句建立相关数据库
drop database if exists LPRDB;
create database LPRDB;
create user 'LPRadmin'@'localhost' identified by '123456';
grant all on LPRDB.* to 'LRPadmin'@'localhost';

use LPRDB;

drop table if exists `record`;
create table `record`(
    `lisense` int(7) not null,
    `first_appear_time` datetime DEFAULT CURRENT_TIMESTAMP,
    `last_appear_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `total_times` int default 1,
    `pic_name` varchar(64),
    primary key (`lisense`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
class MyDataBase():
    def __init__(self):
        self.username = 'LPRadmin'
        self.host = 'localhost'
        self.password = '123456'
        self.db = 'LPRDB'
        self.charset = 'utf8'
        self.isConnected = False

    def myConnect(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                db=self.db,
                charset=self.charset
            )
            self.cur = self.conn.cursor()
            self.cur.execute('show tables;')
            self.isConnected = True
        except pymysql.Error as e:
            print(e)
            print('数据库连接失败')
            self.isConnected = False
        finally:
            return self.isConnected

    def myClose(self):
        if self.isConnected:
            self.cur.close()
            self.conn.close()

    # 返回数据库中是否查询到对应车牌，-1表示连接失败，0表示未查询到，其余表示曾出现次数
    def mySelect(self, str):
        if self.myConnect():
            sql = 'select total_times from `record` where `lisense` = %s;' % str
            self.cur.execute(sql)
            res = self.cur.fetchall()
            if not res:
                num = 0
            else:
                num = res[0][0]
            self.myClose()
            return num
        return -1

    # 插入一个新的车牌记录，要求输入车牌号和图片源，并且保证原本没有此条车牌记录
    def myInsert(self, lisense, picname):
        if self.myConnect():
            sql = 'insert into `record`(`lisense`,`pic_name`) values (%s,\'%s\');' % (lisense,picname)
            res = self.cur.execute(sql)
            self.conn.commit()
            self.myClose()
            return res
        return -1

    # 更新一个车牌记录，要求输入车牌号和出现次数，图片源，并保证存在此车牌号
    def myUpdate(self, lisense, picname,times):
        if self.myConnect():
            sql = 'update `record` set `total_times` = %d, `pic_name` = \'%s\' where `lisense` = %s;' % (times,picname,lisense)
            res = self.cur.execute(sql)
            self.conn.commit()
            self.myClose()
            return res
        return - 1

    def getLastTime(self, str):
        if self.myConnect():
            sql = 'select last_appear_time from `record` where `lisense` = %s;' % str
            self.cur.execute(sql)
            res = self.cur.fetchall()
            if not res:
                num = -1
            else:
                num = res[0][0]
            self.myClose()
            return num
        return -1       
        
    def myProcess(self, lisense, picname):
        num = self.mySelect(lisense)
        if num == -1:
            return '数据库连接失败'
        elif num == 0:
            if self.myInsert(lisense,picname) == -1:
                return '数据库中不存在车牌号%s，插入失败：无法连接到数据库' % lisense
            else:
                return '数据库中不存在车牌号%s，已插入' % lisense
        else:
            res = self.getLastTime(lisense)
            if self.myUpdate(lisense, picname, num + 1) == -1:
                return '数据库中存在车牌号%s，已出现 %d 次，上次出现时间为 %s，更新信息失败：无法连接到数据库' % (lisense,num,res)
            else:
                return '数据库中存在车牌号%s，已出现 %d 次，上次出现时间为 %s，已更新信息' % (lisense,num,res)


if __name__ == '__main__':
    mydb = MyDataBase()
    # mydb.mySelect('1234567')
    # # mydb.myInsert('1234566','./origin/t100.jpg')
    # mydb.myUpdate('1234566',2,'./origin/t101.jpg')
    print(mydb.myProcess('1234567','./origin/t3.jpg'))

