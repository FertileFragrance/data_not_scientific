#!/opt/anaconda3/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: njuselhx
@Time: 2021/1/25 下午8:26
@File: test_by_cnsenti.py
@Software: PyCharm
"""
import pymongo
import datetime
from cnsenti import Emotion

emotion = Emotion()
emotion_dict = {
    '好': 0,
    '乐': 0,
    '哀': 0,
    '怒': 0,
    '惧': 0,
    '恶': 0,
    '惊': 0
}
with open('data/emotion_frequency_by_cnsenti.csv', 'a+', encoding='utf-8') as f:
    f.write('日期,好,乐,哀,怒,惧,恶,惊' + '\n')
client = pymongo.MongoClient(host='124.70.84.12', port=27017, username="pkun", password="lcyyds")
db = client['weibo_keyword_epidemic']
date = '2020-03-16'
while datetime.datetime.strptime(date, '%Y-%m-%d') <= datetime.datetime.strptime('2020-06-30', '%Y-%m-%d'):
    print(date)
    collection = db[date]
    documents_obj = collection.find({})
    for i in range(0, min(collection.count_documents({}), 3000)):
        res = emotion.emotion_count(documents_obj[i]['text'])
        for key in res.keys():
            if key == 'words' or key == 'sentences':
                continue
            emotion_dict[key] = emotion_dict[key] + res[key]
    with open('data/emotion_frequency_by_cnsenti.csv', 'a+', encoding='utf-8') as f:
        f.write(date + ',')
        f.write(str(emotion_dict['好']) + ',')
        f.write(str(emotion_dict['乐']) + ',')
        f.write(str(emotion_dict['哀']) + ',')
        f.write(str(emotion_dict['怒']) + ',')
        f.write(str(emotion_dict['惧']) + ',')
        f.write(str(emotion_dict['恶']) + ',')
        f.write(str(emotion_dict['惊']) + '\n')
    for key in emotion_dict.keys():
        emotion_dict[key] = 0
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    date = date + datetime.timedelta(days=1)
    date = str(date).split(' ')[0]
