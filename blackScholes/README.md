# **Black Scholes**
---
- determines price of European *option* (contracts that can only be exercised at expiration)
    - no dividends paid out during option's lifespan
    - no transaction/commission costs included 
    - measures option's predicted value at expiration
- help create a short-term-risk-neutral portfolio via calculating *fair value* of the options contract in relation to underlying asset 


#### Assumptions: 
> - NOT a divedend-paying stock 
> - random-walk simulation for price movements 
> - no transaction costs/commissions/taxes
> - risk-free rate offers a *fixed* and known rate-of-return 
> - underlying asset's volatility known and constant
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


#### Black-Scholes is a Partial Differential Equation (PDE): 
- contains single unknown f(x) involving x and it's partial derivatives 
- 'order of the PDE' is the maxiumum number of derivatives in the equation 
- 'constant coefficient linear PDE' because x and derivatives appear linearly (first power only, just multiplied by constants)
- 'variable coefficient linear PDE' because x and derivatives appear linearly (first power only, just multiplied by functions of coordinates (a,b))
- What kind of data going into PDE? How does the output change when you modify various input? Quantitative vs. Qualitative results? 
- Other PDEs: 
    - *Wave Equation*, *Heat Equation*, *Poisson's Equation*, *Laplace's Equation*, *Schrodinger's Equation* (all second order, linear)
    - *Transport Equation* (first order, linear)
    - *Burger's Equation* (first order, non-linear)

#### Assumes Log-Normal Distribution: Gaussian Distribution 
- Normal Distribution: 68% in one SD and 95% within two SD (can have negative values)
- Log-Normal can only come from a normal distribution 
    - via logarithmic mathmematics (only positive values)
    - result of taking **natural log** with base `e=2.718`
    - scaled taking different bases (changes shape)
- Graphing stock returns in a normal distribution
    - but PRICES graphed LOG-NORMAL (only positive values) 
- positively skewed with long right tails 
    - low mean values
    - high variances 


---
---

# **Implied Volatility**
---
#### Black Scholes: *European Options*
- expected future volatility of underlying asset
- assumes price of asset follows geometric Brownian Motion 
- used to help analyze potential suppy and demand affects and correlation to future prices of the asset 
- longer the period to expiration = higher the implied volatility 
- constantly changing depending on what is going on in the market 
#### Implied Volatility Factors 
> - Supply and Demand 
> - Time to Expiration 
> - Strike Price 
> - Historic Volatility 
> - Interest Rates

#### Binomial Model: *American Options* 
- Tree Diagram with various levels
- different execution time at each level to show various exit opportunities within bounds of options contract 

#### Newton's Model: *bisection method, more granular and variable Black-Scholes*
- combines Black-Scholes method with an equation from Isaac Newton 
- usually done by traders who can code 

---
---
# **Greeks**
---
- measure derivative price sensitivity in relation to various parameters 
- risk management tools to isolate various risk factors 
# **Delta:** correlation between the option price and underlying asset price (Volatility)
- Directional risk -> if the underlying asset goes up or down what is the risk held by the option contract? 
- Only valid for a short period of time 
- `Beta`: market's overall volatility -> systemic market risk 
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
#### Delta Spread: *options trading strategy* 
- establish a delta neutral position 
    - buy and sell options to keep delta ratio neutral
    - postive/negative deltas to offset each other 
        - Long Call Option: `Delta = 0:1`
        - Long Put Option: `Delta = -1:0`
    - small profit if underlying security is not volatile 
    - adjust portfolio as underlying asset price changes to maintain neutrality 
- Calendar Spread: delta neutral via varying expiration dates 

# **Gamma:** rate of change between option's **delta** and underlying asset price 
- Second-Order Price Sensitivity  (second-derivative of option's price)
    - First Derivative of **Delta**
    - Does not change as often as **Delta** 
- How much **Delta** will change given a `$1` move in the underlying security 
> Delta Hedging (cont.):
> - Reduce Gamma to maintain a hedge over wider price range  
>   - Alpha also reduces alongside Gamma (downside) 
>> - **Alpha**: investment's ability to `"beat the market"`
>>      - aka `"excess return"` or `"abnormal rate of return"`
>>      - `"seeking alpha"` to eliminate 'unsystemic risk'
>>      - represents portfolio risk vs. overall market risk 
>>      - returns outside of general market movements 
>   - Deep in/out -of-the-money: Gamma small (approaches zero)
>   - near/at -the-money: Gamma largest (approaches one)
>> Long Positions = Positive Gamma <br />
>> Short Positions = Negative Gamma 
> - Third-Order Derivative `color`: measures **Gammma's** rate of change 
>   - maintaining **Gamma**-hedged portfolio 

- Corrects for **convexity** issues in hedging startegies 
- Convexity: degree of the curve (relationship between bond prices and yields)
    - helps manage a portfolio's exposure to **interest-rate-risk**
    - how the duration of a bond changes alongside interest rates 
    - Negative Convexity: bond's duration increases as yield increases
        - bond price decreases faster with a rise in yields
        - duration increases -> price falls 
    - Positive Convexity: bond's duration increases as yield decreases 
        - bond price increases faster with a fall in yields 
        - higher bond price with less yield 
    - **Convexity Increases: Systemic Risk Exposure to Portfolio Increases**
    - Higher coupon rates (yield) = lower convexity (aka market risk)
        - market rates would increase substaintially to surpass coupon 
        - Higher the coupon rate -> lower the degree of convexity 
    

# **Theta:** Decline in value of an option due to passage of time 
### aka Time Decay 
- Quantifies Risk of Time: option loses value as it moves closer to maturity 
- Generally Negative 
    - amount by which an option's value decreases every day 
    - all other values constant: option value will still decline with time
- Selling an Option = 'Positive Theta Trade" 
- Theta Accelerates: seller's earnings increase 
- Favorable to someone who writes option contracts 
    - cheaper to buy back options to close out short positions
> Call Option: 
> - Strike Price: `$1,150`
> - Option Price: `$5`
> - Underlying Asset: `$1,125`
> - To Expiration: 5 Days 
> - Theta: `$1` (aka value of the option drops `$1` per day until expiration) 
>> 2 Days Later: 
>> - Underlying Asset: `$1,125`
>> - Option Price: `$3` <br />
>>
>> Only way the `Option Price > $5` would be Underlying Asset Price rising above `$1,155`
>> - `$1,155 - $1,150 = $5` -> minimum to offset price of the option 
- Intrinsic Value: difference between underlying secuirty's price and the option's *strike price*
- Extrinisc Value: difference between Option's market price (premium) and it's *intrinsic value*
    - most affected by **Theta** 
    - also affected by *implied volatility*

# **Vega:** Rate of change between option's value and the underlying asset's *implied volatility*
- Option's price change in relation to a `1%` change of *implied volatility*
    - theoretical price change 
- Changes with large price movements from underlying asset 
- Falls when close to expiration 
- Used to Hedge Against Volatility
>  Competitive Spread: **Vega** > bid-ask-spread 
> - Stock Price: `$50`
> - Call Option: `$52.50`
>> - Bid Price: `$1.50`
>> - Ask Price: `$1.55`
> - Vega: `0.25`
> - Implied Vol: `30%`
>> Competitive: <br />
>> Vega: `0.25` > `$0.05` bid-ask-spread 
- too high of a spread is also dangerous as exiting can become increasingly difficult 
- increased vol: price goes up 
- decreased vol: price goes down 
> **Implied Volatility Increases by `1%`:**
>> - Bid Price: `$1.75` (1.50 + (1 x 0.25))
>> - Ask Price: `$1.80`(1.55 + (1 x 0.25))
> - Vega: `0.25`
> - Implied Vol: `31%`
>> Competitive: <br />
>> Vega: `0.25` > `$0.05` bid-ask-spread <br />
>
> **Implied Volatility Drops by `5%`:**
>> - Bid Price: `$0.25` (1.50 - (5 x 0.25))
>> - Ask Price: `$0.30`(1.55 - (5 x 0.25))
> - Vega: `0.25`
> - Implied Vol: `25%`
>> Competitive: <br />
>> Vega: `0.25` > `$0.05` bid-ask-spread 
## <br />
# **Rho:** Rate of Change between option's value and a `1%` interest rate change 
### Interest Rate Sensitivity
- rate of change per `1%` risk-free interest rate change
    - **Rho** = 1 -> IR increases by `1%` -> Value of the Option Increases by `1%` (perfectly correlated)
    - risk exposure to interest rate change 
- High Risk: at-the-money or long time to expiration 
> Call Option Price: `$4`
> - Rho: `0.25`
> - Risk-Free-Rate: `+1%`
>   - from `3%` to `4%`
>> New Call Option Price: `$4.25` <br />
>> Put Option Price (Below): `$9.35`
- Call Options Generally Rise in Price as IR increases
- Put Options Generally Degrease in Price as IR increases 
> Put Option Price: `$9`
> - Rho: `-0.35`
> - Risk-Free-Rate: `-1%`
>   - from `5%` to `4%`
>> New Put Option Price: `$9.35` <br />
>> Call Option Price (Above): `$3.75`
- Larger for in-the-money
- Smaller for out-of-the-money 
- Increases as Time to Expiration Increases 


---
---
# **Level of Underlying**
---
- returns on the underlying are normally distributed 

- time to expiration of one year
- no time to expiration 
- time to expiration of three years 


---
---
# **Brownian Motion**
---
---
##### Brownian Motion: 

---
---





### References: 
---
##### Fisher Black, Myron Scholes model thesis: 
- [The Pricing of Options and Corporate Liabilities](https://www.jstor.org/stable/1831029)

##### Robert C. Merton addition: 
- [Theory of Rational Option Pricing](https://www-jstor-org.i.ezproxy.nypl.org/stable/3003143?searchText=%22Theory+of+Rational+Option+Pricing%22&searchUri=%2Faction%2FdoBasicSearch%3FQuery%3D%25E2%2580%259CTheory%2Bof%2BRational%2BOption%2BPricing%25E2%2580%259D%26so%3Drel&ab_segments=0%2Fbasic_phrase_search%2Fcontrol&refreqid=fastly-default%3Ae82e4a7d53e2c0435fbebd8be045a80e&seq=1)

##### University Materials: 
- [City University of Hong Kong: Black Scholes Equations](https://www.math.cuhk.edu.hk/~rchan/teaching/math4210/chap08.pdf)
- [University of Chicago: Brownian Motion](https://galton.uchicago.edu/~lalley/Courses/313/BrownianMotionCurrent.pdf)
- [Berkeley: Brownian Motion](https://www.stat.berkeley.edu/~aldous/205B/bmbook.pdf)
- [MIT: Introduction to PDEs](https://ocw.mit.edu/courses/18-152-introduction-to-partial-differential-equations-fall-2011/resources/mit18_152f11_lec_01/)


##### Websites: 
- [Tokenist: Complete Guide to the Black-Scholes Model](https://tokenist.com/investing/black-scholes-model/)
- [Tokenist: Complete Guide to Implied Volatility](https://tokenist.com/investing/implied-volatility/)
- [SoFi: The Black-Scholes Model Explained](https://www.sofi.com/learn/content/what-is-the-black-scholes-model/)

##### Investopedia: 
- [Investopedia: How is Implied Volatility Used in the Black-Scholes Formula](https://www.investopedia.com/ask/answers/060115/how-implied-volatility-used-blackscholes-formula.asp)
- [Investopedia: Implied Volatility: Buy Low and Sell High](https://www.investopedia.com/articles/optioninvestor/08/implied-volatility.asp)
- [Investopedia: Log-Normal Distribution](https://www.investopedia.com/terms/l/log-normal-distribution.asp)
- [Investopedia: What is Delta?](https://www.investopedia.com/terms/d/delta.asp)
- [Investopedia: Delta Neutral](https://www.investopedia.com/terms/d/deltaneutral.asp)
- [Investopedia: Gamma Definition](https://www.investopedia.com/terms/g/gamma.asp)
- [Invvestopedia: Convexity](https://www.investopedia.com/terms/c/convexity.asp)
- [Investopedia: Alpha](https://www.investopedia.com/terms/a/alpha.asp)
- [Investopedia: Theta](https://www.investopedia.com/terms/t/theta.asp)
- [Investopedia: Extrinsic Value](https://www.investopedia.com/terms/e/extrinsicvalue.asp)
- [Investopedia: Vega Definition](https://www.investopedia.com/terms/v/vega.asp)
- [Investopedia: Rho](https://www.investopedia.com/terms/r/rho.asp)



  
    