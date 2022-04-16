from django.urls import path
from . import views

app_name = 'gcp'

urlpatterns = [
    path('text-to-speech/', views.text_to_speech, name='text_to_speech'),
    path("speech-to-text/<str:local_file_name>/", views.speech_to_text, name="speech_to_text"),
    path("voice-files/", views.voice_files, name="voice_files"),
    path("examine-voice-file/<str:name>", views.output_file, name="output_file"),
]
