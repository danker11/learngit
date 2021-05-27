# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/4/29
# filename:maskRuleGroup


import requests
from public.common.filePath import filePath
from public.common.getExcelContent import GetExcelConetnt
from public.common.timeStamp import TimeStamp
from public.common import do_log
from interfaceBox.login.login import Login
import traceback

'''
拓展规则组相关操作接口

拓展规则组列表
拓展规则组启动
拓展规则组禁用
'''


class ExtRuleGroup:

    def __init__(self, token):
        self.token = token

    def extRuleGroupList(self, indata):
        '''
        拓展规则组列表获取接口
        :param indata: 接口传参type:数据库类型,字符串类型
        :return:返回json
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_extRule_Path() + '/拓展规则组列表接口.xlsx',)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "获取拓展规则组接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "获取拓展规则组接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def extRuleGroupEnable(self, indata):
        '''
        拓展规则组启用接口
        :param indata:传参id:规则组id，字符串类型
        :return:返回接口json
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_extRule_Path() + '/拓展规则组启用接口.xlsx', )
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "启用拓展规则组接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "启用拓展规则组接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def extRuleGroupDisable(self, indata):
        '''
        拓展规则组禁用接口
        :param indata:传参id:规则组id，字符串类型
        :return:返回接口json
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_extRule_Path() + '/拓展规则组禁用接口.xlsx', )
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "禁用拓展规则组接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "禁用拓展规则组接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e


if __name__ == '__main__':
    extR = ExtRuleGroup(Login().login())
    print(extR.extRuleGroupList({"type":"MySQL"}))
    # print(extR.extRuleGroupEnable({'id':'7'}))
    # print(extR.extRuleGroupDisable({'id':'7'}))
