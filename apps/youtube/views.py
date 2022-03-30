import subprocess
import youtube_dl

from django.conf import settings as conf_settings
from django.shortcuts import render

media_folder = conf_settings.MEDIA_ROOT


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
    elif d['status'] == 'downloading':
        print(f"Elapsed: {d['elapsed']}")
        print(f"ETA: {d['eta']}")


def extracted(request):
    print(f"Media root: {media_folder}")
    return render(request, 'youtube/yt-extractor.html')


def test(request):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'outtmpl': media_folder + '/%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=V1bFr2SWP1I'])
    return render(request, 'youtube/yt-extractor.html')
