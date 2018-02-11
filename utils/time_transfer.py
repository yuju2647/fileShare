#!usr/bin/env python
#coding=utf-8

__author__ = 'yujun huang'

import time
import datetime

def time_to_timestamp(time_str):
    """
    :param time_str: 字符串类型，格式：'%Y-%m-%d %H:%M:%S'
    :return: 返回 int 类型的 unix_timestamp
    """
    return time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S'))

def timestamp_to_time(timestamp,format='%Y-%m-%d %H:%M:%S'):
    """
    :param timestamp: 若 timestamp 是None 则，返回的是当前时刻时间
    :return: 返回格式：默认为%Y-%m-%d %H:%M:%S
    """
    if not timestamp:
        return None
    st=time.gmtime(timestamp)
    date_time=datetime.datetime(year=st.tm_year,
                                month=st.tm_mon,
                                day=st.tm_mday,
                                hour=st.tm_hour,
                                minute=st.tm_min,
                                second=st.tm_sec)
    date_time+=datetime.timedelta(hours=8)
    return date_time.strftime(format)

def strtime_timedelta(strtime, default='%Y%m%d', day_move=0):
    year = int(strtime[0:4])
    month = int(strtime[4:6])
    day = int(strtime[6:8])
    date = datetime.datetime(year=year, month=month, day=day)
    if day_move:
        date += datetime.timedelta(days=day_move)
    return date.strftime(default)

if __name__ == '__main__':
    strtime_to_datetime('20180213')






