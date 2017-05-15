# -*- coding:utf-8 -*-
import os
import sqlite3
import sys

from logger import logger

class operateEmployee():
    def __init__(self):
        self.dbDir = 'db\\DB.db'
        if os.path.isdir(sys.path[0]):
            self.currentDir = sys.path[0]
        elif os.path.isfile(sys.path[0]):
            self.currentDir = os.path.dirname(sys.path[0])
        logger.info(self.currentDir)
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        cu.execute("CREATE TABLE IF NOT EXISTS 'employee'"
                   "('emID' VARCHAR(10) NOT NULL,"
                   "'emName' VARCHAR(20) NOT NULL,"
                   "'emSex' VARCHAR(8) DEFAULT NULL,"
                   "'emPhone' VARCHAR(20) DEFAULT NULL,"
                   "PRIMARY KEY ('emID'))")
        cu.close()
        cx.close()

    def emAdd(self,emID,emName,emSex,emPhone):
        logger.info(u"添加用户：%s，%s，%s，%s" % (emID, emName, emSex, emPhone))
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        try:
            cu.execute("insert into 'employee' values (?,?,?,?)" \
                     , (emID, emName, emSex, emPhone))
        except Exception as E:
            cu.close()
            cx.close()
            logger.exception(u"添加失败")
            return 0
        cx.commit()
        cu.close()
        cx.close()
        return 1

    def emDelete(self,emID):
        logger.info(u"删除用户：%s" % emID)
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        cu.execute("select * from 'employee' where emID='%s'" % emID)
        if cu.fetchall()==[]:
            cu.close()
            cx.close()
            logger.error(u"删除失败，不存在该用户")
            return 0
        cu.execute("delete from 'employee' where emID='%s'" %emID)
        cx.commit()
        cu.close()
        cx.close()
        return 1

    def emModify(self,emID1,emID2,emName,emSex,emPhone):
        logger.info(u"修改用户：%s" % (emID1))
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        try:
            cu.execute("update 'employee' set emID='%s',emName='%s',emSex='%s',emPhone='%s'"
                       "where emID='%s'" %(emID2,emName,emSex,emPhone,emID1))
        except Exception as E:
            cu.close()
            cx.close()
            logger.exception(u"修改失败")
            return 0
        cx.commit()
        cu.close()
        cx.close()
        return 1


    def emGet(self,emID):
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        sql = "select * from 'employee' where emID='%s'" % emID
        cu.execute(sql)
        emInf = cu.fetchall()
        cu.close()
        cx.close()
        if emInf == []:
            return 0
        return emInf

    def emGetByName(self,emName):
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        sql = "select * from 'employee' where emName='%s' order by emName" % emName
        cu.execute(sql)
        emInf = cu.fetchall()
        cu.close()
        cx.close()
        if emInf == []:
            return 0
        return emInf

    def emGetAll(self):
        cx = sqlite3.connect(os.path.join(self.currentDir, self.dbDir))
        cu = cx.cursor()
        sql = "select * from 'employee' order by emID"
        cu.execute(sql)
        emInf = cu.fetchall()
        cu.close()
        cx.close()
        if emInf == []:
            return 0
        return emInf


if __name__ == "__main__":
    EM = operateEmployee()
    EM.emAdd(1,u"李明",u"男",u"1874401")
    EM.emAdd(2, u"李雷", u"男", u"1874401")
    # print (EM.emDelete(1))
    # print (EM.emDelete(2))
    # print(EM.emModify(1,4,u"小明",u"男",u"1874401"))
    print (EM.emGetAll())


