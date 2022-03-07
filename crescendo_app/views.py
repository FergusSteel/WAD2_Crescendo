from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from crescendo_app import models


def index(request):
    return render(request, 'crescendo/index.html')


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
