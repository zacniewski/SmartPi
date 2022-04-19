from django.urls import path
from . import views

app_name = 'aws'

urlpatterns = [
    path('text-detection/', views.text_detection, name='text_detection'),
]
