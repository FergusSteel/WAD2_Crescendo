 
# IMPORTS  
from doctest import TestResults
from this import d
from django.test import TestCase  
from crescendo_app.models import User,UserProfile , Playlist , Song , Genre, Comment 
from datetime import datetime 
from crescendo_app.views import index 
from django.urls import reverse 
from django.test import Client 
from django.contrib import auth
 
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
        today = datetime.today().strftime('%Y-%m-%d')
         
        self.assertEquals(str(today) , str(Comment.objects.get(id = comment.id).comment_time)[0:10])
         
         

#View Tests 
 
class ViewMethodTests(TestCase):  
      
    def test_index_page_has_response(self):
        response = self.client.get(reverse('crescendo:index')) 
        self.assertEquals(response.status_code, 200) 
         
    def test_index_page_has_playlist(self):   
        user = User(username = "Another user") 
        user.save()
        user_profile = UserProfile(user = user, numberOfProfileViews=-100)
        user_profile.save() 
        playlist = Playlist(author = user_profile , name = "The best crescendo_app" , views = -100 )
        playlist.save() 
        
        response = self.client.get(reverse('crescendo:index'))  
        self.assertTrue('The best crescendo_app' in response.content.decode()) 
          
    def test_index_page_has_song(self):  
        user = User(username = "Another user") 
        user.save()
        user_profile = UserProfile(user = user, numberOfProfileViews=-100)
        user_profile.save()  
        song = Song(author = user_profile,name  = "The second best song I guess")   
        song.save()  
          
        response = self.client.get(reverse('crescendo:index')) 
        self.assertTrue('The second best song I guess' in response.content.decode())
   
class SongPage(TestCase):   
    
    def test_song_catalogue_has_response(self):
        response = self.client.get(reverse('crescendo:SongCatalogue')) 
        self.assertEquals(response.status_code, 200)  


    def test_amount_of_songs_matches_amount_in_database(self):
        user = User(username = "Another user") 
        user.save()
        user_profile = UserProfile(user = user, numberOfProfileViews=-100)
        user_profile.save()  
        

        songs = ['Song1','Song2','Song3'] 
        
        for song in songs:  
            songObject = Song.objects.create(author = user_profile,name = song)  
            songObject.save()
            
            
        response = self.client.get(reverse('crescendo:SongCatalogue'))   
        
        

        self.assertTrue('<strong>Song1</strong>' in response.content.decode())
        self.assertTrue('<strong>Song2</strong>' in response.content.decode())  
        self.assertTrue('<strong>Song3</strong>' in response.content.decode()) 


class PlaylistPage(TestCase):   
     
        def test_song_catalogue_has_response(self):
            response = self.client.get(reverse('crescendo:PlaylistCatalogue')) 
            self.assertEquals(response.status_code, 200) 
        
        def test_amount_of_playlists_matches_amount_in_database(self):
            user = User(username = "Another user") 
            user.save()
            user_profile = UserProfile(user = user, numberOfProfileViews=-100)
            user_profile.save()  
            

            playlists = ['Playlist1','Playlist2','Playlist3'] 
            
            for playlist in playlists:  
                playlistObject = Playlist.objects.create(author = user_profile,name = playlist)  
                playlistObject.save()
                
                
            response = self.client.get(reverse('crescendo:PlaylistCatalogue'))   
            
            

            self.assertTrue('<strong>Playlist1</strong>' in response.content.decode())
            self.assertTrue('<strong>Playlist2</strong>' in response.content.decode())  
            self.assertTrue('<strong>Playlist3</strong>' in response.content.decode()) 

        
                
class Login(TestCase):  
    def test_song_catalogue_has_response(self):
        response = self.client.get(reverse('auth_login')) 
        self.assertEquals(response.status_code, 200)  
              
    def test_can_login(self):  
        user = User(username = "Another user")  
        user.password = "test123"
        user.save()
        user_profile = UserProfile(user = user, numberOfProfileViews=-100)
        user_profile.save()  
        response = self.client.post(reverse('auth_login'), {'username': user.username, 'password': user.password})
  
        self.assertTrue(user.is_authenticated)
 
    def login_redirects_to_index(self):  
        user = User(username = "Another user")  
        user.password = "test123"
        user.save()
        user_profile = UserProfile(user = user, numberOfProfileViews=-100)
        user_profile.save()  
        response = self.client.post(reverse('auth_login'), {'username': user.username, 'password': user.password}) 

        self.assertRedirects(response, 'crescendo:index', status_code=302, 
        target_status_code=200, fetch_redirect_response=True) 
 

class Register(TestCase):  

    def test_register_has_response(self):
        response = self.client.get(reverse('registration_register')) 
        self.assertEquals(response.status_code, 200)  
             
    def test_successfull_register(self): 
        username = "usernameOfUser" 
        email = "usernameOfUser@gmail.com" 
        password = "testpass123"  

        self.client.post(reverse('registration_register'), {'username': username, 'email': email,'password1': password , 'password2':password}) 
        

        self.assertFalse(User.objects.get_or_create(username = username)[1]) 
         
    def test_register_incorrect_username_invalid_invalid_character(self):  
        username = "usernameOfUser........*&^%$#@#$%^&*().." 
        email = "usernameOfUser@gmail.com" 
        password = "testpass123"  
 
  
        self.client.post(reverse('registration_register'), {'username': username, 'email': email,'password1': password , 'password2':password}) 
        try:  
            User.objects.get(username = username)  
            self.assertFalse(True , "User has been creted with an invalid username") 
        except User.DoesNotExist:  
            self.assertTrue(True) 
             

    def test_register_invalid_email(self):  
        username = "usernameOfUser........*&^%$#@#$%^&*().." 
        email = "usernameOfUsergmail.com" 
        password = "testpass123"    
         
          
        self.client.post(reverse('registration_register'), {'username': username, 'email': email,'password1': password , 'password2':password}) 
        try:  
            User.objects.get(username = username)  
            self.assertFalse(True , "User has been creted with an invalid email") 
        except User.DoesNotExist:  
            self.assertTrue(True) 
             
              
    def test_register_invalid_password_fully_numeric(self):   
        username = "usernameOfUser........*&^%$#@#$%^&*().." 
        email = "usernameOfUser@gmail.com" 
        password = "123456789"   

        self.client.post(reverse('registration_register'), {'username': username, 'email': email,'password1': password , 'password2':password}) 
        try:  
            User.objects.get(username = username)  
            self.assertFalse(True , "User has been creted with an invalid password") 
        except User.DoesNotExist:  
            self.assertTrue(True)   
             
    def test_register_invalid_password_too_short(self):   
        username = "usernameOfUser........*&^%$#@#$%^&*().." 
        email = "usernameOfUser@gmail.com" 
        password = "a"   

        self.client.post(reverse('registration_register'), {'username': username, 'email': email,'password1': password , 'password2':password}) 
        try:  
            User.objects.get(username = username)  
            self.assertFalse(True , "User has been creted with an invalid password") 
        except User.DoesNotExist:  
            self.assertTrue(True)  
             

    def test_register_invalid_password_common_word(self):  
        username = "usernameOfUser........*&^%$#@#$%^&*().." 
        email = "usernameOfUser@gmail.com" 
        password = "hello123"   
         
        self.client.post(reverse('registration_register'), {'username': username, 'email': email,'password1': password , 'password2':password}) 
        try:  
            User.objects.get(username = username)  
            self.assertFalse(True , "User has been creted with an invalid password - common word of hello") 
        except User.DoesNotExist:  
            self.assertTrue(True) 
 

# class UserProfileTests(TestCase): 
     
#     def test_userprofile_displays_correctly(self):  
#         user = User(username = "Another user") 
#         user.save()
#         user_profile = UserProfile(user = user)
#         user_profile.save()    
         
#         response = self.client.get(reverse('crescendo:userprofile' , kwargs= {''}))    

          
        
        


         
        



         
         
    