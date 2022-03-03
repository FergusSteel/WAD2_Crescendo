from django.db import models 
from django.contrib.auth.models import User

# Create your models here. 
 
  
class UserProfile(models.Model):  
    user = models.OneToOneField(User, on_delete = models.CASCADE) 
     
    numberOfComments = models.IntegerField(default=0) 
    numberOfProfileViews = models.IntegerField(default =0) 
    image = models.ImageField(upload_to = "profile_images",blank = True)  
     
    def __str__(self): 
        return self.user.username 
         


class Genre(models.Model): 
    name = models.CharField(unique=True , max_length = 30) 
     
    def __str__(self): 
        return self.name 
 
   
class Playlist(models.Model): 
    author = models.ForeignKey(User , on_delete=models.CASCADE) 
    genre = models.ManyToManyField(Genre) 
    name = models.CharField(max_length  = 30) 
    views = models.IntegerField(default = 0) 
    numberOfComments = models.IntegerField(default = 0) 
    description = models.CharField(max_length = 300) 
    image = models.ImageField(upload_to = "playlist_images" , blank = True)  
     
    def __str__(self): 
        return self.name
 
class Song(models.Model): 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)  
    name = models.CharField(max_length = 30) 
    artist = models.CharField(max_length = 300) 
    numberOfComments = models.IntegerField() 
    image = models.ImageField(upload_to = "song_images",blank = True) 
    lyrics = models.CharField(max_length = 1000) 
    actualSong = models.FileField(upload_to = "music_files") 
     
    def __str__(self): 
        return self.name  
         
  
class Comment(models.Model):  
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    comment = models.CharField(max_length = 300) 
    rating = models.IntegerField() 

class SongComment(Comment): 
    song = models.ForeignKey(Song , on_delete=models.CASCADE) 
     
    def __str__(self): 
        return "Comment about a song from " + self.author + " of rating" + self.rating 

     
class PlaylistComment(Comment):  
    playlist = models.ForeignKey(Playlist , on_delete = models.CASCADE)  
     
    def __str__(self): 
        return "Comment about a playlist from " + self.author + " of rating" + self.rating  
         
          
     






