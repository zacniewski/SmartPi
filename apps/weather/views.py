import requests

from django.conf import settings
from django.shortcuts import render

wak = settings.WEATHER_API_KEY


def weather_in_default_location(request):
    default_location = settings.DEFAULT_LOCATION
    current_weather_api_url = f"https://api.weatherapi.com/v1/current.json"
    current_weather_api_url += f"?key={wak}&q={default_location}&aqi=no"
    forecast_weather_api_url = f"https://api.weatherapi.com/v1/forecast.json"
    forecast_weather_api_url += f"?key={wak}&q={default_location}&aqi=no"
    response_current = requests.get(current_weather_api_url)
    response_forecast = requests.get(forecast_weather_api_url)
    print(response_current.json())
    return render(request, 'weather/default-weather.html',
                  {'default_weather_data': response_current.json(),
                   'default_location': default_location,
                   'forecast_default_weather': response_forecast.json()})


def current_weather(request):
    query = request.GET.get('weather_query')
    current_weather_api_url = f"https://api.weatherapi.com/v1/current.json"
    current_weather_api_url += f"?key={wak}&q={query}&aqi=no"
    forecast_weather_api_url = f"https://api.weatherapi.com/v1/forecast.json"
    forecast_weather_api_url += f"?key={wak}&q={query}&aqi=no"
    response_current = requests.get(current_weather_api_url)
    response_forecast = requests.get(forecast_weather_api_url)
    print(response_current.json())
    return render(request, 'weather/current-weather.html',
                  {'current_weather_data': response_current.json(),
                   'forecast_current_weather': response_forecast.json(),
                   'query': query})
