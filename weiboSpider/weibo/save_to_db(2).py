import pymongo
import re

client = pymongo.MongoClient(host='124.70.84.12', port=27017, username="pkun", password="lcyyds")
db = client['weibo_content']
collection = db['people_daily']
with open('人民日报\\人民日报微博(2).csv', 'r', encoding='utf-8') as f:
    info_list = []
    for line in f:
        info_list.append(str(line))


for each in info_list:
    piece_list = each.split(',')
    wid = piece_list[0]
    content = piece_list[1]
    time = piece_list[2]
    up_num = piece_list[3]
    transmit_num = piece_list[4]
    comment_num = piece_list[5].split('\n')[0]
    data = {
        'wid': wid,
        'content': content,
        'time': time,
        'up_num': up_num,
        'transmit_num': transmit_num,
        'comment_num': comment_num
    }
    collection.insert_one(data)
