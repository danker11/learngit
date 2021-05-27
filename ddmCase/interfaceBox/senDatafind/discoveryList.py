# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/4/20
# filename:taskList


import requests
from public.common.filePath import filePath
from public.common.getExcelContent import GetExcelConetnt
from public.common.timeStamp import TimeStamp
from public.common.do_log import logOutput
import traceback
from interfaceBox.login.login import Login

'''
敏感数据发现结果

敏感数据发现结果接口

'''


class DiscoveryList:

    def __init__(self,token):
        self.token = token
        requests.packages.urllib3.disable_warnings()

    def discoveryList(self, indata):
        '''
        敏感数据发现结果查看
        :param indata:传参：id任务id,dbType数据库类型
        :return:返回响应数据
        '''
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_senDataFind_Path() + '/敏感数据扫描详情接口.xlsx', 1)
        base_url = base_url.format(TimeStamp().timeStamp())
        header.update({"token": self.token})
        param_data.update(indata)
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url=base_url, headers=header, json=param_data, verify=False)
        try:
            logOutput("info", "敏感数据发现接口正常，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            return r.json()
        except Exception as e:
            logOutput("error", "敏感数据发现接口错误，传入的参数为{}，返回的结果为{}".format(r.request.body, r.json()))
            logOutput("error", traceback.format_exc())
            raise e


if __name__ == '__main__':
    dis = DiscoveryList(Login().login())
    dict1 = dis.discoveryList({"id":"136", "dbType":"MySQL"})
    print(str(dict1))
    if "auto_table" in str(dict1):
        print("通过")
