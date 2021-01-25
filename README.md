# data_not_scientific

**来看大作业的，麻烦给个Star再走啊喂~**

## 项目结构

只列出非普遍功能或者比较重要的目录和文件。

```
.
├─magpie							# 机器学习模块
	├─data							# 进行训练的数据集和测试结果目录
    ├─magpie						# 机器学习核心代码，经修改后支持中文
    └─save							# 训练好模型之后的保存目录
    ├─test.py						# 测试数据并存入文件
    ├─test_by_cnsenti.py			# 用cnsenti库测试数据并存入文件
    └─train.py						# 训练模型脚本
├─predict							# 心态预测模块
	├─predict-res					# 预测结果目录
    ├─checkout.py					# 确定ARIMA模型参数的脚本
    ├─emotion_frequency.xlsx		# 进行预测的现有数据
    └─predict.py					# 预测脚本
├─tf-idf							# 关键词提取模块
	├─keyword						# 得到的关键词
    ├─compute.py					# 用tf-idf算法计算出关键词并存入文件
    └─compute_by_jieba.py			# 使用jieba内置的函数提取关键词并存入文件
├─weibo-search						# 微博关键词搜索爬虫模块
	├─crawls						# 爬虫的缓存文件目录
    └─weibo						# 爬虫的核心代码
    	├─spiders					# 执行爬虫
    	├─utils					# 工具包
    	└─settings.py				# 爬虫全局设置
├─weiboSpider						# 微博博文爬虫模块
	├─weibo						# 结果目录
    ├─weibo_spider					# 爬虫的核心代码
    └─config.json					# 爬虫全局设置
├─word-cloud						# 词云制作模块
	├─font							# 显示的字体目录
    ├─image						# 词云的掩膜和结果保存目录
    └─word_cloud.ipynb				# 词云绘制脚本
├─xinLang news						# 新浪新闻爬虫模块
│  └─main.py						# 执行爬虫
└─crawl_executor.py				# 微博关键词爬虫自动管理脚本
```

## 项目流程

### 环境搭建

`mongodb`环境

```shell
(base) njuselhx@njuselhx-LinuxPC:~$ mongosh "mongodb://124.70.84.12:27017" --username pkun
Enter password: ******Current sessionID:  600ef3958d3bd627df8e6b34
Connecting to:    mongodb://124.70.84.12:27017
Using MongoDB:      3.6.3
Using Mongosh Beta: 0.6.1

For more information about mongosh, please see our docs: https://docs.mongodb.com/mongodb-shell/


To help improve our products, anonymous usage data is collected and sent to MongoDB periodically (https://www.mongodb.com/legal/privacy-policy).
You can opt-out by running the disableTelemetry() command.

>
```

`Python`环境

```shell
(base) njuselhx@njuselhx-LinuxPC:~$ python -V
Python 3.8.3
(base) njuselhx@njuselhx-LinuxPC:~$ python3.7 -V
Python 3.7.3
(base) njuselhx@njuselhx-LinuxPC:~$ pip -V
pip 20.3.3 from /opt/anaconda3/lib/python3.8/site-packages/pip (python 3.8)
(base) njuselhx@njuselhx-LinuxPC:~$ pip3.7 -V
pip 20.2.4 from /home/njuselhx/.local/lib/python3.7/site-packages/pip (python 3.7)
```

注意一定要有一个`Python 3.7`及以下的`Python3`版本，因为所需的依赖`tensorflow~=1.15.2`只能在`Python 3.7`及以下的版本安装。

至于要用到的全部依赖没有专门整理到`requirements.txt`，有些模块有所整理，除了这些还有常用的如`pandas` `matplotlib`之类，没有很少见的依赖，可自行到脚本中查看。

`Jupyter`环境

```shell
(base) njuselhx@njuselhx-LinuxPC:~$ jupyter --version
jupyter core     : 4.7.0
jupyter-notebook : 6.1.6
qtconsole        : 5.0.1
ipython          : 7.19.0
ipykernel        : 5.4.2
jupyter client   : 6.1.7
jupyter lab      : 3.0.0
nbconvert        : 6.0.7
ipywidgets       : 7.6.2
nbformat         : 5.0.8
traitlets        : 5.0.5
```

### 执行步骤

首先执行爬虫，三个爬虫模块无固定先后顺序，亦可同时执行。注意，在执行微博关键词搜索爬虫模块和微博博文爬虫模块之前要正确地改写配置文件，包括但不限于设置起止日期、设置Cookie等，进入模块有具体的说明。如果要批量爬取微博关键词搜索结果，则需要在`crawl_executor.py`中设置起止日期。

爬取完成后，接下来就可以利用数据了。用新浪新闻的数据，我们不难以集合为一个小型语料库计算出该集合的文档中各个词的tf-idf值，从大到小排序后可以得到关键词；我们划分了9个心态标签，用微博评论的数据手动地给每个标签标记了100条数据，以此作为机器学习的训练用数据集。

接上述思路，拿到关键词，很容易用`wordcloud`依赖制作词云；而机器学习的模型训练完成之后，就可以用模型对数据——微博关键词搜索爬取的博文——进行心态分析，统计频率并保存。

到此，我们已经获得了从2019-12-08到2020-06-30之前的网络公众心态频率数据，进一步地，对未来一段时间内心态进行预测是很具有现实意义的，于是就到了`predict`模块，它使用时间序列中的ARIMA模型进行预测。

## 致谢

### 提供服务器的好心人

https://github.com/pppppkun

### Magpie开源库

https://github.com/inspirehep/magpie

### 微博关键词搜索爬虫项目

https://github.com/inspirehep/magpie

### 微博博文爬虫项目

https://github.com/dataabc/weiboSpider

## 许可证

[Apache License 2.0](https://github.com/FertileFragrance/data_not_scientific/blob/main/LICENSE)

Copyright (c) 2020 FertileFragrance