""" Tests the Forecast Summary class """
import pytest
from forecastsummary import ForecastSummary
import math

def test_new_summary():
    test_sumary = ForecastSummary()
    assert math.isnan(test_sumary.max_temp)

def test_summary_first_temp():
    test_sumary = ForecastSummary()
    test_sumary.eval_new_temp(5.4)
    assert test_sumary.max_temp == 5.4
    assert test_sumary.min_temp == 5.4

def test_summary_2temp_evals():
    test_sumary = ForecastSummary()
    test_sumary.eval_new_temp(5.4)
    test_sumary.eval_new_temp(10)
    assert test_sumary.max_temp == 10
    assert test_sumary.min_temp == 5.4

def test_prevailing_condition_1_condition():
    test_sumary = ForecastSummary()
    test_sumary.add_condition('Cloudy')
    assert test_sumary.get_prevailing_condition() == 'Cloudy'

def test_prevailing_condition_3_conditions():
    test_sumary = ForecastSummary()
    test_sumary.add_condition('Cloudy')
    test_sumary.add_condition('Snow')
    test_sumary.add_condition('Cloudy')
    assert test_sumary.get_prevailing_condition() == 'Cloudy'

