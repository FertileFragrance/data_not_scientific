#!/opt/anaconda3/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: njuselhx
@Time: 2020/12/26 下午5:59
@File: crawl_executor.py
@Software: PyCharm
"""
import os
import subprocess
from datetime import datetime, timedelta

'''设置开始日期'''
current_date = '2020-05-18'
# 将字符串类型的日期转换成datetime类型以便增长
current_date = datetime.strptime(current_date, '%Y-%m-%d')
'''设置搜索结束日期'''
last_date = '2020-05-24'
last_date = datetime.strptime(last_date, '%Y-%m-%d')


def pre_work():
    # 进入微博爬虫工作目录
    os.chdir('weibo-search')


def change_date_to_string():
    global current_date
    # 将日期转换为字符串类型以设置START_DATE
    current_date = str(current_date).split(' ')[0]


def change_date_from_string():
    global current_date
    # 将字符串类型的日期转换成datetime类型以便增长
    current_date = datetime.strptime(current_date, '%Y-%m-%d')


def increase_date():
    global current_date
    # 日期加一
    current_date = current_date + timedelta(days=1)


def modify_date():
    global current_date
    file_data = ''
    with open('weibo/settings.py', 'r', encoding='utf-8') as f:
        for line in f:
            if 'START_DATE' in line:
                line = line.replace(line, "START_DATE = '" + current_date + "'\n")
            if 'END_DATE' in line:
                line = line.replace(line, "END_DATE = '" + current_date + "'\n")
            file_data += line
    with open('weibo/settings.py', 'w', encoding='utf-8') as f:
        f.write(file_data)


def execute():
    global current_date
    global last_date
    while current_date <= last_date:
        change_date_to_string()
        modify_date()
        # 执行爬虫
        print(subprocess.getoutput('scrapy crawl search'))
        change_date_from_string()
        increase_date()


if __name__ == '__main__':
    pre_work()
    execute()
