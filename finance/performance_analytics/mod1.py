
# """
# defunct
# """

# # import pandas._tseries as _tseries
# # import pandas.stats.moments as moments
# from math import sqrt


# def return_annualised(returns, scale=12, geometric=True):
#     '''
#     Parameters
#     ----------
#     returns   : TimeSeries or DataFrame
#     scale     : integer [default=12]
#     geometric : boolean [default=True]

#     Returns
#     --------
#     float64 if `returns` is a TimeSeries
#     pandas.core.series.Series if `returns` is a DataFrame

#     scale n.  periods per year (daily=252, monthly=12, quarterly=4)
#     geometric geometric(True), simple(False) [default=True]

#     '''
#     scale = float(scale)
#     if geometric:
#         # R might be right after all... What does returns.count() give you??
#         return ((1+returns).prod() ** (scale/returns.count())) - 1

#     else:
#         return returns.mean() * scale


# def return_cumulative(returns, geometric=True):
#     '''
#     if geometric = True,  returns `prod(1+returns)-1`
#     if geometric = False, returns `sum(returns)`

#     Parameters
#     ----------
#     returns   : TimeSeries or DataFrame
#     geometric : boolean [default=True]

#     Returns
#     --------
#     float64 if `returns` is a TimeSeries
#     pandas.core.series.Series if `returns` is a DataFrame
#     '''

#     if geometric:
#         return (1 + returns).prod() - 1

#     else:
#         return returns.sum()


# def active_premium(portfolio_returns, benchmark_returns, scale=12):
#     '''The return on an investment's annualized return minus the benchmark's
#        annualized return.  [aka Excess Return]

#        Active Premium = portfolio ann. return - benchmark ann. return

#     Parameters
#     ----------
#     portfolio_returns : TimeSeries or DataFrame
#     benchmark_returns : TimeSeries [or DataFrame???]
#     scale : periods per year (daily=252, monthly=12, quarterly=4)

#     THIS ISN'T WORKING YET FOR SOME OF THE CODES
#     AND THE SUSPECTED REASON IS THE BENCHMAKRK SERIES NEEDS TO
#     BE TRUNCATED TO THE SAME AS THE SERIES BEING EXAMINED

#     Returns
#     --------

#     .. todo::
#        as this function stands you can't compare multiple returns against
#         multiple benchmarks... Something to come back to...

#         using a Panel might be the solution...
#     '''

#     p_returns = return_annualised(portfolio_returns, scale)
#     b_returns = return_annualised(benchmark_returns, scale)

#     # I think what you need to do here is loop through p_returns
#     # and match up the dates... ie so that you're not using the
#     # the full series of b_returns for each p_return.

#     # and that means that you need to *compose* a data frame
#     # (or possibly a panel) for the returned data.

#     return p_returns - b_returns


# def tracking_error(portfolio_returns, benchmark_returns, scale=12):
#     '''A measure of the unexplained portion of performance relative
#        to a benchmark

#     TE = sqrt(sum(Ra - Rb)^2 / (length(R) - 1)) * sqrt(scale)
#     TE = std(Ra-Rb) * sqrt(scale)

#     Parameters
#     ----------
#     portfolio_returns : TimeSeries or DataFrame
#     benchmark_returns : TimeSeries [or DataFrame???]
#     scale : periods per year (daily=252, monthly=12, quarterly=4)

#     '''
#     # this only works 1 against 1 -- which is no good...!!!
#     scale = float(scale)
#     R = portfolio_returns - benchmark_returns
#     return R.std() * sqrt(scale)


# def information_ratio(portfolio_returns, benchmark_returns, scale=12):
#     '''This relates the *degree* to which an investment has beaten the
#     benchmark to the *consistency* with which the investment has beaten the
#     benchmark.

#     Parameters
#     ----------
#     portfolio_returns : TimeSeries or DataFrame
#     benchmark_returns : TimeSeries [or DataFrame???]
#     scale : periods per year (daily=252, monthly=12, quarterly=4)
#     '''

#     ap = active_premium(portfolio_returns, benchmark_returns, scale=scale)
#     te = tracking_error(portfolio_returns, benchmark_returns, scale=scale)

#     return ap / te


# # def leverage(weights):
# #     """
# #     Parameters
# #     ----------

# #     Returns
# #     -------
# #     y : TimeSeries
# #     """
# #     pass


# # def turnover(weights):
# #     """

# #     Returns
# #     -------
# #     y : TimeSeries
# #     """
# #     pass


# # def max_drawdown(returns):
# #     """
# #     Parameters
# #     ----------
# #     returns : TimeSeries or DataFrame

# #     """
# #     pass


# # def sharpe_ratio(returns):
# #     """

# #     Parameters
# #     ----------
# #     returns : TimeSeries or DataFrame

# #     Returns
# #     -------
# #     y : Series
# #     """
# #     pass


# # def rolling_sharpe_ratio(returns, window, min_periods=None):
# #     """

# #     Parameters
# #     ----------
# #     returns : TimeSeries or DataFrame


# #     Returns
# #     -------
# #     y : TimeSeries or DataFrame
# #     """
# #     pass


# # def beta(returns, market_returns):
# #     """

# #     Parameters
# #     ----------
# #     returns : TimeSeries or DataFrame


# #     Returns
# #     -------
# #     y : TimeSeries or DataFrame
# #     """
# #     pass

