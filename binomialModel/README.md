# **Binomial Option Pricing Model**
---
> For each Option Pricing Process One Must Look At:  <br />
> 1. Specific contract details calculated properly within the model 
> 2. Optimal volatility modeling varies for different securities (simplest form here) 
> 3. Assumption that volatility will remain relatively constant during analysis. 
> 4. Assumption of no arbitrage in the portfolio for these measurements. 

- American-based Options: exercised at any point prior to expiration date 
- Embedded Options: lets issues/holders take specific actions against other party at a future time 
- Values Options via Iterative Approach Utilizing Various Nodes Representing Different Periods of Time 
    - Two Possible Outcomes for Each Iteration via **Binomial Tree**
        - Up or Down 
- Removes Possibility for Arbitrage 
    - `d<1+r<u` = no arbitrage, value of portfolio that is the return of the option is the price of the option 

> - Use same probability each period for success and failure (up until expiration date)
>      - can incorporate new information into new probabilities as time passes 
> - Problem with construction is various values the underlying asset can have in a period of time 
>      - many different routes asset can take vs. just up/down
>      - one period `50/50` asset moves up/down by `30%` in a period
>      - next period could be `70/30`
- simplicity over Black-Scholes Model -> Fewer Errors 
- Iterative operation -> easier to adjust prices over time 
    - reduces buyers ability to arbitrage 

> Stock Price: `$100`
> - Month One:
>   - Up: `$110` Down: `$90` <br />
> 
> Call Option Expires 1month
> - Strike Price: `$100`: 
>   - Up: worth `$10`
>   - Down: worth `$0` <br />
>
> Binomial Model Prices Call Option for Today
>> Purchases 1/2 share of stock <br />
>> Writes/Sells 1 Call Option <br />
>>> Option Price: `$50`
>>> - Up: `$55` - max(`$110 - $100`, `0`) = `$45`
>>> - Down: `$45` - max(`$90 - $100`, `0`) = `$45` <br />
>> 
>> assuming no arbitrage, investor earns risk-free rate over the month  <br />
>> cost today = payoff discouted at the risk-free rate <br />
>
## Equation:
- `e` = natural log -> 2.7183
- `RF` = risk-free rate
- `T` = time to expiration  
```
OptionPriceToday = Option Price - Portfolio Value * e^(-RF * T)
``` 
- `X` = current market price of stock 
- `X*up` = Upward Movement (`Pup` = Option Payoff)
- `X*dn` = Downward Movement (`Pdn` = Option Payoff)
- `t` = Future time
- `s` = # of shares 
#### `VUM` = Portfolio Value: Upward Movement 
```
VUM = s * X*up - Pup
```
#### `VDM` = Portfolio Value: Downward Movement 
```
VDM = s * X*dn - Pdn
```
#### Number of shares to purchase: 
``` 
s = (Pup - Pdn) / ((X * (up-dn))
```
#### Present Value: via discounting with risk-free rate 
```
PV = e(-rf * t) * [((Pup - Pdn) / (up-dn)) * up - Pup]
```

---
# GARCH Process: 
--- 
## Generalized Autoregressive Conditional Heteroskedasticity Process 
#### By Robert F. Engle to estimate volatility in financial markets 
## Heteroskedascity: 
- irregular pattern of variation in a variable 
- standard deviations of variable are nonconstant 
- observations cluster rather than form linear pattern 
> Three Steps: <br />
> 1. estimate best-fitting autoregressive model 
> 2. compute autocorrelations of error term 
> 3. test for significance 
## Autoregressive: 
- depend on past squared observations and past variances to model current 
- accounts for errors in prior forecasting 

# Embedded Options: 
- pull from investopedia link below 




# References: 


#### Investopedia: 
- [Investopedia: Binomial Option Pricing Model](https://www.investopedia.com/terms/b/binomialoptionpricing.asp)
- [Investopedia: Understanding the Binomial Option Pricing Model](https://www.investopedia.com/articles/investing/021215/examples-understand-binomial-option-pricing-model.asp)
- [Investopedia: American Option](https://www.investopedia.com/terms/a/americanoption.asp)
- [Investopedia: Embedded Option](https://www.investopedia.com/terms/e/embeddedoption.asp)
- [Investopedia: GARCH Process](https://www.investopedia.com/terms/g/generalalizedautogregressiveconditionalheteroskedasticity.asp)