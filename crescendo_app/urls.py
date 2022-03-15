"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from crescendo_app import views

app_name = 'crescendo'

urlpatterns = [
                  # Add URL Paths, Uncomment as Views and Templates are implemented. (Make sure name parameter
                  # matches view's name)

                  # Home Page
                  path('', views.index, name='index'),
                  path('about/', views.about, name='about'),
                  path('contactUs/', views.contactUs, name='contactUs'),
                  path('faq', views.faq, name='faq'),
                  path('userprofile', views.userProfile, name='userprofile'),
                  path('crescendo_app/<slug:playlist_slug>-<slug:playlist_id>/', views.show_playlist,
                       name='show_playlist'),
                  path('PlaylistCatalogue/', views.PlaylistCatalogue, name='PlaylistCatalogue'),
                  path('SongCatalogue/', views.SongCatalogue, name='SongCatalogue'),
                  path('song/<slug:song_slug>-<slug:song_id>/', views.show_song, name='show_song'),
                  path('add_playlist/', views.add_playlist, name='add_playlist'),
                  path('search/', views.search, name='search'),
                  path('add_playlist/<slug:playlist_slug>-<slug:playlist_id>/',views.add_playlist,name='add_playlist'), 
                  path('playlist/edit_playlist/<int:pk>/', views.edit_playlist, name='edit_playlist')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
