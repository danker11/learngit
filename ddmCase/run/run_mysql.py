# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/4/13
# filename:run_test2
import pytest
import os

try:
    for one in os.listdir('../report/tmp'):
        if 'json' in one or 'txt' in one:
            os.remove(f'../report/tmp/{one}')
except:
    print('第一次执行pytest框架')



# 数据源模块的新增、搜索、编辑
pytest.main(['../testCase/testMysql/testDatasourceManage.py', '-s', '--alluredir', '../report/tmp'])
# # 敏感扫描模块
pytest.main(['../testCase/testMysql/testSenDataFind.py', '-s', '--alluredir', '../report/tmp'])
# 脱敏规则模块--规则批量操作/规则组操作
pytest.main(['../testCase/testMysql/testMaskRules.py', '-s', '--alluredir', '../report/tmp'])
# 脱敏规则模块--规则单个操作
pytest.main(['../testCase/testMysql/testMaskRule.py', '-s', '--alluredir', '../report/tmp'])
# SQL语法测试
pytest.main(['../testCase/testMysql/testSQL.py', '-s', '--alluredir', '../report/tmp'])
# 白名单测试
pytest.main(['../testCase/testMysql/testWriteLIst.py', '-s', '--alluredir', '../report/tmp'])
# 拓展规则测试-遍历所有拓展规则类型
pytest.main(['../testCase/testMysql/testExtRuleSQL.py', '-s', '--alluredir', '../report/tmp'])
# 拓展规则测试-其他功能
pytest.main(['../testCase/testMysql/testExtRule.py', '-s', '--alluredir', '../report/tmp'])
# 后置操作-删除资产，清空数据
pytest.main(['../testCase/testMysql/testMysqlTeradown.py', '-s', '--alluredir', '../report/tmp'])


os.system('allure generate ../report/tmp -o ../report/report --clean')
os.system('allure open -h 192.168.11.235 -p 9999 ../report/report')




