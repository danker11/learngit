# !/usr/bin/python3
# -*- coding: utf-8 -*-
import configparser
import pymysql
from public.filePath import filePath


class dbGBase():
    '''
    python连接dbGBase数据库及对应操作
    '''
    def __init__(self):

        # 读取配置文件，需要填写绝对路径
        cf = configparser.ConfigParser(allow_no_value=True)
        cf.read(filePath().databases_Path(), encoding='utf-8')
        #  读取配置文件中的所有section，以列表形式返回，这步可以不需要
        sections = cf.sections()
        # 获取section为Mysql-Database下的所有详细的配置host，port，user，password，以列表形式返回，这步可以不需要
        opt = cf.options("GBase-Database")

        # 读取每个配置对应的值
        self.host = cf.get("GBase-Database","host")
        # cf.getint()返回的是整数类型
        self.port = cf.getint("GBase-Database","port")
        self.user = cf.get("GBase-Database", "user")
        self.password = cf.get("GBase-Database", "password")
        self.database = cf.get("GBase-Database", "database")

        # 连接数据库执行sql，port需要为整数类型的
        self.conn = pymysql.connect(host = self.host, port = self.port,user = self.user, password = self.password,db = self.database,charset = 'utf8mb4')
        self.cursor = self.conn.cursor()

    # 执行查询sql
    def query(self,sql):
        '''
        :param str sql: 执行的sql语句
        :return: tuple results，sql查询的结果集
        '''
        self.cursor.execute(sql)
        # 获取所有的返回结果,以元组的形式返回所有集合，每条数据是一个元组，也可以用fetchone()获取一条记录
        results = self.cursor.fetchall()
        return results

    # 执行除查询外的其他类型的sql
    def execute(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    # 关闭游标跟连接
    def close(self):
        self.cursor.close()
        self.conn.close()

'''
测试代码
'''
if __name__ == '__main__':
    conn = dbGBase()
    results = conn.query("SELECT * FROM secsmart_test limit 10;")
    for result in results:
        print(result)
    conn.close()