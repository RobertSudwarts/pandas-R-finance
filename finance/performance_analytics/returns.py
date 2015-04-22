

import pandas._tseries as _tseries
import pandas.stats.moments as moments
from pandas import TimeSeries, DataFrame
from math import sqrt

# constants for "sqrt of time" rule.
DAILY = 252
WEEKLY = 52
MONTHLY = 12
QUARTERLY = 4
YEARLY = 1

def annualised(R, scale=12, geometric=True):
    '''
    
    Parameters
    ----------
    R [returns] : TimeSeries or DataFrame
    scale     : integer [default=12]
    geometric : boolean [default=True]
    
    Returns
    --------
    float64 if `returns` is a TimeSeries
    pandas.core.series.TimeSeries if `returns` is a DataFrame

    scale n.  periods per year (eg. daily=252, monthly=12, quarterly=4)
    geometric [True]  ->  (1+returns).prod() ** (scale/n) - 1
    geometric [False] ->  returns.mean() * scale

    '''
    scale = float(scale)
    if geometric:
        n = R.count()
        return (1+R).prod() ** (scale/n) - 1
        
    else:
        return R.mean() * scale
        
        
def cumulative(R, geometric=True):
    '''
    
    
    Parameters
    ----------
    R [returns] : TimeSeries or DataFrame
    geometric : boolean [default=True]
    
    Returns
    --------
    float64 if `returns` is a TimeSeries
    pandas.core.series.Series if `returns` is a DataFrame
    
    geometric [True]  -> (1+returns).prod() - 1`
    geometric [False] -> returns.sum()
    
    '''
    
    if geometric:
        return (1 + R).prod() - 1
        
    else:
        return R.sum()
