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

number=len(tickers)
initial_weights=np.repeat(1/number, number)
weighted_stock_return=stock_return.mul(initial_weights, axis=1)
stock_return_port=weighted_stock_return.sum(axis=1)
initial_return=(stock_return_port.mean() *252)
initial_std=np.sqrt(np.dot(initial_weights.T,np.dot(stock_return.cov()*252,initial_weights)))

print(initial_weights)
print(initial_return)
print(initial_std)