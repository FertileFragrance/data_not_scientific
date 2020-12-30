# -*- coding:utf-8 -*-
# datetime:2020/12/12 12:36 下午
# author:macbookair
import pymongo

myclient=pymongo.MongoClient(host="124.70.84.12",port=27017)
mydb=myclient["dataScience"] #创建数据库
#dblist=client.list_database_names()
dblist = myclient.database_names()
# dblist = myclient.database_names()
mycol2=mydb["stage2"]
mycol = mydb["stage1"]
mycol3=mydb["stage3"]
mycol4=mydb["stage4"]
x=mycol.find_one()
print(x)
# x = mycol4.delete_many({})
#
# print(x.deleted_count, "个文档已删除")
collist = mydb. list_collection_names()
# for x in mycol2.find():
#   print(x)
# collist = mydb.collection_names()
# if "dataScience" in dblist:
#   print("数据库已存在！")
# else:
#     print("meiyou")
# if "sites" in collist:   # 判断 sites 集合是否存在
#   print("集合已存在！")
# for i in dblist:
#     print(i)