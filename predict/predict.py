#!/opt/anaconda3/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: njuselhx
@Time: 2021/1/25 下午1:26
@File: predict.py
@Software: PyCharm
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import style  # 自定义图表风格
from IPython.core.interactiveshell import InteractiveShell
from statsmodels.tsa.arima_model import ARIMA
InteractiveShell.ast_node_interactivity = "all"
style.use('ggplot')

# 解决中文乱码问题
plt.rcParams['font.sans-serif'] = ['simhei']
# 解决坐标轴刻度负号乱码
plt.rcParams['axes.unicode_minus'] = False


data = pd.read_excel('./emotion_frequency.xlsx', index_col='日期', usecols='A, J', skipfooter=1)
# 创建模型
model = ARIMA(data, (1, 1, 2)).fit()
# 查看模型报告
# model.summary2()
# print(model.forecast(120))
forecast = pd.Series(model.forecast(120)[0], index=pd.date_range('2020-07-01', periods=120, freq='D'))
print(forecast)
data = pd.concat((data, forecast), axis=0)
data.columns = ['怀疑', '未来预测']
plt.figure(figsize=(10, 5))
data.plot()
plt.show()
