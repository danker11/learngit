# -*- coding: UTF-8 -*-
# author:lixinbo 
# time:2021/4/15
# filename:login

'''
登录模块封装

获取秘钥接口
登录接口
'''

import requests
from config.config import user, passwd
from public.common.timeStamp import TimeStamp
from public.common.filePath import filePath
from public.common.getExcelContent import GetExcelConetnt
from public.common.encrypt import encrypt
from public.common import do_log
import traceback


class Login:

    def randomCode(self):
        '''
        获取秘钥接口，加密方式为AES
        :return:获取秘钥id，与秘钥code码
        '''
        requests.packages.urllib3.disable_warnings()
        (base_url, header, param_data) = GetExcelConetnt().getExcelConetnt(
            filePath().testData_login_Path() + '/登录接口.xlsx')
        base_url = base_url.format(TimeStamp().timeStamp())
        r = requests.get(url=base_url, headers=header, verify=False)
        try:
            assert r.json().get('status') == 0
            return r.json().get('data').get('randomId'), r.json().get('data').get('randomCode')
        except Exception as e:
            do_log.logOutput("error", "获取秘钥失败")
            do_log.logOutput("error", traceback.format_exc())
            raise e

    def login(self, indata=None, token=True):
        '''
        登录接口封装
        :param indata:接口传参,默认值为变量user/passwd
        :param token:token值默认为True,获取token值
        :return:默认返回token值，变量token为false时，返回登录状态
        '''
        if indata is None:
            indata = {'userName': user, 'userPwd': passwd}
        requests.packages.urllib3.disable_warnings()
        base_url, header, param_data = GetExcelConetnt().getExcelConetnt(
            filePath().testData_login_Path() + '/登录接口.xlsx', 2)
        base_url = base_url.format(TimeStamp().timeStamp())
        # 获取秘钥
        randomId, randomCode = self.randomCode()
        # 接口传参
        indata.update({'userPwd': encrypt(passwd, randomCode), 'randomId': randomId})
        r = requests.post(url=base_url, json=indata, headers=header, verify=False)
        try:
            if token:
                # do_log.logOutput("info","登录成功，获取token正常")
                return r.json()['data']['token']
            else:
                return r.json().get('status')
        except Exception as e:
            do_log.logOutput("error", "登录接口错误,传入的接口参数为{},返回的结果为{}".format(r.request.body, r.json()))
            do_log.logOutput("error", traceback.format_exc())
            raise e


if __name__ == '__main__':
    randomCode = Login()
    # randomCode.randomCode()
    print(randomCode.login())
