# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/5/11
# filename:testSQL


import pytest
import os
import allure
from time import sleep
from interfaceBox.maskRule.maskRuleGroup import MaskRuleGroup
from interfaceBox.maskRule.maskRule import MaskRule
from interfaceBox.login.login import Login
from public.DataBase.dbMysql import DbMysql
from public.common.rulesLoadCheck import rulesLoadCheck
from testCase.testMysql.mysqlTestConfig import databaseName
from public.common import do_log
import traceback

databaseName = databaseName  # 可重新传参，方便单个模块测试


@allure.epic('mysql数据库流程测试')
@allure.feature('SQL语法测试')
class TestMaskRule:
    token = Login().login()
    rule = MaskRule(token)
    ruleGroup = MaskRuleGroup(token)
    db = DbMysql()

    def setup_class(self):
        '''
        前置条件，需要创建 规则1:auto_table-name-中文姓名-部分遮蔽
                         规则2:auto_table_copy-name-中文姓名-部分遮蔽
                         规则3：auto_table_copy-card_id-身份证号/社保卡号/驾驶证号-部分遮蔽
        :return:
        '''
        rulesG = self.ruleGroup.maskRuleGroupList({"type": "MySQL"})['data'][0]['id']
        adddata = {"name": "自动化测试-手动创建规则",
                   "groupId": rulesG,
                   "databaseName": databaseName,
                   "schemaName": "auto",
                   "tableName": "auto_table",
                   "colName": "name",
                   "dataType": "中文姓名", "template": "部分遮蔽"}
        r1 = self.rule.maskRuleAdd(adddata)
        adddata2 = {"name": "自动化测试-手动创建规则2",
                   "groupId": rulesG,
                   "databaseName": databaseName,
                   "schemaName": "auto",
                   "tableName": "auto_table_copy",
                   "colName": "name",
                   "dataType": "中文姓名", "template": "部分遮蔽"}
        r2 = self.rule.maskRuleAdd(adddata2)
        adddata3 = {"name": "自动化测试-手动创建规则3",
                   "groupId": rulesG,
                   "databaseName": databaseName,
                   "schemaName": "auto",
                   "tableName": "auto_table_copy",
                   "colName": "card_id",
                   "dataType": "身份证号/社保卡号/驾驶证号", "template": "部分遮蔽"}
        r3 = self.rule.maskRuleAdd(adddata3)
        try:
            assert r1['status'] == 0
            assert r2['status'] == 0
            assert r3['status'] == 0
            do_log.logOutput("info", "用例前置操作正常，创建规则正常")
        except Exception as e:
            do_log.logOutput("error", "用例前置操作异常")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    @allure.title("SQL语法_select*/关键字大小写")
    def testSelect(self):
        # 持续一分钟看是否下发了规则
        re = rulesLoadCheck(self.db, 'select * from auto_table', '张*')
        assert re is True
        sql = self.db.query('SELECT* FROM auto_table')
        assert sql[0][1] == '张*'
        sql = self.db.query('SELECT *FROM auto_table limit 10')
        assert sql[0][1] == '张*'
        sql = self.db.query('SELECT*FROM auto_table limit 10')
        assert sql[0][1] == '张*'
        sql = self.db.query('SELECT * FROM auto.auto_table limit 1,10')
        assert sql[0][1] == '古**'

    @allure.title('SQL语法_select字段名测试')
    def testSqlColumn(self):
        sql = self.db.query('SELECT name FROM auto_table')
        assert sql[0][0] == '张*'
        sql = self.db.query('SELECT id,name FROM auto_table')
        assert sql[0][1] == '张*'

    @allure.title('SQL语法_库名表名列名加``测试')
    def testSymbol(self):
        sql = self.db.query('SELECT * FROM `auto_table` LIMIT 0, 1000')
        assert sql[0][1] == '张*'
        sql = self.db.query('SELECT * FROM `auto`.`auto_table` LIMIT 0, 1000')
        assert sql[0][1] == '张*'
        sql = self.db.query('SELECT * FROM `auto`.auto_table LIMIT 0, 1000')
        assert sql[0][1] == '张*'
        sql = self.db.query('SELECT * FROM auto.`auto_table` LIMIT 0, 1000')
        assert sql[0][1] == '张*'
        sql = self.db.query('SELECT id,name FROM auto_table limit 10')
        assert sql[0][1] == '张*'
        sql = self.db.query('SELECT `id`,`name` FROM auto_table limit 10')
        assert sql[0][1] == '张*'


    @allure.title('SQL语法_all测试')
    def testAll(self):
        sql = self.db.query("select ALL id,name from auto_table")
        assert sql[0][1] == '张*'

    @allure.title('SQL语法_distinct/distinctrow测试')
    def testDISTINCT(self):
        sql = self.db.query("select DISTINCT id,name from auto_table")
        assert sql[0][1] == '张*'
        sql = self.db.query("select DISTINCTROW id,name from auto_table")
        assert sql[0][1] == '张*'


    @allure.title('SQL语法_HIGH_PRIORITY/STRAIGHT_JOIN等语法测试')
    def testOther(self):
        sql = self.db.query("SELECT HIGH_PRIORITY id,name FROM auto_table")
        assert sql[0][1] == '张*'
        sql = self.db.query("SELECT STRAIGHT_JOIN id,name FROM auto_table")
        assert sql[0][1] == '张*'
        sql = self.db.query("SELECT SQL_SMALL_RESULT id,name FROM auto_table")
        assert sql[0][1] == '张*'
        sql = self.db.query("SELECT SQL_BIG_RESULT id,name FROM auto_table")
        assert sql[0][1] == '张*'
        sql = self.db.query("SELECT SQL_BUFFER_RESULT id,name FROM auto_table")
        assert sql[0][1] == '张*'
        sql = self.db.query("SELECT SQL_NO_CACHE id,name FROM auto_table")
        assert sql[0][1] == '张*'
        sql = self.db.query("SELECT SQL_CALC_FOUND_ROWS id,name FROM auto_table")
        assert sql[0][1] == '张*'

    #PARTITION分区表

    @allure.title('SQL语法_where后面加各种条件测试')
    def testWhere(self):
        sql = self.db.query('SELECT name FROM auto_table where id = 1')
        assert sql[0][0] == '张*'
        sql = self.db.query('SELECT id,name FROM auto_table where id <> 10')
        assert sql[0][1] == '张*'
        sql = self.db.query('SELECT name FROM auto_table where id < 10 and id > 0')
        assert sql[0][0] == '张*'
        sql = self.db.query("SELECT * FROM auto_table WHERE id in(2,3)")
        assert sql[0][1] == '古**'
        sql = self.db.query("SELECT * FROM auto_table WHERE name in ('古天乐','欧阳震华')")
        assert sql[0][1] == '古**'
        sql = self.db.query('select * FROM auto_table where id BETWEEN 2 and 10 order by id')
        assert sql[0][1] == '古**'
        sql = self.db.query('select * FROM auto_table where id NOT BETWEEN 2 and 10')
        assert sql[0][1] == '张*'
        sql = self.db.query('SELECT * from auto_table,auto_table_copy where auto_table.id = auto_table_copy.id')
        assert sql[0][1] == '张*'
        assert sql[0][21] == '张*'

    @allure.title('SQL语法_表别名测试')
    def testAlias(self):
        sql = self.db.query('select * from auto_table t')
        assert sql[0][1] == '张*'
        sql = self.db.query('select t.id, t.name from auto_table t')
        assert sql[0][1] == '张*'
        sql = self.db.query('select t.* from auto_table t')
        assert sql[0][1] == '张*'
        sql = self.db.query('SELECT a.name,b.name from auto_table a,auto_table_copy b where a.id = b.id')
        assert sql[0][0] == '张*'
        assert sql[0][1] == '张*'

    @allure.title('SQL语法_as测试')
    def testAs(self):
        sql = self.db.query('SELECT name AS 姓名 from auto_table')
        assert sql[0][0] == '张*'
        sql = self.db.query("SELECT name AS '姓名' from auto_table")
        assert sql[0][0] == '张*'
        sql = self.db.query('SELECT name AS "姓名" from auto_table')
        assert sql[0][0] == '张*'
        sql = self.db.query('SELECT name AS `姓名` from auto_table')
        assert sql[0][0] == '张*'

    @allure.title('SQL语法_or测试')
    def testOr(self):
        sql = self.db.query('SELECT * FROM auto_table WHERE id>4 or id=2')
        assert sql[0][1] == '古**'

    @allure.title('SQL语法_like测试')
    def testOr(self):
        sql = self.db.query("SELECT * FROM auto_table WHERE name like '%古%'")
        assert sql[0][1] == '古**'

    @allure.title('SQL语法_groupBy测试')
    def testGroupBy(self):
        sql = self.db.query("SELECT id,name FROM auto_table WHERE id>1 GROUP BY id")
        assert sql[0][1] == '古**'
        # sql = self.db.query("SELECT name,COUNT(name) FROM auto_table WHERE id>10 GROUP BY name WITH ROLLUP")
        # assert sql[0][1] == '周**'

    @allure.title('SQL语法_count测试')
    def testCount(self):
        sql = self.db.query("select name,count(age) from auto_table")
        assert sql[0][0] == '张*'
        sql = self.db.query("select count(age),name from auto_table where id >1")
        assert sql[0][1] == '古**'

    @allure.title('SQL语法_withRollup测试')
    def testWithRollup(self):
        sql = self.db.query("SELECT id,name FROM auto_table WHERE id<10 GROUP BY id,email WITH ROLLUP;")
        assert sql[0][1] == '张*'
        assert sql[1][1] == '张*'

    @allure.title('SQL语法_Having测试')
    def testHaving(self):
        sql = self.db.query("SELECT id,name FROM auto_table  GROUP BY id HAVING id=1")
        assert sql[0][1] == '张*'

    @allure.title('SQL语法_orderBy测试')
    def testOrderBy(self):
        sql = self.db.query("SELECT id,name FROM auto_table order by id,name")
        assert sql[0][1] == '张*'
        sql = self.db.query("SELECT id,name FROM auto_table order by id desc")
        assert sql[0][1] == '周**'
        sql = self.db.query("SELECT id,name FROM auto_table where id < 10 order by id desc")
        assert sql[0][1] == '林*'
        sql = self.db.query("SELECT id,name FROM auto_table where id < 10 order by id asc")
        assert sql[0][1] == '张*'

    @allure.title('SQL语法_forUpdate测试')
    def testForUpdate(self):
        sql = self.db.query("select * from auto_table for UPDATE")
        assert sql[0][1] == '张*'

    # 代码不支持该sql
    # @allure.title('SQL语法_@变量测试')
    # def testVariable(self):
    #     self.db.query("SELECT id,name INTO @x,@y FROM auto_table;")
    #     sql = self.db.query("SELECT @x,@y;")
    #     assert sql[0][1] == '张*'

    # into outfile
    #into dumpfile待研究

    @allure.title('SQL语法_union测试')
    def testUnion(self):
        sql = self.db.query("select * from auto_table where name like'张%' UNION select * from auto_table_copy where name like '张%'")
        assert sql[0][1] == '张*'
        sql = self.db.query('SELECT * FROM (SELECT name FROM auto_table UNION SELECT card_id FROM auto_table_copy) tmp limit 100')
        assert sql[0][0] == '张*'
        assert sql[18][0] == '23***************7'
        sql = self.db.query('SELECT * FROM (SELECT card_id FROM auto_table_copy UNION SELECT name FROM auto_table) tmp limit 100;')
        assert sql[17][0] == '张*'
        assert sql[0][0] == '23***************7'
        sql = self.db.query("select * from auto_table where name like'张%' UNION ALL select * from auto_table_copy where name like '张%'")
        assert sql[0][1] == '张*'
        assert sql[1][1] == '张*'
        sql = self.db.query("select * from auto_table where name like'张%' UNION distinct select * from auto_table_copy where name like '张%'")
        assert sql[0][1] == '张*'
        sql = self.db.query("select name from auto_table UNION select name from auto_table ORDER BY name;")
        assert sql[0][1] == '古**'
        sql = self.db.query("select name from auto_table UNION all select name from auto_table ORDER BY name;")
        assert sql[0][2] == '古**'
        assert sql[0][3] == '古**'

    @allure.title('SQL语法_using测试')
    def testUsing(self):
        sql = self.db.query("select name from auto_table a inner join auto_table_copy d USING(name)")
        assert sql[0][0] == '张*'

    @allure.title('SQL语法_select(select ...)测试')
    def testSelect2(self):
        sql = self.db.query("SELECT (SELECT name FROM auto_table WHERE id=1)")
        assert sql[0][0] == '张*'

    @allure.title('SQL语法_select upper测试')
    def testupper(self):
        sql = self.db.query("SELECT UPPER((SELECT name FROM auto_table WHERE id=1)) FROM auto_table;")
        assert sql[0][0] == '张*'

    @allure.title('SQL语法_any测试')
    def testAny(self):
        sql = self.db.query("SELECT * FROM auto_table WHERE id > ANY (SELECT id FROM auto_table);")
        assert sql[0][1] == '古**'
        sql = self.db.query("SELECT * FROM auto_table WHERE id <> ANY (SELECT id FROM auto_table);")
        assert sql[0][1] == '张*'

    @allure.title('SQL语法_some测试')
    def testSome(self):
        sql = self.db.query("SELECT * FROM auto_table WHERE id <> SOME (SELECT id FROM auto_table);")
        assert sql[0][1] == '张*'

    @allure.title('SQL语法_行子查询测试')
    def testLineSql(self):
        sql = self.db.query("SELECT * FROM auto_table WHERE (id,name) = (1,'张三');")
        assert sql[0][1] == '张*'

    @allure.title('SQL语法_join测试')
    def testJoin(self):
        sql = self.db.query("SELECT * from auto_table JOIN auto_table_copy ON auto_table.id=auto_table_copy.id")
        assert sql[0][1] == '张*'
        assert sql[0][21] == '张*'
        sql = self.db.query("SELECT * from auto_table INNER JOIN auto_table_copy ON auto_table.id=auto_table_copy.id")
        assert sql[0][1] == '张*'
        assert sql[0][21] == '张*'
        sql = self.db.query("SELECT * FROM auto_table INNER JOIN auto_table_copy USING (id)")
        assert sql[0][1] == '张*'
        assert sql[0][21] == '张*'
        sql = self.db.query("SELECT * from auto_table LEFT JOIN auto_table_copy ON auto_table.id=auto_table_copy.id")
        assert sql[0][1] == '张*'
        assert sql[0][21] == '张*'
        sql = self.db.query("SELECT * from auto_table RIGHT JOIN auto_table_copy ON auto_table.id=auto_table_copy.id")
        assert sql[0][1] == '张*'
        assert sql[0][21] == '张*'
        sql = self.db.query("select * from auto_table NATURAL JOIN auto_table_copy")
        assert sql[0][1] == '张*'

    @allure.title('SQL语法_EXISTS测试')
    def testEXISTS(self):
        sql = self.db.query("select id,name from auto_table where EXISTS (SELECT name from auto_table where id >10)")
        assert sql[0][1] == '张*'
        sql = self.db.query("select id,name from auto_table where NOT EXISTS (SELECT name from auto_table where id >100)")
        assert sql[0][1] == '张*'
        self.db.close()


if __name__ == '__main__':
    pytest.main(['testSQL.py', '-s'])






