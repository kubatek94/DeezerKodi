from .View import View
from .TracksView import TracksView

import xbmcgui
import xbmcplugin

class PlaylistsView(View):
	def __init__(self, scene, viewRouter, parentView = None):
		super(PlaylistsView, self).__init__(scene, viewRouter, "playlists", parentView)
		self.lazyPlaylists = None

	def setLazyPlaylists(self, lazyPlaylists):
		self.lazyPlaylists = lazyPlaylists

	def _getLazyPlaylists(self):
		#try to get lazy playlists from the parent if none are set
		if self.lazyPlaylists is None:
			self.lazyPlaylists = self.parentView.getLazyPlaylists()
		return self.lazyPlaylists

	def _showPlaylists(self):
		self.playlists = self._getLazyPlaylists()()
		listItems = []

		for i in range(0, len(self.playlists)):
			try:
				playlist = self.playlists[i]
				listItem = xbmcgui.ListItem(playlist.title, thumbnailImage=playlist.picture_big)
				listItem.setArt({'fanart': self.scene.sceneRouter.fanartPath})
				listItems.append((self.getUrl("/%d/tracks" % i), listItem, True))
			except:
				pass
		xbmcplugin.addDirectoryItems(self.scene.sceneRouter.addonHandle, listItems)

	def getListItems(self):
		self.playlists = self._getLazyPlaylists()()
		playlist = self.playlists[self.id]
		listItems = []

		for track in playlist.getTracks():
			try:
				listItem = xbmcgui.ListItem("%s - %s" % (track.artist.name, track.title), thumbnailImage=track.album.cover_big)
				listItem.setProperty('IsPlayable', 'true')
				listItem.setArt({'fanart': playlist.picture_big})
				self.addItemTrackInfo(listItem, track)
				listItems.append((self.getUrl("/%d" % track.id), listItem, False))
			except:
				pass
		return listItems

	def show(self):
		print "Show PlaylistsView"
		self._showPlaylists()