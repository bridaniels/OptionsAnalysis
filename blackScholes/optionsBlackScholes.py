# Options Analysis Black Scholes 
import warnings 

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import ipywidgets as widgets

from pandas_datareader import data as web
from requests import TooManyRedirects 
from scipy.stats import norm
from math import log, sqrt, pi, exp 
from typing import List 
from datascience import *
from datetime import datetime, date
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
    def __init__(self, lastCloseP, strike, tMature, riskFree, sigma, d1=None, d2=None):
        self.lastCloseP = lastCloseP
        self.strike = strike
        self.tMature = tMature
        self.riskFree = riskFree
        self.sigma = sigma
        self.d1 = (log(self.lastCloseP/self.strike) + (self.riskFree+self.sigma **2/2) * self.tMature) / (self.sigma * sqrt(self.tMature))
        self.d2 = (self.d1 - self.sigma * sqrt(self.tMature))
    
    def delta(self, option='call'):
        if option == 'call':
            call_delta = norm.pdf(self.d1) / (self.lastCloseP * self.sigma * sqrt(self.tMature))
            return call_delta 
        if option == 'put': 
            put_delta = norm.pdf(self.d1)
            return put_delta
    def gamma(self, option='call'):
        if option == 'call':
            call_gamma = norm.pdf(self.d1) / (self.lastCloseP * self.sigma * sqrt(self.tMature))
            return call_gamma
        if option == 'put':
            put_gamma = norm.pdf(self.d1) / (self.lastCloseP * self.sigma * sqrt(self.tMature))
            return put_gamma
    def vega(self, option='call'):
        if option == 'call': 
            call_vega = 0.01 * (self.lastCloseP * norm.pdf(self.d1) * sqrt(self.tMature))
            return call_vega
        if option == 'put':
            put_vega = 0.01 * (self.lastCloseP * norm.pdf(self.d1) * sqrt(self.tMature))
            return put_vega
    def theta(self, option='call'):
        if option == 'call': 
            call_theta = 0.01 * (-(self.lastCloseP * norm.pdf(self.d1) * self.sigma) / (2 * sqrt(self.tMature)) - self.riskFree*self.strike * exp(-self.riskFree*self.tMature) * norm.cdf(self.d2))
            return call_theta
        if option == 'put':
            put_theta = 0.01 * (-(self.lastCloseP * norm.pdf(self.d1) * self.sigma) / (2 * sqrt(self.tMature)) + self.riskFree*self.strike * exp(-self.riskFree*self.tMature) * norm.cdf(-self.d2))
            return put_theta
    def rho(self, option='call'):
        if option == 'call':
            call_rho = 0.01 * (self.strike * self.tMature * exp(-self.riskFree*self.tMature) * norm.cdf(self.d2))
            return call_rho
        if option == 'put':
            put_rho = 0.01 * (-self.strike * self.tMature * exp(-self.riskFree*self.tMature) * norm.cdf(-self.d2))
            return put_rho 


# Implied Volatility
class implied_volatility(object): 
    def __init__(self, lastCloseP, strike, tMature, riskFree, threshhold, call_put_price, sigma=0.001, d1=None, d2=None): 
        self.lastCloseP = lastCloseP
        self.strike = strike
        self.tMature = tMature
        self.riskFree = riskFree
        self.threshhold = threshhold 
        self.sigma = sigma
        self.call_put_price = call_put_price
        self.d1 = (log(self.lastCloseP/self.strike) + (self.riskFree+self.sigma **2/2) * self.tMature) / (self.sigma * sqrt(self.tMature))
        self.d2 = (self.d1 - self.sigma * sqrt(self.tMature))

    def call_implied_vol(self): 
        new_sig = self.sigma
        while new_sig < 1:
            implied_p = (self.lastCloseP * norm.cdf(self.d1) - self.strike * exp(-self.riskFree*self.tMature) * norm.cdf(self.d2))
            if self.call_put_price - implied_p < self.sigma: 
                return new_sig
            new_sig += self.sigma
        return 'Not Found'

    def put_implied_vol(self): 
        new_sig = self.sigma
        while new_sig < 1:
            implied_p = (self.strike * exp(-self.riskFree*self.tMature) - self.lastCloseP * self.call_put_price)
            if self.call_put_price - implied_p < self.sigma: 
                return new_sig 
            new_sig += self.sigma
        return 'Not Found'


# LEVEL UNDERLYING
class Underlying(black_scholes):
    def __init__(self, stock: str,currPrice: float,strike: int,risk: float,sigma: float,option='call') -> None: 
        self.stock = stock 
        self.currPrice = currPrice
        self.strike = strike
        self.risk = risk
        self.sigma = sigma
        self.option = 'call'

    def makeFullTable(self, exp: List[int]):
        start = self.currPrice - ((self.currPrice//4)*2)
        end = self.currPrice + (self.currPrice//4)
        step = (self.currPrice/2)//10

        def expireArray(expiration, start,end,step):
            arr = make_array()
            for price in np.arange(start,end,step):
                if price == 0:
                    arr = np.append(arr,0)
                else: 
                    arr = np.append(arr, black_scholes(price,self.strike,expiration,self.risk,self.sigma,self.option))
            return arr

        new_table = Table().with_column("Level of Underlying", np.arange(start,end,step))
        for x in range(len(exp)):
            if exp[x] == 0:
                exp[x] = 0.000001
            new_table = new_table.with_column("Time to Expiration of {} Year".format(exp[x]), expireArray(self, exp[x], start,end,step))
        return new_table

    def plotting(self, table):
        table.plot('Level of Underlying')
        plt.title("Level of Underlying for {}".format(self.stock))
        plt.xlabel('Level of Underlying (Arbitrary)')
        plt.ylabel('Price (Arbitrary)')
        plt.show()