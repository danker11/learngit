# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/4/29
# filename:maskRule


import requests
from public.common.filePath import filePath
from public.common.getExcelContent import GetExcelConetnt
from public.common.timeStamp import TimeStamp
from public.common import do_log
from interfaceBox.login.login import Login
import traceback
import json

'''
拓展规则单个操作

拓展规则列表
单个拓展规则新增  
单个拓展规则编辑
单个拓展规则删除
单个拓展规则启用
单个拓展规则禁用


'''

class ExtRule:
    def __init__(self, token):
        self.token = token

    def extRuleList(self, indata):
        """
        拓展规则列表展示，拓展规则搜索
        :param indata: 传参：groupId:规则组id，
        :return: 返回json
        """
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_extRule_Path() + '/拓展规则列表接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "获取拓展规则列表接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "获取拓展规则列表接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def extRuleAdd(self, indata, n, from_time=None, to_time=None):
        '''
        单个拓展规则添加
        :param indata:传参
        :return:返回接口json
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_extRule_Path() + '/拓展规则单个添加接口.xlsx', n)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        ruleInfoJson = json.loads(param_data.get('ruleInfoJson'))
        matcherInfo = ruleInfoJson.get('matcherInfo')
        matcherInfo.update({'fromTime': from_time, 'toTime': to_time})
        ruleInfoJson.update({'matcherInfo': matcherInfo})
        ruleInfoJson = json.dumps(ruleInfoJson, ensure_ascii=False)
        param_data.update({"ruleInfoJson":ruleInfoJson})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, data=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "单个拓展规则新增接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "单个拓展规则新增接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def extRuleModify(self, indata):
        '''
        单个拓展规则编辑
        :param indata:传参
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_extRule_Path() + '/拓展规则单个编辑接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "拓展规则单条编辑接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "拓展规则单条编辑接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def extRuleEnable(self, indata):
        '''
        单个拓展规则启用
        :param indata:传参id:规则id,字符串类型
        :return:返回接口状态
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_extRule_Path() + '/拓展规则单个启用接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, data=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "单个规则启用接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "单个规则启用接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def extRuleDisable(self, indata):
        '''
        单个拓展规则禁用
        :param indata:传参id规则id，字符串类型
        :return:返回接口状态
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_extRule_Path() + '/拓展规则单个禁用接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, data=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "单个拓展规则禁用接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "单个拓展规则禁用接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def extRuleDelete(self, indata):
        '''
        单个拓展规则删除
        :param indata:传参id规则id，字符串类型
        :return:返回接口json
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_extRule_Path() + '/拓展规则单个删除接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, data=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "单个拓展规则删除接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "单个拓展规则删除接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e


if __name__ == '__main__':
    mlist = ExtRule(Login().login())
    # print(mlist.extRuleDisable({"id":"157"}))
    # print(mlist.extRuleEnable({"id":"157"}))
    # print(mlist.extRuleDelete({"id":"157"}))
    print(mlist.extRuleList({"groupId":"7"})['data'])
    # print(mlist.extRuleAdd({"groupId":"7"},1))
    from public.common.timeStamp import TimeStamp

    # self.ext.extRuleList({"groupId": extGId})['data'][0]['name']
    # print(mlist.extRuleAdd({"groupId": "7"},10,str(TimeStamp().timeMinute(3,2)),str(TimeStamp().timeMinute(2,5))))
    # mod = {"id":"175","name":"表名-搜索并替换字符串","enabled":True,"matcherInfo":
    #     {"type":"表名","tableName":"auto_table"},"actionInfo":{"type":"搜索并替换字符串","searchText":"tel","replaceText":"name"},"description":""}
    # print(mlist.extRuleModify(mod))




