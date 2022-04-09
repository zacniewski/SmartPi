from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import SongForm
from .models import Song
from .tasks import yt_downloader


def extracted(request):
    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            url = cd['url']
            # title = cd['title']
            if Song.objects.filter(url=url).exists():
                messages.warning(request, 'This file was already downloaded!')
                return redirect('youtube:extracted')
            else:
                # new_song = form.save(commit=False)
                # new_song.title = title
                form.save()
            yt_downloader.delay(url)  # launch asynchronous task
            return redirect('youtube:downloader')
    else:
        form = SongForm()
    return render(request, 'youtube/extracted-songs.html',
                  {'form': form})


def downloader(request):
    return render(request, 'youtube/downloading-song.html')
