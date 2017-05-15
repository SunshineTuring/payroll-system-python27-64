# -*- coding:utf-8 -*-
import os
import sqlite3
import sys
from logger import logger


class operateWorkType():
    def __init__(self):
        self.dbDir = 'db\\DB.db'
        if os.path.isdir(sys.path[0]):
            self.currentDir = sys.path[0]
        elif os.path.isfile(sys.path[0]):
            self.currentDir = os.path.dirname(sys.path[0])
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        cu.execute("CREATE TABLE IF NOT EXISTS 'workType'"
                   "('workID' VARCHAR(20) NOT NULL,"
                   "'workName' VARCHAR(20) NOT NULL,"
                   "'unitPrice' DECIMAL(9) DEFAULT NULL,"
                   "PRIMARY KEY ('workID'))")
        cu.close()
        cx.close()

    def wtAdd(self,workID,workName,unitPrice):
        logger.info(u"添加工种：%s，%s，%.4f" % (workID, workName, unitPrice))
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        try:
            cu.execute("insert into 'workType' values (?,?,?)" \
                     , (workID,workName,unitPrice))
        except Exception as E:
            cu.close()
            cx.close()
            logger.exception(u"添加失败")
            return 0
        cx.commit()
        cu.close()
        cx.close()
        return 1

    def wtDelete(self,workID):
        logger.info(u"删除工种：%s" % workID)
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        cu.execute("select * from 'workType' where workID='%s'" % workID)
        if cu.fetchall()==[]:
            cu.close()
            cx.close()
            logger.error(u"删除失败，不存在该工种")
            return 0
        cu.execute("delete from 'workType' where workID='%s'" %workID)
        cx.commit()
        cu.close()
        cx.close()
        return 1

    def wtModify(self,workID1,workID2,workName,unitPrice):
        logger.info(u"修改工种：%s" % (workID1))
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        try:
            cu.execute("update 'workType' set workID='%s',workName='%s',unitPrice='%.4f'"
                       "where workID='%s'" % (workID2, workName, unitPrice, workID1))
        except Exception as E:
            cu.close()
            cx.close()
            logger.exception(u"修改失败")
            return 0
        cx.commit()
        cu.close()
        cx.close()
        return 1


    def wtGet(self,workID):
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        sql = "select * from 'workType' where workID='%s'" % workID
        cu.execute(sql)
        emInf = cu.fetchall()
        cu.close()
        cx.close()
        if emInf == []:
            return 0
        return emInf

    def wtGetByName(self,workName):
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        sql = "select * from 'workType' where workName='%s' order by workID" % workName
        cu.execute(sql)
        emInf = cu.fetchall()
        cu.close()
        cx.close()
        if emInf == []:
            return 0
        return emInf

    def wtGetAll(self):
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        sql = "select * from 'workType' order by workID"
        cu.execute(sql)
        emInf = cu.fetchall()
        cu.close()
        cx.close()
        if emInf == []:
            return 0
        return emInf


if __name__ == "__main__":
    WT = operateWorkType()
    WT.wtAdd(1,u"亚焊",1.254521)
    WT.wtAdd(2, u"碰焊", 0.2545)
    print (WT.wtDelete(3))
    print (WT.wtDelete(2))
    print(WT.wtModify(10,5,u"切线",1.25488))
    print (WT.wtGet(1))
    print (WT.wtGet(4))


