# !/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from public.filePath import filePath
from public.getExcelContent import getExcelConetnt
import base64


class testEnvCheck_mysql:
    def __init__(self):
        self.param_data = getExcelConetnt().getExcelConetnt(filePath().testData_datasourceManage_Path() + '/数据源列表添加接口.xlsx', 1)[2]
        self.host = self.param_data.get('address')
        self.port = int(self.param_data.get('port'))
        self.user = self.param_data.get('userName')
        self.database = self.param_data.get('databasename')
        self.password = base64.b64decode(self.param_data.get('passWord')).decode("utf-8")
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                        database=self.database, charset='utf8')
            self.cursor = self.conn.cursor()
        except:
            print('mysql数据源无法连接，请检查数据源账号密码及网络环境')
            print(self.host,self.port,self.password,self.user,self.database)

    def tableCheck(self):
        '''
        校验是否存在auto库，不存在的话创建auto库及对应的表
        :return:
        '''
        self.cursor.execute('show schemas')
        results = self.cursor.fetchall()
        # print(results)
        if ('auto',) not in results:
            self.cursor.execute('create database auto character set utf8')
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                               database='auto', charset='utf8')
        cursor = conn.cursor()
        with open(filePath().script_Path() + '/mysql/script.sql', mode='r', encoding='utf-8') as f:
            sql_list1 = f.read().split(';')
            for sql in sql_list1:
                # 判断包含空行的
                if '\n' in sql:
                    # 替换空行为空字符串
                    sql = sql.replace('\n', '')
                    cursor.execute(sql)
                    conn.commit()
                elif sql == '':
                    pass
                else:
                    cursor.execute(sql)
                    conn.commit()
            cursor.close()
            conn.close()
        print('mysql测试环境已准备好，即将开始执行用例')
        return True


if __name__ == '__main__':
    testEnvCheck_mysql().tableCheck()
