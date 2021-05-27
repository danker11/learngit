# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/5/18
# filename:testWriteLIst



import pytest
import os
import allure
from interfaceBox.whiteList.whiteList import WhiteList
from interfaceBox.login.login import Login
from public.common import do_log
from config.config import database
from public.DataBase.dbMysql import DbMysql
from interfaceBox.maskRule.maskRuleGroup import MaskRuleGroup
from public.common.IPGet import innerIPGet
from public.common.timeStamp import TimeStamp
from public.common.rulesLoadCheck import rulesLoadCheck

import traceback


@allure.epic('mysql数据库流程测试')
@allure.feature('白名单模块测试')
class TestWritelist:
    token = Login().login()
    wi = WhiteList(token)
    ruleGroup = MaskRuleGroup(token)
    rulesG = None
    conn = DbMysql()
    writeId = None

    def setup_class(self):
        global ruleGroupId
        rulesG = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
        ruleGroupId = rulesG['data'][0]['id']  # 取出规则组id，字符串类型

    @allure.title('添加白名单测试')
    def testWriteAdd(self):
        indata = {"assetId":ruleGroupId,"username":database['mysqlDB']['userName'],"ipScope":[innerIPGet()],
                  "fromTime":TimeStamp().timeCurrent(3,1),"toTime":TimeStamp().timeCurrent(2,1),"rules":"*","dbType":"MySQL"}
        add = self.wi.whiteAdd(indata)
        try:
            assert add['status'] == 0
            do_log.logOutput("info","新增白名单通过")
        except Exception as e:
            do_log.logOutput("error","新增白名单未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("白名单列表测试")
    def testWriteList(self):
        global writeId
        wlist = self.wi.whiteList({"assetId":ruleGroupId})
        try:
            assert wlist['status'] == 0
            assert wlist['data'][0]['username'] == database['mysqlDB']['userName']
            writeId = int(wlist['data'][0]['id'])
            do_log.logOutput("info","查看白名单列表通过")
        except Exception as e:
            do_log.logOutput("error","查看白名单列表未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("规则组列表显示白名单数量测试")
    def testWriteNum(self):
        rulesG = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
        try:
            assert rulesG['status'] == 0
            assert rulesG['data'][0]['whiteListNum'] == 1
            do_log.logOutput("info","查看规则组列表显示白名单数量通过")
        except Exception as e:
            do_log.logOutput("error","查看规则组列表显示白名单数量未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("白名单是否生效测试")
    def testWriteEnAble(self):
        sql = rulesLoadCheck(self.conn, 'select name from auto.auto_table', '张三', 0, 0)
        try:
            assert sql is True
            do_log.logOutput("info","白名单是否生效用例通过")
        except Exception as e:
            do_log.logOutput("error","白名单是否生效用例未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("修改白名单测试")
    def testWriteModify(self):
        indata = {"id":writeId,"assetId":None,"username":database['mysqlDB']['userName'],"ipScope":[innerIPGet()],
                  "fromTime":TimeStamp().timeCurrent(3,1),"toTime":TimeStamp().timeCurrent(2,1),"rules":"*","dbType":"MySQL"}
        mod = self.wi.whiteModify(indata)
        try:
            assert mod['status'] == 0
            sql = rulesLoadCheck(self.conn, 'select name from auto.auto_table', '张三', 0, 0)
            assert sql is True
            do_log.logOutput("info","修改白名单通过")
        except Exception as e:
            do_log.logOutput("error","修改白名单未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("修改白名单测试-非白名单用户")
    def testWriteModify1(self):
        indata = {"id":writeId,"assetId":None,"username":TimeStamp().timeStamp(),"ipScope":[innerIPGet()],
                  "fromTime":TimeStamp().timeCurrent(3,1),"toTime":TimeStamp().timeCurrent(2,1),"rules":"*","dbType":"MySQL"}
        mod = self.wi.whiteModify(indata)
        try:
            assert mod['status'] == 0
            sql = rulesLoadCheck(self.conn, 'select name from auto.auto_table', '张*', 0, 0)
            assert sql is True
            do_log.logOutput("info","修改白名单-非白名单用户通过")
        except Exception as e:
            do_log.logOutput("error","修改白名单-非白名单用户未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("修改白名单测试-非本地IP")
    def testWriteModify2(self):
        indata = {"id":writeId,"assetId":None,"username":database['mysqlDB']['userName'],"ipScope":["10.10.10.10"],
                  "fromTime":TimeStamp().timeCurrent(3,1),"toTime":TimeStamp().timeCurrent(2,1),"rules":"*","dbType":"MySQL"}
        mod = self.wi.whiteModify(indata)
        try:
            assert mod['status'] == 0
            sql = rulesLoadCheck(self.conn, 'select name from auto.auto_table', '张*', 0, 0)
            assert sql is True
            do_log.logOutput("info","修改白名单测试-非本地IP通过")
        except Exception as e:
            do_log.logOutput("error","修改白名单测试-非本地IP未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("修改白名单测试-非白名单时间段")
    def testWriteModify3(self):
        indata = {"id":writeId,"assetId":None,"username":database['mysqlDB']['userName'],"ipScope":[innerIPGet()],
                  "fromTime":TimeStamp().timeCurrent(2,3),"toTime":TimeStamp().timeCurrent(2,5),"rules":"*","dbType":"MySQL"}
        mod = self.wi.whiteModify(indata)
        try:
            assert mod['status'] == 0
            sql = rulesLoadCheck(self.conn, 'select name from auto.auto_table', '张*', 0, 0)
            assert sql is True
            do_log.logOutput("info","修改白名单测试-非白名单时间段通过")
        except Exception as e:
            do_log.logOutput("error","修改白名单测试-非白名单时间段未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e

    @allure.title("删除白名单")
    def testWriteDelete(self):
        de = self.wi.whiteDelete({"id":writeId})
        try:
            # 1.校验接口返回状态
            assert de['status'] == 0
            # 2.校验白名单列表
            assert self.wi.whiteList({"assetId": ruleGroupId})['data'] == []
            # 3.校验规则组，显示白名单数量
            rulesG = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})
            assert rulesG['data'][0]['whiteListNum'] == 0
            # 4.校验白名单是否已失效
            sql = rulesLoadCheck(self.conn, 'select name from auto.auto_table', '张*', 0, 0)
            assert sql is True
            do_log.logOutput("info","删除白名单通过")
        except Exception as e:
            do_log.logOutput("error","删除白名单未通过")
            do_log.logOutput("error",traceback.format_exc())
            raise e


if __name__ == '__main__':
    pytest.main(['testWriteLIst.py', '-s'])


