# !/usr/bin/python3
# -*- coding: utf-8 -*-


import requests
from public.common.getExcelContent import GetExcelConetnt
from public.common.timeStamp import TimeStamp
from public.common.filePath import filePath
from public.common.encrypt import encrypt
from interfaceBox.login.login import Login
from public.common import do_log
import traceback

'''
数据源模块接口封装

添加数据源接口
搜索数据源接口
修改数据源接口
删除数据源接口
'''


class Database:

    def __init__(self, token):
        self.token = token

    def databaseAdd(self, indata):
        '''
        数据源新增接口
        :param indata: 传参
        :return: 返回接口状态
        '''
        # 获取对数据库密码加密的秘钥
        login = Login()
        randomId, randomCode = login.randomCode()
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_datasourceManage_Path() + '/数据源列表添加接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        param_data.update(indata)
        param_data.update({'passWord': encrypt(param_data['passWord'], randomCode),
                           'randomId': randomId})
        header.update({"token": self.token})
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, data=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info","新增数据源接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "新增数据源接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def databaseList(self, indata=None):
        '''
        数据源列表搜索接口
        :param indata: 传参
        :param code: 1返回第一条数据源的id与name,2返回接口状态，3返回全部接口内容
        :return:
        '''
        if indata is None:
            indata = {"page": 0, "size": 100}
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_datasourceManage_Path() + '/数据源列表查询接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info","查询数据源接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "查询数据源接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def databaseModify(self, indata):
        '''
        数据源修改接口
        :param indata: 传参
        :return: 返回修改状态
        '''
        login = Login()
        randomId, randomCode = login.randomCode()
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_datasourceManage_Path() + '/数据源列表修改接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        param_data.update(indata)
        param_data.update({'passWord': encrypt(param_data['passWord'], randomCode),
                           'randomId': randomId})
        header.update({"token": self.token})
        r = requests.post(url=base_url, data=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "修改数据源接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "修改数据源接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def databaseDelete(self, indata):
        '''
        删除数据源接口
        :param indata: 传参：name（必填项），type（必填项）
        :return: 返回接口状态
        '''
        login = Login()
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_datasourceManage_Path() + '/数据源列表删除接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        param_data.update(indata)
        header.update({"token": login.login()})
        r = requests.post(url=base_url, data=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "删除数据源接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "删除数据源接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def databaseConnect(self, indata):
        '''
        数据源测试连接接口
        :param indata: 传参：name（必填项）
        :return: 返回接口状态
        '''
        login = Login()
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_datasourceManage_Path() + '/数据源测试连接接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        param_data.update(indata)
        header.update({"token": login.login()})
        r = requests.post(url=base_url, data=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "数据源测试连接接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "数据源测试连接接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e



if __name__ == '__main__':
    token = Login().login()
    db = Database(token=token)
    # mysqldb = {
    #     "name": 'name',
    #     "newname": 'name',
    #     'type': 'MySQL',
    #     'version': '5.6',
    #     'address': '192.168.10.251',
    #     'databasename': 'test',
    #     'port': '3306',
    #     'userName': 'root',
    #     'passWord': '123456',
    #     'proxyPort': '13900',
    # }
    # add = db.databaseAdd(indata=mysqldb)
    # print(add)
    # print(db.databaseList(indata={"dbType":"MySql"}))
    # print(db.databaseDelete({'name':'name','type':'MySql'}))
    print(db.databaseConnect({"name":"mysql库-自动化测试","type":"MySQL"}))
