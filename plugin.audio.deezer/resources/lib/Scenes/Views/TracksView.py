from .View import View

import xbmcgui
import xbmcplugin

class TracksView(View):
	def __init__(self, scene, viewRouter, parentView = None):
		super(TracksView, self).__init__(scene, viewRouter, "tracks", parentView)

	def _playTrack(self):
		url = self.scene.sceneRouter.api.getStreamingUrl(id=self.id, type='track')
		item = xbmcgui.ListItem(path=url)
		xbmcplugin.setResolvedUrl(self.scene.sceneRouter.addonHandle, True, listitem=item)

	def _showTracks(self):
		listItems = self.parentView.getListItems()
		xbmcplugin.addDirectoryItems(self.scene.sceneRouter.addonHandle, listItems, len(listItems))
		xbmcplugin.setContent(self.scene.sceneRouter.addonHandle, 'songs')

	def show(self):
		print "Show TracksView"
		if self.id is not None:
			self._playTrack()
		else:
			self._showTracks()