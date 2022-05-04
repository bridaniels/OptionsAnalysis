# Level Underlying
import CONFIG as c
import BLACK_SCHOLES as bs

import matplotlib
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from typing import List
from pandas_datareader import data as web
from datetime import datetime, date
from scipy.stats import norm
from math import log, sqrt, pi, exp
from datascience import *
from ipywidgets import interact, interactive, fixed, interact_manual
plt.style.use('fivethirtyeight')
warnings.simplefilter('ignore',FutureWarning)


class Underlying(object):

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

        def expireArray(self, expiration, start,end,step):
            arr = make_array()
            for price in np.arange(start,end,step):
                if price == 0:
                    arr = np.append(arr,0)
                else: 
                    arr = np.append(arr, bs.black_scholes(price,self.strike,expiration,self.risk,self.sigma,self.option))
            return arr

        new_table = Table().with_column("Level of Underlying", np.arange(start,end,step))
        for x in range(len(exp)):
            new_table = new_table.with_column("Time to Expiration of {} Year".format(exp[x]), expireArray(self, exp[x], start,end,step))
        return new_table

    def plotting(self, table):
        table.plot('Level of Underlying')
        plt.title("Level of Underlying for {}".format(c.stock))
        plt.xlabel('Level of Underlying (Arbitrary)')
        plt.ylabel('Price (Arbitrary)')
        plt.show()

levels = [1,0,3]
Under = Underlying(c.stock, bs.lastCloseP, c.strike_price, bs.riskFree, bs.sigma)
k = Under.makeFullTable(levels)
Under.plotting(k)
print(k)