# IMPORTS
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


# MODELS 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    numberOfComments = models.IntegerField(default=0)
    numberOfProfileViews = models.IntegerField(default=0)
    image = models.ImageField(upload_to="profile_images", default='profile_images/default.jpg')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if (self.numberOfComments < 0 or self.numberOfProfileViews < 0):
            self.numberOfComments = 0
            self.numberOfProfileViews = 0
        super(UserProfile, self).save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=30)
    nameAsSlug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.nameAsSlug = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)


class Playlist(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="playlists")
    genre = models.ManyToManyField(Genre)
    name = models.CharField(max_length=30)
    nameAsSlug = models.SlugField()
    views = models.IntegerField(default=0)
    numberOfComments = models.IntegerField(default=0)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to="playlist_images", default='playlist_images/default.png')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.nameAsSlug = slugify(self.name)
        if (self.views < 0 or self.numberOfComments < 0):
            self.views = 0
            self.numberOfComments = 0
        super(Playlist, self).save(*args, **kwargs)


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    text = models.CharField(max_length=300)
    comment_time = models.DateTimeField(auto_now_add=True)

    # for reply
    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name='reply', null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['comment_time']


class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    liked_num = models.IntegerField(default=0)


class LikeRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_time = models.DateTimeField(auto_now_add=True)


class Song(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="songs")
    genre = models.ManyToManyField(Genre)
    playlist = models.ManyToManyField(Playlist)
    name = models.CharField(max_length=30)
    nameAsSlug = models.SlugField()
    artist = models.CharField(max_length=300)
    numberOfComments = models.IntegerField(default=0)
    image = models.ImageField(upload_to="song_images", default='song_images/default.jpg')
    lyrics = models.CharField(max_length=1000)
    actualSong = models.FileField(upload_to="music_files", blank=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.nameAsSlug = slugify(self.name)
        if (self.numberOfComments < 0):
            self.numberOfComments = 0
        super(Song, self).save(*args, **kwargs)


class Question(models.Model):
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=300)

    def __str__(self):
        return "Question " + self.question
