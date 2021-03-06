from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.contrib import auth
from django.urls import reverse

# Create your views here.
from django.views import View
from registration.forms import RegistrationForm

from crescendo_app.models import Playlist, Song, Question, UserProfile, Comment, User, LikeRecord, LikeCount
from crescendo_app.form import EditUserProfile, PlaylistForm, PlaylistEditForm, CommentForm, SongForm
from django.shortcuts import redirect


def index(request):
    context_dict = {}
    context_dict['playlists'] = Playlist.objects.all()
    context_dict['playlists'] = Playlist.objects.order_by("-views")
    context_dict['songs'] = Song.objects.all()[:3]
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

        context_dict['playlist'] = playlist
        playlist.views = playlist.views + 1
        playlist.save()

    except Playlist.DoesNotExist:
        context_dict['playlist'] = None

    return render(request, 'crescendo/playlist.html', context=context_dict)


def show_song(request, song_slug, song_id):
    context_dict = {}
    playlists = None

    try:
        song = Song.objects.get(nameAsSlug=song_slug, id=song_id)
        if request.user.is_authenticated:
            user, _ = UserProfile.objects.get_or_create(user=request.user)
            playlists = user.playlists.all()

        song = Song.objects.get(nameAsSlug=song_slug, id=song_id)
        # comment and reply for song
        song_content_type = ContentType.objects.get_for_model(song)
        if request.user.is_authenticated:
            user, _ = UserProfile.objects.get_or_create(user=request.user)
            playlists = user.playlists.all()

        context_dict['playlists'] = playlists
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
            form.author = UserProfile.objects.get_or_create(user=request.user)

            PlaylistF.author_id = request.user.id
            PlaylistF.name = form.cleaned_data.get("name")
            PlaylistF.save()
            # return redirect(request.META.get('HTTP_REFERER'))

            return redirect(f'/crescendo/userprofile/{request.user.id}')

    return render(request, 'crescendo/add_playlist.html', {'form': form})


def add_song(request):
    form = SongForm()

    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)

        if form.is_valid():

            print("isvalid")
            SongF = form.save(commit=False)
            form.author = UserProfile.objects.get_or_create(user=request.user)

            SongF.author_id = request.user.id
            print(form.cleaned_data.get('image'))
            SongF.save()
            
            return redirect(f'/crescendo/userprofile/{request.user.id}')
        else:
            print("notValid")
            print(form.errors)
    return render(request, 'crescendo/add_song.html', {'form': form})


def edit_playlist(request, playlist_slug, playlist_id):
    context_dict = {}
    form = PlaylistEditForm()

    context_dict['form'] = form
    try:
        playlist = Playlist.objects.get(nameAsSlug=playlist_slug, id=playlist_id)
        if request.method == 'POST':
            form = PlaylistEditForm(request.POST, request.FILES)
            if form.is_valid():
                playlist.image = form.cleaned_data.get("image")
                playlist.name = form.cleaned_data.get("name")
                playlist.nameAsSlug = slugify(form.cleaned_data.get("name"))
                playlist.description = form.cleaned_data.get("description")
                playlist.save()

                return render(request, 'crescendo/playlist.html', context={'playlist_slug': slugify(form.cleaned_data.get("name")), 'playlist_id' : playlist_id})


        try:
            songs = []
            for song in Song.objects.all():
                if playlist in song.playlist.all():
                    songs.append(song)
            context_dict['songs'] = songs
        except Song.DoesNotExist:
            context_dict['songs'] = None

        context_dict['playlist'] = playlist
        playlist.views = playlist.views + 1

    except Playlist.DoesNotExist:
        context_dict['playlist'] = None

    return render(request, 'crescendo/edit_playlist.html', context=context_dict)


def userProfile(request, id):
    context = {}
    songs = []
    playlists = []
    if request.user.is_authenticated:
        username = request.user.username
        user, _ = UserProfile.objects.get_or_create(user=request.user)
        user_id = request.user.id
        songs = user.songs.all()
        playlists = user.playlists.all()

        context['songs'] = songs
        context['playlists'] = playlists
        context['userprofile'] = user

    playlists = []
    user = User.objects.get(id=id)
    context['userNotNative'] = user
    user_content_type = ContentType.objects.get_for_model(user)
    username = user.username

    user, _ = UserProfile.objects.get_or_create(user=user)
    user_id = id
    songs = user.songs.all()
    playlists = user.playlists.all()

    context['songs'] = songs
    context['playlists'] = playlists
    context['userprofile'] = user

    user.numberOfProfileViews = user.numberOfProfileViews + 1
    user.save()

    return render(request, 'crescendo/user_profile.html',
                  context=context)


def add_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    context_dict = {}

    if comment_form.is_valid():
        # for comment
        comment = Comment()
        comment.author = comment_form.cleaned_data['user']
        user_profile, _ = UserProfile.objects.get_or_create(user=comment_form.cleaned_data['user'])
        user_profile.numberOfComments = int(user_profile.numberOfComments) + 1
        comment.author = comment_form.cleaned_data['user']
        user_profile, _ = UserProfile.objects.get_or_create(user=comment_form.cleaned_data['user'])
        user_profile.numberOfComments = int(user_profile.numberOfComments) + 1
        user_profile.save()
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


def add_to_playlist(request, song, playlist):
    playlistObject = Playlist.objects.get(id=playlist)
    songObject = Song.objects.get(id=song)
    songObject.playlist.add(playlistObject)
    songs = []
    for song in Song.objects.all():
        if playlistObject in song.playlist.all():
            songs.append(song)

    return render(request, 'crescendo/playlist.html', context={"playlist": playlistObject, "songs": songs})


def add_more_songs(request):
    data = {}
    return JsonResponse(data)


class PlaylistSort(View):
    def get(self, request):
        if 'sortBy' in request.GET:
            sortBy = request.GET['sortBy']
        else:
            sortBy = ''

        if sortBy == "views" or sortBy == "":
            playlists = Playlist.objects.order_by("-views")
        elif sortBy == "noOfComments":
            playlists = Playlist.objects.order_by("-numberOfComments")

        return render(request, "crescendo/playlist_sort.html", {'playlists': playlists})


def edit_profile(request):
    if request.method == 'POST':
        form = EditUserProfile(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            profile = UserProfile.objects.get(id=user.id)
            profile.image = form.cleaned_data.get("image")
            profile.save()
            return redirect(f'/crescendo/userprofile/{user.id}')
    else:
        form = EditUserProfile()

    return render(request, 'crescendo/edit_profile.html', context={'form': form})


class delete_song(View):
    def post(self, request):
        playlistID = request.POST['playlistID']
        songID = request.POST['songID']

        targetPlaylist = Playlist.objects.get(id=playlistID)
        targetSong = Song.objects.get(id=songID)

        targetSong.playlist.remove(targetPlaylist)

        return render(request, 'crescendo/edit_playlist.html')

class delete_playlist(View):
    def post(self, request):
        playlistID = request.POST['playlistID']

        Playlist.objects.filter(id=playlistID).delete()

        return render(request, 'crescendo/edit_playlist.html')

class drop_song(View):
    def post(self, request):
        songID = request.POST['songID']

        Song.objects.filter(id=songID).delete()

        return render(request, 'crescendo/SongCatalogue.html')

def edit_details(request, playlist_slug, playlist_id):
    form = PlaylistEditForm()
    context_dict = {}
    playlist = Playlist.objects.get(playlist_id)
    if request.method == 'POST':
        form = PlaylistEditForm(request.POST)
        if form.is_valid():
            playlist.image = form.cleaned_data.get("image")
            playlist.name = form.cleaned_data.get("name")
            playlist.description = form.cleaned_data.get("description")
            playlist.save()

            context_dict['playlists'] = Playlist.objects.order_by()
            return render(request, 'crescendo/PlaylistCatalogue.html', context=context_dict)
        else:
            print(form.errors)

    return render(request, 'crescendo/PlaylistCatalogue.html', context=context_dict)


def ErrorResponse(code, message):
    data = {'status': 'ERROR', 'code': code, 'message': message}
    return JsonResponse(data)


def SuccessResponse(liked_num):
    data = {'status': 'SUCCESS', 'liked_num': liked_num}
    return JsonResponse(data)


def like_change(request):
    # get data
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, 'you were not login')

    content_type = request.GET.get('content_type')
    object_id = request.GET.get('object_id')

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(id=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, 'object not exist')

    if request.GET.get('is_like') == 'true':
        # likes
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id,
                                                                user=user)
        if created:
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            # already liked
            return ErrorResponse(402, 'you were liked')
    else:
        # cancel like
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                return ErrorResponse(404, 'data error')
        else:
            # not liked, can not cancel
            return ErrorResponse(403, 'you were not liked')
