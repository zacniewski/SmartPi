import requests

from django.conf import settings
from django.shortcuts import render

wak = settings.WEATHER_API_KEY


def weather_in_default_location(request):
    default_location = settings.DEFAULT_LOCATION
    current_weather_api_url = "https://api.weatherapi.com/v1/current.json"
    current_weather_api_url += "?key=" + wak + "&q=" + default_location + "&aqi=no"
    response = requests.get(current_weather_api_url)
    print(response.json())
    return render(request, 'weather/weather.html', {'current_weather_data': response.json(),
                                                    'default_location': default_location})


def current_weather(request):
    query = request.GET.get('weather_query')