# Options Analysis Black Scholes 

import pandas as pd 
import numpy as np

from pandas_datareader import data as web 
from scipy.stats import norm
from math import log, sqrt, pi, exp 

from datetime import datetime, date

from torch import threshold

from blackScholes.BLACK_SCHOLES import d1





stock = 'SPY'
expiration = '12-18-2022'
strike_price = 370
dataSource = 'yahoo'
desired_threshold = 0.015
tradingDays = 252
today = datetime.now()
one_yr_ago = today.replace(year=today.year-1)


# CONFIG.py 
class configure(object): 
    def __init__(self, stock, expiration, datasource, threshold, today, past_time) -> None:
        self.stock = stock
        self.expiration = expiration
        self.datasource = 'yahoo'
        self.threshold = threshold
        self.today = datetime.now()
        self.past_time = self.today.replace(year=self.today.year-1)
    
    def downloadDF(self): 
        df = web.DataReader(self.sock, self.datasource, self.today, self.past_time)
        df = df.sort_values(by='Date')
        df = df.dropna()
        df = df.assign(close_day_before = df.Close.shift(1))
        df['returns'] = ((df.Close-df.close_day_before) /  df.close_day_before)
        return df 


#BLACK_SCHOLES.py 
class black_scholes(object): 
    def __init__(self, stockData, strike, expiration): 
        self.stockData = stockData 
        self.strike = strike 
        self.expiration = expiration

    # Variables 
    def var_sigma(self, tradingDays):
        sigma = np.sqrt(tradingDays) * self.stockData.std()
        return sigma
    def var_riskFree(self, today):
        usTY10 = "^TNX"
        riskFree = (web.DataReader(name=usTY10, data_source=dataSource, start=today.replace(day=today.day-1), end=today) ['Close'].iloc[-1]) / 100
        return riskFree
    def var_closePrice(self):
        lastCloseP = self.stockData['Close'].iloc[-1]
        return lastCloseP
    def var_tMature(self): 
        tMature = (datetime.strptime(self.expiration, "%m-%d-%Y") - datetime.utcnow()).days / 365
        return tMature

    # Risk-Adjusted Probability 
    def prob_d1(self, lastCloseP, tMature, riskFree, sigma):
        d1 = (log(lastCloseP/self.strike) + (riskFree+sigma **2/2) * tMature) / (sigma * sqrt(tMature))
        return d1
    def prob_d2(self, lastCloseP, tMature, riskFree, sigma): 
        d2 = (d1(lastCloseP, self.strike, tMature, riskFree, sigma) - sigma * sqrt(tMature))
        return d2 
    
    # Black Scholes Options
    def bs_call(self, lastCloseP, tMature, riskFree, sigma): 
        call = lastCloseP*norm.cdf(d1(lastCloseP, self.strike, tMature, riskFree, sigma)) - self.strike*exp(-riskFree*tMature) * norm.cdf(self.prob_d2(lastCloseP,self.strike,tMature,riskFree,sigma))
        return call 
    def bs_put(self, lastCloseP, tMature, riskFree, sigma): 
        put = self.strike*exp(-riskFree/tMature) - lastCloseP + self.bs_call(lastCloseP, self.strike, tMature, riskFree, sigma)
        return put 
    def black_scholes(self, lastCloseP, tMature, riskFree, sigma, option='call'):
        d1 = (log(lastCloseP/self.strike) + (riskFree+sigma **2/2) * tMature) / (sigma * sqrt(tMature))
        d2 = (d1(lastCloseP, self.strike, tMature, riskFree, sigma) - sigma * sqrt(tMature))
        if option == 'call':
            call = lastCloseP*norm.cdf(d1(lastCloseP, self.strike, tMature, riskFree, sigma)) - self.strike*exp(-riskFree*tMature) * norm.cdf(self.prob_d2(lastCloseP,self.strike,tMature,riskFree,sigma))
            return call 
        if option == 'put':
            put = self.strike*exp(-riskFree/tMature) - lastCloseP + self.bs_call(lastCloseP, self.strike, tMature, riskFree, sigma)
            return put 


# GREEKS.py 
class GREEKS(object):
    def __init__(self, lastCallP, strike, tMature, riskFree, sigma):
        self.lastCallP = lastCallP
        self.strike = strike
        self.tMature = tMature
        self.riskFree = riskFree
        self.sigma = sigma
    
    def delta(self, option='call'):
        if option == 'call':
            call_delta = norm.pdf(black_scholes.prob_d1(self.lastCallP, self.strike, self.tMature, self.riskFree, self.sigma)) / (self.lastCallP*self.sigma * sqrt(self.tMature))
            return call_delta 
        if option == 'put': 
            put_delta = norm.pdf(black_scholes.prob_d1(self.lastCallP, self.strike, ))
            return put_delta
    def gamma(self):


    def vega(self):


    def theta(self):


    def rho(self):

