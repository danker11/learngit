# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/5/22
# filename:testExtRuleSQL


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
import traceback


@allure.epic('mysql数据库流程测试')
@allure.feature('拓展规则测试')
class TestExtRuleSQL:
    token = Login().login()
    ext = ExtRule(token)
    extGroup = ExtRuleGroup(token)
    extGId = None
    conn = DbMysql()

    @allure.title('获取拓展规则组列表测试')
    def testExtGroupList(self):
        global extGId
        extG = self.extGroup.extRuleGroupList({"type": "MySQL"})
        try:
            assert extG['status'] == 0
            extGId = extG['data'][0]['id']
            do_log.logOutput("info","获取拓展规则组列表测试通过")
        except Exception as e:
            do_log.logOutput("error", "获取拓展规则组列表测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('启用拓展规则组测试')
    def testExtGroupEnable(self):
        extGE = self.extGroup.extRuleGroupEnable({"id":extGId})
        try:
            assert extGE['status'] == 0
            extGL = self.extGroup.extRuleGroupList({"type": "MySQL"})
            assert extGL['data'][0]['enable'] == "1"
            do_log.logOutput("info","启用拓展规则组测试通过")
        except Exception as e:
            do_log.logOutput("error", "启用拓展规则组测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('新增拓展规则_表名_替换表名测试')
    def testExtRuleAdd1(self):
        add = self.ext.extRuleAdd({"groupId":extGId},1)
        try:
            # 1.断言接口状态
            assert add['status'] == 0
            # 2.断言拓展规则列表
            assert self.ext.extRuleList({"groupId":extGId})['data'][0]['name'] == "表名-替换表名"
            # 3.断言拓展规则组
            extG = self.extGroup.extRuleGroupList({"type": "MySQL"})
            assert extG['data'][0]['ruleNum'] == 1 and extG['data'][0]['enabledRuleNum'] == 1
            # 4.断言SQL语句
            assert rulesLoadCheck(self.conn,'select * from test1','张*') is True
            do_log.logOutput("info","拓展规则_表名_替换表名测试通过")
        except Exception as e:
            do_log.logOutput("error","拓展规则_表名_替换表名测试未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title('新增拓展规则_表名-搜索并替换字符串测试')
    def testExtRuleAdd2(self):
        add = self.ext.extRuleAdd({"groupId":extGId},2)
        try:
            assert add['status'] == 0
            assert rulesLoadCheck(self.conn,'select tel from auto_table','张*',0,0) is True
            do_log.logOutput("info","拓展规则_表名_搜索并替换字符串测试通过")
        except Exception as e:
            do_log.logOutput("error","拓展规则_表名_搜索并替换字符串测试未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title('新增拓展规则_表名-替换SQL测试')
    def testExtRuleAdd3(self):
        add = self.ext.extRuleAdd({"groupId":extGId},3)
        try:
            assert add['status'] == 0
            assert rulesLoadCheck(self.conn,'select * from test2','张*',0,1) is True
            do_log.logOutput("info","拓展规则_表名-替换SQL测试通过")
        except Exception as e:
            do_log.logOutput("error","拓展规则_表名-替换SQL测试未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title('新增拓展规则_表名-阻断测试')
    def testExtRuleAdd4(self):
        add = self.ext.extRuleAdd({"groupId":extGId},4)
        try:
            assert add['status'] == 0
            sleep(2)
            try:
                self.conn.query('select * from auto_table_copy')
                result = False
            except:
                result = True
            assert result is True
            do_log.logOutput("info","拓展规则_表名-阻断测试通过")
        except Exception as e:
            do_log.logOutput("error","拓展规则_表名-阻断测试未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title('新增拓展规则_字符串_替换表名测试')
    def testExtRuleAdd5(self):
        add = self.ext.extRuleAdd({"groupId": extGId}, 5)
        try:
            assert add['status'] == 0
            assert rulesLoadCheck(self.conn, 'select name from test3', '张*',0,0) is True
            do_log.logOutput("info", "拓展规则_字符串_替换表名测试通过")
        except Exception as e:
            do_log.logOutput("error", "拓展规则_字符串_替换表名测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('新增拓展规则_字符串-搜索并替换字符串测试')
    def testExtRuleAdd6(self):
        add = self.ext.extRuleAdd({"groupId": extGId}, 6)
        try:
            assert add['status'] == 0
            assert rulesLoadCheck(self.conn, 'select email from auto_table', '张*', 0, 0) is True
            do_log.logOutput("info", "拓展规则_字符串_搜索并替换字符串测试通过")
        except Exception as e:
            do_log.logOutput("error", "拓展规则_字符串_搜索并替换字符串测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('新增拓展规则_字符串-替换SQL测试')
    def testExtRuleAdd7(self):
        add = self.ext.extRuleAdd({"groupId": extGId}, 7)
        try:
            assert add['status'] == 0
            assert rulesLoadCheck(self.conn, 'select test4 from aaa', '张*', 0, 1) is True
            do_log.logOutput("info", "拓展规则_字符串-替换SQL测试通过")
        except Exception as e:
            do_log.logOutput("error", "拓展规则_字符串-替换SQL测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('新增拓展规则_字符串-阻断测试')
    def testExtRuleAdd8(self):
        add = self.ext.extRuleAdd({"groupId": extGId}, 8)
        try:
            assert add['status'] == 0
            sleep(2)
            try:
                self.conn.query('delete from auto_table_copy_mask')
                result = False
            except:
                result = True
            assert result is True
            do_log.logOutput("info", "拓展规则_字符串-阻断测试通过")
        except Exception as e:
            do_log.logOutput("error", "拓展规则_字符串-阻断测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('新增拓展规则_时间段_替换表名测试')
    def testExtRuleAdd9(self):
        add = self.ext.extRuleAdd({"groupId": extGId}, 9,str(TimeStamp().timeMinute(3,2)),str(TimeStamp().timeMinute(2,2)))
        try:
            assert add['status'] == 0
            assert rulesLoadCheck(self.conn, 'select * from test7', '张*',0,1) is True
            do_log.logOutput("info", "拓展规则_时间段_替换表名测试通过")
        except Exception as e:
            do_log.logOutput("error", "拓展规则_时间段_替换表名测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('新增拓展规则_时间段-搜索并替换字符串测试')
    def testExtRuleAdd10(self):
        add = self.ext.extRuleAdd({"groupId": extGId}, 10,str(TimeStamp().timeMinute(3,2)),str(TimeStamp().timeMinute(2,2)))
        try:
            assert add['status'] == 0
            assert rulesLoadCheck(self.conn, 'select car_number from auto_table', '张*', 0, 0) is True
            do_log.logOutput("info", "拓展规则_时间段_搜索并替换字符串测试通过")
        except Exception as e:
            do_log.logOutput("error", "拓展规则_时间段_搜索并替换字符串测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('新增拓展规则_时间段-替换SQL测试')
    def testExtRuleAdd11(self):
        add = self.ext.extRuleAdd({"groupId": extGId}, 11,str(TimeStamp().timeMinute(3,2)),str(TimeStamp().timeMinute(2,2)))
        try:
            assert add['status'] == 0
            assert rulesLoadCheck(self.conn, 'select * from bbb', '张*', 0, 1) is True
            do_log.logOutput("info", "拓展规则_时间段-替换SQL测试通过")
        except Exception as e:
            do_log.logOutput("error", "拓展规则_时间段-替换SQL测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('新增拓展规则_时间段-阻断测试')
    def testExtRuleAdd12(self):
        add = self.ext.extRuleAdd({"groupId": extGId}, 12,str(TimeStamp().timeMinute(3,2)),str(TimeStamp().timeMinute(2,2)))
        try:
            assert add['status'] == 0
            sleep(2)
            try:
                DbMysql()
                result = False
            except:
                result = True
            assert result is True
            do_log.logOutput("info", "拓展规则_时间段-阻断测试通过")
        except Exception as e:
            do_log.logOutput("error", "拓展规则_时间段-阻断测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title('禁用拓展规则组测试')
    def testExtGroupDisable(self):
        extGD = self.extGroup.extRuleGroupDisable({"id":extGId})
        try:
            assert extGD['status'] == 0
            extGL = self.extGroup.extRuleGroupList({"type": "MySQL"})
            assert extGL['data'][0]['enable'] == "0"
            assert rulesLoadCheck(self.conn, 'select * from auto_table', '张*', 0, 1) is True
            self.conn.close()
            do_log.logOutput("info","禁用拓展规则组测试通过")
        except Exception as e:
            do_log.logOutput("error", "禁用拓展规则组测试未通过")
            do_log.logOutput("error", traceback.format_exc())
            self.conn.close()
            raise e


if __name__ == '__main__':
    pytest.main(['testExtRuleSQL.py', '-s'])















