#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: njuselhx
@Time: 2021/1/21 下午2:04
@File: test.py
@Software: PyCharm
"""
from magpie import Magpie
# labels = ['Gravitation and Cosmology', 'Experiment-HEP', 'Theory-HEP']
labels = ['军事', '旅游', '政治']
magpie = Magpie(
    keras_model='save/keras_model_zh.h5',
    word2vec_model='save/word2vec_model_zh',
    scaler='save/scaler_zh',
    labels=labels
)
# print(magpie.predict_from_file('data/hep-categories/1002413.txt'))
print(magpie.predict_from_text('特朗普在联合国大会发表演讲谈到这届美国政府成绩时，称他已经取得了美国历史上几乎最大的成就。随后大会现场传出了嘲笑声，特朗普立即回应道：“这是真的。”'))
