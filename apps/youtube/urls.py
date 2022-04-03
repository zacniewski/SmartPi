from django.urls import path
from . import views

app_name = 'youtube'

urlpatterns = [
    path('extracted/', views.extracted, name='extracted'),
    path('test/<str:url>', views.test, name='test'),
]
