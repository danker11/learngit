# !/usr/bin/python3
# -*- coding: utf-8 -*-

'''
获取时间戳
获取linux服务器时间
'''

import time
import datetime

class TimeStamp():
    def timeStamp(self):
        '''
        将当前时间转换为毫秒时间戳
        '''
        time_now = datetime.datetime.now()
        # 转换后的字符类型是int类型的
        obj_temp = int(time.mktime(time_now.timetuple()) * 1000 + time_now.microsecond / 1000)
        return str(obj_temp)

    def timeCurrent(self, ti=1,day=None):
        '''
        默认获取当前时间，2，获取后面几天的时间；3获取已经过去的时间
        :param ti:
        :param day:
        :return:
        '''
        datetime.datetime.now()
        if ti == 1:
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif ti == 2:
            return (datetime.datetime.now() + datetime.timedelta(days=day)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            return (datetime.datetime.now() - datetime.timedelta(days=day)).strftime("%Y-%m-%d %H:%M:%S")

    def timeMinute(self,min=1,n=None):
        datetime.datetime.now()
        if min == 1:
            return datetime.datetime.now().strftime("%H:%M")
        elif min == 2:
            return (datetime.datetime.now() + datetime.timedelta(hours=n)).strftime("%H:%M")
        else:
            return (datetime.datetime.now() - datetime.timedelta(hours=n)).strftime("%H:%M")

    def server_time_transform(self,results,weeks = 0,days = 0,hours = 0,minutes = 0,seconds = 0,microseconds = 0,milliseconds = 0):
        '''
        获取linux服务器时间，前后x分钟作为拓展规则时间段的开始及结束时间
        '''
        for ele in results:
            if ((':' in ele) == True):
                time_str = '2020-01-01 ' + ele
                time_str = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                start_time = time_str - datetime.timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds,
                                                           microseconds=microseconds, milliseconds=milliseconds)
                start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
                end_time = time_str + datetime.timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds,
                                                         milliseconds=milliseconds)
                end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
                return start_time[-8:-3],end_time[-8:-3]




if __name__ == '__main__':
    print(TimeStamp().timeStamp())
    print(TimeStamp().timeCurrent(2,1))
    print(TimeStamp().timeMinute(3,2))