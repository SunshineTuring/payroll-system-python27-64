# -*- coding:utf-8 -*-
import os
import sqlite3
import sys
from logger import logger


class operateWorkInfo():
    def __init__(self):
        self.dbDir = 'db\\DB.db'
        if os.path.isdir(sys.path[0]):
            self.currentDir = sys.path[0]
        elif os.path.isfile(sys.path[0]):
            self.currentDir = os.path.dirname(sys.path[0])
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        cu.execute("CREATE TABLE IF NOT EXISTS 'workInfo'"
                   "('emID' VARCHAR(10) NOT NULL,"
                   "'emName' VARCHAR(20) NOT NULL,"
                   "'workID' VARCHAR(20) DEFAULT NULL,"
                   "'workName' VARCHAR(20) DEFAULT NULL,"
                    "'number' INT(10) NOT NULL,"
                    "'unitPrice' DECIMAL(9) NOT NULL,"
                    "'totalPrice' DECIMAL(20) NOT NULL,"
                   "'date' VARCHAR(20) NOT NULL)")

        cu.close()
        cx.close()

    def wiAdd(self,emID,emName,workID,workName,number,unitPrice,totalPrice,date):
        logger.info(u"添加工作记录：%s，%s，%s，%s，%d，%.4f，%.4f，%s" % (emID, emName, workID, workName, number, unitPrice,totalPrice,date))
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        try:
            cu.execute("insert into 'workInfo' values (?,?,?,?,?,?,?,?)" \
                     , (emID,emName,workID,workName,number,unitPrice,totalPrice,date))
        except Exception as E:
            cu.close()
            cx.close()
            logger.exception(u"添加失败")
            return 0
        cx.commit()
        cu.close()
        cx.close()
        return 1

    def wiDelete(self,emID,emName,workID,workName,number,unitPrice,totalPrice,date):
        logger.info(u"删除工作记录：%s，%s，%s，%s，%d，%.4f，%.4f，%s" % (emID, emName, workID, workName, number,unitPrice, totalPrice,date))
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        cu.execute("select * from 'workInfo' where emID='%s' and emName='%s' and workID='%s' and workName='%s'\
                    and number='%d' and unitPrice='%.4f' and totalPrice='%.4f'  and date='%s'" \
                   %(emID,emName,workID,workName,number,unitPrice,totalPrice,date))
        if cu.fetchall()==[]:
            cu.close()
            cx.close()
            logger.error(u"删除失败，不存在该工作记录")
            return 0
        cu.execute("delete from 'workInfo' where emID='%s' and emName='%s' and workID='%s' and workName='%s' and "
                   "number='%d' and unitPrice='%.4f' and totalPrice='%.4f' and date='%s'"\
                   %(emID,emName,workID,workName,number,unitPrice,totalPrice,date))
        cx.commit()
        cu.close()
        cx.close()
        return 1

    def wiModify(self,emID,emName,workID,workName,number,unitPrice,totalPrice,date,\
                 emID1,emName1,workID1,workName1,number1,unitPrice1,totalPrice1,date1):
        logger.info(u"修改工作记录：%s,%s,%s,%s,%d,%.4f,%.4f,%s" % (emID, emName, workID, workName, number,unitPrice,totalPrice, date))
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        sql = "select * from workInfo where emID='%s' and emName='%s' and workID='%s' and workName='%s' and number='%d' and \
              unitPrice='%.4f' and totalPrice='%.4f' and date='%s'"%(emID,emName,workID,workName,number,unitPrice,totalPrice,date)
        cu.execute(sql)
        if cu.fetchall() == []:
            logger.error("修改失败")
            return 0
        try:
            cu.execute("update 'workInfo' set emID='%s',emName='%s',workID='%s',workName='%s',number='%d',unitPrice='%.4f', totalPrice='%.4f',date='%s'"
                       "where emID='%s' and emName='%s' and workID='%s' and workName='%s' and number='%d' and unitPrice='%.4f' and totalPrice='%.4f' and date='%s'"
                       %(emID1,emName1,workID1,workName1,number1,unitPrice1,totalPrice1,date1,emID,emName,workID,workName,number,unitPrice,totalPrice,date))
        except Exception as E:
            cu.close()
            cx.close()
            logger.exception(u"修改失败")
            return 0
        cx.commit()
        cu.close()
        cx.close()
        return 1


    def wiGetBYemID(self,emID):
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        sql = "select * from 'workInfo' where emID='%s'" % emID
        cu.execute(sql)
        emInf = cu.fetchall()
        cu.close()
        cx.close()
        if emInf == []:
            return 0
        return emInf

    def wiGetBYworkID(self,workID):
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        sql = "select * from 'workInfo' where workID='%s'" % workID
        cu.execute(sql)
        emInf = cu.fetchall()
        cu.close()
        cx.close()
        if emInf == []:
            return 0
        return emInf

    def wiGetByDate(self,date):
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        sql = "select * from 'workInfo' where date='%s'" % date
        cu.execute(sql)
        emInf = cu.fetchall()
        cu.close()
        cx.close()
        if emInf == []:
            return 0
        return emInf

    def wiGetAll(self):
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        sql = "select * from 'workInfo' order by date"
        cu.execute(sql)
        emInf = cu.fetchall()
        cu.close()
        cx.close()
        if emInf == []:
            return 0
        return emInf

    def wiGetByDateArea(self,date1,date2):
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        sql = "select * from 'workInfo' where date>='%s' and date<='%s'" % (date1, date2)
        cu.execute(sql)
        emInf = cu.fetchall()
        cu.close()
        cx.close()
        if emInf == []:
            return 0
        return emInf

    def wiGetByDateAreaAndNameAndId(self,date1,date2,emName,emID):
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()

        sql = "select * from 'workInfo' where date>='%s' and date<='%s' and emName='%s'\
              and emID='%s' order by date"%(date1,date2,emName,emID)
        cu.execute(sql)
        emInf = cu.fetchall()
        cu.close()
        cx.close()
        if emInf == []:
            return 0
        return emInf


if __name__ == "__main__":
    EM = operateWorkInfo()
    import datetime
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')

    # EM.wiAdd("1", u"李雷", "1", u"亚焊", 222,0.25, 222*0.25,date)
    # EM.wiAdd("1", u"李雷", "1",u"亚焊" ,234,0.34,234*0.34,date)
    # print (EM.wiDelete("1", u"李雷", "1", u"亚焊", 222, date))
    # print (EM.wiDelete("1", u"李雷", "1", u"亚焊", 223, date))
    info1 = EM.wiGetAll()
    info2 = EM.wiGetByDateArea("2017-05-13","2017-05-14")
    # print info
    # print(EM.wiModify("1", u"成龙", "1",u"亚焊" ,20,0.0021,0.042,date,"1", u"成龙", "1",u"亚焊" ,200,0.0021,0.42,date))

    print (info1)
    print (info2)
    # print (EM.wiGetBYemID(1))


