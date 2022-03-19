from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from crescendo_app.models import Playlist, Song, Question, UserProfile, Comment
from crescendo_app.form import PlaylistForm, PlaylistEditForm, CommentForm
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
        playlist_content_type = ContentType.objects.get_for_model(playlist)
        comments = Comment.objects.filter(content_type=playlist_content_type, object_id=playlist_id, parent=None)
        context_dict['comments'] = comments('-comment_time')
        context_dict['comment_form'] = CommentForm(
            initial={'content_type': playlist_content_type.model, 'object_id': playlist_id})
        context_dict['comment_count'] = Comment.objects.filter(content_type=playlist_content_type,
                                                               object_id=playlist_id).count()
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
        # comment and reply for song
        song_content_type = ContentType.objects.get_for_model(song)
        comments = Comment.objects.filter(content_type=song_content_type, object_id=song_id, parent=None)
        context_dict['comments'] = comments.order_by('-comment_time')
        context_dict['comment_form'] = CommentForm(
            initial={'content_type': song_content_type.model, 'object_id': song_id, 'reply_comment_id': 0})
        context_dict['comment_count'] = Comment.objects.filter(content_type=song_content_type,
                                                               object_id=song_id).count()

        context_dict['song'] = song

    except Song.DoesNotExist:
        context_dict['song'] = None

    return render(request, 'crescendo/song.html', context=context_dict)


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
            PlaylistF = form.save(commit=False)
            form.author = UserProfile.objects.get(user=request.user)

            PlaylistF.author_id = request.user.id
            PlaylistF.save()

            return redirect('/crescendo/')
        else:

            print(form.errors)

    return render(request, 'crescendo/add_playlist.html', {'form': form})


def edit_playlist(request, pk):
    print(pk)
    try:
        playlist = Playlist.objects.get(id=pk)
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

        return render(request, 'crescendo/edit_playlist.html', context={'form': form, 'playlist': playlist})


def userProfile(request):
    username = None
    context = {}
    songs = []
    playlists = []
    if request.user.is_authenticated:
        username = request.user.username
        user , _ = UserProfile.objects.get_or_create(user=request.user) 
        user_id = request.user.id
        songs = user.songs.all()
        playlists = user.playlists.all()

        user_content_type = ContentType.objects.get_for_model(user)
        comments = Comment.objects.filter(content_type=user_content_type, object_id=user_id, parent=None)
        context['comments'] = comments
        context['comment_form'] = CommentForm(
            initial={'content_type': user_content_type.model, 'object_id': user_id})
        context['comment_count'] = Comment.objects.filter(content_type=user_content_type,
                                                          object_id=user_id).count()
        context['songs'] = songs
        context['playlists'] = playlists 
        context['userprofile'] = user

    return render(request, 'crescendo/user_profile.html',
                  context=context)


def add_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    context_dict = {}

    if comment_form.is_valid():
        # for comment
        comment = Comment()
        comment.author = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        # for reply
        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.author
        comment.save()

        # return data
        # ajax
        context_dict['status'] = 'SUCCESS'
        # comment
        context_dict['username'] = comment.author.username
        context_dict['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        context_dict['text'] = comment.text

        # reply
        if parent is not None:
            context_dict['reply_to'] = comment.reply_to.username
        else:
            context_dict['reply_to'] = ''

        context_dict['id'] = comment.id
        context_dict['root_id'] = comment.root.id if comment.root is not None else ''
    # ajax error message
    else:
        context_dict['status'] = 'ERROR'
        context_dict['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(context_dict)
