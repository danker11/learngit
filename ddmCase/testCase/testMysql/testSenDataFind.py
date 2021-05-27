# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/4/28
# filename:testSenDataFind

import pytest
import os
import allure
from interfaceBox.senDatafind import taskList
from interfaceBox.senDatafind import taskConfig
from interfaceBox.senDatafind import discoveryList
from time import sleep
from interfaceBox.login.login import Login
from testCase.testMysql.mysqlTestConfig import databaseName,dataTypes
from public.common import do_log
import traceback

databaseName = databaseName  # 可重新传参，方便单个模块测试
@allure.epic('mysql数据库流程测试')
@allure.feature('敏感数据发现模块测试')
class TestSenDataFind:
    token = Login().login()
    config = taskConfig.TaskConfig(token)
    tlist = taskList.TaskList(token)
    dlist = discoveryList.DiscoveryList(token)
    taskId = None
    avgThread = None
    @allure.title("获取扫描任务列表测试")
    def testTasklist(self):
        global taskId
        taList = self.tlist.taskList({"type":"MySql"})
        try:
            assert taList['status'] == 0
            assert taList['data'][0]['taskName'] == databaseName
            do_log.logOutput("info", "获取扫描任务列表通过")
            taskId = str(taList['data'][0]['id'])
            print(f"扫描任务id为{taskId}")
        except Exception as e:
            do_log.logOutput("error","获取扫描任务列表未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("获取最大线程数测试")
    def testMaxThreadCountGet(self):
        maxThreadCountGet = self.config.maxThreadCountsGet()
        try:
            assert maxThreadCountGet['status'] == 0#这里只是简单的断言，没有校验系统的CPU核数，后续优化
            do_log.logOutput("info", "获取最大线程数用例通过")
        except Exception as e:
            do_log.logOutput("error","获取最大线程数用例未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("任务配置获取数据类型列表测试")
    def testAlginfoList(self):
        alginfo = self.config.alginfoList()
        try:
            assert alginfo['status'] == 0
            for dataType in dataTypes:
                assert dataType in str(alginfo['data'])
            do_log.logOutput("info", "任务配置获取数据类型列表测试通过")
        except Exception as e:
            do_log.logOutput("error","任务配置获取数据类型列表测试未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("任务配置获取所有Schema测试")
    def testAllSchemaList(self):
        allSchema = self.config.getAllSchema({'name':databaseName,'type':'MySQL'})
        try:
            assert allSchema['status'] == 0
            assert "auto" in str(allSchema)
            do_log.logOutput("info", "任务配置获取所有Schema测试通过")
        except Exception as e:
            do_log.logOutput("error","任务配置获取所有Schema测试未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("任务配置获取配置信息测试")
    def testGetDiscoveryConfig(self):
        global avgThread
        discoveryConfig = self.config.getDiscoveryConfig({'taskId':taskId,'type':'MySQL'})
        try:
            assert discoveryConfig['status'] == 0
            assert discoveryConfig['data']['sampleCount'] == 10000
            if discoveryConfig['data']['threadCount'] == 0:
                avgThread = 1
            else:
                avgThread = discoveryConfig['data']['threadCount']
            do_log.logOutput("info", "任务配置获取配置信息测试通过")
        except Exception as e:
            do_log.logOutput("error","任务配置获取配置信息测试未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("任务配置获取所有模板测试")
    def testTemplateList(self):
        global avgThread
        templateList = self.config.templateList({'type':'MySQL'})
        try:
            assert templateList['status'] == 0
            assert '个人敏感信息模版' in str(templateList['data'])
            assert '企事业单位敏感信息模版' in str(templateList['data'])
            do_log.logOutput("info", "任务配置获取所有模板测试通过")
        except Exception as e:
            do_log.logOutput("error","任务配置获取所有模板测试未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("任务配置不勾选模板获取所有数据类型测试")
    def testTemplateNoUsed(self):
        global avgThread
        templateNoUsed = self.config.templateNoUsed({'dbType':'MySQL','name':databaseName})
        try:
            assert templateNoUsed['status'] == 0
            for dataType in dataTypes:
                assert dataType in str(templateNoUsed['data'])
            do_log.logOutput("info", "任务配置不勾选模板获取所有数据类型测试通过")
        except Exception as e:
            do_log.logOutput("error","任务配置不勾选模板获取所有数据类型测试未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("任务配置获取所选库下所有表测试")
    def testGetAllTable(self):
        global avgThread
        allTable = self.config.getAllTable({'Type':'MySQL','name':databaseName,'schemaName':'auto'})
        try:
            assert allTable['status'] == 0
            assert allTable['data'] == ['auto_table', 'auto_table_copy', 'auto_table_copy_mask']
            do_log.logOutput("info", "任务配置获取所选库下所有表测试通过")
        except Exception as e:
            do_log.logOutput("error","任务配置获取所选库下所有表测试未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("保存敏感发现任务测试")
    def testSaveTaskConfig(self):
        scanSchemas = [
            {"allTable": True, "schema": "auto", "tables": ["auto_table", "auto_table_copy", "auto_table_copy_mask"]}]
        try:
            save = self.config.saveTaskConfig({"taskId":taskId,"id":taskId,"dbType":"MySql","threadCount":avgThread,"scanSchemas":scanSchemas})
            assert save['status'] == 0
            do_log.logOutput("info", "保存敏感发现任务通过")
        except Exception as e:
            do_log.logOutput("error","保存敏感发现任务未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("启动扫描任务测试")
    def testTaskStart(self):
        start = self.tlist.taskStart({'id':int(taskId)})
        try:
            assert start['status'] == 0
            do_log.logOutput("info", "启动扫描任务测试通过")
        except Exception as e:
            do_log.logOutput("error", "启动扫描任务测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("扫描进度测试")
    def testTaskStatus(self):
        status = self.tlist.taskList({"type":"MySql"})['data'][0]["status"]
        try:
            while status != "Complete":
                sleep(2)
                status = self.tlist.taskList({"type":"MySql"})['data'][0]["status"]
            assert status == "Complete"
            do_log.logOutput("info", "扫描进度测试通过")
        except Exception as e:
            do_log.logOutput("error", "扫描进度测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("扫描结果测试")
    def testDiscoveryList(self):
        dislist = str(self.dlist.discoveryList({"id":taskId, "dbType":"MySQL"}))
        try:
            assert "auto_table" in dislist
            assert "auto_table_copy" in dislist
            do_log.logOutput("info", "扫描结果测试通过")
        except Exception as e:
            do_log.logOutput("error", "扫描结果测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e




if __name__ == '__main__':
    pytest.main(['testSenDataFind.py', '-s'])
