# Binomial Option Pricing Model 


#import libraries 
import arch
import math 

import numpy as np
import pandas as pd 
import pandas_datareader.data as pdr 
import fix_yahoo_finance as yf 
import matplotlib.pyplot as plt

from statsmodels.graphics.tsaplots import plot_acf 

yf.pdr_override()



# Define Stock Parameters 
stock = 'AAPL'
start = '2016-01-01'
end = '2016-03-01'





class STOCK_OPTION():
    def __init__(self, N, stock_p, strike, riskFree, tMature, prm) -> None:
        """
        N = number of binomial iterations 
        stock_p = initial stock price
        strike = strike price 
        riskFree = risk-free interest rate 
        tMature = time to maturity 
        prm = dictionary with additional parameters 
        """
        self.N = N
        self.stock_p = stock_p
        self.strike = strike 
        self.riskFree = riskFree
        self.tMature = tMature
        """
        prm params: 
        ============
        start = start date "yyyy-mm-dd"
        end = end day (often current date) "yyyy-mm-dd"
        ticker = ticker 
        div = dividend paid 
        sigma = volatility of stock 
        is_calc = is vol calculated using price history? (boolean)
        use_garch = use GARCH model (boolean) 
        is_call = is call option? (boolean) 
        eu_option = is european option? or american (boolean)
        """
        self.ticker = prm.get('ticker', None)
        self.start = prm.get('start', None) 
        self.end = prm.get('end', None) 
        self.div = prm.get('div', 0) 

        self.is_calc = prm.get('is_calc', False)
        self.use_garch = prm.get('use_garch', False) 
        self.vol = self.VOLATILITY(self.ticker, self.start, self.end) 

        if self.is_calc: 
            if self.use_garch: 
                self.sigma = self.vol.garch_sigma() 
            else: 
                self.sigma = self.vol.mean_sigma() 
        else: 
            self.sigma = prm.get('sigma', 0) 
        
        self.is_call = prm.get('is_call', True) 
        self.eu_option = prm.get('eu_option', True) 

        """
        derived values: 
        ================
        dt = time per step, in years 
        df = discount factor
        """
        self.dt = tMature/float(N)
        self.df = math.exp(-(riskFree - self.div) * self.dt)


class EUROPEAN_OPTION(STOCK_OPTION):
    """
    CALCULATE PARAMS
    =======================
    u = upstate factor change 
    d = downstate factor change 
    qu = risk-free upstate probability 
    qd = risk-free downstate probability 
    M = number of nodes 
    """
    def __init_prms__(self): 
        self.M = self.N + 1
        self.u = math.exp(self.sigma* math.sqrt(self.dt))
        self.d = 1./self.u
        self.qu = (math.exp((self.riskFree - self.div) * self.dt) - self.d) / (self.u - self.d)
        self.qd = 1-self.qu 

    def stock_tree(self): 
        stocktree = np.zeros([self.M, self.M])
        for i in range(self.M): 
            for j in range(self.M): 
                stocktree[j, i] = self.stock_p * (self.u**(i-j)) * (self.d**j) 
        return stocktree
    
    def option_price(self, stocktree): 
        option = np.zeros([self.M, self.M]) 
        if self.is_call: 
            option[:, self.M-1] = np.maximum(np.zeros(self.M), stocktree[:, self.N] - self.strike)
        else: 
            option[:, self.M-1] = np.maximum(np.zeros(self.M), (self.strike - stocktree[:, self.N]))
        return option 
    
    def option_price_tree(self, option): 
        for i in np.arange(self.M-2, -1, -1): 
            for j in range(0, i+1): 
                option[j, i] = math.exp(-self.riskFree * self.dt) * (self.qu * option[j, i+1] + self.qd * option[j+1, i+1]) 
        return option 
        
    def begin_tree(self): 
        stocktree = self.stock_tree()
        payoff = self.option_price(stocktree)
        return self.option_price_tree(payoff) 

    def price(self): 
        self.__init_prms__()
        self.stock_tree()
        payoff = self.begin_tree()
        return payoff[0,0]



class BINOMIAL_MODEL(): 
    def __init__(self, N, stock_p, upstate, riskFree, strike): 
        """
        N = number of binomial iteration s
        stock_p = initial stock price 
        upstate = upstate factor change 
        riskFree = risk-free interest rate 
        strike = strike price 
        
        DERIVED PARAMS
        =========================
        u = upstate factor change 
        d = downstate factor change 
        qu = risk-free upstate probability 
        qd = risk-free downstate probability 
        M = number of nodes 

        """
        self.N = N 
        self.stock_p = stock_p 
        self.upstate = upstate
        self.riskFree = riskFree
        self.strike = strike
        # Derived Params 
        self.M = self.N+1
        self.u = math.exp(self.sigma * math.sqrt(self.dt))
        self.d = 1/self.u 
        self.qu = (math.exp((self.riskFree - self.div) * self.dt) - self.d) / (self.u - self.d) 
        self.qd = 1 - self.qu 

    def stock_tree(self): 
        stocktree = np.zeros([self.M, self.M])
        for i in range(self.M): 
            for j in range(i + 1): 
                stocktree[j,i] = self.stock_p * (self.upstate ** (i-j)) * (self.d**j)
        return stocktree
        
    def option_price(self, stocktree):  
        option = np.zeros([self.M, self.M]) 
        option[:, self.N] = np.maximum(np.zeros(self.N+1), (stocktree[:, self.N] - self.strike))
        for i in range(self.N -1, -1, -1): 
            for j in range(0, i+1): 
                option[j,i] = ( 1/(1+self.riskFree) * (self.qu * option[j, i+1] + self.qd * option[j+1, i+1]))
        return option 



