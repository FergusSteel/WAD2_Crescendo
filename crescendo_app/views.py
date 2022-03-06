from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from crescendo_app import models


def index(request):
    return render(request, 'crescendo/index.html')



def playlist(request):
    pass


def song(request):
    pass


def userProfile(request):
    pass
