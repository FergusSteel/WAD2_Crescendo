from django.contrib import admin 
from crescendo_app.models import UserProfile,Genre,Song,SongComment,Playlist,PlaylistComment

# Register your models here.
  
admin.site.register(UserProfile) 
admin.site.register(Genre) 
admin.site.register(Song) 
admin.site.register(SongComment) 
admin.site.register(Playlist) 
admin.site.register(PlaylistComment)   
 

# class GenreAdmin(admin.ModelAdmin): 
#     list_display = ('name') 

# class SongAdmin(admin.ModelAdmin): 
#     list_display  = ('name','artist','genre') 

# class PlaylistAdmin(admin.ModelAdmin): 
#     list_display  = ('name','genre')  
