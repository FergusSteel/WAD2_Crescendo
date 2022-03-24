 
# IMPORTS  
from cgitb import strong
from operator import contains
from django.test import TestCase  
from crescendo_app.models import User,UserProfile , Playlist , Song , Genre, Comment 
from datetime import datetime 
from crescendo_app.views import index
 
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
        playlist = Playlist(author = user_profile , name = "The best crescendo_app" , views = -100 )
        playlist.save() 

        self.assertTrue((playlist.views >= 0), True) 
         
    def test_ensure_playlist_comments_are_positive(self):  
        user = User(username = "Yet another user") 
        user.save()
        user_profile = UserProfile(user = user, numberOfProfileViews=-100)
        user_profile.save()  
        playlist = Playlist(author = user_profile,name  = "The second best crescendo_app I guess" , numberOfComments = -100)
        playlist.save() 

        self.assertTrue((playlist.numberOfComments >= 0), True)  
        
    def test_ensure_playlist_name_is_slugged(self):  
        user = User(username = "User") 
        user.save()
        user_profile = UserProfile(user = user, numberOfProfileViews=-100)
        user_profile.save() 
        playlist = Playlist(author = user_profile , name = "The best crescendo_app" )
        playlist.save() 

        self.assertEquals(playlist.nameAsSlug , 'the-best-crescendo_app')
         
    def test_ensure_there_is_a_default_image_for_playlist(self):  
        user = User(username = "Playlist Owner") 
        user.save()
        user_profile = UserProfile(user = user, numberOfProfileViews=-100)
        user_profile.save() 
        playlist = Playlist(author = user_profile , name = "The best crescendo_app")
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
 
    def test_ensure_song_is_added_to_playlists(self): 
        user = User(username = "Playlist Owner") 
        user.save()    
        userprofile = UserProfile(user = user) 
        userprofile.save()
        names = ["Playlist 1" , "Playlist 2 " , "Playlist 3" , "Playlist 4"]  
        playlists = {}
        for name in names: 
            playlist = Playlist(author = userprofile , name = name)
            playlist.save() 
            playlists[name] = playlist

        song = Song(author = userprofile,name  = "The second best song I guess")   
        song.save() 
        song.playlist.add(*playlists.values())
        song.save()

        self.assertTrue(all([True if playlist.name in names else False for playlist in song.playlist.all()]))  
         
          
class CommentMethodTests(TestCase):  
     
    def test_ensure_comment_is_added(self): 
        user = User(username = "A User") 
        user.save()    
        userprofile = UserProfile(user = user) 
        userprofile.save()  
        song = Song(author = userprofile,name  = "The next big song")   
        song.save()  
         
        comment = Comment() 
        comment.text = "A new Commment" 
        comment.author = user 
        comment.content_object = song 
        comment.save() 
         
        self.assertEquals(1, Comment.objects.filter(author = user).count()) 
         
          
    def test_ensure_correct_comment_time(self):  
        user = User(username = "A User") 
        user.save()    
        userprofile = UserProfile(user = user) 
        userprofile.save()  
        song = Song(author = userprofile,name  = "The next big song")   
        song.save()  
         
        comment = Comment() 
        comment.text = "A new Commment" 
        comment.author = user 
        comment.content_object = song 
        comment.save() 
        print(comment.comment_time)   
        today = datetime.today().strftime('%Y-%m-%d')
         
        self.assertEquals(str(today) , str(Comment.objects.get(id = comment.id).comment_time)[0:10])
         
         

#Views 
 

         
        



         
         
    