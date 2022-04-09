from celery import shared_task
from django.conf import settings as conf_settings
import youtube_dl

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


@shared_task
def yt_downloader(url):
    id_of_song = url.split("?")[1]
    link_to_audio = 'https://www.youtube.com/watch?' + id_of_song
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link_to_audio])
    return ydl.progress_hooks
