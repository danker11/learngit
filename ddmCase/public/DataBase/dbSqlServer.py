# !/usr/bin/python3
# -*- coding: utf-8 -*-
import configparser
import warnings
warnings.simplefilter('ignore', DeprecationWarning)
import pymssql
from public.filePath import filePath
class dbSqlServer:
    '''
    pyython连接SqlServer数据库及对应操作
    '''
    def __init__(self, connMode=1):
        # 读取配置文件，需要填写绝对路径
        cf = configparser.ConfigParser(allow_no_value=True)
        cf.read(filePath().databases_Path(), encoding='utf-8')
        # 读取配置文件中的所有section，以列表形式返回，这步可以不需要
        sections = cf.sections()
        # Oracle-Database下的所有详细的配置host，port，user，password，database以列表形式返回，这步可以不需要
        opt = cf.options("SqlServer-Database")
        self.connMode = connMode
        if self.connMode == 1:
            # 读取每个配置对应的值
            self.host = cf.get("SqlServer-Database-Proxy","host")
            self.port = cf.get("SqlServer-Database-Proxy","port")
            self.user = cf.get("SqlServer-Database-Proxy", "user")
            self.password = cf.get("SqlServer-Database-Proxy", "password")
            self.database = cf.get("SqlServer-Database-Proxy", "database")
        elif self.connMode == 2:
            # 读取每个配置对应的值
            self.host = cf.get("SqlServer-Database","host")
            self.port = cf.get("SqlServer-Database","port")
            self.user = cf.get("SqlServer-Database", "user")
            self.password = cf.get("SqlServer-Database", "password")
            self.database = cf.get("SqlServer-Database", "database")
        else:
            print('connMode(连接模式)不正确，只能填写1或者2,1代表代理，2代表直连')
        # 连接SqlServer
        self.conn = pymssql.connect(host=self.host, port=self.port, user=self.user, password=self.password,database=self.database, charset='utf8')
        # 创建游标
        self.cursor = self.conn.cursor()

    # 执行查询sql
    def query(self, sql, args=[]):
        self.cursor.execute(sql, args)
        data = self.cursor.fetchall()
        return data

    # 执行除查询sql外的其他类型sql
    def execute(self, sql, args=[]):
        self.cursor.execute(sql, args)
        self.conn.commit()

    # 关闭游标和数据库连接
    def close(self):
        self.cursor.close()
        self.conn.close()


# 测试代码
if __name__ == '__main__':
    conn = dbSqlServer(2)
    results = conn.query("SELECT TOP 10 * FROM auto_table")
    for result in results:
        print(result)
    conn.close()