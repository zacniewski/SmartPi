from django.urls import path
from . import views

app_name = 'gcp'

urlpatterns = [
    path('text-to-speech/', views.text_to_speech, name='text_to_speech'),
]
