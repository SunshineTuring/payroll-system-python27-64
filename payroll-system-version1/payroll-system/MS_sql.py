# -*- coding:utf-8 -*-
import sqlite3
import sys
import os
import datetime
dbDir = 'db\\employee.db'
currentDir = sys.path[0]

def init():
    '''
    数据库初始化
    1）创建员工管理数据库；
    2）为每个员工创建一个数据库
    :return:
    '''
    cx = sqlite3.connect(os.path.join(currentDir,dbDir))
    cu = cx.cursor()
    cu.execute("create table if not exists 'staff'"
               "('name' varchar(20) NOT NULL,"
               "'ID' int(11) DEFAULT NULL,"
               "'IDCard' int(30) DEFAULT NULL,"
               "'phone' varchar(20) DEFAULT NULL,"
               "PRIMARY KEY ('name'))")
    cu.execute("select name from staff")
    for name in cu.fetchall():
        cu.execute("create table if not exists '%s'"
                   "('name' varchar(30) NOT NULL,"
                   "'ID' int(10) NOT NULL,"
                   "'price' int(10) NOT NULL,"
                   "'number' int(10) NOT NULL,"
                   "'totalPrice' int(10) NOT NULL,"
                   "'date' varchar(20) NOT NULL)"%name[0])
    cu.close()
    cx.close()

def addStaff(name,ID=0,IDCard=0,phone=0):
    '''
    添加员工，以名字为唯一标志
    1）添加前判断是否已经存在该员工，存在则提示，否则往staff数据库添加记录
    2）添加员工的同时创建相应数据库
    :param name:
    :param ID:
    :param IDCard:
    :param phone:
    :return:
    '''
    cx = sqlite3.connect(os.path.join(currentDir, dbDir))
    cu = cx.cursor()
    sql = "select * from 'staff' where name='%s'"%name
    cu.execute(sql)

    if cu.fetchall() !=  []:
        print ("添加失败，已经存在'%s'"%name)
    else:
        cu.execute("insert into 'staff' values (?,?,?,?)"\
               ,(name,ID,IDCard,phone))
        cu.execute("create table if not exists '%s'"
                   "('name' varchar(30) NOT NULL,"
                   "'ID' int(10) NOT NULL,"
                   "'price' int(10) NOT NULL,"
                   "'number' int(10) NOT NULL,"
                   "'totalPrice' int(10) NOT NULL,"
                   "'date' varchar(20) NOT NULL)" % name)
        cx.commit()
    cu.close()
    cx.close()

def deleStaff(name):
    '''
    删除员工
    1）判断待删除员工是否存在，不存在则提示
    2）删除员工同时删除相应的数据库
    :param name:
    :return:
    '''
    cx = sqlite3.connect(os.path.join(currentDir, dbDir))
    cu = cx.cursor()
    sql = "select * from 'staff' where name='%s'" % name
    cu.execute(sql)

    if cu.fetchall() == []:
        print("删除失败，不存在'%s'" % name)
    else:
        cu.execute("delete from 'staff' where name='%s'"%name)
        cu.execute("drop table '%s'"%name)
        cx.commit()
    cu.close()
    cx.close()



def updateStaff(name,item,value):
    '''
    更新员工信息
    1）判断员工是否存在
    2）更新员工信息
    3）如果更新员工名字，先判断更新后的员工是否已经ucnzai，不存在则同时重命名相应的数据库，
    :param name:
    :param item:
    :param value:
    :return:
    '''
    cx = sqlite3.connect(os.path.join(currentDir,dbDir))
    cu = cx.cursor()
    sql = "select * from 'staff' where name='%s'" % name
    cu.execute(sql)
    if cu.fetchall() == []:
        print("更新失败，不存在'%s'" % name)
    else:
        if item=='name':
            sql = "select * from 'staff' where name='%s'" % value
            cu.execute(sql)
            if cu.fetchall() == []:
                cu.execute("update 'staff' set '%s'='%s' where name='%s'" % (item, value, name))
                cu.execute("ALTER TABLE %s RENAME TO '%s'"%(name,value))
            else:
                print("更新失败，已经存在%s"%value)
        else:
            cu.execute("update 'staff' set '%s'='%s' where name='%s'" % (item, value, name))
        cx.commit()
    cu.close()
    cx.close()

def checkItemExie(name):
    '''
    判断表是否存在，不存在则提错
    :param name:
    :return:re:存在表则返回1，否则返回0
    '''
    cx = sqlite3.connect(os.path.join(currentDir,dbDir))
    cu = cx.cursor()
    sql = "SELECT COUNT(*) FROM sqlite_master where type='table' and name='%s'"%name
    cu.execute(sql)
    re = cu.fetchall().pop()
    cu.close()
    cx.close()
    return re[0]


def addItem(emp,name,ID,price,number,totalPrice,date):
    '''
    添加工种
    :param emp:
    :param name:
    :param ID:
    :param price:
    :param number:
    :param totalPrice:
    :param date:
    :return:
    '''
    cx = sqlite3.connect(os.path.join(currentDir, dbDir))
    cu = cx.cursor()
    cu.execute("insert into '%s' values (?,?,?,?,?,?)" %emp\
                   , (name, ID, price, number,totalPrice,date))
    cx.commit()
    cu.close()
    cx.close()

def getTotalPrice(price,number):
    '''
    根据单价和数量计算总价
    :param price:
    :param number:
    :return:
    '''
    return price*number

def getDate():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')


if __name__ ==  '__main__':
    init()
    #测试初始化函数
    cx = sqlite3.connect(os.path.join(currentDir, dbDir))
    cu = cx.cursor()
    cu.execute("select * from staff")
    print(cu.fetchall())
    #测试添加函数功能：添加数据库已存在的记录时不添加记录，并提示
    addStaff("李明",1,123,"123")
    addStaff("小明", 1, 123, "123")
    addStaff("小陈", 1, 123, "123")
    addStaff("小陈", 1, 123, "123")
    cu.execute("select * from staff")
    print(cu.fetchall())
    #测试删除函数功能，删除不存在的记录时提示
    deleStaff("小李")
    deleStaff("小陈")
    cu.execute("select * from staff")
    print(cu.fetchall())
    #测试更新函数，更新不存在记录时提示，更新员工名字时判断新名字是否存在，不存在则同步更新对应表
    updateStaff("小李","phone","sss")
    updateStaff("小明", "phone", "sss")
    updateStaff("小明", "name", "sss")
    cu.execute("select * from staff")
    print(cu.fetchall())
    #测试判断表是否存在函数,不存在返回0，存在返回1
    print (checkItemExie('staff'))
    print (checkItemExie('小名'))


    if checkItemExie('李明'):
        emp = '李明'
        name = '亚焊'
        price = 0.62
        number = 3000
        totalPrice = getTotalPrice(price,number)
        date = getDate()
        ID = 1
        addItem(emp, name, ID, price, number, totalPrice, date)



