 
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','crescendo.settings') 
 
import django 
django.setup()  

from crescendo_app.models import User,UserProfile,Genre,Song,SongComment,Playlist,PlaylistComment 
from django.db import models
# actual function to populate 
   
def populate():   
     
    if not os.path.exists('static'):
        os.makedirs('static')
        os.makedirs('static/playlist_images') 
        os.makedirs('static/profile_images') 
        os.makedires('static/song_images')
     
    users = [ 
        {"name" : "James"},
        {"name" : "Michal"},
        {"name" : "Henry"}
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
    ] 
     
    playlists = [
        {"author":"James", 
        "name" : "Playlist 1", 
        "views" : 20, 
        "numberOfComments" : 3, 
        "description" : "Just an upbeat playlist", 
        "genres": ["Upbeat","Mellow"], 
        "image":None, 
        "comments" : [{"comment" : "Great collection of songs", 
                "rating" : 4, 
                "author" : "Henry"} , 
                {"comment" : "Could be better", 
                "rating":3, 
                "author":"James" 
                }, 
                {"comment":"Very upbeat and nice to listen to", 
                "rating":4, 
                "author":"Michal"} 
                ]
        },  
        {"author":"James", 
        "name" : "Playlist 2", 
        "views" : 120, 
        "numberOfComments" : 3,  
        "description" : "Just a mellow playlist", 
        "genres": ["Upbeat"], 
        "image":None, 
        "comments":[
                {"comment" : "Plain collection of songs", 
                "rating" : 2, 
                "author" : "Henry"} , 
                {"comment" : "Could be better, better luck next time", 
                "rating":3, 
                "author" : "James" 
                }, 
                {"comment":".....", 
                "rating":4, 
                "author" : "Michal"}
                ] 
        }, 
        {"author":"Henry", 
        "name" : "Playlist 3", 
        "views" : 1, 
        "numberOfComments" : 1, 
        "description" : "Just a random playlist",   
        "genres": ["Upbeat","Mellow","Rock"], 
        "image":None, 
        "comments": [
                {"comment" : "Great collection of songs", 
                "rating" : 4, 
                "author" : "Henry"} , 
                ] 
        },  
        {"author":"Michal", 
        "name" : "Playlist 1", 
        "views" : 500, 
        "numberOfComments" : 2, 
        "description" : "The best", 
        "image" : "default.png",  
        "genres": ["Mellow","Pop"], 
        "comments": [
                {"comment" : "All time favourite", 
                "rating" : 4, 
                "author" : "Henry"} ,  
                {"comment":"Very upbeat and nice to listen to", 
                "rating":4, 
                "author" : "James"}
                ] 
        }, 
        {"author":"Henry", 
        "name" : "Playlist 5", 
        "views" : 1000, 
        "numberOfComments" : 2, 
        "description" : "Just a playlist", 
        "genres": ["Rap"], 
        "image":None,  
        "comments" : [
                {"comment" : "Great collection of songs", 
                "rating" : 4, 
                "author" : "Henry"} , 
                {"comment" : "Could be better", 
                "rating":3, 
                "author" : "James", 
                }
                ]
        } 

    ] 
     
    songs = [ 
        {
            "author":"Henry", 
            "genres":["Indie"], 
            "name" : "Fields of Gold", 
            "artist" : "String", 
            "numberOfComments" : 1, 
            "image" : None, 
            "lyrics" : None, 
            "actualSong" : "population_script_music/sound1.mp3", 
            "comments" : [{"author" : "James", 
                            "rating":5, 
                            "comment" : "Great" } ]
        }, 
        {
            "author":"James", 
            "genres":["Indie","Rap","Mellow"], 
            "name" : "Gold", 
            "artist" : "Anonymous Artist", 
            "numberOfComments" : 1, 
            "image" : None, 
            "lyrics" : None, 
            "actualSong" : "population_script_music/sound2.mp3" ,
            "comments" : [{"author" : "Henry", 
                            "rating":2, 
                            "comment" : "mid"}]
        }, 
        {
            "author":"Michal", 
            "genres":["Upbeat","Rock"], 
            "name" : "SIU", 
            "artist" : "Anonymous Artist", 
            "numberOfComments" : 3, 
            "image" : None, 
            "lyrics" : None, 
            "actualSong" : "population_script_music/sound3.mp3" ,
            "comments" : [{"author" : "Henry", 
                            "rating":2, 
                            "comment" : "mid",},
                            {"author" : "James", 
                            "rating":5, 
                            "comment" : "Great" },  
                            {"author" : "Michal", 
                            "rating":5, 
                            "comment" : "My favourite"}]
        }
    ]
            
      
    usersForLaterUsage = {}
    for userDict in users:   
        userProfileObject, userObject = add_user(userDict['name']) 
        usersForLaterUsage[userDict['name']] =  userObject  
         
    genresForLaterUsage = {}  
    for genre in genres: 
        genreObject = add_genre(genre) 
        genresForLaterUsage[genre] = genreObject 
         
    for playlist in playlists:   
        comments = playlist['comments']
        genre = [genresForLaterUsage[genre] for genre in playlist['genres']]
        playlistObject = add_playlist(playlist['name'] , genre,usersForLaterUsage[playlist['author']], playlist['views'],playlist['numberOfComments'],playlist['description'],playlist['image'])  
        for comment in comments: 
            commentObject = add_playlist_comment(playlistObject,usersForLaterUsage[comment['author']],comment["comment"],comment["rating"])
         
    for song in songs: 
        comments = song['comments']  
        genre = [genresForLaterUsage[genre] for genre in playlist['genres']]
        songObject = add_song(song["name"], genre , usersForLaterUsage[song['author']],song['artist'],song['numberOfComments'],song["actualSong"])  
        for comment in comments: 
            commentObject = add_song_comment(songObject,usersForLaterUsage[comment['author']],comment["comment"],comment["rating"])

 
    
  
   

def add_user(name):  
    userObject , _ = User.objects.get_or_create(username = name) 
    userObject.save()  
     
    return UserProfile.objects.get_or_create(user = userObject)[0] , User.objects.get(username = name)
   
def add_genre(name): 
    genreObject , _ = Genre.objects.get_or_create(name = name) 
    genreObject.save() 
     
    return genreObject 
     
def add_playlist(name , genreList , author , views, numberOfComments , description , image = None):  
    playlistObject,_ = Playlist.objects.get_or_create(name = name, author = author , views = views, numberOfComments = numberOfComments , description = description) 
    playlistObject.genre.add(*genreList)
    playlistObject.save() 
     
    return playlistObject 
     

def add_playlist_comment(playlist,author,comment,rating):  
    commentObject,_ = PlaylistComment.objects.get_or_create(playlist = playlist,author = author , comment = comment , rating = rating)  
    commentObject.save()
    return commentObject 
     
def add_song_comment(song,author,comment,rating):  
    commentObject,_ = SongComment.objects.get_or_create(song = song,author = author , comment = comment , rating = rating)  
    commentObject.save()
    return commentObject 
     
def add_song(name , genreList , author , artist , numberOfComments, song, lyrics = None,image = None ):  
    songObject,_ = Song.objects.get_or_create(name = name, author = author ,artist = artist, numberOfComments = numberOfComments,actualSong = song) 
    songObject.genre.add(*genreList)
    songObject.save() 
     
    return songObject 



if __name__ == "__main__": 
    populate()