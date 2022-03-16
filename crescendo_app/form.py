from django import forms
from django.contrib.auth.models import User

from crescendo_app.models import UserProfile, Song, Playlist, Genre


class PlaylistForm(forms.ModelForm):
    
    name = forms.CharField(max_length=128, help_text="Please enter the playlist name.")
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Playlist
        fields = ('name',)
 
  
class PlaylistEditForm(forms.ModelForm): 
    name = forms.CharField(max_length = 128) 
    image = forms.ImageField()  
    description = forms.CharField(max_length = 300) 
    # genre = forms.ChoiceField(*Genre.objects) 

    class Meta: 
        model = Playlist  
        fields = ('name','image','description',)
