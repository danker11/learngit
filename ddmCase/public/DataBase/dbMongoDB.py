#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 导入模块
from pymongo import MongoClient

# 建立Mongodb数据库连接
client = MongoClient('localhost', 27017)
# test为数据库
db = client.test
# test为集合，相当于表名
collection = db.test
# 插入集合数据
collection.insert({"title": "test"})
# 打印集合中所有数据
for item in collection.find():
    print(item)
# 更新集合里的数据
collection.update({"title": "test"}, {"title": "this is update test"})
# 关闭连接
client.close()
# !!!!其他操作
# 查找集合中单条数据
# print collection.find_one()
# 删除集合collection中的所有数据
# collection.remove()
# 删除集合collection
# collection.drop()
