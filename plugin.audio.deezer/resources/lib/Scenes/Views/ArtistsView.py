from .View import View
from .TracksView import TracksView
from .AlbumsView import AlbumsView
from .PlaylistsView import PlaylistsView

import os
import xbmc
import xbmcgui
import xbmcplugin


class ArtistTopView(View):
	def __init__(self, scene, viewRouter, parentView = None):
		super(ArtistTopView, self).__init__(scene, viewRouter, "artisttop", parentView)
		self.lazyTop = None

	def _getLazyTop(self):
		#try to get lazy top from the parent if none are set
		if self.lazyTop is None:
			self.lazyTop = self.parentView.getLazyTop()
		return self.lazyTop

	def _showTop(self):
		self.topTracks = self._getLazyTop()()
		listItems = []

		for i in range(0, len(self.topTracks)):
			try:
				track = self.topTracks[i]
				listItem = xbmcgui.ListItem("%s - %s" % (track.artist.name, track.title), thumbnailImage=track.album.cover_big)
				listItem.setProperty('IsPlayable', 'true')
				listItem.setArt({'fanart': self.scene.sceneRouter.fanartPath})
				listItems.append((self.getUrl("/tracks/%d" % track.id), listItem, False))
			except:
				pass
		xbmcplugin.addDirectoryItems(self.scene.sceneRouter.addonHandle, listItems)
		xbmcplugin.setContent(self.scene.sceneRouter.addonHandle, 'songs')

	def show(self):
		self._showTop()


class ArtistMenuView(View):
	def __init__(self, scene, viewRouter, parentView = None):
		super(ArtistMenuView, self).__init__(scene, viewRouter, "artistmenu", parentView)

	def getLazyAlbums(self):
		artist = self.parentView.getArtist()
		return lambda:artist.getAlbums()

	def getLazyPlaylists(self):
		artist = self.parentView.getArtist()
		return lambda:artist.getPlaylists()

	def getLazyRadio(self):
		artist = self.parentView.getArtist()
		return lambda:artist.getRadio()

	def getLazyTop(self):
		artist = self.parentView.getArtist()
		return lambda:artist.getTop()

	#to display the radio as tracks
	def getListItems(self):
		artist = self.parentView.getArtist()
		listItems = []
		for track in artist.getRadio():
			try:
				listItem = xbmcgui.ListItem("%s - %s" % (track.artist.name, track.title), thumbnailImage=track.album.cover_big)
				listItem.setProperty('IsPlayable', 'true')
				listItem.setArt({'fanart': track.artist.picture_big})
				self.addItemTrackInfo(listItem, track)
				listItems.append((self.getUrl("/%d" % track.id), listItem, False))
			except:
				pass
		return listItems

	def _showMenu(self):
		items = {
			3000 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.sceneRouter.imagesPath, "genre-%s.png" % self.scene.sceneRouter.color)),
				"url" : self.getUrl("/artisttop")
			},
			3001 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.sceneRouter.imagesPath, "myalbums-%s.png" % self.scene.sceneRouter.color)),
				"url" : self.getUrl("/albums")
			},
			3002 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.sceneRouter.imagesPath, "myplaylists-%s.png" % self.scene.sceneRouter.color)),
				"url" : self.getUrl("/playlists")
			},
			3003 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.sceneRouter.imagesPath, "radiochannels-%s.png" % self.scene.sceneRouter.color)),
				"url" : self.getUrl("/tracks")
			}
		}
		artist = self.parentView.getArtist()
		listItems = []
		for item in items:
			try:
				listItem = xbmcgui.ListItem(self.scene.sceneRouter.language(item), iconImage=items[item]["image"])
				listItem.setArt({'fanart': artist.picture_big})
				listItems.append((items[item]["url"], listItem, True))
			except:
				pass
		xbmcplugin.addDirectoryItems(self.scene.sceneRouter.addonHandle, listItems)

	def show(self):
		print "Show MenuView"
		self._showMenu()



class ArtistsView(View):
	def __init__(self, scene, viewRouter, parentView = None):
		super(ArtistsView, self).__init__(scene, viewRouter, "artists", parentView)
		self.lazyArtists = None

	def setLazyArtists(self, lazyArtists):
		self.lazyArtists = lazyArtists

	def _getLazyArtists(self):
		#try to get lazy artists from the parent if none are set
		if self.lazyArtists is None:
			self.lazyArtists = self.parentView.getLazyArtists()
		return self.lazyArtists

	def getArtist(self):
		self.artists = self._getLazyArtists()()
		return self.artists[self.id]

	def _showArtists(self):
		self.artists = self._getLazyArtists()()
		listItems = []

		for i in range(0, len(self.artists)):
			try:
				artist = self.artists[i]
				listItem = xbmcgui.ListItem(artist.name, thumbnailImage=artist.picture_big)
				listItem.setArt({'fanart': self.scene.sceneRouter.fanartPath})
				listItems.append((self.getUrl("/%d/artistmenu" % i), listItem, True))
			except:
				pass
		xbmcplugin.addDirectoryItems(self.scene.sceneRouter.addonHandle, listItems)

	def show(self):
		print "Show ArtistsView"
		self._showArtists()