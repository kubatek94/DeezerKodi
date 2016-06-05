import requests
import hashlib
import json


def _object_from_type(type, connection, content):
    if type == "album":
        return Album(connection, content)
    if type == "artist":
        return Artist(connection, content)
    if type == "comment":
        return Comment(connection, content)
    if type == "genre":
        return Genre(connection, content)
    if type == "playlist":
        return Playlist(connection, content)
    if type == "radio":
        return Radio(connection, content)
    if type == "track":
        return Track(connection, content)
    if type == "user":
        return User(connection, content)


class Connection(object):
    """Connection class holds user login and password. It is responsible for obtaining access_token automatically when a request is made"""
    _API_BASE_URL = "http://api.deezer.com/2.0/{service}/{id}/{method}"
    _API_BASE_STREAMING_URL = "http://tv.deezer.com/smarttv/streaming.php"
    _API_AUTH_URL = "http://tv.deezer.com/smarttv/authentication.php"

    def __init__(self, username=None, password=None):
        self._username = self._password = self._access_token = None
        self.set_username(username)
        self.set_password(password)
        self._obtain_access_token()

    """save username"""
    def set_username(self, username):
        self._username = username

    """save md5 of user password"""
    def set_password(self, password):
        self._password = password
        if self._password is not None:
            md5 = hashlib.md5()
            md5.update(self._password)
            self._password = md5.hexdigest()

    def _object_decoder(self, dct):
        if 'type' in dct:
            return _object_from_type(dct['type'], self, dct)
        if 'data' in dct:
            return IterableCollection(self, collection=dct)
        return dct

    """obtain access token by pretending to be a smart tv"""
    def _obtain_access_token(self):
        if self._username is None or self._password is None:
            raise Exception("Username and password is required!")
        r = requests.get(self._API_AUTH_URL, params={
            'login': self._username,
            'password': self._password,
            'device': 'panasonic'
        })
        response = r.json()
        if 'access_token' in response:
            self._access_token = response['access_token']
        else:
            if 'error' in response:
                error = response['error']
                raise Exception(error['message'])
            else:
                raise Exception("Could not obtain access token!")

    """Given two dicts, merge them into a new dict as a shallow copy."""
    def _merge_two_dicts(self, x, y):
        z = x.copy()
        z.update(y)
        return z

    """make request to the api and return response as a dict"""
    def make_request(self, service, id='', method='', parameters={}):
        base_url = self._API_BASE_URL.format(service=service, id=id, method=method)
        print "make_request: %s" % base_url
        r = requests.get(base_url, params=self._merge_two_dicts(
            {'output': 'json', 'access_token': self._access_token}, parameters
        ))
        return json.loads(r.text, object_hook=self._object_decoder)

    def make_request_url(self, url):
        r = requests.get(url)
        return json.loads(r.text, object_hook=self._object_decoder)

    def make_request_streaming_custom(self, id='', type=''):
        r = requests.get(self._API_BASE_STREAMING_URL, params={
            'access_token': self._access_token,
            ("%s_id" % type): id,
            'device': 'panasonic'
        })
        if type.startswith('radio') or type.startswith('artist'):
            return json.loads(r.text, object_hook=self._object_decoder)
        return r.text

    def make_request_streaming(self, deezer_object):
        return self.make_request_streaming_custom(deezer_object.id, deezer_object.type)


class Api(object):
    def __init__(self, connection):
        if connection is None:
            raise Exception("Connection is required!")
        self.connection = connection

    def get_user(self, id='me'):
        return self.connection.make_request('user', id)

    def get_track(self, id=None):
        if id is None:
            raise Exception("Track id is required!")
        return self.connection.make_request('track', id)

    def get_artist(self, id=None):
        if id is None:
            raise Exception("Artist id is required!")
        return self.connection.make_request('artist', id)

    def get_album(self, id=None):
        if id is None:
            raise Exception("Album id is required!")
        return self.connection.make_request('album', id)

    def get_chart(self):
        return Chart(self.connection)

    def get_genre(self, id=None):
        if id is None:
            raise Exception("Genre id is required!")
        return self.connection.make_request('genre', id)

    def get_genres(self):
        return self.connection.make_request('genre')

    def get_radios(self):
        return self.connection.make_request('radio')

    def get_playlist(self, id=None):
        if id is None:
            raise Exception("Playlist id is required!")
        return self.connection.make_request('playlist', id)

    def search(self, query=None, type=''):
        if query is None:
            raise Exception("Query is required!")
        return self.connection.make_request('search', id=type, parameters={'q': query})

    def search_artist(self, query=None):
        return self.search(query, 'artist')

    def search_album(self, query=None):
        return self.search(query, 'album')

    def search_history(self, query=None):
        return self.search(query, 'history')

    def search_playlist(self, query=None):
        return self.search(query, 'playlist')

    def search_radio(self, query=None):
        return self.search(query, 'radio')

    def search_track(self, query=None):
        return self.search(query, 'track')

    def get_streaming_url(self, id=None, type='track'):
        return self.connection.make_request_streaming_custom(id, type)


class IterableCollection(object):
    def __init__(self, connection, collection):
        self.connection = connection
        self.data = []
        self._iterable_index = 0
        self._load_collection(collection)

    def _append_data(self, data):
        self.data.extend(data)
        self.data_length = len(self.data)

    def _update_info(self, total=0, _prev=None, _next=None):
        self.total = total
        self._prev = _prev
        self._next = _next

    def _load_collection(self, collection):
        if isinstance(collection, list):
            self._append_data(collection)
            self._update_info(total=self.data_length)
        elif isinstance(collection, IterableCollection):
            self._append_data(collection.data)
            self._update_info(total=collection.total, _prev=collection._prev, _next=collection._next)
        else:
            if 'data' not in collection:
                raise Exception("Collection is not iterable!")
            self._append_data(collection['data'])
            self._update_info(total=collection.get('total', self.data_length), _prev=collection.get('prev', None),
                              _next=collection.get('next', None))

    def _retrieve_item(self, index):
        # if we have the item with such index
        if index < self.data_length:
            return self.data[index]
        if self._next is not None:
            self._load_collection(self.connection.make_request_url(self._next))
            return self._retrieve_item(index)
        return None

    def __len__(self):
        return self.total

    def __getitem__(self, index):
        item = self._retrieve_item(index)
        if item is None:
            raise IndexError("Index is out of bounds!")
        return item

    def __iter__(self):
        self._iterable_index = 0
        return self

    def next(self):
        item = self._retrieve_item(self._iterable_index)
        self._iterable_index += 1
        if item is None:
            raise StopIteration()
        return item

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.data)


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
