from django.urls import path
from . import views

app_name = 'youtube'

urlpatterns = [
    path('extracted/', views.extracted, name='extracted'),
    path('downloading/', views.downloader, name='downloader'),
    path('download/<str:path>/', views.download_file, name='download_file'),
]
