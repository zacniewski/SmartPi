# -*- encoding: utf-8 -*-
from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
