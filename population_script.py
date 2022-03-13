import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crescendo.settings')

import django

django.setup()

from crescendo_app.models import User, UserProfile, Genre, Song, SongComment, Playlist, PlaylistComment
from django.db import models


def populate():
    # ensuring all necessary folders are within project directory
    necessary_folders = ['media', 'media/playlist_images', 'media/profile_images', 'media/song_images']

    for folder in necessary_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    users = [
        {"name": "Greg",
         "image": "population_script_images/greg.png"},
        {"name": "Sarah",
         "image": "population_script_images/sarah.png"},
        {"name": "Craig",
         "image": "population_script_images/craig.png"}
    ]

    genres = [
        "Upbeat",
        "Mellow",
        "Rock",
        "Punk",
        "Indie",
        "Alternative Rock",
        "Pop",
        "Rap",
        "Emo",
    ]

    playlists = [
        {"author": "Greg",
         "name": "Playlist 1",
         "views": 20,
         "numberOfComments": 3,
         "description": "Just an upbeat crescendo_app",
         "genres": ["Upbeat", "Mellow"],
         "image": None,
         "comments": [{"comment": "Great collection of songs",
                       "rating": 4,
                       "author": "Sarah"},
                      {"comment": "Could be better",
                       "rating": 3,
                       "author": "Greg"
                       },
                      {"comment": "Very upbeat and nice to listen to",
                       "rating": 4,
                       "author": "Craig"}
                      ]
         },
        {"author": "Greg",
         "name": "Playlist 2",
         "views": 120,
         "numberOfComments": 3,
         "description": "Just a mellow crescendo_app",
         "genres": ["Upbeat"],
         "image": None,
         "comments": [
             {"comment": "Plain collection of songs",
              "rating": 2,
              "author": "Sarah"},
             {"comment": "Could be better, better luck next time",
              "rating": 3,
              "author": "Greg"
              },
             {"comment": ".....",
              "rating": 4,
              "author": "Craig"}
         ]
         },
        {"author": "Sarah",
         "name": "Playlist 3",
         "views": 1,
         "numberOfComments": 1,
         "description": "Just a random crescendo_app",
         "genres": ["Upbeat", "Mellow", "Rock"],
         "image": None,
         "comments": [
             {"comment": "Great collection of songs",
              "rating": 4,
              "author": "Sarah"},
         ]
         },
        {"author": "Craig",
         "name": "Playlist 1",
         "views": 500,
         "numberOfComments": 2,
         "description": "The best",
         "image": "default.png",
         "genres": ["Mellow", "Pop"],
         "comments": [
             {"comment": "All time favourite",
              "rating": 4,
              "author": "Sarah"},
             {"comment": "Very upbeat and nice to listen to",
              "rating": 4,
              "author": "Greg"}
         ]
         },
        {"author": "Sarah",
         "name": "Playlist 5",
         "views": 1000,
         "numberOfComments": 2,
         "description": "Just a crescendo_app",
         "genres": ["Rap"],
         "image": None,
         "comments": [
             {"comment": "Great collection of songs",
              "rating": 4,
              "author": "Sarah"},
             {"comment": "Could be better",
              "rating": 3,
              "author": "Greg",
              }
         ]
         }

    ]

    songs = [
        {
            "author": "Sarah",
            "genres": ["Indie"],
            "name": "Fields of Gold",
            "artist": "String",
            "numberOfComments": 1,
            "image": None,
            "lyrics": None,
            "playlists": ["Playlist 1", "Playlist 2"],
            "actualSong": "population_script_music/sound1.mp3",
            "comments": [{"author": "Greg",
                          "rating": 5,
                          "comment": "Great"}]
        },
        {
            "author": "Greg",
            "genres": ["Indie", "Rap", "Mellow"],
            "name": "Gold",
            "artist": "Anonymous Artist",
            "numberOfComments": 1,
            "image": None,
            "playlists": ["Playlist 1", "Playlist 3"],
            "lyrics": None,
            "actualSong": "population_script_music/sound2.mp3",
            "comments": [{"author": "Sarah",
                          "rating": 2,
                          "comment": "mid"}]
        },
        {
            "author": "Craig",
            "genres": ["Upbeat", "Rock"],
            "name": "SIU",
            "artist": "Anonymous Artist",
            "numberOfComments": 3,
            "image": None,
            "lyrics": None,
            "playlists": [],
            "actualSong": "population_script_music/sound3.mp3",
            "comments": [{"author": "Sarah",
                          "rating": 2,
                          "comment": "mid", },
                         {"author": "Greg",
                          "rating": 5,
                          "comment": "Great"},
                         {"author": "Craig",
                          "rating": 5,
                          "comment": "My favourite"}]
        }
    ]

    usersForLaterUsage = {}
    for userDict in users:
        userObject, userProfileObject = add_user(userDict['name'], userDict['image'])
        usersForLaterUsage[userDict['name']] = (userObject, userProfileObject)

    genresForLaterUsage = {}
    for genre in genres:
        genreObject = add_genre(genre)
        genresForLaterUsage[genre] = genreObject

    playlistsForLaterUsage = {}
    for playlist in playlists:
        comments = playlist['comments']
        genre = [genresForLaterUsage[genre] for genre in playlist['genres']]
        playlistObject = add_playlist(playlist['name'], genre, usersForLaterUsage[playlist['author']][1],
                                      playlist['views'], playlist['numberOfComments'], playlist['description'],
                                      playlist['image'])
        playlistsForLaterUsage[playlist['name']] = playlistObject
        for comment in comments:
            commentObject = add_playlist_comment(playlistObject, usersForLaterUsage[comment['author']][1],
                                                 comment["comment"], comment["rating"])

    for song in songs:
        comments = song['comments']
        genre = [genresForLaterUsage[genre] for genre in song['genres']]
        playlist = [playlistsForLaterUsage[playlist] for playlist in song['playlists']]
        songObject = add_song(song["name"], genre, usersForLaterUsage[song['author']][1], song['artist'],
                              song['numberOfComments'], song["actualSong"], playlist)
        for comment in comments:
            commentObject = add_song_comment(songObject, usersForLaterUsage[comment['author']][1], comment["comment"],
                                             comment["rating"])


def add_user(name, image):
    userObject, _ = User.objects.get_or_create(username=name)
    userObject.save()
    userObject, _ = UserProfile.objects.get_or_create(user=userObject, image=image)
    userObject.save()

    return User.objects.get(username=name), userObject


def add_genre(name):
    genreObject, _ = Genre.objects.get_or_create(name=name)
    genreObject.save()

    return genreObject


def add_playlist(name, genreList, author, views, numberOfComments, description, image=None):
    playlistObject, _ = Playlist.objects.get_or_create(name=name, author=author, views=views,
                                                       numberOfComments=numberOfComments, description=description)
    playlistObject.genre.add(*genreList)
    playlistObject.save()

    return playlistObject


def add_playlist_comment(playlist, author, comment, rating):
    commentObject, _ = PlaylistComment.objects.get_or_create(playlist=playlist, author=author, comment=comment,
                                                             rating=rating)
    commentObject.save()
    return commentObject


def add_song_comment(song, author, comment, rating):
    commentObject, _ = SongComment.objects.get_or_create(song=song, author=author, comment=comment, rating=rating)
    commentObject.save()
    return commentObject


def add_song(name, genreList, author, artist, numberOfComments, song, playlists, lyrics=None, image=None):
    songObject, _ = Song.objects.get_or_create(name=name, author=author, artist=artist,
                                               numberOfComments=numberOfComments, actualSong=song)
    songObject.genre.add(*genreList)
    songObject.playlist.add(*playlists)
    songObject.save()

    return songObject


if __name__ == "__main__":
    populate()
