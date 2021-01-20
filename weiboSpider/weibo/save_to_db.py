#!/opt/anaconda3/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: njuselhx
@Time: 2021/1/21 上午12:25
@File: save_to_db.py
@Software: PyCharm
"""
import pymongo
import datetime

client = pymongo.MongoClient(host='124.70.84.12', port=27017, username="pkun", password="lcyyds")
db = client['weibo_comment']
collection = db['southern_weekly']
with open('南方周末评论.csv', 'r', encoding='utf-8') as f:
    file_data = ''
    for line in f:
        file_data += line.strip('\n')
info_list = file_data.split('https://weibo.com/')
# print(info_list[0])
del info_list[0]
for each in info_list:
    piece_list = each.split(',')
    if len(piece_list) != 18:
        continue
    if piece_list[11] == '' and piece_list[15] == '':
        continue
    # piece_list[0]是博文网址，需要其wid
    wid = piece_list[0].split('?')[0].split('/')[1]
    # piece_list[11]是一级评论内容
    first_level_comment = piece_list[11]
    # piece_list[12]是一级评论时间
    temp = datetime.datetime.strptime(piece_list[12].split(' ')[0], '%Y-%m-%d')
    first_level_time = str(temp).split(' ')[0]
    # piece_list[13]是一级评论点赞数
    first_level_good_time = piece_list[13]
    if first_level_good_time == '':
        first_level_good_time = 0
    else:
        first_level_good_time = int(first_level_good_time)
    # piece_list[15]是二级评论内容
    second_level_comment = piece_list[15].strip('"').strip()
    if second_level_comment != '':
        # piece_list[16]是二级评论时间
        if '12月' in piece_list[16]:
            piece_list[16] = piece_list[16].replace('12月', '2019-12-')
        elif '月' in piece_list[16]:
            piece_list[16] = piece_list[16].replace('月', '-')
            piece_list[16] = '2020-' + piece_list[16]
        if '日' in piece_list[16]:
            piece_list[16] = piece_list[16].replace('日', '')
        temp = datetime.datetime.strptime(piece_list[16].split(' ')[0], '%Y-%m-%d')
        second_level_time = str(temp).split(' ')[0]
        # piece_list[17]是二级评论点赞数
        second_level_good_time = piece_list[17]
        if second_level_good_time == '':
            second_level_good_time = 0
        else:
            second_level_good_time = int(second_level_good_time)
    data = {
        'wid': wid,
        'comment': first_level_comment,
        'date': first_level_time,
        'support': first_level_good_time
    }
    if collection.count_documents({'comment': first_level_comment}) == 0:
        collection.insert_one(data)
    if second_level_comment != '':
        data = {
            'wid': wid,
            'comment': second_level_comment,
            'date': second_level_time,
            'support': second_level_good_time
        }
        collection.insert_one(data)
