from itertools import chain

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from crescendo_app import models
from crescendo_app.models import Playlist, Song, SongComment
from crescendo_app.form import PlaylistForm
from django.shortcuts import redirect


def index(request):
    context_dict = {}
    context_dict['playlists'] = Playlist.objects.all()
    context_dict['songs'] = Song.objects.all()
    return render(request, 'crescendo/index.html', context=context_dict)


def about(request):
    context_dict = {}
    return render(request, 'crescendo/about.html', context=context_dict)


def faq(request):
    context_dict = {}
    return render(request, 'crescendo/faq.html', context=context_dict)


def contactUs(request):
    context_dict = {}
    return render(request, 'crescendo/contactUs.html', context=context_dict)


def show_playlist(request, playlist_slug, playlist_id):
    context_dict = {}

    try:
        playlist = Playlist.objects.get(nameAsSlug=playlist_slug, id=playlist_id)
        try:
            songs = []
            for song in Song.objects.all():
                if playlist in song.playlist.all():
                    songs.append(song)
            context_dict['songs'] = songs
        except Song.DoesNotExist:
            context_dict['songs'] = None

        context_dict['crescendo_app'] = playlist

    except Playlist.DoesNotExist:
        context_dict['crescendo_app'] = None

    return render(request, 'crescendo/playlist.html', context=context_dict)


def show_song(request, song_slug, song_id):
    context_dict = {}

    try:
        song = Song.objects.get(nameAsSlug=song_slug, id=song_id)
        try:
            comments = []
            for comment in SongComment.objects.all():
                if comment.song == song:
                    comments.append(comment)
            context_dict['comments'] = comments
        except:
            context_dict['comments'] = None

        context_dict['song'] = song

    except Song.DoesNotExist:
        context_dict['song'] = None

    return render(request, 'crescendo/song.html', context=context_dict)


def userProfile(request):
    pass


def search(request,  *args, **kwargs):
    print(args, kwargs)
    """
       :param kwargs :  {'playlist_name': '0'', 'song_name': '0'}
    """
    q = request.GET.get('q')
    search = {}
    for k, v in kwargs.item():
        temp = int(v)
        kwargs[k] = temp
        if temp:
            search[k] = temp
    playlist_list = Playlist.objects.filter(name__icontains=q)
    song_list = Song.objects.filter(name__icontains=q)
    return render(request, 'crescendo/search.html', {'kwargs':kwargs,'playlist_list':playlist_list, 'song_list':song_list})


# Playlists and Songs
def PlaylistCatalogue(request):
    context_dict = {}
    context_dict['playlists'] = Playlist.objects.order_by()
    return render(request, 'crescendo/PlaylistCatalogue.html', context=context_dict)


def SongCatalogue(request):
    context_dict = {}
    context_dict['songs'] = Song.objects.order_by()
    return render(request, 'crescendo/SongCatalogue.html', context=context_dict)


# Add crescendo_app

def add_playlist(request):
    form = PlaylistForm()

    if request.method == 'POST':
        form = PlaylistForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return redirect('/crescendo/')
        else:

            print(form.errors)

    return render(request, 'crescendo/add_playlist.html', {'form': form})
