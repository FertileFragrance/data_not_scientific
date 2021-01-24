#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: njuselhx
@Time: 2021/1/21 下午2:04
@File: test.py
@Software: PyCharm
"""
import pymongo
import datetime
from magpie import Magpie
# labels = ['Gravitation and Cosmology', 'Experiment-HEP', 'Theory-HEP']

# labels = ['军事', '旅游', '政治']
# magpie = Magpie(
#     keras_model='save/keras_model_zh.h5',
#     word2vec_model='save/word2vec_model_zh',
#     scaler='save/scaler_zh',
#     labels=labels
# )
# # print(magpie.predict_from_file('data/hep-categories/1002413.txt'))
# print(magpie.predict_from_text('特朗普在联合国大会发表演讲谈到这届美国政府成绩时，称他已经取得了美国历史上几乎最大的成就。随后大会现场\
# 传出了嘲笑声，特朗普立即回应道：“这是真的。”此外，美军方也有专门的低轨甚至超低轨小型卫星星座计划，这些卫星不仅可用于通信和侦察，还可用于支援反高超音速导弹作战。'))
# print(magpie.predict_from_text('此外，美军方也有专门的低轨甚至超低轨小型卫星星座计划，这些卫星不仅可用于通信和侦察，还可用于支援反高超\
# 音速导弹作战。特朗普在联合国大会发表演讲谈到这届美国政府成绩时，称他已经取得了美国历史上几乎最大的成就。随后大会现场传出了嘲笑声，特朗普立即回应道：“这是真的。”'))

labels = ['满意', '喜悦', '乐观', '愤怒', '悲哀', '恐惧', '厌恶', '焦虑', '怀疑']
magpie = Magpie(
    keras_model='save/emotion_keras_model.h5',
    word2vec_model='save/emotion_word2vec_model',
    scaler='save/emotion_scaler',
    labels=labels
)
# print(magpie.predict_from_text('害怕，恐怖如斯'))
# print(magpie.predict_from_text('气死我了'))
# print(magpie.predict_from_text('加油，很快就会好的'))
# print(magpie.predict_from_text('希望早日康复'))
# print(magpie.predict_from_text('英国航母战斗群已于1月达到初始作战能力，这标志着英国海军投射力量能力的一个阶段性变化。'))
# print(magpie.predict_from_text('近年来伊朗、叙利亚、缅甸正逐渐成为朝鲜核技术和导弹技术出口的主要客户，其中伊朗所占的比重较高。'))

emotion_dict = {
    '满意': 0,
    '喜悦': 0,
    '乐观': 0,
    '愤怒': 0,
    '悲哀': 0,
    '恐惧': 0,
    '厌恶': 0,
    '焦虑': 0,
    '怀疑': 0
}
client = pymongo.MongoClient(host='124.70.84.12', port=27017, username="pkun", password="lcyyds")
db = client['weibo_keyword_epidemic']
date = '2019-12-08'
with open('data/emotion_frequency.csv', 'a+', encoding='utf-8') as f:
    f.write('日期,满意,喜悦,乐观,愤怒,悲哀,恐惧,厌恶,焦虑,怀疑' + '\n')
while datetime.datetime.strptime(date, '%Y-%m-%d') <= datetime.datetime.strptime('2020-01-08', '%Y-%m-%d'):
    print(date)
    collection = db[date]
    documents_obj = collection.find({})
    for i in range(0, min(collection.count_documents({}), 3000)):
        # print(documents_obj[i]['text'])
        # 拿到每一条微博的情感分析结果
        res = magpie.predict_from_text(documents_obj[i]['text'])
        # 如果最大的数字小于0.75表明没有明显的情绪，跳过
        if res[0][1] < 0.75:
            continue
        # 第二大的数字比最大的数字小0.05以上则只保留第一个
        if res[0][1] - res[1][1] > 0.05:
            emotion_dict[res[0][0]] = emotion_dict[res[0][0]] + 1
            continue
        # 第三大的数字比第二大的数字小0.03以上则只保留前两个
        if res[1][1] - res[2][1] > 0.03:
            emotion_dict[res[0][0]] = emotion_dict[res[0][0]] + 1 / 2
            emotion_dict[res[1][0]] = emotion_dict[res[1][0]] + 1 / 2
            continue
        # 保留前三个
        emotion_dict[res[0][0]] = emotion_dict[res[0][0]] + 1 / 3
        emotion_dict[res[1][0]] = emotion_dict[res[1][0]] + 1 / 3
        emotion_dict[res[2][0]] = emotion_dict[res[2][0]] + 1 / 3

    with open('data/emotion_frequency.csv', 'a+', encoding='utf-8') as f:
        f.write(date + ',')
        f.write(str(round(emotion_dict['满意'], 2)) + ',')
        f.write(str(round(emotion_dict['喜悦'], 2)) + ',')
        f.write(str(round(emotion_dict['乐观'], 2)) + ',')
        f.write(str(round(emotion_dict['愤怒'], 2)) + ',')
        f.write(str(round(emotion_dict['悲哀'], 2)) + ',')
        f.write(str(round(emotion_dict['恐惧'], 2)) + ',')
        f.write(str(round(emotion_dict['厌恶'], 2)) + ',')
        f.write(str(round(emotion_dict['焦虑'], 2)) + ',')
        f.write(str(round(emotion_dict['怀疑'], 2)) + '\n')

    for key in emotion_dict.keys():
        emotion_dict[key] = 0

    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    date = date + datetime.timedelta(days=1)
    date = str(date).split(' ')[0]
