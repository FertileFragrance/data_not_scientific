#!/opt/anaconda3/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: njuselhx
@Time: 2021/1/19 上午12:37
@File: compute_by_jieba.py
@Software: PyCharm
"""
import jieba.analyse
import pymongo

client = pymongo.MongoClient(host='124.70.84.12', port=27017, username='pkun', password='lcyyds')
collection = client['dataScience'].get_collection('stage4')
documents = collection.find({})
doc_content_list = []
for document in documents:
    doc_content_list.append(document['content'])
res = []
for doc in doc_content_list:
    keyword_list = jieba.analyse.extract_tags(doc, topK=10)
    for keyword in keyword_list:
        if keyword not in res:
            res.append(keyword)
with open('keyword/stage4_by_jieba.txt', 'w', encoding='utf-8') as f:
    f.write('------结巴分词自身基于tf-idf筛选出的关键词，无先后顺序之分------' + '\n')
    for r in res:
        f.write(r + '\n')
    f.flush()
