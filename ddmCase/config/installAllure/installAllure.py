# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/4/13
# filename:installAllure


'''
临时添加的allure客户端的环境变量，不知道能不能


'''

import os

def allurePathAdd():
    try:
        current = os.getcwd()
        allurePage = r'allure-2.13.9\allure-2.13.9\bin'
        allurePath=os.path.join(current,allurePage)
        os.environ["PATH"] += allurePath + os.pathsep
        return os.environ["PATH"]
    except Exception as e:
        pass


if __name__ == '__main__':
    for i in allurePathAdd().split(';'):
        print(i)

