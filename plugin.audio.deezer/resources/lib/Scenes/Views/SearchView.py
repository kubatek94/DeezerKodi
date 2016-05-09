from .View import View
from ...DeezerApi import Track, Album, Artist

import os
import xbmc
import xbmcgui
import xbmcplugin

class SearchView(View):
	def __init__(self, scene, viewRouter, parentView = None):
		super(SearchView, self).__init__(scene, viewRouter, "search", parentView)

	def _getQuery(self):
		dialog = xbmcgui.Dialog()
		return dialog.input(self.scene.sceneRouter.language(self.id))

	def _search(self, query):
		#check if query is in the cache first
		if self.scene.cache.has(query):
			return self.scene.cache.get(query)

		#otherwise do the search
		search = {
			3010 : lambda q: self.scene.sceneRouter.api.search(query=q),
			3011 : lambda q: self.scene.sceneRouter.api.searchArtist(query=q),
			3012 : lambda q: self.scene.sceneRouter.api.searchAlbum(query=q),
			3013 : lambda q: self.scene.sceneRouter.api.searchTrack(query=q)
		}
		if self.id in search:
			results = search[self.id](query)
			#and put the result in the cache
			self.scene.cache.set(query, results)
			return results
		return None

	def getLazyAlbums(self):
		self.query = ''
		#check if query isn't in the url already
		urlQuery = self.scene.sceneRouter.getQuery().split("=")
		if "searchQuery" in urlQuery:
			print "re-using query"
			self.query = urlQuery[1]
		else:
			self.query = self._getQuery()
			self.scene.sceneRouter.setQuery("searchQuery=%s" % self.query)

		if self.query != '':
			results = self._search(self.query)
			return lambda:results
		return lambda:[]

	def getLazyArtists(self):
		self.query = ''
		#check if query isn't in the url already
		urlQuery = self.scene.sceneRouter.getQuery().split("=")
		if "searchQuery" in urlQuery:
			self.query = urlQuery[1]
		else:
			self.query = self._getQuery()
			self.scene.sceneRouter.setQuery("searchQuery=%s" % self.query)

		if self.query != '':
			results = self._search(self.query)
			return lambda:results
		return lambda:[]

	def getListItems(self):
		self.query = ''
		#check if query isn't in the url already
		urlQuery = self.scene.sceneRouter.getQuery().split("=")
		if "searchQuery" in urlQuery:
			self.query = urlQuery[1]
		else:
			self.query = self._getQuery()

		if self.query != '':
			results = self._search(self.query)
			url = self.getUrl()

			listItems = []
			for track in results:
				try:
					listItem = xbmcgui.ListItem("%s - %s" % (track.artist.name, track.title), thumbnailImage=track.album.cover_big)
					listItem.setProperty('IsPlayable', 'true')
					listItem.setArt({'fanart': track.artist.picture_big})
					self.addItemTrackInfo(listItem, track)
					listItems.append((self.getUrl("/%d?searchQuery=%s" % (track.id, self.query)), listItem, False))
				except:
					pass
			return listItems
		return []

	#to display menu
	def _showSearchMenu(self):
		items = {
			3010 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.sceneRouter.imagesPath, "search-%s.png" % self.scene.sceneRouter.color)),
				"url" : self.getUrl('/3010/tracks') #search all
			},
			3011 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.sceneRouter.imagesPath, "myartists-%s.png" % self.scene.sceneRouter.color)),
				"url" : self.getUrl('/3011/artists') #search artist 
			},
			3012 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.sceneRouter.imagesPath, "myalbums-%s.png" % self.scene.sceneRouter.color)),
				"url" : self.getUrl('/3012/albums') #search album
			},
			3013 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.sceneRouter.imagesPath, "search-%s.png" % self.scene.sceneRouter.color)),
				"url" : self.getUrl('/3013/tracks') #search track
			}
		}
		listItems = []
		for item in items:
			listItem = xbmcgui.ListItem(self.scene.sceneRouter.language(item), iconImage=items[item]["image"])
			listItem.setArt({'fanart': self.scene.sceneRouter.fanartPath})
			listItems.append((items[item]["url"], listItem, True))
		xbmcplugin.addDirectoryItems(self.scene.sceneRouter.addonHandle, listItems)

	def show(self):
		self._showSearchMenu()
			