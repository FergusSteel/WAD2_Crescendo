from itertools import chain

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from crescendo_app import models
from crescendo_app.models import Playlist, Song


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


def playlist(request):
    pass


def song(request):
    pass


def userProfile(request):
    pass


def search(request):
    results_playlist = []
    results_song = []
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "Please entry the other key words!"
        return render(request, 'crescendo/result.html', {'error_msg': error_msg})

    results_playlist = results_playlist + list(Playlist.objects.filter(title__icontains=q))
    results_song = results_song + list(Playlist.objects.filter(title__icontains=q))
    results = chain(results_playlist, results_song)
    return render(request, 'crescendo/result.html', {'error_msg': error_msg, 'results': results})

# Playlists and Songs
def PlaylistCatalogue(request):
    context_dict = {}
    context_dict['playlists'] = Playlist.objects.order_by()
    return render(request, 'crescendo/PlaylistCatalogue.html', context=context_dict)

def SongCatalogue(request):
    context_dict = {}
    context_dict['songs'] = Song.objects.order_by()
    return render(request, 'crescendo/SongCatalogue.html', context=context_dict)
