from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('default-location/', views.weather_in_default_location, name='default_weather'),
    path('<str:query>/', views.current_weather, name='current_weather'),
]
