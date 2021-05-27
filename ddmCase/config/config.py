# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/4/15
# filename:config

'''
测试环境ip
'''

ip = "192.168.11.86"
user = "sysadmin"
passwd = "111111"


'''
数据库配置信息,根据需要自行修改
'''
database = {
    # mysql数据库
    "mysqlDB":{
        'type': 'MySQL',
        'version': '5.6',
        'address': '192.168.10.251',
        'databasename': 'auto',
        'port': '3306',
        'userName': 'root',
        'passWord': '123456',
        'proxyPort': '13500',},

    # oracle数据库
    "oracleDB":{
        "ip": "192.168.10.251",
        "port": "1521",
        "user": "sys",
        "passwd": "123456",
        "proxyPort": "13801"}

    #待完善
}



url = "https://{}:8282".format(ip)




