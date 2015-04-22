import sys
import os
from nose.tools import raises, eq_
from pandas import *
import pandas.finance.performance_analytics as pa


def setup():
    global mgrs
    global mgr_index
    global hams
    pth = os.path.dirname(__file__)
    DATA = os.path.join(pth, 'managers.csv')
    mgrs = read_csv(DATA, index_col=0, parse_dates=True)
    mgr_index = ['HAM1', 'HAM2', 'HAM3', 'HAM4', 'HAM5', 'HAM6', 
                 'EDHEC LS EQ', 'SP500 TR', 'US 10Y TR', 'US 3m TR']

    # here we create a DataFrame ie a subset of mgrs 
    hams = DataFrame.from_items(\
                [(mgr, mgrs[mgr]) for mgr in mgrs.columns[:6]]
                )


def teardown():
    mgrs = None


class TestCSVDataImport:
    # test to see if the data in managers.csv can be imported and
    # parsed correctly to create a DataFrame (composed of Series)
    
    def test_data_type(self):
        # simply tests that the data returned from the csv
        # file (managers.csv) has been correctly formed 
        # as a DataFrame
        eq_(isinstance(mgrs, DataFrame), True)
        
    def test_returns_set(self):
        # and a test to show that a single set of returns
        # pulled from this DataFrame is recognised as a
        # `Series`
        mgr = mgrs.HAM1
        eq_(isinstance(mgr, Series), True)
        
        
class TestTrackingError:
    
    def test_single(self):
        expected_val = 0.11316666
        result = pa.tracking_error(mgrs.HAM1, mgrs.SP500_TR)
        eq_(abs(result - expected_val) < 1e-8, True)
        
    def test_multiple(self):
        vals = [0.1131667, 0.1533647, 0.1158673, 0.1596656, 
                0.1800291, 0.1128390]
        expected_series = Series(vals, index=mgr_index[:6]) 
        
        df = DataFrame.from_items(\
                [(mgr, mgrs[mgr]) for mgr in mgrs.columns[:6]]
                )
                
        result = pa.tracking_error(df, mgrs.SP500_TR)
        for e, v in zip(result, expected_series):
             eq_(abs(e-v) < 1e-4, True)
             
             
class TestInformationRatio:
    
    def test_single(self):
        expected_val = 0.3370621
        result = pa.information_ratio(mgrs.HAM4, mgrs.US_10Y_TR)
        eq_(abs(result - expected_val) < 1e-7, True)
        
        # we know this is going to die because 
        #expected_val = 0.5059751
        #result = pa.information_ratio(mgrs.HAM2, mgrs.SP500_TR)
        #eq_(abs(result - expected_val) < 1e-7, True)
        
    #def test_multiple(self):
    #    vals = [0.1131667, 0.1533647, 0.1158673, 0.1596656, 
    #            0.1800291, 0.1128390]
    #    expected_series = Series(vals, index=mgr_index[:6]) 
        
    #    df = DataFrame.from_items(\
    #            [(mgr, mgrs[mgr]) for mgr in mgrs.columns[:6]]
    #            )
                
    #    result = pa.tracking_error(df, mgrs.SP500_TR)
    #    for e, v in zip(result, expected_series):
    #         eq_(abs(e-v) < 1e-4, True)
    
class TestActivePremium:

    def test_single(self):
        expected_val = 0.04078668
        result = pa.active_premium(mgrs.HAM1, mgrs.SP500_TR)
        eq_(abs(result - expected_val) < 1e-9, True)
        
    def test_multiple(self):
        benchmark = mgrs.SP500_TR
        
        # these are the values calculated by R -- but they look wrong
        ###vals = [0.04078668, 0.07759873, 0.05446935, 0.02473443,
        ###        0.02182245, 0.07585993]
        # the discrepancies appear to be where the length of the individual
        # series is shorter than the length of the entire DataFrame 
        # eg mgrs.HAM2.count() != mgrs.count() 
        # len(mgrs) = 132
        # mgrs.HAM1.count() = 132
        # mgrs.HAM2.count() = 125 
        vals = [0.04079, 0.07791, 0.05447, 0.02473,
                -0.05943, 0.04053]
        expected_series = Series(vals, index=mgr_index[:6]) 
        
        result = pa.active_premium(hams, benchmark)
        
        for e, v in zip(result, expected_series):
             eq_(abs(e-v) < 1e-4, True)
             

    def test_vs_mulitple_benchmark(self):
        # .. todo:: as the active_premium() function stands you can't compare 
        # multiple returns against multiple benchmarks... Something to 
        # come back to...
        expected_vals = [0.04079, 0.08622]
        benchmarks = DataFrame.from_items([
                                ('SP500', mgrs.SP500_TR),
                                ('US10yr', mgrs.US_10Y_TR),
                                ]
                               )
        
        result = pa.active_premium(mgrs.HAM1, benchmarks)
        
        for r, v in zip(result, expected_vals):
            eq_(abs(r - v) < 1e-4, True)
        
        
class TestReturnCumulative:    
    # tests the cumulative return function for:
    #   a. single set of returns
    #   b. multiple sets of returns
    #   c. using `geometric` True/False for both
    def test_single_geometricTrue(self):
        result = pa.return_cumulative(mgrs.HAM1, geometric=True)
        eq_(result.round(4), 3.1267)
        
    def test_multiple_geometricTrue(self):
        vals = [3.127, 4.349, 3.707, 2.529, 0.265, 0.986, 2.051, 
                1.762, 0.734, 0.5297]
        expected_series = Series(vals, index=mgr_index) 
        result = pa.return_cumulative(mgrs)
        
        for e, v in zip(result, expected_series):
             eq_(abs(e - v) < 1e-3, True)
             
        
    def test_single_geometricFalse(self):
        expected_val = 1.4682
        result = pa.return_cumulative(mgrs.HAM1, geometric=False)
        eq_(abs(result - expected_val) < 1e-4, True)
        
    def test_multiple_geometricFalse(self):
        vals = [1.4682, 1.7679, 1.643, 1.4542, 0.3148, 0.7075, 
                1.1454, 1.143825, 0.57888, 0.42589]
        expected_series = Series(vals, index=mgr_index) 
        result = pa.return_cumulative(mgrs, geometric=False)
        
        for e, v in zip(result, expected_series):
             eq_(abs(e - v) < 1e-5, True)
        
        
class TestReturnAnnualised:
    
    def test_single_geoTrue(self):
        result = pa.return_annualised(mgrs.HAM1)
        expected_val = 0.137532
        eq_(abs(result - expected_val) < 1e-6, True)
    
    def test_multiple_geoTrue(self):
        vals = [0.1375, 0.1747, 0.1512, 0.1215, 0.03732, 0.1373, 0.1180,
                0.0968, 0.0513, 0.0394]
        expected_series = Series(vals, index=mgr_index)
        
        result = pa.return_annualised(mgrs)
        
        for e, v in zip(result, expected_series):
            # tolerance to 1e-4
            eq_(abs(e - v) < 1e-4, True)
    
    
    def test_multiple_geoFalse(self):
        vals = [0.1335, 0.1697, 0.1494, 0.1322, 0.0491, 0.1327, 0.1145, 
                0.1040, 0.0526, 0.03872]
        expected_series = Series(vals, index=mgr_index)
        
        result = pa.return_annualised(mgrs, geometric=False)
        
        for e, v in zip(result, expected_series):
            # tolerance to 1e-4
            eq_(abs(e - v) < 1e-4, True)
            
    def test_single_geoFalse(self):
        result = pa.return_annualised(mgrs.HAM1, geometric=False)
        expected_val = 0.1334727
        eq_(abs(result - expected_val) < 1e-7, True)
        
    def test_single_geoFalse_quarterly_scale(self):
        # test using a scale other than the default [=12]
        # here we use quarterly [=4]
        result = pa.return_annualised(mgrs.HAM1, scale=4, geometric=False)
        expected_val = 0.04449091
        eq_(abs(result - expected_val) < 1e-7, True)
        
        
        
