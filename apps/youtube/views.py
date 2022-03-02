import subprocess

from django.shortcuts import render


def extracted(request):
    return render(request, 'youtube/yt-extractor.html')
