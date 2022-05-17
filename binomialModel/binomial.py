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


stock = 'AAPL'
start = '2016-01-01'
end = '2016-03-01'



class VOLATILITY(): 
    def __init__(self, ticker, start, end) -> None:
        self.ticker = ticker 
        self.start = start
        self.end = end
        all_data = pdr.get_data_yahoo(self.ticker, start=self.start, end=self.end) 
        self.stock_data = pd.DataFrame(all_data['Adj_Close'], columns=['Adj Close'])
        self.stock_data['log'] = np.log(self.stock_data) - np.log(self.stock_data.shift(1))
    
    def mean_sigma(self): 
        st = self.stock_data['log'].dropna().ewm(span=252).std() 
        sigma = st.iloc[-1]
        return sigma 
    
    def garch_sigma(self): 
        model = arch.arch_model(self.stock_data["log"].dropna(), mean='Zero', vol='GARCH', p=1, q=1)
        model_fit = model.fit()
        forecast = model_fit.forecast(horizon=1)
        var = forecast.variance.iloc[-1]
        sigma = float(np.sqrt(var))
        return sigma 

if __name__=='__main__':
    vol = VOLATILITY(stock, start, end)
    test = vol.stock_data['log'].dropna()
    print(test) 
    fig = plot_acf(test)
    plt.show() 


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
        self.vol = VOLATILITY(self.ticker, self.start, self.end) 

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


    def binomial_model(self, upstate_change): 
        """
        upstate_change = factor change upstate
        """
        down = 1/upstate_change
        p = (1+ self.riskFree - down) / (upstate_change - down) 
        q = 1 - p 

        # stock price tree 
        stock_matrix = np.zeros([self.N +1, self.N+1])
        for i in range(self.N+1): 
            for j in range(i + 1): 
                stock_matrix[j,i] = self.stock_p * (upstate_change ** (i-j)) * (down**j)
        
        # generaste option prices 
        option = np.zeros([self.N+1, self.N+1]) 
        option[:, self.N] = np.maximum(np.zeros(self.N+1), (stock_matrix[:, self.N] - self.strike))
        for i in range(self.N -1, -1, -1): 
            for j in range(0, i+1): 
                option[j,i] = ( 1/(1+self.riskFree) * (p * option[j, i+1] + q * option[j+1, i+1]))
        return option 

#if __name__ == "__main__": 
    #print("Calculating example otpion price") 
    #op_price = binomial_model(5,4,2,0.25, 8) 
    #print(op_price)

