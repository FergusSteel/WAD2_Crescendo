from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget

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


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
                           error_messages={'required': 'Comment can not be empty!!'})

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        # check login
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('Your are not log in')

        content_type = self.cleaned_data['content_type']
        object_id  =  self.cleaned_data['object_id']
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(id=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('Comment object does not exist!')

        return self.cleaned_data
