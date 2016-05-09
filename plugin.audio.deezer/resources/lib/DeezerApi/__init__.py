import requests
import hashlib
from urlparse import urlparse, parse_qs
import json


def _objectFromType(type, connection, content):
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

	def __init__(self, username = None, password = None):
		print "Initialise Connection"
		self._username = self._password = self._access_token = None
		self.setUsername(username)
		self.setPassword(password)
		self._obtain_access_token()

	"""save username"""
	def setUsername(self, username):
		self._username = username

	"""save md5 of user password"""
	def setPassword(self, password):
		self._password = password
		if self._password is not None:
			md5 = hashlib.md5()
			md5.update(self._password)
			self._password = md5.hexdigest()

	def _objectDecoder(self, dct):
		if 'type' in dct:
			return _objectFromType(dct['type'], self, dct)
		if 'data' in dct:
			return IterableCollection(self, collection=dct)
		return dct

	"""obtain access token by pretending to be a smart tv"""
	def _obtain_access_token(self):
		if self._username is None or self._password is None:
			raise Exception("Username and password is required!")
		r = requests.get(self._API_AUTH_URL, params={
			'login' : self._username,
			'password' : self._password,
			'device' : 'panasonic'
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
	def make_request(self, service, id = '', method = '', parameters = {}):
		baseUrl = self._API_BASE_URL.format(service=service, id=id, method=method)
		print "make_request: %s" % baseUrl
		r = requests.get(baseUrl, params = self._merge_two_dicts(
			{'output' : 'json', 'access_token' : self._access_token}, parameters
		))
		return json.loads(r.text, object_hook=self._objectDecoder)

	def request_streaming_url(self, id='', type=''):
		r = requests.get(self._API_BASE_STREAMING_URL, params = {
			'access_token' : self._access_token,
			("%s_id" % type) : id,
			'device' : 'panasonic'
		})
		if type.startswith('radio') or type.startswith('artist'):
			return json.loads(r.text, object_hook=self._objectDecoder)
		return r.text

	def make_request_streaming(self, deezerObject):
		type = deezerObject.type + "_id"
		r = requests.get(self._API_BASE_STREAMING_URL, params = {
			'access_token' : self._access_token,
			type : deezerObject.id,
			'device' : 'panasonic'
		})
		if type.startswith('radio') or type.startswith('artist'):
			return json.loads(r.text, object_hook=self._objectDecoder)
		return r.text

	def make_request_url(self, url):
		r = requests.get(url)
		return json.loads(r.text, object_hook=self._objectDecoder)


class Api(object):
	def __init__(self, connection):
		print "Initialise Api"
		if connection is None:
			raise Exception("Connection is required!")
		self.connection = connection

	def getUser(self, id = 'me'):
		return self.connection.make_request('user', id)

	def getTrack(self, id = None):
		if id is None:
			raise Exception("Track id is required!")
		return self.connection.make_request('track', id)

	def getArtist(self, id = None):
		if id is None:
			raise Exception("Artist id is required!")
		return self.connection.make_request('artist', id)

	def getAlbum(self, id = None):
		if id is None:
			raise Exception("Album id is required!")
		return self.connection.make_request('album', id)

	def getChart(self):
		return Chart(self.connection)

	def getGenre(self, id = None):
		if id is None:
			raise Exception("Genre id is required!")
		return self.connection.make_request('genre', id)

	def getGenres(self):
		return self.connection.make_request('genre')

	def getRadios(self):
		return self.connection.make_request('radio')

	def getPlaylist(self, id = None):
		if id is None:
			raise Exception("Playlist id is required!")
		return self.connection.make_request('playlist', id)

	def search(self, query=None, type=''):
		if query is None:
			raise Exception("Query is required!")
		return self.connection.make_request('search', id=type, parameters={'q' : query})

	def searchArtist(self, query=None):
		return self.search(query, 'artist')

	def searchAlbum(self, query=None):
		return self.search(query, 'album')

	def searchHistory(self, query=None):
		return self.search(query, 'history')

	def searchPlaylist(self, query=None):
		return self.search(query, 'playlist')

	def searchRadio(self, query=None):
		return self.search(query, 'radio')

	def searchTrack(self, query=None):
		return self.search(query, 'track')

	def getStreamingUrl(self, id=None, type='track'):
		if id is None:
			raise Exception("Object id is required")
		return self.connection.request_streaming_url(id, type)


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
			self._update_info(total = collection.total, _prev = collection._prev, _next = collection._next)
		else:
			if 'data' not in collection:
				raise Exception("Collection is not iterable!")
			self._append_data(collection['data'])
			self._update_info(total = collection.get('total', self.data_length), _prev = collection.get('prev', None), _next = collection.get('next', None))

	def _retrieve_item(self, index):
		#if we have the item with such index
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

	def getTracks(self):
		if hasattr(self, 'tracks') and isinstance(self.tracks, IterableCollection):
			return self.tracks
		self.tracks = self.connection.make_request('album', self.id, 'tracks')
		return self.tracks

	def getFans(self):
		if hasattr(self, 'fans') and isinstance(self.fans, IterableCollection):
			return self.fans
		self.fans = self.connection.make_request('album', self.id, 'fans')
		return self.fans

	def getComments(self):
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

	def getTop(self):
		if hasattr(self, 'top') and isinstance(self.top, IterableCollection):
			return self.top
		self.top = self.connection.make_request('artist', self.id, 'top')
		return self.top

	def getAlbums(self):
		if hasattr(self, 'albums') and isinstance(self.albums, IterableCollection):
			return self.albums
		self.albums = self.connection.make_request('artist', self.id, 'albums')
		return self.albums

	def getFans(self):
		if hasattr(self, 'fans') and isinstance(self.fans, IterableCollection):
			return self.fans
		self.fans = self.connection.make_request('artist', self.id, 'fans')
		return self.fans

	def getComments(self):
		if hasattr(self, 'comments') and isinstance(self.comments, IterableCollection):
			return self.comments
		self.comments = self.connection.make_request('artist', self.id, 'comments')
		return self.comments

	def getRelated(self):
		if hasattr(self, 'related') and isinstance(self.related, IterableCollection):
			return self.related
		self.related = self.connection.make_request('artist', self.id, 'related')
		return self.related

	def getRadio(self):
		if hasattr(self, 'radio') and isinstance(self.radio, IterableCollection):
			return self.radio
		self.radio = self.connection.make_request('artist', self.id, 'radio')
		return self.radio

	def getPlaylists(self):
		if hasattr(self, 'playlists') and isinstance(self.playlists, IterableCollection):
			return self.playlists
		self.playlists = self.connection.make_request('artist', self.id, 'playlists')
		return self.playlists

	def getTrack(self):
		return self.connection.make_request_streaming(self)

	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.name.encode('utf8')




class Chart(object):
	def __init__(self, connection):
		self.connection = connection

	def getTracks(self):
		self.tracks = self.connection.make_request('chart', 0, 'tracks')
		return self.tracks

	def getAlbums(self):
		self.albums = self.connection.make_request('chart', 0, 'albums')
		return self.albums

	def getArtists(self):
		self.artists = self.connection.make_request('chart', 0, 'artists')
		return self.artists

	def getPlaylists(self):
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

	def getArtists(self):
		if hasattr(self, 'artists') and isinstance(self.artists, IterableCollection):
			return self.artists
		self.artists = self.connection.make_request('genre', self.id, 'artists')
		return self.artists

	def getRadios(self):
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

	def getTracks(self):
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

	def getTracks(self):
		if hasattr(self, 'tracks') and isinstance(self.tracks, IterableCollection):
			return self.tracks
		self.tracks = self.connection.make_request('radio', self.id, 'tracks')
		return self.tracks

	def getTrack(self):
		return self.connection.make_request_streaming(self)

	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.title.encode('utf8')


class Track(object):
	def __init__(self, connection, track):
		self.connection = connection
		self.__dict__.update(track)

	def getUrl(self):
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

	def getAlbums(self):
		if hasattr(self, 'albums') and isinstance(self.albums, IterableCollection):
			return self.albums
		self.albums = self.connection.make_request('user', self.id, 'albums')
		return self.albums

	def getArtists(self):
		if hasattr(self, 'artists') and isinstance(self.artists, IterableCollection):
			return self.artists
		self.artists = self.connection.make_request('user', self.id, 'artists')
		return self.artists

	def getCharts(self):
		if hasattr(self, 'charts') and isinstance(self.charts, IterableCollection):
			return self.charts
		self.charts = self.connection.make_request('user', self.id, 'charts')
		return self.charts

	def getFlow(self):
		if hasattr(self, 'flow') and isinstance(self.flow, IterableCollection):
			return self.flow
		self.flow = self.connection.make_request('user', self.id, 'flow')
		return self.flow

	def getHistory(self):
		if hasattr(self, 'history') and isinstance(self.history, IterableCollection):
			return self.history
		self.history = self.connection.make_request('user', self.id, 'history')
		return self.history

	def getPlaylists(self):
		if hasattr(self, 'playlists') and isinstance(self.playlists, IterableCollection):
			return self.playlists
		self.playlists = self.connection.make_request('user', self.id, 'playlists')
		return self.playlists

	def getRadios(self):
		if hasattr(self, 'radios') and isinstance(self.radios, IterableCollection):
			return self.radios
		self.radios = self.connection.make_request('user', self.id, 'radios')
		return self.radios

	def getTracks(self):
		if hasattr(self, 'tracks') and isinstance(self.tracks, IterableCollection):
			return self.tracks
		self.tracks = self.connection.make_request('user', self.id, 'tracks')
		return self.tracks

	def getRecommendations(self):
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

	def getAlbums(self):
		if hasattr(self, 'albums') and isinstance(self.albums, IterableCollection):
			return self.albums
		self.albums = self.connection.make_request('user', self.user.id, 'recommendations/albums')
		return self.albums

	def getArtists(self):
		if hasattr(self, 'artists') and isinstance(self.artists, IterableCollection):
			return self.artists
		self.artists = self.connection.make_request('user', self.user.id, 'recommendations/artists')
		return self.artists

	def getTracks(self):
		if hasattr(self, 'tracks') and isinstance(self.tracks, IterableCollection):
			return self.tracks
		self.tracks = self.connection.make_request('user', self.user.id, 'recommendations/tracks')
		return self.tracks

	def getPlaylists(self):
		if hasattr(self, 'playlists') and isinstance(self.playlists, IterableCollection):
			return self.playlists
		self.playlists = self.connection.make_request('user', self.user.id, 'recommendations/playlists')
		return self.playlists

	def getRadios(self):
		if hasattr(self, 'radios') and isinstance(self.radios, IterableCollection):
			return self.radios
		self.radios = self.connection.make_request('user', self.user.id, 'recommendations/radios')
		return self.radios

	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return "Recommendations for %s" % self.user