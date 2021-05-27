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

'''
脱敏规则单个操作

获取规则列表/搜索
单个规则新增
    规则新增时有以下接口：
        
单个规则编辑
单个规则删除
单个规则启用
单个规则禁用


'''


class MaskRule:
    def __init__(self, token):
        self.token = token

    def maskRuleList(self, indata=None):
        """
        脱敏规则列表展示，脱敏规则搜索
        :param indata: 传参：
                groupId:规则组id，字符串类型
                dataTypes:数据类型，列表格式，默认为空
                pageNo:第n页，默认为1
                pageSize:一页多少条数据，默认50条
                enabled:是否启用，默认全部all
                kwargs:方便其他参数写入，例如规则名称name
        :return: 返回json
        """
        if indata is None:
            indata = {"dataTypes": [], "pageNo": 1, "pageSize": 50, "enabled": "all"}
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/脱敏规则列表查询接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "获取规则列表接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "获取规则列表接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def addDataTypeALL(self, indata):
        '''
        单个规则添加获取数据类型接口
        :param indata: 传参，数据库类型，type，例如{'type':'MySQL'}
        :return:
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/单个规则添加获取数据类型接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=base_url, params=indata, headers=header, verify=False)
        try:
            do_log.logOutput("info", "添加规则时获取数据类型接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "添加规则时获取数据类型接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def addDbSource(self, indata):
        '''
        单个规则添加获取资产信息接口
        :param indata: 传参规则组id，groupId，例如{'groupId':'10'}
        :return:
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/单个规则添加获取资产信息接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=base_url, params=indata, headers=header, verify=False)
        try:
            do_log.logOutput("info", "添加规则时获取资产信息接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "添加规则时获取资产信息接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def addGetSchema(self, indata):
        '''
        单个规则添加获取schema接口
        :param indata: 传参name:数据源名称，type:数据库类型
        :return:
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/单个规则添加获取模式接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=base_url, params=indata, headers=header, verify=False)
        try:
            do_log.logOutput("info", "单个规则添加获取模式接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "单个规则添加获取模式接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def addGetTable(self, indata):
        '''
        单个规则添加获取表名接口
        :param indata: 传参name:数据源名称，type:数据库类型,schemaName:
        :return:
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/单个规则添加获取表名接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=base_url, params=indata, headers=header, verify=False)
        try:
            do_log.logOutput("info", "单个规则添加获取表名接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "单个规则添加获取表名接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def addGetColumn(self, indata):
        '''
        单个规则添加获取列名接口
        :param indata: 传参name:数据源名称，type:数据库类型,schemaName,tableName
        :return:
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/单个规则添加获取列名接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=base_url, params=indata, headers=header, verify=False)
        try:
            do_log.logOutput("info", "单个规则添加获取列名接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "单个规则添加获取列名接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def addGetAlgorithm(self, indata):
        '''
        单个规则添加获取脱敏算法接口
        :param indata: 传参:type:数据库类型,dataType:数据类型
        :return:
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/单个规则添加获取脱敏算法接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=base_url, params=indata, headers=header, verify=False)
        try:
            do_log.logOutput("info", "单个规则添加获取脱敏算法接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "单个规则添加获取脱敏算法接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def maskRuleAdd(self, indata):
        '''
        单个规则添加
        :param indata:传参，全是字符串类型
                name：规则名称   groupId：规则组id   databaseName：数据资产名称
                schemaName：库名   tableName：表名    colName：字段名
                dataType：数据类型   template：脱敏算法
        :return:返回接口json
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/脱敏规则手动新增接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "脱敏规则手动新增接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "脱敏规则手动新增接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def maskRuleModify(self, indata):
        '''
        单个规则编辑
        :param indata:传参，全是字符串类型
                id：规则id    name：规则名称   groupId：规则组id   databaseName：数据资产名称
                schemaName：库名   tableName：表名    colName：字段名
                dataType：数据类型   template：脱敏算法
        :return:返回接口json
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/脱敏规则单条编辑接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, json=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "脱敏规则单条编辑接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "脱敏规则单条编辑接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def maskRuleEnable(self, indata):
        '''
        单个规则启用
        :param indata:传参id:规则id,字符串类型
        :return:返回接口状态
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/脱敏规则单条启用接口.xlsx', 1)
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

    def maskRuleDisable(self, indata):
        '''
        单个规则禁用
        :param indata:传参id规则id，字符串类型
        :return:返回接口状态
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/脱敏规则单条禁用接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, data=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "单个规则禁用接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "单个规则禁用接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def maskRuleDelete(self, indata):
        '''
        单个规则删除
        :param indata:传参id规则id，字符串类型
        :return:返回接口json
        '''
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_maskRule_Path() + '/脱敏规则单条删除接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, data=param_data, headers=header, verify=False)
        try:
            do_log.logOutput("info", "单个规则删除接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            do_log.logOutput("error", "单个规则删除接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e


if __name__ == '__main__':
    mlist = MaskRule(Login().login())
    # print(mlist.maskRuleList({'groupId': '178', 'securityGroupId': '178'}))
    # print(mlist.maskRuleEnable({'id':'1369'}))
    # print(mlist.maskRuleDisable({'id': '1369'}))
    # print(mlist.maskRuleDelete({'id': '1369'}))
    adddata = {"name":"手机号",
              "groupId":"31",
              "databaseName":"mysql库-自动化测试",
              "schemaName":"auto",
              "tableName":"auto_table",
              "colName":"tel",
              "dataType":"手机号","template":"全遮蔽"}
    adddata.update({'id':'214'})
    print(adddata)
    # moddata = {"id": 1375, "name": "编辑", "groupId": "136", "databaseName": "name", "schemaName": "test13", "tableName": "T1W",
    #  "colName": "COL1", "dataType": "字符串", "template": "置空"}
    # print(mlist.maskRuleAdd(adddata))
    print(mlist.maskRuleModify(adddata))

    # 添加规则时获取相关配置
    # mlist.addDataTypeALL({'type':'MySQL'}) # 获取数据类型
    # mlist.addDbSource({'groupId':'10'})  # 获取资产信息
    # mlist.addGetSchema({'name':'192.168.10.251','type':'MySQL'})  #获取所有数据库
    # mlist.addGetTable({'name':'192.168.10.251','type':'MySQL','schemaName':'auto'})
    # mlist.addGetColumn({'name':'192.168.10.251','type':'MySQL',
    #                     'schemaName':'auto','tableName':'auto_table'})
    # mlist.addGetAlgorithm({'type':'MySQL','dataType':'手机号'})


