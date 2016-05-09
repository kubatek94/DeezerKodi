from .View import View
from .TracksView import TracksView

import xbmcgui
import xbmcplugin

class AlbumsView(View):
	def __init__(self, scene, viewRouter, parentView = None):
		super(AlbumsView, self).__init__(scene, viewRouter, "albums", parentView)
		self.lazyAlbums = None

	def setLazyAlbums(self, lazyAlbums):
		self.lazyAlbums = lazyAlbums

	def _getLazyAlbums(self):
		#try to get lazy albums from the parent if none are set
		if self.lazyAlbums is None:
			self.lazyAlbums = self.parentView.getLazyAlbums()
		return self.lazyAlbums

	def _showAlbums(self):
		self.albums = self._getLazyAlbums()()
		listItems = []

		for i in range(0, len(self.albums)):
			try:
				album = self.albums[i]
				listItem = xbmcgui.ListItem(album.title, thumbnailImage=album.cover_big)
				listItem.setArt({'fanart': self.scene.sceneRouter.fanartPath})
				listItems.append((self.getUrl("/%d/tracks" % i), listItem, True))
			except:
				pass
		xbmcplugin.addDirectoryItems(self.scene.sceneRouter.addonHandle, listItems)

	def getListItems(self):
		self.albums = self._getLazyAlbums()()
		album = self.albums[self.id]
		listItems = []

		for track in album.getTracks():
			try:
				listItem = xbmcgui.ListItem("%s - %s" % (track.artist.name, track.title), thumbnailImage=album.cover_big)
				listItem.setProperty('IsPlayable', 'true')
				listItem.setArt({'fanart': self.scene.sceneRouter.fanartPath})
				self.addItemTrackInfo(listItem, track)
				listItems.append((self.getUrl("/%d" % track.id), listItem, False))
			except:
				pass
		return listItems

	def show(self):
		print "Show AlbumsView"
		self._showAlbums()