# Greeks -> Black Scholes 
import pandas as pd
import numpy as np 
from datetime import datetime, date
from scipy.stats import norm
from math import log, sqrt, pi, exp 


import CONFIG as c 
import BLACK_SCHOLES as bs


# Delta 
class DELTA():
    def call(s,k,t,r,sigma): 
        return norm.cdf(bs.d1(s,k,t,r,sigma))
    def put(s,k,t,r,sigma): 
        return -norm.cdf(-bs.d1(s,k,t,r,sigma))
D = DELTA()
Dcall = D.call
Dput = D.put


# Gamma
class GAMMA(): 
    def call(s,k,t,r,sigma): 
        return norm.pdf(bs.d1(s,k,t,r,sigma)) / (s*sigma*sqrt(t))
    def put(s,k,t,r,sigma): 
        return norm.pdf(bs.d1(s,k,t,r,sigma)) / (s*sigma*sqrt(t))
G = GAMMA()
Gcall = G.call
Gput = G.put


# Vega
class VEGA(): 
    def call(s,k,t,r,sigma): 
        return 0.01 * (s * norm.pdf(bs.d1(s,k,t,r,sigma))*sqrt(t))
    def put(s,k,t,r,sigma): 
        return 0.01 * (s * norm.pdf(bs.d1(s,k,t,r,sigma))*sqrt(t))
V = VEGA()
Vcall = V.call
Vput = V.put


# Theta
class THETA(): 
    def call(s,k,t,r,sigma): 
        return 0.01 * (-(s * norm.pdf(bs.d1(s,k,t,r,sigma))*sigma)/(2*sqrt(t)) - r*k*exp(-r*t)*norm.cdf(bs.d2(s,k,t,r,sigma)))
    def put(s,k,t,r,sigma): 
        return 0.01 * (-(s * norm.pdf(bs.d1(s,k,t,r,sigma))*sigma)/(2*sqrt(t)) + r*k*exp(-r*t)*norm.cdf(-bs.d2(s,k,t,r,sigma)))
T = THETA()
Tcall = T.call
Tput = T.put


# Rho 
class RHO():
    def call(s,k,t,r,sigma): 
        return 0.01 * (k*t*exp(-r*t) * norm.cdf(bs.d2(s,k,t,r,sigma)))
    def put(s,k,t,r,sigma): 
        return 0.01 * (-k*t*exp(-r*t) * norm.cdf(-bs.d2(s,k,t,r,sigma)))
R = RHO()
Rcall = R.call
Rput = R.put
