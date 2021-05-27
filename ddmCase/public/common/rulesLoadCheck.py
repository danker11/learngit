# !/usr/bin/python3
# -*- coding: utf-8 -*-
import time

'''
检查1分钟内是否下发了规则,如果1分钟未下发规则，则返回False，如果1分钟之内下发了规则，则返回True
'''


def rulesLoadCheck(conn, sql, checkresult, cell_number=0, column_number=1, minute=1):
    '''
    :param conn: 数据库连接
    :param sql: 执行的sql语句
    :param checkresult: 需要校验的值
    :param cell_number: 数据库执行sql返回的数据的指定行数
    :param column_number: 数据库执行sql返回的指定列数
    :param minute: 连续校验的时间，默认1分钟
    :return: 通过校验返回True，不通过返回False
    '''
    i = 0
    while i < minute * 20:
        time.sleep(3)
        results = conn.query(sql)
        if results[cell_number][column_number] == checkresult:  # 默认校验第一条数据的第2个字段，可以随参数自己修改
            return True
        else:
            i += 1
    return False


if __name__ == '__main__':
    from public.DataBase.dbMysql import DbMysql
    db = DbMysql(1)
    print(rulesLoadCheck(db, 'select * from auto_table_copy', '张三', 0, 0))