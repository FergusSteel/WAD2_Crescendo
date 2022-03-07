# IMPORTS 
from django.db import models
from django.contrib.auth.models import User 
from django.template.defaultfilters import slugify  
 
# MODEL TESTS 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    numberOfComments = models.IntegerField(default=0)
    numberOfProfileViews = models.IntegerField(default=0)
    image = models.ImageField(upload_to="profile_images", default = 'profile_images/default.jpg')

    def __str__(self):
        return self.user.username 
         
    def save(self, *args, **kwargs):    
        if (self.numberOfComments < 0 or self.numberOfProfileViews < 0):
            self.numberOfComments = 0 
            self.numberOfProfileViews = 0
        super(UserProfile, self).save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=30) 
    nameAsSlug = models.SlugField(unique = True)

    def __str__(self):
        return self.name  
         
    def save(self, *args , **kwargs): 
        self.nameAsSlug = slugify(self.name) 
        super(Genre , self).save(*args , **kwargs)
    

class Playlist(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    name = models.CharField(max_length=30)
    views = models.IntegerField(default=0)
    numberOfComments = models.IntegerField(default=0)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to="playlist_images" , default = 'playlist_images/default.jpg')

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    rating = models.IntegerField()


class Song(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre) 
    playlist = models.ManyToManyField(Playlist)
    name = models.CharField(max_length=30)
    artist = models.CharField(max_length=300)
    numberOfComments = models.IntegerField()
    image = models.ImageField(upload_to="song_images", default = 'song_images/default.jpg')
    lyrics = models.CharField(max_length=1000)
    actualSong = models.FileField(upload_to="music_files")

    def __str__(self):
        return self.name

 
# Both song and playlist comment classes inherit from the comment class, due to shared attributes
class SongComment(Comment):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return "Comment about a song from " + self.author.user + " of rating" + self.rating


class PlaylistComment(Comment):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    def __str__(self):
        return "Comment about a playlist from " + self.author.user + " of rating" + self.rating