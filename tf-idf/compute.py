#!/opt/anaconda3/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: njuselhx
@Time: 2021/1/18 下午8:34
@File: compute.py
@Software: PyCharm
"""
import math

import jieba
import pymongo


def tokenize(data):
    words = jieba.cut(data)
    word_list = []
    for word in words:
        word_list.append(word)
    return word_list


def compute_frequency(word_list):
    frequency_dict = {}
    for word in word_list:
        if frequency_dict.get(word) is None:
            frequency_dict[word] = 1
        else:
            frequency_dict[word] = frequency_dict[word] + 1
    # print(frequency_dict)
    for key in frequency_dict.keys():
        frequency_dict[key] = frequency_dict[key] / len(word_list)
    # print(frequency_dict)
    return frequency_dict


def connect_db():
    client = pymongo.MongoClient(host='124.70.84.12', port=27017, username="pkun", password="lcyyds")
    # 在此修改要连接的集合和要获取的文档
    collection = client['dataScience'].get_collection('stage4')
    documents = collection.find({})
    doc_content_list = []
    for document in documents:
        doc_content_list.append(document['content'])
    # 返回的列表里都是字符串
    return doc_content_list


def select_top_words(frequency_dict, top_n):
    # print(sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True))
    word_frequency_list = sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True)
    res = []
    ii = 0
    for word_frequency in word_frequency_list:
        res.append(word_frequency)
        ii = ii + 1
        if ii == top_n:
            break
    return res


def compute_idf(all_top_words_list_arg, content_list_arg):
    idf_dict_arg = {}
    for top_word in all_top_words_list_arg:
        if top_word[0] not in idf_dict_arg.keys():
            idf_dict_arg[top_word[0]] = 0
        for content_arg in content_list_arg:
            if top_word[0] in content_arg:
                idf_dict_arg[top_word[0]] = idf_dict_arg[top_word[0]] + 1
    for key in idf_dict_arg.keys():
        idf_dict_arg[key] = math.log10(len(content_list_arg) / idf_dict_arg[key])
    return idf_dict_arg


def filtrate(words_list):
    res = []
    for word in words_list:
        if len(word) < 2 or word.isdigit():
            continue
        res.append(word)
    return res


def multiply_tf_idf(tf_list, idf_dict_arg):
    res = {}
    for word_frequency in tf_list:
        res[word_frequency[0]] = word_frequency[1] * idf_dict_arg[word_frequency[0]]
    res = sorted(res.items(), key=lambda x: x[1], reverse=True)
    return res


def save_file(words_list):
    with open('keyword/stage4.txt', 'w', encoding='utf-8') as f:
        for word in words_list:
            f.write(word + '\n')
        f.flush()


if __name__ == '__main__':
    content_list = connect_db()
    all_top_words_list = []
    for content in content_list:
        content_frequency_dict = compute_frequency(tokenize(content))
        top_words_list = select_top_words(content_frequency_dict, 20)
        # print(top_words_list)
        for i in range(0, len(top_words_list)):
            is_found = False
            save_j = -1
            for j in range(0, len(all_top_words_list)):
                if top_words_list[i][0] == all_top_words_list[j][0]:
                    is_found = True
                    save_j = j
                    break
            if not is_found:
                all_top_words_list.append(top_words_list[i])
            elif top_words_list[i][1] > all_top_words_list[save_j][1]:
                del all_top_words_list[save_j]
                all_top_words_list.append(top_words_list[i])
    # print(len(all_top_words_list))
    # print(all_top_words_list)
    idf_dict = compute_idf(all_top_words_list, content_list)
    # print(idf_dict)
    keywords = multiply_tf_idf(all_top_words_list, idf_dict)
    # print(keywords)
    pure_keywords = []
    for keyword in keywords:
        pure_keywords.append(keyword[0])
    pure_keywords = filtrate(pure_keywords)
    # print(pure_keywords)
    save_file(pure_keywords)
