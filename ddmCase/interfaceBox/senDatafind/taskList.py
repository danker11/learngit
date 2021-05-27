# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/4/20
# filename:taskList


import requests
from public.common.filePath import filePath
from public.common.getExcelContent import GetExcelConetnt
from public.common.timeStamp import TimeStamp
from public.common.do_log import logOutput
import traceback
from interfaceBox.login.login import Login

'''
敏感数据发现列表模块

任务列表接口
启动任务接口

'''


class TaskList:


    def __init__(self,token):
        self.token = token
        requests.packages.urllib3.disable_warnings()

    def taskList(self, indata):
        '''
        获取敏感数据发现列表接口
        :param indata: 传入参数，"type":"MySql"
        :param code:code值为true/false
        :return:默认返回接口状态，code==false时返回列表数据
        '''
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_senDataFind_Path() + '/敏感数据发现任务列表查询接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=base_url, headers=header, params=param_data, verify=False)
        try:
            logOutput("info", "获取敏感数据发现任务列表接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            logOutput("error", "获取敏感数据发现任务列表接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body,r.json()))
            logOutput("error", traceback.format_exc())
            raise e

    def taskStart(self, indata):
        '''
        启动任务接口
        :param indata:传参id:任务id,整数类型
        :return:返回接口状态
        '''
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_senDataFind_Path() + '/任务启动接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, headers=header, json=param_data, verify=False)
        try:
            logOutput("info", "启动任务接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body,r.json()))
            return r.json()
        except Exception as e:
            logOutput("error", "启动任务接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body,r.json()))
            logOutput("error", traceback.format_exc())
            raise e


if __name__ == '__main__':
    token = Login().login()
    list1 = TaskList(token)
    print(list1.taskList({"type":"MySql"}))
    # print(list1.taskStart({'id':136}))