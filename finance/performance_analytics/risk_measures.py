
"""
Compute common portfolio statistics
"""

import pandas._tseries as _tseries
import pandas.stats.moments as moments
from pandas import TimeSeries, DataFrame
import returns
from math import sqrt

# constants for "sqrt of time" rule.
DAILY = 252
WEEKLY = 52
MONTHLY = 12
QUARTERLY = 4
YEARLY = 1

       
# left as a lambda as an aide memoire(!) and in case there's 
# a call for simply presenting two annualised returns...
_active_premium = lambda Rp, Rb: Rp - Rb
        
def active_premium(Rp, Rb, scale=12):
    '''The return on an investment's annualized return minus the benchmark's 
       annualized return.  [aka Excess Return]

       Active Premium = portfolio ann. return - benchmark ann. return
    
    .. note:: 
       the methodoloy used here relies on pairwise comparison of each 
       'portfolio' returns series to each 'benchmark' return series; reason
       being, that `annualised return` [whilst sharing the same 
       frequency/scale] should be directly comparable where the series are of 
       different lengths such that, where Rp[A, B, C] vs Rb[X, Y].  
       `annualised return` for 'X' will be different if the periods for 
       'A', 'B' & 'C' are different 
    
    Parameters
    ----------
    Rp [portfolio returns] : TimeSeries or DataFrame
    Rb [benchmark returns] : TimeSeries or DataFrame
    scale : periods per year (daily=252, monthly=12, quarterly=4)
    
    Returns
    --------
    DataFrame
    [or `float` when both Rp & Rb are TimeSeries]
    
    '''
    
    def calc(df):
        '''
        The rationale for passing in a DataFrame (consisting of only the 
        portfolio and benchmark series) is simply to use the dropna() function 
        on the combined set of data.
        '''
        df = df.dropna()
        p_ar = returns.annualised(df['p'], scale)
        b_ar = returns.annualised(df['b'], scale)
        # [pointlessly?] uses lambda function above for the subtraction
        return _active_premium(p_ar, b_ar)
    
    assert isinstance(Rp, (DataFrame, TimeSeries)), \
            "portfolio_returns must be either a `DataFrame` or a `TimeSeries`" 
    assert isinstance(Rb, (DataFrame, TimeSeries)), \
            "benchmark_returns must be either a `DataFrame` or a `TimeSeries`" 
    
    if isinstance(Rp, TimeSeries) and isinstance(Rb, TimeSeries):
        # we can take a short cut and return the result as a float
        df = DataFrame({'p': Rp, 'b': Rb})
        ap = calc(df)
        return ap
    
    # If either Rp or Rb are `TimeSeries`, we force them into a `DataFrame`
    # with just a single column : the rationale being that we're then able
    # to use a nested for...next loop.
    if isinstance(Rp, TimeSeries):
        Rp = DataFrame({Rp.name: Rp})
        
    if isinstance(Rb, TimeSeries):
        Rb = DataFrame({Rb.name: Rb})
        
    D = {}
    for p in Rp.columns:
        D[p] = {}
        for b in Rb.columns:
            df = DataFrame({'p': Rp[p], 'b': Rb[b]})
            D[p][b] = calc(df)
            
    return DataFrame.from_dict(D, orient='index')
     

def tracking_error(Rp, Rb, scale=12):
    '''A measure of the unexplained portion of performance relative 
       to a benchmark
    
    TE = sqrt(sum(Ra - Rb)^2 / (length(R) - 1)) * sqrt(scale)
    TE = std(Ra-Rb) * sqrt(scale)
    
    Parameters
    ----------
    Rp [portfolio returns] : TimeSeries or DataFrame
    Rb [benchmark returns] : TimeSeries [or DataFrame???]
    scale : periods per year (daily=252, monthly=12, quarterly=4)
    
    Returns
    --------
    
    Interesting... Here, R uses the Excess return function
        
    '''
    scale = float(scale)
    def _calc(Rp, Rb):
        R = Rp - Rb
        return R.std() * sqrt(scale)
    
    


def information_ratio(Rp, Rb, scale=12):
    '''This relates the *degree* to which an investment has beaten the 
    benchmark to the *consistency* with which the investment has beaten the 
    benchmark.
    
    Parameters
    ----------
    Rp [portfolio returns] : TimeSeries or DataFrame
    Rb [benchmark returns] : TimeSeries [or DataFrame???]
    scale : periods per year (daily=252, monthly=12, quarterly=4)
    '''
    
    ap = active_premium(Rp, Rb, scale=12)
    te = tracking_error(Rp, Rb, scale=12)

    return ap / te

    
def leverage(weights):
    """
    Parameters
    ----------

    Returns
    -------
    y : TimeSeries
    """
    pass

def turnover(weights):
    """

    Returns
    -------
    y : TimeSeries
    """
    pass

def max_drawdown(returns):
    """
    Parameters
    ----------
    returns : TimeSeries or DataFrame

    """
    pass

def sharpe_ratio(returns):
    """

    Parameters
    ----------
    returns : TimeSeries or DataFrame

    Returns
    -------
    y : Series
    """
    pass

def rolling_sharpe_ratio(returns, window, min_periods=None):
    """

    Parameters
    ----------
    returns : TimeSeries or DataFrame


    Returns
    -------
    y : TimeSeries or DataFrame
    """
    pass

def beta(returns, market_returns):
    """

    Parameters
    ----------
    returns : TimeSeries or DataFrame


    Returns
    -------
    y : TimeSeries or DataFrame
    """
    pass
    
def sortino_ratio(): pass
def jensens_alpha(): pass 
def calmar_ratio(): pass
def treynor_measure(): pass 

