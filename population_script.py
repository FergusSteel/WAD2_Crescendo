import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crescendo.settings')

import django

django.setup()

from crescendo_app.models import User, UserProfile, Genre, Song, Playlist, Question, Comment
from django.db import models


def populate():
    # ensuring all necessary folders are within project directory
    necessary_folders = ['media', 'media/playlist_images', 'media/profile_images', 'media/song_images']

    for folder in necessary_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    questions = [
        {"question": "What is this website for?",
         "answer": "Crescendo is a website used for music and playlist uploading and sharing. It is aimed mainly at independent artists looking to put their music out there."},
        {"question": "How to make an account?",
         "answer": "Simply head over to crescedo/register to access our registration page, where you can make an account by providing a bunch of information."},
        {"question": "Can I publish music that I have not made?",
         "answer": "Only if you have the legal ownership of the product."}
    ]
    users = [
        {"name": "Greg",
         "image": "population_script_images/greg.png"},
        {"name": "Sarah",
         "image": "population_script_images/sarah.png"},
        {"name": "Craig",
         "image": "population_script_images/craig.png"},
        {"name": "Michal",
         "image": None},
        {"name": "Angelo",
         "image": None},
        {"name": "Fergus",
         "image": None},
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
        "Hip-Hop",
        "Trap",
        "Punk Rock",
        "Dance",
        "Dub-Step",
        "Electronic",
        "K-Pop"
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
                       "author": "Sarah"},
                      {"comment": "Could be better",
                       "rating": 3,
                       "author": "Greg"
                       },
                      {"comment": "Very upbeat and nice to listen to",
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
              "author": "Sarah"},
             {"comment": "Could be better, better luck next time",
              "author": "Greg"
              },
             {"comment": ".....",
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
              "author": "Sarah"},
         ]
         },
        {"author": "Craig",
         "name": "Playlist 4",
         "views": 500,
         "numberOfComments": 2,
         "description": "The best",
         "image": None,
         "genres": ["Mellow", "Pop"],
         "comments": [
             {"comment": "All time favourite",
              "author": "Sarah"},
             {"comment": "Very upbeat and nice to listen to",
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
              "author": "Sarah"},
             {"comment": "Could be better",
              "author": "Greg",
              }
         ]
         },
        {"author": "Angelo",
         "name": "Best of 2020",
         "views": 0,
         "numberOfComments": 0,
         "description": "Biggest Hits from 2020 - the quarantine year",
         "genres": ["Rap", "Pop", "Electronic", "Dance", "Punk Rock"],
         "image": None,
         "comments": [
         ]
         },
        {"author": "Michal",
         "name": "Movie Soundtracks",
         "views": 500,
         "numberOfComments": 1,
         "description": "Some of the best music pieces",
         "image": "population_script_images/unnamed.jpg",
         "genres": ["Mellow"],
         "comments": [
             {"comment": "Heat",
              "author": "Angelo"},
         ]
         },
        {"author": "Fergus",
         "name": "Personal Favourites",
         "views": 10,
         "numberOfComments": 1,
         "description": "Some of my favourite music pieces, all genres included",
         "image": None,
         "genres": ["Upbeat",
                    "Mellow",
                    "Rock",
                    "Punk",
                    "Indie",
                    "Alternative Rock",
                    "Pop",
                    "Rap",
                    "Emo",
                    "Hip-Hop",
                    "Trap",
                    "Punk Rock",
                    "Dance",
                    "Dub-Step",
                    "Electronic",
                    "K-Pop"],
         "comments": [
             {"comment": "Some of my favourites are here",
              "author": "Angelo"},
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
            "comments": [{"comment": "Beautiful Song", "author": "Craig"}]
        },
        {
            "author": "Greg",
            "genres": ["Indie", "Rap", "Mellow"],
            "name": "Gold",
            "artist": "Anonymous Artist",
            "numberOfComments": 2,
            "image": "population_script_images/1.jpg",
            "playlists": ["Playlist 1", "Playlist 3"],
            "lyrics": None,
            "actualSong": "population_script_music/sound2.mp3",
            "comments": [{"author": "Sarah",
                          "comment": "Great"}, {"author": "Fergus",
                                                "comment": "mid"}]
        },
        {
            "author": "Craig",
            "genres": ["Upbeat", "Rock"],
            "name": "SIU",
            "artist": "Anonymous Artist",
            "numberOfComments": 3,
            "image": "population_script_images/3.jpg",
            "lyrics": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus congue sem quam, vel porttitor ligula vulputate ut. Morbi elementum dolor tellus, et porta enim ultricies dapibus. Cras in nunc ullamcorper, rutrum eros et, porta elit. Curabitur porttitor, mi ut hendrerit placerat, dolor purus aliquam mi, quis semper ligula ligula vel dolor. Sed suscipit nulla ut ante ultricies rutrum. Aenean tristique efficitur felis, sit amet bibendum felis facilisis quis. Aliquam sit amet elit ligula. Donec dapibus sem vel dui finibus convallis. Vestibulum efficitur lobortis dapibus. Fusce rhoncus, diam sed gravida varius, odio tortor ornare turpis, et aliquam nisi felis in dolor. Phasellus gravida efficitur lectus in efficitur. Suspendisse maximus dui sapien, nec tristique diam facilisis non. Fusce metus turpis, molestie dictum est sit amet, imperdiet molestie quam. In eu eros et tellus hendrerit eleifend. ",
            "playlists": [],
            "actualSong": "population_script_music/sound3.mp3",
            "comments": [{"author": "Fergus",
                          "comment": "mid", },
                         {"author": "Craig",
                          "comment": "Great"},
                         {"author": "Michal",
                          "comment": "My favourite"}]
        },
        {
            "author": "Michal",
            "genres": ["Rap", "Rock"],
            "name": "Tuesday",
            "artist": "Michal",
            "numberOfComments": 0,
            "image": "population_script_images/4.jpg",
            "lyrics": None,
            "playlists": [],
            "actualSong": "population_script_music/sound3.mp3",
            "comments": []
        },
        {
            "author": "Fergus",
            "genres": ["Punk Rock"],
            "name": "Song",
            "artist": "Fergus",
            "numberOfComments": 0,
            "image": None,
            "lyrics": None,
            "playlists": [],
            "actualSong": "population_script_music/sound3.mp3",
            "comments": []
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
                                      image=playlist['image'])
        playlistsForLaterUsage[playlist['name']] = playlistObject

        for comment in comments:
            add_comment(usersForLaterUsage[comment['author']][0], comment['comment'], playlistObject)

    for song in songs:
        comments = song['comments']
        genre = [genresForLaterUsage[genre] for genre in song['genres']]
        playlist = [playlistsForLaterUsage[playlist] for playlist in song['playlists']]
        songObject = add_song(song["name"], genre, usersForLaterUsage[song['author']][1], song['artist'],
                              song['numberOfComments'], song["actualSong"], playlist, lyrics=song["lyrics"],
                              image=song['image'])

        for comment in comments:
            add_comment(usersForLaterUsage[comment['author']][0], comment['comment'], songObject)

    for question in questions:
        questionObject = add_question(question['question'], question['answer'])


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

    if image:
        playlistObject.image = image

    playlistObject.genre.add(*genreList)
    playlistObject.save()

    return playlistObject


def add_song(name, genreList, author, artist, numberOfComments, song, playlists, lyrics=None, image=None):
    songObject, _ = Song.objects.get_or_create(name=name, author=author, artist=artist,
                                               numberOfComments=numberOfComments, actualSong=song)

    if lyrics:
        songObject.lyrics = lyrics

    if image:
        songObject.image = image

    songObject.genre.add(*genreList)
    songObject.playlist.add(*playlists)
    songObject.save()

    return songObject


def add_question(question, answer):
    questionObject, _ = Question.objects.get_or_create(question=question, answer=answer)
    questionObject.save()
    return questionObject


def add_comment(author, text, content_object):
    comment = Comment()
    comment.author = author
    comment.text = text
    comment.content_object = content_object
    comment.save()
    return comment


if __name__ == "__main__":
    populate()
