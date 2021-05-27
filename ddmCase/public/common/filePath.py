# !/usr/bin/python3
# -*- coding: utf-8 -*-

'''
获取excel数据所在的绝对路径

'''

import os


class filePath:
    def __init__(self):
        # 获取当前路径
        self.path = os.path.dirname(__file__)
        # 获取父级路径
        self.parent_path = os.path.dirname(self.path)
        # 获取祖父级路径
        self.grandParent_path = os.path.dirname(os.path.dirname(self.path))


    def testData_login_Path(self):
        '''
        获取login文件夹的绝对路径
        :return:
        '''
        testData_login_Path = self.grandParent_path + '/testData/interfaceExcel/login'
        return testData_login_Path

    def testData_datasourceManage_Path(self):
        '''
        获取datasourceManage文件夹的绝对路径
        :return:
        '''
        testData_datasourceManage_Path = self.grandParent_path + '/testData/interfaceExcel/datasourceManage'
        return testData_datasourceManage_Path

    def script_Path(self):
        '''
        获取script文件夹的绝对路径
        :return:
        '''
        script_Path = self.grandParent_path + '/testData/script'
        return script_Path

    def testData_maskRule_Path(self):
        '''
        获取maskRule文件夹的绝对路径
        :return:
        '''
        testData_maskRule_Path = self.grandParent_path + '/testData/interfaceExcel/maskRule'
        return testData_maskRule_Path

    def testData_extRule_Path(self):
        '''
        获取extRule文件夹的绝对路径
        :return:
        '''
        testData_extRule_Path = self.grandParent_path + '/testData/interfaceExcel/extRule'
        return testData_extRule_Path

    def testData_senDataFind_Path(self):
        '''
        获取senDataFind文件夹的绝对路径
        :return:
        '''
        testData_senDataFind_Path = self.grandParent_path + '/testData/interfaceExcel/senDataFind'
        return testData_senDataFind_Path


    def testData_license_Path(self):
        '''
        获取license文件夹的绝对路径
        :return:
        '''
        testData_license_Path = self.grandParent_path + '/testData/interfaceExcel/license'
        return testData_license_Path

    def testData_whiteList_Path(self):
        '''
        获取whiteList文件夹的绝对路径
        :return:
        '''
        testData_whiteList_Path = self.grandParent_path + '/testData/interfaceExcel/whiteList'
        return testData_whiteList_Path

    def report_Path(self):
        '''
        获取report文件夹的绝对路径
        :return:
        '''
        report_Path = self.grandParent_path + '/report/'
        return report_Path




if __name__ == '__main__':
    print(filePath().testData_login_Path())
    print(filePath().testData_senDataFind_Path())
