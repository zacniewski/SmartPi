from django.urls import path
from . import views

app_name = 'youtube'

urlpatterns = [
    path('extracted/', views.extracted, name='extracted'),
    path('downloading/', views.downloader, name='downloader'),
]
