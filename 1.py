#__author:"LIN SHIH-WAI"
#date:  2017/11/11
import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

f=open(r'代码.txt','r+',encoding='utf-8')
k=f.read()
c=k.split('\n')


# df=ts.get_hist_data('600000',ktype='D',start='2017-01-01',end='2017-11-11')
# df=df.loc[:,'close']
dict1={}
for i in c:
    z=ts.get_hist_data(i, ktype='D', start='2017-01-01', end='2017-11-11')
    z=z.loc[:,'close']
    dict1.setdefault(i,z)
df=pd.DataFrame(dict1)
df.to_excel('保存测试.xlsx')
df=df.dropna(axis=0,how='any')#任何有确实数据就删掉行
df.to_excel('对缺失数据已经处理完毕.xlsx')
returns = np.log(df/df.shift(1))#求出每日的收益
long=len(c)

dfm=returns.mean()
dfv=returns.var()
df2=pd.DataFrame([dfm,dfv],index=['期望','方差'])
print(df2)
df2=df2.T
df2.to_excel('第二个组合的方差和期望.xlsx')


port_returns = []
port_variance = []
for p in range(8000000):
    weights = np.random.random(long)
    weights /=np.sum(weights)
    port_returns.append(np.sum(returns.mean()*365*weights))
    port_variance.append(np.sqrt(np.dot(weights.T, np.dot(returns.cov()*365, weights))))

port_returns = np.array(port_returns)
port_variance = np.array(port_variance)

#无风险利率设定为4%
risk_free = 0.04
plt.figure(figsize = (8,4))
plt.scatter(port_variance, port_returns, c=(port_returns-risk_free)/port_variance, marker = 'o')
plt.grid(True)
plt.xlabel('excepted volatility')
plt.ylabel('expected return')
plt.colorbar(label = 'Sharpe ratio')
plt.savefig("examples.png")