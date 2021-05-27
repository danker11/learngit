# !/usr/bin/python3
# -*- coding: utf-8 -*-


import requests
from public.common.filePath import filePath
from public.common.getExcelContent import GetExcelConetnt
from public.common.timeStamp import TimeStamp
from public.common.do_log import logOutput
import traceback
from interfaceBox.login.login import Login

'''
敏感扫描任务配置：

任务配置获取最大线程数接口
获取所有数据类型接口
获取所有库名接口
加载发现配置接口
获取行业模板接口
获取不使用的模板接口
选择库之后，获取库下所有表接口

'''


class TaskConfig:


    def __init__(self,token):
        self.token = token
        requests.packages.urllib3.disable_warnings()

    def maxThreadCountsGet(self):
        '''
        获取最大线程数接口
        :param code:code值为true/false
        :return:默认返回数据，code==false返回接口状态
        '''
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_senDataFind_Path() + '/任务配置获取最大线程数接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=base_url, headers=header, verify=False)
        try:
            logOutput("info", "任务配置获取最大线程数接口正常，返回的结果为{}".format(r.json()))
            return r.json()
        except Exception as e:
            logOutput("error", "任务配置获取最大线程数接口错误，返回的结果为{}".format(r.json()))
            logOutput("error", traceback.format_exc())
            raise e

    def alginfoList(self):
        '''
        任务配置获取数据类型列表接口
        :return: 返回所有的数据类型
        '''
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_senDataFind_Path() + '/任务配置获取数据类型列表接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=base_url, headers=header, verify=False)
        try:
            logOutput("info", "任务配置获取数据类型列表接口正常，返回的结果为{}".format(r.json()))
            return r.json()
        except Exception as e:
            logOutput("error", "任务配置获取数据类型列表接口错误，返回的结果为{}".format(r.json()))
            logOutput("error", traceback.format_exc())
            raise e

    def getAllSchema(self,indata):
        '''
        任务配置获取所有数据库列表接口
        :return: 返回所有的schema
        '''
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_senDataFind_Path() + '/任务配置获取所有数据库列表接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=base_url, params=indata, headers=header, verify=False)
        try:
            logOutput("info", "任务配置获取所有数据库列表接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            logOutput("error", "任务配置获取所有数据库列表接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            logOutput("error", traceback.format_exc())
            raise e

    def getAllTable(self,indata):
        '''
        任务配置获取库下所有表接口
        :return: 返回所有的table
        '''
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_senDataFind_Path() + '/任务配置获取所有数据表接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=base_url, params=indata, headers=header, verify=False)
        try:
            logOutput("info", "任务配置获取所有数据表接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            logOutput("error", "任务配置获取所有数据表接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            logOutput("error", traceback.format_exc())
            raise e


    def getDiscoveryConfig(self,indata):
        '''
        任务配置获取配置信息接口
        :return: 返回扫描任务配置信息
        '''
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_senDataFind_Path() + '/任务配置获取配置信息接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=indata, headers=header, verify=False)
        try:
            logOutput("info", "任务配置获取配置信息接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            logOutput("error", "任务配置获取配置信息接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            logOutput("error", traceback.format_exc())
            raise e

    def templateList(self,indata):
        '''
        任务配置获取模板接口
        :return: 返回扫描任务配置模板枚举选项
        '''
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_senDataFind_Path() + '/任务配置获取模板接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=base_url, params=indata, headers=header, verify=False)
        try:
            logOutput("info", "任务配置获取模板接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            logOutput("error", "任务配置获取模板接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            logOutput("error", traceback.format_exc())
            raise e

    def templateNoUsed(self, indata=None):
        '''
        任务配置不选择模板返回所有数据类型接口
        :param indata: 传入参数：assetId:任务id，好像一直都是空的
                        dbType:数据库类型，name:资产名称
        :return:返回接口json
        '''
        if indata is None:
            indata = {"assetId": ''}
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_senDataFind_Path() + '/任务配置不使用模板返回数据类型接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, headers=header, json=param_data, verify=False)
        try:
            logOutput("info", "任务配置不选择模板返回所有数据类型接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            logOutput("error", "任务配置不选择模板返回所有数据类型接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            logOutput("error", traceback.format_exc())
            raise e

    def saveTaskConfig(self, indata=None):
        '''
        保存任务配置接口
        :param indata: 传入参数：taskId:任务id，数字类型、dbType:数据库类型、threadCount:线程数配置
                        scanSchemas:选择扫描的schema/table，sampleCount:抽取样本数配置
        :return:返回接口json
        '''
        if indata is None:
            indata = {"sampleCount": 10000}
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_senDataFind_Path() + '/任务配置保存接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, headers=header, json=param_data, verify=False)
        try:
            logOutput("info", "任务配置保存接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            logOutput("error", "任务配置保存接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            logOutput("error", traceback.format_exc())
            raise e


if __name__ == '__main__':
    from  pprint import pprint
    token = Login().login()
    task = TaskConfig(token)
    # threadCount = task.maxThreadCountsGet()
    # print(threadCount)
    # scanSchemas = [{"allTable":True,"schema":"auto","tables":["auto_table","auto_table_copy","auto_table_copy_mask"]}]
    # task.saveTaskConfig({"taskId":136,"id":136,"dbType":"MySql","threadCount":2,"scanSchemas":scanSchemas})
    # print(task.alginfoList()) #获取所有数据库类型
    # print(task.getAllSchema({'name':'自动化流程-mysql库测试','type':'MySQL'})) #获取所有数据库名
    # print(task.getDiscoveryConfig({"type":"MySQL","taskId":169}))  #获取扫描任务配置信息
    # pprint(task.templateList({'type':'MySQL'})) #获取所有模板
    # print(task.templateNoUsed({'dbType':'MySQL','name':'自动化流程-mysql库测试'})) #不选择模板时显示所有数据类型
    print(task.getAllTable({'schemaName':'auto','type':'MySQL','name':'自动化流程-mysql库测试'}))


