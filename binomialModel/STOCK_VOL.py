# Binomial Model: Stock Volatility 

# import libraries 
import arch 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from statsmodels.graphics.tsaplots import plot_acf
from pandas_datareader import data as web 



class VOLATILITY: 
    def __init__(self, ticker, start, end):
        self.ticker = ticker 
        self.start = start
        self.end = end

    def get_dataframe(self): 
        df = web.DataReader(name=self.ticker, data_source='yahoo', start=self.start, end=self.end)
        stock_data = pd.DataFrame(df['Adj Close'])
        stock_data['log'] = np.log(stock_data) - np.log(stock_data.shift(1))
        data = stock_data['log'].dropna()
        return data
    
    def mean_sigma(self): 
        st = self.get_dataframe().ewm(span=252).std() 
        sigma = st.iloc[-1]
        return sigma 
    
    def garch_sigma(self): 
        model = arch.arch_model(self.get_dataframe(), mean='Zero', vol='GARCH', p=1, q=1)
        model_fit = model.fit()
        forecast = model_fit.forecast(horizon=1)
        var = forecast.variance.iloc[-1]
        sigma = float(np.sqrt(var))
        return sigma 

    def plotting_autocorrelation(self): 
        df = self.get_dataframe()
        fig, ax = plt.subplots(figsize=(15,5))
        plot_acf(df, title="Autocorrelation of {} from {} to {}".format(self.ticker, self.start, self.end), ax=ax)
        plt.show()

