# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/5/10
# filename:testMaskRule

import pytest
import os
import allure
from time import sleep
from interfaceBox.maskRule.maskRules import MaskRules
from interfaceBox.maskRule.maskRuleGroup import MaskRuleGroup
from interfaceBox.maskRule.maskRule import MaskRule
from interfaceBox.login.login import Login
from public.DataBase.dbMysql import DbMysql
from testCase.testMysql.mysqlTestConfig import databaseName, dataTypes2, tableAll
from public.common.rulesLoadCheck import rulesLoadCheck
from public.common import do_log
import traceback

databaseName = databaseName  # 可重新传参，方便单个模块测试


@allure.epic('mysql数据库流程测试')
@allure.feature('脱敏规则模块测试')
class TestMaskRule:
    token = Login().login()
    rules = MaskRules(token)
    rule = MaskRule(token)
    ruleGroup = MaskRuleGroup(token)
    db = DbMysql()
    ruleGroupId = None  # 规则组id
    ruleID = None  # 规则id
    adddata = None  # 新增规则字典

    def setup_class(self):
        global ruleGroupId
        rulesG = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
        try:
            ruleGroupId = rulesG['data'][0]['id']  # 取出规则组id，字符串类型
            do_log.logOutput("info", "用例前置操作正常，获取规则组id")
        except Exception as e:
            do_log.logOutput("error", "用例前置操作异常")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("创建单个规则获取数据类型接口测试")
    def testAddDataTypeALL(self):
        dataTy = self.rule.addDataTypeALL({'type': 'MySQL'})
        try:
            assert dataTy['status'] == 0
            assert dataTy['data'] == dataTypes2
            do_log.logOutput("info", "创建规则获取数据类型接口测试通过")
        except Exception as e:
            do_log.logOutput("error", "创建规则获取数据类型接口测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("创建单个规则获取资产名称接口测试")
    def testAddDbSource(self):
        sourceNa = self.rule.addDbSource({'groupId': ruleGroupId})
        try:
            assert sourceNa['status'] == 0
            assert sourceNa['data']['name'] == databaseName
            do_log.logOutput("info", "创建规则获取资产名称接口测试通过")
        except Exception as e:
            do_log.logOutput("error", "创建规则获取资产名称接口测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("创建单个规则获取schema接口测试")
    def testAddGetSchema(self):
        schemaAll = self.rule.addGetSchema({'name': databaseName, 'type': 'MySQL'})
        try:
            assert schemaAll['status'] == 0
            assert set(schemaAll['data']) == set(tableAll("show databases;"))
            do_log.logOutput("info", "创建规则获取schema接口测试通过")
        except Exception as e:
            do_log.logOutput("error", "创建规则获取schema接口测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("创建单个规则获取表名接口测试")
    def testAddGetTable(self):
        tableA = self.rule.addGetTable({'name': databaseName, 'type': 'MySQL', 'schemaName': 'auto'})
        try:
            assert tableA['status'] == 0
            assert set(tableA['data']) == set(tableAll(
                "select table_name from information_schema.tables where TABLE_SCHEMA = 'auto';"))
            do_log.logOutput("info", "创建规则获取表名接口测试通过")
        except Exception as e:
            do_log.logOutput("error", "创建规则获取表名接口测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("创建单个规则获取列名接口测试")
    def testAddGetColumn(self):
        columnA = self.rule.addGetColumn({'name': databaseName, 'type': 'MySQL',
                                          'schemaName': 'auto', 'tableName': 'auto_table'})
        try:
            assert columnA['status'] == 0
            assert set(columnA['data']) == set(tableAll("SELECT COLUMN_NAME FROM information_schema.COLUMNS "
                                               "WHERE TABLE_SCHEMA = 'auto' AND TABLE_NAME = 'auto_table';"))
            do_log.logOutput("info", "创建规则获取列名接口测试通过")
        except Exception as e:
            do_log.logOutput("error", "创建规则获取列名接口测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("创建单个规则获取脱敏算法接口测试")
    def testAddGetAlgorithm(self):
        algorithm = self.rule.addGetAlgorithm({'type': 'MySQL', 'dataType': '手机号'})
        try:
            assert algorithm['status'] == 0
            algorithmALL = ['部分遮蔽', '置空', '全遮蔽']
            for alg in algorithmALL:
                assert alg in str(algorithm)
            do_log.logOutput("info", "创建规则获取脱敏算法接口测试通过")
        except Exception as e:
            do_log.logOutput("error", "创建规则获取脱敏算法接口测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("创建单个规则测试")
    def testMaskRuleAdd(self):
        global ruleID,adddata
        adddata = {"name": "自动化测试-手动创建规则",
                   "groupId": ruleGroupId,
                   "databaseName": databaseName,
                   "schemaName": "auto",
                   "tableName": "auto_table",
                   "colName": "name",
                   "dataType": "中文姓名", "template": "全遮蔽"}
        addRule = self.rule.maskRuleAdd(adddata)
        try:
            # 1.校验接口返回状态
            assert addRule['status'] == 0
            # 2.校验规则列表
            ruleList = self.rule.maskRuleList({'groupId': ruleGroupId, 'securityGroupId': ruleGroupId})
            assert ruleList['data']['data'][0]['name'] == "自动化测试-手动创建规则"
            assert ruleList['data']['data'][0]['enabled'] == True
            ruleID = str(ruleList['data']['data'][0]['id'])
            # 3.校验规则组
            ruleGroup = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
            assert ruleGroup['data'][0]['ruleNum'] == 1
            assert ruleGroup['data'][0]['enabledRuleNum'] == 1
            # 4.校验是否脱敏
            assert rulesLoadCheck(self.db, 'select name from auto.auto_table', '**',0,0) is True
            sql = self.db.query('select name from auto.auto_table;')
            for name in sql:
                for i in name[0].split('*'):
                    assert i == ''
            do_log.logOutput("info", "创建单个规则测试通过")
        except Exception as e:
            do_log.logOutput("error", "创建单个规则测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("禁用单个规则测试")
    def testMaskRuleDisable(self):
        ruleDis = self.rule.maskRuleDisable({'id':ruleID})
        try:
            # 1.校验接口返回状态
            assert ruleDis['status'] == 0
            # 2.校验规则列表，规则状态
            ruleList = self.rule.maskRuleList({'groupId': ruleGroupId, 'securityGroupId': ruleGroupId})
            for rule in  ruleList['data']['data']:
                if rule['id'] == ruleID:
                    assert rule['enabled'] == False
            # 3.校验规则组
            ruleGroup = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
            assert ruleGroup['data'][0]['enabledRuleNum'] == 0
            # 4.校验是否脱敏
            assert rulesLoadCheck(self.db, 'select name from auto.auto_table', '张三', 0, 0) is True
            sql = self.db.query('select name from auto.auto_table;')
            for name in sql:
                assert "*" not in name[0]
            do_log.logOutput("info", "禁用单个规则测试通过")
        except Exception as e:
            do_log.logOutput("error", "禁用单个规则测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("启用单个规则测试")
    def testMaskRuleEnable(self):
        ruleEn = self.rule.maskRuleEnable({'id':ruleID})
        try:
            # 1.校验接口返回状态
            assert ruleEn['status'] == 0
            # 2.校验规则列表
            ruleList = self.rule.maskRuleList({'groupId': ruleGroupId, 'securityGroupId': ruleGroupId})
            assert ruleList['data']['data'][0]['enabled'] is True
            # 3.校验规则组
            ruleGroup = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
            assert ruleGroup['data'][0]['enabledRuleNum'] == 1
            # 4.校验是否脱敏
            assert rulesLoadCheck(self.db, 'select name from auto.auto_table', '**', 0, 0) is True
            sql = self.db.query('select name from auto.auto_table;')
            for name in sql:
                for i in name[0].split('*'):
                    assert i == ''
            do_log.logOutput("info", "启用单个规则测试通过")
        except Exception as e:
            do_log.logOutput("error", "启用单个规则测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("编辑单个规则测试")
    def testMaskRuleModify(self):
        adddata.update({'id':ruleID,"template": "置空"})
        ruleEn = self.rule.maskRuleModify(adddata)
        try:
            # 1.校验接口返回状态
            assert ruleEn['status'] == 0
            # 2.校验规则列表
            ruleList = self.rule.maskRuleList({'groupId': ruleGroupId, 'securityGroupId': ruleGroupId})
            assert ruleList['data']['data'][0]['template'] == '置空'
            # 3.校验规则组
            ruleGroup = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
            assert ruleGroup['data'][0]['enabledRuleNum'] == 1
            # 4.校验是否脱敏
            assert rulesLoadCheck(self.db, 'select name from auto.auto_table', None, 0, 0) is True
            sql = self.db.query('select name from auto.auto_table;')
            for name in sql:
                assert name[0] is None
            do_log.logOutput("info", "编辑单个规则测试通过")
        except Exception as e:
            do_log.logOutput("error", "编辑单个规则测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("删除单个规则测试")
    def testMaskRuledelete(self):
        ruleDe = self.rule.maskRuleDelete({'id':ruleID})
        try:
            # 1.校验接口返回状态
            assert ruleDe['status'] == 0
            # 2.校验规则列表
            ruleList = self.rule.maskRuleList({'groupId': ruleGroupId, 'securityGroupId': ruleGroupId})
            assert ruleList['data']['data'] == []
            # 3.校验规则组
            ruleGroup = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
            assert ruleGroup['data'][0]['ruleNum'] == 0
            # 4.校验是否脱敏
            assert rulesLoadCheck(self.db, 'select name from auto.auto_table', '张三', 0, 0) is True
            self.db.close()
            do_log.logOutput("info", "删除单个规则测试通过")
        except Exception as e:
            do_log.logOutput("error", "删除单个规则测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e


if __name__ == '__main__':
    pytest.main(['testMaskRule.py','-s'])











