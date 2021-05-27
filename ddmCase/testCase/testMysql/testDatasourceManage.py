# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/4/28
# filename:TestDatasourceManage



'''
前置条件
登录获取token,判断数据库是否可连接，连接后创建3张表，清空数据
后置条件
清空数据

数据源模块测试

'''
import pytest
import os
import allure
from interfaceBox.datasourceManage.database import Database
from config.config import database
from interfaceBox.login.login import Login
from public.common import do_log
from public.DataBase.dbMysql import DbMysql
from testCase.testMysql.mysqlTestConfig import databaseName
import traceback


@allure.epic('mysql数据库流程测试')
@allure.feature('数据源模块测试')
class TestDatasourceManage:
    db = Database(Login().login())
    dbconn = DbMysql(2)  # 用于判断源库是否连接

    @allure.title('添加mysql数据源测试')
    def testDatabaseAdd(self):
        addData = database["mysqlDB"]
        name = databaseName
        addData.update({"name":name,"newname":name})
        add = self.db.databaseAdd(indata=addData)
        try:
            assert add['status'] == 0
            do_log.logOutput("info","新增mysql数据源通过")
        except Exception as e:
            do_log.logOutput("error","新增mysql数据源未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("搜索mysql数据源测试")
    def testDatabaseList(self):
        dblist = self.db.databaseList({"dbType":"MySql"})
        try:
            assert dblist['status'] == 0
            assert dblist['data']['content'][0]['name'] == databaseName
            do_log.logOutput("info","查看mysql数据源通过")
        except Exception as e:
            do_log.logOutput("error","查看mysql数据源未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("数据源测试连接测试")
    def testDatabaseConnect(self):
        connect = self.db.databaseConnect({"name":databaseName,"type":"MySQL"})
        try:
            assert connect['status'] == 0
            assert "连接成功" in str(connect['data'])
            do_log.logOutput("info","数据源测试连接测试通过")
        except Exception as e:
            do_log.logOutput("error","数据源测试连接测试未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e



if __name__ == '__main__':
    pytest.main(['testDatasourceManage.py', '-s'])