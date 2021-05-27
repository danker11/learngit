# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/4/29
# filename:testMaskRules


import pytest
import os
import allure
from time import sleep
from interfaceBox.maskRule.maskRules import MaskRules
from interfaceBox.maskRule.maskRuleGroup import MaskRuleGroup
from interfaceBox.maskRule.maskRule import MaskRule
from interfaceBox.login.login import Login
from public.DataBase.dbMysql import DbMysql
from testCase.testMysql.mysqlTestConfig import databaseName
from public.common.rulesLoadCheck import rulesLoadCheck
from public.common import do_log
import traceback

databaseName = databaseName  # 可重新传参，方便单个模块测试


@allure.epic('mysql数据库流程测试')
@allure.feature('脱敏规则模块测试')
class TestMaskRules:
    token = Login().login()
    rules = MaskRules(token)
    rule = MaskRule(token)
    ruleGroup = MaskRuleGroup(token)
    db = DbMysql()
    ruleGroupId = None  # 规则组id
    ruleIds = []  # 规则id列表

    @allure.title("查看规则组列表测试")
    def testRuleGroupList(self):
        global ruleGroupId
        rulesG = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
        try:
            assert rulesG['status'] == 0
            assert rulesG['data'][0]['databaseName'] == databaseName
            ruleGroupId = rulesG['data'][0]['id']  # 取出规则组id，字符串类型
            do_log.logOutput("info", "查看规则组列表测试通过")
        except Exception as e:
            do_log.logOutput("error", "查看规则组列表测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("查看规则列表测试")
    def testRulesList(self):
        ruleList = self.rule.maskRuleList({'groupId': ruleGroupId, 'securityGroupId': ruleGroupId})
        try:
            assert ruleList['status'] == 0
            assert ruleList['data']['data'] == []
            do_log.logOutput("info", "查看规则列表测试通过")
        except Exception as e:
            do_log.logOutput("error", "查看规则列表测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("批量创建规则测试")
    def testRulesAdd(self):
        global ruleIds
        rulesAdd = self.rules.maskRulesCreat({"checkIds": "40", "dbType": "MySQL", "name": databaseName})
        try:
            # 1.校验接口返回状态
            assert rulesAdd['status'] == 0
            # 2.校验规则组创建规则的数量
            sleep(1)
            rulesG = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
            assert rulesG['data'][0]['ruleNum'] == 2
            # 3.校验规则列表的信息('粗略校验')
            ruleList = self.rule.maskRuleList({'groupId': ruleGroupId, 'securityGroupId': ruleGroupId})
            assert ruleList['data']['data'][1]['enabled'] is False
            for ruleId in ruleList['data']['data']:
                self.ruleIds.append(ruleId['id'])  # 规则列表，数字类型
            # 4.规则未启用，检测是否脱敏
            re = rulesLoadCheck(self.db, 'select name from auto.auto_table', '张三', 0, 0)
            assert re is True
            do_log.logOutput("info", "批量创建规则通过")
        except Exception as e:
            do_log.logOutput("error", "批量创建规则未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    # @pytest.mark.skip('跳过')
    @allure.title("批量启用规则测试")
    def testRulesEnable(self):
        rulesEnable = self.rules.maskRulesEnable({"ids": self.ruleIds})
        try:
            # 1.校验接口返回状态
            assert rulesEnable['status'] == 0
            # 2.校验规则组启用规则的数量
            sleep(1)
            rulesG = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
            assert rulesG['data'][0]['enabledRuleNum'] == 2
            # 3.校验规则列表的信息('粗略校验')
            ruleList = self.rule.maskRuleList({'groupId': ruleGroupId, 'securityGroupId': ruleGroupId})
            assert ruleList['data']['data'][0]['enabled'] is True
            assert ruleList['data']['data'][1]['enabled'] is True
            # 4.规则未启用，检测是否脱敏
            re = rulesLoadCheck(self.db, 'select name from auto.auto_table', '张*',0,0)
            assert re is True
            assert rulesLoadCheck(self.db, 'select name from auto.auto_table_copy', '张*', 0, 0) is True
            do_log.logOutput("info", "批量启用规则通过")
        except Exception as e:
            do_log.logOutput("error", "批量启用规则未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    # @pytest.mark.skip('跳过')
    @allure.title("禁用规则组测试")
    def testRuleGroupDisable(self):
        groupDis = self.ruleGroup.maskRuleGroupDisable({"id": ruleGroupId})
        try:
            # 1.校验接口返回状态
            assert groupDis['status'] == 0
            # 2.校验规则组启用状态
            sleep(1)
            rulesG = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
            assert rulesG['data'][0]['enable'] == "0"
            # 3.规则组禁用，检测是否脱敏
            assert rulesLoadCheck(self.db, 'select name from auto.auto_table', '张三', 0, 0) is True
            for name in self.db.query("select name from auto.auto_table;"):
                assert "*" not in name[0]
            do_log.logOutput("info", "禁用规则组测试通过")
        except Exception as e:
            do_log.logOutput("error", "禁用规则组测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    # @pytest.mark.skip('跳过')
    @allure.title("启用规则组测试")
    def testRuleGroupEnable(self):
        groupEn = self.ruleGroup.maskRuleGroupEnable({"id": ruleGroupId})
        try:
            # 1.校验接口返回状态
            assert groupEn['status'] == 0
            # 2.校验规则组启用状态
            sleep(1)
            rulesG = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
            assert rulesG['data'][0]['enable'] == "1"
            # 3.规则组禁用，检测是否脱敏
            assert rulesLoadCheck(self.db, 'select name from auto.auto_table', '张*', 0, 0) is True
            for name in self.db.query("select name from auto.auto_table;"):
                assert "*" in name[0]
            do_log.logOutput("info", "启用规则组测试通过")
        except Exception as e:
            do_log.logOutput("error", "启用规则组测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    # @pytest.mark.skip('跳过')
    @allure.title("批量禁用规则测试")
    def testRulesDisable(self):
        rulesDisable = self.rules.maskRulesDisable({"ids": self.ruleIds})
        try:
            # 1.校验接口返回状态
            assert rulesDisable['status'] == 0
            # 2.校验规则组启用规则的数量
            sleep(1)
            rulesG = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
            assert rulesG['data'][0]['ruleNum'] == 2
            assert rulesG['data'][0]['enabledRuleNum'] == 0
            # 3.校验规则列表的信息('粗略校验')
            ruleList = self.rule.maskRuleList({'groupId': ruleGroupId, 'securityGroupId': ruleGroupId})
            assert ruleList['data']['data'][0]['enabled'] is False
            assert ruleList['data']['data'][1]['enabled'] is False
            # 4.规则未启用，检测是否脱敏
            assert rulesLoadCheck(self.db, 'select name from auto.auto_table', '张三', 0, 0) is True
            assert rulesLoadCheck(self.db, 'select name from auto.auto_table_copy', '张三', 0, 0) is True
            do_log.logOutput("info", "批量禁用规则通过")
        except Exception as e:
            do_log.logOutput("error", "批量禁用规则未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    # @pytest.mark.skip('跳过')
    @allure.title("批量删除规则测试")
    def testRulesDelete(self):
        rulesDelete = self.rules.maskRulesDelete({"ids": self.ruleIds})
        try:
            # 1.校验接口返回状态
            assert rulesDelete['status'] == 0
            # 2.校验规则组启用规则的数量
            sleep(1)
            rulesG = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
            assert rulesG['data'][0]['ruleNum'] == 0
            assert rulesG['data'][0]['enabledRuleNum'] == 0
            # 3.校验规则列表的信息
            ruleList = self.rule.maskRuleList({'groupId': ruleGroupId, 'securityGroupId': ruleGroupId})
            assert ruleList['data']['data'] == []
            # 4.规则未启用，检测是否脱敏
            assert rulesLoadCheck(self.db, 'select name from auto.auto_table', '张三', 0, 0) is True
            assert rulesLoadCheck(self.db, 'select name from auto.auto_table_copy', '张三', 0, 0) is True
            self.db.close()
            do_log.logOutput("info", "批量删除规则通过")
        except Exception as e:
            do_log.logOutput("error", "批量删除规则未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e


if __name__ == '__main__':
    pytest.main(['testMaskRules.py', '-s'])
