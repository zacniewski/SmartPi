# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),                # Django admin route
    path('weather/', include('apps.weather.urls', namespace='weather')),
    path('weather/', include('apps.youtube.urls', namespace='youtube')),
    path('', include('apps.authentication.urls')),  # Auth routes - login / register
    path('', include('apps.home.urls')),             # UI Kits Html files
]
