import requests
import hashlib
import json
from kodi.service import ContainerAwareInterface


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


class Connection(ContainerAwareInterface):
    """Connection class holds user login and password. It is responsible for obtaining access_token automatically when a request is made"""
    _API_BASE_URL = "http://api.deezer.com/2.0/{service}/{id}/{method}"
    _API_BASE_STREAMING_URL = "http://tv.deezer.com/smarttv/streaming.php"
    _API_AUTH_URL = "http://tv.deezer.com/smarttv/authentication.php"

    def __init__(self, username, password):
        self._username = self._password = self._access_token = None
        self.set_username(username)
        self.set_password(password)
        self._obtain_access_token()


    def set_username(self, username):
        """save username"""
        self._username = username


    def set_password(self, password):
        """save md5 of user password"""
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


    def _obtain_access_token(self):
        """obtain access token by pretending to be a smart tv"""
        if self._username is None or self._password is None:
            raise Exception("Username and password is required")
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


    def _merge_two_dicts(self, x, y):
        """Given two dicts, merge them into a new dict as a shallow copy."""
        z = x.copy()
        z.update(y)
        return z


    def make_request(self, service, id='', method='', parameters={}):
        """make request to the api and return response as a dict"""
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


class Api(ContainerAwareInterface):
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

