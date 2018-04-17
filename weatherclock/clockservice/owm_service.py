import requests, json, datetime, time
import config as cfg
import currentconditions as cc
import forecast as fc

def get_current_conditions():
    weatherresponse = get_owm_current_conditions()
    print("Received from OWM: ",weatherresponse)
    condition_code = weatherresponse['weather'][0]['icon']
    temperature = weatherresponse['main']['temp']
    dt = datetime.datetime.fromtimestamp(int(weatherresponse['dt']))
    sunrise = datetime.datetime.fromtimestamp(int(weatherresponse['sys']['sunrise']))
    sunset  = datetime.datetime.fromtimestamp(int(weatherresponse['sys']['sunset']))
    currentconditions = cc.CurrentConditions(condition_code, temperature, dt, sunrise, sunset)
    return currentconditions

def get_owm_current_conditions():
    payload = {'id':cfg.owm['cityid'], 'appid':cfg.owm['apikey'], 'units': 'metric'}
    api_response = requests.get(cfg.owm['url']+'weather', params=payload)
    return api_response.json()

def get_forecast_conditions():
    forecastresponse = get_owm_forecast_conditions()
    forecasts = []
    for forecast in forecastresponse['list']:
        condition_code = forecast['weather'][0]['icon']
        dt = datetime.datetime.fromtimestamp(int(forecast['dt']))
        temperature = forecast['main']['temp']
        min_temp = temperature = forecast['main']['temp_min']
        max_temp = temperature = forecast['main']['temp_max']
        rainfall = float(forecast['rain'].get('3h', 0)) if 'rain' in forecast else 0
        snowfall = float(forecast['snow'].get('3h', 0)) if 'snow' in forecast else 0
        iter_forecast = fc.Forecast(condition_code, temperature, min_temp, max_temp, dt, rainfall, snowfall)
        forecasts.append(iter_forecast)
    return forecasts

def get_owm_forecast_conditions():
    payload = {'id':cfg.owm['cityid'], 'appid':cfg.owm['apikey'], 'units': 'metric', 'cnt': 12}
    api_response = requests.get(cfg.owm['url']+'forecast', params=payload)
    return api_response.json()

if __name__ == '__main__':
    
    #grab_weather()
    current = get_current_conditions()
    print(current)
    forecasts = get_forecast_conditions()
    print('First forecast: ',forecasts[0])