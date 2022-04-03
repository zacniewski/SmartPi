from django.shortcuts import render, redirect

from .tasks import yt_downloader


def extracted(request):
    return render(request, 'youtube/yt-extractor.html')


def test(request, url):
    # launch asynchronous task
    yt_downloader.delay(url)
    return redirect('youtube:extracted')
