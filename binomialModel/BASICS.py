# Binomial Model Basics 

# import libraries 
import math
import numpy as np 


# basic math 
def combos (n):
    res = (n+1) * [0]
    fair_value = 0
    threshold = n - (n * 1//3)
    t_fv = 0 
    for i in range(n+1):
        res[i] = (math.factorial(n) / (math.factorial(n-i) * math.factorial(i)))
        fair_value += res[i] * 0.5**i * 0.5**(n-i) * i
        if i >= threshold: 
            t_fv += res[i] * 0.5**i * 0.5**(n-i) * i
    return res,fair_value, t_fv

#print(combos(10))


'''
Cox, Ross, Rubenstein
=====================
Assuming European Options 
1. write 3 calls at price 'c' 
2. buy 2 shares at $50
3. borrow $40 at 25%
4. price goes up to $100 or down to $25
'''
# 3 calls at price 'c' 
cn = 3
cp = 20
# buy two shares at $50 
sn = 2
sp = 50
# borrow $40 at 25% paid end of period 
b = 40
ir = 0.25
# up, down, strike given 
up = 2
dn = 0.5
strike = 50 

def crr_options(call_num, call_price, share_num, share_price, borrowed, interest, up, down, strike): 
    k = call_num*call_price - share_num*share_price + borrowed
    if  k == 0: 
        print('No Arbitrage, a Call Price of ${} Returns ${}\n'.format(call_price, k))
    elif k > 0: 
        print('Profit Arbitrage, a Call Price of ${} Will Return a Cash Inflow of ${} in Risk-Free Profit\n'.format(call_price, k))
    else: 
        print('Loss Arbitrage, a Call Price of ${} Will Return a Loss of ${}\n'.format(call_price, k))

    r = 1 + interest 
    # risk neutral probability of an up move
    p_up = (r-down)/(up-down)
    # binomial value 
    b_val = (1/r) * (max(up*share_price-strike, 0) * p_up + max(down*share_price-strike, 0) * (1-p_up))
    print('Risk-Neutral Probability Up: {} \nBinomial Value: {}\n'.format(p_up, b_val))

c1 = 20
c2 = 25
c3 = 15
scenario1 = crr_options(cn, c1, sn, sp, b, ir, up, dn, strike)
scenario2 = crr_options(cn, c2, sn, sp, b, ir, up, dn, strike)
scenario3 = crr_options(cn, c3, sn, sp, b, ir, up, dn, strike)


'''
Determining Up and Down Probabilities
======================================
stock trading at $100
strike price of $105
time to maturity 6 months 
historic vol is 40%
Estimate price using 4 steps using natural exponents 
- Up and Down probabilities often not given
- calculated via volatility from historical data 
Natural Exponents: 
- math.exp() = natural exponent 
- np.exp() = natural exponent 
'''
t = 6 #months 
price = 100
strike = 105 
h_vol = 0.4
steps = 4 
odds = 0.5
rf = 0.05


def Node_Prices(steps, trading_price, strike, tMature_yr, historic_vol, riskFree): 
    dt = tMature_yr / steps
    #up = np.exp(historic_vol * np.sqrt(dt))
    up = math.exp(historic_vol * math.sqrt(dt))
    #down = np.exp(-historic_vol * np.sqrt(dt))
    down = math.exp(-historic_vol * math.sqrt(dt))
    prob = (np.exp(riskFree*dt) - down) / (up-down)

    print("Up Probability: {} \nDown Probability: {} \nPrice Probabilty: {}\n".format(up,down,prob))

    # Find Prices and Probabilites of Terminal Nodes 
    # Finding Value of Call Option 
    call_value = 0
    def factorials(steps, k): 
        return math.factorial(steps) / (math.factorial(steps-k) * math.factorial(k))
    
    for k in reversed(range(steps+1)):
        node_price = trading_price * up**k * down**(steps-k)
        node_probability = factorials(steps,k) * prob**k * (1-prob)**(steps-k) 
        call_value += max(node_price-strike, 0) * node_probability

        print("Node {}: \n Stock Price: ${}\n Option Value: ${}\n Probability: {}\n Call Value: {}".format(k, round(node_price,2), round(max(node_price-strike, 0),2), round(node_probability, 2), round(call_value, 5)))

    end_p = call_value * np.exp(-riskFree * tMature_yr)
    print("Ending Price: {}".format(round(end_p,5)))
    
# Correct up through here 
dos = Node_Prices(steps, price, strike, t/12, h_vol, rf)





# [working link](https://www.codearmo.com/python-tutorial/options-trading-binomial-pricing-model)
# [medium article](https://medium.com/engineer-quant/binomial-option-pricing-model-5e6b9e91c7da)
# [garch in python](https://barnesanalytics.com/garch-models-in-python/)