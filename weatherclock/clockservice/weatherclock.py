import requests, json, datetime, time
import config as cfg
from forecastsummary import ForecastSummary

current_conditions = {}
today_summary, tonight_summary, tomorrow_summary = ForecastSummary(), ForecastSummary(), ForecastSummary()

# Now: temperature, condition
# Today: min / max temperature, condition, snowfall or rainfall (if applicable). Today covers sunrise to sunset
#   If it is currently night, skip Today
# Tonight: Same as today, covers sunset to sunrise
# Tomorrow: sunrise to sunset, next day

def get_time(forecast_weather):
    return datetime.datetime.fromtimestamp(int(forecast_weather['dt']))

def get_sunrise(current_weather):
    return datetime.datetime.fromtimestamp(int(current_weather['sys']['sunrise']))
def get_sunset(current_weather):
    return datetime.datetime.fromtimestamp(int(current_weather['sys']['sunset']))

def get_temp(forecast_weather):
    return forecast_weather['main']['temp']

def get_condition(forecast_weather):
    return forecast_weather['weather'][0]['main']

def get_rainfall(forecast_weather):
    return float(forecast_weather['rain'].get('3h', 0)) if 'rain' in forecast_weather else 0

def get_snowfall(forecast_weather):
    return float(forecast_weather['snow'].get('3h', 0)) if 'snow' in forecast_weather else 0

def is_after_midnight(somedate):
    current_time = somedate.time()
    if  current_time < datetime.time(6,00):
        return True
    else:
        return False

def is_tonight(forecast_time, sunrise_time, sunset_time,after_midnight):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
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

def when_is_it(current_weather, forecast_weather):
    # Today: if forecast is today and forecast time < now sunset
    # Tonight: (It is currently before midnight and Forecast time is today after sunset or tomorrow before sunrise) or
    #           (it is currently after midnight and forecast time is today before sunrise)
    # Tomorrow: (It is currently before sunrise and forecast time is today) or 
    #           (it is after sunrise and  Forecast time is tomorrow before sunset)
    sunrise = get_sunrise(current_weather)
    sunset = get_sunset(current_weather)
    forecast_time = get_time(forecast_weather)
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    if (forecast_time.date() == today and
            forecast_time.time() > sunrise.time() and forecast_time.time() < sunset.time()):
        return 'Today'
    if is_tonight(forecast_time, sunrise, sunset, is_after_midnight(datetime.datetime.now())):
        return 'Tonight'
    if (forecast_time.date() == tomorrow and forecast_time.time() > sunrise.time() and
            forecast_time.time() < sunset.time()):
        return 'Tomorrow'
    else:
        return 'Not Today, Tonight or Tomorrow'

def get_current_conditions():
    payload = {'id':cfg.owm['cityid'], 'appid':cfg.owm['apikey'], 'units': 'metric'}
    api_response = requests.get(cfg.owm['url']+'weather', params=payload)
    return api_response.json()

def get_forecast_conditions():
    payload = {'id':cfg.owm['cityid'], 'appid':cfg.owm['apikey'], 'units': 'metric', 'cnt': 12}
    api_response = requests.get(cfg.owm['url']+'forecast', params=payload)
    return api_response.json()

def bucket_forecast(forecast, now):
    for weather in forecast['list']:
        time_of_day = when_is_it(now, weather)
        _temp = get_temp(weather)

        if time_of_day == 'Today':
            current_summary = today_summary

        elif time_of_day == 'Tonight':
            current_summary = tonight_summary

        elif time_of_day == 'Tomorrow':
            current_summary = tomorrow_summary

        current_summary.eval_new_temp(_temp)
        current_summary.add_precipitation(get_rainfall(weather), get_snowfall(weather))
        current_summary.add_condition(get_condition(weather))

def grab_weather():
    global current_conditions
    current_conditions = get_current_conditions()
    # print('Weather in',now['name'],now['weather'][0]['main'],now['main']['temp'],datetime.datetime.fromtimestamp(int(now['dt'])),'Sunrise: ',datetime.datetime.fromtimestamp(int(now['sys']['sunrise'])).strftime('%I:%M %p'),'Sunset: ',datetime.datetime.fromtimestamp(int(now['sys']['sunset'])).strftime('%I:%M %p'))
    forecast = get_forecast_conditions()
    bucket_forecast(forecast, current_conditions)       

def get_weather_transitions():
    grab_weather()
    results = {'now': current_conditions, 
               'forecast': [today_summary.__dict__, tonight_summary.__dict__, tomorrow_summary.__dict__]}
    return json.dumps(results)

if __name__ == '__main__':
    
    #grab_weather()
    print(get_weather_transitions())
        