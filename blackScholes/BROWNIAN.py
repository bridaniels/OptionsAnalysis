# Geometric Brownian Motion 
import numpy as np
import pandas as pd
import datetime as dt



# Class to Model Market Environment Relevant for Valuation 
class MarketEnvironment(object): 
    def __init__(self, name, pricing_date): 
        self.name = name
        self.pricing_date = pricing_date
        self.constants = {}
        self.lists = {}
        self.curves = {}
        
    def add_constant(self,key,constant): 
        self.constants[key] = constant 
    def get_constant(self,key): 
        return self.constants[key]
    
    def add_list(self, key, list_object): 
        self.lists[key] = list_object
    def get_list(self, key):
        return self.lists[key]
    
    def add_curve(self, key, curve): 
        self.curves[key] = curve
    def get_curve(self, key): 
        return self.curves[key]
    
    def add_environment(self, env): 
        for key in env.constants: 
            self.constants[key] = env.constants[key]
        for key in env.lists: 
            self.lists[key] = env.lists[key]
        for key in env.curves: 
            self.curves[key] = env.curves[key]


# Simulation Class to Simulate Various Models
class SimulationClass(object): 
    def __init__(self, name, mar_env, corr): 
        try: 
            self.name = name
            self.pricing_date = mar_env.pricing_date
            self.initial_value = mar_env.get_constant('initial_value')
            self.volatility = mar_env.get_constant('volatility')
            self.final_date = mar_env.get_constant('final_date')
            self.currency = mar_env.get_constant('currency')
            self.frequency = mar_env.get_constant('frequency')
            self.paths = mar_env.get_constant('paths')
            self.discount_curve = mar_env.get_constant('discount_curve')
        
            try: 
                self.time_grid = mar_env.get_list('time_grid')
            except: 
                self.time_grid = None
        
            #try: 
            #    self.special_dates = mar_env.get_list('special_dates')
            #except: 
            #    self.special_dates = None
        
            self.instrument_values = None
            self.correlated = corr
            if corr is True: 
                self.cholesky_matrix = mar_env.get_list('cholesky_matrix')
                self.rn_set = mar_env.get_list('rn_set')[self.name]
                self.random_numbers = mar_env.get_list('random_numbers')
        except: 
            print("Error Parsing Market Environment")
            
            
        
    def generate_time_grid(self): 
        start = self.pricing_date
        end = self.final_date
        
        time_grid = pd.date_range(start=start, end=end, freq=self.frequency).to_pydatetime()
        time_grid = list(time_grid)
        
        if start not in time_grid: 
            time_grid.insert(0,start)
        if end not in time_grid:
            time_grid.append(end)
        #if len(self.special_dates) > 0: 
        #    time_grid.extend(self.special_dates)
        #    time_grid = list(set(time_grid)) #delete duplicates
        #    time_grid.sort()
        self.time_grid = np.array(time_grid) 
        
        
    def get_instrument_values(self, fixed_seed=True): 
        if self.instrument_values is None: 
            # self.generate_paths in GeometricBrownianMotion
            self.generate_paths(fixed_seed=fixed_seed, day_count=365.)
        elif fixed_seed is False: 
            self.generate_paths(fixed_seed=fixed_seed, day_count=365.)
        return self.instrument_values


# Generates Simulated Paths
# Super Method -> calls SimulationClass
class GeometricBrownianMotion(SimulationClass): 
    
    def __init__(self, name, mar_env, corr=False): 
        super(GeometricBrownianMotion, self).__init__(name, mar_env, corr)
        
    
    def update(self, initial_value=None, volatility=None, final_date=None): 
        if initial_value is not None: 
            self.initial_value = initial_value
        if volatility is not None: 
            self.volatility = volatility
        if final_date is not None: 
            self.final_date = final_date
    
    def generate_paths(self, fixed_seed=False, day_count=365.):
        if self.time_grid is None: 
            self.generate_time_grid()
        
        M = len(self.time_grid)
        J = self.paths
        paths = np.zeros((M,J))
        
        if not self.correlated: 
            rand = sn_random_numbers((1,M,J), fixed_seed=fixed_seed)
        else: 
            rand = self.random_numbers
        
        short_rate = self.discount_curve.short_rate
        for t in range(1, len(self.time_grid)):
            if not self.correlated:
                ran = rand[t]
            else: 
                ran = np.dot(self.cholesky_matrix, rand[:, t, :])
                ran = ran[self.rn_set]
            dt = (self.time_grid[t] - self.time_grid[t-1]).days/day_count
            paths[t] = paths[t-1] * np.exp((short_rate - 0.5 * 
                                    self.volatility**2) * dt + 
                                    self.volatility*np.sqrt(dt)*ran)
        self.instrument_values = paths 

class ConstantShortRate(object):
    
    def __init__(self, name, short_rate): 
        self.name=name
        self.short_rate = short_rate 
        if short_rate < 0: 
            raise ValueError("Negative Short Rate")
    
    def get_discount_factors(self, date_list, dtobjects=True): 
        if dtobjects is True: 
            dlist = get_year_deltas(date_list)
        else: 
            dlist = np.array(date_list)
        dflist = np.exp(self.short_rate * -dlist)
        return np.array((date_list, dflist)).T


# returns array of random numbers that are normall distributed 
def sn_random_numbers(shape, antithetic=True, moment_matching=True, fixed_seed=False):
    '''input -> shape: tuple(o,n,m) of (pesudo) random numbers
    Results
    =======
    ran: tuple of (o,n,m) PseudoRandom Numbers'''
    if fixed_seed:
        np.random.seed(1000)
    if antithetic: 
        ran = np.random.standard_normal((shape[0],shape[1],shape[2] // 2))
        ran = np.concatenate((ran, -ran), axis=2)
    else: 
        ran = np.random.standard_normal(shape)
    if moment_matching:
        ran = ran - np.mean(ran)
        ran = ran / np.std(ran)
    if shape[0] == 1:
        return ran[0]
    else: return ran


def get_year_deltas(date_list, day_count=365): 
    start = min(date_list)
    delta_list = [(date - start).days / day_count for date in date_list]
    return np.array(delta_list)



me_gbm = MarketEnvironment('me_gbm', dt.datetime(2020,1,1))

me_gbm.add_constant('initial_value',36)
me_gbm.add_constant('volatility', 0.1)
me_gbm.add_constant('final_date', dt.datetime(2020,12,31))
me_gbm.add_constant('currency', 'EUR')
me_gbm.add_constant('frequency', 'M')
me_gbm.add_constant('paths', 10000)

csr = ConstantShortRate('csr', 0.05)
me_gbm.add_curve('discount_curve', csr)

gbm = GeometricBrownianMotion('gbm', me_gbm)

gbm.generate_time_grid()
paths_1 = gbm.get_instrument_values()
gbm.update(volatility=0.5)
paths_2 = gbm.get_instrument_values(fixed_seed=False)




import matplotlib.pyplot as plt
plt.figure(figsize=(16,5))
p1 = plt.plot(gbm.time_grid, paths_1[:,:15], 'b')
p2 = plt.plot(gbm.time_grid, paths_2[:,:15], 'r-.')
plt.grid(True)
l1 = plt.legend([p1[0], p2[0]], ['LowVolatility', 'HighVolatility'], loc=2)
plt.gca().add_artist(l1)
plt.xticks(rotation=30)
plt.show()