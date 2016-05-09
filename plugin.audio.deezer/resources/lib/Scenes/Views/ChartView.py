from .View import View
from .TracksView import TracksView
from .AlbumsView import AlbumsView
from .PlaylistsView import PlaylistsView

import os
import xbmc
import xbmcgui
import xbmcplugin

class ChartView(View):
	def __init__(self, scene, viewRouter, parentView = None):
		super(ChartView, self).__init__(scene, viewRouter, "chart", parentView)
		self.lazyChart = None

	def setLazyChart(self, lazyChart):
		self.lazyChart = lazyChart

	def _getLazyChart(self):
		#try to get lazy chart from the parent if none are set
		if self.lazyChart is None:
			self.lazyChart = self.parentView.getLazyChart()
		return self.lazyChart

	#to display the albums
	def getLazyAlbums(self):
		chart = self._getLazyChart()()
		return lambda:chart.getAlbums()

	#to display the artists
	def getLazyArtists(self):
		chart = self._getLazyChart()()
		return lambda:chart.getArtists()

	#to display the playlists
	def getLazyPlaylists(self):
		chart = self._getLazyChart()()
		return lambda:chart.getPlaylists()

	#to display the tracks
	def getListItems(self):
		chart = self._getLazyChart()()
		listItems = []
		for track in chart.getTracks():
			try:
				listItem = xbmcgui.ListItem("%s - %s" % (track.artist.name, track.title), thumbnailImage=track.album.cover_big)
				listItem.setProperty('IsPlayable', 'true')
				listItem.setArt({'fanart': track.artist.picture_big})
				self.addItemTrackInfo(listItem, track)
				listItems.append((self.getUrl("/%d" % track.id), listItem, False))
			except:
				pass
		return listItems

	#to diplay first menu
	def _showChartMenu(self):
		items = {
			3005 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.sceneRouter.imagesPath, "genre-%s.png" % self.scene.sceneRouter.color)),
				"url" : self.getUrl('/tracks')
			},
			3006 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.sceneRouter.imagesPath, "myalbums-%s.png" % self.scene.sceneRouter.color)),
				"url" : self.getUrl('/albums')
			},
			3007 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.sceneRouter.imagesPath, "myartists-%s.png" % self.scene.sceneRouter.color)),
				"url" : self.getUrl('/artists')
			},
			3008 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.sceneRouter.imagesPath, "myplaylists-%s.png" % self.scene.sceneRouter.color)),
				"url" : self.getUrl('/playlists')
			}
		}
		listItems = []
		for item in items:
			listItem = xbmcgui.ListItem(self.scene.sceneRouter.language(item), iconImage=items[item]["image"])
			listItem.setArt({'fanart': self.scene.sceneRouter.fanartPath})
			listItems.append((items[item]["url"], listItem, True))
		xbmcplugin.addDirectoryItems(self.scene.sceneRouter.addonHandle, listItems)

	def show(self):
		print "Show ChartView"
		self._showChartMenu()