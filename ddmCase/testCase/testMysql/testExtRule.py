# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/5/22
# filename:testExtRule



import pytest
import os
import allure
from interfaceBox.extRule.extRuleGroup import ExtRuleGroup
from interfaceBox.extRule.extRule import ExtRule
from interfaceBox.login.login import Login
from public.common import do_log
from public.DataBase.dbMysql import DbMysql
from public.common.rulesLoadCheck import rulesLoadCheck
from time import sleep
from public.common.timeStamp import TimeStamp
from interfaceBox.extRule.extRules import ExtRules
import traceback



@allure.epic('mysql数据库流程测试')
@allure.feature('拓展规则测试')
class TestExtRuleSQL:
    token = Login().login()
    ext = ExtRule(token)
    extGroup = ExtRuleGroup(token)
    exts = ExtRules(token)
    extGId = None

    def setup_class(self):
        global extGId, Diss
        extGId = self.extGroup.extRuleGroupList({"type": "MySQL"})['data'][0]['id']
        self.extGroup.extRuleGroupEnable({"id":int(extGId)})
        dislist = []
        extlist = self.ext.extRuleList({"groupId":extGId})['data']
        for extl in extlist:
            if "时间段" in extl['name']:
                dislist.append(extl['id'])
        Diss = self.exts.extRulesDisable({'ids':dislist})

    @allure.title('拓展规则批量禁用测试')
    def testExtRulesDisable(self):
        try:
            # 1.校验接口返回状态
            assert Diss['status'] == 0
            # 2.校验列表状态
            assert self.ext.extRuleList({"groupId":extGId})['data'][0]['enabled'] is False
            # 3.校验规则组启用创建规则数量
            extG = self.extGroup.extRuleGroupList({"type": "MySQL"})['data'][0]
            assert extG['ruleNum'] == 12 and extG['enabledRuleNum'] == 8
            # 4.校验SQL是否正常
            sleep(5)
            conn = DbMysql()
            rulesLoadCheck(conn,'select * from auto_table','张*')
            do_log.logOutput("info","拓展规则批量禁用测试通过")
            conn.close()
        except Exception as e:
            do_log.logOutput("error", "拓展规则批量禁用测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('拓展规则批量启用测试')
    def testExtRulesEnable(self):
        extIdlist = []
        extlist = self.ext.extRuleList({"groupId":extGId})['data']
        for extl in extlist:
            if extl['name'] == '时间段-替换表名' or extl['name'] == '时间段-搜索并替换字符串':
                extIdlist.append(extl['id'])
        Ens = self.exts.extRulesEnable({'ids':extIdlist})
        try:
            # 1.校验接口返回状态
            assert Ens['status'] == 0
            # 2.校验列表状态
            lstatuss = self.ext.extRuleList({"groupId":extGId})['data']
            for lstatus in lstatuss:
                if lstatus['name'] == '时间段-替换表名' or lstatus['name'] == '时间段-搜索并替换字符串':
                    assert lstatus['enabled'] is True
            # 3.校验规则组启用创建规则数量
            extG = self.extGroup.extRuleGroupList({"type": "MySQL"})['data'][0]
            assert extG['ruleNum'] == 12 and extG['enabledRuleNum'] == 10
            # 4.校验SQL是否正常
            sleep(5)
            conn = DbMysql()
            assert rulesLoadCheck(conn, 'select * from test7', '张*',0,1) is True
            assert rulesLoadCheck(conn, 'select car_number from auto_table', '张*', 0, 0) is True
            do_log.logOutput("info","拓展规则批量启用测试通过")
            conn.close()
        except Exception as e:
            do_log.logOutput("error", "拓展规则批量启用测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('拓展规则批量删除测试')
    def testExtRulesDelete(self):
        extIdlist = []
        extlist = self.ext.extRuleList({"groupId":extGId})['data']
        for extl in extlist:
            if extl['name'] == '字符串-替换SQL' or extl['name'] == '字符串-搜索并替换字符串':
                extIdlist.append(extl['id'])
        delExt = self.exts.extRulesDelete({'ids':extIdlist})
        try:
            # 1.校验接口返回状态
            assert delExt['status'] == 0
            # 2.校验列表状态
            extL = str(self.ext.extRuleList({"groupId":extGId})['data'])
            assert '字符串-替换SQL' not in extL and '字符串-搜索并替换字符串' not in extL
            # 3.校验规则组启用创建规则数量
            extG = self.extGroup.extRuleGroupList({"type": "MySQL"})['data'][0]
            assert extG['ruleNum'] == 10 and extG['enabledRuleNum'] == 8
            # 4.校验SQL是否正常
            sleep(3)
            conn = DbMysql()
            assert rulesLoadCheck(conn, 'select email from auto_table', 'pmsfqmsfugfyqa53784255@sina.cn', 0, 0) is True
            conn.close()
            do_log.logOutput("info","拓展规则批量删除测试通过")
        except Exception as e:
            do_log.logOutput("error", "拓展规则批量删除测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('拓展规则禁用测试')
    def testExtDisadble(self):
        global extId
        extlist = self.ext.extRuleList({"groupId":extGId})['data']
        for extl in extlist:
            if extl['name'] == '表名-阻断':
                extId = extl['id']
        dis = self.ext.extRuleDisable({"id":extId})
        try:
            # 1.校验接口返回状态
            assert dis['status'] == 0
            # 2.校验列表状态
            extL = self.ext.extRuleList({"groupId":extGId})['data']
            for extl in extL:
                if extl['name'] == '表名-阻断':
                    assert extl['enabled'] is False
            # 3.校验规则组启用创建规则数量
            extG = self.extGroup.extRuleGroupList({"type": "MySQL"})['data'][0]
            assert extG['ruleNum'] == 10 and extG['enabledRuleNum'] == 7
            # 4.校验SQL是否正常
            conn = DbMysql()
            assert rulesLoadCheck(conn, 'select * from auto_table_copy', '张*', 0, 1) is True
            conn.close()
            do_log.logOutput("info","拓展规则禁用测试通过")
        except Exception as e:
            do_log.logOutput("error", "拓展规则禁用测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('拓展规则启用测试')
    def testExtEnadble(self):
        En = self.ext.extRuleEnable({"id": extId})
        try:
            # 1.校验接口返回状态
            assert En['status'] == 0
            # 2.校验列表状态
            sleep(1)
            extL2 = self.ext.extRuleList({"groupId": extGId})['data']
            for extl2 in extL2:
                if extl2['name'] == '表名-阻断':
                    assert extl2['enabled'] is True
            # 3.校验规则组启用创建规则数量
            extG = self.extGroup.extRuleGroupList({"type": "MySQL"})['data'][0]
            assert extG['ruleNum'] == 10 and extG['enabledRuleNum'] == 8
            # 4.校验SQL是否正常
            conn = DbMysql()
            sleep(3)
            try:
                conn.query('select * from auto_table_copy')
                result = False
            except:
                result = True
            assert result is True
            conn.close()
            do_log.logOutput("info", "拓展规则启用测试通过")
        except Exception as e:
            do_log.logOutput("error", "拓展规则启用测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('拓展规则编辑测试')
    def testExtModify(self):
        indata = {"id":extId,"name":"表名-阻断","enabled":False,"matcherInfo":
            {"type":"表名","tableName":"auto_table"},"actionInfo":{"type":"阻断"},"description":""}
        mod = self.ext.extRuleModify(indata)
        try:
            # 1.校验接口返回状态
            assert mod['status'] == 0
            # 2.校验列表状态
            extL = self.ext.extRuleList({"groupId": extGId})['data']
            for extl in extL:
                if extl['name'] == '表名-阻断':
                    assert extl['matcherInfo']['tableName'] == "auto_table"
            # 3.校验SQL是否正常
            conn = DbMysql()
            sleep(3)
            try:
                conn.query('select * from auto_table')
                result = False
            except:
                result = True
            assert result is True
            conn.close()
            do_log.logOutput("info", "拓展规则编辑测试通过")
        except Exception as e:
            do_log.logOutput("error", "拓展规则编辑测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('拓展规则删除测试')
    def testExtDelete(self):
        dele = self.ext.extRuleDelete({"id": extId})
        try:
            # 1.校验接口返回状态
            assert dele['status'] == 0
            # 2.校验列表状态
            extL = self.ext.extRuleList({"groupId": extGId})['data']
            assert '表名-阻断' not in str(extL)
            # 3.校验规则组启用创建规则数量
            extG = self.extGroup.extRuleGroupList({"type": "MySQL"})['data'][0]
            assert extG['ruleNum'] == 9 and extG['enabledRuleNum'] == 7
            # 4.校验SQL是否正常
            conn = DbMysql()
            assert rulesLoadCheck(conn,'select * from auto_table','张*') is True
            conn.close()
            do_log.logOutput("info", "拓展规则删除测试通过")
        except Exception as e:
            do_log.logOutput("error", "拓展规则删除测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e


if __name__ == '__main__':
    pytest.main(['testExtRule.py', '-s'])















