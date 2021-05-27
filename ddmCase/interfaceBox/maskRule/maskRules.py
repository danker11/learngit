# !/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from public.common.filePath import filePath
from public.common.getExcelContent import GetExcelConetnt
from public.common.timeStamp import TimeStamp
from public.common import do_log
from interfaceBox.login.login import Login
import traceback

'''
脱敏规则批量操作

批量创建脱敏规则接口--调用页面：在敏感数据发现页面批量创建脱敏规则
批量启用规则
批量禁用规则
批量删除规则


'''


class MaskRules:
    requests.packages.urllib3.disable_warnings()

    def __init__(self,token):
        self.token = token

    def maskRulesCreat(self, indata):
        '''
        规则批量创建
        :param indata:传参：checkIds：选择数据类型、脱敏算法   dbType:数据库类型    name:数据源名称
        :return:返回接口数据
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/批量创建脱敏规则接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "规则批量创建接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "规则批量创建接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def maskRulesEnable(self, indata):
        '''
        批量启用规则接口
        :param indata: 传参：ids:传入规则的id,列表格式
        :return: 返回接口
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/脱敏规则批量启用接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "批量启用规则接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "批量启用规则接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def maskRulesDisable(self, indata):
        '''
        批量禁用规则接口
        :param indata: 传参：ids:传入规则的id,列表格式
        :return: 返回接口
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/脱敏规则批量禁用接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "批量禁用规则接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "批量禁用规则接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def maskRulesDelete(self, indata):
        '''
        批量删除规则接口
        :param indata: 传参：ids:传入规则的id,列表格式
        :return: 返回接口
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/脱敏规则批量删除接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "批量删除规则接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "批量删除规则接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e


if __name__ == '__main__':
    rules = MaskRules(Login().login())
    # print(rules.maskRulesCreat({"checkIds":"16,136,52,28,40,4,64,88,76,628,100,112,124,652,148,640","dbType":"MySQL","name":"name"}))
    # rules.maskRulesEnable({"ids":[1351, 1354]})
    # print(rules.maskRulesDisable({"ids": [1351, 1354]}))
    print(rules.maskRulesDelete({"ids": [1351, 1354]}))

