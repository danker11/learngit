# !/usr/bin/python3
# -*- coding: utf-8 -*-

from config.config import database
from config.config import ip
import pymysql
from public.common.do_log import logOutput
import traceback

'''
mysql数据库连接
'''


class DbMysql:
    def __init__(self, connMode=1):
        self.connMode = connMode
        self.user = database["mysqlDB"]["userName"]
        self.password = database["mysqlDB"]["passWord"]
        self.database = database["mysqlDB"]["databasename"]
        if self.connMode == 1:
            # 代理连接
            self.host = ip
            self.port = int(database["mysqlDB"]["proxyPort"])  # 数据库连接端口需要整数类型的

        else:
            # 直连
            self.host = database["mysqlDB"]["address"]
            self.port = int(database["mysqlDB"]["port"])

        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                        database=self.database, charset='utf8')
            self.cursor = self.conn.cursor()
        except Exception as e:
            logOutput("error",
                      "数据库连接失败了，数据库ip:{}，port:{},user:{},passwd:{},database:{}".format(self.host, self.port, self.user,
                                                                                       self.password, self.database))
            logOutput("error", traceback.format_exc())
            raise e

    # 执行查询sql
    def query(self, sql):
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
    db = DbMysql()
    # sel = db.query("SELECT * FROM (SELECT name FROM auto_table UNION SELECT card_id FROM auto_table_copy) tmp limit 100")

    sel = db.query("select * from auto_table_copy")

    # alist = []
    # for i in sel:
    #     alist.append(i[0])
    # print(alist)
    # import pprint
    # pprint.pprint(sel)
    # print(sel[18])
    print(sel)
    db.close()
