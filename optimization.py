#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 21:38:30 2019

@author: a0
"""

import pandas as pd
import numpy as np
#从本地读取股票数据
stock_data={}
tickers=['CAT','BA']
for ticker in tickers:
    filename=ticker+'.txt'
    data=pd.read_csv(filename, index_col=1)
    stock_data[ticker]=data

#提取收盘价，置入数据框中，按日期排序，计算收益并删去第一行缺省值
stock_final_data=pd.DataFrame()
for ticker in tickers:
    stock_final_data[ticker]=stock_data[ticker]['Close']
     #stock_final_data[ticker]=stock_data[ticker].loc['2013':'2018','5. adjusted close']
stock_final_data=stock_final_data.sort_values(by='Date')
stock_return=stock_final_data.pct_change().dropna()

#产生随机权重，计算收益、波动率以及夏普比率
np.random.seed(30)
sim_ports = 6000

weights_of_stocks = np.zeros((sim_ports, len(tickers)), dtype=np.float64)
return_array = np.zeros(sim_ports, dtype=np.float64)
volatility_array = np.zeros(sim_ports, dtype=np.float64)
var_array = np.zeros(sim_ports, dtype=np.float64)

for x in range(sim_ports):
    #Randomizing the weights
    weights = np.array(np.random.random(len(tickers)))
    weights = weights/np.sum(weights)
    
    #Save Weights to our array
    weights_of_stocks[x,:] = weights
    
    # Calculating the expected return for the portfolio
    return_array[x] = ((np.sum( (stock_return.mean() * weights))))*252
    
    var_array[x] = np.dot(weights.T,np.dot(stock_return.cov()*252,weights))
    
    #Calculating the Volatility
    volatility_array[x] = np.sqrt(np.dot(weights.T, np.dot(stock_return.cov()*252, weights)))
 
ls = return_array
number = 0.3 # 输入的数
ls_cul = ls - number  # 求距离
ls_abs = abs(ls_cul)  # 求绝对值
argmin = ls_abs.argmin()  # 求最小值位置
print(return_array[argmin])

max_var = var_array[argmin]
max_std = np.sqrt(max_var)

print('Risk is: {}'.format(max_std))
print('Index of portfolio: {}'.format(ls_abs.argmin()))
print(weights_of_stocks[ls_abs.argmin(),:])

max_ret = return_array[var_array.argmin()]
max_vol = volatility_array[var_array.argmin()]













