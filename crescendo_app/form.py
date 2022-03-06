from django import forms
from django.contrib.auth.models import User

from crescendo_app.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), min_length=6)

    class Meta:
        model = User
        fields = ('username', 'password', 'email',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('image',)
