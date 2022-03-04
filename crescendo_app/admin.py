
from django.contrib import admin 
from crescendo_app.models import UserProfile,Genre,Song,SongComment,Playlist,PlaylistComment

# Register your models here. 
 
class SongAdmin(admin.ModelAdmin): 
    list_display = ('name','artist',)
  
class PlaylistAdmin(admin.ModelAdmin): 
    list_display = ('name','author',) 
     
class GenreAdmin(admin.ModelAdmin): 
    list_display = ('name',) 
     
class CommentAdmin(admin.ModelAdmin):  
    list_display = ('author','rating',)
     
  
admin.site.register(UserProfile) 
admin.site.register(Genre, GenreAdmin) 
admin.site.register(Song, SongAdmin) 
admin.site.register(SongComment , CommentAdmin) 
admin.site.register(Playlist , PlaylistAdmin) 
admin.site.register(PlaylistComment , CommentAdmin)   
 
