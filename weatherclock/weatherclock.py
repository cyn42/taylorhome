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

print('Weather in',now['name'],now['weather'][0]['main'],now['main']['temp'],datetime.datetime.fromtimestamp(int(now['dt'])),'Sunrise: ',datetime.datetime.fromtimestamp(int(now['sys']['sunrise'])).strftime('%I:%M %p'),'Sunset: ',datetime.datetime.fromtimestamp(int(now['sys']['sunset'])).strftime('%I:%M %p'))

payload['cnt'] = 12
r = requests.get(cfg.owm['url']+'forecast',params=payload)
forecast = r.json()

print(forecast['cnt'])

def get_time(weather):
    return datetime.datetime.fromtimestamp(int(weather['dt']))

def get_temp(weather):
    return weather['main']['temp']

def get_condition(weather):
    return weather['weather'][0]['main']

def get_rainfall(weather):
    return weather['rain'].get('3h',0) if 'rain' in weather else '0'

for counter,weather in enumerate(forecast['list']):
    print('...',counter,get_time(weather),
        'temp:',get_temp(weather),
        'condition: ',get_condition(weather),
        'rainfall:', get_rainfall(weather)) 