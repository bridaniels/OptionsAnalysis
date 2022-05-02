# Import libraries
import CONFIG as c
import pandas as pd 
import numpy as np
from pandas_datareader import data as web
from datetime import datetime,date
from scipy.stats import norm
from math import log, sqrt, pi, exp 

# Import Data 
df = web.DataReader(name=c.stock, data_source=c.dataSource, start=c.one_yr_ago, end=c.today)
df = df.sort_values(by='Date')
df = df.dropna()
df = df.assign(close_day_before=df.Close.shift(1))
df['returns'] = ((df.Close-df.close_day_before) / df.close_day_before)
# df.info()


# Collecting Variables 
# Sigma: Volatility 
sigma = np.sqrt(c.tradingDays) * df['returns'].std()
# r: Risk-Free Rate (from 10yr US T-YIELD '^TNX')
usTY10 = "^TNX"
riskFree = (web.DataReader(name=usTY10, data_source=c.dataSource, start=c.today.replace(day=c.today.day-1), end=c.today) ['Close'].iloc[-1]) / 100
# s: Current Stock Price/Spot Price/Last Close Price
lastCloseP = df['Close'].iloc[-1]
# t: Time to Maturity 
tMature = (datetime.strptime(c.expiration, "%m-%d-%Y") - datetime.utcnow()).days / 365
# print(sigma,riskFree,lastCloseP,tMature)


# Calculate Risk-Adjusted Probability Factors D1 and D2 
def d1(s,k,t,r,sigma):
    return (log(s/k) + (r+sigma**2/2) * t) / (sigma*sqrt(t))
def d2(s,k,t,r,sigma):
    return d1(s,k,t,r,sigma) - sigma*sqrt(t)
prob1 = d1(lastCloseP, c.strike_price, tMature, riskFree, sigma)
prob2 = d2(lastCloseP, c.strike_price, tMature, riskFree, sigma)
# print(prob1,prob2)


# Black Scholes Call Option
def bs_call(s,k,t,r,sigma):
    return s*norm.cdf(d1(s,k,t,r,sigma)) - k*exp(-r*t)*norm.cdf(d2(s,k,t,r,sigma))
# Black Scholes Put Option 
def bs_put(s,k,t,r,sigma):
    return k*exp(-r*t) - s + bs_call(s,k,t,r,sigma)
callOption = bs_call(lastCloseP, c.strike_price, tMature, riskFree, sigma)
putOption = bs_put(lastCloseP, c.strike_price, tMature, riskFree, sigma)
# print(callOption, putOption)


# Black Scholes as a Single Function 
def black_scholes(s,k,t,r,sigma,option='call'):
    d1 = (log(s/k) + (r+sigma**2/2) * t) / (sigma*sqrt(t))
    d2 = d1 - sigma*sqrt(t)
    if option == 'call':
        call = s*norm.cdf(d1) - k*exp(-r*t)*norm.cdf(d2)
        return call
    if option == 'put':
        call = s*norm.cdf(d1) - k*exp(-r*t)*norm.cdf(d2)
        put = k*exp(-r*t) - s + call
        return put
callWhole = black_scholes(lastCloseP, c.strike_price, tMature, riskFree, sigma, option='call')
putWhole = black_scholes(lastCloseP, c.strike_price, tMature, riskFree, sigma, option='put')
# print(callWhole, putWhole)


# PRINTING
print('Stock: {} \n Expiration: {} \n Strike Price: {} \n Data Source: {} \n'.format(c.stock, c.expiration, c.strike_price, c.dataSource))
print(df.info(),end='\n \n')
print('Variables: \n s = Last Close Price: {} \n k = Strike Price: {} \n t = Time to Maturity: {} \n r = Risk-Free-Rate: {} \n Sigma: {}'.format(lastCloseP, c.strike_price, tMature, riskFree, sigma))
print('Risk-Adjusted Probability (d1): {} (d2): {}'.format(prob1,prob2))
print('Individual Functions: \n Call Option: {} \n Put Option: {}'.format(callOption, putOption))
print('black_scholes(): \n Call Option: {} \n Put Option: {}'.format(callWhole,putWhole))

    
