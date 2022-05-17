# Stock Option 

# import libraries 
import math 
# import PY files 
from STOCK_VOL import VOLATILITY


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
        # CALL STOCK_VOL.VOLATILITY HERE
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

