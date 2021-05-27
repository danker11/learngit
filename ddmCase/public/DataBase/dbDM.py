# !/usr/bin/python3
# -*- coding: utf-8 -*-

import configparser
# import dmPython
from public.filePath import filePath


class dbDM():
    '''
    python连接DM数据库及对应操作
    '''

    def __init__(self,connMode=1):
        # 读取配置文件，需要填写绝对路径
        cf = configparser.ConfigParser(allow_no_value=True)
        cf.read(filePath().databases_Path(), encoding='utf-8')

        #  读取配置文件中的所有section，以列表形式返回，这步可以不需要
        sections = cf.sections()
        # print(sections)

        # 获取section为DM-Database下的所有详细的配置host，port，user，password以列表形式返回，这步可以不需要
        opt = cf.options("DM-Database-Proxy")
        # print(opt)
        self.connMode = connMode
        if self.connMode == 1:
            # 读取每个配置对应的值
            self.host = cf.get("DM-Database-Proxy", "host")
            self.port = int(cf.get("DM-Database-Proxy", "port"))
            self.user = cf.get("DM-Database-Proxy", "user")
            self.password = cf.get("DM-Database-Proxy", "password")
        elif self.connMode == 2:
            self.host = cf.get("DM-Database", "host")
            self.port = int(cf.get("DM-Database", "port"))
            self.user = cf.get("DM-Database", "user")
            self.password = cf.get("DM-Database", "password")
        else:
            print('connMode(连接模式)不正确，只能填写1或者2,1代表代理，2代表直连')
        # 连接数据库执行sql，port需要为整数类型的，读取后为str类型需要转换
        # self.conn = dmPython.connect(host=self.host, port=self.port, user=self.user, password=self.password,autoCommit=True)
        # self.conn = dmPython.connect(port=self.port, user=self.user, password=self.password)
        self.cursor = self.conn.cursor()

    # 执行查询sql
    def query(self, sql):
        self.cursor.execute(sql)
        # 获取所有的返回结果,以列表的形式返回所有集合，每条数据是一个元组，也可以用fetchone()获取一条记录
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
    conn = dbDM(1)
    results = conn.query('select * from "test"."auto_table"')
    for result in results:
        print(result)
    conn.close()
