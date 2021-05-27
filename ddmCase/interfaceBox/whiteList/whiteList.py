# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/5/15
# filename:whiteList


import requests
from public.common.filePath import filePath
from public.common.getExcelContent import GetExcelConetnt
from public.common.timeStamp import TimeStamp
from public.common.do_log import logOutput
import traceback
from interfaceBox.login.login import Login

'''
规则列表白名单模块

'''


class WhiteList:
    def __init__(self,token):
        self.token = token

    def whiteAdd(self, indata):
        '''
        新增白名单接口
        :param indata: 传参assetId：规则组id字符串类型     username：数据库用户名     ipScope：IP范围，列表格式
                        fromTime：开始时间      toTime：结束时间      rules：白名单规则     dbType：数据库类型
        :return:
        '''
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_whiteList_Path() + '/白名单新增接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, headers=header, json=param_data, verify=False)
        try:
            logOutput("info", "新增白名单接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            logOutput("error", "新增白名单接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body,r.json()))
            logOutput("error", traceback.format_exc())
            raise e

    def whiteList(self, indata):
        '''
        白名单列表
        :param indata: assetId：规则组id
        :return:
        '''
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_whiteList_Path() + '/白名单列表查询接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=base_url, headers=header, params=indata, verify=False)
        try:
            logOutput("info", "白名单列表接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            logOutput("error", "白名单列表接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body,r.json()))
            logOutput("error", traceback.format_exc())
            raise e

    def whiteModify(self, indata=None):
        '''
        修改白名单
        :param indata: 传参id：白名单id   assetId：规则组id默认为空     username：数据库用户名     ipScope：IP范围，列表格式
                        fromTime：开始时间      toTime：结束时间      rules：白名单规则     dbType：数据库类型
        :return:
        '''
        if indata is None:
            indata = {"assetId": None}
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_whiteList_Path() + '/白名单修改接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, headers=header, json=indata, verify=False)
        try:
            logOutput("info", "白名单修改接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            logOutput("error", "白名单修改接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body,r.json()))
            logOutput("error", traceback.format_exc())
            raise e

    def whiteDelete(self, indata):
        '''
        删除白名单
        :param indata:传参白名单id
        :return:
        '''
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_whiteList_Path() + '/白名单删除接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=base_url, headers=header, params=indata, verify=False)
        try:
            logOutput("info", "白名单修改接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            logOutput("error", "白名单修改接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body,r.json()))
            logOutput("error", traceback.format_exc())
            raise e

if __name__ == '__main__':
    token = Login().login()
    wi = WhiteList(token)
    # indata = {"assetId":"7","username":"root","ipScope":["192.168.11.235"],"fromTime":"2021-05-17 10:03:13","toTime":"2021-05-27 10:03:16","rules":"*","dbType":"MySQL"}
    # add = wi.whiteAdd(indata)
    # listw = wi.whiteList({"assetId":"7"})
    modIndata = {"id":13,"assetId":None,"username":"root","ipScope":["192.168.11.245"],"fromTime":"2021-05-17 10:03:13","toTime":"2021-05-27 10:03:16","rules":"*","dbType":"MySQL"}
    print(wi.whiteModify(modIndata))
    print(wi.whiteDelete({"id":"13"}))
















