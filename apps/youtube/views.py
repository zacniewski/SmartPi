import glob
import mimetypes
import os

from django.conf import settings as project_settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import SongForm
from .models import Song
from .tasks import yt_downloader


def extracted(request):
    song_list = []
    dir_path = project_settings.MEDIA_ROOT
    for full_path in glob.iglob(dir_path + '/' + '*.mp3'):
        print(f"{full_path=}")
        song_list.append([full_path, os.path.basename(full_path)])

    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            url = cd['url']
            if Song.objects.filter(url=url).exists():
                messages.warning(request, 'This file was already downloaded!')
                return redirect('youtube:extracted')
            else:
                form.save()
            yt_downloader.delay(url)  # launch asynchronous task
            return redirect('youtube:downloader')
    else:
        form = SongForm()
    return render(request, 'youtube/extracted-songs.html',
                  {'form': form,
                   'song_list': song_list})


def downloader(request):
    return render(request, 'youtube/downloading-song.html')


def download_file(request, path):
    file_path = os.path.join(project_settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            mime_type, _ = mimetypes.guess_type(file_path)
            response = HttpResponse(fh.read(), content_type=mime_type)
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                file_path
            )
            return response
        raise Http404("Nie ma takiego pliku!")
    else:
        return render(request, "youtube/404.html")
