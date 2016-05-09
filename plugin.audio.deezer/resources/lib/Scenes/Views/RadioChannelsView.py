from .View import View

import xbmcgui
import xbmcplugin

class RadioChannelsView(View):
	def __init__(self, scene, viewRouter, parentView = None):
		super(RadioChannelsView, self).__init__(scene, viewRouter, "radiochannels", parentView)
		self.lazyRadios = None

	def setLazyRadios(self, lazyRadios):
		self.lazyRadios = lazyRadios

	def _getLazyRadios(self):
		#try to get lazy radios from the parent if none are set
		if self.lazyRadios is None:
			self.lazyRadios = self.parentView.getLazyRadios()
		return self.lazyRadios

	def _showRadios(self):
		self.radios = self._getLazyRadios()()
		listItems = []

		for i in range(0, len(self.radios)):
			try:
				radio = self.radios[i]
				listItem = xbmcgui.ListItem(radio.title, thumbnailImage=radio.picture_big)
				listItem.setArt({'fanart': self.scene.sceneRouter.fanartPath})
				listItems.append((self.getUrl("/%d/tracks" % i), listItem, True))
			except:
				pass
		xbmcplugin.addDirectoryItems(self.scene.sceneRouter.addonHandle, listItems)

	def getListItems(self):
		self.radios = self._getLazyRadios()()
		radios = self.radios[self.id]
		listItems = []

		for track in radios.getTracks():
			try:
				listItem = xbmcgui.ListItem("%s - %s" % (track.artist.name, track.title), thumbnailImage=track.album.cover_big)
				listItem.setProperty('IsPlayable', 'true')
				listItem.setArt({'fanart': track.artist.picture_big})
				self.addItemTrackInfo(listItem, track)
				listItems.append((self.getUrl("/%d" % track.id), listItem, False))
			except:
				pass
		return listItems

	def show(self):
		print "Show RadioChannelsView"
		self._showRadios()