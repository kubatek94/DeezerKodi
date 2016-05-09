import urlparse
import xbmcplugin
import xbmc
import xbmcgui
import xbmcaddon
import os

from .MainScene import MainScene
from .RadioChannelsScene import RadioChannelsScene
from .MyPlaylistsScene import MyPlaylistsScene
from .MyAlbumsScene import MyAlbumsScene
from .MyArtistsScene import MyArtistsScene
from .SearchScene import SearchScene
from .ChartScene import ChartScene

from ..DeezerApi import Connection, Api
from ..cache import Cache

class SceneRouter(object):
	def __init__(self):
		print "Initialised SceneRouter"
		self.addon = xbmcaddon.Addon('plugin.audio.deezer')
		self.language  = self.addon.getLocalizedString
		self.addonPath = self.addon.getAddonInfo('path')
		self.resourcesPath = xbmc.translatePath(os.path.join(self.addonPath, 'resources'))
		self.imagesPath = xbmc.translatePath(os.path.join(self.resourcesPath, 'img'))
		self.fanartPath = xbmc.translatePath(os.path.join(self.addonPath, 'fanart.jpg'))
		self.color = "white"
		self.cache = Cache("deezerapi")

		self.scenes = {
			"main" : lambda: MainScene(self),
			"chart" : lambda: ChartScene(self),
			"radiochannels" : lambda: RadioChannelsScene(self),
			"playlists" : lambda: MyPlaylistsScene(self),
			"albums" : lambda: MyAlbumsScene(self),
			"artists" : lambda: MyArtistsScene(self),
			"search" : lambda: SearchScene(self)
		}

	#url consists of the path and query parts
	def getUrl(self, scene = None):
		return {'path':self.getPath(scene), 'query':self.getQuery(scene)}

	def setUrl(self, url):
		fullUrl = "%s?%s" % (url['path'], url['query'])
		self.args['path'] = [fullUrl]

	#path consists of e.g. /search/3000/tracks/1
	def getPath(self, scene = None):
		path = None
		if scene is None:
			path = self.args.get('path', ["/"])[0]
		else:
			path = self.args.get('path', ["/%s" % scene.name])[0]
		return path.split('?')[0]

	def setPath(self, path):
		url = {'path':path, 'query':self.getQuery()}
		self.setUrl(url)

	def setQuery(self, query):
		url = {'path':self.getPath(), 'query':query}
		self.setUrl(url)

	#query consists of e.g. searchQuery=Hello&foo=bar
	def getQuery(self, scene = None):
		path = None
		if scene is None:
			path = self.args.get('path', ["/"])[0]
		else:
			path = self.args.get('path', ["/%s" % scene.name])[0]
		s = path.split('?')
		if len(s) > 1:
			return s[1]
		else:
			return ''

	def notification(self, header, message):
		command = 'Notification(%s, %s)' % (header, message)
		xbmc.executebuiltin(command)

	def _hasCredentials(self):
		self.username = self.addon.getSetting('username')
		self.password = self.addon.getSetting('password')
		if self.username != "" and self.password != "":
			return self.connect()
		else:
			return False

	def _checkCredentials(self):
		if not self._hasCredentials():
			dialog = xbmcgui.Dialog()

			while True:
				self.addon.openSettings()
				if not self._hasCredentials():
					# Sign in required | Do you want to try again, or exit Deezer? | Try again | Exit
					tryAgain = dialog.yesno(self.language(2006), self.language(2008), yeslabel=self.language(2009), nolabel=self.language(2010))
					if not tryAgain:
						return False
				else:
					return True
		return True

	def getUser(self):
		self.user = self.cache.get('user', defaultProducer = lambda: self.api.getUser())
		return self.user

	def connect(self):
		try:
			self.connection = self.cache.get('connection', defaultProducer = lambda: Connection(self.username, self.password))
		except Exception as e:
			self.notification("Could not sign in", e)
			return False
		return True

	def route(self, argv):
		self.baseUrl = argv[0]
		self.addonHandle = int(argv[1])
		self.args = urlparse.parse_qs(argv[2][1:])

		#print "baseUrl: %s" % self.baseUrl
		#print "addonHandle: %d" % self.addonHandle
		print "args: %s" % self.args

		isSignedIn = self._checkCredentials()

		if isSignedIn:
			self.api = self.cache.get('api', defaultProducer = lambda: Api(self.connection))

			#xbmcplugin.setContent(self.addonHandle, 'audio')
			sceneType = self.args.get('scene', ['main'])[0]
			scene = self.scenes.get(sceneType, None)

			if scene is not None:
				scene()

		print "endOfDirectory!"
		xbmcplugin.endOfDirectory(self.addonHandle, succeeded=isSignedIn)
		self.cache.save()