#!/opt/anaconda3/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: njuselhx
@Time: 2021/1/25 下午1:28
@File: checkout.py
@Software: PyCharm
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.pylab import style  # 自定义图表风格
from IPython.core.interactiveshell import InteractiveShell
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf  # 自相关图、偏自相关图
InteractiveShell.ast_node_interactivity = "all"
style.use('ggplot')
# 解决中文乱码问题
plt.rcParams['font.sans-serif'] = ['simhei']
# 解决坐标轴刻度负号乱码
plt.rcParams['axes.unicode_minus'] = False

# 读取数据并展示
data = pd.read_excel('./emotion_frequency.xlsx', index_col='日期', usecols='A, J')
plt.figure(figsize=(10, 5))
data.plot()
plt.show()
# 展示原始数据的自相关图
plot_acf(data, lags=200).show()
# 展示原始数据的偏自相关图
plot_pacf(data, lags=99).show()

# 计算一阶差分并展示
d1_data = data.diff(periods=1, axis=0).dropna()
plt.figure(figsize=(10, 5))
d1_data.plot()
plt.show()
# 展示一阶差分的自相关图
plot_acf(d1_data, lags=199).show()
# 展示一阶差分的偏自相关图
plot_pacf(d1_data, lags=99).show()

# 计算二阶差分并展示
d2_data = data.diff(periods=1, axis=0).dropna()
plt.figure(figsize=(10, 5))
d2_data.plot()
plt.show()
# 展示二阶差分的自相关图
plot_acf(d2_data, lags=198).show()
# 展示二阶差分的偏自相关图
plot_pacf(d2_data, lags=98).show()
