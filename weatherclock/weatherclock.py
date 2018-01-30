import requests
import json
import datetime
import config as cfg
import math
from collections import Counter

# Now: temperature, condition
# Today: min / max temperature, condition, snowfall or rainfall (if applicable). Today covers sunrise to sunset
#   If it is currently night, skip Today
# Tonight: Same as today, covers sunset to sunrise
# Tomorrow: sunrise to sunset, next day

payload = {'id':cfg.owm['cityid'], 'appid':cfg.owm['apikey'], 'units': 'metric'}
r = requests.get(cfg.owm['url']+'weather', params=payload)
now = r.json()
today = []
tonight = []
tomorrow = []

today_summary = {'max_temp':float('nan'), 'min_temp':float('nan'), 'total_rainfall':0, 'total_snowfall':0, 'conditions':[]}
tonight_summary = {'max_temp':float('nan'), 'min_temp':float('nan'), 'total_rainfall':0, 'total_snowfall':0, 'conditions':[]}
tomorrow_summary = {'max_temp':float('nan'), 'min_temp':float('nan'), 'total_rainfall':0, 'total_snowfall':0, 'conditions':[]}

def get_time(weather):
    return datetime.datetime.fromtimestamp(int(weather['dt']))

def get_sunrise(weather):
    return datetime.datetime.fromtimestamp(int(now['sys']['sunrise']))
def get_sunset(weather):
    return datetime.datetime.fromtimestamp(int(now['sys']['sunset']))

def get_temp(weather):
    return weather['main']['temp']

def get_condition(weather):
    return weather['weather'][0]['main']

def get_rainfall(weather):
    return float(weather['rain'].get('3h',0)) if 'rain' in weather else 0

def get_snowfall(weather):
    return float(weather['snow'].get('3h',0)) if 'snow' in weather else 0

def is_after_midnight(somedate):
    current_time = somedate.time()
    if  current_time < datetime.time(6,00):
        return True
    else:
        return False

def is_tonight(forecast_time, sunrise_time, sunset_time,after_midnight):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    # print('Is today?',forecast_time.date() == today)
    # print('Is after midnight?',after_midnight)

    #1. It is currently after midnight and Forecast time is today before sunrise
    if (forecast_time.date() == today and after_midnight and forecast_time.time() < sunrise_time.time()):
        return True
    #2. It is currently before midnight and Forecast time is today after sunset
    if (forecast_time.date() == today and not after_midnight and forecast_time.time() > sunset_time.time()):
        return True
    #3. It is currently before midnight and Forecast time is tomorrow before sunrise
    if (forecast_time.date() == tomorrow and not after_midnight and forecast_time.time() < sunrise_time.time()):
        return True
    
    return False

def when_is_it(now, weather):
    # Today: if forecast is today and forecast time < now sunset
    # Tonight: (It is currently before midnight and Forecast time is today after sunset or tomorrow before sunrise) or
    #           (it is currently after midnight and forecast time is today before sunrise)
    # Tomorrow: (It is currently before sunrise and forecast time is today) or 
    #           (it is after sunrise and  Forecast time is tomorrow before sunset)
    sunrise = get_sunrise(now)
    sunset = get_sunset(now)
    forecast_time = get_time(weather)
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    if forecast_time.date() == today and forecast_time.time() > sunrise.time() and forecast_time.time() < sunset.time():
        return 'Today'
    if is_tonight(forecast_time,sunrise,sunset,is_after_midnight(datetime.datetime.now())):
       return 'Tonight'
    if forecast_time.date() == tomorrow and forecast_time.time() > sunrise.time() and forecast_time.time() < sunset.time():
        return 'Tomorrow'
    else:
        return 'Not Today, Tonight or Tomorrow'

def set_min_and_max_temp(summary, temp):
    if math.isnan(summary['max_temp']) or summary['max_temp'] < temp:
        summary['max_temp'] = temp
    if math.isnan(summary['min_temp']) or summary['min_temp'] > temp:
        summary['min_temp'] = temp

if __name__ == '__main__':
    print('Weather in',now['name'],now['weather'][0]['main'],now['main']['temp'],datetime.datetime.fromtimestamp(int(now['dt'])),'Sunrise: ',datetime.datetime.fromtimestamp(int(now['sys']['sunrise'])).strftime('%I:%M %p'),'Sunset: ',datetime.datetime.fromtimestamp(int(now['sys']['sunset'])).strftime('%I:%M %p'))

    payload['cnt'] = 12
    r = requests.get(cfg.owm['url']+'forecast',params=payload)
    forecast = r.json()

    for counter,weather in enumerate(forecast['list']):
        time_of_day = when_is_it(now,weather)
        print('...', counter,get_time(weather),
            'temp:', get_temp(weather),
            'condition: ', get_condition(weather),
            'rainfall:', get_rainfall(weather),
            'snowfall:', get_snowfall(weather),
            time_of_day) 
        _temp = get_temp(weather)
        if time_of_day == 'Today':
            today.append(weather)
            set_min_and_max_temp(today_summary, _temp)
            today_summary['total_rainfall'] += get_rainfall(weather)
            today_summary['total_snowfall'] += get_snowfall(weather)
            today_summary['conditions'].append(get_condition(weather))

        elif time_of_day == 'Tonight':
            tonight.append(weather)
            set_min_and_max_temp(tonight_summary, _temp)
            tonight_summary['total_rainfall'] += get_rainfall(weather)
            tonight_summary['total_snowfall'] += get_snowfall(weather)
            tonight_summary['conditions'].append(get_condition(weather))

        elif time_of_day == 'Tomorrow':
            tomorrow.append(weather)
            set_min_and_max_temp(tomorrow_summary, _temp)
            tomorrow_summary['total_rainfall'] += get_rainfall(weather)
            tomorrow_summary['total_snowfall'] += get_snowfall(weather)
            tomorrow_summary['conditions'].append(get_condition(weather))
        
    print('# Todays: ',len(today),'Today Summary: ',today_summary, 'Prevailing condition: ', Counter(today_summary['conditions']).most_common(1)[0][0] if len(today_summary['conditions'])>0 else 'None')
    print('# Tonights: ',len(tonight),'Tonight summary: ',tonight_summary, 'Prevailing condition: ', Counter(tonight_summary['conditions']).most_common(1)[0][0] if len(tonight_summary['conditions'])>0 else 'None')
    print('# Tomorrows: ',len(tomorrow), 'Tomorrow Summary:', tomorrow_summary, 'Prevailing condition: ', Counter(tomorrow_summary['conditions']).most_common(1)[0][0] if len(tomorrow_summary['conditions'])>0 else 'None')
            
        