# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/5/24
# filename:testMysqlTeradown

# mysql后置操作，修改数据源端口号，删除资产

import pytest
import os
import allure
from interfaceBox.datasourceManage.database import Database
from interfaceBox.senDatafind.taskList import TaskList
from interfaceBox.maskRule.maskRuleGroup import MaskRuleGroup
from interfaceBox.extRule.extRuleGroup import ExtRuleGroup
from config.config import database
from interfaceBox.login.login import Login
from public.common import do_log
from testCase.testMysql.mysqlTestConfig import databaseName
import traceback
import pymysql
from config.config import ip
import time

@allure.epic('mysql数据库流程测试')
@allure.feature('数据源模块测试')
class TestDatasourceMD:
    token = Login().login()
    db = Database(token)
    datafind = TaskList(token)
    mRule = MaskRuleGroup(token)
    eRule = ExtRuleGroup(token)
    dbid = None

    def setup_class(self):
        global dbid
        dblist = self.db.databaseList({"dbType":"MySql"})
        dbid = dblist['data']['content'][0]['id']

    @allure.title('修改数据源端口号测试')
    def testDatabaseModify(self):
        addData = database["mysqlDB"]
        addData.update({"name":databaseName,"newname":databaseName,"id":dbid,"proxyPort":"13611"})
        add = self.db.databaseModify(indata=addData)
        try:
            assert add['status'] == 0
            time.sleep(10)
            conn = pymysql.connect(host=ip, port=13611, user=database["mysqlDB"]["userName"],
                                password=database["mysqlDB"]["passWord"],
                                database=database["mysqlDB"]["databasename"], charset='utf8')
            cursor = conn.cursor()
            cursor.execute("select * from auto_table_copy")
            assert cursor.fetchall()[0][1] == "张*"
            cursor.close()
            conn.close()
            do_log.logOutput("info","修改数据源端口号测试通过")
        except Exception as e:
            do_log.logOutput("error","修改数据源端口号测试未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("删除mysql数据源测试")
    def testDatabaseDelete(self):
        dbdelete = self.db.databaseDelete({'name':databaseName,'type':'MySql'})
        time.sleep(6)
        try:
            assert dbdelete['status'] == 0
            # 校验敏感数据列表
            assert self.datafind.taskList({"type":"MySql"})['data'] == []
            # 校验脱敏规则列表
            assert self.mRule.maskRuleGroupList({"type":"MySQL"})['data'] == []
            # 校验拓展规则列表
            assert self.eRule.extRuleGroupList({"type":"MySQL"})['data'] == []
            # 校验端口是否关闭
            try:
                pymysql.connect(host=ip, port=13611, user=database["mysqlDB"]["userName"],
                                       password=database["mysqlDB"]["passWord"],
                                       database=database["mysqlDB"]["databasename"], charset='utf8')
                testconn = True
            except:
                testconn = False
            assert testconn is False
            do_log.logOutput("info","删除mysql数据源测试通过")
        except Exception as e:
            do_log.logOutput("error","删除mysql数据源测试未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e


if __name__ == '__main__':
    pytest.main(['testMysqlTeradown.py', '-s'])








