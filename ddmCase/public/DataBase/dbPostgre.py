# !/usr/bin/python3
# -*- coding: utf-8 -*-

import configparser
import psycopg2
from public.filePath import filePath


class dbPostgre:
    '''
    python连接Postgre数据库及对应操作
    '''

    def __init__(self, connMode=1):
        # 读取配置文件，需要填写绝对路径
        # cf = configparser.ConfigParser(allow_no_value=True)
        cf = configparser.RawConfigParser(allow_no_value=True)
        cf.read(filePath().databases_Path(), encoding='utf-8')
        # 读取配置文件中的所有section，以列表形式返回，这步可以不需要
        sections = cf.sections()
        # Oracle-Database下的所有详细的配置host，port，user，password，mode，以列表形式返回，这步可以不需要
        opt = cf.options("Postgre-Database")
        self.connMode = connMode
        if self.connMode == 1:
            # 读取每个配置对应的值
            self.host = cf.get("Postgre-Database-Proxy", "host")
            self.port = cf.get("Postgre-Database-Proxy", "port")
            self.user = cf.get("Postgre-Database-Proxy", "user")
            self.password = cf.get("Postgre-Database-Proxy", "password")
            self.database = cf.get("Postgre-Database-Proxy", "database")
        elif self.connMode == 2:
            # 读取每个配置对应的值
            self.host = cf.get("Postgre-Database", "host")
            self.port = cf.get("Postgre-Database", "port")
            self.user = cf.get("Postgre-Database", "user")
            self.password = cf.get("Postgre-Database", "password")
            self.database = cf.get("Postgre-Database", "database")
        else:
            print('connMode(连接模式)不正确，只能填写1或者2,1代表代理，2代表直连')
        self.conn = psycopg2.connect(host=self.host,port=self.port, user=self.user, password=self.password,database= self.database)
        self.cursor = self.conn.cursor()

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
#############测试代码#######################
'''
if __name__ == '__main__':
    conn = dbPostgre(2)
    # conn.execute('CREATE DATABASE testdb')
    results = conn.query('SELECT * FROM "public"."auto_table" limit 10')
    # results = conn.query('select * from "postgres"."public"."student" LIMIT 10')
    for result in results:
        print(result)
    # conn.execute('''
    # INSERT INTO "!#$%^&*()@, '-./_+"."!#$%^&*()@, '-./_+" ("id", "!#$%^&*()@, '-./_+", "birthday", "age", "card_id", "bank_id", "phone", "tel", "email", "address", "campany_name", "post_code", "car_number", "vic_number", "passport_no", "social_credit_code", "ga_passport_no", "tw_passport_no", "army_id", "url") VALUES ('1', '张三', '1992-10-01', '28', '230227198302151067', '6224906205424108', '15854488628', '0571-88672500', 'pmsfqmsfugfyqa53784255@sina.cn', '浙江省拱墅区中心街128号-1-6', '闪捷信息科技有限公司', '344800', '浙A12345', 'LGBK22E7X7Y008423', 'E00123045', '92371000MA3MXH0E3W', 'H12340001', '00032451', '军0001235', 'https://192.168.11.89:8282/')
    # ''')
    conn.close()
