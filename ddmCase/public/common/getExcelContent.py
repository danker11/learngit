# !/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import xlrd
from public.common.filePath import filePath
from config.config import url


class GetExcelConetnt:
    def getExcelConetnt(self, excel_url, lineNumber=1, sheetNumber=1):
        '''
        从excel中获取维护好的接口参数
        :param  excel_url: 维护好的excel接口地址，绝对路径
        :type excel_url：str
        :param lineNumber: 获取第i+1行的数据
        :type lineNumber：int
        :param sheetNumber: excel中的sheet页，默认都是第一个sheet页，即sheetnumber = 0
        :type sheetNumber：int
        :return: base_url,header,param_data,expect_data
        '''
        # 根据传入的Excel地址打开url
        temp = xlrd.open_workbook(excel_url)
        # 打开temp中的sheet页签，[1]为第二个sheet，默认打开第二个sheet
        if sheetNumber == 1:
            table = temp.sheets()[sheetNumber]
            # 获取打开的sheet页签的第i+1行数据，组成一个列表
            interfaceInfo = table.row_values(lineNumber)
            # 拼接为一个完整的url
            base_url = url + interfaceInfo[2]
            # 获取请求头数据
            header = json.loads(interfaceInfo[3])
            # 7判断json参数是否为空，不为空的话将json转化为python数据类型，从excel中获取的是string类型，需要转化
            if interfaceInfo[4] == '':
                param_data = ''
            else:
                # 将json格式的参数转化为字典
                try:
                    param_data = json.loads(interfaceInfo[4])
                # 将表单格式的参数串转化为字典
                except:
                    list = interfaceInfo[4].split('&')
                    data = {}
                    for ele in list:
                        new_list = ele.split('=')
                        data.update({new_list[0]: new_list[1]})
                    param_data = data
            return base_url, header, param_data

        else:
            table =temp.sheets()[0]
            parameter = table.row_values(lineNumber)
            try:
                # 将json格式的参数转化为字典
                param_data = json.loads(parameter[2])
            except:
                # 将表单格式的参数串转化为字典
                list = parameter[2].split('&')
                data = {}
                for ele in list:
                    new_list = ele.split('=')
                    data.update({new_list[0]: new_list[1]})
                param_data = data
            return param_data

if __name__ == '__main__':
    getExcel = GetExcelConetnt()
    getlogin = getExcel.getExcelConetnt(filePath().testData_datasourceManage_Path() + '/数据源列表添加接口.xlsx',1,1)
    print(getlogin)


