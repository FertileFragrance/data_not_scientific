#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: njuselhx
@Time: 2021/1/21 下午7:01
@File: train.py
@Software: PyCharm
"""
from magpie import Magpie
magpie = Magpie()
magpie.init_word_vectors('data/hep-categories-zh', vec_dim=100)
labels = ['军事', '旅游', '政治']
magpie.train('data/hep-categories-zh', labels, test_ratio=0.2, epochs=100)
magpie.save_model('save/keras_model_zh.h5')
magpie.save_word2vec_model('save/word2vec_model_zh', overwrite=True)
magpie.save_scaler('save/scaler_zh', overwrite=True)
print(magpie.predict_from_text('特朗普在联合国大会发表演讲谈到这届美国政府成绩时，称他已经取得了美国历史上几乎最大的成就。随后大会现场传出了嘲笑声，特朗普立即回应道：“这是真的。”'))
