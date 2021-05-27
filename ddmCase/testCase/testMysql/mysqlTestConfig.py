# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/5/7
# filename:mysqlTestConfig


# 数据源名称
databaseName = "mysql库-自动化测试"

# 扫描时可勾选的数据类型
dataTypes = ['车架号',
             '三证合一码(税务登记、组织机构、营业执照)',
             '邮政编码',
             '固定电话',
             '护照号',
             '军队证件',
             '台湾居民来往大陆通行证',
             '港澳居民来往大陆通行证',
             '身份证号/社保卡号/驾驶证号',
             '电子邮箱',
             '中文地址',
             '中文姓名',
             '手机号',
             '企业单位名称',
             '车牌号',
             '银行卡号']

# 添加单个规则时，枚举
dataTypes2 = ["三证合一码(税务登记、组织机构、营业执照)",
              "中文地址", "中文姓名", "企业单位名称",
              "军队证件", "台湾居民来往大陆通行证", "固定电话",
              "字符串", "手机号", "护照号", "数值", "日期",
              "港澳居民来往大陆通行证", "电子邮箱",
              "身份证号/社保卡号/驾驶证号", "车架号",
              "车牌号", "邮政编码", "银行卡号"]

from public.DataBase.dbMysql import DbMysql

# 直连数据库，获取相关数据，转换为列表模式
db = DbMysql(2)


def tableAll(sql):
    sel = db.query(sql)
    alist = []
    for i in sel:
        alist.append(i[0])
    return alist


# print(tableAll("show databases;"))
# print(tableAll("select table_name from information_schema.tables where TABLE_SCHEMA = 'auto';"))
# print(tableAll("SELECT COLUMN_NAME FROM information_schema.COLUMNS "
#                "WHERE TABLE_SCHEMA = 'auto' AND TABLE_NAME = 'auto_table';"))




