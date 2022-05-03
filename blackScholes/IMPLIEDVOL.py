# Implied Volatility
import CONFIG as c
import BLACK_SCHOLES as bs

import math
import pandas as pd
import numpy as np
from datetime import datetime, date
from scipy.stats import norm


# Implied Call Option Volatility
def call_implied_volatility(price, s,k,t,r, sigma=0.001):
    og_sig = sigma
    while sigma < 1: 
        # sigma is different than in bs.prob1 and bs.prob2 
        implied_p = (s * norm.cdf(bs.d1(s,k,t,r,sigma)) - k*math.exp(-r*t) * norm.cdf(bs.d2(s,k,t,r,sigma)))
        if price-implied_p < og_sig: 
            return sigma
        sigma += og_sig
    return "Not Found"


#Implied Put Option Volatility 
def put_implied_volatility(price, s,k,t,r, sigma=0.001):
    og_sig = sigma 
    while sigma < 1: 
        # call back to sigma function 
        implied_p = k*math.exp(-r*t) - s + bs.bs_call(s,k,t,r,sigma)
        if price-implied_p < og_sig: 
            return sigma
        sigma += og_sig
    return "Not Found"