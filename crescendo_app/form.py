from django import forms
from django.contrib.auth.models import User

from crescendo_app.models import UserProfile,Song,Playlist

class PlaylistForm(forms.ModelForm):
    name = forms.CharField(max_length=128,help_text="Please enter the playlist name.")
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    comments= forms.CharField(max_length=128,help_text="Please enter comment...")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:

        model = Playlist
        fields = ('name',)