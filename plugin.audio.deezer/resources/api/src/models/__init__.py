

class Album(object):
    def __init__(self, connection, album):
        self.connection = connection
        self.__dict__.update(album)

    def get_tracks(self):
        if hasattr(self, 'tracks') and isinstance(self.tracks, IterableCollection):
            return self.tracks
        self.tracks = self.connection.make_request('album', self.id, 'tracks')
        return self.tracks

    def get_fans(self):
        if hasattr(self, 'fans') and isinstance(self.fans, IterableCollection):
            return self.fans
        self.fans = self.connection.make_request('album', self.id, 'fans')
        return self.fans

    def get_comments(self):
        if hasattr(self, 'comments') and isinstance(self.comments, IterableCollection):
            return self.comments
        self.comments = self.connection.make_request('album', self.id, 'comments')
        return self.comments

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.title.encode('utf8')


class Artist(object):
    def __init__(self, connection, artist):
        self.connection = connection
        self.__dict__.update(artist)

    def get_top(self):
        if hasattr(self, 'top') and isinstance(self.top, IterableCollection):
            return self.top
        self.top = self.connection.make_request('artist', self.id, 'top')
        return self.top

    def get_albums(self):
        if hasattr(self, 'albums') and isinstance(self.albums, IterableCollection):
            return self.albums
        self.albums = self.connection.make_request('artist', self.id, 'albums')
        return self.albums

    def get_fans(self):
        if hasattr(self, 'fans') and isinstance(self.fans, IterableCollection):
            return self.fans
        self.fans = self.connection.make_request('artist', self.id, 'fans')
        return self.fans

    def get_comments(self):
        if hasattr(self, 'comments') and isinstance(self.comments, IterableCollection):
            return self.comments
        self.comments = self.connection.make_request('artist', self.id, 'comments')
        return self.comments

    def get_related(self):
        if hasattr(self, 'related') and isinstance(self.related, IterableCollection):
            return self.related
        self.related = self.connection.make_request('artist', self.id, 'related')
        return self.related

    def get_radio(self):
        if hasattr(self, 'radio') and isinstance(self.radio, IterableCollection):
            return self.radio
        self.radio = self.connection.make_request('artist', self.id, 'radio')
        return self.radio

    def get_playlists(self):
        if hasattr(self, 'playlists') and isinstance(self.playlists, IterableCollection):
            return self.playlists
        self.playlists = self.connection.make_request('artist', self.id, 'playlists')
        return self.playlists

    def get_track(self):
        return self.connection.make_request_streaming(self)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name.encode('utf8')


class Chart(object):
    def __init__(self, connection):
        self.connection = connection

    def get_tracks(self):
        self.tracks = self.connection.make_request('chart', 0, 'tracks')
        return self.tracks

    def get_albums(self):
        self.albums = self.connection.make_request('chart', 0, 'albums')
        return self.albums

    def get_artists(self):
        self.artists = self.connection.make_request('chart', 0, 'artists')
        return self.artists

    def get_playlists(self):
        self.playlists = self.connection.make_request('chart', 0, 'playlists')
        return self.playlists

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Chart"


class Comment(object):
    def __init__(self, connection, comment):
        self.connection = connection
        self.__dict__.update(comment)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.text.encode('utf8')


class Genre(object):
    def __init__(self, connection, genre):
        self.connection = connection
        self.__dict__.update(genre)

    def get_artists(self):
        if hasattr(self, 'artists') and isinstance(self.artists, IterableCollection):
            return self.artists
        self.artists = self.connection.make_request('genre', self.id, 'artists')
        return self.artists

    def get_radios(self):
        if hasattr(self, 'radios') and isinstance(self.radios, IterableCollection):
            return self.radios
        self.radios = self.connection.make_request('genre', self.id, 'radios')
        return self.radios

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name.encode('utf8')


class Playlist(object):
    def __init__(self, connection, playlist):
        self.connection = connection
        self.__dict__.update(playlist)
        self._tracks_retrieved = False

    def get_tracks(self):
        if not self._tracks_retrieved:
            self.tracks = self.connection.make_request('playlist', self.id, 'tracks')
            self._tracks_retrieved = True
        return self.tracks

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.title.encode('utf8')


class Radio(object):
    def __init__(self, connection, radio):
        self.connection = connection
        self.__dict__.update(radio)

    def get_tracks(self):
        if hasattr(self, 'tracks') and isinstance(self.tracks, IterableCollection):
            return self.tracks
        self.tracks = self.connection.make_request('radio', self.id, 'tracks')
        return self.tracks

    def get_track(self):
        return self.connection.make_request_streaming(self)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.title.encode('utf8')


class Track(object):
    def __init__(self, connection, track):
        self.connection = connection
        self.__dict__.update(track)

    def get_url(self):
        if hasattr(self, 'url'):
            return self.url
        self.url = self.connection.make_request_streaming(self)
        return self.url

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.title.encode('utf8')


class User(object):
    def __init__(self, connection, user):
        self.connection = connection
        self.__dict__.update(user)

    def get_albums(self):
        if hasattr(self, 'albums') and isinstance(self.albums, IterableCollection):
            return self.albums
        self.albums = self.connection.make_request('user', self.id, 'albums')
        return self.albums

    def get_artists(self):
        if hasattr(self, 'artists') and isinstance(self.artists, IterableCollection):
            return self.artists
        self.artists = self.connection.make_request('user', self.id, 'artists')
        return self.artists

    def get_charts(self):
        if hasattr(self, 'charts') and isinstance(self.charts, IterableCollection):
            return self.charts
        self.charts = self.connection.make_request('user', self.id, 'charts')
        return self.charts

    def get_flow(self):
        if hasattr(self, 'flow') and isinstance(self.flow, IterableCollection):
            return self.flow
        self.flow = self.connection.make_request('user', self.id, 'flow')
        return self.flow

    def get_history(self):
        if hasattr(self, 'history') and isinstance(self.history, IterableCollection):
            return self.history
        self.history = self.connection.make_request('user', self.id, 'history')
        return self.history

    def get_playlists(self):
        if hasattr(self, 'playlists') and isinstance(self.playlists, IterableCollection):
            return self.playlists
        self.playlists = self.connection.make_request('user', self.id, 'playlists')
        return self.playlists

    def get_radios(self):
        if hasattr(self, 'radios') and isinstance(self.radios, IterableCollection):
            return self.radios
        self.radios = self.connection.make_request('user', self.id, 'radios')
        return self.radios

    def get_tracks(self):
        if hasattr(self, 'tracks') and isinstance(self.tracks, IterableCollection):
            return self.tracks
        self.tracks = self.connection.make_request('user', self.id, 'tracks')
        return self.tracks

    def get_recommendations(self):
        if hasattr(self, 'recommendations') and isinstance(self.recommendations, Recommendations):
            return self.recommendations
        self.recommendations = Recommendations(self)
        return self.recommendations

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name.encode('utf8')


class Recommendations(object):
    def __init__(self, user):
        self.user = user
        self.connection = self.user.connection

    def get_albums(self):
        if hasattr(self, 'albums') and isinstance(self.albums, IterableCollection):
            return self.albums
        self.albums = self.connection.make_request('user', self.user.id, 'recommendations/albums')
        return self.albums

    def get_artists(self):
        if hasattr(self, 'artists') and isinstance(self.artists, IterableCollection):
            return self.artists
        self.artists = self.connection.make_request('user', self.user.id, 'recommendations/artists')
        return self.artists

    def get_tracks(self):
        if hasattr(self, 'tracks') and isinstance(self.tracks, IterableCollection):
            return self.tracks
        self.tracks = self.connection.make_request('user', self.user.id, 'recommendations/tracks')
        return self.tracks

    def get_playlists(self):
        if hasattr(self, 'playlists') and isinstance(self.playlists, IterableCollection):
            return self.playlists
        self.playlists = self.connection.make_request('user', self.user.id, 'recommendations/playlists')
        return self.playlists

    def get_radios(self):
        if hasattr(self, 'radios') and isinstance(self.radios, IterableCollection):
            return self.radios
        self.radios = self.connection.make_request('user', self.user.id, 'recommendations/radios')
        return self.radios

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Recommendations for %s" % self.user
