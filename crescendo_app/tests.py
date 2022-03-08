 
# IMPORTS  
from cgitb import strong
from operator import contains
from django.test import TestCase  
from crescendo_app.models import User,UserProfile , Playlist , Song , PlaylistComment , SongComment , Genre
 
# MODEL TESTS
 
class UserMethodTests(TestCase):  

    def test_ensure_profile_views_are_positive(self): 
        user = User(username = "A Brand New Test User") 
        user.save()
        user_profile = UserProfile(user = user, numberOfProfileViews=-100)
        user_profile.save() 

        self.assertEqual((user_profile.numberOfProfileViews >= 0), True) 
         
    def test_ensure_comments_are_positive(self):  
        user = User(username = "A Brand New Test User 2") 
        user.save()
        user_profile = UserProfile(user = user, numberOfComments=-100)
        user_profile.save() 

        self.assertEqual((user_profile.numberOfComments >= 0), True) 

    def test_ensure_user_is_related_to_user_profile(self):  
        user = User(username = "A Brand New Test User 3") 
        user.save()
        user_profile = UserProfile(user = user)
        user_profile.save()  
         
        self.assertEqual(user_profile.user , user) 
         
class GenreMethodTests(TestCase): 
    def test_ensure_category_name_is_in_slug_form(self): 
        genre = Genre(name = "Electronic Dance Music") 
        genre.save() 
         
        self.assertEquals(genre.nameAsSlug , "electronic-dance-music")
  
 
class PlaylistMethodTests(TestCase):  
     
    def test_ensure_playlist_views_are_positive(self):  
        user = User(username = "Another user") 
        user.save()
        user_profile = UserProfile(user = user, numberOfProfileViews=-100)
        user_profile.save() 
        playlist = Playlist(author = user_profile , name = "The best playlist" , views = -100 ) 
        playlist.save() 

        self.assertTrue((playlist.views >= 0), True) 
         
    def test_ensure_playlist_comments_are_positive(self):  
        user = User(username = "Yet another user") 
        user.save()
        user_profile = UserProfile(user = user, numberOfProfileViews=-100)
        user_profile.save()  
        playlist = Playlist(author = user_profile,name  = "The second best playlist I guess" , numberOfComments = -100) 
        playlist.save() 

        self.assertTrue((playlist.numberOfComments >= 0), True)  
        
    def test_ensure_playlist_name_is_slugged(self):  
        user = User(username = "User") 
        user.save()
        user_profile = UserProfile(user = user, numberOfProfileViews=-100)
        user_profile.save() 
        playlist = Playlist(author = user_profile , name = "The best playlist" ) 
        playlist.save() 

        self.assertEquals(playlist.nameAsSlug , 'the-best-playlist')  
         
    def test_ensure_there_is_a_default_image_for_playlist(self):  
        user = User(username = "Playlist Owner") 
        user.save()
        user_profile = UserProfile(user = user, numberOfProfileViews=-100)
        user_profile.save() 
        playlist = Playlist(author = user_profile , name = "The best playlist") 
        playlist.save()  
         
        self.assertTrue(playlist.image != None)
  
class SongMethodTests(TestCase):  
         
    def test_ensure_song_comments_are_positive(self):  
        user = User(username = "Song owner") 
        user.save()
        user_profile = UserProfile(user = user, numberOfProfileViews=-100)
        user_profile.save() 
        song = Song(author = user_profile,name  = "The second best song I guess" , numberOfComments = -100) 
        song.save() 

        self.assertTrue((song.numberOfComments >= 0), True)  


    def test_ensure_song_name_is_slugged(self):  
        user = User(username = "Song owner 2") 
        user.save()
        user_profile = UserProfile(user = user, numberOfProfileViews=-100)
        user_profile.save() 
        playlist = Song(author = user_profile , name = "The best song" ) 
        playlist.save()  

        self.assertEquals(playlist.nameAsSlug , 'the-best-song')  
 
    # def test_ensure_song_is_added_to_playlists(self): 
    #     user = User(username = "Playlist Owner") 
    #     user.save()   
    #     names = ["Playlist 1" , "Playlist 2 " , "Playlist 3" , "Playlist 4"]  
    #     playlists = {}
    #     for name in names: 
    #         playlist = Playlist(author = user , name = name) 
    #         playlist.save()  

    #     song = Song(author = user,name  = "The second best song I guess")  
        #song.playlist.add(*playlists.values) 
        #song.save()

        #self.assertTrue(all([True if names.contains(playlist.name) else False for playlist in song.playlist]))