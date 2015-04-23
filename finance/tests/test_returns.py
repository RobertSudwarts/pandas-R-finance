# import sys
import os
from nose.tools import eq_
from pandas import *
from finance import returns


def setup():
    global mgrs
    global mgr_index
    pth = os.path.dirname(__file__)
    DATAFILE = os.path.join(pth, 'managers.csv')
    mgrs = read_csv(DATAFILE, index_col=0, parse_dates=True)
    mgr_index = ['HAM1', 'HAM2', 'HAM3', 'HAM4', 'HAM5', 'HAM6',
                 'EDHEC LS EQ', 'SP500 TR', 'US 10Y TR', 'US 3m TR']


class TestReturnCumulative:
    # tests the cumulative return function for:
    #   a. single set of returns
    #   b. multiple sets of returns
    #   c. using `geometric` True/False for both
    def test_single_geometricTrue(self):
        result = returns.cumulative(mgrs.HAM1, geometric=True)
        eq_(result.round(4), 3.1267)

    def test_multiple_geometricTrue(self):
        vals = [3.127, 4.349, 3.707, 2.529, 0.265, 0.986, 2.051,
                1.762, 0.734, 0.5297]
        expected_series = Series(vals, index=mgr_index)
        result = returns.cumulative(mgrs)

        for e, v in zip(result, expected_series):
            eq_(abs(e - v) < 1e-3, True)

    def test_single_geometricFalse(self):
        expected_val = 1.4682
        result = returns.cumulative(mgrs.HAM1, geometric=False)
        eq_(abs(result - expected_val) < 1e-4, True)

    def test_multiple_geometricFalse(self):
        vals = [1.4682, 1.7679, 1.643, 1.4542, 0.3148, 0.7075,
                1.1454, 1.143825, 0.57888, 0.42589]
        expected_series = Series(vals, index=mgr_index)
        result = returns.cumulative(mgrs, geometric=False)

        for e, v in zip(result, expected_series):
            eq_(abs(e - v) < 1e-5, True)


class TestReturnAnnualised:

    def test_single_geoTrue(self):
        result = returns.annualised(mgrs.HAM1)
        expected_val = 0.137532
        eq_(abs(result - expected_val) < 1e-6, True)

    def test_multiple_geoTrue(self):
        vals = [0.1375, 0.1747, 0.1512, 0.1215, 0.03732, 0.1373, 0.1180,
                0.0968, 0.0513, 0.0394]
        expected_series = Series(vals, index=mgr_index)

        result = returns.annualised(mgrs)

        for e, v in zip(result, expected_series):
            # tolerance to 1e-4
            eq_(abs(e - v) < 1e-4, True)

    def test_multiple_geoFalse(self):
        vals = [0.1335, 0.1697, 0.1494, 0.1322, 0.0491, 0.1327, 0.1145,
                0.1040, 0.0526, 0.03872]
        expected_series = Series(vals, index=mgr_index)

        result = returns.annualised(mgrs, geometric=False)

        for e, v in zip(result, expected_series):
            # tolerance to 1e-4
            eq_(abs(e - v) < 1e-4, True)

    def test_single_geoFalse(self):
        result = returns.annualised(mgrs.HAM1, geometric=False)
        expected_val = 0.1334727
        eq_(abs(result - expected_val) < 1e-7, True)

    def test_single_geoFalse_quarterly_scale(self):
        # test using a scale other than the default [=12]
        # here we use quarterly [=4]
        result = returns.annualised(mgrs.HAM1, scale=4, geometric=False)
        expected_val = 0.04449091
        eq_(abs(result - expected_val) < 1e-7, True)
