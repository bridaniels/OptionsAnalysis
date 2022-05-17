# Binomial Model Basics 

# import libraries 
import math 

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

print(combos(10))


# [working link](https://www.codearmo.com/python-tutorial/options-trading-binomial-pricing-model)
# [medium article](https://medium.com/engineer-quant/binomial-option-pricing-model-5e6b9e91c7da)
# [garch in python](https://barnesanalytics.com/garch-models-in-python/)