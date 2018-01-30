import pytest
import datetime
import weatherclock

def test_11oclockpm_before_midnight():
    d = datetime.date(2018, 1, 14)
    t = datetime.time(23, 00)
    assert not weatherclock.is_after_midnight(datetime.datetime.combine(d,t))

def test_530am_after_midnight():
    d = datetime.date(2018, 1, 14)
    t = datetime.time(5, 30)
    assert weatherclock.is_after_midnight(datetime.datetime.combine(d,t))

def test_12oclockpm_before_midnight():
    d = datetime.date(2018, 1, 14)
    t = datetime.time(12, 00)
    assert not weatherclock.is_after_midnight(datetime.datetime.combine(d,t))

def test_is_tonight_currently_before_midnight_forecast_10pm():
    d = datetime.datetime.now().date()
    forecast_time = datetime.datetime.combine(d, datetime.time(22, 00))
    sunset_time = datetime.datetime.combine(d, datetime.time(18, 00))
    sunrise_time = datetime.datetime.combine(d, datetime.time(6, 00))
    assert weatherclock.is_tonight(forecast_time,sunrise_time,sunset_time,False)

def test_is_tonight_currently_after_midnight_forecast_3am():
    d = datetime.datetime.now().date()
    forecast_time = datetime.datetime.combine(d, datetime.time(3, 00))
    sunset_time = datetime.datetime.combine(d, datetime.time(18, 00))
    sunrise_time = datetime.datetime.combine(d, datetime.time(6, 00))
    assert weatherclock.is_tonight(forecast_time,sunrise_time,sunset_time,True)

def test_is_tonight_currently_before_midnight_forecast_1am_tomorrow():
    d = datetime.datetime.now().date()
    tomorrowdate = d + datetime.timedelta(days=1)
    forecast_time = datetime.datetime.combine(tomorrowdate, datetime.time(1, 00))
    sunset_time = datetime.datetime.combine(d, datetime.time(18, 00))
    sunrise_time = datetime.datetime.combine(d, datetime.time(6, 00))
    assert weatherclock.is_tonight(forecast_time,sunrise_time,sunset_time,False)

def test_is_tonight_currently_before_midnight_forecast_11am_tomorrow():
    d = datetime.datetime.now().date()
    tomorrowdate = d + datetime.timedelta(days=1)
    forecast_time = datetime.datetime.combine(tomorrowdate, datetime.time(11, 00))
    sunset_time = datetime.datetime.combine(d, datetime.time(18, 00))
    sunrise_time = datetime.datetime.combine(d, datetime.time(6, 00))
    assert not weatherclock.is_tonight(forecast_time,sunrise_time,sunset_time,False)