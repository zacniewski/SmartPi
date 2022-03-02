import subprocess

from django.conf import settings as conf_settings
from django.shortcuts import render


def extracted(request):
    media_folder = conf_settings.MEDIA_ROOT
    print(f"Media root: {media_folder}")
    return render(request, 'youtube/yt-extractor.html')
