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
拓展规则批量操作

批量启用规则
批量禁用规则
批量删除规则


'''


class ExtRules:

    def __init__(self,token):
        self.token = token

    def extRulesEnable(self, indata):
        '''
        批量启用拓展规则接口
        :param indata: 传参：ids:传入规则的id,列表格式
        :return: 返回接口
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_extRule_Path() + '/拓展规则批量启用接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "批量启用拓展规则接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "批量启用拓展规则接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def extRulesDisable(self, indata):
        '''
        批量禁用拓展规则接口
        :param indata: 传参：ids:传入规则的id,列表格式
        :return: 返回接口
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_extRule_Path() + '/拓展规则批量禁用接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "批量禁用拓展规则接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "批量禁用拓展规则接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def extRulesDelete(self, indata):
        '''
        批量删除拓展规则接口
        :param indata: 传参：ids:传入规则的id,列表格式
        :return: 返回接口
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_extRule_Path() + '/拓展规则批量删除接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "批量删除拓展规则接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "批量删除拓展规则接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e


if __name__ == '__main__':
    rules = ExtRules(Login().login())
    # print(rules.extRulesEnable({"ids":[154]}))
    # print(rules.extRulesDisable({"ids": [154]}))
    print(rules.extRulesDelete({"ids": [154]}))

