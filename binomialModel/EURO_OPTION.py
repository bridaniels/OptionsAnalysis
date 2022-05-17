# European Option 

# import libraries 
import math 
import numpy as np 
# import PY files
from OPTION import STOCK_OPTION


class EUROPEAN_OPTION(STOCK_OPTION):
    """
    CALCULATE PRELIM PARAMS
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
