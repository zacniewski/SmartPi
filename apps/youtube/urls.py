from django.urls import path
from . import views

app_name = 'youtube'

urlpatterns = [
    path('extracted/', views.extracted, name='extracted'),
    # path('current-weather/', views.current_weather, name='current_weather'),
]
