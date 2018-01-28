import requests
import json
import datetime
import config as cfg

# Now: temperature, condition
# Today: min / max temperature, condition, snowfall or rainfall (if applicable). Today covers 6am - 6pm EST
#   If it is currently night, skip Today
# Tonight: Same as today, covers 6pm - 6am
# Tomorrow: 6am - 6pm, next day

payload={'id':cfg.owm['cityid'],'appid':cfg.owm['apikey'],'units': 'metric'}
r=requests.get(cfg.owm['url']+'weather',params=payload)
#now = json.loads(r.text)
now = r.json()
today = {}
tonight = {}
tomorrow = {}

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
    return weather['rain'].get('3h',0) if 'rain' in weather else '0'

def get_snowfall(weather):
    return weather['snow'].get('3h',0) if 'snow' in weather else '0'

def is_after_midnight(somedate):
    current_time = somedate.time()
    if  current_time < datetime.time(12,00):
        return True
    else:
        return False

def is_tonight(forecast_time, sunrise_time, sunset_time,after_midnight):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    # print('Passed forecast: ',forecast_time,'Today is ',today)
    # print('forecast_time.date() == today',forecast_time.date() == today)
    # print('After sunset? ',forecast_time.time() > sunset_time.time())
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

def when_is_it(now,weather):
    # Today: if forecast is today and forecast time < now sunset
    # Tonight: (It is currently before midnight and Forecast time is today after sunset or tomorrow before sunrise) or 
    #           (it is currently after midnight and forecast time is today before sunrise)
    # Tomorrow: (It is currently before sunrise and forecast time is today) or 
    #           (it is after sunrise and  Forecast time is tomorrow before sunset)
    now_datetime = get_time(now)
    sunrise = get_sunrise(now)
    sunset = get_sunset(now)
    forecast_time = get_time(weather)
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    # print('Now: ',now_datetime)
    # print('Sunset: ',sunset)
    # print('Tomorrow: ',tomorrow)
    if forecast_time.date() == today and forecast_time.time() > sunrise.time() and forecast_time.time() < sunset.time():
        return 'Today'
    # print('forecast_time.date() == today',forecast_time.date() == today)
    # print('is_after_midnight(datetime.datetime.now()',is_after_midnight(datetime.datetime.now()))
    if is_tonight(forecast_time,sunrise,sunset,is_after_midnight(datetime.datetime.now())):
       return 'Tonight'

    if (forecast_time.date() == tomorrow and forecast_time > sunrise):
        return 'Tomorrow'
    else:
        return 'Not Today or Tomorrow'
        

if __name__ == '__main__':
    print('Weather in',now['name'],now['weather'][0]['main'],now['main']['temp'],datetime.datetime.fromtimestamp(int(now['dt'])),'Sunrise: ',datetime.datetime.fromtimestamp(int(now['sys']['sunrise'])).strftime('%I:%M %p'),'Sunset: ',datetime.datetime.fromtimestamp(int(now['sys']['sunset'])).strftime('%I:%M %p'))

    payload['cnt'] = 12
    r = requests.get(cfg.owm['url']+'forecast',params=payload)
    forecast = r.json()

    for counter,weather in enumerate(forecast['list']):
        print('...',counter,get_time(weather),
            'temp:',get_temp(weather),
            'condition: ',get_condition(weather),
            'rainfall:', get_rainfall(weather),
            'snowfall:', get_snowfall(weather),
            when_is_it(now,weather)) 