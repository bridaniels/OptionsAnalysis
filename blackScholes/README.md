# **Black Scholes**
---
- determines price of European *option* (contracts that can only be exercised at expiration)
    - no dividends paid out during option's lifespan
    - no transaction/commission costs included 
    - measures option's predicted value at expiration
- help create a short-term-risk-neutral portfolio via calculating *fair value* of the options contract in relation to underlying asset 
- Partial Differential Equation: 

#### Assumptions: 
> - NOT a divedend-paying stock 
> - random-walk simulation for price movements 
> - no transaction costs/commissions/taxes
> - risk-free rate offers a *fixed* and known rate-of-return 
> - underlying asset's volatility known 
> - European-Style: can only be exercised on expiration date 

#### Requires 5 variables:
> - *K* = strike price
> - *S* = current stock price (spot price)
> - *t* = time to maturity
> - *r* = risk-free interest rate 
> - *σ* = volatility (sigma)
> - *N* = CDF of normal distribution 
>>    - **Cumulative Distribution Function** of random variable *x*
>>    - `Fx(t) = P(x <= t)`
>>    - nondecreasing function of *t* for `-inf < t < inf`, but ranges from `0:1` since `Fx(t)` is a probability
>>        - max value of *x* is *b*, thus `Fx(b) = 1`
>>    - *x* is a discrete random variable whose minimum value is *a*
>>        - `Fx(a) = P(x<=a) = P(x=a = fx(a)` if `c < a` then `Fx(c) = 0`
> *C* = Call Option Price 

![BlackScholesFormula](data/black_scholes_formula.png)



# **Implied Volatility**
---
- expected future volatility of underlying asset, derived from Black-Scholes formula
- assumes price of asset follows geometric Brownian Motion 
- 

---
---
# **Brownian Motion**
---
---
##### Brownian Motion: 

---
---
# **Greeks**
---
---
### Delta: correlation between the option price and underlying asset price (Volatility)
> Delta Hedging: 
> - Call Options: Positive Delta -> moves up with underlying asset price 
> - Put Options: Negative Delta -> moves up with underlying asset price decrease 
>> - Delta = `-0.5` -> for every `$1` gain in stock price, option value goes down `$0.50`
>> - Delta = `-0.5` -> net-profitable even when asset price goes up (stock holding profit - cost of hedging put contracts )
>> - if underlying asset price goes down -> only losing half the value 
> - Underlying Asset: Delta of `1` -> `100%`` Correlated to price action 
>> - Each share has a Delta of `1`: position with total Delta of `1000(1x1000)` based on your ownership of `1000` shares
>> - Entirely Reliant on price action of underlying asset 
>> - Price up `$1`, portfolio moves up `$1000` -> Price down `$1`, portfolio moves down `$1000`
> - Risk-Neutral Portfolio: Delta of `0`
>> - buy put options (-delta) to offset call options (+delta)
>> - constantly changing delta to maintain neutral portfolio and make a profit regardless of underlying asset price movements 
- Gamma
- Theta
- Vega
- Rho



# **Level of Underlying**
---
- returns on the underlying are normally distributed 

- time to expiration of one year
- no time to expiration 
- time to expiration of three years 






### References: 
---
##### Fisher Black, Myron Scholes model thesis: 
- [The Pricing of Options and Corporate Liabilities]https://www.jstor.org/stable/1831029

##### Robert C. Merton addition: 
- [Theory of Rational Option Pricing](https://www-jstor-org.i.ezproxy.nypl.org/stable/3003143?searchText=%22Theory+of+Rational+Option+Pricing%22&searchUri=%2Faction%2FdoBasicSearch%3FQuery%3D%25E2%2580%259CTheory%2Bof%2BRational%2BOption%2BPricing%25E2%2580%259D%26so%3Drel&ab_segments=0%2Fbasic_phrase_search%2Fcontrol&refreqid=fastly-default%3Ae82e4a7d53e2c0435fbebd8be045a80e&seq=1)

##### University Materials: 
- [City University of Hong Kong: Black Scholes Equations](https://www.math.cuhk.edu.hk/~rchan/teaching/math4210/chap08.pdf)
- [University of Chicago: Brownian Motion](https://galton.uchicago.edu/~lalley/Courses/313/BrownianMotionCurrent.pdf)
- [Berkeley: Brownian Motion](https://www.stat.berkeley.edu/~aldous/205B/bmbook.pdf)


##### Websites: 
- [Tokenist: Complete Guide to the Black-Scholes Model](https://tokenist.com/investing/black-scholes-model/)
- [SoFi: The Black-Scholes Model Explained](https://www.sofi.com/learn/content/what-is-the-black-scholes-model/)
- [Investopedia: How is Implied Volatility Used in the Black-Scholes Formula](https://www.investopedia.com/ask/answers/060115/how-implied-volatility-used-blackscholes-formula.asp)
- [Investopedia: Implied Volatility: Buy Low and Sell High](https://www.investopedia.com/articles/optioninvestor/08/implied-volatility.asp)





  
    