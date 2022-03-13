from haystack import indexes, query

from crescendo_app.models import Playlist, Song


class PlaylistIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Playlist

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class SongIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Song

    def index_queryset(self, using=None):
        return self.get_model().objects.all()