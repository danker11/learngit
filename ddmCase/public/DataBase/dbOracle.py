# !/usr/bin/python3
# -*- coding: utf-8 -*-

import configparser
import cx_Oracle as cx
from public.filePath import filePath


class dbOracle:
    '''
    python连接oracle数据库及对应操作
    '''

    def __init__(self, connMode=1):
        # 读取配置文件，需要填写绝对路径
        cf = configparser.ConfigParser(allow_no_value=True)
        cf.read(filePath().databases_Path(), encoding='utf-8')
        # # 读取配置文件中的所有section，以列表形式返回，这步可以不需要
        # sections = cf.sections()
        # # Oracle-Database下的所有详细的配置host，port，user，password，mode，以列表形式返回，这步可以不需要
        # opt = cf.options("Oracle-Database")
        self.mode = connMode
        if self.mode == 1:
            # 读取每个配置对应的值
            self.host = cf.get("Oracle-Database-Proxy", "host")
            self.port = cf.get("Oracle-Database-Proxy", "port")
            self.user = cf.get("Oracle-Database-Proxy", "user")
            self.password = cf.get("Oracle-Database-Proxy", "password")
            self.SERVICE_NAME = cf.get("Oracle-Database-Proxy", "SERVICE_NAME")
            self.mode = cf.get("Oracle-Database-Proxy", "mode")
        elif self.mode == 2:
            self.host = cf.get("Oracle-Database", "host")
            self.port = cf.get("Oracle-Database", "port")
            self.user = cf.get("Oracle-Database", "user")
            self.password = cf.get("Oracle-Database", "password")
            self.SERVICE_NAME = cf.get("Oracle-Database", "SERVICE_NAME")
            self.mode = cf.get("Oracle-Database", "mode")
        # 连接oracle
        '''
        连接oracle共有3种方式
        第1种：con = cx.connect(用户名, 密码, 服务器ip:端口号/服务名)
        第2种：con = cx.connect(用户名/密码@服务器ip:端口号/服务名)
        第3种：dsn = cx.makedsn(服务器ip, 端口号, 服务名)
                connection = cx.connect(用户名, 密码, dsn)
                第3种端口号也需要为字符串
        '''
        url = self.host + ':' + self.port + '/' + self.SERVICE_NAME
        if self.mode == '':
            self.conn = cx.connect(self.user, self.password, url)
        elif self.mode == 'SYSDBA':
            self.conn = cx.connect(self.user, self.password, url, mode=cx.SYSDBA)
        else:
            try:
                self.conn = cx.connect(self.user, self.password, url, mode=self.mode)
            except cx.DatabaseError as ex:
                raise Exception("cx_Oracle.DatabaseError:" + str(ex))
            except Exception as ex:
                raise Exception("Exception:" + str(ex))
        self.cursor_ = self.conn.cursor()

    # 执行查询sql
    def query(self, sql, args=[]):
        try:
            self.cursor_.execute(sql, args)
            data = self.cursor_.fetchall()
        except cx.DatabaseError as ex:
            raise Exception("cx_Oracle.DatabaseError:" + str(ex))
        except Exception as ex:
            raise Exception("Exception:" + str(ex))
        return data

    # 执行除查询sql外的其他类型sql
    def execute(self, sql, args=[]):
        try:
            self.cursor_.execute(sql, args)
            self.conn.commit()
        except cx.DatabaseError as ex:
            raise Exception("cx_Oracle.DatabaseError:" + str(ex))
        except Exception as ex:
            raise Exception("Exception:" + str(ex))

    # 调用存储过程
    def call_proc(self, proc_name, args=[]):
        try:
            self.cursor_.callproc(proc_name, args)
        except cx.DatabaseError as ex:
            raise Exception("cx_Oracle.DatabaseError:" + str(ex))
        except Exception as ex:
            raise Exception("Exception:" + str(ex))

    # 调用函数
    def call_func(self, proc_name, ret_type, args=[]):
        try:
            ret_value = self.cursor_.callfunc(proc_name, ret_type, args)
        except cx.DatabaseError as ex:
            raise Exception("cx_Oracle.DatabaseError:" + str(ex))
        except Exception as ex:
            raise Exception("Exception:" + str(ex))
        return ret_value

    # 关闭游标和数据库连接
    def close(self):
        self.cursor_.close()
        self.conn.close()


'''
测试代码
'''
if __name__ == '__main__':
    conn = dbOracle(2)
    results = conn.query('''select  * from SCOTT."auto_table"''')
    for result in results:
        print(result)
    conn.close()

# conn = cx.connect('scott','123456', '192.168.11.89:1521/orcl')
# cursor = conn.cursor()
# cursor.execute('select  * from SCOTT.STUDENT')
# results = cursor.fetchall()
# for result in results:
#     print(result)


# 整形
# cursor.execute('select  * from SCOTT.STUDENT where "id" = :a',a=1)
# date1 = cursor.fetchall()
# print(date1)
# # 浮点型
# cursor.execute('select  * from SCOTT.STUDENT where "id" = :b',b=1.0)
# date2 = cursor.fetchall()
# print(date2)
# # 字符串
# cursor.execute('select  * from SCOTT.STUDENT where "name" = :c',c='张三')
# date3 = cursor.fetchall()
# print(date3)
# cursor.execute('select  * from SCOTT.STUDENT where "DATE_COLUM" = :c',c=datetime.datetime(2020, 6, 2, 10, 26, 34))
# date4 = cursor.fetchall()
# print(date4)
