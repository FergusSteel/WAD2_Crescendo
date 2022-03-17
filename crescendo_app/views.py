
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse


from crescendo_app.models import Playlist, Song, SongComment , Question , UserProfile
from crescendo_app.form import PlaylistForm, PlaylistEditForm
from django.shortcuts import redirect


def index(request):
    context_dict = {}
    context_dict['playlists'] = Playlist.objects.all()
    context_dict['songs'] = Song.objects.all()
    return render(request, 'crescendo/index.html', context=context_dict)


def about(request):
    context_dict = {}
    return render(request, 'crescendo/about.html', context=context_dict)


def faq(request):
    context_dict = {}
    context_dict['questions'] = Question.objects.all()
    return render(request, 'crescendo/faq.html', context=context_dict)


def contactUs(request):
    context_dict = {}
    return render(request, 'crescendo/contactUs.html', context=context_dict)


def show_playlist(request, playlist_slug, playlist_id):
    context_dict = {}

    try:
        playlist = Playlist.objects.get(nameAsSlug=playlist_slug, id=playlist_id)
        try:
            songs = []
            for song in Song.objects.all():
                if playlist in song.playlist.all():
                    songs.append(song)
            context_dict['songs'] = songs
        except Song.DoesNotExist:
            context_dict['songs'] = None

        context_dict['crescendo_app'] = playlist

    except Playlist.DoesNotExist:
        context_dict['crescendo_app'] = None

    return render(request, 'crescendo/playlist.html', context=context_dict)


def show_song(request, song_slug, song_id):
    context_dict = {}

    try:
        song = Song.objects.get(nameAsSlug=song_slug, id=song_id)
        try:
            comments = []
            for comment in SongComment.objects.all():
                if comment.song == song:
                    comments.append(comment)
            context_dict['comments'] = comments
        except:
            context_dict['comments'] = None

        context_dict['song'] = song

    except Song.DoesNotExist:
        context_dict['song'] = None

    return render(request, 'crescendo/song.html', context=context_dict)


def userProfile(request):
    pass


def search(request):
    search_word = request.GET.get('q', '').strip()
    condition = None
    for word in search_word.split(' '):
        if condition is None:
            condition = Q(name__icontains=word)
        else:
            condition = condition | Q(name__icontains=word)
    search_playlist = []
    search_song = []
    if condition is not None:
        search_playlist = Playlist.objects.filter(condition)
        search_song = Song.objects.filter(condition)

    paginator_playlist = Paginator(search_playlist, 3)
    paginator_song = Paginator(search_song, 5)
    page_num = request.GET.get('page', 1)
    page_of_playlist = paginator_playlist.get_page(page_num)
    page_of_song = paginator_song.get_page(page_num)

    context = {}
    context['search_words'] = search_word
    context['playlist_count'] = search_playlist.count()
    context['song_count'] = search_song.count()
    context['page_of_playlist'] = page_of_playlist
    context['page_of_song'] = page_of_song
    return render(request, 'crescendo/search.html', context=context)


# Playlists and Songs
def PlaylistCatalogue(request):
    context_dict = {}
    context_dict['playlists'] = Playlist.objects.order_by()
    return render(request, 'crescendo/PlaylistCatalogue.html', context=context_dict)


def SongCatalogue(request):
    context_dict = {}
    context_dict['songs'] = Song.objects.order_by()
    return render(request, 'crescendo/SongCatalogue.html', context=context_dict)


# Add crescendo_app

def add_playlist(request):
    form = PlaylistForm()

    if request.method == 'POST':
        form = PlaylistForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return redirect('/crescendo/')
        else:

            print(form.errors)

    return render(request, 'crescendo/add_playlist.html', {'form': form})
 
  

def edit_playlist(request , pk):  
    print(pk) 
    try:
        playlist = Playlist.objects.get(id = pk)
    except Playlist.DoesNotExist:
        playlist = None 

    instance = Playlist.objects.get(id=pk)
    form = PlaylistEditForm(request.POST or None, instance=instance)  

    if request.method == 'POST':   
        form = PlaylistEditForm(request.POST)
         
        if form.is_valid(): 
            form.save(commit=True) 
            return redirect('/crescendo/') 
    else:
        form = PlaylistEditForm() 
             
        return render(request,'crescendo/edit_playlist.html',context = {'form': form, 'playlist' : playlist})


def userProfile(request): 
    username = None  
    songs = [] 
    playlists = [] 
    user = None
    if request.user.is_authenticated:
        username = request.user.username  
        user = UserProfile.objects.get(user = request.user)
        songs = user.songs.all() 
        playlists = user.playlists.all() 
        comments = user.comments.all()
         
     
    return render(request,'crescendo/user_profile.html' , context = {'userprofile':user,'songs':songs , 'playlists':playlists , 'comments':comments})
