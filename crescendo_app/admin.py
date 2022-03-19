from django.contrib import admin
from crescendo_app.models import UserProfile, Genre, Song, Playlist, Question, Comment


# Register your models here.

class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist',)


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'text', 'comment_time', 'author', 'rate')
 

admin.site.register(UserProfile)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Question)